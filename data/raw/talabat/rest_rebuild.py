"""Rebuild restaurant brand data (v2, 5 Oct 2026): names + descriptions, photo labels for unclear items."""
import json,glob,re,collections,hashlib,sys
sys.path.insert(0,'.')
from brands2 import detect, v7_flavour
from brands import standalone as _st, LARGE, SIZE
CODE={'V Cola':'VC','V7':'V7','Coca-Cola':'CC','Sprite':'SP','Fanta':'FA','Schweppes':'SC','Pepsi':'PE','7UP':'7U','Mirinda':'MI','Mountain Dew':'MD','Birell':'BI','Fayrouz':'FY','Barbican':'BA','Spiro Spathis':'SS','Big Cola':'BC','Maxi Cola':'MX','Green Cola':'GC'}
CO_OF={'VC':'V7','V7':'V7','CC':'Coca-Cola','SP':'Coca-Cola','FA':'Coca-Cola','SC':'Coca-Cola','PE':'PepsiCo','7U':'PepsiCo','MI':'PepsiCo','MD':'PepsiCo','BI':'Other','FY':'Other','BA':'Other','SS':'Other','BC':'Other','MX':'Other','GC':'Other'}
COBIT={'V7':1,'Coca-Cola':2,'PepsiCo':4,'Other':8}
D=json.load(open('items_v2.json'))
def key(url): return hashlib.md5((url or '').encode()).hexdigest()[:10]
# ---- photo labels (checked by eye against the reference cans, 5 Oct 2026) ----
PH={}   # image key -> ('v7', flavour|'range'|list) or (company, [brand codes])
V7U={0:'dcola',1:'dcola',2:'llime',3:'llime',4:'cola',5:'NOT7UP',6:'llime',7:'pina',8:'llime',9:'llime',10:'llime',11:'llime',12:'cola',13:'cola',14:'cola',15:'cola',16:'cola',17:'lmint',18:'cola',19:'cola',20:'lmint',21:'cola',22:'cola',23:'cola',24:'lmint',25:'cola',26:'cola',27:'llime',28:'llime',29:'cola',30:'llime',31:'lmint',32:'cola',33:'cola',34:'llime',35:'llime'}
for x in D['v7_unclear']:
    lab=V7U[x['i']]; PH[key(x['img'])]=('PepsiCo',['7U'],'override') if lab=='NOT7UP' else ('v7',lab)
GL={'G6':('v7','range'),'G7':('v7','dcola'),'G14':('v7','cola'),'G16':('v7','cola'),'G29':('v7','cola'),'G31':('v7','cola'),'G36':('v7','range'),'G38':('v7','llime'),'G40':('v7','cola'),'G49':('v7','cola'),'G59':('v7','cola'),'G68':('v7','cola'),'G69':('v7','cola'),'G70':('v7','llime'),'G75':('v7','range'),'G140':('v7','lmint'),'G145':('v7','cola'),'G158':('v7','cola'),
 'G4':('Coca-Cola',['FA','CC','SP']),'G25':('Coca-Cola',['SP','CC','FA']),'G26':('Coca-Cola',['CC']),'G27':('Coca-Cola',['CC']),'G28':('Coca-Cola',['SC']),'G34':('Coca-Cola',['CC','SP']),'G50':('Coca-Cola',['SC']),'G56':('Coca-Cola',['CC']),'G76':('Coca-Cola',['SP','CC','FA']),'G126':('Coca-Cola',['CC']),'G127':('Coca-Cola',['CC']),'G128':('Coca-Cola',['SP']),'G142':('Coca-Cola',['SP','CC','FA']),'G159':('Coca-Cola',['CC']),
 'G10':('PepsiCo',['PE']),'G18':('PepsiCo',['MI']),'G41':('PepsiCo',['PE']),'G42':('PepsiCo',['PE']),'G48':('PepsiCo',['PE']),'G51':('PepsiCo',['PE']),'G52':('PepsiCo',['7U']),'G53':('PepsiCo',['MI']),'G54':('PepsiCo',['PE']),'G67':('PepsiCo',['PE']),'G119':('PepsiCo',['PE']),'G129':('PepsiCo',['PE']),'G141':('PepsiCo',['PE']),'G146':('PepsiCo',['7U','PE','MI']),'G147':('PepsiCo',['PE']),
 'G72':('Other',['BC']),'G143':('Other',['BC']),'G144':('Other',['MX'])}
