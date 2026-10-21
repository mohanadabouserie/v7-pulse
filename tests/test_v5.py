import asyncio, json
from playwright.async_api import async_playwright
import os, pathlib
# the dashboard next to this folder; DASH_SRC=file:///…/docs/index.html runs the same checks on the public copy
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
ok=[];bad=[]
def check(name,cond,info=''):
    (ok if cond else bad).append(name+(' :: '+str(info) if info else ''))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1440,'height':900})
        errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(SRC); await pg.wait_for_timeout(1000)
        J=pg.evaluate
        async def nav(v): await J(f"document.querySelector('.side .nav[data-view=\"{v}\"]').click()"); await pg.wait_for_timeout(150)
        async def click(sel): await J(f"document.querySelector({json.dumps(sel)}).click()"); await pg.wait_for_timeout(150)
        # --- filter visibility
        vis = "()=>({row:!document.getElementById('filtersRow').hidden,range:!document.getElementById('rangeWrap').hidden,src:!document.getElementById('srcSeg').hidden,kind:!document.getElementById('kindSeg').hidden,pl:!document.getElementById('platChips').hidden,prod:!document.getElementById('prodBtn').parentNode.hidden})"
        await nav('alerts'); v=await J(vis); check('alerts hides range/src/kind', v['row'] and not v['range'] and not v['src'] and not v['kind'] and v['pl'], v)
        await nav('radar'); v=await J(vis); check('radar uses real posts across all dates, so the filter row is hidden', not v['row'], v)
        await nav('owned'); v=await J(vis); check('owned hides src/kind', v['row'] and not v['src'] and not v['kind'] and v['pl'], v)
        await nav('events'); v=await J(vis); check('events hides filter row', not v['row'], v)
        await nav('overview'); v=await J(vis); check('overview shows all filters', all(v.values()), v)
        # --- overview KPIs: no Accounts posting
        labels = await J("[...document.querySelectorAll('.kpi .k-l')].map(e=>e.textContent)")
        check('overview has no Accounts posting', not any('Accounts' in l for l in labels), labels)
        check('overview has 5 KPIs', len(labels)==5, labels)
        # --- activity math
        m = await J("""()=>{const V=window.__v5;return null}""")
        # --- metric switch
        await click('[data-act=metric][data-v=views]')
        t = await J("document.querySelector('#tchart svg').getAttribute('aria-label')")
        check('views chart renders', 'Views per day' in t, t)
        await click('[data-act=metric][data-v=eng]')
        t = await J("document.querySelector('#tchart svg').getAttribute('aria-label')")
        check('engagement chart renders', 'Engagement per day' in t, t)
        # comments mode: no views option
        await click('#kindSeg [data-kind=comments]')
        opts = await J("[...document.querySelectorAll('[data-act=metric]')].map(b=>b.dataset.v)")
        check('comments mode has no views metric', 'views' not in opts, opts)
        h2 = await J("document.getElementById('tchart').closest('.panel').querySelector('h2').textContent")
        check('comments chart title', h2.startswith('Likes and replies per day') or h2.startswith('Comments per day'), h2)
        title = await J("document.getElementById('navPosts').textContent")
        check('the page keeps its name in every mode (Version 37)', title=='Posts & comments', title)
        await click('#kindSeg [data-kind=posts]')
        await click('[data-act=metric][data-v=posts]')
        # --- events approve flow
        badge = await J("document.getElementById('eventCount').textContent")
        check('pending badge shows 2', badge=='2', badge)
        await nav('events')
        await click('[data-act=evok][data-v=ev9]')
        badge = await J("document.getElementById('eventCount').textContent")
        check('approve decrements badge', badge=='1', badge)
        await nav('overview')
        evl = await J("document.getElementById('evlist').textContent")
        check('approved event on overview chart', 'V Orange launched' in evl, evl[:200])
        await nav('events')
        await click('[data-act=evno][data-v=ev7]')
        rej = await J("[...document.querySelectorAll('.evc .ev-t')].map(e=>e.textContent)")
        check('rejected event listed', any('12-month high' in r for r in rej), rej)
        await click('[data-act=evback][data-v=ev7]')
        badge = await J("document.getElementById('eventCount').textContent")
        check('move back to pending', badge=='1', badge)
        # edit ev7
        await click('[data-act=evedit][data-v=ev7]')
        await pg.fill('#evt_ev7','Searches for V7 hit a 12-month high'); await pg.fill('#evd_ev7','2026-08-10')
        await click('[data-act=evsave][data-v=ev7]')
        ttl = await J("document.querySelector('#evc_ev7 .ev-t').textContent")
        d = await J("document.querySelector('#evc_ev7 .ev-h').textContent")
        check('edit saves title and date', ttl=='Searches for V7 hit a 12-month high' and '10 Aug' in d, (ttl,d))
        # add event: empty title validation
        await click('#evForm button[type=submit]')
        msg = await J("document.getElementById('evFormMsg').textContent")
        check('form validates empty title', 'Write what happened' in msg, msg)
        await pg.fill('#evForm input[name=t]','Ramadan TV ad starts'); await pg.fill('#evForm input[name=d]','2026-09-20')
        await J("document.querySelector('#evForm select[name=p]').value='pom'")
        await click('#evForm button[type=submit]')
        lst = await J("[...document.querySelectorAll('.evr .evr-t')].map(e=>e.textContent)")
        check('added event listed', any('Ramadan TV ad starts' in x for x in lst), lst)
        await nav('overview')
        evl = await J("document.getElementById('evlist').textContent")
        check('added event on chart', 'Ramadan TV ad starts' in evl, evl[:300])
        # product filter on events: event with pom shows when product=pom, hidden for cream
        # --- day filter from events link
        await nav('events')
        await pg.wait_for_timeout(100)
        await click('[data-act=evno][data-v=ev9]'); await click('[data-act=evback][data-v=ev9]')
        await click('#kindSeg [data-kind=both]')   # public posts are few (1-2 a day); the day link opens posts and comments
        await click('[data-act=dayposts]')
        title = await J("document.getElementById('vTitle').textContent")
        chip = await J("[...document.querySelectorAll('.activef .chip')].map(c=>c.textContent)")
        dates = await J("[...document.querySelectorAll('.plist .pc .when')].map(e=>e.textContent.split(',')[0])")
        check('day filter opens posts for that day', title in ('All posts','Posts & comments') and any('On 11 Oct' in c for c in chip) and len(set(dates))==1, (title,chip,set(dates)))
        # --- explorer sorted by reach
        rs = await J("[...document.querySelectorAll('.plist .pc')].length")
        sortv = await J("document.getElementById('pf_sort').value")
        check('explorer default sort is most engagement (Version 37)', sortv=='eng', sortv)
        await click('[data-act=pfreset][data-k=pf]')
        # --- BGC + comments = V7 replies
        await click('#srcSeg [data-src=owned]'); await click('#kindSeg [data-kind=comments]'); await nav('posts')
        tags = await J("[...document.querySelectorAll('.plist .pc')].slice(0,5).map(c=>c.querySelector('.tg')?c.querySelector('.tg').textContent:'')")
        check('BGC comments are V7 replies', all(t=='V7 reply' for t in tags) and len(tags)>0, tags)
        await click('#srcSeg [data-src=earned]'); await click('#kindSeg [data-kind=posts]')
        # --- owned: comments on our posts -> explorer
        await nav('owned')
        await click('[data-act=cmposts][data-k=reply]')
        chip = await J("[...document.querySelectorAll('.activef .chip')].map(c=>c.textContent)")
        kind = await J("document.querySelector('#kindSeg [aria-pressed=true]').dataset.kind")
        check('owned -> waiting comments in explorer', kind=='comments' and any('On V7’s posts' in c for c in chip) and any('No reply' in c for c in chip), (kind,chip))
        await click('#kindSeg [data-kind=posts]')
        # --- hashtags comments note
        await click('#kindSeg [data-kind=comments]'); await nav('hashtags')
        txt = await J("document.getElementById('content').textContent")
        check('hashtags comments note', 'Comments almost never use hashtags' in txt)
        await click('[data-act=kind][data-v=posts]')
        k = await J("document.querySelector('#kindSeg [aria-pressed=true]').dataset.kind")
        check('switch to posts button', k=='posts', k)
        # --- assistant
        await J("document.getElementById('askBtn').click()"); await pg.wait_for_timeout(200)
        n0 = await J("document.querySelectorAll('#chatLog .msg').length")
        sug = await J("[...document.querySelectorAll('[data-ask], .sugg button, #chat button')].map(b=>b.textContent).filter(t=>/visited|events/i.test(t))")
        check('assistant has new suggestions', len(sug)>=2, sug)
        print('ERRORS', errs)
        await b.close()
asyncio.run(main())
print('PASS',len(ok)); [print('  ok',x) for x in ok]
print('FAIL',len(bad)); [print('  !!',x) for x in bad]
