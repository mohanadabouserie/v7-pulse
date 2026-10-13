import asyncio, json, re
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
VIEWS=['overview','posts','products','voice','people','hashtags','owned','alerts','events','stores','restaurants','trends','radar','abroad']
GRAB="""()=>{
  const t=document.getElementById('content').innerText;
  const tips=[...document.querySelectorAll('#content [data-tip]')].map(e=>'TIP: '+e.getAttribute('data-tip'));
  const titles=[...document.querySelectorAll('#content [title]')].map(e=>e.getAttribute('title')).filter(x=>x&&x.length>25).slice(0,40).map(x=>'TITLE: '+x);
  return [document.getElementById('vTitle').textContent+' | '+document.getElementById('period').textContent, t, ...tips, ...titles].join('\\n');}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(SRC); await pg.wait_for_timeout(900); J=pg.evaluate; out=[]
        async def grab(label): out.append('\n########## '+label+'\n'+await J(GRAB))
        side=await J("document.querySelector('.side').innerText"); out.append('########## SIDEBAR\n'+side)
        filt=await J("[...document.querySelectorAll('#filtersRow button, #filtersRow [title]')].map(e=>(e.textContent||'')+' '+(e.getAttribute('title')||'')).join(' | ')"); out.append('########## FILTERS\n'+filt)
        for v in VIEWS:
            await J(f"document.querySelector('.side .nav[data-view=\"{v}\"]').click()"); await pg.wait_for_timeout(250); await grab(v)
        await J("document.querySelector('.side .nav[data-view=stores]').click()")
        for t in ['stock','ratings','ranks']:
            await J(f"document.querySelector('[data-act=stab][data-v={t}]').click()"); await pg.wait_for_timeout(250); await grab('stores/'+t)
        await J("document.querySelector('[data-act=stab][data-v=prices]').click()")
        await J("document.querySelector('.side .nav[data-view=abroad]').click()")
        for t in ['countries','posts','people','voice','pages']:
            await J(f"document.querySelector('[data-act=xtab][data-v={t}]').click()"); await pg.wait_for_timeout(250); await grab('abroad/'+t)
        await J("document.querySelector('#kindSeg [data-kind=comments]').click()")
        for v in ['overview','owned']:
            await J(f"document.querySelector('.side .nav[data-view=\"{v}\"]').click()"); await pg.wait_for_timeout(250); await grab(v+' (comments)')
        await J("document.querySelector('#kindSeg [data-kind=posts]').click()")
        await J("document.getElementById('helpBtn').click()"); await pg.wait_for_timeout(250)
        out.append('\n########## HELP\n'+await J("document.getElementById('drBody').innerText"))
        await J("document.getElementById('drClose').click()")
        await J("document.querySelector('.side .nav[data-view=overview]').click()"); await pg.wait_for_timeout(200)
        await J("document.getElementById('askBtn').click()"); await pg.wait_for_timeout(300)
        out.append('\n########## CHAT HEAD\n'+await J("document.querySelector('#chat .dr-h').innerText+'\\n'+document.getElementById('chatLog').innerText+'\\n'+document.getElementById('sugg').innerText+'\\nPLACEHOLDER: '+document.getElementById('askInput').placeholder"))
        ks=await J("[...document.querySelectorAll('#sugg button')].map(b=>b.dataset.k)")
        for k in ks:
            await J(f"document.querySelector('#sugg button[data-k=\"{k}\"]').click()"); await pg.wait_for_timeout(350)
            out.append('\n########## ANSWER '+k+'\n'+await J("document.querySelector('#chatLog .msg.bot:last-child').innerText"))
        open('copy/all_text.txt','w').write('\n'.join(out))
        await b.close()
asyncio.run(main())
