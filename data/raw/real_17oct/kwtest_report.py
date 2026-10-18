"""19 Oct 2026: scores the Instagram keyword scrapers tested by `collect.py kwtest` on the same three keywords (V7 soda, ڤي سڤن,
V7 كريم صودا; quoted for the scrapers that take exact phrases). For each scraper: posts returned, posts with a date inside
20 Apr to 16 Oct, posts about V7 (a caption, hashtag or account naming V7, its Arabic spelling with ڤ or its V Cola line, and not
the Haval V7 car), which numbers come back, and the cost of each useful post (about V7 and inside the window).
Usage: python3 kwtest_report.py   (APIFY_API_TOKEN in the environment to read each run's final charge)"""
import collections, datetime, json, os, pathlib, re, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
SINCE, UNTIL = '2026-04-20', '2026-10-16'
K = ['V7 soda', 'ڤي سڤن', 'V7 كريم صودا']
GROUPS = [   # scraper, Store link, its runs (one keyword each, or all three in one run)
    ('apidojo', 'apidojo/instagram-scraper-api', ['kw_apidojo_1', 'kw_apidojo_2', 'kw_apidojo_3']),
    ('apify search (popular reels)', 'apify/instagram-search-scraper', ['kw_apify_search']),
    ('memo23 (exact phrases)', 'memo23/instagram-reels-search-scraper', ['kw_memo23']),
    ('scraping_solutions (exact phrases)', 'scraping_solutions/instagram-boolean-search-scraper-posts-reels', ['kw_boolean_1', 'kw_boolean_2', 'kw_boolean_3']),
    ('data-slayer reels', 'data-slayer/instagram-search-reels', ['kw_dataslayer_1', 'kw_dataslayer_2', 'kw_dataslayer_3']),
    ('dami_studio reels', 'dami_studio/instagram-reels-search-scraper', ['kw_dami']),
    ('seemuapps (used 18 Oct)', 'seemuapps/instagram-keyword-posts-scraper', ['kw_seemuapps']),
]
ABOUT = re.compile(r'(?<![\w.])v7(?![\w])|ڤي ?سڤن|ڤى ?سڤن|ڤيسڤن|v7egypt|v7\.egypt|vsupersoda|v\.super\.soda|super ?soda|ڤي ?كولا|ڤى ?كولا|(?<![\w])v ?cola(?![\w])|ڤي ?(?:أ|ا)ورانج|(?<![\w])v orange(?![\w])', re.I)
NOT_V7 = re.compile(r'haval|هافال|great ?wall', re.I)
OWN = {'v7egypt', 'v7.egypt', 'vsupersoda', 'v.super.soda', 'v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco'}   # V7's own accounts: already collected, not public posts


def pick(x, *keys):
    for k in keys:
        v = x
        for part in k.split('.'):
            v = v.get(part) if isinstance(v, dict) else None
        if v not in (None, ''):
            return v
    return None


def day(v):
    if v is None:
        return None
    if isinstance(v, (int, float)) or re.fullmatch(r'\d{10,13}', str(v)):
        f = float(v)
        return datetime.datetime.fromtimestamp(f / 1000 if f > 1e11 else f, datetime.timezone.utc).date().isoformat()
    m = re.match(r'(\d{4}-\d\d-\d\d)', str(v))
    return m.group(1) if m else None


