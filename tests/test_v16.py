"""Version 16: Online stores in plain words. Stock status first, rank and rating rows open full charts,
prices compared like for like, and the Summary's price and stock table in words."""
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
        async def click(sel,w=400): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        await click('.side .nav[data-view=stores]')
        # Summary: price and stock in words
        h2=await J("document.querySelector('.smx').closest('.panel').querySelector('h2').textContent")
        check('summary table says what it shows', h2.startswith('V7 price and stock in each store'), h2)
        over=await J("[...document.querySelectorAll('.smx .s2.bad')].map(x=>x.textContent)")
        check('prices above the shelf price say by how much', any('over shelf price' in x for x in over), over)
        check('no stock dots, words instead', await J("!document.querySelector('.smx .sdot')"))
        stk=await J("[[...document.querySelectorAll('.smx thead th')].map(t=>t.textContent.trim()).pop(),[...document.querySelectorAll('.smx td.stk .av')].map(x=>x.className.split(' ')[1]+':'+x.textContent),[...document.querySelectorAll('.smx tbody td:not(.stk)')].some(t=>/stock|Low|Out/.test(t.textContent)),getComputedStyle(document.querySelector('.smx .stk-m')).display]")
        check('stock in its own column, store columns show prices only', stk[0]=='Stock' and stk[1].count('in:✓ In stock')==10 and 'low:Low on Noon · 8 left' in stk[1] and not stk[2] and stk[3]=='none', stk)
        # Stock
        await click('[data-act=stab][data-v=stock]')
        ban=await J("[document.querySelector('.sbanner').className,document.querySelector('.sbanner').textContent]")
        check('stock opens with one sentence: all can be bought, one running low', 'warn' in ban[0] and 'All 24 V7 listings can be bought right now' in ban[1] and 'Piña Colada on Noon (Only 8 left)' in ban[1], ban[1])
        av=await J("[document.querySelectorAll('.avail tbody tr').length,[...document.querySelectorAll('.avail thead th')].map(t=>t.textContent)]")
        check('availability grid: 12 products by 3 stores', av[0]==12 and av[1]==['Product','Amazon.eg','Carrefour','Noon'], av)
        cell=await J("[...document.querySelectorAll('.avail tbody tr')].find(r=>r.textContent.includes('Piña Colada')).lastElementChild.textContent")
        check('Piña Colada on Noon shows low with the count', cell=='Low · 8 left', cell)
        probs=await J("[...document.querySelectorAll('.prob:not(.prob-head)')].map(r=>[r.querySelector('.pn').textContent,r.querySelector('.strip').children.length])")
        check('problem list starts with what is wrong now', probs and probs[0][0].startswith('Piña Colada') and 'Noon' in probs[0][0], probs[:2])
        check('every strip has one cell per day (30)', all(x[1]==30 for x in probs), set(x[1] for x in probs))
        clean=await J("document.querySelector('.prob').closest('.panel').querySelector('.hint-line').textContent")
        check('listings without problems summed up in one line', 'were in stock every day' in clean, clean)
        check('demo days marked lighter, real ones not', await J("document.querySelectorAll('.strip i.dm').length")>0 and await J("[...document.querySelectorAll('.strip')].every(s=>!s.lastElementChild.classList.contains('dm'))"))
        # Ranks: table, rows open the full chart
        await click('[data-act=stab][data-v=ranks]')
        hd=await J("[...document.querySelector('tr[data-act=rankd]').closest('table').querySelectorAll('thead th')].map(t=>t.textContent.replace(/[↓↑]/g,'').trim())")
        check('rank table columns', hd[:5]==['Product','Rank now','Change since 6 Sep','Best','Days at #1'], hd)
        first=await J("document.querySelector('tr[data-act=rankd] .rnow').textContent")
        check('best rank first', first=='#1', first)
        await click('tr[data-act=rankd]',600)
        d=await J("[document.getElementById('drawer').hidden,document.getElementById('drTitle').textContent,document.querySelectorAll('#drBody .bigchart svg').length,[...document.querySelectorAll('#drBody .bigchart text')].map(t=>t.textContent).includes('#1')]")
        check('a rank row opens its full chart, top is #1', d[0] is False and d[2]==1 and d[3], d)
        await J("document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        # Ratings: rows open details, keyboard works
        await click('[data-act=stab][data-v=ratings]')
        await pg.focus('tr[data-act=rated]'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(600)
        r=await J("[document.getElementById('drawer').hidden,document.querySelectorAll('#drBody .srow').length,document.querySelectorAll('#drBody .bigchart svg').length,document.querySelectorAll('#drBody .wk > div').length,document.getElementById('drTitle').textContent]")
        check('Enter on a rating row opens the details', r[0] is False, r)
        check('details: Amazon star split, full chart, full weeks only', r[1]==5 and r[2]==1 and r[3]==4, r)
        cmp=await J("document.querySelectorAll('#drBody table.mini tbody tr').length")
        check('details compare with other products in the category', cmp>=2, cmp)
        await J("document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        # Prices: one drink type at a time
        await click('[data-act=stab][data-v=prices]')
        t1=await J("document.querySelector('.ptab').closest('.panel').querySelector('h2').textContent")
        await click('[data-act=pseg][data-v=fruit]')
        t2=await J("document.querySelector('.ptab').closest('.panel').querySelector('h2').textContent")
        check('price table follows the drink type switch', t1.startswith('Cola:') and t2.startswith('Fruit flavours:'), (t1,t2))
        rows=await J("[...document.querySelectorAll('.ptab tbody tr')].map(r=>[r.querySelectorAll('td.best').length,r.querySelectorAll('td').length])")
        check('each row shades its cheapest store', all(x[0]>=1 for x in rows) and all(x[1]==4 for x in rows), rows)
        await pg.close()
        # phone and dark
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1000)
            await q.evaluate("document.querySelector('.side .nav[data-view=stores]').click()"); await q.wait_for_timeout(400)
            fit=[await q.evaluate("[...document.querySelectorAll('.smx')].every(t=>t.scrollWidth<=t.parentElement.clientWidth+1)")]
            ph=await q.evaluate("[[...document.querySelectorAll('.smx td.stk')].every(t=>getComputedStyle(t).display==='none'),[...document.querySelectorAll('.smx .stk-m')].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.closest('th').textContent)]")
            check(f'[390 {cs}] stock problems move under the product name', ph[0] and ph[1]==['Piña ColadaLow on Noon · 8 left'], ph)
            await q.evaluate("document.querySelector('[data-act=stab][data-v=stock]').click()"); await q.wait_for_timeout(400)
            fit.append(await q.evaluate("(()=>{const t=document.querySelector('.avail');return t.scrollWidth<=t.parentElement.clientWidth+1})()"))
            pw=[]
            for t in ('summary','prices','ranks','stock','ratings'):
                await q.evaluate(f"document.querySelector('[data-act=stab][data-v={t}]').click()"); await q.wait_for_timeout(300)
                pw.append(await q.evaluate("document.documentElement.scrollWidth"))
            check(f'[390 {cs}] summary and stock grids fit, no page scrolls sideways', all(fit) and max(pw)<=390, (fit,pw))
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
