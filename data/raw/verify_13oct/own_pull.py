"""13 Oct 2026, deeper pass: V7's own posts on every platform and its pages abroad, so Our content and
"V7 pages outside Egypt" can show real numbers. Capped runs; total cap USD 0.30.
Usage (token in the environment): python3 own_pull.py"""
import json, os, time, urllib.request, urllib.error
TOK = os.environ['APIFY_API_TOKEN']; HERE = os.path.dirname(os.path.abspath(__file__)); CAP = 0.30
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False, "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
RUNS = {
 'ig_profiles': ('apify~instagram-profile-scraper', {"usernames": ["v7egypt", "v7tunisia", "v7uzbekistan", "v7ldnuk", "drinkv7", "thehalaldrinksco"]}, 6, 0.06),
 'fb_page':     ('apify~facebook-posts-scraper', {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "resultsLimit": 15}, 15, 0.10),
 'tt_profile10':('clockworks~tiktok-scraper', dict(NODL, profiles=["v7.egypt"], resultsPerPage=10), 10, 0.50),
 'yt_channel':  ('streamers~youtube-channel-scraper', {"startUrls": [{"url": "https://www.youtube.com/@V7Egypt"}], "maxResults": 6, "maxResultsShorts": 6, "maxResultStreams": 0}, 12, 0.05),
}
def usage():
    r = urllib.request.Request('https://api.apify.com/v2/users/me/limits', headers={'Authorization': 'Bearer ' + TOK})
    return json.load(urllib.request.urlopen(r, timeout=60))['data']['current']['monthlyUsageUsd']
start = usage(); log = open(os.path.join(HERE, 'run.log'), 'a', encoding='utf-8')
for name, (actor, body, cap, max_usd) in RUNS.items():
    spent = usage() - start
    if spent + min(max_usd, 0.10) > CAP:
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
