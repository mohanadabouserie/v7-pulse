import json, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'.')
from apify_run import run, usage
areas=[l.strip().split(' ',2) for l in open('tal/areas_sel.txt') if l.strip()]
def one(a):
    aid,slug,name=a
    body={"country":"eg","fullCatalog":True,"catalogAreas":[aid],"maxPagesPerArea":5,"scrapeMenu":True,"maxItems":75,"maxConcurrency":8}
    try: items=run('memo23~talabat-scraper', body, f'tal/area_{aid}.json', 75, 0.1, 290)
    except Exception as e: print(name,'ERR',e); items=None
    return name, (len(items) if items is not None else None)
u0=usage()
with ThreadPoolExecutor(3) as ex:
    for name,n in ex.map(one, areas): print('DONE',name,n)
time.sleep(5); u1=usage(); print(f'usage ${u0:.4f} -> ${u1:.4f} (+${u1-u0:.4f})')
