"""19 Oct 2026: scores the Facebook search scrapers tested by `collect.py fbtest` on the same three keywords as the Instagram comparison
(V7 soda, ڤي سڤن, V7 كريم صودا). For each scraper: posts returned, posts dated inside 20 Apr to 16 Oct, posts about V7 (a text, hashtag
or account naming V7, its Arabic spelling with ڤ or its V Cola line, and not the Haval V7 car), which numbers come back (reactions,
comments, shares, video views, the account's followers), and the cost of each useful post (about V7, inside the window, not V7's own page).
Then how much the scrapers overlap: no single one finds everything.
Usage: python3 fbtest_report.py   (APIFY_API_TOKEN in the environment to read each run's final charge)"""
import collections, datetime, json, os, pathlib, re, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
SINCE, UNTIL = '2026-04-20', '2026-10-16'
K = ['V7 soda', 'ڤي سڤن', 'V7 كريم صودا']
GROUPS = [   # label, Store link, kind, runs
    ('scraper_one (used since 17 Oct)', 'scraper_one/facebook-posts-search', 'posts', ['fbkw_scraperone_1', 'fbkw_scraperone_2', 'fbkw_scraperone_3']),
    ('scrapeforge', 'scrapeforge/facebook-search-posts', 'posts', ['fbkw_scrapeforge_1', 'fbkw_scrapeforge_2', 'fbkw_scrapeforge_3']),
    ('apify search (posts)', 'apify/facebook-search-scraper', 'posts', ['fbkw_apify_1', 'fbkw_apify_2', 'fbkw_apify_3']),
    ('danek', 'danek/facebook-search-ppr', 'posts', ['fbkw_danek_1', 'fbkw_danek_2', 'fbkw_danek_3']),
    ('powerai', 'powerai/facebook-post-search-scraper', 'posts', ['fbkw_powerai_1', 'fbkw_powerai_2', 'fbkw_powerai_3']),
    ('alien_force', 'alien_force/facebook-search-scraper', 'posts', ['fbkw_alienforce_1', 'fbkw_alienforce_2', 'fbkw_alienforce_3']),
    ('fetch_cat', 'fetch_cat/facebook-post-search-scraper', 'posts', ['fbkw_fetchcat_1', 'fbkw_fetchcat_2', 'fbkw_fetchcat_3']),
    ('mina_safwat', 'mina_safwat/facebook-search-actor', 'posts', ['fbkw_mina_1', 'fbkw_mina_2', 'fbkw_mina_3']),
    ('igview-owner (old posts)', 'igview-owner/facebook-old-posts-search', 'posts', ['fbkw_igview_1', 'fbkw_igview_2', 'fbkw_igview_3']),
    ('silentflow', 'silentflow/facebook-search-scraper', 'posts', ['fbkw_silentflow_1', 'fbkw_silentflow_2', 'fbkw_silentflow_3']),
    ('topapi', 'topapi/facebook-search-posts-scraper', 'posts', ['fbkw_topapi']),
    ('headply (posts)', 'headply/facebook-post-search-scraper', 'posts', ['fbkw_headply']),
    ('apify search (reels)', 'apify/facebook-search-scraper', 'reels', ['fbreels_apify_1', 'fbreels_apify_2', 'fbreels_apify_3']),
    ('apify video search', 'apify/facebook-video-search-scraper', 'videos', ['fbvs_apify_1', 'fbvs_apify_2', 'fbvs_apify_3']),
    ('powerai video search', 'powerai/facebook-video-search-scraper', 'videos', ['fbvs_powerai_1', 'fbvs_powerai_2', 'fbvs_powerai_3']),
    ('headply video search', 'headply/facebook-video-search-scraper', 'videos', ['fbvs_headply']),
    ('axesso video search', 'axesso_data/facebook-video-search-scraper', 'videos', ['fbvs_axesso']),
    ('apify hashtags (4 tags)', 'apify/facebook-hashtag-scraper', 'hashtags', ['fbtags_apify']),
    ('lofomachines groups (2 other keywords)', 'lofomachines/facebook-groups-posts-search-scraper', 'groups', ['fbgroups_lofo']),
]
ABOUT = re.compile(r'(?<![\w.])v7(?![\w])|ڤي ?سڤن|ڤى ?سڤن|ڤيسڤن|v7egypt|v7\.egypt|vsupersoda|v\.super\.soda|super ?soda|ڤي ?كولا|ڤى ?كولا|(?<![\w])v ?cola(?![\w])'
                   r'|ڤي ?(?:أ|ا)ورانج|(?<![\w])v orange(?![\w])', re.I)
NOT_V7 = re.compile(r'haval|هافال|great ?wall|jaecoo|chery', re.I)
OWN = re.compile(r'facebook\.com/(?:V7Egypt|Vsupersoda)(?:[/?]|$)|^(?:V7 ?Egypt|V Super Soda|V7)$', re.I)   # V7's own pages: collected elsewhere


