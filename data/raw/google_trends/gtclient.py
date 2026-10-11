import json, urllib.request, urllib.parse, http.cookiejar, time, random
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
def _get(url,tries=4):
    for i in range(tries):
        try:
            r=op.open(urllib.request.Request(url,headers=UA),timeout=40); b=r.read().decode('utf-8','ignore')
            return json.loads(b[b.index('{'):] if b.startswith(')') else b)
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(20*(i+1)); continue
            raise
    raise RuntimeError('rate limited')
_get_home=lambda: op.open(urllib.request.Request('https://trends.google.com/trends/?geo=EG',headers=UA),timeout=30).read()
def explore(keywords,cat=0,time_='today 12-m',geo='EG'):
    req={"comparisonItem":[{"keyword":k,"geo":geo,"time":time_} for k in keywords],"category":cat,"property":""}
    d=_get('https://trends.google.com/trends/api/explore?'+urllib.parse.urlencode({'hl':'en-US','tz':'-120','req':json.dumps(req,ensure_ascii=False)}))
    time.sleep(2+random.random()*2); return d['widgets']
def widget(w,kind):
    path={'TIMESERIES':'multiline','GEO_MAP':'comparedgeo','RELATED_QUERIES':'relatedsearches','RELATED_TOPICS':'relatedsearches'}[kind]
    d=_get(f'https://trends.google.com/trends/api/widgetdata/{path}?'+urllib.parse.urlencode({'hl':'en-US','tz':'-120','req':json.dumps(w['request'],ensure_ascii=False),'token':w['token']}))
    time.sleep(2+random.random()*2); return d
def related(keyword,cat=0,time_='today 12-m'):
    ws=explore([keyword],cat,time_); out={}
    for w in ws:
        if w['id']=='RELATED_QUERIES':
            d=widget(w,'RELATED_QUERIES'); rk=d['default']['rankedList']
            out['top']=[(x['query'],x['value']) for x in rk[0]['rankedKeyword']]; out['rising']=[(x['query'],x.get('formattedValue')) for x in rk[1]['rankedKeyword']]
    return out
def series(keywords,cat=0,time_='today 12-m'):
    ws=explore(keywords,cat,time_); res={'keywords':keywords,'cat':cat}
    for w in ws:
        if w['id']=='TIMESERIES':
            d=widget(w,'TIMESERIES'); tl=d['default']['timelineData']
            res['weeks']=[x['formattedTime'] for x in tl]; res['values']=[x['value'] for x in tl]; res['partial']=[bool(x.get('isPartial')) for x in tl]
        if w['id']=='GEO_MAP' and len(keywords)==1:
            d=widget(w,'GEO_MAP'); res['geo']=[(x['geoName'],x['value'][0]) for x in d['default']['geoMapData']]
    return res
_get_home()
