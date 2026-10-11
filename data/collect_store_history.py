#!/usr/bin/env python3
"""Daily store check for V7 Pulse: price, stock, ratings and ranks on Amazon.eg, Carrefour Egypt and Noon.

Writes one file per day to data/store_history/YYYY-MM-DD.json, in the same format as the first real
snapshots (2026-10-04 and 2026-10-05). The dashboard's Stock, Ratings and Rankings views read these.

Noon's top 20 comes from its Soft Drinks page read by Claude (data/noon_llm.py), since the
crawlerbros/noon-scraper actor was removed from Apify on 11 Oct 2026.

Usage (the project's own Python, data/.venv, has the Anthropic SDK):
  data/.venv/bin/python data/collect_store_history.py --dry-run   # show what would run and the estimated cost
  data/.venv/bin/python data/collect_store_history.py             # run it (needs APIFY_API_TOKEN and ANTHROPIC_API_KEY)
  data/.venv/bin/python data/collect_store_history.py --v7-only   # skip competitor listings

Schedule it once a day (cron on the server, or an Apify schedule). Every run is capped with
maxItems and maxTotalChargeUsd, so it can't spend more than the estimate.
"""
import argparse, datetime, glob, json, os, re, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "store_history")
API = "https://api.apify.com/v2"

PRICE = {  # USD per item, free-tier prices checked on 5 Oct 2026
    "amazon": 0.005, "carrefour_start": 0.01, "carrefour": 0.002,
    "noon_rating": 0.0002,
    "noon_llm": 0.08,  # one Claude call (claude-opus-5-5) reading Noon's page, about 7K tokens in and 2K out
}


def latest_snapshot():
    files = sorted(glob.glob(os.path.join(OUT, "*.json")))
    if not files:
        raise SystemExit("No earlier snapshot in data/store_history to copy the tracked listings from.")
    listings = []
    for f in files[-2:]:                       # the last two days together hold V7 and competitor listings
        listings += json.load(open(f, encoding="utf-8"))["listings"]
    return listings


def plan(v7_only):
    L = latest_snapshot()
    keep = lambda x: (not v7_only) or x.get("company") == "V7"
    amazon = sorted({x["url"] for x in L if x["store"] == "Amazon.eg" and x.get("url") and keep(x)})
    carrefour = sorted({x["url"] for x in L if x["store"] == "Carrefour" and x.get("url") and keep(x)})
    noon_skus = sorted({x["sku"] for x in L if x["store"] == "Noon" and x.get("sku") and keep(x)})
    cost = (len(amazon) * PRICE["amazon"]
            + PRICE["carrefour_start"] + len(carrefour) * PRICE["carrefour"]
            + PRICE["noon_llm"] + len(noon_skus) * PRICE["noon_rating"])
    return {"amazon": amazon, "carrefour": carrefour, "noon_skus": noon_skus, "cost": cost}


def run(actor, body, max_items, max_usd, token, wait=600):
    q = f"?maxItems={max_items}&maxTotalChargeUsd={max_usd:.3f}"
    req = urllib.request.Request(f"{API}/acts/{actor}/runs{q}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    run_id = json.load(urllib.request.urlopen(req, timeout=60))["data"]["id"]
    t = time.time()
    while True:
        time.sleep(10)
        r = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/actor-runs/{run_id}", headers={"Authorization": "Bearer " + token}), timeout=60))["data"]
        if r["status"] in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT") or time.time() - t > wait:
            break
    items = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}/datasets/{r['defaultDatasetId']}/items?clean=1", headers={"Authorization": "Bearer " + token}), timeout=120))
    return items if isinstance(items, list) else []


