import json,re,glob
amz=json.load(open('comp/amazon_comp.json'))['items']
car=json.load(open('comp/carrefour_comp.json'))['items']
for f in glob.glob('comp/car_*.json'): car+=json.load(open(f))['items']
noon=[]
for f in glob.glob('comp/noon_*.json'):
    if 'comp.json' in f: continue
    noon+=json.load(open(f))['items']
def pv(x):
    p=x.get('price'); return p.get('value') if isinstance(p,dict) else p
def amzpick(title_rx):
    for x in amz:
        if re.search(title_rx,x.get('title') or '',re.I): return x
    raise SystemExit('amazon not found '+title_rx)
def carpick(name_rx):
    for x in car:
        if re.search(name_rx,x.get('name') or '',re.I): return x
    raise SystemExit('carrefour not found '+name_rx)
def noonpick(rx):
    for x in noon:
        if re.search(rx,x.get('name') or '',re.I): return x
    raise SystemExit('noon not found '+rx)
def rank(x):
    out={}
    br=x.get('bestsellerRanks') or []
    for b in br:
        if b.get('category')=='Grocery': out['g']=b.get('rank')
        elif 'cr' not in out and b.get('category') not in ('Grocery','Home & Kitchen','Sports & Outdoors','Sports Water Bottles','Drinking Flasks'): out['cr']=b.get('rank'); out['c']=b.get('category')
    return out
def bought(x):
    m=x.get('monthlyPurchaseVolume') or ''
    mm=re.match(r'([\d.]+)(K?)\+',m)
    if not mm: return None,None
    v=float(mm.group(1))*(1000 if mm.group(2) else 1); return int(v), mm.group(0)
C=[]
def A(co,b,seg,rx,ml,pk=1,label=None):
    x=amzpick(rx); bv,bl=bought(x); r=rank(x)
    C.append({'co':co,'b':b,'seg':seg,'s':'Amazon.eg','t':label or x['title'][:70],'p':pv(x),'ml':ml,'pk':pk,'st':bool(x.get('inStock')),'r':x.get('stars'),'n':x.get('reviewsCount'),'bv':bv,'bl':bl,**r,'u':(x.get('url') or '').split('?')[0]})
def Cf(co,b,seg,rx,ml,pk=1,label=None):
    x=carpick(rx)
    C.append({'co':co,'b':b,'seg':seg,'s':'Carrefour','t':label or x['name'],'p':x.get('price'),'reg':x.get('regularPrice'),'ml':ml,'pk':pk,'st':bool(x.get('available')),'u':x.get('url')})
def N(co,b,seg,rx,ml,label=None):
    x=noonpick(rx)
    C.append({'co':co,'b':b,'seg':seg,'s':'Noon','t':label or x['name'][:70],'p':x.get('price'),'ml':ml,'pk':1})
