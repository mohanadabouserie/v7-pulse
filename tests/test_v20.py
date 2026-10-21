"""Version 20: the page-by-page review (13 Oct 2026). Demo volumes match what real searches return, posts and comments
show together, and things that can't be collected reliably are gone (emotions, word cloud, dialects, Facebook groups tab)."""
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
        async def nav(v): await click(f'.side .nav[data-view={v}]',600)
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        # posts and comments together by default, at real volumes
        k=await J("[document.querySelector('#kindSeg [aria-pressed=true]').dataset.kind,document.querySelector('.kpi .k-l').textContent,document.querySelector('.kpi .k-v').textContent]")
        check('opens on posts and comments together', k[0]=='both' and k[1]=='Posts and comments', k)
        where=await J("[...document.querySelectorAll('.panel')].find(p=>p.textContent.startsWith('Where and who')).innerText")
        m=re.search(r'Comments under V7’s posts\s*(\d+)%',where)
        check('the conversation is split: comments under V7’s posts, under other people’s posts, public posts', m and 0<int(m.group(1))<100 and 'Comments under other people’s posts' in where and 'Public posts about V7' in where, m and m.group(0))   # v26: 26% under V7’s posts in the last 30 days (Kareem Elsayed’s video drew ~600 comments); it was 55–75% before
        await click('#kindSeg [data-kind=posts]')
        n=int((await J("document.querySelector('.kpi .k-v').textContent")).replace(',',''))
        check('public posts at real volume: a few a day', 15<=n<=300, n)   # Version 25: real data everywhere; v29: the wider Instagram search, about 6 a day in the last 30 days
        await click('#kindSeg [data-kind=both]')
        txt=await J("document.getElementById('content').innerText")
        check('no emotion labels', 'emotion' not in txt.lower() and 'Anticipation' not in txt)
        check('only clear languages, no dialect guesses', not re.search(r'Gulf Arabic|Maghrebi|Iraqi Arabic|Levantine|Sudanese',txt))
        check('no "Mentioned together with"', 'Mentioned together with' not in txt)
        # navigation
        navs=await J("[...document.querySelectorAll('.side .nav')].map(n=>n.dataset.view)")
        check('Facebook groups tab removed; Hashtags renamed', 'groups' not in navs and await J("document.querySelector('.side .nav[data-view=hashtags]').textContent.trim()")=='Hashtags', navs)
        # products
        await nav('products')
        ptxt=await J("document.getElementById('content').innerText")
        check('no "Core" badges, only Seasonal', 'CORE' not in ptxt and 'Core range' not in ptxt and 'SEASONAL' in ptxt.upper())
        small=await J("[...document.querySelectorAll('table.t tbody tr')].filter(r=>{const c=r.children[1];return c&&/^\\d+$/.test(c.textContent.trim())&&+c.textContent.trim()<5}).map(r=>r.children[4]&&r.children[4].textContent.trim())")
        check('no sentiment score on fewer than 5 items', all(x=='—' for x in small), small)
        # customer voice: categories from real comments
        await nav('voice')
        await click('#rangeSeg [data-r="90"]',700)   # V7's real posts since late July (v21): the last 30 days alone may have no "can't reach V7" comment
        vtxt=await J("document.getElementById('content').innerText")
        await click('#rangeSeg [data-r="30"]',700)
        check('requests use the real asks (watermelon, sugar-free malt) and the “can’t reach V7” complaint', 'watermelon' in vtxt and 'malt too' in vtxt and 'Can’t reach V7' in vtxt)
        # hashtags
        await nav('hashtags')
        tags=await J("[...document.querySelectorAll('table.t tbody tr td:first-child')].map(t=>t.textContent.toLowerCase())")
        htxt=await J("document.getElementById('content').innerText")
        check('no generic platform tags, no word cloud', not any(t.startswith(('#fyp','#foryou','#viral','#explore')) for t in tags) and 'Words people use' not in htxt, tags[:6])
        # under 10 now and higher than before means the previous period was also under 10: no percentage then
        pct_small=await J("[...document.querySelectorAll('table.t tbody tr')].filter(r=>+r.children[1].textContent<10).map(r=>r.children[2].textContent).filter(t=>t.includes('%')&&t.includes('▲'))")
        absn=await J("[...document.querySelectorAll('table.t tbody tr td:nth-child(3)')].map(t=>t.textContent.trim()).filter(t=>/^[+−] ?[0-9]+$/.test(t)).length")
        check('small numbers show the change in number, not a percentage', not pct_small and absn>0, (pct_small,absn))
        # our content
        await nav('owned')
        otxt=await J("document.getElementById('content').innerText")
        check('no follower details or profile visits; the heatmap is when people comment', 'Who follows us' not in otxt and 'Profile visits' not in otxt and 'When people comment' in otxt)   # Version 25: real data everywhere
        await J("(()=>{const b=document.querySelector('[data-act=ownall]');if(b)b.click();})()"); await pg.wait_for_timeout(600)   # Version 38: Our posts is a grid
        check('V7’s real TikTok videos are in Our posts', await J("document.querySelectorAll('#content .gc .gc-av .pl.tt').length")>=1)   # Version 25: real data everywhere
        # alerts: thresholds for real volumes
        await nav('alerts')
        rules=await J("[...document.querySelectorAll('.rule')].map(r=>[r.querySelector('span').textContent,r.querySelector('.switch').getAttribute('aria-checked')])")
        al=await J("[...document.querySelectorAll('.al .t1')].map(x=>x.textContent)")
        check('“unanswered for a day” is on, “mention spike” is gone', ['Unanswered for a day','true'] in rules and not any('Mention spike' in r[0] for r in rules), rules)
        check('a launch gets its own alert', any(a.startswith('V Orange launch:') for a in al), al)   # v21; v26: “can’t find V7” fires on real comments now, and test_v26 checks it leaves launch questions out
        # outside Egypt
        await nav('abroad')
        sub=await J("[...document.querySelectorAll('.subtabs button')].map(b=>b.textContent)")
        check('abroad sub-tab is People (no groups)', 'People' in sub and 'People & groups' not in sub, sub)
        await pg.close()
        # phones and dark mode
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1000); w=[]
            for v in ('overview','voice','products','owned','abroad','hashtags'):
                await q.evaluate(f"document.querySelector('.side .nav[data-view={v}]').click()"); await q.wait_for_timeout(400)
                w.append(await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)"))
            check(f'[390 {cs}] no page scrolls sideways', max(w)<=390, w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
