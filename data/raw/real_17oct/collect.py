"""Real data for every tab except Market (17 Oct 2026). The plan, the budget and the window are in PLAN.md.

Usage:  python3 collect.py <stage> [--force]
Stages, in order: test, own, comments, abroad, ugc; then test2 and wide (18 Oct, the wider search for public posts)
- Each run saves raw/<name>.json ({input, run, items}) and is skipped next time unless --force is given.
- Every run has a USD cap (Apify's maxTotalChargeUsd), and the whole collection stops at BUDGET, read from Apify's usage meter.
- The token is read from the environment only:  set -a; . ./.env.apify; set +a
"""
import json, os, pathlib, re, sys, time, urllib.error, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
TOK = os.environ['APIFY_API_TOKEN']
SINCE, UNTIL = '2026-04-20', '2026-10-16'       # 180 days: the dashboard's range
BUDGET = 14.00                                   # of the USD 19 a month; the rest is the reserve
BUDGET_YTC = 16.45                               # 18 Oct: YouTube comments, after the wider search
BUDGET_WIDE = 15.60                              # 18 Oct: the wider search for public posts may spend up to here (DECISIONS #127)
NODL = {"shouldDownloadVideos": False, "shouldDownloadCovers": False, "shouldDownloadSlideshowImages": False,
        "shouldDownloadAvatars": False, "shouldDownloadMusicCovers": False}
FB_POSTS, FB_COMMENTS = 'apify~facebook-posts-scraper', 'apify~facebook-comments-scraper'
IG_POSTS, IG_COMMENTS, IG_TAGS = 'apify~instagram-post-scraper', 'apify~instagram-comment-scraper', 'apify~instagram-hashtag-scraper'
IG_TAGGED = 'apify~instagram-tagged-scraper'      # posts in which other accounts tag a profile
IG_KW_SEEMUAPPS = 'seemuapps~instagram-keyword-posts-scraper'   # Instagram's keyword search, kept only inside the dates asked (used 18 Oct)
IG_KW = 'apidojo~instagram-scraper-api'          # Instagram keyword search from 19 Oct (DECISIONS #133; KEYWORD_SCRAPERS.md)
IG_REELS = 'dami_studio~instagram-reels-search-scraper'   # Instagram's Reels search, next to apidojo (DECISIONS #134)
IG_SCRAPER = 'apify~instagram-scraper'           # resultsType 'mentions': posts whose caption mentions a profile
GOOGLE = 'apify~google-search-scraper'
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


def run(name, actor, body, cap_usd, max_items=None, budget=None):
    """Runs one actor with a cost cap; returns its items. Saves them with the input and the run's numbers."""
    out = RAW / (name + '.json')
    if out.exists() and '--force' not in sys.argv:
        print(f'{name}: already collected, skipped')
        return json.load(open(out, encoding='utf-8'))['items']
    before, budget = spent(), budget or BUDGET
    if budget - before < cap_usd:
        log(f'{name}: skipped, only ${budget - before:.2f} of the ${budget:.2f} budget left (needs a ${cap_usd:.2f} cap)')
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


def stage_test2():
    """18 Oct: the 17 Oct search found almost nothing recent on Instagram (8 hashtags, mostly Cambodia's V-Cola) or TikTok (unrelated
    videos). A few results from each new method first: Instagram keyword search (posts and reels), posts tagging @v7egypt, and
    TikTok searched and browsed from Egypt."""
    B = BUDGET_WIDE
    run('t2_ig_tagged', IG_TAGGED, {"username": ["v7egypt"], "resultsLimit": 5}, 0.03, 5, budget=B)
    run('t2_ig_kw_posts', IG_TAGS, {"hashtags": ["ڤي سڤن", "V7 مشروب"], "keywordSearch": True, "resultsType": "posts", "resultsLimit": 4}, 0.04, 8, budget=B)
    run('t2_ig_kw_reels', IG_TAGS, {"hashtags": ["ڤي سڤن", "V7 مشروب"], "keywordSearch": True, "resultsType": "reels", "resultsLimit": 4}, 0.04, 8, budget=B)
    run('t2_tt_search_eg', TT, dict(NODL, searchQueries=["ڤي سڤن", "في سفن مشروب"], searchSection="/video", resultsPerPage=5, proxyCountryCode="EG"), 0.50, 10, budget=B)
    run('t2_tt_top_eg', TT, dict(NODL, searchQueries=["V7 مشروب"], searchSection="", resultsPerPage=5, proxyCountryCode="EG"), 0.50, 5, budget=B)
    run('t2_tt_tags_eg', TT, dict(NODL, hashtags=["v7egypt", "ڤي_سڤن"], resultsPerPage=5, proxyCountryCode="EG"), 0.50, 10, budget=B)
    # TikTok's own date filter returned unrelated videos on 17 Oct (searched from abroad); tried again from Egypt
    run('t2_tt_6m_eg', TT, dict(NODL, searchQueries=["ڤي سڤن"], searchSection="/video", videoSearchDateFilter="LAST_6_MONTHS", resultsPerPage=5, proxyCountryCode="EG"), 0.50, 5, budget=B)
    run('t2_tt_month_eg', TT, dict(NODL, searchQueries=["V7 مشروب"], searchSection="/video", videoSearchDateFilter="PAST_MONTH", resultsPerPage=5, proxyCountryCode="EG"), 0.50, 5, budget=B)
    run('t2_ig_mentions', IG_SCRAPER, {"directUrls": ["https://www.instagram.com/v7egypt/"], "resultsType": "mentions", "resultsLimit": 5}, 0.03, 5, budget=B)
    run('t2_ig_kw_dated', IG_KW_SEEMUAPPS, {"keywords": ["ڤي سڤن", "V7 drink"], "maxPostsPerKeyword": 5, "dateFrom": SINCE, "dateTo": UNTIL}, 0.06, 10, budget=B)
    run('t2_google', GOOGLE, {"queries": '"ڤي سڤن" site:instagram.com\n"ڤي سڤن" site:tiktok.com', "quickDateRange": "m6", "countryCode": "eg",
                              "maxPagesPerQuery": 1}, 0.50, 2, budget=B)   # USD 0.50 is the lowest cap it accepts; it costs USD 0.0025 a page


# ------------------------------------------------------------------ 18 Oct: the wider search for public posts (DECISIONS #127)
# Spellings people use for V7 and its line, in Arabic and English, most useful first (a run that reaches its cap drops the last ones)
KW_IG = ["ڤي سڤن", "في سفن", "فى سفن", "فيسفن", "ڤيسڤن", "V7 drink", "V7 soda", "V7 Egypt", "مشروب ڤي سڤن", "مشروب V7", "ڤي كولا", "في كولا",
         "V Cola", "ڤي اورانج", "V Orange", "ڤي سوبر صودا", "V Super Soda", "V7 كريم صودا", "V7 cream soda", "ڤي سڤن كريم صودا", "V7 بينك ليمونيد",
         "V7 pink lemonade", "V7 رمان", "V7 بلوبيري"]
KW_GOOGLE = ['"ڤي سڤن"', '"في سفن"', '"فى سفن"', '"فيسفن"', '"V7 drink"', '"V7 soda"', '"V7 Egypt"', '"ڤي كولا"', '"في كولا"', '"V Cola" مصر',
             '"ڤي اورانج"', '"V Orange"', '"V Super Soda"', '"V7 cream soda"', '"V7 كريم صودا"', '"@v7egypt"', '"V7" مشروب', '"V7" كانز']
KW_TT = ["ڤي سڤن", "في سفن مشروب", "فيسفن", "V7 مشروب", "V7 drink", "ڤي كولا", "ڤي اورانج", "V7 كريم صودا", "V7 cream soda", "V7 بينك ليمونيد"]
B62 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'


def id_day(pl, key):
    """The day a post went up, read from its id (no request needed): Instagram's shortcode holds milliseconds since 24 Aug 2011
    in its top bits, TikTok's video id holds seconds since 1970 in its top 32 bits."""
    import datetime
    try:
        if pl == 'ig':
            n = 0
            for ch in key: n = n * 64 + B62.index(ch)
            t = ((n >> 23) + 1314220021721) / 1000
        else:
            t = int(key) >> 32
        return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date().isoformat()
    except (ValueError, OverflowError):
        return None


def known_keys():
    """Shortcodes and TikTok ids already collected, so Google's finds are only fetched when new."""
    import re as _re
    keys = set()
    for f in RAW.glob('*.json'):
        for x in json.load(open(f, encoding='utf-8')).get('items', []):
            if isinstance(x, dict):
                k = x.get('shortCode') or x.get('shortcode')
                if k: keys.add('ig:' + k)
                if x.get('webVideoUrl'): keys.add('tt:' + str(x.get('id')))
    return keys


