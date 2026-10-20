"""20 Oct 2026, the user's idea: "maybe having date filter can solve this problem with getting different posts everytime we search,
I mean if we go day by day". A test on August 2026, the busiest month for public posts about V7:

- Google's site search of instagram.com and facebook.com one day at a time and one week at a time, for the phrases whose month searches
  were cut off most often on 19 Oct (47 of 84 Instagram and 32 of 84 Facebook month searches still had a next page). The month searches
  of 19 Oct (ig_google_months, fbc_google_months) are the baseline.
- Facebook's own search limited to one day (scraper_one, latest; silentflow, top) on the three busiest days we know, three keywords.
- The new finds fetched by link (Instagram: Apify's post scraper; Facebook: danek), then normalize.py and label.py, then the report.

Usage: python3 dateslice_test.py check|run|fetch|report
check, run and fetch need APIFY_API_TOKEN in the environment; report reads the saved runs (and the final charges, with the token)."""
import collections, datetime, json, os, pathlib, re, sys, urllib.parse, urllib.request

import collect as C

HERE = pathlib.Path(__file__).resolve().parent
RAW = C.RAW
BUDGET = 74.50   # 20 Oct: the test may spend up to here on Apify's meter (USD 71.83 before it; expected about USD 2)
IG_TERMS = ['"@v7egypt"', '"V7 cream soda"', '"V Cola"', '"مشروب V7"', '"ڤي سڤن"']   # most new posts about V7 per find on 19 Oct
FB_TERMS = ['"مشروب V7"', '"V Super Soda"', '"ڤى كولا"', '"V Cola" مصر', '"V7 cream soda"', '"ڤي كولا"']   # cut off most often on 19 Oct
DAYS = [datetime.date(2026, 8, d) for d in range(1, 32)]
WEEKS = [(datetime.date(2026, 8, a), datetime.date(2026, 8, b)) for a, b in ((1, 7), (8, 14), (15, 21), (22, 28), (29, 31))]
FB_DAYS = ['2026-10-15', '2026-08-15', '2026-08-04']   # the busiest days for Facebook public posts about V7 (14, 12 and 9 collected)
FB_KW = ['ڤي كولا', 'V7 كريم صودا', 'ڤي سڤن']
PAGE = 0.0025    # Google: USD a results page (19 Oct runs)
FB_LINK = re.compile(r'facebook\.com/(?:reel/|watch/?\?v=|[^"\s?]+/videos/(?:[^/"\s?]+/)?|[^"\s?]+/posts/(?:[^/"\s?]+/)?|permalink\.php\?story_fbid=|groups/\d+/posts/)([\w]{8,})')
IG_LINK = re.compile(r'instagram\.com/(?:[\w.]+/)?(?:p|reel|reels|tv)/([\w-]{8,})')
OWN_PAGES = re.compile(r'facebook\.com/(?:V7Egypt|Vsupersoda)/|instagram\.com/(?:v7egypt|vsupersoda)/', re.I)
GOOGLE_RUNS = {'igl_ds_day': 'Google, Instagram, a day at a time', 'igl_ds_week': 'Google, Instagram, a week at a time',
               'fbl_ds_day': 'Google, Facebook, a day at a time', 'fbl_ds_week': 'Google, Facebook, a week at a time'}


def gurl(term, site, d0, d1):
    tbs = 'cdr:1,cd_min:%d/%d/%d,cd_max:%d/%d/%d' % (d0.month, d0.day, d0.year, d1.month, d1.day, d1.year)
    return 'https://www.google.com/search?q=' + urllib.parse.quote_plus(term + ' site:' + site) + '&tbs=' + urllib.parse.quote(tbs, safe='')


def google_run(name, terms, site, slices, pages):
    urls = [gurl(t, site, a, b) for t in terms for a, b in slices]
    return (name, C.GOOGLE, {"queries": '\n'.join(urls), "maxPagesPerQuery": pages, "countryCode": "eg"},
            round(max(0.50, len(urls) * pages * PAGE + 0.05), 2), len(urls) * pages)


