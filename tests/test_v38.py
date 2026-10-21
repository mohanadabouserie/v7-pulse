"""Version 38 (22 Oct 2026): no BGC on Overview and Posts & comments; Our content sits under Posts & comments, shows Our posts as the card
grid (with engagement rate and positive comments) and adds Top comments, a grid sorted by engagement: likes plus replies (DECISIONS #175)."""
import asyncio, os, pathlib
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails = 0
def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e))); J = pg.evaluate
        async def nav(v, w=1200): await J(f"document.querySelector('.side .nav[data-view={v}]').click()"); await pg.wait_for_timeout(w)
        def panel(t): return f"[...document.querySelectorAll('#content .panel')].find(p=>{{const h=p.querySelector('h2');return h&&h.textContent.startsWith({t!r});}})"
        await pg.goto(SRC); await pg.wait_for_timeout(1500)
        order = await J("[...document.querySelectorAll('.side .nav')].map(b=>b.dataset.view)")
        check('Our content comes right after Posts & comments', order[order.index('posts') + 1] == 'owned', order[:5])
        for v in ('overview', 'posts'):
            await nav(v)
            check(f'{v}: no UGC/BGC switch', await J("document.getElementById('srcSeg').hidden"))
        await nav('people')
        check('other pages keep the switch', not await J("document.getElementById('srcSeg').hidden"))
        await nav('owned', 1800)
        g = await J(panel('Our posts') + ".querySelectorAll('.pgrid > .gc').length")
        er = await J("[..." + panel('Our posts') + ".querySelectorAll('.pgrid > .gc')].every(c=>/engagement rate/.test(c.textContent)&&!c.querySelector('.pill'))")
        check('Our posts is a card grid; each card has its engagement rate and no made-up sentiment', g >= 5 and er, g)
        sorts = await J("[..." + panel('Our posts') + ".querySelectorAll('[data-act=ownsort]')].map(b=>b.textContent)")
        check('Our posts can be sorted', sorts == ['Newest', 'Most engagement', 'Most views', 'Engagement rate'], sorts)
        await J("document.querySelector('[data-act=ownsort][data-v=views]').click()"); await pg.wait_for_timeout(700)
        v = await J("[..." + panel('Our posts') + ".querySelectorAll('.pgrid > .gc')].map(c=>+((c.querySelector('.gs[title$=\" views\"]')||{title:'0'}).title.replace(/[^0-9]/g,'')))")
        check('sorted by most views', v == sorted(v, reverse=True), v[:6])
        tc = await J("[..." + panel('Top comments') + ".querySelectorAll('.pgrid > .gcm')].map(c=>[[...c.querySelectorAll('.gs')].reduce((s,x)=>s+ +x.title.replace(/[^0-9]/g,''),0),c.textContent.includes('V7 reply'),!!c.querySelector('.gc-q')])")
        check('Top comments: a grid, most engagement (likes + replies) first', len(tc) == 12 and [t[0] for t in tc] == sorted([t[0] for t in tc], reverse=True), [t[0] for t in tc])
        check('Top comments: no V7 replies, each shows the post it is under', tc and not any(t[1] for t in tc) and all(t[2] for t in tc))
        await J(panel('Top comments') + ".querySelector('.gc-q').click()"); await pg.wait_for_timeout(700)
        check('a comment opens the post it is under', await J("!!document.querySelector('#drBody .pv-t')"))
        await J("document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        await J("document.querySelector('[data-act=owncmall]').click()"); await pg.wait_for_timeout(700)
        n = await J(panel('Top comments') + ".querySelectorAll('.pgrid > .gcm').length")
        check('Show the top 60', n == 60, n)
        ov = await J("""(()=>{let o=0;document.querySelectorAll('#content .pgrid').forEach(g=>{const r=[...g.children].map(x=>x.getBoundingClientRect());for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],b=r[j];if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)o++;}});return o;})()""")
        check('no cards overlap in either grid', ov == 0, ov)
        check('no page errors', not errs, errs[:3])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
