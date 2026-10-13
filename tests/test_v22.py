"""Version 22: V7's own posts backfilled to the dashboard's first day (16 Apr 2026; Instagram from 27 May), pulled 13 Oct.
The older real posts bring real moments: the V Lemon relaunch, V Cola's "Raise the flag" World Cup campaign, the new can design."""
import asyncio, os, pathlib, re
from playwright.async_api import async_playwright
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
        async def click(sel,w=500): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        async def nav(v): await click(f'.side .nav[data-view={v}]',700)
        async def span(a,z):
            await click('#customBtn',300)
            await J(f"document.getElementById('dFrom').value='{a}';document.getElementById('dTo').value='{z}';document.getElementById('dateForm').requestSubmit()"); await pg.wait_for_timeout(800)
        def panel(title): return f"[...document.querySelectorAll('.panel')].find(p=>{{const h=p.querySelector('h2');return h&&h.textContent.startsWith({title!r});}})"
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        # Our content over the whole period
        await nav('owned'); await span('2026-04-16','2026-10-12')
        hint=await J(panel('Our posts')+".querySelector('.hint').textContent")
        m=re.search(r'(\d+) real, (\d+) demo',hint)
        check('180 days: 129 real posts, a few demo ones (Instagram before 27 May)', m and int(m.group(1))==129 and 0<int(m.group(2))<=12, hint)
        await click('[data-act=more][data-k=own]',600)
        demo=await J("[..."+panel('Our posts')+".querySelectorAll('tbody tr')].filter(r=>!r.querySelector('.real')).map(r=>[r.children[0].textContent.trim(),r.children[1].textContent.trim()])")
        check('the demo posts are Instagram posts from before 27 May', demo and all('Image' in x[1] or 'Reel' in x[1] or 'Carousel' in x[1] for x in demo) and all(re.match(r'\d+ (Apr|May)$',x[0]) for x in demo), demo[:6])
        # the V Lemon relaunch week: the real reels lead
        await span('2026-05-19','2026-05-25')
        top=await J("[..."+panel('Our posts')+".querySelectorAll('tbody tr')].map(r=>[r.children[2].textContent.trim().slice(0,40),r.children[4].textContent.trim()])")
        check('19–25 May: the real V Lemon videos, 11.8M views on Facebook among them', any('V Lemon' in t[0] and t[1]=='12M' for t in top), top[:5])
        # events
        await nav('events')
        on=await J("[...document.querySelectorAll('.evr .evr-t')].map(e=>e.textContent)")
        for n in ['Lemon-Lime relaunched as V Lemon','V Cola “Raise the flag” World Cup campaign','“Hello Summer”: the new can design']:
            check('real event on the charts: '+n, any(n in x and 'Real' in x for x in on), [x for x in on if n[:12] in x])
        # the World Cup weeks: V Cola leads the conversation
        await nav('products'); await span('2026-05-28','2026-07-07')
        cards=await J("[...document.querySelectorAll('.pcard')].map(c=>[c.dataset.v,+c.querySelector('.k-v').textContent.replace(/,/g,'')])")
        best=max(cards,key=lambda c:c[1])
        check('28 May – 7 Jul: V Cola is the most-discussed product', best[0]=='cola', sorted(cards,key=lambda c:-c[1])[:4])
        await pg.close()
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1000)
            await q.evaluate("document.querySelector('.side .nav[data-view=owned]').click()"); await q.wait_for_timeout(500)
            w=await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
            check(f'[390 {cs}] Our content doesn’t scroll sideways', w<=390, w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