def google_finds(name, pl):
    import re as _re
    out = {}
    for page in (json.load(open(RAW / (name + '.json'), encoding='utf-8'))['items'] if (RAW / (name + '.json')).exists() else []):
        for r in page.get('organicResults') or []:
            u = r.get('url') or ''
            m = _re.search(r'instagram\.com/(?:[\w.]+/)?(?:p|reel|tv)/([\w-]{8,})', u) if pl == 'ig' else _re.search(r'tiktok\.com/@([\w.]+)/(?:video|photo)/(\d{15,})', u)
            if m:
                key = m.group(1) if pl == 'ig' else m.group(2)
                out[key] = 'https://www.instagram.com/p/%s/' % key if pl == 'ig' else 'https://www.tiktok.com/@%s/video/%s' % (m.group(1), m.group(2))
    return out


def stage_wide():
    """Public posts the 17 Oct search missed: Instagram posts tagging V7's accounts, Instagram's keyword search kept inside the window,
    Google searches limited to instagram.com and tiktok.com (posts with the words in their caption), then more spellings on
    Facebook, X, TikTok and YouTube."""
    B = BUDGET_WIDE
    run('ig_tagged_v7', IG_TAGGED, {"username": ["v7egypt"], "resultsLimit": 180}, 0.45, 180, budget=B)
    run('ig_tagged_vss', IG_TAGGED, {"username": ["vsupersoda"], "resultsLimit": 60}, 0.15, 60, budget=B)
    run('ig_kw_wide', IG_KW_SEEMUAPPS, {"keywords": KW_IG, "maxPostsPerKeyword": 30, "dateFrom": SINCE, "dateTo": UNTIL}, 0.75, 720, budget=B)
    q = lambda site, pages: {"queries": '\n'.join('%s site:%s' % (k, site) for k in KW_GOOGLE), "quickDateRange": "m6", "countryCode": "eg",
                             "maxPagesPerQuery": pages}
    run('google_ig', GOOGLE, q('instagram.com', 3), 0.50, len(KW_GOOGLE) * 3, budget=B)
    run('google_tt', GOOGLE, q('tiktok.com', 2), 0.50, len(KW_GOOGLE) * 2, budget=B)
    have = known_keys()
    for pl, name in (('ig', 'google_ig'), ('tt', 'google_tt')):
        finds = google_finds(name, pl)
        new = {k: u for k, u in finds.items() if (pl + ':' + k) not in have and SINCE <= (id_day(pl, k) or '') <= UNTIL}
        log(f'  {name}: {len(finds)} post links, {len(new)} new inside the window')
        if new and pl == 'ig':
            run('ig_google_posts', IG_POSTS, {"username": list(new.values())}, round(len(new) * 0.0023 * 1.3 + 0.05, 2), len(new), budget=B)
        if new and pl == 'tt':
            run('tt_google_posts', TT, dict(NODL, postURLs=list(new.values())), max(0.50, round(len(new) * 0.004 * 1.3, 2)), len(new), budget=B)
    for i, kw in enumerate(['فى سفن', 'فيسفن', 'ڤي اورانج', 'V Orange', 'V Super Soda', 'V7 بينك ليمونيد'], start=12):
        run(f'fb_search_{i:02d}', FB_SEARCH, {"query": kw, "resultsCount": 30, "searchType": "latest", "startDate": SINCE, "endDate": UNTIL}, 0.12, 30, budget=B)
    run('x_extra', X, {"twitterContent": x_query('(فيسفن OR ڤيسڤن OR "ڤى سڤن" OR "في سيفن" OR Vseven OR "V Orange" OR "ڤي اورانج" OR "ڤي أورانج" '
                                                 'OR "V Super Soda" OR "ڤي سوبر صودا")'), "maxItems": 200, "queryType": "Latest"}, 0.08, 200, budget=B)
    # TikTok: searched and browsed from Egypt, without TikTok's date filter (it returns unrelated videos); dates are checked afterwards
    run('tt_tags_wide', TT, dict(NODL, hashtags=['v7egypt', 'ڤي_سڤن', 'فيسفن', 'vseven', 'ڤي_اورانج'], resultsPerPage=25, proxyCountryCode="EG"), 0.50, 125, budget=B)
    run('tt_wide', TT, dict(NODL, searchQueries=KW_TT, searchSection="/video", resultsPerPage=30, proxyCountryCode="EG"), 0.50, 300, budget=B)
    run('yt_recent', YT, {"searchQueries": ['ڤي سڤن', 'في سفن مشروب', 'V7 drink', 'ڤي كولا', 'V7 cream soda'], "maxResults": 10, "maxResultsShorts": 10,
                          "maxResultStreams": 0, "dateFilter": "year", "sortingOrder": "date"}, 0.35, 100, budget=B)


YT_COMMENTS, YT_COMMENTS2 = 'apidojo~youtube-comments-scraper', 'calm_builder~youtube-scraper'


def stage_test3():
    """18 Oct: comments on public YouTube videos about V7 (V7 Egypt's own videos have comments turned off). The user found two
    comment scrapers; 20 comments each from Kareem Elsayed's video (9 Oct, 1.47M views, 943 comments)."""
    v = "https://www.youtube.com/watch?v=i9PVV4QqtXE"
    run('t3_yt_comments_apidojo', YT_COMMENTS, {"startUrls": [{"url": v}], "sort": "top", "maxItems": 20, "includeReplies": False}, 0.05, 20, budget=16.0)
    run('t3_yt_comments_calm', YT_COMMENTS2, {"startUrls": [{"url": v}], "maxResults": 1, "maxComments": 20, "commentsSortBy": "top", "maxReplyDepth": 1,
                                              "maxRepliesPerComment": 3}, 0.50, 90, budget=16.0)   # USD 0.50: its lowest accepted cap


def stage_ytcheck():
    """18 Oct: are comments really off on V7 Egypt's own videos? calm_builder's video rows say so per video (USD 0.0012 a video)."""
    urls = [v['url'] for v in json.load(open(RAW / 'yt_posts.json', encoding='utf-8'))['items'] if v.get('url')]
    run('yt_own_check', YT_COMMENTS2, {"startUrls": [{"url": u} for u in urls], "maxResults": 1, "maxComments": 0}, 0.50, len(urls) + 2, budget=16.0)


def stage_ytc():
    """18 Oct: YouTube comments (apidojo's comments scraper, USD 0.0005 a comment). V7 Egypt's own videos with comments (75 by
    their counts, replies included: V7's answers count) and the public videos about V7 that Claude kept on 17 Oct (top-level
    comments, the biggest video first)."""
    own = [x for x in json.load(open(RAW / 'yt_own_check.json', encoding='utf-8'))['items'] if (x.get('commentCount') or 0) > 0]
    n_own = sum(x['commentCount'] for x in own)
    run('yt_comments_own', YT_COMMENTS, {"startUrls": [{"url": x['url']} for x in own], "sort": "top", "maxItems": n_own + 40, "includeReplies": True},
        round((n_own + 40) * 0.0005 + len(own) * 0.002 + 0.05, 2), n_own + 40, budget=BUDGET_YTC)
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    pub = sorted((i for i in items if i['pl'] == 'yt' and i['src'] == 'ugc' and (labels.get(i['id']) or {}).get('about') and (i.get('comments') or 0) > 0),
                 key=lambda i: -i['comments'])
    n = sum(i['comments'] for i in pub)
    log(f'  public YouTube videos about V7 with comments: {len(pub)}, {n} comments by their counts (replies included)')
    run('yt_comments_public', YT_COMMENTS, {"startUrls": [{"url": i['url']} for i in pub], "sort": "top", "maxItems": n, "includeReplies": False},
        round(n * 0.0005 + len(pub) * 0.001 + 0.05, 2), n, budget=BUDGET_YTC)


def stage_ttkw():
    """18 Oct: the TikTok keyword search the wide stage skipped at its budget line, run at the user's request. Searched from Egypt,
    without TikTok's date filter (it returns unrelated videos); dates are checked afterwards."""
    run('tt_wide', TT, dict(NODL, searchQueries=KW_TT, searchSection="/video", resultsPerPage=30, proxyCountryCode="EG"), 0.50, 300, budget=16.40)


