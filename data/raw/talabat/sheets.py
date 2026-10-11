import json,os,textwrap
from PIL import Image,ImageDraw,ImageFont
D=json.load(open('items_v2.json'))
def font(sz):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/TTF/DejaVuSans-Bold.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p,sz)
    return ImageFont.load_default()
F=font(15); FS=font(12)
def sheet(tiles,out,cols=4,tw=260,th=260,cap=34):
    rows=(len(tiles)+cols-1)//cols
    W=cols*tw; H=rows*(th+cap)
    S=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(S)
    for i,(path,label) in enumerate(tiles):
        x=(i%cols)*tw; y=(i//cols)*(th+cap)
        try:
            im=Image.open(path).convert('RGB'); im.thumbnail((tw-8,th-8))
            S.paste(im,(x+(tw-im.width)//2,y+(th-im.height)//2))
        except Exception as e: d.text((x+10,y+10),'no image',fill='red',font=F)
        d.rectangle([x,y,x+tw-1,y+th+cap-1],outline='#bbb')
        d.text((x+6,y+th+2),label[:cap],fill='black',font=F)
    S.save(out,quality=88); return out
NAMES={'blue':'Blueberry','lmint':'Lemon Mint','llime':'Lemon Lime (Carrefour)','llime_amz':'Lemon Lime (Amazon)','pina':'Pina Colada','pine':'Pineapple','pom':'Pomegranate','pink':'Pink Lemonade','amalt':'Apple Malt','pmalt':'Pineapple Malt','cola':'V Cola','dcola':'V Cola Diet'}
os.makedirs('img/sheets',exist_ok=True)
print(sheet([(f'img/ref/{k}.jpg',v) for k,v in NAMES.items()],'img/sheets/ref.jpg',cols=4,tw=240,th=240,cap=24))
U=D['v7_unclear']
for i,x in enumerate(U): x['i']=i
for s in range(0,len(U),12):
    print(sheet([(x['f'],f"#{x['i']} {x['n']}") for x in U[s:s+12]],f'img/sheets/v7_{s//12}.jpg',cols=4,tw=260,th=260,cap=24))
# generic: one tile per unique image
G=D['gen_img']; uniq={}
for x in G: uniq.setdefault(x['f'],[]).append(x)
GU=[{'f':f,'names':sorted({x['n'] for x in xs}),'n_items':len(xs)} for f,xs in uniq.items()]
for i,g in enumerate(GU): g['i']=i
for s in range(0,len(GU),20):
    print(sheet([(g['f'],f"G{g['i']} {g['names'][0]}") for g in GU[s:s+20]],f'img/sheets/gen_{s//20}.jpg',cols=5,tw=210,th=210,cap=22))
D['gen_uniq']=GU; json.dump(D,open('items_v2.json','w'),ensure_ascii=False,indent=0)
print('generic unique images',len(GU))
