import asyncio
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
VIEWS = ['overview','posts','products','voice','people','hashtags','owned','alerts','events','stores','restaurants','trends','radar','abroad']
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs=[]; issues=[]
        for vw,vh,tag,scheme in [(1440,900,'d','light'),(820,1180,'t','light'),(390,844,'m','light'),(1440,900,'dk','dark'),(390,844,'mdk','dark')]:
            ctx = await b.new_context(viewport={'width':vw,'height':vh}, color_scheme=scheme)
            pg = await ctx.new_page()
            pg.on('pageerror', lambda e, tag=tag: errs.append(f'{tag}: {e}'))
            pg.on('console', lambda m, tag=tag: errs.append(f'{tag} console: {m.text}') if m.type=='error' else None)
            await pg.goto(SRC); await pg.wait_for_timeout(900)
            for kind in ['posts','comments','both']:
                await pg.evaluate(f"document.querySelector('#kindSeg [data-kind=\"{kind}\"]').click()"); await pg.wait_for_timeout(120)
                for v in VIEWS:
                    await pg.evaluate(f"document.querySelector('.side .nav[data-view=\"{v}\"]').click()"); await pg.wait_for_timeout(120)
                    hs = await pg.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth + 1')
                    if hs: issues.append(f'{tag} {kind} {v}: horizontal scroll')
                    if v=='abroad':
                        for xt in ['countries','posts','people','voice','pages']:
                            await pg.evaluate(f"document.querySelector('[data-act=xtab][data-v=\"{xt}\"]').click()"); await pg.wait_for_timeout(100)
                            hs = await pg.evaluate('document.documentElement.scrollWidth > document.documentElement.clientWidth + 1')
                            if hs: issues.append(f'{tag} {kind} abroad/{xt}: horizontal scroll')
                        await pg.evaluate("document.querySelector('[data-act=xtab][data-v=overview]').click()")
            if tag in ('dk','mdk'):
                await pg.evaluate("document.querySelector('#kindSeg [data-kind=posts]').click()")
                for v in ['events','owned','overview']:
                    await pg.evaluate(f"document.querySelector('.side .nav[data-view=\"{v}\"]').click()"); await pg.wait_for_timeout(250)
                    await pg.screenshot(path=f'shots5/{tag}-{v}.png', full_page=False)
            await ctx.close()
        print('ERRORS:', errs or 'none'); print('ISSUES:', issues or 'none')
        await b.close()
asyncio.run(main())
