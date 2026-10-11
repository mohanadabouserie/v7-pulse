"""Real posts for the Rumors & attacks page (11 Oct 2026). Spend cap USD 1.50 for the whole pull.
Usage: python3 collect.py test   (3 items per actor)   |   python3 collect.py full   |   python3 collect.py extra"""
import json, os, sys, time, urllib.request, urllib.error
TOK = os.environ['APIFY_API_TOKEN']; HERE = os.path.dirname(os.path.abspath(__file__)); CAP = 1.50
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False, "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
X = 'kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest'; FB = 'scraper_one~facebook-posts-search'
TT = 'clockworks~tiktok-scraper'; IG = 'apify~instagram-hashtag-scraper'
NOISE = ' -هافال -Haval -Raptor -midjourney -Vivo -Honor'
def x(q, n): return (X, {"twitterContent": q + NOISE, "maxItems": n, "queryType": "Latest"}, n)
def fb(q, n): return (FB, {"query": q, "resultsCount": n, "searchType": "latest"}, n)
TESTS = {'t_x': x('V7 مشروب', 3), 't_fb': fb('مشروب V7', 3), 't_tt': (TT, dict(NODL, searchQueries=["V7 مشروب"], resultsPerPage=3), 3),
         't_ig': (IG, {"hashtags": ["v7egypt"], "keywordSearch": False, "resultsLimit": 3}, 3)}
FULL = {
 # every rumor theme on the fact sheet, plus general V7 talk where rumors also show up
 'x_owner':   x('(V7 OR "في كولا" OR "ڤي كولا") (كوكاكولا OR "كوكا كولا" OR اتباعت OR باعوها OR اشتروها OR صاحبها OR صهيوني OR اسرائيلي OR مقاطعة)', 60),
 'x_quality': x('V7 (تسمم OR مضر OR مضرة OR بايظ OR وحش OR مغشوش OR "مش صحي" OR سرطان OR مواد)', 50),
 'x_malt':    x('V7 (شعير OR مالت OR malt) (كحول OR alcohol OR حرام)', 30),
 'x_price':   x('(V7 OR "في كولا") (سعر OR غلي OR غليت OR "بقت ب" OR جنيه)', 50),
 'x_give':    x('V7 (مسابقة OR giveaway OR نصب OR مزيفة OR fake OR هدية)', 40),
 'x_general': x('(V7 OR "ڤي سڤن" OR "في سفن") (مشروب OR كانز OR صودا OR كولا OR رمان OR بيناكولادا)', 80),
 'fb_owner':  fb('في كولا اتباعت', 15), 'fb_coke': fb('V7 كوكاكولا', 15), 'fb_quality': fb('V7 تسمم', 12),
 'fb_malt':   fb('V7 شعير كحول', 10), 'fb_give': fb('مسابقة V7', 15), 'fb_general': fb('ڤي سڤن', 20),
 'ig_v7':     (IG, {"hashtags": ["v7egypt", "vcola", "في_كولا"], "keywordSearch": False, "resultsLimit": 15}, 45),
 'tt_rumor':  (TT, dict(NODL, searchQueries=["V7 مقاطعة", "في كولا كوكاكولا", "V7 مشروب مضر"], resultsPerPage=8), 24),
}
# 11 Oct, second pass: the first pull found the news and V7's denial of the Coca-Cola sale rumor (2-4 May 2024)
# but not the posts that spread it, so search those weeks directly.
EXTRA = {
 'x_coke2024': x('(V7 OR "في كولا" OR "ڤي كولا" OR "ڤي سڤن" OR "في سفن") (كوكاكولا OR "كوكا كولا" OR "coca cola" OR اتباعت OR اشترت OR استحوذت) since:2024-04-20 until:2024-05-25', 40),
}
def usage():
    r = urllib.request.Request('https://api.apify.com/v2/users/me/limits', headers={'Authorization': 'Bearer ' + TOK})
    return json.load(urllib.request.urlopen(r, timeout=60))['data']['current']['monthlyUsageUsd']
def run(name, actor, body, cap, max_usd):
    url = f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd={max_usd:.3f}&maxItems={cap}'
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json'})
    try:
        items = json.load(urllib.request.urlopen(req, timeout=330))
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}: {e.read()[:200]!r}', 0
    json.dump({'input': body, 'items': items}, open(os.path.join(HERE, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return f'{len(items)} items', len(items)
if __name__ == '__main__':
    plan = {'test': TESTS, 'full': FULL, 'extra': EXTRA}[sys.argv[1]]
    start = usage(); spent_before = start
    log = open(os.path.join(HERE, 'run.log'), 'a', encoding='utf-8')
    for name, (actor, body, cap) in plan.items():
        left = CAP - (usage() - start) if sys.argv[1] == 'full' else 0.10   # 'extra' runs alone, capped at USD 0.10
        per_run = {X: 0.08, FB: 0.15, IG: 0.15, TT: 0.50}[actor]   # TikTok's actor won't run with a cap under USD 0.50
        if left < per_run:
            print(f'{name}: skipped, only ${left:.2f} of the cap left'); log.write(f'{name}: skipped, cap\n'); continue
        msg, n = run(name, actor, body, cap, per_run)
        time.sleep(2); now = usage()
        line = f'{name:10s} {actor.split("~")[0]:14s} {msg:12s} run cost ~${now - spent_before:.4f} | total ${now - start:.4f}'
        print(line); log.write(line + '\n'); spent_before = now