def fb_day_runs(n):
    out = []
    for day in FB_DAYS:
        for i, k in enumerate(FB_KW, 1):
            tag = day[5:].replace('-', '')
            out.append((f'fbp_one_ds_{tag}_{i}', C.FB_SEARCH, {"query": k, "resultsCount": n, "searchType": "latest", "startDate": day, "endDate": day},
                        round(n * 0.003 * 1.3 + 0.05, 2), n))
            out.append((f'fbp_sf_ds_{tag}_{i}', C.FB_SILENT, {"query": k, "search_type": "posts", "max_posts": n, "start_date": day, "end_date": day},
                        round(n * 0.0022 * 1.3 + 0.05, 2), n))
    return out


def check():
    """Three tiny calls first: does a one-day window come back, and on that day?"""
    one, sf = fb_day_runs(3)[:2]
    for name, actor, body, cap, n in ((one[0].replace('_ds_', '_dst_'),) + one[1:], (sf[0].replace('_ds_', '_dst_'),) + sf[1:]):
        items = C.run(name, actor, body, cap, n, budget=BUDGET)
        days = collections.Counter(str(x.get('timestamp') or x.get('time') or x.get('created_time') or '')[:10] for x in items if isinstance(x, dict))
        print(name, len(items), 'rows; raw dates:', dict(days))
    d = datetime.date(2026, 8, 15)
    g = google_run('fbl_dst_google', ['"ڤي كولا"'], 'facebook.com', [(d, d)], 1)
    items = C.run(*g, budget=BUDGET)
    for x in items:
        print('google', len(x.get('organicResults') or []), 'results; next page:', x.get('hasNextPage'))


def run():
    todo = [google_run('igl_ds_day', IG_TERMS, 'instagram.com', [(d, d) for d in DAYS], 2),
            google_run('igl_ds_week', IG_TERMS, 'instagram.com', WEEKS, 3),
            google_run('fbl_ds_day', FB_TERMS, 'facebook.com', [(d, d) for d in DAYS], 2),
            google_run('fbl_ds_week', FB_TERMS, 'facebook.com', WEEKS, 3)] + fb_day_runs(10)
    C.log(f'  dateslice: {len(todo)} runs, caps USD {sum(t[3] for t in todo):.2f} in all, line ${BUDGET:.2f}')
    C.parallel(todo, BUDGET)


def google_links(name):
    """(platform, key) -> link for every post a Google run found, V7's own pages left out."""
    out = {}
    f = RAW / (name + '.json')
    if not f.exists():
        return out
    for x in json.load(open(f, encoding='utf-8')).get('items') or []:
        for r in (x.get('organicResults') or []) if isinstance(x, dict) else []:
            u = (r.get('url') or '').split('#')[0]
            if OWN_PAGES.search(u):
                continue
            m = IG_LINK.search(u)
            if m:
                out[('ig', m.group(1))] = 'https://www.instagram.com/p/%s/' % m.group(1)
            m = FB_LINK.search(u)
            if m:
                out[('fb', m.group(1))] = u
    return out


def month_links(name, site):
    """The August month searches of 19 Oct: the baseline."""
    out = {}
    f = RAW / (name + '.json')
    terms = {t + ' site:' + ('instagram.com' if site == 'ig' else 'facebook.com') for t in (IG_TERMS if site == 'ig' else FB_TERMS)}
    for x in json.load(open(f, encoding='utf-8')).get('items') or []:
        q = (x.get('searchQuery') or {}) if isinstance(x, dict) else {}
        if q.get('term') not in terms or 'cd_min:8/1/2026' not in urllib.parse.unquote(q.get('url') or ''):   # the same phrases, August only
            continue
        for r in x.get('organicResults') or []:
            u = r.get('url') or ''
            if OWN_PAGES.search(u):
                continue
            m = (IG_LINK if site == 'ig' else FB_LINK).search(u)
            if m:
                out[(site, m.group(1))] = u
    return out


def known_fb_keys():
    keys = set(C.fb_known())
    for it in json.load(open(HERE / 'items.json', encoding='utf-8'))['items']:
        if it['pl'] == 'fb':
            for u in [it.get('url')] + (it.get('urls') or []):
                m = FB_LINK.search(u or '')
                if m: keys.add(m.group(1))
    return keys


