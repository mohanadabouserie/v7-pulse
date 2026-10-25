"""V7 Pulse refresh pipeline (19 Oct 2026, DECISIONS #152-#158; PIPELINE.md): the whole real-data chain in one command, made robust.

  python3 pipeline.py plan   [--mode M] [--since D] [--until D] [--jobs a,b] [--keywords "x|y"]   what would run and its worst cost; spends nothing
  python3 pipeline.py run    [--mode M] [--since D] [--until D] [--max-usd N] [--jobs a,b] [--keywords "x|y"] [--no-chain] [--no-alert]
  python3 pipeline.py status                                                                     the last runs and any job that needed a standby

Modes: sweep (every route over the whole window, as on 19 Oct), daily (the core routes over the last 2 days), weekly (the second-tier
routes over the last 8 days), fill (no searches: only the gaps of what's collected). daily and weekly need the dashboard's window to
roll forward first (PIPELINE.md, "Before a schedule"); until then use sweep or fill.

What makes it robust:
- Every Apify run is checked: it must end SUCCEEDED and its rows must carry the fields its reader needs (VALID). A run that fails or
  comes back in a changed format is run again on a standby scraper with the same output format, so normalize.py reads it unchanged.
  A job whose every run comes back empty, when it found posts before, is tried once on a standby too.
- Reads from Apify's API are retried on 5xx errors (collect.api); a run that can't start goes to the standby.
- Budget guard: a run starts only if its cap (its worst cost) fits under this pipeline run's limit (--max-usd, default 10) and the
  account's usage limit minus what's spent. A run that doesn't fit is skipped and reported.
- One pipeline at a time (pipeline.lock), a ledger of every Apify run (pipeline_ledger.json), a report per run (pipeline_runs/).
- A Telegram message to the bot's admin after each run: what was found, what failed, which standby took over, the cost.
  The token stays in .env.telegram and is never printed or written.
- After the searches, the chain: normalize, label (Claude), fill the gaps (collect.py fbfill/fbfill2/fbviews/fbnames/igspeech/
  igprofiles/igcomments/igcomments2/igvisfetch), the pictures (vis_media.py, vis_read.py), label again, build_real.py --inject,
  fetch_media.py, build_media.py --inject, then the quick tests. Publishing stays manual: build_sites.py dashboard, then a push,
  which needs the user's OK each time.
"""
import argparse, datetime, json, os, pathlib, re, subprocess, sys, time, traceback, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def env_from(fname, keys):
    p = ROOT / fname
    if p.exists():
        for line in open(p, encoding='utf-8'):
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.strip().split('=', 1)
                if k in keys and not os.environ.get(k):
                    os.environ[k] = v


env_from('.env.apify', ('APIFY_API_TOKEN',))
import collect as C   # noqa: E402  (reads APIFY_API_TOKEN, V7_RAW, APIFY_API_BASE, V7_SINCE/V7_UNTIL)

STATE = pathlib.Path(os.environ['V7_PIPELINE_STATE']) if os.environ.get('V7_PIPELINE_STATE') else HERE
LEDGER, LOCK, REPORTS = STATE / 'pipeline_ledger.json', STATE / 'pipeline.lock', STATE / 'pipeline_runs'
SUBSCRIBERS = pathlib.Path(os.environ['V7_BOT_STATE']) / 'subscribers.json' if os.environ.get('V7_BOT_STATE') else ROOT / 'bot' / 'state' / 'subscribers.json'
TG_API = os.environ.get('V7_TG_API', 'https://api.telegram.org')
WINDOW = ('2026-04-20', '2026-10-16')     # the dashboard's window today (END in V7_Pulse_Dashboard.html)

