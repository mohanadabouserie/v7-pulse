"""Real data for every tab except Market (17 Oct 2026). The plan, the budget and the window are in PLAN.md.

Usage:  python3 collect.py <stage> [--force]
Stages, in order: test, own, comments, abroad, ugc
- Each run saves raw/<name>.json ({input, run, items}) and is skipped next time unless --force is given.
- Every run has a USD cap (Apify's maxTotalChargeUsd), and the whole collection stops at BUDGET, read from Apify's usage meter.
- The token is read from the environment only:  set -a; . ./.env.apify; set +a
"""
import json, os, pathlib, sys, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
TOK = os.environ['APIFY_API_TOKEN']
SINCE, UNTIL = '2026-04-20', '2026-10-16'       # 180 days: the dashboard's range
BUDGET = 14.00                                   # of the USD 19 a month; the rest is the reserve
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False,
        "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
FB_POSTS, FB_COMMENTS = 'apify~facebook-posts-scraper', 'apify~facebook-comments-scraper'
IG_POSTS, IG_COMMENTS, IG_TAGS = 'apify~instagram-post-scraper', 'apify~instagram-comment-scraper', 'apify~instagram-hashtag-scraper'
TT, TT_COMMENTS = 'clockworks~tiktok-scraper', 'clockworks~tiktok-comments-scraper'
YT, YT_CHANNEL = 'streamers~youtube-scraper', 'streamers~youtube-channel-scraper'
X, FB_SEARCH, REDDIT = 'kaitoeasyapi~twitter-x-data-tweet-scraper-pay-per-result-cheapest', 'scraper_one~facebook-posts-search', 'trudax~reddit-scraper-lite'
ABROAD = ['v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco']   # V7's pages abroad and the UK distributor
X_NOISE = ' -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery'