def stage_kwtest():
    """19 Oct: which Instagram keyword scraper is strongest? The same three keywords (English, Arabic with ڤ, mixed), up to 10 results each,
    for the six best-rated keyword scrapers in the Store and the one used on 18 Oct. Scrapers that take exact phrases get them in quotes."""
    B = 17.40   # at most about USD 1 over the 16.33 spent; expected about 0.45
    K = ['V7 soda', 'ڤي سڤن', 'V7 كريم صودا']; Q = ['"%s"' % k for k in K]

    def go(name, actor, body, cap, n):
        run(name, actor, body, cap, n, budget=B)
        if not (RAW / (name + '.json')).exists():    # some scrapers refuse a cap under USD 0.50 (the cap is a ceiling, not the cost)
            run(name, actor, body, 0.50, n, budget=B)
    for i, k in enumerate(K, 1):
        go(f'kw_apidojo_{i}', 'apidojo~instagram-scraper-api', {"keywords": [k], "maxItems": 10, "until": SINCE}, 0.10, 10)
    go('kw_apify_search', 'apify~instagram-search-scraper', {"search": ', '.join(K), "searchType": "popular", "searchLimit": 10}, 0.12, 30)
    go('kw_memo23', 'memo23~instagram-reels-search-scraper', {"queries": Q, "maxResultsPerQuery": 10, "oldestPostDate": SINCE, "newestPostDate": UNTIL,
                                                               "contentType": "posts_and_reels"}, 0.10, 30)
    for i, q in enumerate(Q, 1):
        go(f'kw_boolean_{i}', 'scraping_solutions~instagram-boolean-search-scraper-posts-reels', {"searchQuery": q, "resultsLimit": 10, "contentType": "posts_and_reels",
                                                                                              "oldestPostDate": SINCE, "newestPostDate": UNTIL}, 0.10, 10)
    for i, k in enumerate(K, 1):
        go(f'kw_dataslayer_{i}', 'data-slayer~instagram-search-reels', {"query": k, "maxPages": 1}, 0.05, 10)
    go('kw_dami', 'dami_studio~instagram-reels-search-scraper', {"searchQueries": K, "maxReelsPerTerm": 10, "maxReels": 30, "newerThan": SINCE}, 0.05, 30)
    go('kw_seemuapps', IG_KW_SEEMUAPPS, {"keywords": K, "maxPostsPerKeyword": 10, "dateFrom": SINCE, "dateTo": UNTIL}, 0.10, 30)


# Instagram keyword search from 19 Oct: English and mixed phrases only (Instagram's own search fails on Arabic spellings; Arabic posts come
# from the posts that tag V7 and from Google's exact-phrase search). One apidojo run per keyword: its item limit is per run, not per keyword.
KW_IG_EN = ["V7 soda", "V7 drink", "V7 Egypt", "مشروب V7", "V7 كانز", "V Cola", "V Orange", "V Super Soda", "V7 cream soda", "V7 كريم صودا",
            "V7 pink lemonade", "V7 بينك ليمونيد", "V7 رمان", "V7 بلوبيري", "V7 شعير"]
BUDGET_IGKW = 32.0   # 19 Oct: the limit is USD 100 (was 18.40 under the USD 19 ceiling)
IG_OWN = {'v7egypt', 'v7.egypt', 'vsupersoda', 'v.super.soda'} | set(ABROAD)   # V7's own accounts: collected elsewhere, never re-fetched


def ig_gaps(tag):
    """Links of the apidojo rows that came back without a caption or likes (DECISIONS #135), unless dami_studio returned the same
    reel complete. Instagram's own gaps stay: a post with no caption, or likes the owner hid, comes back the same."""
    complete = set()
    for f in sorted(RAW.glob('igreels_%s*.json' % tag)):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            if x.get('shortcode') and x.get('caption') and x.get('likeCount') is not None:
                complete.add(x['shortcode'])
    gaps = {}
    for f in sorted(RAW.glob('igkw_%s_[0-9][0-9].json' % tag)):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            if (x.get('code') and x.get('url') and x['code'] not in complete and ((x.get('owner') or {}).get('username') or '').lower() not in IG_OWN
                    and (not x.get('caption') or x.get('likeCount') is None)):
                gaps[x['code']] = x['url']
    return list(gaps.values())