# ------------------------------------------------------------------ scrapers: Apify id, output format, USD a row, USD a run start, lowest cap
A = {
    'silentflow': ('silentflow~facebook-search-scraper', 'fbp_sf', 0.0022, 0.0001, 0),
    'scrapeforge': ('scrapeforge~facebook-search-posts', 'fbp_sf', 0.0026, 0.0001, 0),
    'topapi': ('topapi~facebook-search-posts-scraper', 'fbp_sf', 0.0034, 0, 0),
    'scraper_one': (C.FB_SEARCH, 'fbp_one', 0.003, 0.0001, 0),
    'fetch_cat': ('fetch_cat~facebook-post-search-scraper', 'fbp_one', 0.006, 0, 0),
    'apify_search': (C.FB_APIFY_SEARCH, 'fbp_ap', 0.005, 0.001, 0),
    'fb_shorts': ('simple.actor~google-short-videos', 'fbl', 0.0008, 0.006, 0),
    'alien_reels': ('alien_force~facebook-search-scraper', 'fbl', 0.0108, 0.002, 0),
    'apify_reels': (C.FB_APIFY_SEARCH, 'fbl', 0.005, 0.001, 0),
    'headply_video': (C.FB_V_HEADPLY, 'fbp_hp', 0.0042, 0.001, 0),
    'apify_video': (C.FB_V_APIFY, 'fbl', 0.005, 0, 0),
    'groups': (C.FB_GROUPS, 'fbp_lofo', 0.004, 0.03, 0),
    'fb_google': (C.GOOGLE, 'fbl', 0.0096, 0, 0.50),
    'danek_link': (C.FB_POST_LINK, 'fbp_sf', 0.00233, 0.0001, 0),
    'apify_fb_link': (C.FB_POSTS, 'fbp_ap', 0.005, 0.001, 0),
    'ig_tagged': (C.IG_TAGGED, 'igp_post', 0.0023, 0, 0),
    'apidojo': (C.IG_KW, 'igp_apidojo', 0.0005, 0.015, 0),
    'seemuapps': (C.IG_KW_SEEMUAPPS, 'igp_seemu', 0.0025, 0, 0),
    'dami': (C.IG_REELS, 'igp_dami', 0.0004, 0, 0),
    'ig_hashtags': (C.IG_TAGS, 'igp_post', 0.0023, 0, 0),
    'ig_shorts': ('simple.actor~google-short-videos', 'igl', 0.0008, 0.006, 0),
    'ig_google': (C.GOOGLE, 'igl', 0.0096, 0, 0.50),
    'ig_post_link': (C.IG_POSTS, 'igp_post', 0.0023, 0, 0),
}
VALID = {   # does a row carry what its reader needs? (a scraper that changed its output fails this)
    'fbp_sf': lambda x: bool(x.get('timestamp')) and bool(x.get('url') or x.get('post_id') or x.get('video_id')),
    'fbp_one': lambda x: bool(x.get('postId')) and bool(x.get('timestamp')),
    'fbp_ap': lambda x: bool(x.get('postId')) and bool(x.get('timestamp') or x.get('time')),
    'fbp_hp': lambda x: bool(x.get('postId')) and bool(x.get('createdAt')),
    'fbp_lofo': lambda x: bool(x.get('post_url')) and bool(x.get('date')),
    'fbl': lambda x: 'organicResults' in x or bool(FB_LINK.search(json.dumps(x, ensure_ascii=False))),
    'igp_post': lambda x: bool(x.get('shortCode')) and bool(x.get('timestamp')),
    'igp_apidojo': lambda x: bool(x.get('code')),
    'igp_seemu': lambda x: bool(x.get('shortcode')),
    'igp_dami': lambda x: bool(x.get('shortcode') or x.get('code')),
    'igl': lambda x: 'organicResults' in x or bool(IG_LINK.search(json.dumps(x, ensure_ascii=False))),
}
FB_LINK = re.compile(r'facebook\.com/(?:reel/|watch/?\?v=|[^"\s?]+/videos/(?:[^/"\s?]+/)?|[^"\s?]+/posts/(?:[^/"\s?]+/)?|permalink\.php\?story_fbid=|groups/\d+/posts/)([\w]{8,})')
IG_LINK = re.compile(r'instagram\.com/(?:[\w.]+/)?(?:p|reel|reels|tv)/([\w-]{8,})')
OWN_PAGES = re.compile(r'facebook\.com/(?:V7Egypt|Vsupersoda)/|instagram\.com/(?:v7egypt|vsupersoda)/', re.I)

# the 20 Facebook keywords that found 94% of the posts the keyword searches found on 19 Oct (daily); all 30 in a sweep
FB_DAILY_KW = ['V7 soda', 'ڤي كولا', 'V Super Soda', 'V7 cream soda', 'V7 كريم صودا', 'V7 مشروب', 'مشروب V7', 'V7 بينا كولادا', 'V7 رمان', 'V7 كانز',
               'V7 pink lemonade', 'ڤي سڤن', 'V7 drink', 'V7 شعير', 'V Cola', 'ڤي سڤن رمان', 'ڤي كولا دايت', 'ڤي سڤن كريم صودا', 'V7 بينك ليمونيد', 'ڤي سڤن ليمون نعناع']
IG_SHORTS_K = ['V7 cream soda', 'V7 كريم صودا', 'ڤي سڤن', 'ڤي كولا', 'V7 soda', 'V Cola']
IG_HASHTAGS = ['ڤي_سڤن', 'vsupersoda', 'vorange', 'v7drink', 'v7creamsoda', 'ڤي_كولا', 'vcolaegypt', 'ڤي_اورانج', 'v7egypt']


class Job:
    def __init__(self, name, modes, actors, keywords=None, n=None, note=''):
        self.name, self.modes, self.actors, self.keywords, self.n, self.note = name, modes, actors, keywords, n or {}, note


