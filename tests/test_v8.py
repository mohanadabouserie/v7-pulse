import asyncio, json
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
ok=[];bad=[]
def check(n,c,i=''): (ok if c else bad).append(n+(' :: '+str(i) if i!='' else ''))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1440,'height':900}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(900); J=pg.evaluate
        async def click(sel): await J(f"document.querySelector({json.dumps(sel)}).click()"); await pg.wait_for_timeout(200)
        # custom date
        k0=await J("document.querySelector('.kpi .k-v').textContent")
        await click('#customBtn'); vis=await J("!document.getElementById('datePop').hidden"); check('custom popover opens',vis)
        await pg.fill('#dFrom','2026-09-15'); await pg.fill('#dTo','2026-09-10'); await click('#dateForm button[type=submit]')
        msg=await J("document.getElementById('dateMsg').textContent"); check('custom validates order','before' in msg,msg)
        await pg.fill('#dFrom','2026-09-01'); await pg.fill('#dTo','2026-09-14'); await click('#dateForm button[type=submit]')
        per=await J("document.getElementById('period').textContent"); lbl=await J("document.getElementById('customBtn').textContent")
        check('custom applies to period', '1 Sep – 14 Sep' in per, per); check('custom button label', lbl=='1 Sep – 14 Sep', lbl)
        k1=await J("document.querySelector('.kpi .k-v').textContent"); check('custom changes KPIs', k1!=k0, (k0,k1))
        await click('.side .nav[data-view=products]'); hint=await J("document.querySelector('.dd-head .period').textContent"); check('products uses custom text','1 Sep – 14 Sep' in hint, hint)
        # stores history with custom range
        await click('.side .nav[data-view=stores]'); await click('[data-act=stab][data-v=stock]')
        per=await J("document.getElementById('period').textContent"); check('stores period uses custom', '1 Sep – 14 Sep' in per, per)
        fr=await J("!document.getElementById('filtersRow').hidden && document.getElementById('platChips').hidden"); check('stores history shows date filter, hides platforms', fr)
        await click('#rangeSeg [data-r="7"]')
        per=await J("document.getElementById('period').textContent"); check('7 days clears custom', '29 Sep – 5 Oct' in per and await J("document.getElementById('customBtn').textContent")=='Custom', per)
        strips=await J("[...document.querySelectorAll('.prob:not(.prob-head) .strip')].map(s=>s.children.length)"); check('problem strips have one cell per day of the range', len(strips)>0 and set(strips)=={7}, strips)
        await click('[data-act=hstore][data-v=Noon]'); cols=await J("[...document.querySelectorAll('.avail thead th')].map(h=>h.textContent)"); check('store filter Noon', cols==['Product','Noon'], cols)
        low=await J("document.querySelector('.sbanner').textContent"); check('status line names Piña Colada running low', 'Running low:' in low and 'Piña Colada' in low and 'Only 8 left' in low, low)
        await click('[data-act=comp][data-v="0"]'); n_ex=await J("document.querySelectorAll('.prob:not(.prob-head)').length"); await click('[data-act=comp][data-v="1"]')
        has=await J("!!document.querySelector('[data-act=sopen][data-v=stkComp]')")
        if has: await click('[data-act=sopen][data-v=stkComp]')
        n_in=await J("document.querySelectorAll('.prob:not(.prob-head)').length")
        check('competitor stock problems open on demand', has and n_in>n_ex, (has,n_ex,n_in))
        if has: await click('[data-act=sopen][data-v=stkComp]')
        # ratings selector
        await click('[data-act=stab][data-v=ratings]')
        vals={}
        for src in ['Amazon.eg','Noon','both']:
            await click(f'[data-act=hrate][data-v="{src}"]'); vals[src]=await J("document.querySelector('.tile .k-v').textContent+' / '+document.querySelector('.tile p').textContent")
        check('ratings Amazon/Noon/Both differ', len(set(vals.values()))==3, vals)
        star=await J("[...document.querySelectorAll('#content th')].some(h=>h.textContent.includes('Amazon stars'))"); check('star split shown for Both', star)
        await click('[data-act=hrate][data-v=Noon]'); star=await J("[...document.querySelectorAll('#content th')].some(h=>h.textContent.includes('Amazon stars'))"); check('no star split for Noon', not star)
        # ranks
        await click('[data-act=stab][data-v=ranks]'); t=await J("document.querySelector('.tile p').textContent"); check('Amazon #1 now tile', 'V Cola' in t, t)
        await click('[data-act=hrank][data-v=Noon]'); t=await J("document.querySelector('.tile p').textContent"); check('Noon #1 now = Pink Lemonade', t=='Pink Lemonade', t)
        tab=await J("[...document.querySelectorAll('#content h2')].some(h=>h.textContent.startsWith('Noon Soft Drinks'))"); check('Noon top 20 table', tab)
        # prices tab still works and hides date filter
        await click('[data-act=stab][data-v=prices]'); fr=await J("document.getElementById('filtersRow').hidden"); check('prices tab hides filters', fr)
        # trends
        await click('.side .nav[data-view=trends]'); lg=await J("document.querySelectorAll('#gtchart path').length")
        nosplit=await J("!document.querySelector('[data-act=gtsplit]') && !document.getElementById('content').textContent.includes('Split by spelling')"); check('trends: no split toggle, one company line', nosplit and lg==1, (nosplit,lg))
        rows=await J("[...document.querySelectorAll('#content table tbody tr td:first-child')].map(t=>t.textContent)"); check('terms table has one V7 row', rows.count('V7, the company')==1 and not any(r.startswith('V7:') for r in rows), rows)
        terms=await J("[...document.querySelectorAll('#content table td')].map(t=>t.textContent).join(' ')"); check('terms list shows exclusions', '-haval' in terms and '"v cola"' in terms)
        # alerts
        await click('.side .nav[data-view=alerts]'); al=await J("document.getElementById('content').textContent"); check('Noon low stock alert', 'Low stock on Noon' in al)
        # assistant built-in search answer
        await click('#askBtn'); await click('#sugg button[data-k=search]'); await pg.wait_for_timeout(400)
        a=await J("document.querySelector('#chatLog .msg.bot:last-child').textContent"); check('search answer uses company series', 'the company' in a and 'noise' not in a.lower(), a[:120])
        print('ERRORS',errs); await b.close()
asyncio.run(main())
print('PASS',len(ok)); [print('  ok',x) for x in ok]
print('FAIL',len(bad)); [print('  !!',x) for x in bad]
