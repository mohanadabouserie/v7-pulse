import json,re,html,collections
DASH='/home/mohanad/My_Laptop/D_Data/Jobs/Current/9. V7 Social Media Project/V7_Pulse_Dashboard.html'
src=open(DASH,encoding='utf-8').read()
m=re.search(r'var REST=(\[.*?\]);\n',src,re.S); REST=json.loads(m.group(1))
assert json.dumps(REST,ensure_ascii=False,separators=(',',':'))==m.group(1), 'round-trip differs'
AREAS=json.loads(re.search(r'var REST_AREAS=(\[.*?\]);',src).group(1))
names={}
for i,s_,t in re.findall(r'href="/egypt/restaurants/(\d+)/([^"?]+)"[^>]*>(.*?)</a>',open('sitemap.html',encoding='utf-8',errors='ignore').read(),re.S):
    names[int(i)]=html.unescape(re.sub('<[^>]+>','',t)).strip()
sa={int(k):v for k,v in json.load(open('shoparea.json')).items()}
s=json.load(open('sample_listing.json'))
by_slug=collections.defaultdict(list)
for aid,a in s.items():
    for v in a['restaurants']:
        L=by_slug[v['branchSlug']]
        if not any(x['branchId']==v['branchId'] for x in L): L.append(v)
def clean(bn,brand):
    bn=re.sub(r'\b(TMP|TGO|tgo|Tmp|DS)\b','',(bn or '')).strip(' ,-')
    if ',' in bn: x=bn.split(',',1)[1]
    elif ' - ' in bn: x=bn.split(' - ',1)[1]
    else: return ''
    parts=[t.strip(' ,-') for t in re.split(r',\s*(?=[A-Za-z])',x)]
    x=max(parts,key=len) if parts else ''
    x=re.sub(r'\s+-\s*|\s*-\s+',' - ',x); x=re.sub(r'\s+',' ',x).strip(' ,-')
    if x and x==x.upper():
        bw=[w.lower() for w in re.findall(r"[A-Za-z']+",brand)]
        ws=[w for w in x.split(' ') if not (w.isalpha() and any(b==w.lower() or (len(w)>=3 and b.startswith(w.lower())) for b in bw))]
        x=' '.join(w if w=='-' or len(w)<=3 else w.capitalize() for w in ws); x=re.sub(r'\s*-\s*',' - ',x).strip(' -')
    elif x and x==x.lower():
        x=' '.join(w.capitalize() for w in x.split(' '))
    return x
out=[];src_count=collections.Counter();changed=[]
for r in REST:
    cands=by_slug.get(r['u'],[])
    if len(cands)>1:
        aids={AREAS[i]['id'] for i in r['a']}
        cands=[v for v in cands if v['name'].strip()==r['n']] or cands
    assert cands, ('no match',r['n'],r['u'])
    v=cands[0]
    off=names.get((sa.get(v['branchId']) or {}).get('shopArea'))
    raw=clean(v['branchName'],v['name'])
    lab=off or raw
    src_count['talabat area' if off else 'branch name' if raw else 'none']+=1
    if off and raw and off!=raw: changed.append((v['branchName'],'->',off))
    r2=dict(r); r2['id']=v['branchId']; r2['l']=lab
    out.append(r2)
print('records',len(out),dict(src_count))
print('ids unique',len({r['id'] for r in out})==len(out))
for c in changed[:40]: print('  ',*c)
json.dump(out,open('rest_with_loc.json','w'),ensure_ascii=False)
