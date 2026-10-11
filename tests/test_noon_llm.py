"""data/noon_llm.py: Noon's top products read by Claude, checked against the page.

Runs the real Anthropic SDK request path against a local stand-in for the API (no key, no cost),
on the real Noon page saved on 11 Oct 2026. Run with the project's Python:
  data/.venv/bin/python tests/test_noon_llm.py
"""
import http.server, json, os, sys, threading
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "data"))
import anthropic
import noon_llm

PAGE = open(os.path.join(ROOT, "data/raw/stores/noon_llm_tests/2026-10-11_soft_drinks_popularity.html"), encoding="utf-8").read()
fails = 0
def check(name, ok, info=""):
    global fails
    if not ok: fails += 1
    print(("  ok " if ok else "FAIL ") + name + (" :: " + str(info) if info != "" else ""))

# what the stand-in API answers: a few right rows, and three wrong ones the checks must catch
ROWS = [
    {"sku": "Z8296195D9C08A7260DACZ", "name": "V7 Sparkling Drink Flavor Pink Lemonade 300 ml", "price_egp": 20, "rating": 4.4, "ratings": 157, "stock_text": None},
    {"sku": "Z128FA02BE5480FC920ABZ", "name": "Fanta Soft Drink With Orange Flavour 1.25L", "price_egp": 3.75, "rating": 3.4, "ratings": 5, "stock_text": None},      # per-100 ml price, not the price
    {"sku": "ZCAD2F4E26F7C9C26333CZ", "name": "Schweppes Pineapple Gold 320ml", "price_egp": 28.44, "rating": 5.0, "ratings": 6, "stock_text": "Only 2 left in stock"},  # warning isn't on the page
    {"sku": "ZFAKEFAKEFAKEFAKEFAKEZ", "name": "Made-up product", "price_egp": 15, "rating": 4.0, "ratings": 10, "stock_text": None},                                 # not on the page
    {"sku": "Z956CC311C04270D55EDEZ", "name": "V7 Vitamin Sparkling Drink - Pomegranate", "price_egp": 20, "rating": 4.4, "ratings": 211, "stock_text": "Only 9 left in stock"},
]
SEEN = {}
REPLY = {"stop_reason": "end_turn"}

class API(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["content-length"])))
        SEEN.update(path=self.path, beta=self.headers.get("anthropic-beta", ""), body=body)
        msg = {"id": "msg_test", "type": "message", "role": "assistant", "model": body["model"],
               "content": [{"type": "text", "text": json.dumps({"products": ROWS})}],
               "stop_reason": REPLY["stop_reason"], "stop_sequence": None,
               "usage": {"input_tokens": 6800, "output_tokens": 1900}}
        if REPLY["stop_reason"] == "refusal":
            msg["content"], msg["stop_details"] = [], {"type": "refusal", "category": None, "explanation": None}
        out = json.dumps(msg).encode()
        self.send_response(200); self.send_header("content-type", "application/json"); self.send_header("request-id", "req_test")
        self.send_header("content-length", str(len(out))); self.end_headers(); self.wfile.write(out)
    def log_message(self, *a): pass

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), API)
threading.Thread(target=srv.serve_forever, daemon=True).start()
client = anthropic.Anthropic(api_key="test-key", base_url=f"http://127.0.0.1:{srv.server_port}", max_retries=0)
noon_llm.fetch = lambda url=noon_llm.URL: PAGE          # the saved page instead of a live request

# the page itself
text = noon_llm.page_text(PAGE)
seg, order = noon_llm.segments(text)
check("38 products found on the page, one marker each", len(order) == 38 and text.count("[SKU ") == 38, len(order))
check("page order starts with V7 Pink Lemonade", order[0] == "Z8296195D9C08A7260DACZ")
check("page text is small enough for one call", len(text) < 40000, len(text))
check("per-100 ml price isn't counted as a price", 6.67 not in noon_llm._prices(seg["Z8296195D9C08A7260DACZ"]) and 20.0 in noon_llm._prices(seg["Z8296195D9C08A7260DACZ"]))

