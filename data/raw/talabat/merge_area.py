import json,re,collections,sys
R=json.load(open('rest_with_loc.json'))
M=json.load(open('menu_area.json'))
s=json.load(open('sample_listing.json'))
bn={v['branchId']:v['branchName'] for a in s.values() for v in a['restaurants']}
def key(t): return re.sub(r'[^a-z0-9]','',(t or '').lower())
def district(t): return key(re.split(r'\s*-\s*',t or '')[0])
alias={'mohandiseen':'mohandesin','mohandessin':'mohandesin','elsheikhzayed':'sheikhzayed','elmaadi':'maadi','maadiold':'maadi','newmaadi':'maadi','zahraaelmaadi':'maadi','maadicorniche':'maadi','tagammoa5':'newcairo','tagammoa1':'newcairo','6thofoctober':'october'}
def dn(t): d=district(t); return alias.get(d,d)
GENERIC={'cairo','cairo governorate','giza','giza governorate','egypt'}
stats=collections.Counter(); diffs=[]
for r in R:
    m=M.get(str(r['id'])) or {}
    off=m.get('areaName')
    if m.get('http')==404: stats['gone (404)']+=1; r['x']=1
    if not off: stats['no Talabat area']+=1; continue
    stats['Talabat area']+=1
    old=r['l']
    if not old: stats['name had no area']+=1
    elif key(old)==key(off) or key(off) in key(old) or key(old) in key(off): stats['same area']+=1
    elif dn(old)==dn(off): stats['same district']+=1
    else: stats['different district']+=1; diffs.append((bn[r['id']],off))
    if off.strip().lower() in GENERIC and old: stats['kept specific branch-name area']+=1
    else: r['l']=off
print(dict(stats))
for d in diffs[:25]: print('  name:',d[0],'| Talabat:',d[1])
json.dump(R,open('rest_final.json','w'),ensure_ascii=False)
