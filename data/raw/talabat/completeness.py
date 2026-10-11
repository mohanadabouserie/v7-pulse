import json,glob,re,random,time,urllib.request,sys
sys.path.insert(0,'.')
from brands2 import detect
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
AIDS=['8045','7772','8196','7534','7595','7611','7676','7842','8062','10063']
menus={}
for f in glob.glob('menus_*.json')+glob.glob('area_*.json')+['test_zamalek.json','test_bid.json']:
    if 'retry' in f: continue
    for r in json.load(open(f))['items']:
        if r.get('menu_items'): menus[str(r.get('branch_id'))]=r
R=[r for r in json.load(open('rest_v2.json'))['REST'] if r.get('m')]
random.seed(33); S=random.sample(R,30)
norm=lambda s: re.sub(r'\s+',' ',(s or '').strip().lower())
out=[]
for r in S:
    url=f"https://www.talabat.com/egypt/restaurant/{r['id']}/{r['u']}?aid={AIDS[r['a'][0]]}"
    try:
        h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=40).read().decode('utf-8','ignore')
        live=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S).group(1))['props']['pageProps']['initialMenuState']['menuData']['items']
    except Exception as e: out.append({'n':r['n'],'err':str(e)[:60]}); time.sleep(2); continue
    scraped=menus[str(r['id'])]['menu_items']
    Ls={norm(i['name']) for i in live}; Ss={norm(i['name']) for i in scraped}
    miss=sorted(Ls-Ss); extra=sorted(Ss-Ls)
    br_live=sorted({b for i in live for b,c,w in detect(i['name'],i.get('description',''))}); br_scr=sorted({b for i in scraped for b,c,w in detect(i['name'],i.get('description',''))})
    out.append({'n':r['n'],'live':len(Ls),'scraped':len(Ss),'missing_in_scrape':miss[:12],'n_missing':len(miss),'n_extra':len(extra),'brands_live':br_live,'brands_scraped':br_scr})
    time.sleep(1.3)
json.dump(out,open('completeness.json','w'),ensure_ascii=False,indent=1)
ok=[o for o in out if 'err' not in o]
print('checked',len(ok),'| errors',len(out)-len(ok))
print('identical item sets:',sum(1 for o in ok if o['n_missing']==0 and o['n_extra']==0))
print('same brands found:',sum(1 for o in ok if o['brands_live']==o['brands_scraped']))
for o in ok:
    if o['n_missing'] or o['brands_live']!=o['brands_scraped']: print(' ',o['n'],'| live',o['live'],'scraped',o['scraped'],'| missing',o['n_missing'],o['missing_in_scrape'][:6],'| brands live',o['brands_live'],'scraped',o['brands_scraped'])