def stage_igkw():
    """Instagram posts about V7 by keyword, newer than --since (default: the window's start), from two of Instagram's searches:
    - apidojo (posts, reels and albums): about USD 0.015 a keyword plus USD 0.0005 a post, first 10 results per keyword (--per);
    - dami_studio (Reels search, which finds reels apidojo misses): USD 0.0004 a reel delivered or checked, 30 per keyword (--reels).
    Usage: python3 collect.py igkw [--since 2026-10-17] [--per 10] [--reels 30]"""
    a = sys.argv
    since = a[a.index('--since') + 1] if '--since' in a else SINCE
    per = int(a[a.index('--per') + 1]) if '--per' in a else 10   # apidojo gives captions and likes for about its first 10 results; past that, mostly bare links
    for i, kw in enumerate(KW_IG_EN):
        run('igkw_%s_%02d' % (since.replace('-', ''), i), IG_KW, {"keywords": [kw], "maxItems": per, "until": since},
            round(0.03 + per * 0.0005 * 1.5, 2), per, budget=BUDGET_IGKW)
    reels = int(a[a.index('--reels') + 1]) if '--reels' in a else 30
    per_run = max(1, 100 // reels)   # it delivers at most 100 reels a run, so a few keywords a run; reels older than --since are checked and billed, not delivered
    for k in range(0, len(KW_IG_EN), per_run):
        kws = KW_IG_EN[k:k + per_run]; n = reels * len(kws)
        run('igreels_%s_%02d' % (since.replace('-', ''), k // per_run), IG_REELS, {"searchQueries": kws, "maxReelsPerTerm": reels, "maxReels": n, "newerThan": since},
            round(n * 0.000395 * 2 + 0.05, 2), n + 5, budget=BUDGET_IGKW)
    # Re-fetch by link what apidojo returned without a caption or likes (Apify's post scraper, USD 0.0023 a post; DECISIONS #135)
    gaps = ig_gaps(since.replace('-', ''))
    log(f'  igkw: {len(gaps)} posts to re-fetch for a missing caption or likes')
    if gaps:
        run('igkw_%s_refetch' % since.replace('-', ''), IG_POSTS, {"username": gaps}, round(len(gaps) * 0.0023 * 1.3 + 0.05, 2), len(gaps), budget=BUDGET_IGKW)


def stage_kwdeep():
    """19 Oct: apidojo missed 4 of dami_studio's reels for "V7 soda" in the top 10. Are they further down its results (depth) or not there at all?"""
    run('kw_apidojo_deep', 'apidojo~instagram-scraper-api', {"keywords": ["V7 soda"], "maxItems": 40, "until": SINCE}, 0.10, 40, budget=17.10)


def stage_refetchtest():
    """19 Oct: does the re-fetch close apidojo's gaps? The 25 posts the step picks from the comparison runs, fetched for real."""
    global RAW
    import shutil, tempfile
    t = pathlib.Path(tempfile.mkdtemp())
    for src, dst in (('kw_apidojo_1', 'igkw_TEST_00'), ('kw_apidojo_3', 'igkw_TEST_01'), ('kw_apidojo_deep', 'igkw_TEST_02'), ('kw_dami', 'igreels_TEST')):
        shutil.copy(RAW / (src + '.json'), t / (dst + '.json'))
    real, RAW = RAW, t
    gaps = ig_gaps('TEST')
    RAW = real
    run('kw_refetch_test', IG_POSTS, {"username": gaps}, round(len(gaps) * 0.0023 * 1.3 + 0.05, 2), len(gaps), budget=17.10)


def stage_transcripttest():
    """19 Oct: can Instagram reels in Egyptian Arabic be transcribed? apple_yang's speech-to-text on 3 reels about V7 (USD 0.0045 a reel)."""
    urls = json.load(open(sys.argv[sys.argv.index('--urls') + 1], encoding='utf-8'))
    run('kw_transcript_test', 'apple_yang~instagram-transcripts-scraper', {"bulkUrls": urls, "resultsLimit": len(urls)}, 0.05, len(urls) + 2, budget=17.10)


SPEECH = 'apple_yang~instagram-transcripts-scraper'   # what's said in a reel (speech to text): USD 0.001 a reel + USD 0.0035 a started minute
PROFILES = 'apify~instagram-profile-scraper'           # an account's follower count: USD 0.0023 an account
BUDGET_SPEECH = 40.0                                 # 19 Oct: speech and follower counts may spend up to here (DECISIONS #137, #138)


def _seconds():
    """Each Instagram video's length, from every raw file that has one."""
    out = {}
    for f in RAW.glob('*.json'):
        for x in json.load(open(f, encoding='utf-8')).get('items', []):
            if isinstance(x, dict):
                code = x.get('shortCode') or x.get('shortcode') or x.get('code')
                d = x.get('videoDuration') or x.get('durationSeconds') or ((x.get('video') or {}).get('duration') if isinstance(x.get('video'), dict) else None)
                if code and d:
                    out[code] = float(d)
    return out


def stage_igspeech():
    """19 Oct (user's OK): what's said in the Instagram reels, for Claude to read with the caption. First the 166 public reels about
    V7, most viewed first; then the reels that tag V7 but whose caption alone didn't show it. Reels already transcribed are skipped."""
    import math
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    about = lambda i: (labels.get(i['id']) or {}).get('about')
    done = set()
    for f in list(RAW.glob('igspeech_*.json')) + [RAW / 'kw_transcript_test.json']:
        if f.exists():
            done |= {x.get('code') for x in json.load(open(f, encoding='utf-8'))['items'] if x.get('code')}
    reels = [i for i in items if i['src'] == 'ugc' and i['kind'] == 'post' and i['pl'] == 'ig' and i.get('fmt') == 'Reel' and i.get('url') and i['id'][3:] not in done]
    first = sorted((i for i in reels if about(i)), key=lambda i: -(i.get('views') or 0))
    second = sorted((i for i in reels if not about(i) and any(r.startswith('ig_tagged') for r in i['found_by'])), key=lambda i: -(i.get('views') or 0))
    secs = _seconds()
    cost = lambda lst: round((sum(math.ceil(secs.get(i['id'][3:], 60) / 60) for i in lst) * 0.0035 + len(lst) * 0.001) * 1.3 + 0.05, 2)
    tag = time.strftime('%Y%m%d%H%M')
    for name, lst in (('igspeech_about_' + tag, first), ('igspeech_tagged_' + tag, second)):
        log(f'  {name}: {len(lst)} reels, cap ${cost(lst):.2f}')
        if lst:
            run(name, SPEECH, {"bulkUrls": [i['url'] for i in lst], "resultsLimit": len(lst)}, cost(lst), len(lst) + 5, budget=BUDGET_SPEECH)


def stage_igprofiles():
    """19 Oct (user's OK): the follower counts the keyword and post scrapers don't return, for the Instagram accounts that posted about V7."""
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    handles = sorted({(i.get('author') or {}).get('handle') for i in items if i['src'] == 'ugc' and i['kind'] == 'post' and i['pl'] == 'ig'
                      and (labels.get(i['id']) or {}).get('about') and (i.get('author') or {}).get('handle') and (i.get('author') or {}).get('followers') is None})
    log(f'  igprofiles: {len(handles)} accounts without a follower count')
    if handles:
        run('ig_profiles_' + time.strftime('%Y%m%d%H%M'), PROFILES, {"usernames": handles}, round(len(handles) * 0.0023 * 1.3 + 0.05, 2), len(handles) + 5, budget=BUDGET_SPEECH)


def stage_vistest():
    """19 Oct: which method reads music reels and photos best? Step 1: the sample's posts fetched fresh (full-size media links)."""
    sample = json.load(open(sys.argv[sys.argv.index('--sample') + 1], encoding='utf-8'))
    urls = [x['url'] for x in sample]
    run('vis_posts', IG_POSTS, {"username": urls}, round(len(urls) * 0.0023 * 1.3 + 0.05, 2), len(urls), budget=30.0)


def stage_vistest2():
    """19 Oct: the alternatives on the same sample: afanasenko's on-screen-text extractor (USD 0.075 a reel) on 3 reels, and the posts'
    comments from scrapesmith (USD 0.0005 a comment) and from Apify's own scraper (USD 0.0023) to compare them."""
    sample = json.load(open(sys.argv[sys.argv.index('--sample') + 1], encoding='utf-8'))
    urls = [x['url'] for x in sample]
    reels = ['https://www.instagram.com/reel/Db0cx1pMQ37/', 'https://www.instagram.com/reel/DeFaRKwo4zU/', 'https://www.instagram.com/reel/DZYSInqKZh0/']
    run('vis_afanasenko', 'afanasenko~instagram-reel-script-extractor', {"reelUrls": reels, "maxItemsMode1": 3}, 0.30, 3, budget=30.0)
    run('vis_cm_scrapesmith', 'scrapesmith~instagram-comments-scraper', {"postUrls": urls, "maxCommentsPerPost": 20, "sortOrder": "popular"}, 0.15, 170, budget=30.0)
    run('vis_cm_apify', IG_COMMENTS, {"directUrls": urls, "resultsLimit": 20}, 0.50, 170, budget=30.0)


def stage_covtest():
    """19 Oct: three more ways to find Instagram posts about V7, a few results each: reels that use V7's own ad audio (apidojo, audio
    pages), Google limited to one month at a time (exact phrase, site:instagram.com), and hashtags not tried before."""
    import urllib.parse
    run('cov_audio', IG_KW, {"startUrls": ["https://www.instagram.com/reels/audio/27762052746747139/", "https://www.instagram.com/reels/audio/40046659618266325/"],
                              "maxItems": 20}, 0.10, 20, budget=30.0)
    g = lambda q, a, b: 'https://www.google.com/search?' + urllib.parse.urlencode({'q': q + ' site:instagram.com', 'tbs': 'cdr:1,cd_min:%s,cd_max:%s' % (a, b), 'num': 10})
    run('cov_google_month', GOOGLE, {"queries": '\n'.join([g('"V7"', '6/1/2026', '6/30/2026'), g('"ڤي سڤن"', '6/1/2026', '6/30/2026')]), "maxPagesPerQuery": 1, "countryCode": "eg"},
        0.50, 4, budget=30.0)
    run('cov_tags', IG_TAGS, {"hashtags": ['ڤي_سڤن', 'vsupersoda', 'vorange', 'v7drink'], "resultsLimit": 5, "keywordSearch": False}, 0.10, 20, budget=30.0)


BUDGET_IG = 40.0     # 19 Oct: closing the Instagram gaps may spend up to here (the limit is USD 100 since 19 Oct; DECISIONS #139)
MONTHS = [('4/20/2026', '4/30/2026'), ('5/1/2026', '5/31/2026'), ('6/1/2026', '6/30/2026'), ('7/1/2026', '7/31/2026'), ('8/1/2026', '8/31/2026'),
          ('9/1/2026', '9/30/2026'), ('10/1/2026', '10/16/2026')]
G_PHRASES = ['"V7"', '"ڤي سڤن"', '"ڤي كولا"', '"V Cola"', '"V7 cream soda"', '"V7 كريم صودا"', '"@v7egypt"', '"V7 Egypt"', '"V Orange"', '"ڤي اورانج"',
             '"V Super Soda"', '"مشروب V7"']


def stage_igcover():
    """19 Oct (user: close all the Instagram gaps): more Instagram posts about V7 from every route that tested well:
    - Google one month at a time (12 exact phrases x 7 months, 3 pages each), then the new posts inside the window fetched by link;
    - the posts tagging @v7egypt back to 20 Apr (the 180 of 18 Oct reached 19 Jun);
    - 8 hashtags not tried before;
    - one more keyword sample (seemuapps, English and mixed phrases), since Instagram's search shuffles.
    The apidojo + dami_studio keyword search runs as `igkw --since 2026-04-20`."""
    import urllib.parse
    B = BUDGET_IG
    g = lambda q, a, b: 'https://www.google.com/search?' + urllib.parse.urlencode({'q': q + ' site:instagram.com', 'tbs': 'cdr:1,cd_min:%s,cd_max:%s' % (a, b)})
    run('ig_google_months', GOOGLE, {"queries": '\n'.join(g(q, a, b) for q in G_PHRASES for a, b in MONTHS), "maxPagesPerQuery": 3, "countryCode": "eg"},
        1.00, len(G_PHRASES) * len(MONTHS) * 3, budget=B)
    have = known_keys()
    finds = google_finds('ig_google_months', 'ig')
    new = {k: u for k, u in finds.items() if ('ig:' + k) not in have and SINCE <= (id_day('ig', k) or '') <= UNTIL}
    log(f'  ig_google_months: {len(finds)} post links, {len(new)} new inside the window')
    if new:
        run('ig_google2_posts', IG_POSTS, {"username": list(new.values())}, round(len(new) * 0.0023 * 1.3 + 0.05, 2), len(new), budget=B)
    run('ig_tagged_v7_full', IG_TAGGED, {"username": ["v7egypt"], "resultsLimit": 520}, 1.40, 520, budget=B)
    run('ig_tags2', IG_TAGS, {"hashtags": ['ڤي_سڤن', 'vsupersoda', 'vorange', 'v7drink', 'v7creamsoda', 'ڤي_كولا', 'vcolaegypt', 'ڤي_اورانج'], "resultsLimit": 30,
                              "keywordSearch": False}, 0.70, 240, budget=B)
    run('ig_kw_wide2', IG_KW_SEEMUAPPS, {"keywords": ["V Super Soda", "V7 cream soda", "V7 كريم صودا", "V7 pink lemonade", "V7 بينك ليمونيد", "V7 رمان",
                                                      "V7 بلوبيري", "V7 شعير", "V7 كانز"], "maxPostsPerKeyword": 30, "dateFrom": SINCE, "dateTo": UNTIL}, 0.60, 270, budget=B)


IG_CM_CHEAP = 'scrapesmith~instagram-comments-scraper'   # USD 0.0005 a comment; same comments as Apify's own (75 of 86 in the 19 Oct test)


def _ig_public(about_only=True):
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    out = [i for i in items if i['src'] == 'ugc' and i['kind'] == 'post' and i['pl'] == 'ig' and i.get('url')]
    return [i for i in out if (labels.get(i['id']) or {}).get('about')] if about_only else out, labels


def stage_igcomments():
    """19 Oct (DECISIONS #141): the comments under the public Instagram posts about V7, up to 100 a post, most liked first (scrapesmith).
    They add what people say about V7 under other people's posts. Posts already done are skipped."""
    posts, _ = _ig_public()
    done = set()
    for f in RAW.glob('igcm_*.json'):
        done |= {(x.get('postUrl') or '').rstrip('/').split('/')[-1] for x in json.load(open(f, encoding='utf-8'))['items']}
    todo = [i for i in posts if (i.get('comments') or 0) > 0 and i['id'][3:] not in done]
    n = sum(min(i['comments'], 100) for i in todo)
    log(f'  igcomments: {len(todo)} posts, about {n} comments')
    if todo:
        tag = time.strftime('%Y%m%d%H%M')
        run('igcm_' + tag, IG_CM_CHEAP, {"postUrls": [i['url'] for i in todo], "maxCommentsPerPost": 100, "sortOrder": "popular"},
            round(n * 0.0005 * 1.3 + 0.05, 2), n + 50, budget=BUDGET_IG)


def stage_igvisfetch():
    """19 Oct (DECISIONS #140): fresh media links for the Instagram posts whose pictures Claude will read (vis_media.py, vis_read.py):
    posts about V7 that are photos, albums, or reels without usable speech, and posts that tag or hashtag V7 but whose text didn't show
    it. Posts already read are skipped."""
    posts, labels = _ig_public(about_only=False)
    read = json.load(open(HERE / 'vis_read.json', encoding='utf-8')) if (HERE / 'vis_read.json').exists() else {}
    about = lambda i: (labels.get(i['id']) or {}).get('about')
    quiet = lambda i: i.get('fmt') in ('Image', 'Album') or len(i.get('speech') or '') < 20
    signal = lambda i: any(r.startswith(('ig_tagged', 'ig_tags')) for r in i['found_by'])
    fetched = set()
    for f in RAW.glob('vis_posts*.json'):
        fetched |= {x.get('shortCode') for x in json.load(open(f, encoding='utf-8'))['items'] if x.get('shortCode')}
    todo = [i for i in posts if i['id'][3:] not in read and i['id'][3:] not in fetched and quiet(i) and (about(i) or signal(i))]
    log(f'  igvisfetch: {len(todo)} posts ({sum(1 for i in todo if about(i))} about V7, {sum(1 for i in todo if not about(i))} to check)')
    if todo:
        tag = time.strftime('%Y%m%d%H%M')
        run('vis_posts_' + tag, IG_POSTS, {"username": [i['url'] for i in todo]}, round(len(todo) * 0.0023 * 1.3 + 0.05, 2), len(todo), budget=BUDGET_IG)


def stage_igcomments2():
    """19 Oct: scrapesmith returned nothing for 137 of 251 posts (DECISIONS #141), so the posts with no comments collected get them from
    Apify's own comment scraper (USD 0.0023 a comment), up to 100 a post."""
    posts, _ = _ig_public()
    done = set()
    for f in RAW.glob('igcm_*.json'):
        done |= {(x.get('postUrl') or '').rstrip('/').split('/')[-1] for x in json.load(open(f, encoding='utf-8'))['items']}
    todo = [i for i in posts if (i.get('comments') or 0) > 0 and i['id'][3:] not in done]
    n = sum(min(i['comments'], 100) for i in todo)
    log(f'  igcomments2: {len(todo)} posts without comments, about {n} comments')
    if todo:
        run('igcm_official_' + time.strftime('%Y%m%d%H%M'), IG_COMMENTS, {"directUrls": [i['url'] for i in todo], "resultsLimit": 100, "includeNestedComments": False},
            round(n * 0.0023 * 1.2 + 0.05, 2), n + 50, budget=BUDGET_IG)


# ------------------------------------------------------------------ 19 Oct: Facebook, the same work as Instagram (user: "do the same with facebook")
FB_TEST_K = ['V7 soda', 'ڤي سڤن', 'V7 كريم صودا']   # the three keywords of the Instagram comparison (KEYWORD_SCRAPERS.md)


def parallel(todo, budget, workers=8):
    """Runs (name, actor, body, cap, n) in parallel threads; a scraper that refuses a cap under USD 0.50 is retried with 0.50
    (the cap is a ceiling, not the cost). Costs per run are read later from the run records (scrapers_report.py)."""
    import concurrent.futures

    def one(t):
        name, actor, body, cap, n = t
        run(name, actor, body, cap, n, budget=budget)
        if not (RAW / (name + '.json')).exists():
            run(name, actor, body, 0.50, n, budget=budget)
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, todo))


