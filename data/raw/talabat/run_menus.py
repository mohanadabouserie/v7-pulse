import json, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'.')
from apify_run import run, usage
need=json.load(open('tal/need_branches.json'))
chunks=[need[i:i+95] for i in range(0,len(need),95)]   # free users are capped at 100 items a run
def one(ix):
    ch=chunks[ix]
    body={"country":"eg","branchIds":ch,"scrapeMenu":True,"maxItems":len(ch),"maxConcurrency":8}
    try: items=run('memo23~talabat-scraper', body, f'tal/menus_{ix}.json', len(ch), round(len(ch)*0.0012+0.01,3), 290)
    except Exception as e: print(ix,'ERR',e); items=None
    return ix, len(ch), (len(items) if items is not None else None)
u0=usage(); print('chunks',len(chunks),'usage start $%.4f'%u0)
with ThreadPoolExecutor(3) as ex:
    for ix,n,got in ex.map(one, range(len(chunks))): print('DONE chunk',ix,'asked',n,'got',got)
time.sleep(5); u1=usage(); print(f'usage ${u0:.4f} -> ${u1:.4f} (+${u1-u0:.4f})')
