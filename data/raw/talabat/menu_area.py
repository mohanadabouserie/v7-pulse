import json,re,urllib.request,time,os
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
AIDS=['8045','7772','8196','7534','7595','7611','7676','7842','8062','10063']
R=[r for r in json.load(open('rest_with_loc.json')) if r.get('m') and (r.get('c',0)&7)]
OUT='menu_area.json'
done=json.load(open(OUT)) if os.path.exists(OUT) else {}
n=0
for r in R:
    k=str(r['id'])
    if k in done and done[k].get('ok'): continue
    url=f"https://www.talabat.com/egypt/restaurant/{r['id']}/{r['u']}?aid={AIDS[r['a'][0]]}"
    rec={'ok':False}
    for attempt in range(3):
        try:
            h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=40).read().decode('utf-8','ignore')
            d=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S).group(1))['props']['pageProps']
            rest=(d.get('initialMenuState') or {}).get('restaurant') or {}
            rec={'ok':True,'areaName':rest.get('areaName'),'name':rest.get('name'),'status':rest.get('statusCode') if 'statusCode' in rest else rest.get('status')}
            break
        except urllib.error.HTTPError as e:
            rec={'ok':e.code==404,'http':e.code}; break
        except Exception as e:
            rec={'ok':False,'err':str(e)[:80]}; time.sleep(5)
    done[k]=rec; n+=1
    if n%25==0:
        json.dump(done,open(OUT,'w'),ensure_ascii=False); print('progress',len(done),'of',len(R),flush=True)
    time.sleep(1.2)
json.dump(done,open(OUT,'w'),ensure_ascii=False)
ok=sum(1 for v in done.values() if v.get('areaName'))
print('DONE',len(done),'with areaName',ok,'| http errors',sum(1 for v in done.values() if v.get('http')),'| failed',sum(1 for v in done.values() if not v.get('ok')),flush=True)