def fetch():
    links = {}
    for name in GOOGLE_RUNS:
        links.update(google_links(name))
    known_ig, known_fb = C.known_keys(), known_fb_keys()
    new_ig = {k: u for (pl, k), u in links.items() if pl == 'ig' and 'ig:' + k not in known_ig and C.SINCE <= (C.id_day('ig', k) or '') <= C.UNTIL}
    new_fb = {k: u for (pl, k), u in links.items() if pl == 'fb' and k not in known_fb}
    C.log(f'  dateslice fetch: Instagram {len(new_ig)} new in the window, Facebook {len(new_fb)} new links')
    todo = []
    if new_ig:
        todo.append(('igp_post_ds_links', C.IG_POSTS, {"username": sorted(new_ig.values())}, round(len(new_ig) * 0.0023 * 1.3 + 0.05, 2), len(new_ig)))
    if new_fb:
        todo.append(('fbp_sf_ds_links', C.FB_POST_LINK, {"direct_urls": [{"url": u} for u in sorted(new_fb.values())]},
                     round(len(new_fb) * 0.00233 * 1.3 + 0.05, 2), len(new_fb)))
    C.parallel(todo, BUDGET)


def charge(name):
    f = RAW / (name + '.json')
    if not f.exists():
        return 0.0, 'not run', 0
    body = json.load(open(f, encoding='utf-8'))
    tok, rid = os.environ.get('APIFY_API_TOKEN'), (body.get('run') or {}).get('id')
    n = len(body.get('items') or [])
    if tok and rid:
        req = urllib.request.Request(C.API_BASE + '/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok})
        r = json.load(urllib.request.urlopen(req, timeout=40))['data']
        return r.get('usageTotalUsd') or 0.0, r.get('status'), n
    return body.get('cost_usd') or 0.0, (body.get('run') or {}).get('status'), n


FINDINGS = ['## What it shows (20 Oct)', '',
            '- **Facebook\'s own search, one day at a time, did best:** 12 new posts about V7 for USD 0.27, 10 of them from scraper_one '
            'sorted by latest on 15 Aug. 6 of the 12 are different people posting the same copy-and-paste text ("choose V Cola, an Egyptian '
            'product"). Both scrapers keep to a one-day window (scraper_one 5 to 10 of 10 rows on the day). A month sorted by top (the 19 Oct '
            'June test) returned filler instead.',
            '- **Google, a week at a time:** 7 new Instagram and about 7 new Facebook posts about V7 in August, about USD 0.05 to 0.07 a post '
            'with fetching. Most of what it finds is off topic.',
            '- **Google, a day at a time:** results keep to the day, but quiet days are filled with near matches (Cambodia\'s V-Cola, other '
            'colas, random posts): Instagram 10 of 295 new finds about V7, Facebook 1 of 125. About USD 0.11 to 0.76 a post. Not worth it.',
            '- **The snippet can\'t pre-filter Google\'s finds:** the phrase is missing from it for 6 of the 14 new Instagram posts about V7 '
            'and 5 of the 7 Facebook ones.',
            '- **Whole test:** USD 2.87 on Apify\'s meter (71.83 to 74.70); 661 new posts collected and labelled, 33 about V7 (Instagram 14, '
            'Facebook 19), 32 of them from August. Not in the dashboard yet.', '']


def report():
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    about = lambda it: bool((labels.get(it['id']) or {}).get('about'))
    ds = lambda r: '_ds_' in r or '_dst_' in r
    new = lambda it: bool(it.get('found_by')) and all(ds(r) for r in it['found_by'])
    pub = [it for it in items if it['kind'] == 'post' and it['src'] == 'ugc' and it['pl'] in ('ig', 'fb')]
    by_key = {}
    for it in pub:
        if it['pl'] == 'ig':
            by_key[('ig', it['id'].split(':', 1)[1])] = it
        else:
            for u in [it.get('url')] + (it.get('urls') or []):
                m = FB_LINK.search(u or '')
                if m: by_key[('fb', m.group(1))] = it
            for k in ('post_id', 'video_id'):
                if it.get(k): by_key[('fb', str(it[k]))] = it
            by_key[('fb', it['id'].split(':', 1)[1].lstrip('v'))] = it
    lines = ['# Date slices: a test (20 Oct 2026)', '',
             'The user\'s idea: search one day at a time so each search returns that day\'s posts. Tested on August 2026. **New** means no '
             'earlier route had found the post; **about V7** is Claude\'s label. Cost is Apify\'s charge for the search runs; fetching the new '
             'finds by link is counted apart.', '', '## Google\'s site search, August', '',
             '| Search | Searches | Pages | Cost (USD) | Posts found | In the collection | Found before | New | New, about V7 | Of the month search\'s finds |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    month = {'ig': month_links('ig_google_months', 'ig'), 'fb': month_links('fbc_google_months', 'fb')}
    summary = {}
    for name, label in [('ig_google_months', 'Google, Instagram, the month (19 Oct)')] + [(n, GOOGLE_RUNS[n]) for n in ('igl_ds_week', 'igl_ds_day')] + \
                       [('fbc_google_months', 'Google, Facebook, the month (19 Oct)')] + [(n, GOOGLE_RUNS[n]) for n in ('fbl_ds_week', 'fbl_ds_day')]:
        pl = 'ig' if name.startswith('ig') else 'fb'
        if name.endswith('_months'):
            found, cost, pages, searches = month[pl], None, None, (len(IG_TERMS) if pl == 'ig' else len(FB_TERMS))
        else:
            found = google_links(name)
            cost, status, pages = charge(name)
            body = json.load(open(RAW / (name + '.json'), encoding='utf-8')) if (RAW / (name + '.json')).exists() else {}
            searches = len([q for q in (body.get('input') or {}).get('queries', '').split('\n') if q])
        its = {k: by_key.get(k) for k in found}
        got = [it for it in its.values() if it]
        inwin = len(got)
        known = sum(1 for it in got if not new(it))
        nw = [it for it in got if new(it)]
        nwa = [it for it in nw if about(it)]
        of_month = '' if name.endswith('_months') else '%d of %d' % (len(set(found) & set(month[pl])), len(month[pl]))
        summary[name] = (cost, len(nwa))
        lines.append('| %s | %s | %s | %s | %d | %d | %d | %d | %d | %s |' % (label, searches, pages if pages is not None else '', '%.3f' % cost if cost is not None else '(19 Oct)',
                                                                          len(found), inwin, known, len(nw), len(nwa), of_month))
    lines += ['', 'Posts found = distinct post links in the results, V7\'s own pages left out. In the collection = fetched and kept (posted 20 Apr '
              'to 16 Oct). The 19 Oct month search read 3 pages (Instagram) or 2 (Facebook) for each phrase.', '']
    # Facebook's own search, one day at a time
    lines += ['## Facebook\'s own search, one day at a time', '',
              '| Day | Keyword | Scraper | Rows | On that day | About V7 | New, about V7 | Of that day\'s posts collected before |', '|---|---|---|---:|---:|---:|---:|---:|']
    before = collections.defaultdict(set)
    for it in pub:
        if it['pl'] == 'fb' and about(it) and not new(it):
            before[it['date'][:10]].add(it['id'])
    fbcost, rows, ab_all, new_all = 0.0, 0, set(), set()
    for day in FB_DAYS:
        tag = day[5:].replace('-', '')
        for i, k in enumerate(FB_KW, 1):
            for fam, scraper in (('fbp_one', 'scraper_one, latest'), ('fbp_sf', 'silentflow, top')):
                name = f'{fam}_ds_{tag}_{i}'
                c, status, n = charge(name)
                fbcost += c
                mine = [it for it in pub if name in (it.get('found_by') or [])]
                on_day = [it for it in mine if it['date'][:10] == day]
                ab = [it for it in mine if about(it)]
                nwa = [it for it in ab if new(it)]
                hit = len({it['id'] for it in ab} & before[day])
                rows += n; ab_all |= {it['id'] for it in ab}; new_all |= {it['id'] for it in nwa}
                lines.append('| %s | %s | %s | %d | %d | %d | %d | %d of %d |' % (day, k, scraper, n, len(on_day), len(ab), len(nwa), hit, len(before[day])))
    lines += ['', 'Facebook\'s own search, all 18 runs: %d rows, %d distinct posts about V7, %d of them new; USD %.3f.' % (rows, len(ab_all), len(new_all), fbcost), '']
    fc_ig, _, n_ig = charge('igp_post_ds_links')
    fc_fb, _, n_fb = charge('fbp_sf_ds_links')
    lines += ['## Fetching the new finds by link', '', '- Instagram: %d posts, USD %.3f. Facebook: %d posts, USD %.3f.' % (n_ig, fc_ig, n_fb, fc_fb), '']
    lines += FINDINGS
    (HERE / 'DATESLICE_TEST.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    {'check': check, 'run': run, 'fetch': fetch, 'report': report}[sys.argv[1]]()