# the request the SDK sends
rows, meta = noon_llm.top_products(20, client=client, save=False)
b = SEEN["body"]
check("goes to the Messages API", SEEN["path"].startswith("/v1/messages"), SEEN["path"])
check("model is claude-opus-5-5", b["model"] == "claude-opus-5-5", b["model"])
check("server-side fallback on (beta header and fallbacks: default)", "server-side-fallback-2026-07-01" in SEEN["beta"] and b.get("fallbacks") == "default", (SEEN["beta"], b.get("fallbacks")))
check("structured output with the product schema", b["output_config"]["format"]["type"] == "json_schema" and b["output_config"]["format"]["schema"] == noon_llm.SCHEMA)
check("effort set to low, thinking not disabled, no sampling params", b["output_config"].get("effort") == "low" and "thinking" not in b and "temperature" not in b)
check("asks for the first 20 products", "first 20 products" in b["system"])
check("sends the page text with the SKU markers", "[SKU Z8296195D9C08A7260DACZ]" in b["messages"][0]["content"] and b["messages"][0]["role"] == "user")
check("cost worked out from usage", meta["input_tokens"] == 6800 and abs(meta["usd"] - (6800 * 4 + 1900 * 20) / 1e6) < 1e-4, meta["usd"])

# the checks against the page
by = {r["sku"]: r for r in rows}
check("made-up SKU dropped", "ZFAKEFAKEFAKEFAKEFAKEZ" not in by and any("not a product on the page" in n for n in meta["notes"]))
check("rank comes from the page order", [by[s]["rank"] for s in ("Z8296195D9C08A7260DACZ", "Z128FA02BE5480FC920ABZ", "ZCAD2F4E26F7C9C26333CZ", "Z956CC311C04270D55EDEZ")] == [1, 2, 3, 5])
check("per-100 ml price rejected", by["Z128FA02BE5480FC920ABZ"]["price_egp"] is None)
check("stock warning not on the page rejected", by["ZCAD2F4E26F7C9C26333CZ"]["stock_text"] is None and by["ZCAD2F4E26F7C9C26333CZ"]["stock"] == "in")
check("real low-stock warning kept", by["Z956CC311C04270D55EDEZ"]["stock_text"] == "Only 9 left in stock" and by["Z956CC311C04270D55EDEZ"]["stock"] == "low")
check("correct values kept", by["Z8296195D9C08A7260DACZ"]["price_egp"] == 20 and by["Z8296195D9C08A7260DACZ"]["rating"] == 4.4 and by["Z8296195D9C08A7260DACZ"]["ratings"] == 157)
check("missing products reported", any("weren't returned" in n for n in meta["notes"]))

# a declined or cut-off answer stops the run instead of saving bad data
for reason, words in (("refusal", "declined"), ("max_tokens", "cut off")):
    REPLY["stop_reason"] = reason
    try:
        noon_llm.top_products(20, client=client, save=False); got = None
    except RuntimeError as e:
        got = str(e)
    check(f"{reason} stops the run", got is not None and words in got, got)
REPLY["stop_reason"] = "end_turn"

# the daily collector's Noon step (Apify stubbed, nothing spent, snapshot written to a temp folder)
import tempfile, collect_store_history as cs
calls = []
def fake_run(actor, body, max_items, max_usd, token, wait=600):
    calls.append((actor, body))
    return [{"sku": s, "product_rating": {"value": 4.1, "count": 99}} for s in body.get("productUrls", [])] if "scrapesmith" in actor else []
cs.run = fake_run
orig = noon_llm.top_products
noon_llm.top_products = lambda limit=20, **k: orig(limit, client=client, save=False)
cs.OUT = tempfile.mkdtemp()
tracked_outside = "ZD5C1F8E0E6B6E6D0C2A0Z"
cs.collect({"amazon": [], "carrefour": [], "noon_skus": ["Z8296195D9C08A7260DACZ", tracked_outside]}, "token")
snap = json.load(open(os.path.join(cs.OUT, os.listdir(cs.OUT)[0]), encoding="utf-8"))
noon = [x for x in snap["listings"] if x["store"] == "Noon"]
ranked = [x for x in noon if x.get("rank")]
check("snapshot names Claude as the Noon source", any("read by claude-opus-5-5" in x for x in snap["sources"]) and not any("crawlerbros" in x for x in snap["sources"]), snap["sources"])
check("top rows carry rank, price, stock and the page's ratings", [x["rank"] for x in ranked] == [1, 2, 3, 5] and ranked[0]["ratings"] == 157 and ranked[3]["stock"] == "low")
scr = [b for a, b in calls if "scrapesmith" in a]
check("ratings actor only asked for the gaps", len(scr) == 1 and scr[0]["productUrls"] == [tracked_outside], scr)
out = [x for x in noon if x["sku"] == tracked_outside]
check("tracked product outside the top 20 still gets a row", len(out) == 1 and out[0]["rating"] == 4.1 and out[0]["stock"] == "in", out)
check("no Amazon or Carrefour run when there's nothing to check", all("scrapesmith" in a for a, b in calls))

srv.shutdown()
print("FAIL", fails)
