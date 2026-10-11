"""Version 18: Rumors & attacks filled from real posts (pulled and read on 11 Oct 2026).
Claims, statuses and risk come from the posts' real dates; private people aren't named; the other tabs agree."""
import asyncio, json, re
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
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        async def click(sel,w=500): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        # the data itself
        import urllib.parse; html=open(urllib.parse.unquote(urllib.parse.urlparse(SRC).path),encoding='utf-8').read()   # the data block the build script writes
        d=json.loads(re.search(r'/\*RUMOR_DATA\*/var RUMOR_DATA=(.*?);/\*END_RUMOR_DATA\*/',html,re.S).group(1))
        check('real data: 368 posts found, 177 about V7', d['found']==368 and d['about']==177, (d['found'],d['about']))
        urls=[x['url'] for x in d['posts']]
        check('every post links to the real post, not a search', all(re.match(r'https://(x\.com|www\.facebook\.com|www\.instagram\.com|www\.tiktok\.com)/',u) and 'search' not in u for u in urls), [u for u in urls if 'search' in u][:2])
        per={c:sum(1 for x in d['posts'] if x['claim']==c) for c in ('price','owner','alcohol')}
        check('claims: price 38 posts, owner 4, alcohol 1', per=={'price':38,'owner':4,'alcohol':1}, per)
        # other tabs agree with the real data
        brief=await J("[...document.querySelectorAll('.brief li')].map(l=>l.textContent).join(' ')")
        check('overview has no rumor line (nothing high risk)', 'Rumor radar' not in brief)
        check('sidebar shows no high-risk count', await J("document.getElementById('radarCount').hidden"))
        await click('.side .nav[data-view=alerts]')
        al=await J("[...document.querySelectorAll('.al .t1')].map(x=>x.textContent)")
        check('alerts: price confusion to watch, and no false rumors spreading', any(x.startswith('Price confusion: “V7 costs EGP 20 now”') for x in al) and 'No false rumors spreading' in al, al)
        await click('.side .nav[data-view=events]')
        ev=await J("[...document.querySelectorAll('.evc .ev-t')].map(x=>x.textContent)")
        check('the demo Coca-Cola rumor event is gone', not any('Coca-Cola' in x for x in ev), ev)
        # Rumors & attacks
        await click('.side .nav[data-view=radar]',800)
        top=await J("[document.getElementById('dataBadge').textContent,document.getElementById('filtersRow').hidden,document.getElementById('period').textContent]")
        check('marked as real data, date filters hidden, check date shown', top[0]=='Real data' and top[1] and 'checked 11 Oct 2026' in top[2], top)
        ban=await J("[document.querySelector('.sbanner').className,document.querySelector('.sbanner').textContent]")
        check('banner: no false rumor spreading, price is the live issue', 'warn' in ban[0] and 'No false rumor is spreading about V7 right now' in ban[1] and 'The live issue is price' in ban[1], ban[1][:120])
        k=await J("[...document.querySelectorAll('.kpi')].map(x=>x.querySelector('.k-l').textContent+'='+x.querySelector('.k-v').textContent)")
        check('five numbers, all from the real posts', k==['Live issues=1','Posts about V7 read=177','Repeating a claim=26','Asking what’s true=5','Correcting it=12'], k)
        cards=await J("[...document.querySelectorAll('.ccard')].map(c=>[c.querySelector('.ccard-title').textContent,c.querySelector('.cst').textContent,c.querySelector('.risk').textContent])")
        check('claims ordered: active price first, then the watched and contained ones', [c[:2] for c in cards]==[['“V7 costs EGP 20 now”','Active'],['“V7 Malt tastes like alcohol”','Watching'],['“V7 was sold to Coca-Cola”','Contained']], cards)
        det=await J("[document.querySelector('#cdetail h2').textContent,!!document.querySelector('#cchart svg'),[...document.querySelectorAll('#cchart text')].map(t=>t.textContent),document.querySelector('#cdetail .resp-note').textContent]")
        check('price detail: monthly chart with V7’s response marked', det[0]=='“V7 costs EGP 20 now”' and det[1] and 'V7 responded' in det[2] and any(re.match(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) 20\d\d',t) for t in det[2]) and '27 Jan 2026' in det[3], (det[2][-6:],det[3][:60]))
        pc=await J("[...document.querySelectorAll('#cdetail .pc')].map(c=>[c.querySelector('.au').textContent,c.querySelector('.real')?1:0,c.querySelector('.pc-f a').href,c.querySelector('.when').textContent])")
        check('6 newest posts shown, each a real post with its link and full date', len(pc)==6 and all(x[1]==1 and x[2].startswith('https://') and re.search(r'20\d\d$',x[3]) for x in pc), pc[:2])
        await click('[data-act=campmore][data-v=price]')
        n=await J("document.querySelectorAll('#cdetail .pc').length")
        await click('[data-act=campless][data-v=price]')
        check('Show all opens all 38, Show less goes back', n==38 and await J("document.querySelectorAll('#cdetail .pc').length")==6, n)
        txt=await J("document.getElementById('content').innerText")
        check('private people aren’t named (shown as “X user”)', 'X user' in txt and 'nora' not in txt and 'Habiba' not in txt)
        check('no em dashes or “AI” in the page copy', '—' not in txt and not re.search(r'\bAI\b',txt), [m.start() for m in re.finditer('—',txt)][:3])
        await click('[data-act=selcamp][data-v=owner]',700)
        ow=await J("[document.querySelector('#cdetail .cst').textContent,document.querySelector('#cdetail .resp-note').textContent,document.querySelector('#cdetail').textContent.includes('weren’t found'),[...document.querySelectorAll('#cchart text')].map(t=>t.textContent)]")
        check('ownership claim: contained, V7’s 2024 denial, missing posts explained, daily chart', ow[0]=='Contained' and '3 May 2024' in ow[1] and ow[2] and any(re.match(r'\d+ May$',t) for t in ow[3]), (ow[0],ow[1][:50],ow[3][-4:]))
        rows=await J("[...document.querySelectorAll('#factsheet tbody tr')].length")
        own=await J("document.querySelector('#factsheet tbody tr a').href")
        check('fact sheet: 7 facts, ownership sourced to the founder’s denial', rows==7 and 'cairo24_' in own, (rows,own))
        w=await J("[...document.querySelectorAll('.rw .rw-t b')].map(x=>x.textContent)")
        check('also worth a look: sugar claim, “Seven Cola” in the news, the UK video', w==['“Every V7 flavour is sugar-free”','News calls the brand “Seven Cola”','“5 reasons why you shouldn’t buy V7 drinks”'], w)
        srch=await J("[...document.querySelectorAll('#content table.t')].map(t=>t.querySelector('thead').textContent).filter(h=>h.includes('What was searched')).length")
        check('how the posts were found: one table, by platform', srch==1)
        await pg.close()
        # phone and dark
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1000)
            await q.evaluate("document.querySelector('.side .nav[data-view=radar]').click()"); await q.wait_for_timeout(700)
            r=await q.evaluate("[document.documentElement.scrollWidth,document.body.scrollWidth,(()=>{const t=document.querySelector('.rtop');return t?t.scrollWidth<=t.parentElement.clientWidth+1:true})()]")
            check(f'[390 {cs}] nothing scrolls sideways, most-viewed table fits', r[0]<=390 and r[1]<=390 and r[2], r)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