def post(x, run_kw):
    url = pick(x, 'url', 'postUrl', 'post_url', 'permalink', 'link', 'reelUrl', 'reel_url')
    code = pick(x, 'shortcode', 'shortCode', 'code', 'postCode', 'post_code')
    if not code and url:
        m = re.search(r'/(?:p|reel|reels|tv)/([\w-]{6,})', str(url))
        code = m.group(1) if m else None
    if not code:
        return None
    cap = pick(x, 'caption.text', 'captionText', 'caption', 'text', 'description')
    cap = cap if isinstance(cap, str) else ''
    tags = pick(x, 'hashtags') or []
    owner = pick(x, 'ownerUsername', 'username', 'owner.username', 'user.username', 'author.username', 'authorUsername', 'creator.username', 'author.handle')
    own = str(owner or '').lower() in OWN
    words = ' '.join([str(cap or ''), ' '.join(map(str, tags)) if isinstance(tags, list) else str(tags), str(owner or ''),
                      ' '.join(map(str, pick(x, 'mentions') or [])) if isinstance(pick(x, 'mentions'), list) else ''])
    kw = pick(x, 'keyword', 'inputSource', 'sourceQuery', 'discoveryQuery', 'query', 'searchQuery', 'searchTerm', 'search_term', 'searchKeyword') or run_kw
    return {'code': code, 'kw': str(kw or '').strip('"'), 'day': day(pick(x, 'takenAt', 'timestamp', 'taken_at', 'takenAtTimestamp', 'taken_at_timestamp', 'createdAt',
                                                                         'created_at', 'publishedAt', 'postedAt', 'posted_at', 'date', 'time')),
            'about': bool(ABOUT.search(words)) and not NOT_V7.search(words) and not own, 'own': own, 'cap': str(cap or '').replace('\n', ' '), 'owner': owner,
            'likes': pick(x, 'likeCount', 'likesCount', 'like_count', 'likes', 'metrics.likes'), 'comments': pick(x, 'commentCount', 'commentsCount', 'comment_count', 'comments', 'metrics.comments'),
            'views': pick(x, 'playCount', 'videoPlayCount', 'play_count', 'ig_play_count', 'playsCount', 'views', 'viewCount', 'video_view_count', 'videoViewCount', 'plays', 'metrics.plays', 'video.playCount', 'video.viewCount')}


def charge(body):
    tok, rid = os.environ.get('APIFY_API_TOKEN'), (body.get('run') or {}).get('id')
    if tok and rid:
        r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok}), timeout=40))['data']
        return r.get('usageTotalUsd') or 0, r.get('status')
    return body.get('cost_usd') or 0, (body.get('run') or {}).get('status')


def main():
    out = []
    for label, link, runs in GROUPS:
        posts, cost, notes = {}, 0.0, []
        for name in runs:
            f = RAW / (name + '.json')
            if not f.exists():
                notes.append(name + ' did not run'); continue
            body = json.load(open(f, encoding='utf-8'))
            c, status = charge(body); cost += c
            if status != 'SUCCEEDED': notes.append('%s %s' % (name, status))
            inp = body.get('input') or {}
            run_kw = (inp.get('keywords') or [None])[0] if len(inp.get('keywords') or []) == 1 else inp.get('query') or inp.get('searchQuery')
            for x in body.get('items') or []:
                p = post(x, run_kw)
                if p and p['code'] not in posts:
                    posts[p['code']] = p
        ps = list(posts.values())
        inwin = [p for p in ps if p['day'] and SINCE <= p['day'] <= UNTIL]
        useful = [p for p in inwin if p['about']]
        per_kw = {k: (sum(1 for p in ps if p['kw'] == k), sum(1 for p in ps if p['kw'] == k and p['about'])) for k in K}
        has = {f: sum(1 for p in ps if p[f] is not None) for f in ('day', 'likes', 'comments', 'views')}
        notes.append('%d by V7’s own accounts' % sum(1 for p in ps if p['own']))
        out.append((label, link, len(ps), len(inwin), sum(1 for p in ps if p['about']), len(useful), cost, per_kw, has, notes, ps))
    print('%-36s %5s %8s %6s %7s %8s %s' % ('scraper', 'posts', 'inWindow', 'aboutV7', 'useful', 'cost', 'per keyword (about V7 / returned)'))
    for label, link, n, w, a, u, cost, per_kw, has, notes, ps in out:
        print('%-36s %5d %8d %6d %7d  $%.3f  %s %s' % (label, n, w, a, u, cost, '  '.join('%s %d/%d' % (k, v[1], v[0]) for k, v in per_kw.items()),
                                                    ('| ' + '; '.join(notes)) if notes else ''))
        print('%36s fields: date %d, likes %d, comments %d, views %d of %d%s' % ('', has['day'], has['likes'], has['comments'], has['views'], n,
                                                                              ' | per useful post $%.4f' % (cost / u) if u else ''))
    print('\nArabic keyword (ڤي سڤن), first captions per scraper:')
    for label, link, n, w, a, u, cost, per_kw, has, notes, ps in out:
        ar = [p for p in ps if p['kw'] == 'ڤي سڤن'][:4]
        print(' ', label)
        for p in ar:
            print('     %s %-5s %-18s %s' % (p['day'], 'V7' if p['about'] else '-', str(p['owner'] or '')[:18], p['cap'][:70]))
    return out


if __name__ == '__main__':
    main()
