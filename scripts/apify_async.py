import json, os, sys, time, urllib.request, urllib.error
TOK=os.environ['APIFY_API_TOKEN']
def call(method,path,body=None):
    req=urllib.request.Request('https://api.apify.com/v2'+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers={'Authorization':'Bearer '+TOK,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(req,timeout=120))
def run_async(actor,body,out,max_usd,max_items=None,wait=900):
    q=f'?maxTotalChargeUsd={max_usd}'+(f'&maxItems={max_items}' if max_items else '')
    r=call('POST',f'/acts/{actor}/runs{q}',body)['data']; rid=r['id']; t=time.time()
    while True:
        time.sleep(10); s=call('GET',f'/actor-runs/{rid}')['data']
        if s['status'] in ('SUCCEEDED','FAILED','ABORTED','TIMED-OUT'): break
        if time.time()-t>wait: call('POST',f'/actor-runs/{rid}/abort'); s['status']='ABORTED-BY-ME'; break
    items=call('GET',f"/datasets/{s['defaultDatasetId']}/items?clean=1&format=json") if s['status']!='ABORTED-BY-ME' else []
    if isinstance(items,dict): items=items.get('data',items)
    json.dump({'input':body,'status':s['status'],'usage':s.get('usageTotalUsd'),'items':items},open(out,'w'),ensure_ascii=False)
    print(f"{actor}: {s['status']} {len(items)} items in {time.time()-t:.0f}s, run cost ${s.get('usageTotalUsd')} -> {out}")
    return items
if __name__=='__main__':
    spec=json.load(open(sys.argv[1])); run_async(spec['actor'],spec['input'],spec['out'],spec['maxUsd'],spec.get('maxItems'),spec.get('wait',900))
