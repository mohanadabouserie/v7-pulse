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
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(900); J=pg.evaluate
        async def click(sel): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(350)
        # Products default
        await click('.side .nav[data-view=products]')
        cards=await J("[...document.querySelectorAll('.pcard')].map(c=>[c.querySelector('.nm').textContent,+c.querySelector('.k-v').textContent.replace(/,/g,''),c.getAttribute('aria-pressed')])")
        top=max(cards,key=lambda c:c[1]); h2=await J("[...document.querySelector('.dd-head h2').childNodes].find(n=>n.nodeType===3&&n.textContent.trim()).textContent.trim()")
        pick=await J("document.querySelector('.dd-pick').textContent")
        check('products: default is the most-discussed product, not Cream Soda', h2==top[0] and h2!='Cream Soda', (h2,top[0]))
        check('products: selected card highlighted', [c[0] for c in cards if c[2]=='true']==[h2])
        check('products: panel says it is per product', 'click a product above' in pick, pick)
        await click('.pcard[data-v=lmint]'); h2b=await J("[...document.querySelector('.dd-head h2').childNodes].find(n=>n.nodeType===3&&n.textContent.trim()).textContent.trim()")
        check('products: clicking a card switches details', h2b=='Lemon Mint', h2b)
        # single product via filter
        await pg.click('#prodBtn'); await pg.click('#pc_pink'); await pg.wait_for_timeout(300)
        h2c=await J("[...document.querySelector('.dd-head h2').childNodes].find(n=>n.nodeType===3&&n.textContent.trim()).textContent.trim()"); pick2=await J("document.querySelector('.dd-pick').textContent")
        check('products: product filter wins over an old card click', h2c=='Pink Lemonade' and 'product filter' in pick2, (h2c,pick2))
        await J("document.getElementById('prodAll').click()"); await pg.wait_for_timeout(300)
        await J("document.getElementById('prodNew').click()"); await pg.wait_for_timeout(300)
        vc=await J("[...document.querySelectorAll('.pcard')].filter(c=>['cola','dcola','llime','orange'].includes(c.dataset.v)).map(c=>[c.querySelector('.nm').textContent,+c.querySelector('.k-v').textContent.replace(/,/g,'')])")
        h2d=await J("[...document.querySelector('.dd-head h2').childNodes].find(n=>n.nodeType===3&&n.textContent.trim()).textContent.trim()")
        check('products: V Cola line opens on its most-discussed product', h2d==max(vc,key=lambda c:c[1])[0], (h2d,vc))
        await J("document.getElementById('prodAll').click()"); await pg.wait_for_timeout(300)
        # tables
        await click('.side .nav[data-view=restaurants]')
        n0=await J("document.querySelector('[data-tbl=rv7] tbody').rows.length")
        await click('[data-act=more][data-k=rv7]'); n1=await J("document.querySelector('[data-tbl=rv7] tbody').rows.length")
        less=await J("!!document.querySelector('[data-act=less][data-k=rv7]')")
        check('table: Show all then Show less appears', n1>n0 and less, (n0,n1,less))
        await J("window.scrollTo(0,document.body.scrollHeight)"); await pg.wait_for_timeout(200)
        await click('[data-act=less][data-k=rv7]'); n2=await J("document.querySelector('[data-tbl=rv7] tbody').rows.length")
        top_=await J("document.querySelector('[data-tbl=rv7]').closest('.panel').getBoundingClientRect().top"); hdr=await J("document.querySelector('.top').offsetHeight")
        more_again=await J("!!document.querySelector('[data-act=more][data-k=rv7]')")
        check('table: Show less collapses and keeps the table in view', n2==n0 and more_again and hdr<=top_<900, (n2,round(top_),hdr))
        # posts pager
        await click('.side .nav[data-view=posts]')
        c0=await J("document.querySelectorAll('.plist > *').length")
        await click('[data-act=pfmore]'); c1=await J("document.querySelectorAll('.plist > *').length"); l1=await J("!!document.querySelector('[data-act=pfless]')")
        await click('[data-act=pfless]'); c2=await J("document.querySelectorAll('.plist > *').length"); l2=await J("!!document.querySelector('[data-act=pfless]')")
        check('posts: Show 25 more then Show less', c1==c0+25 and l1 and c2==c0 and not l2, (c0,c1,c2))
        # campaign posts
        await click('.side .nav[data-view=radar]')
        has=await J("!!document.querySelector('[data-act=campmore]')")
        if has:
            await click('[data-act=campmore]'); cl=await J("!!document.querySelector('[data-act=campless]')")
            await click('[data-act=campless]'); cm=await J("!!document.querySelector('[data-act=campmore]')")
            check('campaign: Show all then Show less', cl and cm)
        else: check('campaign: no expander needed for the selected campaign', True)
        # governorates
        await click('.side .nav[data-view=trends]')
        g0=await J("document.querySelector('[data-act=gtall]').textContent"); await click('[data-act=gtall]')
        g1=await J("document.querySelector('[data-act=gtall]').textContent"); await click('[data-act=gtall]'); g2=await J("document.querySelector('[data-act=gtall]').textContent")
        check('governorates: Show all / Show less', g0.startswith('Show all') and g1=='Show less' and g2==g0, (g0,g1,g2))
        check('no page errors', not errs, errs)
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
