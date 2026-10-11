#!/usr/bin/env python3
"""Noon Egypt, Soft Drinks by popularity: the top products read from the page by Claude.

Replaces the crawlerbros/noon-scraper Apify actor, which was removed from the Apify Store
(404 "Actor was not found" on 11 Oct 2026).

How it works:
1. curl fetches the listing page. Noon stalls HTTP/1.1 clients, so this needs curl's HTTP/2.
2. The page is reduced to its visible text, with a [SKU ...] marker where each product's link starts.
3. Claude returns the products as JSON that follows a fixed schema.
4. Every value is checked against the page:
   - the SKU must be one of the page's product links;
   - the rank is the product's position on the page;
   - the price, rating, rating count and stock warning must appear in that product's own text.
   A value that can't be found there is dropped, never guessed.

Usage (needs ANTHROPIC_API_KEY, or an `ant auth login` profile):
  data/.venv/bin/python data/noon_llm.py          # fetch, extract, print, save the raw page and result
"""
import datetime, html, json, os, re, subprocess, sys

URL = "https://www.noon.com/egypt-en/grocery-store/beverages-16314/soft-drinks/?sort%5Bby%5D=popularity&sort%5Bdir%5D=desc"
MODEL = "claude-opus-5-5"
USD_PER_MTOK = {"input": 4.0, "output": 20.0}   # claude-opus-5-5, checked 11 Oct 2026
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "stores", "noon_llm")

SYSTEM = """You read the visible text of one noon.com Egypt category page: Soft Drinks, sorted by popularity.
Each product starts at a [SKU Z...Z] marker; everything up to the next marker belongs to that product.
Return the first {limit} products in page order. For each one:
- sku: exactly as written in its marker
- name: the product name as shown
- price_egp: the current selling price in EGP, as a number. Not the price per 100 ml, and not a crossed-out old price
- rating: the star rating shown (for example 4.4), or null
- ratings: the number of ratings shown next to the star rating (for example 157), or null
- stock_text: a stock warning exactly as written (for example "Only 9 left in stock"), or null
Use only what the page says. When a value isn't shown, use null."""

NULLABLE = lambda t: {"anyOf": [{"type": t}, {"type": "null"}]}
SCHEMA = {
    "type": "object",
    "properties": {"products": {"type": "array", "items": {
        "type": "object",
        "properties": {"sku": {"type": "string"}, "name": {"type": "string"}, "price_egp": NULLABLE("number"),
                       "rating": NULLABLE("number"), "ratings": NULLABLE("integer"), "stock_text": NULLABLE("string")},
        "required": ["sku", "name", "price_egp", "rating", "ratings", "stock_text"],
        "additionalProperties": False}}},
    "required": ["products"],
    "additionalProperties": False,
}


def fetch(url=URL):
    r = subprocess.run(["curl", "-s", "--http2", "--compressed", "-m", "40", "-w", "\n%{http_code}",
                        "-H", "User-Agent: " + UA, "-H", "Accept: text/html,application/xhtml+xml",
                        "-H", "Accept-Language: en-US,en;q=0.9", url], capture_output=True)
    body, _, code = r.stdout.decode("utf-8", "replace").rpartition("\n")
    if r.returncode or code != "200":
        raise RuntimeError(f"Noon page fetch failed (curl exit {r.returncode}, HTTP {code or 'none'})")
    return body