def pick(x, *keys):
    for k in keys:
        v = x
        for part in k.split('.'):
            v = v.get(part) if isinstance(v, dict) else None
        if v not in (None, '', [], {}):
            return v
    return None


def day(v):
    if v is None:
        return None
    if isinstance(v, (int, float)) or re.fullmatch(r'\d{9,13}', str(v)):
        f = float(v)
        return datetime.datetime.fromtimestamp(f / 1000 if f > 1e11 else f, datetime.timezone.utc).date().isoformat()
    m = re.match(r'(\d{4}-\d\d-\d\d)', str(v))
    return m.group(1) if m else None


def num(v):
    if isinstance(v, dict):
        v = v.get('count', v.get('total'))
    try:
        return int(float(str(v).replace(',', '')))
    except (TypeError, ValueError):
        return None


MON = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}


def day_of_raw(s):
    """Video search rows give '21 Aug · 2.2K views' or 'March 3, 2025' or '3 days ago': the day where it can be read (19 Oct 2026 is today)."""
    s = s.lower()
    m = re.search(r'(\d{1,2}) (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*(?:,? (\d{4}))?', s) or re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w* (\d{1,2})(?:,? (\d{4}))?', s)
    if m:
        a, b, y = m.groups()
        d, mo = (int(a), MON[b]) if a.isdigit() else (int(b), MON[a])
        y = int(y) if y else (2026 if mo <= 10 else 2025)
        return '%04d-%02d-%02d' % (y, mo, d)
    m = re.search(r'(\d+) (minute|hour|day|week|month|year)s? ago', s)
    if m:
        n, u = int(m.group(1)), m.group(2)
        days = n * {'minute': 0, 'hour': 0, 'day': 1, 'week': 7, 'month': 30, 'year': 365}[u]
        return (datetime.date(2026, 10, 19) - datetime.timedelta(days=days)).isoformat()
    return None


def views_of_raw(s):
    m = re.search(r'([\d.,]+)\s*([km]?)\s*views', s.lower())
    if not m:
        return None
    v = float(m.group(1).replace(',', ''))
    return int(v * {'k': 1e3, 'm': 1e6, '': 1}[m.group(2)])


def key_of(url, pid):
    """One key per post, whatever the link's shape: the numeric id in it (story_fbid, /posts/, /videos/, /reel/, v=, fbid=)."""
    u = str(url or '')
    m = (re.search(r'(?:story_fbid=|/posts/|/videos/(?:[\w.-]+/)?|/reel/|[?&]v=|fbid=|/permalink/|/watch/\?v=)(\d{8,})', u)
         or re.search(r'/(pfbid\w+)', u))
    return m.group(1) if m else (str(pid) if pid else (u.split('?')[0].rstrip('/') or None))


def post(x, run_kw):
    url = pick(x, 'url', 'post_url', 'permalink_url', 'video_url', 'postUrl', 'link', 'permalink', 'reelUrl', 'reel_url', 'shareable_url', 'topLevelUrl', 'videoUrl')
    if url and (str(url).endswith('undefined') or '/search' in str(url)):
        url = None
    pid = pick(x, 'postId', 'post_id', 'video_id', 'videoId', 'id')
    k = key_of(url, pid)
    if not k:
        return None
    text = pick(x, 'postText', 'message', 'text', 'caption', 'title.text', 'description', 'title', 'content', 'post_text', 'body')
    text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False) if text else ''
    author = pick(x, 'author.name', 'user.name', 'pageName.name', 'owner_name', 'authorName', 'ownerName', 'author_name', 'video_owner_profile.name', 'owner.name',
                  'author_title', 'author_username')
    aurl = pick(x, 'author.url', 'author.profileUrl', 'user.profileUrl', 'user.url', 'authorUrl', 'ownerUrl', 'video_owner_profile.url', 'owner.url', 'author_url')
    raw_tv = str(pick(x, 'time_and_views_raw', 'relativeTime', 'relative_time_string') or '')
    tags = pick(x, 'hashtags') or []
    words = ' '.join([text, ' '.join(map(str, tags)) if isinstance(tags, list) else str(tags), str(author or '')])
    own = bool(OWN.search(str(aurl or '')) or OWN.search(str(author or '').strip()))
    kw = pick(x, 'searchQuery', 'search_query', 'source.target', 'inputKeyword', 'searchKeyword', 'keyword', 'query', 'searchTerm') or run_kw
    return {'key': k, 'url': url, 'kw': str(kw or '').strip('"#'), 'day': day(pick(x, 'publishedAt', 'published_at', 'createdAt', 'create_time', 'time', 'timestamp', 'date',
                                                                                  'created_time', 'creation_time', 'publish_time', 'uploadDate')) or day_of_raw(raw_tv),
            'about': bool(ABOUT.search(words)) and not NOT_V7.search(words) and not own, 'own': own, 'text': text.replace('\n', ' '), 'author': author,
            'reactions': num(pick(x, 'reactionsCount', 'reactions_count', 'reactionCount', 'reaction_count', 'statistics.reaction_count', 'like_count', 'likes', 'topReactionsCount')),
            'comments': num(pick(x, 'commentsCount', 'comments_count', 'commentCount', 'comment_count', 'statistics.comment_count', 'comments')),
            'shares': num(pick(x, 'sharesCount', 'reshare_count', 'shareCount', 'share_count', 'statistics.shares_count', 'shares')),
            'views': num(pick(x, 'video_view_count', 'videoPostViewCount', 'videoViewCount', 'statistics.video_view_count', 'play_count', 'view_count', 'viewsCount', 'views',
                              'playCount')) or views_of_raw(raw_tv),
            'followers': num(pick(x, 'author.followers', 'author.followersCount', 'user.followers', 'pageFollowers', 'followers', 'author_followers', 'owner.followers',
                                  'author.followers_count', 'followersCount')),
            'video': bool(re.search(r'/reel/|/videos?/|watch', str(url or '')) or str(pick(x, 'postType', 'type') or '') in ('reel', 'video', 'search_video')
                          or pick(x, 'video', 'videoUrl', 'video_url', 'video_list', 'isVideo', 'playable_url', 'durationMs', 'videoDurationText')
                          or any(isinstance(a, dict) and 'video' in str(a.get('type', '')).lower() for a in (pick(x, 'attachments', 'media') or [])))}


