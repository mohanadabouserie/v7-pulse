import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK = os.environ['APIFY_API_TOKEN']; OUT = sys.argv[1]
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False, "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
tests = {
 'x_general':  ('kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest', {"twitterContent": "V7 (مشروب OR صودا OR كريم OR بيناكولادا OR رمان OR مالت OR كانز) -هافال -Haval -Raptor", "maxItems": 30, "queryType": "Latest"}, 32),
 'x_avail':    ('kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest', {"twitterContent": "V7 (لاقي OR الاقي OR متوفر OR فين OR موجود OR بتتباع) -هافال -Haval", "maxItems": 20, "queryType": "Latest"}, 22),
 'tiktok':     ('clockworks~tiktok-scraper', dict(NODL, searchQueries=["V7 مشروب", "ڤي سڤن", "V7 كريم صودا"], resultsPerPage=4), 12),
 'fb_drink':   ('scraper_one~facebook-posts-search', {"query": "مشروب V7", "resultsCount": 8, "searchType": "latest"}, 8),
 'fb_arabic':  ('scraper_one~facebook-posts-search', {"query": "ڤي سڤن", "resultsCount": 6, "searchType": "latest"}, 6),
 'ig_keyword': ('apify~instagram-hashtag-scraper', {"hashtags": ["V7 مشروب"], "keywordSearch": True, "resultsLimit": 6}, 6),
}
def run(name):
    actor, body, cap = tests[name]
    url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd=0.5&maxItems={cap}'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization': f'Bearer {TOK}', 'Content-Type': 'application/json'})
    t = time.time()
    try:
        items = json.load(urllib.request.urlopen(req, timeout=320))
    except urllib.error.HTTPError as e:
        return name, f'HTTP {e.code}: {e.read()[:300]!r}', time.time() - t
    except Exception as e:
        return name, f'ERR {e}', time.time() - t
    json.dump({'input': body, 'items': items}, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    return name, f'{len(items)} items', time.time() - t
with ThreadPoolExecutor(6) as ex:
    for n, r, dt in ex.map(run, tests): print(f'{n:11s} {r} ({dt:.0f}s)')
