import json, re, random, time, math, urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
areas=[l.strip().split(' ',2) for l in open('tal/areas_sel.txt') if l.strip()]
totals={l.split('|')[0]:int(l.split('|')[2]) for l in open('tal/area_totals.txt') if l.strip()}
def page(aid,slug,p):
    url=f'https://www.talabat.com/egypt/restaurants/{aid}/{slug}?page={p}&sort=a_z'
    h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=40).read().decode('utf-8','ignore')
    d=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S).group(1))['props']['pageProps']['data']
    return d
out={}
for aid,slug,name in areas:
    N=totals[aid]; P=math.ceil(N/15)
    rnd=random.Random(int(aid)); pages=sorted(rnd.sample(range(1,P+1),5))
    vs=[]
    for p in pages:
        for attempt in range(3):
            try: d=page(aid,slug,p); break
            except Exception as e: print('retry',name,p,e); time.sleep(4)
        for v in d['vendors']:
            vs.append({k:v.get(k) for k in ['branchId','restaurantId','name','cuisineString','rate','totalRatings','branchName','latitude','longitude','branchSlug','restaurantSlug','isTalabatGO','verticalType','isGrocery','minimumOrderAmount','deliveryFee','avgDeliveryTime']}|{'page':p})
        time.sleep(1.5)
    rest=[v for v in vs if not v['isGrocery'] and (v['verticalType'] in (0,None))]
    out[aid]={'name':name,'slug':slug,'total':N,'pages':pages,'vendors':vs,'restaurants':rest}
    print(f'{name:15s} total {N:5d} pages {pages} -> {len(vs)} vendors, {len(rest)} restaurants')
json.dump(out,open('tal/sample_listing.json','w'),ensure_ascii=False)
