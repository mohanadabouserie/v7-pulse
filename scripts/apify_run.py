import json, os, sys, time, urllib.request, urllib.error
TOK=os.environ['APIFY_API_TOKEN']
def run(actor, body, out, max_items, max_usd, timeout=290):
    url=f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout={timeout}&maxTotalChargeUsd={max_usd}&maxItems={max_items}'
    req=urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization':'Bearer '+TOK,'Content-Type':'application/json'})
    t=time.time()
    try: items=json.load(urllib.request.urlopen(req, timeout=timeout+40))
    except urllib.error.HTTPError as e: print('HTTP',e.code,e.read()[:400]); return None
    json.dump({'input':body,'items':items}, open(out,'w'), ensure_ascii=False)
    print(f'{actor}: {len(items)} items in {time.time()-t:.0f}s -> {out}')
    return items
def usage():
    req=urllib.request.Request('https://api.apify.com/v2/users/me/limits', headers={'Authorization':'Bearer '+TOK})
    return json.load(urllib.request.urlopen(req, timeout=60))['data']['current']['monthlyUsageUsd']
if __name__=='__main__':
    spec=json.load(open(sys.argv[1]))
    u0=usage()
    run(spec['actor'], spec['input'], spec['out'], spec['maxItems'], spec['maxUsd'], spec.get('timeout',290))
    time.sleep(3); u1=usage(); print(f'usage before ${u0:.4f} after ${u1:.4f} (+${u1-u0:.4f})')
