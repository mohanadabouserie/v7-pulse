"""Version 21: the deeper pass (13 Oct 2026). V7's own posts and its pages abroad are real (pulled 13 Oct), V Orange is in,
dates run to 12 Oct, and the launch reads as a launch: excitement and "when will it be sold?", not taste or "can't find V7"."""
import asyncio, os, pathlib, re
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails=0
def check(name,ok,info=''):
    global fails
    if not ok: fails+=1
    print(('  ok ' if ok else 'FAIL ')+name+(' :: '+str(info) if info!='' else ''))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        async def click(sel,w=500): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        async def nav(v): await click(f'.side .nav[data-view={v}]',700)
        def panel(title): return f"[...document.querySelectorAll('.panel')].find(p=>{{const h=p.querySelector('h2');return h&&h.textContent.startsWith({title!r});}})"
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        # dates
        per=await J("document.getElementById('period').textContent")
        check('the data runs to 12 Oct 2026', '13 Sep – 12 Oct 2026' in per, per)
        foot=await J("document.querySelector('.side-foot').textContent")
        check('sidebar: V7’s own posts are real, demo posts up to 12 Oct', 'V7’s own posts' in foot and 'Demo posts up to 12 Oct 2026' in foot, foot)
        # overview: "can't find it" is about distribution; launch questions are counted apart
        cf=await J(panel('Can’t find it')+".innerText")
        check('overview: launch questions aren’t counted as “can’t find it”', re.search(r'Not counted here: \d+ questions about when and where V Orange will be sold',cf) and 'هتنزل إمتى' not in cf and 'hatenzel' not in cf, cf[-200:])
        # products: V Orange is new, and nobody has tasted it yet
        await nav('products')
        card=await J("(()=>{const c=document.querySelector('.pcard[data-v=orange]');return c?c.innerText:''})()")
        check('V Orange has a card marked new', 'V Orange' in card and 'NEW' in card.upper(), card[:80])
        await click('.pcard[data-v=orange]')
        head=await J("document.querySelector('.dd-head').innerText")
        tiles=await J("[...document.querySelectorAll('#content .tile')].map(t=>t.querySelector('.k-l').textContent.trim()+'='+t.querySelector('.k-v').textContent.trim())")
        check('V Orange: launched 11 Oct, counted since launch', 'launched 11 Oct' in head and 'since launch' in head and 'on the market' not in head, head[:160])
        check('V Orange: nobody “tried it” yet; people are looking for it', 'Tried it=0' in tiles and any(t.startswith('Looking for it=') for t in tiles), tiles)
        # our content: real posts, real followers
        await nav('owned')
        badge=await J("document.getElementById('dataBadge').textContent")
        check('Our content is marked partly real', badge=='Partly real', badge)
        fol=await J("[...document.querySelectorAll('#content .tiles.seven a.tile')].map(t=>t.querySelector('.k-v').textContent+' '+t.querySelector('p').textContent)")
        check('followers are the 13 Oct counts (80K, 39K, 37K, 2.5K)', [f.split(' ')[0] for f in fol]==['80K','39K','37K','2.5K'] and all('real' in f for f in fol), fol)
        rows=await J(panel('Our posts')+".querySelectorAll('tbody tr').length")
        real=await J(panel('Our posts')+".querySelectorAll('tbody tr .real').length")
        hint=await J(panel('Our posts')+".querySelector('.hint').textContent")
        check('the last 30 days: 10 posts, all real', rows==10 and real==10 and 'all real' in hint, (rows,real,hint))
        small=await J(panel('Our posts')+".querySelectorAll('tbody tr').length&&[..."+panel('Our posts')+".querySelectorAll('tbody tr')].filter(r=>+r.children[6].textContent.replace(/[^0-9]/g,'')<5).map(r=>r.children[8].textContent.trim())")
        check('no positive-comment share on posts with fewer than 5 comments', small and all(x=='—' for x in small), small)
        await click('#rangeSeg [data-r="90"]',700)
        hint90=await J(panel('Our posts')+".querySelector('.hint').textContent")
        check('a 90-day view says how many posts are demo (before late July)', re.search(r'\d+ real, \d+ demo',hint90), hint90)
        await click('#rangeSeg [data-r="30"]',700)
        # outside Egypt: the pages are real
        await nav('abroad'); await click('[data-act=xtab][data-v=pages]',700)
        badge=await J("document.getElementById('dataBadge').textContent")
        tab=await J(panel('V7 pages outside Egypt')+".querySelectorAll('tbody tr').length&&[..."+panel('V7 pages outside Egypt')+".querySelectorAll('tbody tr')].map(r=>[...r.children].map(c=>c.innerText.trim()))")
        check('pages abroad: partly real, four real accounts', badge=='Partly real' and len(tab)==4 and all('Real account' in r[0] for r in tab), (badge,len(tab)))
        uk=[r for r in tab if 'V7_UK' in r[0]][0]; ind=[r for r in tab if 'V7 India' in r[0]][0]
        check('V7_UK: no posts in 30 days, last post 3 Sep (real)', uk[3]=='0' and uk[6]=='3 Sep', uk)
        check('V7 India posts so often that 12 posts don’t reach back 30 days: “12+”', ind[3]=='12+', ind)
        lp=await J(panel('Latest post from each V7 page abroad')+".querySelectorAll('.pc').length")
        lr=await J(panel('Latest post from each V7 page abroad')+".querySelectorAll('.pc .real').length")
        check('latest post from each page abroad: 4 real posts, one per page', lp==4 and lr==4, (lp,lr))
        await click('[data-act=xtab][data-v=countries]',700)
        iss=await J("(()=>{const t=[...document.querySelectorAll('#content table.t')][0];const hs=[...t.querySelectorAll('thead th')].map(h=>h.textContent.trim());const i=hs.findIndex(h=>h.startsWith('Main issue'));return [...t.querySelectorAll('tbody tr')].map(r=>r.children[i].textContent.trim());})()")
        check('countries: main issues use short names', iss and max(len(x) for x in iss)<=20, iss[:8])
        # events: the launch is suggested from the comment spike
        await nav('events')
        ev9=await J("document.getElementById('evc_ev9').innerText")
        check('V Orange launch suggested from the spike in posts and comments', 'V Orange launched' in ev9 and 'Suggested' in ev9 and 'posts and comments about V7 on 11 Oct' in ev9 and 'mention V Orange' in ev9, ev9[:240])
        on=await J("[...document.querySelectorAll('.evr .evr-t')].map(e=>e.textContent)")
        need=['Cream Soda summer edition launched','Circle K × V7 Mixology Menu','V7 × Cairokee night','On the Run × V7 Refreshment Menu']
        check('real launches and partnerships are on the charts', all(any(n in x for x in on) for n in need), on)
        check('the unsupported Pomegranate suggestion is gone', not any('Pomegranate post reshared' in x for x in on) and 'Pomegranate post reshared' not in await J("document.getElementById('content').innerText"))
        # alerts
        await nav('alerts')
        al=await J("[...document.querySelectorAll('.al')].map(a=>[a.querySelector('.t1').textContent,(a.querySelector('.when')||{}).textContent||''])")
        check('launch questions get their own alert, not “can’t find V7”', any(a[0].startswith('V Orange launch:') for a in al) and not any(a[0].startswith('More people can’t find V7') for a in al), [a[0] for a in al])
        late=[a for a in al if re.match(r'^(1[3-9]|2\d|3[01]) Oct$',a[1])]
        check('no alert is dated after 12 Oct (store alerts keep their 4–5 Oct dates)', not late and any(a[1]=='4 Oct' for a in al), [a[1] for a in al])
        await click('[data-act=alert][data-k=launch]',700)
        pf=await J("[document.getElementById('vTitle').textContent,document.getElementById('prodBtn').textContent]")
        check('the launch alert opens the V Orange posts', 'V Orange' in pf[1], pf)
        await J("document.getElementById('prodAll').click()"); await pg.wait_for_timeout(300)
        # online stores: checked before the launch
        await nav('stores')
        n=await J("document.querySelectorAll('.smx tbody tr').length")
        note=await J(panel('V7 price and stock in each store')+".innerText")
        check('stores were checked before V Orange: 12 rows and a note', n==12 and 'V Orange launched on 11 Oct, after this check.' in note, (n,note[-90:]))
        await pg.close()
        # phones and dark mode
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1000); w=[]
            for v in ('owned','products','abroad','events','alerts'):
                await q.evaluate(f"document.querySelector('.side .nav[data-view={v}]').click()"); await q.wait_for_timeout(400)
                if v=='abroad':
                    await q.evaluate("document.querySelector('[data-act=xtab][data-v=pages]').click()"); await q.wait_for_timeout(400)
                w.append(await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)"))
            check(f'[390 {cs}] no page scrolls sideways', max(w)<=390, w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
