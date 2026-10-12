"""Version 14: Online stores redesign (Summary first, V7-first detail tabs)."""
import asyncio
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails=0
def check(name,ok,info=''):
    global fails
    if not ok: fails+=1
    print(('  ok ' if ok else 'FAIL ')+name+(' :: '+str(info) if info!='' else ''))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        async def click(sel): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(350)
        await pg.goto(SRC); await pg.wait_for_timeout(900)
        await click('.side .nav[data-view=stores]')
        tabs=await J("[...document.querySelectorAll('.subtabs [data-act=stab]')].map(b=>b.textContent)")
        check('five sub-tabs, Summary first', tabs==['Summary','Prices','Sales & ranks','Stock','Ratings'], tabs)
        sel=await J("document.querySelector('.subtabs [aria-selected=true]').textContent"); check('opens on Summary', sel=='Summary', sel)
        check('summary hides the date and post filters', await J("document.getElementById('filtersRow').hidden"))
        h=await J("document.getElementById('content').scrollHeight"); check('summary is short (under 1,700 px)', h<1700, h)   # 1,600 before the Stock column (11 Oct 2026)
        att=await J("[...document.querySelectorAll('.attn .al .t1')].map(x=>x.textContent)")
        check('needs attention lists Noon pricing, low stock, Apple Malt pack and missing listings', len(att)==4 and 'Noon sellers' in att[0] and 'running low' in att[1], att)
        rows=await J("document.querySelectorAll('.smx tbody tr').length"); check('matrix has all 12 products', rows==12, rows)
        over=await J("[...document.querySelectorAll('.smx .px.over')].map(x=>x.textContent)"); check('matrix marks prices above the shelf price', 'EGP 25' in over and 'EGP 22.70' in over, over)
        low=await J("[...document.querySelectorAll('.smx td.sk .av.low')].map(x=>{const td=x.closest('td');return [td.parentElement.querySelector('th').textContent,td===td.parentElement.lastElementChild,x.textContent]})"); check('matrix says which listing is low (Noon’s stock column)', low==[['Piña Colada',True,'8 left']], low)
        comp=await J("!!document.querySelector('.cmpt')"); check('competitor table shown when competitors are on', comp)
        cells=await J("[...document.querySelectorAll('.cmpt tbody tr')].map(r=>r.querySelector('th').textContent)"); check('competitor table rows', cells==['Amazon.eg sales, last month','Places in Amazon’s top 20','Rating','Can price per 100 ml'], cells)
        await click('[data-act=comp][data-v="0"]')
        t=await J("document.getElementById('content').innerText"); check('competitors off: no competitor table or names', not await J("!!document.querySelector('.cmpt')") and 'PepsiCo' not in t)
        await click('[data-act=comp][data-v="1"]')
        await click('[data-act=stab][data-v=prices]')
        segs=await J("[...document.querySelectorAll('[data-act=pseg]')].map(b=>b.textContent)"); check('price chart has drink-type switch', len(segs)==5, segs)
        await click('[data-act=pseg][data-v=malt]'); nb=await J("document.querySelectorAll('.pbars .bar').length"); check('malt drinks segment shows malt rows', nb>=5, nb)
        pr=await J("[...document.querySelectorAll('.ptab tbody tr')].map(r=>[r.className,r.lastElementChild.textContent])")
        check('price table follows the drink type, V7 first, others compared with V7', len(pr)>=2 and pr[0][0]=='mine' and all(('than V7' in x[1]) or ('same as V7' in x[1]) for x in pr[1:]), pr)
        n1=await J("document.querySelectorAll('.pm tbody tr').length"); await click('[data-act=sopen][data-v=v7detail]'); d=await J("[...document.querySelectorAll('.pm tbody tr')].length"); check('V7 price detail opens on demand', n1==0 and d==12, (n1,d))
        await click('[data-act=stab][data-v=ranks]')
        chips=await J("[...document.querySelectorAll('.place')].map(x=>x.textContent)"); check('top 20 chips use product names', chips==['#1V Cola Diet','#5Pineapple Malt','#8Lemon Mint'], chips)
        r0=await J("document.querySelectorAll('#content tr[data-act=rankd]').length"); await click('[data-act=sopen][data-v=rankComp]'); r1=await J("document.querySelectorAll('#content tr[data-act=rankd]').length")
        check('rank table: competitor rows on demand', r1>r0, (r0,r1))
        await click('[data-act=stab][data-v=ratings]')
        c0=await J("!!document.querySelector('#content table [data-k^=crate]')"); await click('[data-act=sopen][data-v=rateComp]'); c1=await J("document.querySelectorAll('#content table').length")
        check('competitor ratings open on demand', not c0 and c1==2, (c0,c1))
        for w in (390,820):
            q=await b.new_page(viewport={'width':w,'height':900}); await q.goto(SRC); await q.wait_for_timeout(800)
            await q.evaluate("document.querySelector('.side .nav[data-view=stores]').click()"); await q.wait_for_timeout(400)
            fits=await q.evaluate("[...document.querySelectorAll('.smx, .cmpt')].every(t=>t.scrollWidth<=t.parentElement.clientWidth+1)")
            check(f'[{w}] summary tables fit without sideways scroll', fits and await q.evaluate("document.documentElement.scrollWidth")<=w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
