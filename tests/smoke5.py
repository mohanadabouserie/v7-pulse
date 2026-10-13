import asyncio
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
VIEWS = ['overview','posts','products','voice','people','hashtags','owned','alerts','events','stores','trends','radar','abroad']
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        pg.on('pageerror', lambda e: errs.append(f'pageerror: {e}'))
        pg.on('console', lambda m: errs.append(f'console: {m.text}') if m.type == 'error' else None)
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        for kind in ['posts','comments','both']:
            await pg.click(f'#kindSeg [data-kind="{kind}"]'); await pg.wait_for_timeout(200)
            for v in VIEWS:
                n0=len(errs)
                await pg.click(f'.side .nav[data-view="{v}"]'); await pg.wait_for_timeout(150)
                if len(errs)>n0: print(kind, v, errs[n0:])
        print('total errors', len(errs))
        st = await pg.evaluate("""()=>({posts:document.querySelectorAll('.pc').length})""")
        print(st)
        await b.close()
asyncio.run(main())