def stage_fbtest():
    """19 Oct: which Facebook search finds the most posts about V7? Up to 10 results for each of the three keywords, from the eleven
    post-search scrapers with a track record in the Store (scraper_one is the one used since 17 Oct), four video and reel searches, a
    hashtag scraper, a search of public groups and Google limited to one month. A date range (20 Apr to 16 Oct) where the scraper takes one.
    Scored by fbtest_report.py (FB_KEYWORD_SCRAPERS.md)."""
    B = BUDGET_FBTEST
    todo = []
    go = lambda *a: todo.append(a)
    for i, k in enumerate(FB_TEST_K, 1):
        go(f'fbkw_scraperone_{i}', FB_SEARCH, {"query": k, "resultsCount": 10, "searchType": "top", "startDate": SINCE, "endDate": UNTIL}, 0.06, 10)
        go(f'fbkw_scrapeforge_{i}', 'scrapeforge~facebook-search-posts', {"query": k, "search_type": "posts", "max_results": 10, "start_date": SINCE, "end_date": UNTIL}, 0.06, 10)
        go(f'fbkw_apify_{i}', 'apify~facebook-search-scraper', {"categories": [k], "searchType": "posts", "resultsLimit": 10}, 0.08, 10)
        go(f'fbkw_danek_{i}', 'danek~facebook-search-ppr', {"query": k, "search_type": "posts", "max_posts": 10, "start_date": SINCE, "end_date": UNTIL}, 0.06, 10)
        go(f'fbkw_powerai_{i}', 'powerai~facebook-post-search-scraper', {"query": k, "maxResults": 10, "start_date": SINCE, "end_date": UNTIL}, 0.12, 10)
        go(f'fbkw_alienforce_{i}', 'alien_force~facebook-search-scraper', {"search_type": "posts", "keyword": k, "results_limit": 10, "start_date": SINCE,
                                                                            "end_date": UNTIL, "follow_post_scraping": True}, 0.15, 10)
        go(f'fbkw_fetchcat_{i}', 'fetch_cat~facebook-post-search-scraper', {"query": k, "resultsCount": 10, "searchType": "top", "startDate": SINCE, "endDate": UNTIL}, 0.08, 10)
        go(f'fbkw_mina_{i}', 'mina_safwat~facebook-search-actor', {"query": k, "limit": 10, "startDate": SINCE, "endDate": UNTIL}, 0.05, 10)
        go(f'fbkw_igview_{i}', 'igview-owner~facebook-old-posts-search', {"query": k, "maxResults": 10, "startDate": SINCE, "endDate": UNTIL}, 0.07, 10)
        go(f'fbkw_silentflow_{i}', 'silentflow~facebook-search-scraper', {"query": k, "search_type": "posts", "max_posts": 10, "start_date": SINCE, "end_date": UNTIL}, 0.05, 10)
        go(f'fbvs_apify_{i}', 'apify~facebook-video-search-scraper', {"searchTerm": k, "resultsLimit": 10}, 0.07, 10)
        go(f'fbvs_powerai_{i}', 'powerai~facebook-video-search-scraper', {"query": k, "maxResults": 10, "start_date": SINCE, "end_date": UNTIL}, 0.07, 10)
        go(f'fbreels_apify_{i}', 'apify~facebook-search-scraper', {"categories": [k], "searchType": "reels", "resultsLimit": 10}, 0.08, 10)
    go('fbkw_topapi', 'topapi~facebook-search-posts-scraper', {"searchQueries": FB_TEST_K, "sortBy": "top", "startDate": SINCE, "endDate": UNTIL,
                                                               "maxPostsPerQuery": 10, "includePostDetails": False}, 0.12, 30)
    go('fbkw_headply', 'headply~facebook-post-search-scraper', {"searchQueries": FB_TEST_K, "searchSort": "top", "maxItemsPerTarget": 10, "mode": "postSearch"}, 0.20, 30)
    go('fbvs_headply', 'headply~facebook-video-search-scraper', {"searchQueries": FB_TEST_K, "maxItemsPerTarget": 10, "mode": "videoSearch"}, 0.20, 30)
    go('fbvs_axesso', 'axesso_data~facebook-video-search-scraper', {"input": [{"keyword": k, "sort": "RELEVANCE", "maxPosts": 10} for k in FB_TEST_K]}, 0.05, 30)
    go('fbtags_apify', 'apify~facebook-hashtag-scraper', {"keywordList": ['v7egypt', 'ڤي_سڤن', 'vsupersoda', 'ڤيسڤن'], "resultsLimit": 10}, 0.25, 40)
    go('fbgroups_lofo', 'lofomachines~facebook-groups-posts-search-scraper', {"keywords": ['V7 drink', 'ڤي سڤن'], "afterDate": "this_year", "maxPosts": 10,
                                                                               "countryCode": "eg"}, 0.10, 20)
    import urllib.parse
    g = lambda q, a, b: 'https://www.google.com/search?' + urllib.parse.urlencode({'q': q + ' site:facebook.com', 'tbs': 'cdr:1,cd_min:%s,cd_max:%s' % (a, b)})
    go('fbgoogle_month', GOOGLE, {"queries": '\n'.join([g('"ڤي سڤن"', '6/1/2026', '6/30/2026'), g('"V7 cream soda"', '8/1/2026', '8/31/2026'), g('"ڤي كولا"', '6/1/2026', '6/30/2026')]),
                                  "maxPagesPerQuery": 2, "countryCode": "eg"}, 0.50, 6)
    parallel(todo, B)