def charge(body):
    tok, rid = os.environ.get('APIFY_API_TOKEN'), (body.get('run') or {}).get('id')
    if tok and rid:
        r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok}), timeout=40))['data']
        return r.get('usageTotalUsd') or 0, r.get('status')
    return body.get('cost_usd') or 0, (body.get('run') or {}).get('status')


def load(runs):
    posts, cost, notes = {}, 0.0, []
    for name in runs:
        f = RAW / (name + '.json')
        if not f.exists():
            notes.append(name + ' did not run'); continue
        body = json.load(open(f, encoding='utf-8'))
        c, status = charge(body); cost += c
        if status != 'SUCCEEDED': notes.append('%s %s' % (name, status))
        inp = body.get('input') or {}
        run_kw = inp.get('query') or inp.get('keyword') or inp.get('searchTerm') or (inp.get('categories') or [None])[0]
        for x in body.get('items') or []:
            if not isinstance(x, dict) or x.get('error') or x.get('errorMessage'):
                continue
            p = post(x, run_kw)
            if p and p['key'] not in posts:
                posts[p['key']] = p
    return posts, cost, notes


def main():
    out, union = [], collections.defaultdict(set)
    for label, link, kind, runs in GROUPS:
        posts, cost, notes = load(runs)
        ps = list(posts.values())
        inwin = [p for p in ps if p['day'] and SINCE <= p['day'] <= UNTIL]
        useful = [p for p in inwin if p['about']]
        for p in useful:
            union[p['key']].add(label)
        per_kw = {k: (sum(1 for p in ps if p['kw'] == k), sum(1 for p in useful if p['kw'] == k)) for k in K}
        has = {f: sum(1 for p in ps if p[f] is not None) for f in ('day', 'reactions', 'comments', 'shares', 'views', 'followers')}
        vids = [p for p in ps if p['video']]
        has['views_on_videos'] = sum(1 for p in vids if p['views'] is not None)
        notes.append('%d by V7’s own pages' % sum(1 for p in ps if p['own']))
        out.append((label, link, kind, len(ps), len(inwin), sum(1 for p in ps if p['about']), len(useful), cost, per_kw, has, len(vids), notes, ps, useful))
    print('%-38s %-8s %5s %6s %6s %6s %8s  %s' % ('scraper', 'kind', 'posts', 'inWin', 'aboutV7', 'useful', 'cost', 'per keyword (useful / returned)'))
    for label, link, kind, n, w, a, u, cost, per_kw, has, nv, notes, ps, useful in out:
        print('%-38s %-8s %5d %6d %6d %6d  $%.3f  %s %s' % (label[:38], kind, n, w, a, u, cost, '  '.join('%s %d/%d' % (k, v[1], v[0]) for k, v in per_kw.items()),
                                                          ('| ' + '; '.join(notes)) if notes else ''))
        print('%47s fields: date %d, reactions %d, comments %d, shares %d, views %d (videos %d, with views %d), followers %d of %d%s' % (
            '', has['day'], has['reactions'], has['comments'], has['shares'], has['views'], nv, has['views_on_videos'], has['followers'], n,
            ' | per useful post $%.4f' % (cost / u) if u else ''))
    print('\nUseful posts found by all the post searches together: %d' % len(union))
    solo = collections.Counter(next(iter(v)) for v in union.values() if len(v) == 1)
    for label, link, kind, n, w, a, u, cost, per_kw, has, nv, notes, ps, useful in out:
        print('  %-38s %3d useful, %3d found by no other scraper' % (label[:38], u, solo.get(label, 0)))
    return out, union


if __name__ == '__main__':
    main()
