"""Checks for Version 13: Search trends total only, no noise figures; restaurant fixes."""
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
        for w in (1440,390):
            pg=await b.new_page(viewport={'width':w,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto(SRC); await pg.wait_for_timeout(900); J=pg.evaluate
            await J("document.querySelector('.side .nav[data-view=trends]').click()"); await pg.wait_for_timeout(400)
            t=await J("document.getElementById('content').innerText")
            check(f'[{w}] no noise figures on Search trends','oise' not in t and 'Midjourney' not in t, [l for l in t.split('\n') if 'oise' in l][:2])
            check(f'[{w}] no product search chart','Searches by product' not in t and 'V Cola share' not in t)
            rows=await J("[...document.querySelectorAll('#content table tbody tr td:first-child')].map(x=>x.textContent)")
            check(f'[{w}] terms table has only the company row',rows==['V7, the company'],rows)
            lines=await J("document.querySelectorAll('#gtchart path').length"); check(f'[{w}] weekly chart has one line',lines==1,lines)
            tip=await J("[...document.querySelectorAll('#content [data-tip]')].map(e=>e.getAttribute('data-tip')).filter(x=>x.includes('governorate')).join(' ')")
            check(f'[{w}] governorate tip explains share and North Coast','share' in tip and 'North Coast' in tip)
            check(f'[{w}] no sideways scroll',await J("document.documentElement.scrollWidth")<=w)
            await pg.close()
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        await pg.goto(SRC); await pg.wait_for_timeout(900)
        await J("document.querySelector('.side .nav[data-view=restaurants]').click()"); await pg.wait_for_timeout(500)
        await J("(()=>{const b=document.querySelector('[data-act=more][data-k=rv7]');if(b)b.click();})()"); await pg.wait_for_timeout(300)
        dahan=await J("[...document.querySelectorAll('[data-tbl=rv7] tbody tr')].filter(tr=>/Al Dahan/.test(tr.innerText)).map(tr=>tr.innerText.replace(/\\s+/g,' '))")
        check('Al Dahan lists V Cola Diet and is a grill restaurant',dahan and all('V Cola Diet' in r and 'Egyptian & grills' in r for r in dahan),dahan[:1])
        bars=await J("[...document.querySelectorAll('#content .bar-l, #content .bl')].map(e=>e.textContent)")
        t=await J("document.getElementById('content').innerText")
        check('no "flavour not named" in V7 products','flavour not named' not in t)
        await J("document.querySelector('#askBtn').click()"); await pg.wait_for_timeout(300)
        await J("(()=>{const b=document.querySelector('#sugg button[data-k=search]');if(b)b.click();})()"); await pg.wait_for_timeout(300)
        a=await J("(document.querySelector('#chatLog .msg.bot:last-child')||{}).textContent||''")
        check('built-in search answer has no noise or product lines','oise' not in a and 'flavour' not in a.lower(),a[:140])
        check('no page errors',not errs,errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
