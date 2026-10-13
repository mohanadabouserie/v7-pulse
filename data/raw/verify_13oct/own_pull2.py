"""13 Oct 2026, deeper pass, part 2: YouTube likes, comments and exact dates for V7's latest videos; the Facebook page's
follower count; and the first comments on the V Orange launch (11 Oct) on Facebook and Instagram, to check what people
ask about a new product. Capped runs; total cap USD 0.18.  Usage (token in the environment): python3 own_pull2.py"""
import json, os, time, urllib.request, urllib.error
TOK = os.environ['APIFY_API_TOKEN']; HERE = os.path.dirname(os.path.abspath(__file__)); CAP = 0.18
YT = [x['url'] for x in json.load(open(os.path.join(HERE, 'yt_channel.json'), encoding='utf-8'))['items']]
RUNS = {
 'yt_videos':   ('streamers~youtube-scraper', {"startUrls": [{"url": u} for u in YT], "maxResults": 1, "maxResultsShorts": 1, "maxResultStreams": 0}, 12, 0.08),
 'fb_pageinfo': ('apify~facebook-pages-scraper', {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}]}, 1, 0.02),
 'fb_orange':   ('apify~facebook-comments-scraper', {"startUrls": [{"url": "https://www.facebook.com/reel/1044722265279133/"}], "resultsLimit": 40, "includeNestedComments": False}, 40, 0.05),
 'ig_orange':   ('apify~instagram-comment-scraper', {"directUrls": ["https://www.instagram.com/p/DeWgI0dD2Ar/"], "resultsLimit": 30}, 30, 0.04),
}
def usage():
    r = urllib.request.Request('https://api.apify.com/v2/users/me/limits', headers={'Authorization': 'Bearer ' + TOK})
    return json.load(urllib.request.urlopen(r, timeout=60))['data']['current']['monthlyUsageUsd']
start = usage(); log = open(os.path.join(HERE, 'run.log'), 'a', encoding='utf-8')
for name, (actor, body, cap, max_usd) in RUNS.items():
    if usage() - start + max_usd > CAP:
        print(name, 'skipped: cap'); continue
    url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd={max_usd}&maxItems={cap}'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json'})
    t = time.time()
    try:
        items = json.load(urllib.request.urlopen(req, timeout=320)); msg = f'{len(items)} items'
        json.dump({'input': body, 'items': items}, open(os.path.join(HERE, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except urllib.error.HTTPError as e:
        msg = f'HTTP {e.code}: {e.read()[:200]!r}'
    time.sleep(3)
    line = f'{name:12s} {msg:14s} {time.time()-t:4.0f}s  total so far ~${usage()-start:.4f}'
    print(line, flush=True); log.write(line + '\n')
