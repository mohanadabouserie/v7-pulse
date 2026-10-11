import asyncio
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs=[]; res=[]
        pg = await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(900); J=pg.evaluate
        await J("document.querySelector('.side .nav[data-view=restaurants]').click()"); await pg.wait_for_timeout(300)
        t=await J("document.querySelector('.tiles .tile:nth-child(2) .k-v').textContent"); res.append(('rest V7 tile all',t))
        await pg.select_option('#rArea','0'); await pg.wait_for_timeout(300)
        res.append(('area Zamalek tiles', await J("[...document.querySelectorAll('.tiles .tile .k-v')].map(e=>e.textContent)")))
        await pg.select_option('#rCui','0'); await pg.wait_for_timeout(300)
        res.append(('Zamalek + burgers menus', await J("document.querySelector('.tiles .tile .k-v').textContent")))
        await pg.select_option('#rArea','all'); await pg.select_option('#rCui','all'); await pg.wait_for_timeout(300)
        await J("document.querySelector('[data-act=comp][data-v=\"0\"]').click()"); await pg.wait_for_timeout(300)
        txt=await J("document.getElementById('content').textContent")
        res.append(('exclude hides rivals', ('PepsiCo' not in txt, 'Coca-Cola Co.' not in txt)))
        await J("document.querySelector('.side .nav[data-view=stores]').click()"); await pg.wait_for_timeout(300)
        txt=await J("document.getElementById('content').textContent")
        res.append(('stores exclude: no rivals', ('PepsiCo' not in txt, 'Pepsi 8' not in txt)))
        await J("document.querySelector('[data-act=comp][data-v=\"1\"]').click()"); await pg.wait_for_timeout(300)
        txt=await J("document.getElementById('content').textContent")
        res.append(('stores include: rivals + no brand-count line', ('PepsiCo' in txt, '7UP 3 · Coca-Cola 3' not in txt, 'Pepsi 8 ·' not in txt)))
        await J("document.querySelector('[data-act=stab][data-v=ranks]').click()"); await pg.wait_for_timeout(300)
        await J("document.querySelector('[data-act=sort][data-k=amzc][data-v=p]').click()"); await pg.wait_for_timeout(200)
        res.append(('amazon sort by price ok', await J("document.querySelectorAll('table').length")))
        await J("document.getElementById('askBtn').click()"); await pg.wait_for_timeout(300)
        for k in ['compete','restaurants','actions']:
            await J(f"document.querySelector('#sugg button[data-k=\"{k}\"]').click()"); await pg.wait_for_timeout(450)
            res.append((k, (await J("document.querySelector('#chatLog .msg.bot:last-child').textContent"))[:150]))
        for r in res: print(r)
        print('ERRORS',errs)
        # phone + dark screenshots
        for scheme in ['light','dark']:
            ctx=await b.new_context(viewport={'width':390,'height':844},color_scheme=scheme); q=await ctx.new_page(); await q.goto(SRC); await q.wait_for_timeout(800)
            await q.evaluate("document.querySelector('.side .nav[data-view=restaurants]').click()"); await q.wait_for_timeout(300)
            await q.screenshot(path=f'shots5/m-rest-{scheme}.png', full_page=True, clip={'x':0,'y':0,'width':390,'height':2600})
            await q.evaluate("document.querySelector('.side .nav[data-view=stores]').click()"); await q.wait_for_timeout(300)
            await q.screenshot(path=f'shots5/m-stores-{scheme}.png', full_page=True, clip={'x':0,'y':0,'width':390,'height':2600})
            await ctx.close()
        await b.close()
asyncio.run(main())
