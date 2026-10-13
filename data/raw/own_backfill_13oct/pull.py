"""13 Oct 2026: backfill V7 Egypt's own posts to the dashboard's full 180 days (16 Apr to 12 Oct 2026). The 13 Oct pulls in
../verify_13oct cover Facebook from 21 Jul, Instagram from 17 Aug, TikTok from 2 Aug and YouTube from 26 Jul; this fetches the
rest. Date filters keep each run to the missing window where the actor allows it. Every run has a cost cap.
Usage (token in the environment): python3 pull.py test | full"""
import json, os, sys, time, urllib.request, urllib.error
TOK = os.environ['APIFY_API_TOKEN']; HERE = os.path.dirname(os.path.abspath(__file__))
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False, "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
FB = {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "onlyPostsNewerThan": "2026-04-16", "onlyPostsOlderThan": "2026-07-21"}
TT = dict(NODL, profiles=["v7.egypt"], profileSorting="latest", oldestPostDateUnified="2026-04-16", newestPostDate="2026-08-01")
RUNS = {
 'test': {
  'fb_test': ('apify~facebook-posts-scraper', dict(FB, resultsLimit=3), 3, 0.03),
  'tt_test': ('clockworks~tiktok-scraper', dict(TT, resultsPerPage=3), 3, 0.50),   # this actor refuses caps under 0.50; 3 results cost about 0.016
 },
 'full': {
  'fb_backfill': ('apify~facebook-posts-scraper', dict(FB, resultsLimit=30), 30, 0.20),
  'tt_backfill': ('clockworks~tiktok-scraper', dict(TT, resultsPerPage=30), 30, 0.50),   # 30 results at most: about 0.15
  'ig_backfill': ('apify~instagram-post-scraper', {"username": ["v7egypt"], "resultsLimit": 45, "onlyPostsNewerThan": "2026-04-16"}, 45, 0.13),
  'yt_backfill': ('streamers~youtube-channel-scraper', {"startUrls": [{"url": "https://www.youtube.com/@V7Egypt"}], "maxResults": 30, "maxResultsShorts": 30, "maxResultStreams": 0, "oldestPostDate": "2026-04-16"}, 60, 0.06),
 },
}
mode = sys.argv[1]; log = open(os.path.join(HERE, 'run.log'), 'a', encoding='utf-8')
for name, (actor, body, cap, max_usd) in RUNS[mode].items():
    if os.path.exists(os.path.join(HERE, name + '.json')):
        print(name, 'already pulled'); continue
    url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd={max_usd}&maxItems={cap}'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json'})
    t = time.time()
    try:
        items = json.load(urllib.request.urlopen(req, timeout=320)); msg = f'{len(items)} items'
        json.dump({'input': body, 'items': items}, open(os.path.join(HERE, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except urllib.error.HTTPError as e:
        msg = f'HTTP {e.code}: {e.read()[:200]!r}'
    line = f'{time.strftime("%Y-%m-%d %H:%M")}  {name:12s} {msg:14s} {time.time()-t:4.0f}s'
    print(line, flush=True); log.write(line + '\n')