CL={'C0':('Coca-Cola',['CC']),'C1':('Coca-Cola',['CC']),'C7':('Coca-Cola',['CC']),'C13':('Coca-Cola',['CC']),'C20':('Coca-Cola',['CC']),'C21':('Coca-Cola',['CC']),'C24':('Coca-Cola',['CC']),'C27':('Coca-Cola',['CC']),'C31':('Coca-Cola',['CC']),'C32':('Coca-Cola',['CC']),'C49':('Coca-Cola',['CC']),
 'C12':('v7','dcola'),'C18':('v7','cola'),'C43':('v7','dcola'),'C45':('v7','dcola','override'),
 **{c:('Other',['GC']) for c in ['C22','C23','C37','C38','C39','C40','C41','C46','C47']},**{c:('Other',['MX']) for c in ['C29','C44','C50','C51']},'C48':('Other',['BC'])}
fkey=lambda f: f.split('/')[-1][:10]
for g in D['gen_uniq']:
    if 'G%d'%g['i'] in GL: PH[fkey(g['f'])]=GL['G%d'%g['i']]
for c in D['cola_uniq']:
    if c['i'] in CL: PH[fkey(c['f'])]=CL[c['i']]
NAMED={'boba v7':('v7','blue'),'v 7':('v7',['pina','blue','lmint'])}   # photos checked on the excluded sheet
# ---- per-item analysis ----
GENERIC=re.compile(r'soft\s*drinks?|\bsoda\b|\bcans?\b|cold\s*drink|\bcola\b|\bdrinks?\b|مشروب|كانز|ساقع',re.I)
log=collections.Counter()
def item_brands(it):
    n=(it.get('name') or '').strip(); d=(it.get('description') or '').strip()
    found=detect(n,d)                     # [(brand, company, where)]
    codes=[(CODE[b],w) for b,co,w in found]
    ph=PH.get(key(it.get('image'))); flav=set(); src='text'
    nm=NAMED.get(n.lower())
    if nm: ph=nm
    v7_text=[c for c,w in codes if CO_OF[c]=='V7']
    if ph and len(ph)==3 and ph[2]=='override':      # photo contradicts the name
        if ph[0]=='v7': codes=[(c,w) for c,w in codes if CO_OF[c]=='V7']+[('VC','photo')]; flav={ph[1]}; log['override to V7']+=1
        else: codes=[(c,w) for c,w in codes if CO_OF[c]!='V7']+[(b,'photo') for b in ph[1]]; log['override V7 -> other']+=1
        return codes,flav,n,'photo'
    if v7_text:
        fl=v7_flavour(n) if any(w=='name' for c,w in codes if CO_OF[c]=='V7') else None
        if not fl or fl in ('lemon?','diet?','malt?'):
            fd=v7_flavour(d)
            if fd and fd not in ('lemon?','diet?','malt?'): fl=fd
            elif not fl: fl=fd
        if 'VC' in v7_text and fl in (None,'diet?'): fl='dcola' if re.search(r'diet|zero|دايت|زيرو',n+' '+d,re.I) else 'cola'
        if 'VC' in v7_text and fl=='lemon?': fl='llime'          # V line lemon = V Lemon (Lemon-Lime)
        if (not fl or fl in ('lemon?','diet?','malt?')) and ph and ph[0]=='v7':
            fl=ph[1]; src='photo'; log['flavour from photo']+=1
        if isinstance(fl,list): flav=set(fl)
        elif fl and fl!='range': flav={fl}
        elif fl is None: flav={'x'}
        return codes,flav,n,src
    if not codes and ph and GENERIC.search(n):
        log['brand from photo']+=1
        if ph[0]=='v7':
            fl=ph[1]; return [('VC' if fl in ('cola','dcola','llime') else 'V7','photo')],({fl} if isinstance(fl,str) and fl!='range' else set(fl) if isinstance(fl,list) else set()),n,'photo'
        return [(b,'photo') for b in ph[1]],set(),n,'photo'
    return codes,set(),n,'text'
def analyse(m):
    cos=0;brands=set();price={};items=collections.Counter();vp=set();photo_add=set()
    for it in m['menu_items']:
        codes,flav,n,src=item_brands(it)
        if not codes: continue
        for c,w in codes:
            cos|=COBIT[CO_OF[c]]; brands.add(c)
            if w=='photo': photo_add.add(CO_OF[c])
        vp|=flav
        names_only=[c for c,w in codes if w in ('name','photo')]
        single=len(set(names_only))==1 and len(codes)==1
        st=single and (src=='photo' and GENERIC.search(n) and len(n)<30 or _st(n,[(c,0) for c in names_only]) or (src=='photo' and CO_OF[names_only[0]]=='V7'))
        if st:
            c=names_only[0]; items[{'V7':'v','Coca-Cola':'c','PepsiCo':'p','Other':'o'}[CO_OF[c]]]+=1
            try: pr=float(it.get('price'))
            except: pr=None
            if pr and 3<pr<150 and not LARGE.search(n):
                k='VC' if c=='VC' else c
                if c=='V7' and flav and flav<= {'cola','dcola','llime'}: k='VC'
                price[k]=min(price.get(k,1e9),pr)
    return cos,sorted(brands),{k:round(v,2) for k,v in price.items()},dict(items),sorted(vp),photo_add
