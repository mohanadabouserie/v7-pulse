import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK = os.environ['APIFY_API_TOKEN']
OUT = sys.argv[1]
tests = {
 'tiktok':        ('clockworks~tiktok-scraper', {"searchQueries": ["V7 مشروب", "v7 cream soda"], "resultsPerPage": 3,
                    "shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False,
                    "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}),
 'youtube':       ('streamers~youtube-scraper', {"searchQueries": ["V7 مشروب"], "maxResults": 2, "maxResultsShorts": 2, "maxResultStreams": 0}),
 'ig_hashtag':    ('apify~instagram-hashtag-scraper', {"hashtags": ["v7egypt"], "resultsLimit": 5}),
 'x_search':      ('kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest', {"twitterContent": "V7 (مشروب OR صودا OR كريم)", "maxItems": 10, "queryType": "Latest"}),
 'fb_search_loc': ('scraper_one~facebook-posts-search', {"query": "V7", "location": "Cairo, Egypt", "resultsCount": 3}),
 'fb_page':       ('apify~facebook-pages-scraper', {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}]}),
}
only = sys.argv[2:] or list(tests)
def run(name):
    actor, body = tests[name]
    url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd=0.5&maxItems=12'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST',
                                 headers={'Authorization': f'Bearer {TOK}', 'Content-Type': 'application/json'})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=320) as r:
            items = json.load(r)
    except urllib.error.HTTPError as e:
        return name, f'HTTP {e.code}: {e.read()[:300]!r}', time.time()-t
    except Exception as e:
        return name, f'ERR {e}', time.time()-t
    json.dump({'input': body, 'items': items}, open(os.path.join(OUT, name + '.json'), 'w'), ensure_ascii=False, indent=1)
    return name, f'{len(items)} items', time.time()-t
with ThreadPoolExecutor(6) as ex:
    for name, res, dt in ex.map(run, only):
        print(f'{name:14s} {res}  ({dt:.0f}s)')