def collect(p, token):
    from noon_llm import top_products
    today = datetime.date.today().isoformat()
    listings = []
    top, meta = top_products(20)               # first, so a problem here stops the run before any Apify spend
    for n in meta["notes"]:
        print("Noon note:", n)
    if p["amazon"]:
        for x in run("junglee~Amazon-crawler", {"categoryOrProductUrls": [{"url": u} for u in p["amazon"]], "maxItemsPerStartUrl": 1, "language": "en"},
                     len(p["amazon"]), len(p["amazon"]) * PRICE["amazon"] + 0.01, token):
            ranks = x.get("bestsellerRanks") or []
            cat = next((b for b in ranks if b.get("category") != "Grocery"), {})
            price = x.get("price", {}).get("value") if isinstance(x.get("price"), dict) else x.get("price")
            text = x.get("inStockText") or ""
            listings.append({"store": "Amazon.eg", "name": x.get("title"), "url": (x.get("url") or "").split("?")[0], "price_egp": price,
                             "stock": "out" if x.get("inStock") is False else ("low" if re.search(r"only \d+ left", text, re.I) else "in"), "stock_text": text or None,
                             "rating": x.get("stars"), "ratings": x.get("reviewsCount"), "bought_last_month": x.get("monthlyPurchaseVolume"),
                             "rank": cat.get("rank"), "rank_category": cat.get("category")})
    if p["carrefour"]:
        for x in run("blackfalcondata~carrefour-maf-scraper", {"productUrls": p["carrefour"], "market": "mafegy", "language": "en", "compact": True},
                     len(p["carrefour"]), PRICE["carrefour_start"] + len(p["carrefour"]) * PRICE["carrefour"] + 0.01, token):
            listings.append({"store": "Carrefour", "name": x.get("name"), "url": x.get("url"), "price_egp": x.get("price"),
                             "regular_egp": x.get("regularPrice"), "stock": "in" if x.get("available") else "out"})
    noon = [{"store": "Noon", "name": x["name"], "sku": x["sku"], "price_egp": x["price_egp"], "stock": x["stock"],
             "stock_text": x["stock_text"], "rating": x["rating"], "ratings": x["ratings"],
             "rank": x["rank"], "rank_category": "Soft Drinks, by popularity"} for x in top]
    skus = {x["sku"] for x in top}
    # ratings from the product pages: tracked listings outside the top 20, and top-20 rows the page showed no rating for
    want = sorted({x["sku"] for x in noon if x["rating"] is None} | {s for s in p["noon_skus"] if s not in skus})
    rated = {y.get("sku"): (y.get("product_rating") or {}) for y in run("scrapesmith~noon-com-product-seller-scraper", {"productUrls": want, "country": "egypt-en"},
                                                                      len(want), len(want) * PRICE["noon_rating"] + 0.01, token)} if want else {}
    for row in noon:
        r = rated.get(row["sku"])
        if r and row["rating"] is None:
            row["rating"], row["ratings"] = r.get("value"), r.get("count")
    for s in p["noon_skus"]:                   # a tracked Noon listing that fell out of the top 20 still gets a row
        if s not in skus:
            r = rated.get(s) or {}
            noon.append({"store": "Noon", "sku": s, "rating": r.get("value"), "ratings": r.get("count"), "stock": "in" if r else "na"})
    listings += noon
    snap = {"date": today, "sources": ["junglee/Amazon-crawler", "blackfalcondata/carrefour-maf-scraper",
                                       f"noon.com Soft Drinks page, read by {meta['model']}", "scrapesmith/noon-com-product-seller-scraper"],
            "listings": listings}
    path = os.path.join(OUT, today + ".json")
    json.dump(snap, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"saved {len(listings)} listings to {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--v7-only", action="store_true")
    a = ap.parse_args()
    p = plan(a.v7_only)
    print(f"Amazon.eg listings: {len(p['amazon'])} | Carrefour listings: {len(p['carrefour'])} | Noon: top 20 read by Claude + {len(p['noon_skus'])} tracked SKUs")
    print(f"Estimated cost: about USD {p['cost']:.2f} a day, USD {p['cost'] * 30:.2f} a month")
    if not a.dry_run:
        token = os.environ.get("APIFY_API_TOKEN")
        if not token:
            raise SystemExit("Set APIFY_API_TOKEN first.")
        if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("ANTHROPIC_AUTH_TOKEN") and not os.path.isdir(os.path.expanduser("~/.config/anthropic")):
            raise SystemExit("Set ANTHROPIC_API_KEY first (Noon is read by Claude).")
        collect(p, token)
