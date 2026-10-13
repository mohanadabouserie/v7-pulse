"""13 Oct 2026: checks for the page-by-page review. Tiny runs, each with a cost cap; total cap USD 0.30.
Usage (from this folder, token in the environment): python3 run.py"""
import json, os, sys, time, urllib.request, urllib.error
TOK = os.environ['APIFY_API_TOKEN']; HERE = os.path.dirname(os.path.abspath(__file__)); CAP = 0.30
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False, "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
RUNS = {
 # who answers comments on V7's Facebook posts, and how fast (Cream Soda reel, 10 Sep)
 'fb_replies': ('apify~facebook-comments-scraper', {"startUrls": [{"url": "https://www.facebook.com/reel/1583808776758074/"}], "resultsLimit": 8, "includeNestedComments": True}, 16, 0.08),
 # the same for Instagram (Cream Soda post, 98 comments)
 'ig_replies': ('apify~instagram-comment-scraper', {"directUrls": ["https://www.instagram.com/p/DdG_sWYEi_T/"], "resultsLimit": 8, "includeNestedComments": True}, 16, 0.08),
 # V7's latest TikTok videos with views and comment counts, and a few comments
 'tt_profile': ('clockworks~tiktok-scraper', dict(NODL, profiles=["v7.egypt"], resultsPerPage=5, commentsPerPost=4), 30, 0.50),
 # how many posts about V7 X has had in the last week
 'x_week': ('kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest', {"twitterContent": "(V7 OR \"في كولا\" OR \"ڤي كولا\" OR \"ڤي سڤن\") (مشروب OR كانز OR كولا OR رمان OR بيناكولادا OR مالت OR شعير OR صودا OR سعر) since:2026-10-06 -هافال -Haval -Raptor -midjourney", "maxItems": 20, "queryType": "Latest"}, 20, 0.05),
}
def usage():
    r = urllib.request.Request('https://api.apify.com/v2/users/me/limits', headers={'Authorization': 'Bearer ' + TOK})
    return json.load(urllib.request.urlopen(r, timeout=60))['data']['current']['monthlyUsageUsd']
start = usage(); log = open(os.path.join(HERE, 'run.log'), 'a', encoding='utf-8')
for name, (actor, body, cap, max_usd) in RUNS.items():
    if usage() - start + max_usd > CAP + 0.45:   # TikTok's cap must be >= 0.50, its real charge is a few cents
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
    line = f'{name:11s} {msg:14s} {time.time()-t:4.0f}s  total so far ~${usage()-start:.4f}'
    print(line, flush=True); log.write(line + '\n')
