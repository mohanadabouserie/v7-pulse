import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK=os.environ['APIFY_API_TOKEN']; OUT=sys.argv[1]
tests = {
 'amazon_eg':   ('junglee~Amazon-crawler', {"categoryOrProductUrls": [{"url": "https://www.amazon.eg/s?k=V7+drink"}], "maxItemsPerStartUrl": 3, "countryCode": "EG"}, 3),
 'noon_eg':     ('scrapesmith~noon-com-product-seller-scraper', {"searchQueries": ["V7 drink"], "country": "egypt-en", "maxResults": 5}, 5),
 'talabat_eg':  ('thirdwatch~talabat-scraper', {"queries": ["koshary"], "country": "eg", "maxResults": 4, "scrapeMenu": True}, 4),
 'carrefour_eg':('blackfalcondata~carrefour-maf-scraper', {"query": "V7", "market": "mafegy", "maxResults": 5, "language": "en"}, 5),
 'jumia_eg':    ('headply~jumia-price-intelligence', {"searchKeyword": "V7 drink", "countries": ["eg"], "maxResults": 5}, 5),
}
only = sys.argv[2:] or list(tests)
def run(name):
    actor, body, cap = tests[name]
    url=f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd=0.5&maxItems={cap}'
    req=urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization':f'Bearer {TOK}','Content-Type':'application/json'})
    t=time.time()
    try: items=json.load(urllib.request.urlopen(req, timeout=320))
    except urllib.error.HTTPError as e: return name, f'HTTP {e.code}: {e.read()[:300]!r}', time.time()-t
    except Exception as e: return name, f'ERR {e}', time.time()-t
    json.dump({'input':body,'items':items}, open(f'{OUT}/{name}.json','w'), ensure_ascii=False, indent=1)
    return name, f'{len(items)} items', time.time()-t
with ThreadPoolExecutor(5) as ex:
    for n,r,dt in ex.map(run, only): print(f'{n:13s} {r} ({dt:.0f}s)')