# Amazon.eg
A('pepsi','Pepsi','cola',r'^Pepsi Cola Soft Drink, 355 ml Can',355)
A('pepsi','Pepsi','cola',r'Extra Caffeine',355,label='Pepsi Extra Caffeine, 355 ml can')
A('pepsi','Pepsi','cola',r'Pepsi 400Ml',400,label='Pepsi, 400 ml bottle')
A('pepsi','Pepsi Diet','diet',r'Pepsi Cola Diet, 355ml',355)
A('coke','Coca-Cola','cola',r'^Coca-Cola Can 300 ml',300)
A('coke','Coca-Cola Zero','diet',r'^Coca-Cola Zero Can 300 ml',300)
A('coke','Sprite','lemon',r'Sprite Twist off 330',330,label='Sprite, 330 ml bottle')
A('pepsi','7UP','lemon',r'7UP, Carbonated Soft Drink, Can, 355',355,label='7UP, 355 ml can')
A('pepsi','7UP','lemon',r'7UP 250ML PET',250,label='7UP, 250 ml bottle')
A('pepsi','Mirinda','fruit',r'Mirinda Orange 355ml, Can',355,label='Mirinda Orange, 355 ml can')
A('pepsi','Mirinda','fruit',r'Mirinda Orange Soft Drink, 400 ml',400,label='Mirinda Orange, 400 ml bottle')
A('pepsi','Mountain Dew','lemon',r'Mountain Dew 400ml',400,label='Mountain Dew, 400 ml bottle')
A('coke','Fanta','fruit',r'Fanta Orange - Pack Of 24',330,24,label='Fanta Orange, 24 × 330 ml')
A('coke','Schweppes','fruit',r'Schweppes Pineapple 330ml x24',330,24,label='Schweppes Pineapple, 24 × 330 ml')
A('other','Moussy','malt',r'Moussy Pomegranate',275,6,label='Moussy Pomegranate malt, 6 × 275 ml')
# Carrefour Egypt
Cf('coke','Coca-Cola','cola',r'^Coca Cola Original Taste Soft Drink Can - 300ml',300)
Cf('coke','Coca-Cola Zero','diet',r'^Coca Cola Zero - 500 ml',500)
Cf('pepsi','Pepsi','cola',r'^Pepsi Cola Soft Drink - 355ml',355)
Cf('pepsi','Pepsi Diet','diet',r'^Pepsi Cola Diet Soft Drink - 355ml',355)
Cf('coke','Sprite','lemon',r'Sprite Lemon Lime Soda Drink Glass Bottle - 330ml',330)
Cf('pepsi','7UP','lemon',r'^7 Up Soft Drink Pet Bottle - 390 ml',390)
Cf('pepsi','Mountain Dew','lemon',r'^Mountain Dew Soft Drink - 355ml',355)
Cf('coke','Fanta','fruit',r'Fanta Orange Soft Drink Can - 320ml',320)
Cf('pepsi','Mirinda','fruit',r'Mirinda Apple Soft Drink Can - 355ml',355)
Cf('coke','Schweppes','fruit',r'^Schweppes Pomegranate Soft Drink - 240ml',240)
Cf('coke','Schweppes','fruit',r'^Schweppes Tangerine Soft Drink - 240ml',240)
Cf('coke','Schweppes Gold','malt',r'Schweppes Gold Pineapple Malt Drink Can - 250ml',250)
Cf('coke','Schweppes Gold','malt',r'Schweppes Gold Strawberry Malt Beverage - 240ml',240)
Cf('other','Barbican','malt',r'Barbican Orange Malt Drink - 330 ml',330)
Cf('other','Moussy','malt',r'Moussy Malt Drink - Peach Flavor - 275ml',275)
Cf('other','Vamos','malt',r'Vamos Apple Cinnamon Malt Beverage - 300 ml',300)
Cf('other','Shnider','malt',r'Shnider Peach Malt Drink - 385Ml',385)
Cf('other','Big Cola','cola',r'^Big Cola Carbonated Soft Drink - 360ml',360)
Cf('other','Maxi Cola','cola',r'^Maxi Cola Soft Drink - 300ml',300)
# Noon Egypt
N('pepsi','Pepsi','cola',r'Pepsi Cola Flavored Soft Drink Can 285ml',285,'Pepsi, 285 ml can')
N('pepsi','7UP','lemon',r'7up Lemon-Lime Flavored Soft Drink Can 285ml',285,'7UP, 285 ml can')
N('coke','Schweppes','fruit',r'Schweppes Pomegranate Flavoured Can 300ml',300,'Schweppes Pomegranate, 300 ml can')
N('coke','Schweppes Gold','malt',r'Pineapple Gold Flavour 320ml',320,'Schweppes Gold Pineapple, 320 ml')
def fmt(c):
    t=(c.get('t','')+' '+(c.get('u') or '')).lower()
    if 'glass' in t: return 'glass bottle'
    if re.search(r'\bpet\b|-pet|pet-|plastic|bottle',t): return 'bottle'
    if re.search(r'\bcan\b|-can|can-|cans',t): return 'can'
    return 'can' if c.get('ml') in (240,250,285,300,320,330,355) else 'bottle'
for c in C:
    c['f']=fmt(c)
    for k in list(c):
        if c[k] is None: del c[k]
out='/* Real data: competitor listings on Amazon.eg, Carrefour Egypt and Noon, collected 5 Oct 2026 */\nvar COMP='+json.dumps(C,ensure_ascii=False,separators=(',',':'))+';\n'
open('comp/comp_js.js','w').write(out); print(len(C),'listings',len(out),'bytes')
for c in C: print(c['s'][:6],c['b'],c['seg'],c['p'],c.get('ml'),c.get('pk'),c.get('bl'),c.get('cr'),c.get('c'))
