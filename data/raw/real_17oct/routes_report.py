"""20 Oct 2026: what the date slices and the user's ideas 1 and 2 added ("do 1 and 2"). For each route of 20 Oct: the public posts it
returned that are in the collection, how many are about V7 (Claude's label), how many of those no earlier route had (new), how many only
this route found, and Apify's charge for its runs (final run records, with APIFY_API_TOKEN). Writes ROUTES_20OCT.md.
Usage: python3 routes_report.py"""
import collections, json, os, pathlib, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
ROUTES = [   # label, run-name prefixes
    ('Test: Facebook\'s own search by day (3 days, two scrapers)', ('fbp_one_ds_', 'fbp_sf_ds_', 'fbp_one_dst_', 'fbp_sf_dst_')),
    ('Test: Google by day and week, August (fetched by link)', ('igp_post_ds_links', 'fbp_sf_ds_links')),
    ('Facebook\'s own search by day, 30 busiest days (scraper_one, latest)', ('fbp_one_dd_',)),
    ('Google by week, Instagram, the other months (fetched by link)', ('igp_post_gw_links',)),
    ('Google by week, Facebook, the other months (fetched by link)', ('fbp_sf_gw_links',)),
    ('Instagram searches repeated, session 1', ('igkw_rep1_', 'igreels_rep1_')),
    ('Instagram searches repeated, session 2', ('igkw_rep2_', 'igreels_rep2_')),
    ('Instagram searches repeated, session 3', ('igkw_rep3_', 'igreels_rep3_')),
    ('Account feeds, Instagram (10 accounts)', ('igp_post_acct_',)),
    ('Account feeds, Facebook (10 pages)', ('fbp_ap_acct_',)),
]
SEARCH_COST = {   # the Google searches behind the fetched links (their own runs)
    'Test: Google by day and week, August (fetched by link)': ('igl_ds_day', 'igl_ds_week', 'fbl_ds_day', 'fbl_ds_week', 'fbl_dst_google', 'igl_dst_google2'),
    'Google by week, Instagram, the other months (fetched by link)': ('igl_gw',),
    'Google by week, Facebook, the other months (fetched by link)': ('fbl_gw',),
}
NEW_PREFIXES = tuple(p for _, ps in ROUTES for p in ps)
REFRESH = ('fbd_posts_views', 'fbd_posts_names', 'vis_posts_', 'fbf_', 'igspeech_', 'ig_profiles', 'fbcm_', 'igcm_')   # gap fills: they re-read posts already found


def charge(name):
    f = RAW / (name + '.json')
    if not f.exists():
        return 0.0
    body = json.load(open(f, encoding='utf-8'))
    tok, rid = os.environ.get('APIFY_API_TOKEN'), (body.get('run') or {}).get('id')
    if tok and rid:
        req = urllib.request.Request('https://api.apify.com/v2/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok})
        return json.load(urllib.request.urlopen(req, timeout=40))['data'].get('usageTotalUsd') or 0.0
    return body.get('cost_usd') or 0.0


def main():
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    about = lambda it: bool((labels.get(it['id']) or {}).get('about'))
    pub = [it for it in items if it['kind'] == 'post' and it['src'] == 'ugc' and it['pl'] in ('fb', 'ig')]
    finders = lambda it: [r for r in it.get('found_by') or [] if not r.startswith(REFRESH)]
    new = lambda it: bool(finders(it)) and all(r.startswith(NEW_PREFIXES) for r in finders(it))
    def route_of(r):   # the route with the longest matching prefix (fbp_sf_ds_links is the Google test's fetch, not Facebook's day search)
        best = max(((len(p), lab) for lab, ps in ROUTES for p in ps if r.startswith(p)), default=(0, None))
        return best[1]
    lines = ['# What the 20 Oct routes added', '',
             'Public Facebook and Instagram posts in the collection (20 Apr to 16 Oct). **New** means no route before 20 Oct had found it; '
             '**only here** means no other route, of any day, found it. Cost is Apify\'s charge for the route\'s runs, the Google searches '
             'behind fetched links included.', '',
             '| Route | Posts returned | About V7 | New, about V7 | Only here, about V7 | Cost (USD) | USD a new post about V7 |',
             '|---|---:|---:|---:|---:|---:|---:|']
    tot_new = set()
    for lab, ps in ROUTES:
        mine = [it for it in pub if any(route_of(r) == lab for r in it.get('found_by') or [])]
        ab = [it for it in mine if about(it)]
        nw = [it for it in ab if new(it)]
        only = [it for it in ab if all(route_of(r) == lab for r in finders(it))]
        tot_new |= {it['id'] for it in nw}
        runs = sorted({f.stem for p in ps for f in RAW.glob(p + '*.json') if route_of(f.stem) == lab} | set(SEARCH_COST.get(lab, ())))
        cost = sum(charge(n) for n in runs)
        lines.append('| %s | %d | %d | %d | %d | %.2f | %s |' % (lab, len(mine), len(ab), len(nw), len(only), cost,
                                                                  '%.3f' % (cost / len(nw)) if nw else ''))
    by_pl = collections.Counter(it['pl'] for it in pub if it['id'] in tot_new)
    lines += ['', 'New posts about V7 from all the 20 Oct routes together: %d (Facebook %d, Instagram %d).' % (len(tot_new), by_pl['fb'], by_pl['ig']), '']
    (HERE / 'ROUTES_20OCT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
