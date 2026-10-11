import json,glob,sys,re,collections,statistics
sys.path.insert(0,'tal')
from brands import classify_item, standalone, LARGE
menus={}
for f in glob.glob('tal/menus_*.json')+glob.glob('tal/area_*.json')+['tal/test_zamalek.json','tal/test_bid.json']:
    if 'retry' in f: continue
    for r in json.load(open(f))['items']:
        if r.get('menu_items'): menus[str(r.get('branch_id'))]=r
s=json.load(open('tal/sample_listing.json'))
AREAS=[(aid,a['name'],a['total']) for aid,a in s.items()]
def cgroup(cs):
    c=(cs or '').lower()
    for g,kw in [('Cafés & desserts',['coffee','café','cafe','dessert','bakery','sweets','ice cream','waffle','crepe','juice','beverage','bubble tea','donut','cake','karak']),
                 ('Burgers & fried chicken',['burger','fried chicken','chicken','fast food','hot dog']),('Pizza & Italian',['pizza','italian','pasta']),
                 ('Shawarma & Syrian/Lebanese',['shawarma','shawerma','syrian','lebanese','manakeesh','manaqeesh']),
                 ('Egyptian & grills',['koshary','koshari','egyptian','grill','feteer','foul','falafel','kebab','kofta','liver','mandi','arabic','oriental']),
                 ('Seafood',['fish','seafood']),('Asian',['sushi','asian','chinese','japanese','indian','thai','korean']),
                 ('Sandwiches & other',[''])]:
        if any(k in c for k in kw): return g
    return 'Sandwiches & other'
def analyse(r):
    brands=collections.defaultdict(set); price=collections.defaultdict(list); items=collections.Counter()
    for m in r['menu_items']:
        f=classify_item(m.get('name',''))
        if not f: continue
        for b,co in f: brands[co].add(b)
        if standalone(m.get('name',''),f):
            b,co=f[0]; items[co]+=1
            pr=m.get('price')
            try: pr=float(pr)
            except: pr=None
            if pr and pr>3 and not LARGE.search(m.get('name','')) and pr<150: price[b].append(pr)
    return brands,price,items
rest={}   # branchId -> record
for aid,a in s.items():
    for v in a['restaurants']:
        b=str(v['branchId'])
        rec=rest.get(b)
        if not rec:
            m=menus.get(b)
            rec={'id':b,'n':v['name'],'cu':v['cuisineString'],'g':cgroup(v['cuisineString']),'r':v['rate'],'nr':v['totalRatings'],'u':'https://www.talabat.com/egypt/'+(v.get('branchSlug') or ''),'areas':[],'menu':bool(m),'go':v.get('isTalabatGO')}
            if m:
                br,pr,it=analyse(m); rec['co']={k:sorted(v) for k,v in br.items()}; rec['p']={k:min(v) for k,v in pr.items()}; rec['it']=dict(it); rec['mi']=len(m['menu_items'])
            rest[b]=rec
        rec['areas'].append(aid)
print('restaurants in sample',len(rest),'with menu',sum(1 for r in rest.values() if r['menu']))
def share(L,pred): return sum(1 for r in L if pred(r))
for aid,name,tot in AREAS+[('ALL','All 10 areas',0)]:
    L=[r for r in rest.values() if r['menu'] and (aid=='ALL' or aid in r['areas'])]
    n=len(L)
    has=lambda co: (lambda r: co in r.get('co',{}))
    v7=share(L,has('V7')); ck=share(L,has('Coca-Cola')); pp=share(L,has('PepsiCo')); oth=share(L,has('Other'))
    anyb=share(L,lambda r: any(k in r.get('co',{}) for k in ['V7','Coca-Cola','PepsiCo']))
    excl_c=share(L,lambda r: 'Coca-Cola' in r.get('co',{}) and 'PepsiCo' not in r.get('co',{}))
    excl_p=share(L,lambda r: 'PepsiCo' in r.get('co',{}) and 'Coca-Cola' not in r.get('co',{}))
    both=share(L,lambda r: 'PepsiCo' in r.get('co',{}) and 'Coca-Cola' in r.get('co',{}))
    v7only=share(L,lambda r: 'V7' in r.get('co',{}) and 'PepsiCo' not in r.get('co',{}) and 'Coca-Cola' not in r.get('co',{}))
    print(f'{name:15s} n={n:3d} | V7 {v7:3d} ({v7*100//max(n,1):2d}%) | Coke {ck:3d} ({ck*100//max(n,1):2d}%) | Pepsi {pp:3d} ({pp*100//max(n,1):2d}%) | other {oth:2d} | any big3 {anyb} ({anyb*100//max(n,1)}%) | coke-only {excl_c} pepsi-only {excl_p} both {both} v7-only {v7only}')
json.dump({'areas':AREAS,'rest':list(rest.values())},open('tal/rest_data.json','w'),ensure_ascii=False)
# prices
P=collections.defaultdict(list)
for r in rest.values():
    for b,p in (r.get('p') or {}).items(): P[b].append(p)
for b,l in sorted(P.items(),key=lambda x:-len(x[1])): print(f'  {b:14s} menus {len(l):3d} median EGP {statistics.median(l):5.1f} (p25 {sorted(l)[len(l)//4]:.0f}, p75 {sorted(l)[3*len(l)//4]:.0f})')
G=collections.defaultdict(lambda: [0,0,0,0])
for r in rest.values():
    if not r['menu']: continue
    g=G[r['g']]; g[0]+=1; co=r.get('co',{}); g[1]+= 'V7' in co; g[2]+='Coca-Cola' in co; g[3]+='PepsiCo' in co
for k,v in sorted(G.items(),key=lambda x:-x[1][0]): print(f'  {k:28s} n={v[0]:3d} V7 {v[1]*100//v[0]:2d}% Coke {v[2]*100//v[0]:2d}% Pepsi {v[3]*100//v[0]:2d}%')
