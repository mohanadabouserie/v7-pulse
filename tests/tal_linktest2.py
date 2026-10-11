import asyncio, random, re
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(900)
        await pg.evaluate("document.querySelector('.side .nav[data-view=restaurants]').click()"); await pg.wait_for_timeout(500)
        rows=await pg.evaluate("""[...document.querySelectorAll('#content table tbody tr')].filter(tr=>tr.querySelector('a[href*="talabat.com"]')).map(tr=>{const a=tr.querySelector('a[href*="talabat.com"]'),s=tr.querySelector('.sub');return {href:a.href,name:a.textContent.replace(' ↗',''),sub:s?s.textContent:'',tip:s?s.title:''};})""")
        print('rows with Talabat links:',len(rows),'| all new format:',all(re.match(r'https://www\.talabat\.com/egypt/restaurant/\d+/[^/?]+\?aid=\d+$',r['href']) for r in rows))
        for r in rows[:3]: print('  ',r['name'],'|',r['sub'],'|',r['tip'])
        el=await pg.query_selector("xpath=//h2[starts-with(normalize-space(.),'Restaurants that list V7')]/ancestor::section[1]"); await el.screenshot(path='shots9/rest_v7_table.png')
        # filter to Zamalek and confirm aid follows the filter
        await pg.select_option('#rArea','0'); await pg.wait_for_timeout(500)
        z=await pg.evaluate("[...document.querySelectorAll('#content a[href*=\"talabat.com/egypt/restaurant/\"]')].map(a=>a.href)")
        print('Zamalek filter: links',len(z),'all aid=8045:',all(h.endswith('aid=8045') for h in z))
        await pg.select_option('#rArea','all'); await pg.wait_for_timeout(300)
        # open a sample of links from the page
        random.seed(7); sample=random.sample(rows,6)
        ctx=await b.new_context(user_agent=UA,viewport={'width':1280,'height':900}); t=await ctx.new_page()
        for r in sample:
            try:
                resp=await t.goto(r['href'],wait_until='domcontentloaded',timeout=45000); await t.wait_for_timeout(4500)
                txt=' '.join((await t.evaluate("document.body.innerText")).split())
                bad='Page Not Found' in txt or 'Application error' in txt
                m=re.search(r'in ([^,]{3,60}), Egypt',txt)
                print('  ',resp.status if resp else None,'BROKEN' if bad else 'opens','|',r['name'],'| dashboard says:',r['sub'],'| Talabat page says: in',m.group(1) if m else '?')
            except Exception as e: print('  ERR',r['name'],str(e)[:80])
            await t.wait_for_timeout(1200)
        print('page errors',errs); await b.close()
asyncio.run(main())
