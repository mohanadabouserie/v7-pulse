import json, re, time, urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
s=json.load(open('tal/sample_listing.json'))
want={v['branchId'] for a in s.values() for v in a['restaurants']}
got={}
def page(aid,slug,p):
    url=f'https://www.talabat.com/egypt/restaurants/{aid}/{slug}?page={p}&sort=a_z'
    h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=40).read().decode('utf-8','ignore')
    return json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S).group(1))['props']['pageProps']['data']['vendors']
for aid,a in s.items():
    for p in a['pages']:
        for attempt in range(3):
            try: vs=page(aid,a['slug'],p); break
            except Exception as e: print('retry',a['name'],p,e); time.sleep(4); vs=[]
        for v in vs:
            if v['branchId'] in want and v['branchId'] not in got:
                got[v['branchId']]={k:v.get(k) for k in ['shopArea','branchName','menuUrl','latitude','longitude','status','statusCode']}
        time.sleep(1.2)
    print(a['name'],'found so far',len(got),'of',len(want))
json.dump({str(k):v for k,v in got.items()},open('tal/shoparea.json','w'),ensure_ascii=False)
print('missing',len(want-set(got)))
