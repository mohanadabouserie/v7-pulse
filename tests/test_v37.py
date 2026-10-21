"""Versions 36 and 37 (22 Oct 2026): Posts & comments.
- Version 36: posts show as picture-first cards in a masonry grid (DECISIONS #173).
- Version 37: the page keeps the name "Posts & comments" in every mode, sorts by most engagement by default, and has no language
  filter and no "V7 official" option under "Posted by" (DECISIONS #174). Outside Egypt keeps its own filters and sort."""
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
        async def click(sel, w=600): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        await pg.goto(SRC); await pg.wait_for_timeout(1500)
        await click('.side .nav[data-view=posts]', 1200)
        names = []
        for kind in ('posts', 'comments', 'both'):
            await click(f'#kindSeg [data-kind={kind}]', 800)
            names.append(await J("[document.getElementById('vTitle').textContent,document.getElementById('navPosts').textContent]"))
        check('the page is called “Posts & comments” in every mode', all(n == ['Posts & comments'] * 2 for n in names), names)
        check('sorted by most engagement by default', await J("document.getElementById('pf_sort').value") == 'eng')
        check('no language filter', not await J("!!document.getElementById('pf_lang')"))
        who = await J("[...document.getElementById('pf_type').options].map(o=>o.textContent)")
        check('“Posted by” has no V7 official option', 'V7 official' not in who and 'People' in who, who)
        await J("const s=document.getElementById('pf_sort');s.value='new';s.dispatchEvent(new Event('change'))"); await pg.wait_for_timeout(600)
        await click('[data-act=pfreset][data-k=pf]', 800)
        check('Clear these filters goes back to most engagement', await J("document.getElementById('pf_sort').value") == 'eng')
        # Version 36: the grid
        await click('#kindSeg [data-kind=posts]', 1500)
        g = await J("""(()=>{const g=document.querySelector('#content .pgrid');if(!g)return null;const c=[...g.children];
          const r=c.map(x=>x.getBoundingClientRect());let o=0;for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],b=r[j];if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)o++;}
          return {n:c.length,cards:g.querySelectorAll(':scope > .gc').length,media:g.querySelectorAll('.gc-media img').length,mz:g.classList.contains('mz'),cols:new Set(r.map(x=>Math.round(x.left))).size,overlap:o};})()""")
        check('posts show as grid cards, several across, none overlapping', g and g['n'] == 25 and g['cards'] == 25 and g['mz'] and g['cols'] >= 3 and g['overlap'] == 0, g)
        check('most cards show their picture', g and g['media'] >= 15, g)
        await click('#content .pgrid .gc [data-act=postview]', 700)
        check('a card opens the post view', await J("!!document.querySelector('#drBody .pv-t')"))
        await click('#drClose', 300)
        # Outside Egypt keeps its language filter and its sort
        await click('.side .nav[data-view=abroad]', 1200)
        await J("(()=>{const b=document.querySelector('[data-act=xtab][data-v=posts]');if(b)b.click();})()"); await pg.wait_for_timeout(900)
        x = await J("[!!document.getElementById('pfx_lang'),(document.getElementById('pfx_sort')||{}).value]")
        check('Outside Egypt keeps its language filter and most views', x == [True, 'reach'], x)
        # phone: one column, no sideways scroll
        ph = await b.new_page(viewport={'width': 390, 'height': 844}); ph.on('pageerror', lambda e: errs.append(str(e)))
        await ph.goto(SRC); await ph.wait_for_timeout(1500)
        await ph.evaluate("document.querySelector('.side .nav[data-view=posts]').click()"); await ph.wait_for_timeout(1500)
        m = await ph.evaluate("[new Set([...document.querySelectorAll('#content .pgrid > *')].map(x=>Math.round(x.getBoundingClientRect().left))).size,document.documentElement.scrollWidth<=innerWidth]")
        check('on a phone: one column, no sideways scroll', m == [1, True], m)
        check('no page errors', not errs, errs[:3])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