SWEEP, DAILY, WEEKLY = 'sweep', 'daily', 'weekly'
JOBS = [   # actors: the main one first, then standbys with the same output format
    Job('fb_posts_one', {SWEEP, DAILY}, ['scraper_one', 'fetch_cat'], 'fb', {SWEEP: 20, DAILY: 10}, 'Facebook search, its own ranking (most posts no other route finds)'),
    Job('fb_posts_sf', {SWEEP, DAILY}, ['silentflow', 'scrapeforge', 'topapi'], 'fb', {SWEEP: 20, DAILY: 10}, 'Facebook search, the common backend'),
    Job('fb_posts_ap', {SWEEP, WEEKLY}, ['apify_search'], 'fb', {SWEEP: 10, WEEKLY: 10}, "Apify's own search (no date filter)"),
    Job('fb_posts_forge', {SWEEP, WEEKLY}, ['scrapeforge', 'topapi'], 'fb', {SWEEP: 20, WEEKLY: 10}, 'a fourth search for coverage'),
    Job('fb_posts_cat', {SWEEP, WEEKLY}, ['fetch_cat', 'scraper_one'], 'fb', {SWEEP: 20, WEEKLY: 10}, 'a fifth search for coverage'),
    Job('fb_reels_google', {SWEEP, DAILY}, ['fb_shorts'], 'fb_all', {SWEEP: 24, DAILY: 12}, "Google's short videos, Facebook only"),
    Job('fb_reels_alien', {SWEEP, WEEKLY}, ['alien_reels', 'apify_reels'], 'fb_reels', {SWEEP: 20, WEEKLY: 10}, 'reels-only search'),
    Job('fb_videos', {SWEEP, WEEKLY}, ['headply_video', 'apify_video'], 'fb_video', {SWEEP: 20, WEEKLY: 10}, 'Facebook video search'),
    Job('fb_groups', {SWEEP, WEEKLY}, ['groups'], 'fb_groups', {SWEEP: 25, WEEKLY: 10}, 'public groups'),
    Job('fb_google_web', {SWEEP, DAILY}, ['fb_google'], 'fb_phrases', {SWEEP: 2, DAILY: 1}, "Google's site search of facebook.com (pages per query)"),
    Job('ig_tagged', {SWEEP, DAILY}, ['ig_tagged'], 'ig_accounts', {SWEEP: 520, DAILY: 40}, 'posts that tag @v7egypt and @vsupersoda'),
    Job('ig_kw', {SWEEP, DAILY}, ['apidojo', 'seemuapps'], 'ig', {SWEEP: 10, DAILY: 10}, "Instagram's keyword search"),
    Job('ig_reels', {SWEEP, WEEKLY}, ['dami'], 'ig', {SWEEP: 30, WEEKLY: 15}, "Instagram's Reels search"),
    Job('ig_reels_google', {SWEEP, WEEKLY}, ['ig_shorts'], 'ig_shorts', {SWEEP: 24, WEEKLY: 12}, "Google's short videos, Instagram only"),
    Job('ig_google_web', {SWEEP, WEEKLY}, ['ig_google'], 'ig_phrases', {SWEEP: 3, WEEKLY: 1}, "Google's site search of instagram.com (pages per query)"),
    Job('ig_hashtags', {SWEEP, WEEKLY}, ['ig_hashtags'], 'ig_tags', {SWEEP: 30, WEEKLY: 15}, 'hashtags'),
]
FILL = ['fbshareorigins', 'fbfill', 'fbfill2', 'fbviews', 'fbnames', 'igspeech', 'igprofiles', 'igcomments', 'igcomments2', 'igvisfetch']   # collect.py stages
QUICK_TESTS = ['test_v25', 'test_v29', 'test_v30', 'test_v31']


def keywords(src, opts):
    if opts.keywords:
        return [k for k in opts.keywords.split('|') if k]
    full = opts.mode == SWEEP
    return {'fb': C.KW_FB if full else FB_DAILY_KW, 'fb_all': C.KW_FB, 'fb_reels': C.KW_FB_REELS, 'fb_video': C.KW_FB_VIDEO, 'fb_groups': C.KW_FB_GROUPS,
            'fb_phrases': C.G_PHRASES_FB, 'ig': C.KW_IG_EN, 'ig_shorts': IG_SHORTS_K, 'ig_phrases': C.G_PHRASES, 'ig_accounts': ['v7egypt', 'vsupersoda'],
            'ig_tags': IG_HASHTAGS}[src]