def api(method, path, body=None, timeout=60):
    req = urllib.request.Request('https://api.apify.com/v2' + path, method=method,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def spent():
    return api('GET', '/users/me/limits')['data']['current']['monthlyUsageUsd']


def log(line):
    print(line, flush=True)
    with open(HERE / 'run.log', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M  ') + line + '\n')


def run(name, actor, body, cap_usd, max_items=None):
    """Runs one actor with a cost cap; returns its items. Saves them with the input and the run's numbers."""
    out = RAW / (name + '.json')
    if out.exists() and '--force' not in sys.argv:
        print(f'{name}: already collected, skipped')
        return json.load(open(out, encoding='utf-8'))['items']
    before = spent()
    if BUDGET - before < cap_usd:
        log(f'{name}: skipped, only ${BUDGET - before:.2f} of the ${BUDGET:.2f} budget left (needs a ${cap_usd:.2f} cap)')
        return []
    q = f'?maxTotalChargeUsd={cap_usd:.3f}' + (f'&maxItems={max_items}' if max_items else '')
    try:
        r = api('POST', f'/acts/{actor}/runs{q}', body)['data']
    except urllib.error.HTTPError as e:
        log(f'{name}: could not start: HTTP {e.code} {e.read()[:200]!r}')
        return []
    while r['status'] in ('READY', 'RUNNING'):
        time.sleep(8)
        r = api('GET', f"/actor-runs/{r['id']}")['data']
    items = api('GET', f"/datasets/{r['defaultDatasetId']}/items?clean=true&format=json", timeout=300)
    time.sleep(6)
    after = spent()
    RAW.mkdir(exist_ok=True)
    keep = {k: r.get(k) for k in ('id', 'status', 'startedAt', 'finishedAt', 'chargedEventCounts', 'usageTotalUsd')}
    json.dump({'input': body, 'cap_usd': cap_usd, 'run': keep, 'cost_usd': round(after - before, 4), 'items': items},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f'{name:16s} {actor.split("~")[1][:28]:28s} {r["status"]:10s} {len(items):5d} items  ${after - before:.4f}  '
        f'(cap ${cap_usd:.2f})  total ${after:.4f}  events {r.get("chargedEventCounts")}')
    return items


def x_query(q):
    return q + X_NOISE + f' since:{SINCE} until:2026-10-17'


def stage_test():
    run('t_fb_posts', FB_POSTS, {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "resultsLimit": 3, "onlyPostsNewerThan": SINCE}, 0.03, 3)
    run('t_fb_comments', FB_COMMENTS, {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/posts/pfbid02Sqn37RqfHGdQXGMrdMUNfqyzCZ4k91JY3yut9mMo5AHY1qrCj3pZwSrCyfGjN9Ajl"},
                                                     {"url": "https://www.facebook.com/reel/1583808776758074/"}],
                                       "resultsLimit": 3, "includeNestedComments": True}, 0.04, 8)
    run('t_ig_posts', IG_POSTS, {"username": ["v7egypt"], "resultsLimit": 3, "onlyPostsNewerThan": SINCE}, 0.02, 3)
    run('t_ig_comments', IG_COMMENTS, {"directUrls": ["https://www.instagram.com/p/DdG_sWYEi_T/", "https://www.instagram.com/p/DZ2uClLMq8p/"],
                                       "resultsLimit": 3, "includeNestedComments": True}, 0.04, 12)
    run('t_tt_comments', TT_COMMENTS, {"postURLs": ["https://www.tiktok.com/@v7.egypt/video/7678406422190624008"], "commentsPerPost": 4, "maxRepliesPerComment": 2}, 0.05, 8)
    run('t_x', X, {"twitterContent": x_query('(V7 OR "في سفن" OR "ڤي سڤن") (مشروب OR كانز OR صودا)'), "maxItems": 20, "queryType": "Latest"}, 0.02, 20)
    run('t_fb_search', FB_SEARCH, {"query": "V7 مشروب", "resultsCount": 3, "searchType": "latest", "startDate": SINCE, "endDate": UNTIL}, 0.03, 3)
    run('t_ig_tag', IG_TAGS, {"hashtags": ["v7egypt"], "resultsLimit": 3, "keywordSearch": False}, 0.02, 3)
    run('t_tt_search', TT, dict(NODL, searchQueries=["V7 مشروب"], resultsPerPage=3), 0.50, 3)
    run('t_yt_search', YT, {"searchQueries": ["V7 مشروب"], "maxResults": 3, "maxResultsShorts": 0, "maxResultStreams": 0}, 0.03, 3)
    run('t_reddit', REDDIT, {"searches": ["V7 soda"], "searchPosts": True, "searchComments": False, "sort": "new", "maxItems": 3,
                             "maxPostCount": 3, "maxComments": 0, "postDateLimit": SINCE}, 0.05, 3)


def stage_own():
    """V7's own posts since 20 Apr, with their counts as of today."""
    run('fb_posts', FB_POSTS, {"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "resultsLimit": 80, "onlyPostsNewerThan": SINCE}, 0.45, 80)
    run('ig_posts', IG_POSTS, {"username": ["v7egypt"], "resultsLimit": 120, "onlyPostsNewerThan": SINCE}, 0.35, 120)
    run('tt_posts', TT, dict(NODL, profiles=["v7.egypt"], profileSorting="latest", oldestPostDateUnified=SINCE, resultsPerPage=60), 0.50, 60)
    run('yt_posts', YT_CHANNEL, {"startUrls": [{"url": "https://www.youtube.com/@V7Egypt"}], "maxResults": 40, "maxResultsShorts": 60,
                                 "maxResultStreams": 0, "oldestPostDate": SINCE}, 0.30, 100)


def in_window(iso):
    return bool(iso) and SINCE <= str(iso)[:10] <= UNTIL


def num(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


def cap_for(n, price):
    """A cost cap for n items: 40% over the expected cost, plus the start fee."""
    return round(n * price * 1.4 + 0.05, 2)


def stage_comments():
    """Every comment on V7's posts in the window, with replies (V7's own replies included)."""
    raw = lambda n: json.load(open(RAW / (n + '.json'), encoding='utf-8'))['items']
    fb = [(p['url'], num(p.get('comments'))) for p in raw('fb_posts') if in_window(p.get('time')) and num(p.get('comments')) > 0]
    ig = [(p['url'], num(p.get('commentsCount'))) for p in raw('ig_posts') if in_window(p.get('timestamp')) and num(p.get('commentsCount')) > 0]
    tt = [(p['webVideoUrl'], num(p.get('commentCount'))) for p in raw('tt_posts') if in_window(p.get('createTimeISO')) and num(p.get('commentCount')) > 0]
    yt = [(p['url'], num(p.get('commentsCount'))) for p in raw('yt_posts') if in_window(p.get('date')) and num(p.get('commentsCount')) > 0]
    for name, rows in (('fb', fb), ('ig', ig), ('tt', tt), ('yt', yt)):
        log(f'  {name}: {len(rows)} posts with comments, {sum(n for _, n in rows)} comments by their counts')
    if fb:
        n = sum(c for _, c in fb)
        # No onlyCommentsNewerThan: it's a charged filter (USD 0.001 a comment) and every post is already inside the window.
        # The 17 Oct run used it and paid about USD 0.56 for nothing.
        run('fb_comments', FB_COMMENTS, {"startUrls": [{"url": u} for u, _ in fb], "resultsLimit": 1500, "includeNestedComments": True},
            cap_for(n * 1.3, 0.002), int(n * 1.6) + 50)
    if ig:
        n = sum(c for _, c in ig)
        run('ig_comments', IG_COMMENTS, {"directUrls": [u for u, _ in ig], "resultsLimit": 1500, "includeNestedComments": True}, cap_for(n * 1.2, 0.0023), int(n * 1.5) + 50)
    if tt:
        n = sum(c for _, c in tt)
        run('tt_comments', TT_COMMENTS, {"postURLs": [u for u, _ in tt], "commentsPerPost": 1500, "maxRepliesPerComment": 50}, cap_for(n * 1.3, 0.001), int(n * 1.6) + 50)
    if yt:
        n = sum(c for _, c in yt)
        run('yt_comments', 'streamers~youtube-comments-scraper', {"startUrls": [{"url": u} for u, _ in yt], "maxComments": 1500}, cap_for(n, 0.0015), int(n * 1.3) + 20)


def stage_abroad():
    """The posts of V7's pages abroad and the UK distributor since 20 Apr, and their comments."""
    posts = run('abroad_posts', IG_POSTS, {"username": ABROAD, "resultsLimit": 60, "onlyPostsNewerThan": SINCE}, 0.45, 200)
    rows = [(p['url'], num(p.get('commentsCount'))) for p in posts if in_window(p.get('timestamp')) and num(p.get('commentsCount')) > 0]
    n = sum(c for _, c in rows)
    log(f'  abroad: {len(rows)} posts with comments, {n} comments by their counts')
    # 17 Oct: 1,837 comments, far more than planned (giveaway posts abroad). The run was aborted by hand after 829 comments
    # (USD 1.87); raw/abroad_comments.json holds those, so this stage doesn't run it again.
    if rows:
        run('abroad_comments', IG_COMMENTS, {"directUrls": [u for u, _ in rows], "resultsLimit": 800, "includeNestedComments": True}, cap_for(n * 1.2, 0.0023), int(n * 1.5) + 30)


def stage_ugc():
    """Public posts about V7 by anyone else, 20 Apr to 16 Oct: X, Facebook, Instagram hashtags, TikTok, YouTube and Reddit."""
    v7 = '(V7 OR "في سفن" OR "ڤي سڤن" OR "فى سفن")'
    X_Q = {
        'x_drink': (v7 + ' (مشروب OR مشروبات OR كانز OR صودا OR soda OR drink OR بيبسي OR كوكاكولا OR رمان OR "بينا كولادا" OR بيناكولادا OR "ليمون نعناع" '
                    'OR "كريم صودا" OR "cream soda" OR شعير OR malt OR بلوبيري OR أناناس OR "بينك ليموناد")', 250),
        'x_vcola': ('("في كولا" OR "ڤي كولا" OR "V Cola" OR VCola OR "ڤي ليمون" OR "V Lemon" OR "V Orange" OR "ڤي أورانج" OR "في أورانج")', 200),
        'x_talk': (v7 + ' (طعم OR طعمها OR جربت OR حلوة OR حلو OR وحشة OR غالية OR غالي OR سعر OR فين OR "مش لاقي" OR سكر OR فيتامين OR فيتامينات)', 200),
        'x_en': ('("V7 drink" OR "V7 soda" OR "V7 Egypt" OR "V7 cream soda" OR "V7 pomegranate" OR "v7 7elwa" OR "v7 gamda" OR "V7 malt")', 120),
        'x_brand': (v7 + ' (بينيفت OR فيتاليتي OR "منتج مصري" OR "صناعة مصرية" OR مقاطعة OR بديل)', 150),
    }
    for name, (q, n) in X_Q.items():
        run(name, X, {"twitterContent": x_query(q), "maxItems": n, "queryType": "Latest"}, 0.08, n)
    FB_Q = ['V7 مشروب', 'ڤي سڤن', 'في سفن مشروب', 'V7 كريم صودا', 'V7 رمان', 'V7 بينا كولادا', 'V7 شعير', 'في كولا', 'ڤي كولا', 'ڤي ليمون', 'V7 Egypt', 'مشروب V7 غازي']
    for i, q in enumerate(FB_Q):
        run(f'fb_search_{i:02d}', FB_SEARCH, {"query": q, "resultsCount": 30, "searchType": "latest", "startDate": SINCE, "endDate": UNTIL}, 0.12, 30)
    run('ig_tags', IG_TAGS, {"hashtags": ['v7egypt', 'فى_سفن', 'في_سفن', 'vcola', 'في_كولا', 'ڤي_كولا', 'vlemon', 'v7creamsoda'], "resultsLimit": 40,
                             "keywordSearch": False}, 0.85, 320)
    run('tt_search', TT, dict(NODL, searchQueries=['V7 مشروب', 'في سفن', 'ڤي سڤن', 'V7 كريم صودا', 'V7 رمان', 'ڤي كولا', 'في كولا', 'V7 drink', 'مشروب V7', 'V7 شعير'],
                              searchSection='/video', videoSearchDateFilter='LAST_6_MONTHS', resultsPerPage=30), 1.20, 300)
    run('yt_search', YT, {"searchQueries": ['V7 مشروب', 'ڤي سڤن', 'V7 cream soda', 'في كولا', 'V7 soda', 'مشروب ڤي سڤن'], "maxResults": 20, "maxResultsShorts": 10,
                          "maxResultStreams": 0, "dateFilter": "year", "sortingOrder": "relevance"}, 0.85, 180)
    run('reddit', REDDIT, {"searches": ['V7 soda', 'V7 drink', 'V7 cream soda', 'في سفن'], "searchPosts": True, "searchComments": True, "sort": "new",
                           "maxItems": 60, "maxPostCount": 15, "maxComments": 0, "postDateLimit": SINCE}, 0.35, 60)


STAGES = {'test': stage_test, 'own': stage_own, 'comments': stage_comments, 'abroad': stage_abroad, 'ugc': stage_ugc}

if __name__ == '__main__':
    stage = sys.argv[1] if len(sys.argv) > 1 else ''
    if stage not in STAGES:
        sys.exit('Usage: python3 collect.py ' + '|'.join(STAGES) + ' [--force]')
    log(f'--- stage {stage}, spent so far this cycle ${spent():.4f}, budget ${BUDGET:.2f}')
    STAGES[stage]()
    log(f'--- stage {stage} done, spent this cycle ${spent():.4f}')