FB_SAMPLE_VIDEOS = ['https://www.facebook.com/reel/1807300737278091/', 'https://www.facebook.com/reel/1740716823817554/', 'https://www.facebook.com/reel/2258238494941774/',
                    'https://www.facebook.com/reel/1376978311275889/', 'https://www.facebook.com/reel/1130641049532209/']   # creators' V7 reels with speech (19 Oct sample)
FB_SAMPLE_PHOTOS = ['https://www.facebook.com/kareem.hesham.1988/posts/pfbid0QRmo11NFjsvnvZFByBk9ETsjv2bxf1nTdqZrofFsBGH4QL7qQQR3DBj6CLqBWgRSl',
                    'https://www.facebook.com/MaxABco/posts/pfbid034CXY2Y6DF2Vvb6g8yLjjrdBnMLVz352LjVPbr3Raivr6UX3wMatDwARchZxK7f9Hl',
                    'https://www.facebook.com/nancy.wahba.104/posts/pfbid06bLP5LWzDtFyaSqipxpyviv4e71Y7fho1X6e2x27RbUy5vqFH7UAkLMzVV1T2CQSl']
FB_SAMPLE_PAGES = ['https://www.facebook.com/MaxABco', 'https://www.facebook.com/AkramTasteTest', 'https://www.facebook.com/cairo360',
                   'https://www.facebook.com/SeoudiSupermarket', 'https://www.facebook.com/TalabatEG']


def stage_fbtest2():
    """19 Oct: (1) how deep the cheapest complete Facebook searches go (60 results for ڤي سڤن, top and most recent, and one month at a time);
    (2) on a sample of five creators' V7 reels and three photo posts, which scrapers fill the gaps the searches leave: the video's views,
    what's said in it, the comments, and the page's followers."""
    B = BUDGET_FBTEST2
    todo = []
    go = lambda *a: todo.append(a)
    k = 'ڤي سڤن'
    go('fbdeep_silentflow_top', 'silentflow~facebook-search-scraper', {"query": k, "search_type": "posts", "max_posts": 60, "start_date": SINCE, "end_date": UNTIL}, 0.20, 60)
    go('fbdeep_silentflow_recent', 'silentflow~facebook-search-scraper', {"query": k, "search_type": "posts", "max_posts": 60, "recent_posts": True, "start_date": SINCE,
                                                                          "end_date": UNTIL}, 0.20, 60)
    go('fbdeep_topapi_top', 'topapi~facebook-search-posts-scraper', {"searchQueries": [k], "sortBy": "top", "startDate": SINCE, "endDate": UNTIL, "maxPostsPerQuery": 60}, 0.20, 60)
    go('fbdeep_topapi_recent', 'topapi~facebook-search-posts-scraper', {"searchQueries": [k], "sortBy": "recent", "startDate": SINCE, "endDate": UNTIL, "maxPostsPerQuery": 60}, 0.20, 60)
    go('fbdeep_scrapeforge_top', 'scrapeforge~facebook-search-posts', {"query": k, "search_type": "posts", "max_results": 60, "start_date": SINCE, "end_date": UNTIL}, 0.20, 60)
    go('fbdeep_month_silentflow', 'silentflow~facebook-search-scraper', {"query": k, "search_type": "posts", "max_posts": 30, "start_date": "2026-06-01",
                                                                         "end_date": "2026-06-30"}, 0.10, 30)
    go('fbdeep_month_topapi', 'topapi~facebook-search-posts-scraper', {"searchQueries": [k], "sortBy": "top", "startDate": "2026-06-01", "endDate": "2026-06-30",
                                                                       "maxPostsPerQuery": 30}, 0.10, 30)
    go('fbgap_topapi_details', 'topapi~facebook-search-posts-scraper', {"searchQueries": ['V7 كريم صودا'], "sortBy": "top", "startDate": SINCE, "endDate": UNTIL,
                                                                        "maxPostsPerQuery": 10, "includePostDetails": True}, 0.08, 10)
    links = FB_SAMPLE_VIDEOS + FB_SAMPLE_PHOTOS
    go('fbgap_danek', 'danek~facebook-posts-fast', {"direct_urls": [{"url": u} for u in links]}, 0.05, 10)
    go('fbgap_apifyposts', FB_POSTS, {"startUrls": [{"url": u} for u in links], "captionText": True}, 0.10, 10)
    go('fbgap_playcount', 'social_developer~facebook-playcount-scraper', {"startUrls": [{"url": u} for u in FB_SAMPLE_VIDEOS]}, 0.05, 5)
    go('fbgap_reeldetails', 'alpha-scraper~facebook-reels-details-scraper-pro', {"startUrls": [{"url": u} for u in FB_SAMPLE_VIDEOS]}, 0.05, 5)
    go('fbsp_piotr', 'piotrv1001~facebook-video-transcript-scraper', {"pages": [], "videoUrls": FB_SAMPLE_VIDEOS, "transcribeWithAI": True, "language": "auto",
                                                                      "maxResults": 5}, 0.40, 5)
    go('fbsp_sian', 'sian.agency~facebook-ai-transcript-extractor', {"bulkUrls": FB_SAMPLE_VIDEOS}, 0.15, 5)
    go('fbsp_viral', 'viralanalyzer~video-transcriber', {"mediaUrls": FB_SAMPLE_VIDEOS, "language": "ar", "model": "small", "maxMinutesPerItem": 5}, 0.40, 5)
    go('fbsp_invideo', 'invideoiq~video-transcriber', {"video_urls": FB_SAMPLE_VIDEOS}, 0.30, 5)
    go('fbsp_codenest', 'codenest~facebook-video-transcript-scraper', {"post_urls": [{"url": u} for u in FB_SAMPLE_VIDEOS]}, 0.05, 5)
    go('fbsp_alpha', 'alpha-scraper~facebook-transcript-subtitle-scraper', {"videoUrls": [{"url": u} for u in FB_SAMPLE_VIDEOS], "outputFormat": "all_type"}, 0.05, 5)
    cm_posts = [FB_SAMPLE_PHOTOS[0], FB_SAMPLE_PHOTOS[1], FB_SAMPLE_VIDEOS[0]]
    go('fbcm_apify', FB_COMMENTS, {"startUrls": [{"url": u} for u in cm_posts], "resultsLimit": 30, "includeNestedComments": False}, 0.30, 90)
    go('fbcm_thedoor', 'thedoor~facebook-comment-scraper', {"postUrls": cm_posts, "targetComments": 30, "includeReplies": False, "orderingMode": "MOST_RELEVANT"}, 0.10, 90)
    go('fbpages_apify', 'apify~facebook-pages-scraper', {"startUrls": [{"url": u} for u in FB_SAMPLE_PAGES]}, 0.08, 5)
    parallel(todo, B)


# ------------------------------------------------------------------ 19 Oct: Facebook coverage (FB_KEYWORD_SCRAPERS.md, DECISIONS #143-#147)
# Facebook's search gives about 10-15 posts about V7 per keyword, then unrelated ones (people and shops named "Seven"); a month at a time
# returns the same noise. So: many keywords (ڤ spellings, mixed and English; not the ف ones), three search backends that rank differently,
# Facebook's video and reel searches, public groups, and Google one month at a time.
KW_FB = ['ڤي سڤن', 'ڤيسڤن', 'مشروب ڤي سڤن', 'ڤي سڤن كريم صودا', 'ڤي سڤن رمان', 'ڤي سڤن بينا كولادا', 'ڤي سڤن شعير', 'ڤي سڤن ليمون نعناع', 'ڤي كولا',
         'ڤي كولا دايت', 'ڤي اورانج', 'ڤي ليمون', 'ڤي سوبر صودا', 'V7 كريم صودا', 'V7 cream soda', 'V7 مشروب', 'مشروب V7', 'V7 رمان', 'V7 بينا كولادا',
         'V7 بلوبيري', 'V7 شعير', 'V7 بينك ليمونيد', 'V7 pink lemonade', 'V7 Egypt', 'V7 soda', 'V7 drink', 'V Cola', 'V Orange', 'V Super Soda', 'V7 كانز']
