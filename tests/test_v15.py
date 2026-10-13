"""Version 15: V7 brand redesign (green master brand, can colors per product, regrouped navigation, phone filters)."""
import asyncio, re
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails=0
def check(name,ok,info=''):
    global fails
    if not ok: fails+=1
    print(('  ok ' if ok else 'FAIL ')+name+(' :: '+str(info) if info!='' else ''))
def lum(rgb):
    r,g,b=[int(x)/255 for x in re.findall(r'\d+',rgb)[:3]]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True); return (x+0.05)/(y+0.05)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        async def click(sel): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(350)
        await pg.goto(SRC); await pg.wait_for_timeout(1500)
        css=lambda sel,prop: J(f"getComputedStyle(document.querySelector({sel!r})).{prop}")
        # brand
        check('primary button is V7 green #0A7F40', await css('#askBtn','backgroundColor')=='rgb(10, 127, 64)', await css('#askBtn','backgroundColor'))
        check('sidebar is deep V7 green', await css('.side','backgroundColor')=='rgb(8, 112, 58)', await css('.side','backgroundColor'))
        fam=await css('body','fontFamily')
        check('Nunito Sans with Arabic fallback, no monospace', fam.startswith('"Nunito Sans"') and 'IBM Plex Sans Arabic' in fam and 'Mono' not in await css('.k-l','fontFamily'), fam)
        check('page title is uppercase', await css('#vTitle','textTransform')=='uppercase')
        # contrast of the main text pairs (WCAG AA)
        pairs=[('.k-l','.kpi'),('.period','body'),('.side-sec','.side'),('.nav:not([aria-current])','.side'),('.nav[aria-current="page"]','.nav[aria-current="page"]')]
        for t,bg in pairs:
            fg=await css(t,'color'); bgc=await css(bg,'backgroundColor')
            if bgc in ('rgba(0, 0, 0, 0)','transparent'): bgc=await css('body','backgroundColor')
            assert bgc.startswith('rgb'), (bg,bgc)
            v=cr(fg,bgc); check(f'contrast {t} >= 4.5', v>=4.5, round(v,2))
        # navigation groups
        secs=await J("[...document.querySelectorAll('.side-sec')].map(x=>x.textContent)")
        check('navigation groups', secs==['Conversation','To act on','Market','International'], secs)
        act=await J("(()=>{const out=[];let on=false;for(const el of document.querySelector('.side').children){if(el.classList.contains('side-sec'))on=el.textContent==='To act on';else if(on&&el.dataset.view)out.push(el.dataset.view);}return out})()")
        check('To act on holds alerts, rumors and events', act==['alerts','radar','events'], act)
        # overview: brief first, rumor line marked
        first=await J("document.querySelector('#content .g .panel h2').textContent")
        check('What changed comes before the chart', first.startswith('What changed this period'), first)
        check('no rumor line in the brief: no real rumor is high risk', not await J("[...document.querySelectorAll('.brief li')].some(l=>l.textContent.includes('Rumor radar'))"))   # was a demo rumor until Version 18
        # quieter segmented controls: selected option is a white pill with green text
        check('selected filter is a white pill with green text', await css('#rangeSeg [aria-pressed=true]','backgroundColor')=='rgb(255, 255, 255)' and await css('#rangeSeg [aria-pressed=true]','color')=='rgb(10, 127, 64)')
        # product can colors
        await click('.side .nav[data-view=products]')
        pcs=await J("[...document.querySelectorAll('.pcard')].map(c=>c.style.getPropertyValue('--pc'))")
        check('every product card carries its can color', len(pcs)==13 and all(re.match(r'#[0-9a-f]{6}$',x) for x in pcs) and len(set(pcs))==13, pcs)
        check('product details title has its color dot', await J("!!document.querySelector('.dd-head h2 .pdot')"))
        await click('#prodBtn'); n=await J("document.querySelectorAll('#prodList .pdot').length"); await click('#prodBtn')
        check('product filter shows a dot per product', n==13, n)   # 13 with V Orange (launched 11 Oct 2026)
        await click('.side .nav[data-view=posts]')
        check('product chips on posts have dots', await J("document.querySelectorAll('.pc .chip.prod .pdot').length")>0)
        # quantities in navy, sentiment green and red
        await click('.side .nav[data-view=overview]')
        check('KPI sparklines are navy', await J("document.querySelector('.kpi svg path:last-of-type').getAttribute('stroke')")=='var(--bar)')
        check('sentiment bar: positive green, negative red', await J("getComputedStyle(document.querySelector('.stack100 span')).backgroundColor")=='rgb(26, 145, 80)')
        # sidebar fits a 900 px screen
        check('sidebar fits without scrolling at 900 px', await J("document.querySelector('.side').scrollHeight<=document.querySelector('.side').clientHeight+1"))
        await pg.close()
        # dark mode
        d=await b.new_page(viewport={'width':1440,'height':900},color_scheme='dark'); d.on('pageerror',lambda e:errs.append(str(e)))
        await d.goto(SRC); await d.wait_for_timeout(1200)
        check('dark mode: deep forest ground', await d.evaluate("getComputedStyle(document.body).backgroundColor")=='rgb(10, 21, 16)')
        fg=await d.evaluate("getComputedStyle(document.querySelector('.k-l')).color"); bg=await d.evaluate("getComputedStyle(document.querySelector('.kpi')).backgroundColor")
        check('dark mode: label contrast >= 4.5', cr(fg,bg)>=4.5, round(cr(fg,bg),2))
        await d.close()
        # phone: filters fold behind a button
        q=await b.new_page(viewport={'width':390,'height':844}); q.on('pageerror',lambda e:errs.append(str(e)))
        await q.goto(SRC); await q.wait_for_timeout(1200)
        check('[390] Filters button shown, filter row folded', await q.evaluate("getComputedStyle(document.getElementById('fToggle')).display!=='none' && getComputedStyle(document.getElementById('filtersRow')).display==='none'"))
        top=await q.evaluate("document.querySelector('.kpis').getBoundingClientRect().top")
        check('[390] KPI numbers start in the first screen', top<450, round(top))
        await q.click('#fToggle'); await q.wait_for_timeout(200)
        check('[390] Filters button opens the filters', await q.evaluate("getComputedStyle(document.getElementById('filtersRow')).display!=='none'") and await q.get_attribute('#fToggle','aria-expanded')=='true')
        await q.evaluate("document.querySelector('[data-r=\"7\"]').click()"); await q.wait_for_timeout(300)
        check('[390] dot on Filters when filters differ from defaults', await q.evaluate("document.getElementById('fToggle').classList.contains('on')"))
        await q.evaluate("document.querySelector('.side .nav[data-view=stores]').click()"); await q.wait_for_timeout(400)
        check('[390] no Filters button where the filters do not apply', await q.evaluate("document.getElementById('fToggle').hidden"))
        check('[390] no sideways scroll', await q.evaluate("document.documentElement.scrollWidth")<=390)
        await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