def page_text(page):
    """Visible text of the listing, with a [SKU ...] marker where each product's link starts."""
    s = re.sub(r"(?is)<(script|style|svg|noscript)\b.*?</\1>", " ", page)
    s = re.sub(r'(?i)<a\b[^>]*href="/egypt-en/[^"]*?/(Z[0-9A-Z]+Z)/p/[^"]*"[^>]*>', r" [SKU \1] ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def segments(text):
    """{sku: that product's own text} and the SKUs in page order."""
    parts = re.split(r"\[SKU (Z[0-9A-Z]+Z)\]", text)
    seg, order = {}, []
    for sku, body in zip(parts[1::2], parts[2::2]):
        if sku not in seg:
            order.append(sku)
        seg[sku] = seg.get(sku, "") + " " + body
    return seg, order


def extract(text, limit, client):
    resp = client.beta.messages.create(
        model=MODEL, max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        system=SYSTEM.format(limit=limit),
        messages=[{"role": "user", "content": text}],
    )
    if resp.stop_reason == "refusal":
        raise RuntimeError("Claude declined to read the page" + (f" ({resp.stop_details.category})" if resp.stop_details and resp.stop_details.category else ""))
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("Claude's answer was cut off (max_tokens); nothing saved")
    out = json.loads(next(b.text for b in resp.content if b.type == "text"))
    u = resp.usage
    cost = (u.input_tokens * USD_PER_MTOK["input"] + u.output_tokens * USD_PER_MTOK["output"]) / 1e6
    return out["products"], {"model": resp.model, "request_id": resp._request_id, "input_tokens": u.input_tokens,
                             "output_tokens": u.output_tokens, "usd": round(cost, 4)}


def _nums(s):
    """Every number shown in s; "1.2K" also counts as 1200."""
    out = set()
    for n, k in re.findall(r"(\d[\d,]*(?:\.\d+)?)\s*([Kk])?(?![\w])", s):
        v = float(n.replace(",", ""))
        out |= {v, round(v * 1000)} if k else {v}
    return out


def _prices(s):
    """Prices shown as "EGP x", leaving out per-100 ml prices ("EGP 6.67/100ml")."""
    return {float(n.replace(",", "")) for n in re.findall(r"EGP\s*(\d[\d,]*(?:\.\d+)?)(?![\d.,]|\s*/\s*100)", s)}


def check(rows, seg, order, limit):
    """Keep only what the page itself shows; rank comes from the page order, not from Claude."""
    out, notes, seen = [], [], set()
    for x in rows:
        sku = x.get("sku")
        if sku not in seg or sku in seen:
            notes.append(f"dropped {sku!r}: not a product on the page" if sku not in seg else f"dropped duplicate {sku}")
            continue
        seen.add(sku)
        s, row = seg[sku], dict(x)
        shown = {"price_egp": _prices(s), "rating": _nums(s), "ratings": _nums(s)}
        for k, lo, hi in (("price_egp", 0.01, 100000), ("rating", 0.1, 5), ("ratings", 0, 10_000_000)):
            v = row.get(k)
            if v is not None and not (lo <= v <= hi and float(v) in shown[k]):
                notes.append(f"{sku}: {k} {v} isn't shown for this product, left empty")
                row[k] = None
        st = row.get("stock_text")
        if st and st.lower() not in s.lower():
            notes.append(f"{sku}: stock text {st!r} isn't shown for this product, left empty")
            row["stock_text"] = st = None
        row["stock"] = "out" if st and re.search(r"out of stock", st, re.I) else "low" if st and re.search(r"only \d+ left", st, re.I) else "in"
        row["rank"] = order.index(sku) + 1
        out.append(row)
    out.sort(key=lambda r: r["rank"])
    expected = order[:limit]
    missed = [s for s in expected if s not in seen]
    if missed:
        notes.append(f"{len(missed)} of the top {limit} products weren't returned: {', '.join(missed)}")
    return [r for r in out if r["sku"] in expected], notes


def top_products(limit=20, client=None, save=True, url=URL):
    """The top `limit` Soft Drinks on Noon by popularity, as checked rows plus run notes."""
    import anthropic
    page = fetch(url)
    text = page_text(page)
    seg, order = segments(text)
    if len(order) < limit:
        raise RuntimeError(f"Only {len(order)} products found on the Noon page; the page layout may have changed")
    rows, meta = extract(text, limit, client or anthropic.Anthropic())
    rows, notes = check(rows, seg, order, limit)
    meta.update(url=url, products_on_page=len(order), notes=notes)
    if save:
        d = os.path.join(RAW, datetime.date.today().isoformat())
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "page.html"), "w", encoding="utf-8").write(page)
        json.dump({"meta": meta, "rows": rows}, open(os.path.join(d, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return rows, meta


if __name__ == "__main__":
    import anthropic
    try:
        rows, meta = top_products()
    except anthropic.AuthenticationError:
        sys.exit("The Anthropic API key was rejected. Check ANTHROPIC_API_KEY.")
    except anthropic.CredentialsError:
        sys.exit("No Anthropic credentials found. Set ANTHROPIC_API_KEY, or run `ant auth login`.")
    except anthropic.RateLimitError:
        sys.exit("Rate limited by the Anthropic API. Try again in a minute.")
    except anthropic.APIStatusError as e:
        sys.exit(f"Anthropic API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        sys.exit("Couldn't reach the Anthropic API. Check the internet connection.")
    for r in rows:
        print(f"#{r['rank']:>2} {r['sku']} EGP {r['price_egp']} | {r['rating']}★ ({r['ratings']}) | {r['stock']}{' · ' + r['stock_text'] if r['stock_text'] else ''} | {r['name'][:60]}")
    for n in meta["notes"]:
        print("note:", n)
    print(f"{meta['model']} · {meta['input_tokens']} in / {meta['output_tokens']} out tokens · about USD {meta['usd']}")