KW_FB_VIDEO = ['ڤي سڤن', 'مشروب ڤي سڤن', 'ڤي كولا', 'ڤي اورانج', 'V7 كريم صودا', 'V7 cream soda', 'V7 مشروب', 'V7 رمان', 'V7 Egypt', 'V7 drink', 'V Cola',
               'V Super Soda']
KW_FB_GROUPS = ['ڤي سڤن', 'ڤي كولا', 'V7 كريم صودا', 'مشروب V7', 'V7 drink', 'V Cola', 'ڤي اورانج', 'V7 رمان', 'V7 شعير', 'V Super Soda', 'ڤي سڤن سعر',
                'ڤي سڤن جملة']
G_PHRASES_FB = ['"ڤي سڤن"', '"ڤي كولا"', '"ڤى كولا"', '"V7 cream soda"', '"V7 كريم صودا"', '"V Cola" مصر', '"V Super Soda"', '"مشروب V7"', '"ڤي اورانج"',
                '"V7 Egypt"', '"V7 pink lemonade"', '"ڤيسڤن"']
FB_SILENT, FB_APIFY_SEARCH = 'silentflow~facebook-search-scraper', 'apify~facebook-search-scraper'
FB_V_HEADPLY, FB_V_AXESSO, FB_V_APIFY = 'headply~facebook-video-search-scraper', 'axesso_data~facebook-video-search-scraper', 'apify~facebook-video-search-scraper'
FB_GROUPS = 'lofomachines~facebook-groups-posts-search-scraper'
FB_REEL_DETAILS, FB_VIDEO_DETAILS = 'alpha-scraper~facebook-reels-details-scraper-pro', 'alpha-scraper~facebook-video-details-scraper'
FB_POST_LINK, FB_PLAYS, FB_PAGES = 'danek~facebook-posts-fast', 'social_developer~facebook-playcount-scraper', 'apify~facebook-pages-scraper'
FB_SPEECH, FB_CM_CHEAP = 'invideoiq~video-transcriber', 'thedoor~facebook-comment-scraper'
BUDGET_FB = 62.00   # 19 Oct: the Facebook work may spend up to here on the meter (USD 100 limit; about USD 34.1 spent before it)


def stage_fbcover():
    """19 Oct: Facebook public posts about V7, every route that tested well (fbtest, fbtest2): 30 keywords on three search backends
    (silentflow 20 each, scraper_one 20, Apify's search 10), Facebook's reel search and three video searches (12 keywords), public groups
    (12 keywords) and Google one month at a time (12 exact phrases x 7 months). New finds without their details get them in fbdetails."""
    import urllib.parse
    todo = []
    go = lambda *a: todo.append(a)
    for i, k in enumerate(KW_FB):
        go(f'fbc_silent_{i:02d}', FB_SILENT, {"query": k, "search_type": "posts", "max_posts": 20, "start_date": SINCE, "end_date": UNTIL}, 0.07, 20)
        go(f'fbc_one_{i:02d}', FB_SEARCH, {"query": k, "resultsCount": 20, "searchType": "top", "startDate": SINCE, "endDate": UNTIL}, 0.08, 20)
        go(f'fbc_apify_{i:02d}', FB_APIFY_SEARCH, {"categories": [k], "searchType": "posts", "resultsLimit": 10}, 0.08, 10)
    for i, k in enumerate(KW_FB_VIDEO):
        go(f'fbc_reels_{i:02d}', FB_APIFY_SEARCH, {"categories": [k], "searchType": "reels", "resultsLimit": 15}, 0.10, 15)
        go(f'fbc_vapify_{i:02d}', FB_V_APIFY, {"searchTerm": k, "resultsLimit": 15}, 0.10, 15)
    go('fbc_vheadply', FB_V_HEADPLY, {"searchQueries": KW_FB_VIDEO, "maxItemsPerTarget": 20, "mode": "videoSearch"}, 1.20, 240)
    go('fbc_vaxesso', FB_V_AXESSO, {"input": [{"keyword": k, "sort": "RELEVANCE", "maxPosts": 20} for k in KW_FB_VIDEO]}, 0.20, 240)
    go('fbc_groups', FB_GROUPS, {"keywords": KW_FB_GROUPS, "afterDate": "this_year", "maxPosts": 25, "countryCode": "eg"}, 1.60, 300)
    g = lambda q, a, b: 'https://www.google.com/search?' + urllib.parse.urlencode({'q': q + ' site:facebook.com', 'tbs': 'cdr:1,cd_min:%s,cd_max:%s' % (a, b)})
    go('fbc_google_months', GOOGLE, {"queries": '\n'.join(g(q, a, b) for q in G_PHRASES_FB for a, b in MONTHS), "maxPagesPerQuery": 2, "countryCode": "eg"},
       1.00, len(G_PHRASES_FB) * len(MONTHS) * 2)
    parallel(todo, BUDGET_FB)


FB_LOOSE = re.compile(r'v7|ڤي|ڤى|سڤن|v ?cola|super ?soda|كريم صودا|cream soda', re.I)   # a reel or video worth fetching by link


def fb_known():
    """The post ids and video ids in every Facebook row that has an exact time and its numbers (normalize.py reads these)."""
    import re as _re
    ids = set()
    pats = ('fb_search_*', 'fbc_one_*', 'fbc_silent_*', 'fbc_apify_*', 'fbc_vheadply', 'fbc_groups', 'fbd_*', 'fbkw_*', 'fbdeep_*', 'fbgap_*', 'fbvs_headply', 'fbgroups_lofo')
    for pat in pats:
        for f in RAW.glob(pat + '.json'):
            for x in json.load(open(f, encoding='utf-8')).get('items', []):
                if not isinstance(x, dict):
                    continue
                for k in ('postId', 'post_id', 'video_id', 'story_id'):
                    if x.get(k): ids.add(str(x[k]))
                v = x.get('video') if isinstance(x.get('video'), dict) else {}
                if v.get('id'): ids.add(str(v['id']))
                for u in (x.get('url'), x.get('post_url'), v.get('url')):
                    m = _re.search(r'(?:/reel/|/videos/(?:[^/?]+/)?|[?&]v=|/posts/(?:[^/?]+/)?|story_fbid=|/permalink/|[?&]fbid=)(\d{8,})', u or '')
                    if m: ids.add(m.group(1))
    return ids


