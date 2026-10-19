"""19 Oct 2026: scores the Facebook reel and video searches tested by `collect.py fbreeltest` on the same four keywords (V7 كريم صودا,
V7 cream soda, ڤي كولا, ڤي سڤن), the way the Instagram reel scrapers were checked against each other: which reels about V7 (posted
20 Apr to 16 Oct, not by V7's own pages) each one finds, which ones only it finds, and how much they overlap. A reel's date, text and
label come from the collection (items.json, labels.json) once it has been fetched by link (fbreeldetails) and labelled.
Usage: python3 fbreel_report.py [--todo]   (--todo writes fbreel_todo.json: the reels not collected yet, to fetch by link)"""
import collections, itertools, json, os, pathlib, re, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
SCRAPERS = [   # label, Store link, runs
    ('Apify search, reels', 'apify/facebook-search-scraper', ['fbrt_apifyreels_%d' % i for i in (1, 2, 3, 4)]),
    ('alien_force, reels only', 'alien_force/facebook-search-scraper', ['fbrt_alien_%d' % i for i in (1, 2, 3, 4)]),
    ('Apify video search', 'apify/facebook-video-search-scraper', ['fbrt_apifyvideo_%d' % i for i in (1, 2, 3, 4)]),
    ('igview-owner video search', 'igview-owner/facebook-search-scraper', ['fbrt_igview_%d' % i for i in (1, 2, 3, 4)]),
    ('lexis-solutions Watch search', 'lexis-solutions/facebook-videos-watch-scraper', ['fbrt_lexis_%d' % i for i in (1, 2, 3, 4)]),
    ('easyapi Watch search', 'easyapi/facebook-videos-scraper', ['fbrt_easyapi_%d' % i for i in (1, 2, 3, 4)]),
    ('headply video search', 'headply/facebook-video-search-scraper', ['fbrt_headply']),
    ('axesso video search', 'axesso_data/facebook-video-search-scraper', ['fbrt_axesso']),
    ('sasky video links', 'sasky/facebook-keyword-videos-urls-scraper', ['fbrt_sasky']),
    ('natanielsantos video search', 'natanielsantos/facebook-video-search-scraper', ['fbrt_nataniel']),
    ('thenetaji video search', 'thenetaji/facebook-video-search-scraper', ['fbrt_thenetaji']),
    ('automation-lab video search', 'automation-lab/facebook-public-video-search-results', ['fbrt_autolab']),
    ('Google short videos (Facebook)', 'simple.actor/google-short-videos', ['fbrt_google']),
]
VID = re.compile(r'facebook\.com/(?:reel/|watch/?\?v=|[^"\s?]+/videos/(?:[^/"\s?]+/)?|video\.php\?v=)(\d{8,})')
OWN = re.compile(r'facebook\.com/(?:V7Egypt|Vsupersoda)(?:[/?"]|$)|"(?:V7Egypt|V7 Egypt|V Super Soda)"', re.I)


def vids_of(x):
    """The video ids a result row points to (its own link first)."""
    s = json.dumps(x, ensure_ascii=False)
    out = []
    for k in ('url', 'videoUrl', 'video_url', 'reelUrl', 'link', 'post_url', 'permalink', 'videoLink'):
        v = x.get(k) if isinstance(x, dict) else None
        if isinstance(v, str):
            m = VID.search(v)
            if m: out.append(m.group(1))
    for k in ('videoId', 'video_id', 'postId'):
        if isinstance(x, dict) and str(x.get(k) or '').isdigit() and 'reel' in (x.get('url') or x.get('videoUrl') or '') + str(x.get('searchType', '')):
            out.append(str(x[k]))
    out += VID.findall(s)[:1]
    return list(dict.fromkeys(out))


def charge(body):
    tok, rid = os.environ.get('APIFY_API_TOKEN'), (body.get('run') or {}).get('id')
    if tok and rid:
        r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok}), timeout=40))['data']
        return r.get('usageTotalUsd') or 0, r.get('status')
    return body.get('cost_usd') or 0, (body.get('run') or {}).get('status')


def collected():
    """video id -> item id for every public Facebook post in the collection, and the labels."""
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    vmap = {}
    for it in items:
        if it['pl'] != 'fb' or it['kind'] != 'post':
            continue
        for u in [it.get('url')] + it.get('urls', []):
            m = VID.search(u or '')
            if m: vmap[m.group(1)] = it
        if it['id'].startswith('fb:v'):
            vmap[it['id'][4:]] = it
    return vmap, labels


def main():
    vmap, labels = collected()
    useful = lambda it: it is not None and it['src'] == 'ugc' and bool((labels.get(it['id']) or {}).get('about'))
    rows, sets, todo = [], {}, {}
    for label, link, runs in SCRAPERS:
        found, cost, notes, n = set(), 0.0, [], 0
        for name in runs:
            f = RAW / (name + '.json')
            if not f.exists():
                notes.append(name + ' did not run'); continue
            body = json.load(open(f, encoding='utf-8'))
            c, status = charge(body); cost += c
            if status != 'SUCCEEDED': notes.append('%s %s' % (name, status))
            for x in body.get('items') or []:
                if not isinstance(x, dict) or x.get('error'):
                    continue
                vs = vids_of(x)
                if not vs:
                    continue
                n += 1
                v = vs[0]
                it = vmap.get(v)
                if it is None and not OWN.search(json.dumps(x, ensure_ascii=False)):
                    todo[v] = 'https://www.facebook.com/reel/%s/' % v if 'reel' in json.dumps(x) else 'https://www.facebook.com/watch/?v=%s' % v
                if useful(it):
                    found.add(it['id'])
        sets[label] = found
        rows.append((label, link, n, len(found), cost, notes))
    union = set().union(*sets.values())
    print('%-34s %7s %7s %6s %9s  %s' % ('scraper', 'videos', 'useful', 'only', 'cost', 'notes'))
    for label, link, n, u, cost, notes in rows:
        only = len(sets[label] - set().union(*(s for k, s in sets.items() if k != label)))
        print('%-34s %7d %7d %6d  $%.3f  %s' % (label, n, u, only, cost, '; '.join(notes)))
    print('\nUseful reels and videos found by all of them together: %d (not collected yet: %d to fetch)' % (len(union), len(todo)))
    names = [r[0] for r in rows if sets[r[0]]]
    print('\nOverlap (useful found by both):')
    for a, b in itertools.combinations(names, 2):
        m = len(sets[a] & sets[b])
        if m or (sets[a] and sets[b]):
            est = round((len(sets[a]) + 1) * (len(sets[b]) + 1) / (m + 1) - 1)
            print('  %-30s x %-30s %3d %3d both %3d  -> about %d' % (a[:30], b[:30], len(sets[a]), len(sets[b]), m, est))
    if '--todo' in sys.argv:
        json.dump(todo, open(HERE / 'fbreel_todo.json', 'w', encoding='utf-8'), indent=1)
        print('wrote fbreel_todo.json: %d reels and videos to fetch' % len(todo))


if __name__ == '__main__':
    main()
