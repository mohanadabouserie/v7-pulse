import json, os, sys, urllib.request
TOK = os.environ['APIFY_API_TOKEN']
SP = sys.argv[1]
actors = sys.argv[2:]
def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOK}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)
for a in actors:
    slug = a.replace('/', '~')
    try:
        act = get(f'https://api.apify.com/v2/acts/{slug}')['data']
    except Exception as e:
        print(a, 'ACT ERROR', e); continue
    tb = act.get('taggedBuilds') or {}
    bid = (tb.get('latest') or next(iter(tb.values()), {})).get('buildId')
    pricing = (act.get('pricingInfos') or [{}])[-1]
    info = {'title': act.get('title'), 'users30d': (act.get('stats') or {}).get('totalUsers30Days'),
            'pricingModel': pricing.get('pricingModel'), 'notice': act.get('notice'), 'deprecated': act.get('isDeprecated')}
    out = {'act': info}
    if bid:
        try:
            b = get(f'https://api.apify.com/v2/actor-builds/{bid}')['data']
            ad = b.get('actorDefinition') or {}
            out['readme'] = b.get('readme') or ad.get('readme') or ''
            out['dataset'] = (ad.get('storages') or {}).get('dataset')
            out['input'] = b.get('inputSchema') or ad.get('input')
        except Exception as e:
            out['build_error'] = str(e)
    fn = os.path.join(SP, 'actors', slug + '.json')
    json.dump(out, open(fn, 'w'), ensure_ascii=False, indent=1)
    print(f"{a:55s} users30d={info['users30d']} pricing={info['pricingModel']} readme={len(out.get('readme',''))} dataset={'yes' if out.get('dataset') else 'no'} {('BUILD ERR '+out['build_error']) if 'build_error' in out else ''}")
