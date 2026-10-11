import json,glob,sys,re,collections
sys.path.insert(0,'tal')
from brands import classify_item, standalone, LARGE
CODE={'V Cola':'VC','V7':'V7','Coca-Cola':'CC','Sprite':'SP','Fanta':'FA','Schweppes':'SC','Pepsi':'PE','7UP':'7U','Mirinda':'MI','Mountain Dew':'MD','Birell':'BI','Fayrouz':'FY','Barbican':'BA','Spiro Spathis':'SS','Big Cola':'BC'}
COBIT={'V7':1,'Coca-Cola':2,'PepsiCo':4,'Other':8}
GROUPS=['Burgers & fried chicken','Pizza & Italian','Egyptian & grills','Shawarma & Levantine','Asian & sushi','Seafood','Cafés, bakeries & desserts','Sandwiches & other']
def cgroup(cs):
    c=(cs or '').lower()
    rules=[(6,['coffee','café','cafe','dessert','bakery','sweets','ice cream','waffle','crepe','juice','beverage','bubble tea','donut','cake','karak','pastr']),
           (0,['burger','fried chicken','chicken','fast food','hot dog']),(1,['pizza','italian','pasta']),
           (3,['shawarma','shawerma','syrian','lebanese','manakeesh','manaqeesh']),
           (2,['koshary','koshari','egyptian','grill','feteer','foul','falafel','kebab','kofta','liver','mandi','arabic','oriental']),
           (5,['fish','seafood']),(4,['sushi','asian','chinese','japanese','indian','thai','korean'])]
    for g,kw in rules:
        if any(k in c for k in kw): return g
    return 7
def v7prod(n):
    s=n.lower()
    if re.search(r'cola',s) or 'كولا' in s: return 'dcola' if re.search(r'diet|zero|دايت|زيرو',s) else 'cola'
    if re.search(r'malt|barley|شعير',s): return 'amalt' if re.search(r'apple|تفاح',s) else 'pmalt'
    if re.search(r'pina|piña|colada|binacolada|penacolada|pinacolada|coconut|بينا',s): return 'pina'
    if re.search(r'pomegranate|رمان',s): return 'pom'
    if re.search(r'blue|berry|توت',s): return 'blue'
    if re.search(r'pink',s): return 'pink'
    if re.search(r'lime|لايم',s): return 'llime'
    if re.search(r'mint|نعناع',s): return 'lmint'
    if re.search(r'pineapple|ananas|أناناس|اناناس',s): return 'pine'
    if re.search(r'cream|كريم',s): return 'cream'
    return 'x'
menus={}
for f in glob.glob('tal/menus_*.json')+glob.glob('tal/area_*.json')+['tal/test_zamalek.json','tal/test_bid.json']:
    if 'retry' in f: continue
    for r in json.load(open(f))['items']:
        if r.get('menu_items'): menus[str(r.get('branch_id'))]=r
s=json.load(open('tal/sample_listing.json'))
aids=list(s.keys())
def analyse(m):
    cos=0; brands=set(); price={}; items=collections.Counter(); vp=set()
    for it in m['menu_items']:
        f=classify_item(it.get('name',''))
        if not f: continue
        for b,co in f:
            cos|=COBIT[co]; brands.add(CODE[b])
            if co=='V7': vp.add(v7prod(it.get('name','')) if b=='V7' else ('dcola' if re.search(r'diet|zero|دايت|زيرو',it.get('name',''),re.I) else 'cola'))
        if standalone(it.get('name',''),f):
            b,co=f[0]; items[{'V7':'v','Coca-Cola':'c','PepsiCo':'p','Other':'o'}[co]]+=1
            try: pr=float(it.get('price'))
            except: pr=None
            if pr and 3<pr<150 and not LARGE.search(it.get('name','')):
                k=CODE[b]; price[k]=min(price.get(k,1e9),pr)
    return cos,sorted(brands),price,dict(items),sorted(vp)
REST=[];idx={}
for ai,aid in enumerate(aids):
    for v in s[aid]['restaurants']:
        b=str(v['branchId'])
        if b in idx: REST[idx[b]]['a'].append(ai); continue
        rec={'n':v['name'].strip(),'a':[ai],'g':cgroup(v['cuisineString']),'cu':(v['cuisineString'] or '').strip(),'r':v['rate'],'nr':v['totalRatings'],'u':v.get('branchSlug') or ''}
        m=menus.get(b)
        if m:
            cos,br,pr,it,vp=analyse(m); rec.update({'m':1,'c':cos,'b':br,'p':{k:round(x,2) for k,x in pr.items()},'i':it,'v':vp})
        else: rec['m']=0
        idx[b]=len(REST); REST.append(rec)
AREAS=[{'id':aid,'n':s[aid]['name'],'tot':s[aid]['total'],'s':len(s[aid]['restaurants'])} for aid in aids]
for ai,a in enumerate(AREAS): a['m']=sum(1 for r in REST if ai in r['a'] and r['m'])
# Most visible (first listing page of each area, Talabat's default order)
vis={}
for f in glob.glob('tal/area_*.json')+['tal/test_zamalek.json']:
    for r in json.load(open(f))['items']:
        if r.get('menu_items'): vis[str(r['branch_id'])]=r
V=[analyse(r) for r in vis.values()]
VIS={'n':len(V),'v':sum(1 for x in V if x[0]&1),'c':sum(1 for x in V if x[0]&2),'p':sum(1 for x in V if x[0]&4)}
VIS['v7chains']=sorted({r['name'].strip() for r,x in zip(vis.values(),V) if x[0]&1})[:40]
out='/* Real data: Talabat menus, 10 Cairo delivery areas, collected 5 Oct 2026 (random sample of each area\'s full restaurant list) */\n'
out+='var REST_AREAS='+json.dumps(AREAS,ensure_ascii=False)+';\n'
out+='var REST_GROUPS='+json.dumps(GROUPS,ensure_ascii=False)+';\n'
out+='var REST_VIS='+json.dumps(VIS,ensure_ascii=False)+';\n'
out+='var REST='+json.dumps(REST,ensure_ascii=False,separators=(',',':'))+';\n'
open('tal/rest_js.js','w').write(out)
print('REST',len(REST),'with menus',sum(r['m'] for r in REST),'bytes',len(out)); print(AREAS); print({k:v for k,v in VIS.items() if k!='v7chains'}, VIS['v7chains'][:15])
vp=collections.Counter(x for r in REST if r['m'] for x in r.get('v',[])); print('V7 products on menus',vp)