menus={}
for f in glob.glob('menus_*.json')+glob.glob('area_*.json')+['test_zamalek.json','test_bid.json']:
    if 'retry' in f: continue
    for r in json.load(open(f))['items']:
        if r.get('menu_items'): menus[str(r.get('branch_id'))]=r
dash='/home/mohanad/My_Laptop/D_Data/Jobs/Current/9. V7 Social Media Project/V7_Pulse_Dashboard.html'
src=open(dash,encoding='utf-8').read()
REST=json.loads(re.search(r'var REST=(\[.*?\]);\n',src,re.S).group(1))
OLD=json.loads(json.dumps(REST))
GROUP_OF=[(0,['burger','fast food','fried chicken','hot dog','broasted']),(1,['pizza','italian','pasta']),
 (2,['egyptian','arabic','grill','kebab','koshar','foul','falafel','feteer','oriental','liver','mandi','hawawshi','rotisserie','fatta']),
 (3,['shawarma','shawerma','lebanese','syrian','levantine','manakeesh','manaqeesh','turkish']),(4,['sushi','asian','chinese','japanese','indian','thai','korean','noodle']),
 (5,['seafood','fish']),(6,['dessert','coffee','tea','beverage','juice','crepe','bakery','pastr','pies','waffle','ice cream','donut','cake','sweets','bubble','karak','breakfast']),(7,['healthy','diet food'])]
GENERIC_CU={'chicken','international','sandwiches','salads','salad','others','offers','soup','soups','kids meals'}
def cgroup2(cu):
    cs=[c.strip().lower() for c in (cu or '').split(',') if c.strip()]
    order=[c for c in cs if c not in GENERIC_CU]+[c for c in cs if c in GENERIC_CU]
    for c in order:
        for g,kw in GROUP_OF:
            if any(k in c for k in kw): return g
    if cs and cs[0]=='chicken': return 0
    return 7
regrouped=0
for r in REST:
    g=cgroup2(r.get('cu'))
    if g!=r.get('g'): regrouped+=1
    r['g']=g
print('restaurants regrouped by main cuisine:',regrouped)
for r in REST:
    m=menus.get(str(r['id']))
    if not m or not r.get('m'): continue
    cos,br,pr,it,vp,pa=analyse(m)
    r.update({'c':cos,'b':br,'p':pr,'i':it,'v':vp})
    if pa: r['ph']=sorted(pa)
vis={}
for f in glob.glob('area_*.json')+['test_zamalek.json']:
    for x in json.load(open(f))['items']:
        if x.get('menu_items'): vis[str(x['branch_id'])]=x
V=[analyse(x) for x in vis.values()]
VIS={'n':len(V),'v':sum(1 for x in V if x[0]&1),'c':sum(1 for x in V if x[0]&2),'p':sum(1 for x in V if x[0]&4)}
VIS['v7chains']=sorted({x['name'].strip() for x,a in zip(vis.values(),V) if a[0]&1})[:40]
json.dump({'REST':REST,'VIS':VIS},open('rest_v2.json','w'),ensure_ascii=False)
# ---- report ----
M=[r for r in REST if r.get('m')]; O=[r for r in OLD if r.get('m')]
sh=lambda L,b: round(100*sum(1 for r in L if r['c']&b)/len(L),1)
print(dict(log))
print('menus',len(M))
for lab,b in [('V7',1),('Coca-Cola Co.',2),('PepsiCo',4)]: print(f'  {lab:14s} old {sh(O,b):5}% -> new {sh(M,b):5}%  ({sum(1 for r in O if r["c"]&b)} -> {sum(1 for r in M if r["c"]&b)} restaurants)')
v7only=lambda L: sum(1 for r in L if r['c']&1 and not r['c']&6)
print('  V7 and no rival: ',v7only(O),'->',v7only(M))
oldvis=json.loads(re.search(r'var REST_VIS=(\{.*?\});',src).group(1))
print('  most visible: V7',oldvis['v'],'->',VIS['v'],'| Coke',oldvis['c'],'->',VIS['c'],'| Pepsi',oldvis['p'],'->',VIS['p'],'of',VIS['n'])
print('  V7 products old:',dict(collections.Counter(x for r in O for x in r.get('v',[]))))
print('  V7 products new:',dict(collections.Counter(x for r in M for x in r.get('v',[]))))
gained=[r['n'] for r,o in zip(REST,OLD) if r.get('m') and r['c']&1 and not o['c']&1]
lost=[r['n'] for r,o in zip(REST,OLD) if r.get('m') and o['c']&1 and not r['c']&1]
print('  V7 gained:',len(gained),gained[:30]); print('  V7 lost:',lost)
print('  photo-only restaurants by company:',dict(collections.Counter(c for r in M for c in r.get('ph',[]))))