def stage_fbdetails():
    """19 Oct: the reels and videos that the reel search and two video searches return without an exact time or numbers, and Facebook's
    posts that Google found month by month, fetched by link when they're new: reels, videos and posts alike with danek's details scraper
    (USD 0.0023; 1,736 users; in the test it gave reels' text, time, counts and plays). V7's own pages are left out. A reel or video is
    fetched only if its text names V7."""
    import re as _re
    known = fb_known()
    vids = {}
    for f in sorted(RAW.glob('fbc_reels_*.json')) + sorted(RAW.glob('fbreels_apify_*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            if x.get('postId') and x.get('url') and FB_LOOSE.search(x.get('caption') or '') and (x.get('authorName') or '').replace(' ', '').lower() not in ('v7egypt', 'vsupersoda'):
                vids[str(x['postId'])] = x['url']
    for f in [RAW / 'fbc_vaxesso.json', RAW / 'fbvs_axesso.json']:
        for x in (json.load(open(f, encoding='utf-8'))['items'] if f.exists() else []):
            if x.get('videoId') and x.get('videoUrl') and FB_LOOSE.search((x.get('title') or '') + ' ' + (x.get('description') or '')) and 'V7Egypt' not in (x.get('ownerUrl') or ''):
                vids[str(x['videoId'])] = x['videoUrl']
    for f in sorted(RAW.glob('fbc_vapify_*.json')) + sorted(RAW.glob('fbvs_apify_*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            u = x.get('videoUrl') or ''
            m = _re.search(r'(?:/reel/|/videos/(?:[^/?]+/)?|[?&]v=)(\d{8,})', u)
            if m and not u.endswith('undefined') and FB_LOOSE.search(json.dumps([x.get('title'), x.get('save_description'), x.get('label')], ensure_ascii=False)):
                vids[m.group(1)] = u
    posts = {}
    for f in [RAW / 'fbc_google_months.json', RAW / 'fbgoogle_month.json']:
        for page in (json.load(open(f, encoding='utf-8'))['items'] if f.exists() else []):
            for r in page.get('organicResults') or []:
                u = (r.get('url') or '').split('#')[0]
                if _re.search(r'facebook\.com/(?:V7Egypt|Vsupersoda)/', u, _re.I):
                    continue
                mv = _re.search(r'(?:/reel/|/videos/(?:[^/?]+/)?|[?&]v=)(\d{8,})', u)
                mp = _re.search(r'(?:/posts/(?:[^/?]+/)?|story_fbid=|/permalink/|[?&]fbid=|/photos/(?:[^/?]+/)?)(\d{8,}|pfbid\w+)', u)
                if mv: vids[mv.group(1)] = u
                elif mp: posts[mp.group(1)] = u
    new_v = {k: u for k, u in vids.items() if k not in known}
    new_p = {k: u for k, u in posts.items() if k not in known}
    log(f'  fbdetails: {len(vids)} reels and videos found ({len(new_v)} new), {len(posts)} Google post links ({len(new_p)} new)')
    links = list(new_v.values()) + list(new_p.values())   # danek's details scraper reads reels, videos and posts alike (text, time, counts, plays)
    if links:
        run('fbd_posts', FB_POST_LINK, {"direct_urls": [{"url": u} for u in links]}, round(len(links) * 0.00233 * 1.3 + 0.05, 2), len(links), budget=BUDGET_FB)


def _fb_public():
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    posts = [i for i in items if i['src'] == 'ugc' and i['kind'] == 'post' and i['pl'] == 'fb' and i.get('url')]
    return posts, labels


def stage_fbfill():
    """19 Oct: fills the gaps of the public Facebook posts about V7 (after normalize.py and label.py):
    - exact plays for reels and videos without a view count (social_developer, USD 0.004 a video);
    - what's said in reels and videos (invideoiq's transcriber, USD 0.035 a video; it read all five test reels, Facebook's own captions three);
      also the videos whose text is too short to tell what they're about;
    - the followers and category of the pages, creators, businesses and news outlets that posted (Apify's page scraper, USD 0.0082 a page);
    - the comments under them, up to 100 a post (thedoor, USD 0.0005 a comment); fbfill2 sends the posts it returns nothing for to
      Apify's own comment scraper."""
    posts, labels = _fb_public()
    about = lambda i: (labels.get(i['id']) or {}).get('about')
    tag = time.strftime('%Y%m%d%H%M')
    vids = [i for i in posts if i.get('fmt') in ('Reel', 'Video') and (about(i) or len(i.get('text') or '') < 30)]
    done_sp = set()
    for f in RAW.glob('fbf_speech_*.json'):
        done_sp |= {(x.get('video_url') or x.get('url') or '').split('?')[0].rstrip('/') for x in json.load(open(f, encoding='utf-8'))['items']}
    nosp = [i for i in vids if not i.get('speech') and i['url'].split('?')[0].rstrip('/') not in done_sp]
    noviews = [i for i in vids if about(i) and not i.get('views')]
    seg_ok = ('page', 'creator', 'business', 'news')
    page_urls = sorted({(i.get('author') or {}).get('url').split('?')[0].rstrip('/') for i in posts if about(i) and (labels.get(i['id']) or {}).get('seg') in seg_ok
                        and (i.get('author') or {}).get('url') and not (i.get('author') or {}).get('followers')})
    done_cm = set()
    for f in RAW.glob('fbcm_*.json'):
        done_cm |= {x.get('post_url') or x.get('facebookUrl') or x.get('inputUrl') for x in json.load(open(f, encoding='utf-8'))['items']}
    cm = [i for i in posts if about(i) and (i.get('comments') or 0) > 0 and i['url'] not in done_cm]
    n_cm = sum(min(i['comments'], 100) for i in cm)
    log(f'  fbfill: {len(noviews)} videos without views, {len(nosp)} videos to transcribe, {len(page_urls)} pages, {len(cm)} posts with about {n_cm} comments')
    todo = []
    if noviews:
        todo.append(('fbf_plays_' + tag, FB_PLAYS, {"startUrls": [{"url": i['url']} for i in noviews]}, round(len(noviews) * 0.004 * 1.3 + 0.05, 2), len(noviews)))
    if nosp:
        todo.append(('fbf_speech_' + tag, FB_SPEECH, {"video_urls": [i['url'] for i in nosp]}, round(len(nosp) * 0.035 * 1.5 + 0.10, 2), len(nosp)))
    if page_urls:
        todo.append(('fbf_pages_' + tag, FB_PAGES, {"startUrls": [{"url": u} for u in page_urls]}, round(len(page_urls) * 0.0082 * 1.3 + 0.05, 2), len(page_urls)))
    if cm:
        todo.append(('fbcm_door_' + tag, FB_CM_CHEAP, {"postUrls": [i['url'] for i in cm], "targetComments": 100, "includeReplies": False,
                                                       "orderingMode": "MOST_RELEVANT"}, round(n_cm * 0.0005 * 1.3 + 0.10, 2), n_cm + 50))
    parallel(todo, BUDGET_FB)


def stage_fbviews():
    """19 Oct: the video posts about V7 whose link is a post link (a permalink or a group post), so the play count scraper can't read them,
    fetched by link with danek's details scraper, which returns the video's id and plays."""
    posts, labels = _fb_public()
    todo = [i for i in posts if (labels.get(i['id']) or {}).get('about') and i.get('fmt') in ('Reel', 'Video') and not i.get('views')]
    log(f'  fbviews: {len(todo)} video posts without plays')
    if todo:
        run('fbd_posts_views', FB_POST_LINK, {"direct_urls": [{"url": i['url']} for i in todo]}, round(len(todo) * 0.00233 * 1.3 + 0.05, 2), len(todo), budget=BUDGET_FB)


def stage_fbnames():
    """19 Oct: the few public Facebook posts about V7 whose search row came without the account's name, fetched by link (danek)."""
    posts, labels = _fb_public()
    todo = [i for i in posts if (labels.get(i['id']) or {}).get('about') and not (i.get('author') or {}).get('name')]
    log(f'  fbnames: {len(todo)} posts without the account name')
    if todo:
        run('fbd_posts_names', FB_POST_LINK, {"direct_urls": [{"url": i['url']} for i in todo]}, round(len(todo) * 0.00233 * 1.3 + 0.05, 2), len(todo), budget=BUDGET_FB)


def stage_fbfill2():
    """19 Oct: the posts thedoor returned no comments for get them from Apify's own comment scraper (USD 0.0023 a comment), up to 100 a post."""
    posts, labels = _fb_public()
    got = set()
    for f in RAW.glob('fbcm_*.json'):
        got |= {(x.get('post_url') or x.get('facebookUrl') or x.get('inputUrl') or '') for x in json.load(open(f, encoding='utf-8'))['items']}
    cm = [i for i in posts if (labels.get(i['id']) or {}).get('about') and (i.get('comments') or 0) > 0 and i['url'] not in got]
    n = sum(min(i['comments'], 100) for i in cm)
    log(f'  fbfill2: {len(cm)} posts without comments, about {n} comments')
    if cm:
        run('fbcm_official_' + time.strftime('%Y%m%d%H%M'), FB_COMMENTS, {"startUrls": [{"url": i['url']} for i in cm], "resultsLimit": 100,
                                                                           "includeNestedComments": False}, round(n * 0.0023 * 1.2 + 0.05, 2), n + 50, budget=BUDGET_FB)


BUDGET_FBTEST2 = 36.00   # 19 Oct: the depth and gap tests may spend up to here on the meter (about USD 3 over the 33.03 spent; expected about 1.6)
BUDGET_FBTEST = 34.00   # 19 Oct: the Facebook comparison may spend up to here on the meter (about USD 3.7 over the 30.31 spent; expected about 2)


STAGES = {'fbnames': stage_fbnames, 'fbviews': stage_fbviews, 'fbfill2': stage_fbfill2, 'fbfill': stage_fbfill, 'fbdetails': stage_fbdetails, 'fbcover': stage_fbcover, 'fbtest2': stage_fbtest2, 'fbtest': stage_fbtest, 'igcomments2': stage_igcomments2, 'igcomments': stage_igcomments, 'igvisfetch': stage_igvisfetch, 'igcover': stage_igcover, 'covtest': stage_covtest, 'vistest2': stage_vistest2, 'vistest': stage_vistest, 'igspeech': stage_igspeech, 'igprofiles': stage_igprofiles, 'transcripttest': stage_transcripttest, 'refetchtest': stage_refetchtest, 'igkw': stage_igkw, 'kwdeep': stage_kwdeep, 'kwtest': stage_kwtest, 'ttkw': stage_ttkw, 'ytc': stage_ytc, 'ytcheck': stage_ytcheck, 'test': stage_test, 'own': stage_own, 'comments': stage_comments, 'abroad': stage_abroad, 'ugc': stage_ugc, 'test2': stage_test2, 'wide': stage_wide,
          'test3': stage_test3}

if __name__ == '__main__':
    stage = sys.argv[1] if len(sys.argv) > 1 else ''
    if stage not in STAGES:
        sys.exit('Usage: python3 collect.py ' + '|'.join(STAGES) + ' [--force]')
    log(f'--- stage {stage}, spent so far this cycle ${spent():.4f}, budget ${BUDGET:.2f}')
    STAGES[stage]()
    log(f'--- stage {stage} done, spent this cycle ${spent():.4f}')