def months(since, until):
    """Google's date ranges: one a calendar month, clipped to the window."""
    a, b = datetime.date.fromisoformat(since), datetime.date.fromisoformat(until)
    out, d = [], a
    while d <= b:
        end = (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        out.append((d, min(end, b)))
        d = end + datetime.timedelta(days=1)
    return out


def inputs(actor, kw, n, since, until, mode):
    """The input one actor takes for one keyword (or phrase, account, hashtag)."""
    g = lambda q, site: [('https://www.google.com/search?' + urllib.parse.urlencode({'q': q + ' site:' + site, 'tbs': 'cdr:1,cd_min:%s,cd_max:%s' % (
        a.strftime('%-m/%-d/%Y'), b.strftime('%-m/%-d/%Y'))})) for a, b in months(since, until)]
    rng = 'year' if mode == SWEEP else 'week' if mode == WEEKLY else 'day'
    order = 'top' if mode == SWEEP else 'latest'   # a short window sorted by latest lists those days' posts (20 Oct date-slice test, DATESLICE_TEST.md)
    return {
        'silentflow': {"query": kw, "search_type": "posts", "max_posts": n, "start_date": since, "end_date": until},
        'scrapeforge': {"query": kw, "search_type": "posts", "max_results": n, "start_date": since, "end_date": until},
        'topapi': {"searchQueries": [kw], "sortBy": "top", "startDate": since, "endDate": until, "maxPostsPerQuery": n},
        'scraper_one': {"query": kw, "resultsCount": n, "searchType": order, "startDate": since, "endDate": until},
        'fetch_cat': {"query": kw, "resultsCount": n, "searchType": order, "startDate": since, "endDate": until},
        'apify_search': {"categories": [kw], "searchType": "posts", "resultsLimit": n},
        'fb_shorts': {"queries": ['"%s"' % kw], "maxItems": n, "platform": "facebook", "timeRange": rng, "country": "EG", "language": "ar"},
        'alien_reels': {"search_type": "posts", "keyword": kw, "only_reels": True, "follow_post_scraping": True, "results_limit": max(10, n), "start_date": since, "end_date": until},
        'apify_reels': {"categories": [kw], "searchType": "reels", "resultsLimit": n},
        'headply_video': {"searchQueries": [kw], "maxItemsPerTarget": n, "mode": "videoSearch"},
        'apify_video': {"searchTerm": kw, "resultsLimit": n},
        'groups': {"keywords": [kw], "afterDate": "this_year" if mode == SWEEP else "last_week", "maxPosts": n, "countryCode": "eg"},
        'fb_google': {"queries": '\n'.join(g(kw, 'facebook.com')), "maxPagesPerQuery": n, "countryCode": "eg"},
        'ig_tagged': {"username": [kw], "resultsLimit": n},
        'apidojo': {"keywords": [kw], "maxItems": n, "until": since},
        'seemuapps': {"keywords": [kw], "maxPostsPerKeyword": n, "dateFrom": since, "dateTo": until},
        'dami': {"searchQueries": [kw], "maxReelsPerTerm": n, "maxReels": n, "newerThan": since},
        'ig_hashtags': {"hashtags": [kw], "resultsLimit": n, "keywordSearch": False},
        'ig_shorts': {"queries": ['"%s"' % kw], "maxItems": n, "platform": "instagram", "timeRange": rng, "country": "EG", "language": "ar"},
        'ig_google': {"queries": '\n'.join(g(kw, 'instagram.com')), "maxPagesPerQuery": n, "countryCode": "eg"},
    }[actor]


def max_rows(actor, kw, n, since, until):
    if actor in ('fb_google', 'ig_google'):
        return len(months(since, until)) * n
    return n


def cap_for(actor, rows):
    aid, fam, per, start, low = A[actor]
    extra = per * rows + start + (0.006 * max(1, -(-rows // 12)) if actor in ('fb_shorts', 'ig_shorts') else 0)   # Google's short videos: a search a page of 12
    return round(max(low, extra * 1.3 + 0.02), 2)


# ------------------------------------------------------------------ ledger, lock, budget, alerts
def ledger_add(rec):
    data = json.load(open(LEDGER, encoding='utf-8')) if LEDGER.exists() else []
    data.append(rec)
    tmp = LEDGER.with_suffix('.tmp'); json.dump(data, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); os.replace(tmp, LEDGER)


def found_before(job):
    """Did this job return rows in an earlier pipeline run? (an all-empty job that used to find posts is suspicious)"""
    if not LEDGER.exists():
        return False
    return any(r.get('job') == job and (r.get('rows') or 0) > 0 for r in json.load(open(LEDGER, encoding='utf-8')))


def take_lock():
    if LOCK.exists():
        try:
            pid = int(LOCK.read_text().strip())
            os.kill(pid, 0)
            return False                        # another pipeline is running
        except PermissionError:
            return False                        # it runs as another user: still running
        except (ValueError, ProcessLookupError):
            pass                                # a stale lock from a run that died
    LOCK.write_text(str(os.getpid()))
    return True


def account():
    d = C.api('GET', '/users/me/limits')['data']
    return d['current']['monthlyUsageUsd'], (d.get('limits') or {}).get('maxMonthlyUsageUsd') or 0


def admins():
    try:
        subs = json.load(open(SUBSCRIBERS, encoding='utf-8'))
    except Exception:
        return []
    return [cid for cid, s in subs.items() if isinstance(s, dict) and s.get('role') == 'admin']


def alert(text, report):
    """Telegram to the bot's admin(s). The token is read from .env.telegram and never written anywhere."""
    env_from('.env.telegram', ('TELEGRAM_BOT_TOKEN',))
    tok, chats = os.environ.get('TELEGRAM_BOT_TOKEN', ''), admins()
    if not tok or not chats:
        report['alert'] = 'not sent: no bot token or no admin'; return
    sent = 0
    for chat in chats:
        try:
            req = urllib.request.Request('%s/bot%s/sendMessage' % (TG_API, tok), data=json.dumps({'chat_id': chat, 'text': text[:4000]}).encode(),
                                         headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=30).read(); sent += 1
        except Exception as e:
            report.setdefault('alert_errors', []).append(str(e).replace(tok, '<token>')[:200])
    report['alert'] = 'sent to %d admin chat%s' % (sent, '' if sent == 1 else 's')


# ------------------------------------------------------------------ one job: runs, health, standby
def health(actor, name):
    f = C.RAW / (name + '.json')
    if not f.exists():
        return {'status': 'NOT STARTED', 'rows': 0, 'valid': 0, 'ok': False}
    body = json.load(open(f, encoding='utf-8'))
    status = (body.get('run') or {}).get('status')
    items = [x for x in body.get('items') or [] if isinstance(x, dict)]
    fam = A[actor][1]
    good = sum(1 for x in items if not x.get('error') and VALID[fam](x))
    ok = status == 'SUCCEEDED' and (not items or good >= 0.5 * len(items))
    return {'status': status, 'rows': len(items), 'valid': good, 'ok': ok, 'cost': body.get('cost_usd')}


def run_one(job, actor, kw, i, tag, opts, budget, rep, standby_for=None):
    aid, fam, per, start, low = A[actor]
    n = job.n.get(opts.mode, 10)
    rows = max_rows(actor, kw, n, opts.since, opts.until)
    name = '%s_%s_%s_%02d%s' % (fam, job.name, tag, i, '_sb' if standby_for else '')
    cap = cap_for(actor, rows)
    if budget - C.spent() < cap:               # the budget guard: this run's worst cost doesn't fit
        h = {'status': 'SKIPPED (budget)', 'rows': 0, 'valid': 0, 'ok': False}
    else:
        try:
            C.run(name, aid, inputs(actor, kw, n, opts.since, opts.until, opts.mode), cap, rows, budget=budget)
        except Exception as e:                 # an Apify error that outlasted the retries
            rep['errors'].append('%s %s: %s' % (job.name, actor, str(e)[:160]))
        h = health(actor, name)
    rec = dict(time=datetime.datetime.now().isoformat(timespec='seconds'), job=job.name, actor=actor, name=name, keyword=kw, standby_for=standby_for, **h)
    ledger_add(rec)
    return name, h


def run_job(job, opts, tag, budget, rep):
    kws = keywords(job.keywords, opts)
    out, empty = [], True
    for i, kw in enumerate(kws):
        used, h = None, None
        for k, actor in enumerate(job.actors):
            name, h = run_one(job, actor, kw, i, tag, opts, budget, rep, standby_for=job.actors[0] if k else None)
            if h['ok']:
                used = actor; break
            if h['status'].startswith('SKIPPED'):   # out of budget: a standby wouldn't fit either
                rep['problems'].append('%s, "%s": skipped, over the budget line' % (job.name, kw)); break
            rep['problems'].append('%s, "%s": %s on %s (%d rows, %d usable)%s' % (job.name, kw, h['status'], actor, h['rows'], h['valid'],
                                                                                    ', trying a standby' if k + 1 < len(job.actors) else ''))
        if used and used != job.actors[0]:
            rep['standbys'].append('%s, "%s": %s in place of %s' % (job.name, kw, used, job.actors[0]))
        if h and h['rows']:
            empty = False
        out.append(used)
    if empty and kws and found_before(job.name) and len(job.actors) > 1:   # all empty, though it found posts before: the scraper may be broken
        rep['problems'].append('%s: every keyword came back empty; the standby tries the first keyword' % job.name)
        name, h = run_one(job, job.actors[1], kws[0], 99, tag, opts, budget, rep, standby_for=job.actors[0])
        if h['ok'] and h['rows']:
            rep['standbys'].append('%s: %s found rows where %s found none' % (job.name, job.actors[1], job.actors[0]))
    return out


# ------------------------------------------------------------------ links found by Google and the reel searches, fetched by link
def links_from(tag, prefix):
    pat = FB_LINK if prefix == 'fbl' else IG_LINK
    found = {}
    for f in sorted(C.RAW.glob('%s_*_%s_*.json' % (prefix, tag))):
        for x in json.load(open(f, encoding='utf-8')).get('items') or []:
            s = json.dumps(x, ensure_ascii=False)
            urls = [r.get('url') or '' for r in x.get('organicResults') or []] if isinstance(x, dict) and 'organicResults' in x else [s]
            for u in urls:
                if OWN_PAGES.search(u):
                    continue
                for m in pat.finditer(u):
                    found[m.group(1)] = m.group(0)
    return found


def fetch_links(opts, tag, budget, rep):
    fb = links_from(tag, 'fbl')
    known_fb = C.fb_known()
    new_fb = {k: 'https://www.' + v for k, v in fb.items() if k not in known_fb}
    ig = links_from(tag, 'igl')
    known_ig = C.known_keys()
    new_ig = {k: 'https://www.instagram.com/p/%s/' % k for k in ig if ('ig:' + k) not in known_ig and opts.since <= (C.id_day('ig', k) or '') <= opts.until}
    rep['links'] = {'facebook found': len(fb), 'facebook new': len(new_fb), 'instagram found': len(ig), 'instagram new': len(new_ig)}
    jobs = []
    if new_fb:
        jobs.append((Job('fb_links', set(), ['danek_link', 'apify_fb_link']), 'fbp_sf', [{"direct_urls": [{"url": u} for u in new_fb.values()]},
                                                                                      {"startUrls": [{"url": u} for u in new_fb.values()]}], len(new_fb)))
    if new_ig:
        jobs.append((Job('ig_links', set(), ['ig_post_link']), 'igp_post', [{"username": list(new_ig.values())}], len(new_ig)))
    for job, fam, inps, n in jobs:
        for k, actor in enumerate(job.actors):
            aid, fam2, per, start, low = A[actor]
            name = '%s_%s_%s_00%s' % (fam2, job.name, tag, '_sb' if k else '')
            try:
                C.run(name, aid, inps[k], round(max(low, n * per * 1.3 + start + 0.05), 2), n, budget=budget)
            except Exception as e:
                rep['errors'].append('%s %s: %s' % (job.name, actor, str(e)[:160]))
            h = health(actor, name)
            ledger_add(dict(time=datetime.datetime.now().isoformat(timespec='seconds'), job=job.name, actor=actor, name=name, keyword=None,
                            standby_for=job.actors[0] if k else None, **h))
            if h['ok']:
                if k:
                    rep['standbys'].append('%s: %s in place of %s' % (job.name, actor, job.actors[0]))
                break
            rep['problems'].append('%s: %s on %s (%d rows, %d usable)' % (job.name, h['status'], actor, h['rows'], h['valid']))


# ------------------------------------------------------------------ the chain after the searches
def step(rep, label, cmd, timeout=7200):
    t = time.time()
    env = dict(os.environ, V7_SINCE=rep['since'], V7_UNTIL=rep['until'])
    r = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True, timeout=timeout, env=env)
    tail = (r.stdout or '').strip().splitlines()[-1:] + (r.stderr or '').strip().splitlines()[-1:]
    rep['steps'].append({'step': label, 'ok': r.returncode == 0, 'seconds': round(time.time() - t), 'last': ' | '.join(tail)[:300]})
    if r.returncode != 0:
        rep['problems'].append('%s failed: %s' % (label, ' | '.join(tail)[:200]))
    return r.returncode == 0


def report_rejects(rep):
    """24 Oct (DECISIONS #178): comments a scraper returned for a post that can't be that post's (comment_check.py; normalize.py lists them
    in comment_rejects.json and leaves them out). Only this run's are reported; stage_fbfill2 asks Apify's own scraper for those posts."""
    p = HERE / 'comment_rejects.json'
    rej = json.load(open(p, encoding='utf-8')).get('rejects', []) if p.exists() else []
    new = [r for r in rej if (C.RAW / (r['run'] + '.json')).exists() and (C.RAW / (r['run'] + '.json')).stat().st_mtime >= rep['started_ts']]
    if new:
        rep['problems'].append('comments rejected as not their post\'s on %d post%s (%s): %s' % (
            len(new), '' if len(new) == 1 else 's', ', '.join(sorted({r['scraper'] for r in new})), '; '.join('%s %s' % (r['post'], r['why']) for r in new[:5])))


def chain(opts, rep):
    py, venv = sys.executable, str(ROOT / 'data' / '.venv' / 'bin' / 'python')
    for b in ('BUDGET', 'BUDGET_IG', 'BUDGET_FB', 'BUDGET_SPEECH', 'BUDGET_IGKW', 'BUDGET_FBREEL', 'BUDGET_FBMORE'):   # the fill stages obey this run's line
        if hasattr(C, b):
            setattr(C, b, rep['budget_line'])
    ok = step(rep, 'normalize', [py, 'normalize.py']) and step(rep, 'label', [py, 'label.py'])
    if not ok:
        return
    n_skips = len(C.SKIPS)                    # collect.run notes the runs it skips (over the line, or refused by Apify)
    for st in FILL:
        try:
            getattr(C, 'stage_' + st)()
            rep['steps'].append({'step': 'fill ' + st, 'ok': True})
        except Exception as e:
            rep['steps'].append({'step': 'fill ' + st, 'ok': False, 'last': str(e)[:200]})
            rep['problems'].append('fill %s failed: %s' % (st, str(e)[:160]))
    skipped = C.SKIPS[n_skips:]
    if skipped:
        rep['problems'].append('fill steps, %d run%s not started: %s%s' % (len(skipped), '' if len(skipped) == 1 else 's', ', '.join(skipped[:10]),
                                                                       ' and %d more' % (len(skipped) - 10) if len(skipped) > 10 else ''))
    vis = sorted(C.RAW.glob('vis_posts_*.json'), key=lambda p: p.stat().st_mtime)
    new_vis = [str(p) for p in vis if p.stat().st_mtime >= rep['started_ts']]
    if new_vis:
        step(rep, 'pictures, Instagram', [venv, 'vis_media.py'] + new_vis)
    step(rep, 'pictures, Facebook', [venv, 'vis_media.py', '--fb'])
    step(rep, 'read pictures', [py, 'vis_read.py'])
    ok = step(rep, 'normalize again', [py, 'normalize.py']) and step(rep, 'label again', [py, 'label.py'])
    report_rejects(rep)
    if ok and not opts.no_build:
        if step(rep, 'build', [py, 'build_real.py', '--inject']):
            step(rep, 'images', [py, 'fetch_media.py'])
            step(rep, 'embed images', [py, str(HERE.parent / 'media_13oct' / 'build_media.py'), '--inject'])
            for t in QUICK_TESTS:
                step(rep, 'test ' + t, [py, str(ROOT / 'tests' / (t + '.py'))], timeout=900)


# ------------------------------------------------------------------ plan, run, status
def window(opts):
    if opts.until is None:
        opts.until = WINDOW[1] if opts.mode in (SWEEP, 'fill') else (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    if opts.since is None:
        days = {DAILY: 2, WEEKLY: 8}.get(opts.mode)
        opts.since = WINDOW[0] if days is None else (datetime.date.fromisoformat(opts.until) - datetime.timedelta(days=days - 1)).isoformat()
    C.SINCE, C.UNTIL = opts.since, opts.until


def selected(opts):
    names = set(opts.jobs.split(',')) if opts.jobs else None
    return [j for j in JOBS if opts.mode in j.modes and (names is None or j.name in names)]


def plan(opts):
    window(opts)
    rows_total, cost_total, lines = 0, 0.0, []
    for j in selected(opts):
        kws = keywords(j.keywords, opts)
        a = j.actors[0]
        rows = sum(max_rows(a, k, j.n.get(opts.mode, 10), opts.since, opts.until) for k in kws)
        aid, fam, per, start, low = A[a]
        cost = rows * per + len(kws) * start + (0.006 * rows / 12 if a in ('fb_shorts', 'ig_shorts') else 0)
        rows_total += rows; cost_total += cost
        lines.append('  %-16s %-14s %3d inputs  up to %5d rows  about USD %5.2f   standby: %s' % (j.name, a, len(kws), rows, cost, ', '.join(j.actors[1:]) or '-'))
    print('%s, %s to %s' % (opts.mode, opts.since, opts.until))
    print('\n'.join(lines) or '  (no searches: fill only)')
    print('searches: up to %d rows, about USD %.2f at most (Facebook pads results, so most runs return their full count)' % (rows_total, cost_total))
    print('then: fetch new links by link, normalize, label, fill (%s), pictures, build, tests' % ', '.join(FILL))
    return cost_total


def run(opts):
    window(opts)
    if opts.until > WINDOW[1] and not opts.beyond_window:
        print('%s is past the dashboard\'s window (it ends %s): posts after it would be collected but not shown. Roll the window forward '
              'first (PIPELINE.md), or pass --beyond-window.' % (opts.until, WINDOW[1]))
        return 3
    tag = time.strftime('%Y%m%d%H%M')
    rep = {'mode': opts.mode, 'since': opts.since, 'until': opts.until, 'tag': tag, 'started': datetime.datetime.now().isoformat(timespec='seconds'),
           'started_ts': time.time(), 'jobs': {}, 'problems': [], 'standbys': [], 'errors': [], 'steps': []}
    if not take_lock():
        print('another pipeline run is going (pipeline.lock); stopped'); return 2
    REPORTS.mkdir(parents=True, exist_ok=True)
    try:
        spent0, limit = account()
        cap = min(limit or 1e9, spent0 + opts.max_usd)
        rep.update(spent_before=round(spent0, 4), limit=limit, budget_line=round(cap, 4))
        C.log(f'--- pipeline {opts.mode} {opts.since}..{opts.until}, spent so far this cycle ${spent0:.4f}, stops at ${cap:.2f}')
        for j in selected(opts):
            rep['jobs'][j.name] = run_job(j, opts, tag, cap, rep)
        if opts.mode != 'fill':
            fetch_links(opts, tag, cap, rep)
        if not opts.no_chain:
            chain(opts, rep)
        spent1, _ = account()
        rep['spent'] = round(spent1 - spent0, 4)
        rep['spent_after'] = round(spent1, 4)
    except Exception as e:
        rep['errors'].append('pipeline stopped: %s' % ''.join(traceback.format_exception_only(type(e), e)).strip()[:300])
    finally:
        rep['finished'] = datetime.datetime.now().isoformat(timespec='seconds')
        skipped = sum(1 for r in (json.load(open(LEDGER, encoding='utf-8')) if LEDGER.exists() else []) if tag in (r.get('name') or '')
                      and str(r.get('status')).startswith(('NOT STARTED', 'SKIPPED')))
        rep['not_started'] = skipped
        text = summary(rep)
        if not opts.no_alert:
            alert(text, rep)
        rep.pop('started_ts', None)
        json.dump(rep, open(REPORTS / (tag + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        (REPORTS / (tag + '.md')).write_text(text + '\n', encoding='utf-8')
        print(text)
        try:
            LOCK.unlink()
        except FileNotFoundError:
            pass
    return 1 if rep['errors'] else 0


def summary(rep):
    lines = ['V7 Pulse pipeline, %s (%s to %s)' % (rep['mode'], rep['since'], rep['until'])]
    if 'spent' in rep:
        lines.append('Apify: USD %.2f this run, USD %.2f this month of USD %.0f' % (rep['spent'], rep['spent_after'], rep.get('limit') or 0))
    if rep.get('links'):
        lines.append('New links fetched: Facebook %(facebook new)d, Instagram %(instagram new)d' % rep['links'])
    if rep.get('not_started'):
        lines.append('Runs not started (budget or Apify refused): %d' % rep['not_started'])
    if rep['standbys']:
        lines.append('Standbys used: ' + '; '.join(rep['standbys'][:8]))
    if rep['problems']:
        lines.append('Problems: ' + '; '.join(rep['problems'][:8]) + (' (and %d more)' % (len(rep['problems']) - 8) if len(rep['problems']) > 8 else ''))
    if rep['errors']:
        lines.append('Errors: ' + '; '.join(rep['errors'][:5]))
    bad = [s['step'] for s in rep['steps'] if not s['ok']]
    if rep['steps']:
        lines.append('Steps: %d done, %d failed%s' % (len(rep['steps']) - len(bad), len(bad), (' (' + ', '.join(bad[:6]) + ')') if bad else ''))
    if not (rep['problems'] or rep['errors'] or bad):
        lines.append('Everything ran without a problem.')
    return '\n'.join(lines)


def status(opts):
    data = json.load(open(LEDGER, encoding='utf-8')) if LEDGER.exists() else []
    print('%d Apify runs in the ledger' % len(data))
    for r in data[-15:]:
        print('  %s %-16s %-14s %-11s rows %4s usable %4s%s' % (r['time'], r['job'], r['actor'], r['status'], r['rows'], r['valid'],
                                                               '  (standby for %s)' % r['standby_for'] if r.get('standby_for') else ''))
    reps = sorted(REPORTS.glob('*.md')) if REPORTS.exists() else []
    if reps:
        print('\nlast report (%s):\n%s' % (reps[-1].name, reps[-1].read_text(encoding='utf-8')))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('cmd', choices=['plan', 'run', 'status'])
    ap.add_argument('--mode', default=SWEEP, choices=[SWEEP, DAILY, WEEKLY, 'fill'])
    ap.add_argument('--since'); ap.add_argument('--until')
    ap.add_argument('--max-usd', type=float, default=10.0, help='the most this run may spend (default 10)')
    ap.add_argument('--jobs', help='only these jobs, comma-separated')
    ap.add_argument('--keywords', help='only these keywords, separated by |')
    ap.add_argument('--no-chain', action='store_true', help='searches only: no normalize, label, fill, build or tests')
    ap.add_argument('--no-build', action='store_true', help="don't write the dashboard")
    ap.add_argument('--no-alert', action='store_true', help='no Telegram message')
    ap.add_argument('--beyond-window', action='store_true', help="allow dates past the dashboard's window")
    o = ap.parse_args()
    if o.cmd == 'plan':
        plan(o)
    elif o.cmd == 'status':
        status(o)
    else:
        sys.exit(run(o))
