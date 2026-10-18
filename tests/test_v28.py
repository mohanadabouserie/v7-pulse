"""Version 28 (19 Oct 2026): what's said in Instagram reels is read with the caption (speech to text), and Instagram accounts have their
follower counts (Apify's profile scraper). Reels labelled with their speech carry `sp` and say so in the post view; named Instagram
accounts carry follower counts; private people stay anonymous."""
import asyncio, json, os, pathlib, re, urllib.parse
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails = 0
def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))
async def main():
    html = open(urllib.parse.unquote(urllib.parse.urlparse(SRC).path), encoding='utf-8').read()
    d = json.loads(re.search(r'/\*REAL_DATA\*/var REAL_DATA=(.*?);/\*END_REAL_DATA\*/', html, re.S).group(1))
    sp = [u for u in d['ugc'] if u.get('sp')]
    check('Instagram reels read with their speech', len(sp) >= 80 and all(u['pl'] == 'ig' for u in sp), len(sp))
    au = {a['id']: a for a in d['au']}
    ig_named = [a for a in d['au'] if a['pl'] == 'ig' and not a.get('anon')]
    check('named Instagram accounts have follower counts', sum(1 for a in ig_named if a.get('followers')) >= 0.7 * len(ig_named), (sum(1 for a in ig_named if a.get('followers')), len(ig_named)))
    check('Instagram accounts with 100K+ followers are known', sum(1 for a in ig_named if (a.get('followers') or 0) >= 100000) >= 10)
    anon = [a for a in d['au'] if a.get('anon')]
    check('private people stay anonymous: no name, handle, link or follower count', all(a['name'].endswith(' user') and not a.get('handle') and not a.get('url') and not a.get('followers') for a in anon), len(anon))
    check('the data sources say reels were read with their speech', 'also read what’s said in the video' in html)
    check('Ask V7 Pulse knows it too', 'also what’s said in the video, from speech to text' in html)
    top = max(sp, key=lambda u: u.get('views') or 0)
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e))); J = pg.evaluate
        await pg.goto(SRC); await pg.wait_for_timeout(2500)
        await J("document.getElementById('customBtn').click()"); await pg.wait_for_timeout(300)
        await pg.fill('#dFrom', '2026-04-20'); await pg.fill('#dTo', '2026-10-16')
        await J("document.getElementById('dateForm').requestSubmit()"); await pg.wait_for_timeout(900)
        await J("document.querySelector('.side .nav[data-view=posts]').click()"); await pg.wait_for_timeout(900)
        await J("(()=>{const b=[...document.querySelectorAll('[data-act]')].find(x=>x.dataset.act==='pl'&&x.dataset.v==='ig');if(b)b.click();})()"); await pg.wait_for_timeout(700)
        await J("(()=>{const s=[...document.querySelectorAll('#content select')].find(x=>[...x.options].some(o=>o.textContent==='Most views'));if(s){s.value=[...s.options].find(o=>o.textContent==='Most views').value;s.dispatchEvent(new Event('change',{bubbles:true}));}})()")
        await pg.wait_for_timeout(800)
        found = False
        for _ in range(12):
            found = await J(f"(()=>{{const b=document.querySelector('[data-act=postview][data-v=\"{top['id']}\"]');if(!b)return false;b.click();return true;}})()")
            if found: break
            more = await J("(()=>{const b=[...document.querySelectorAll('#content button')].find(x=>/^Show more|^Show all/.test(x.textContent));if(!b)return false;b.click();return true;})()")
            if not more: break
            await pg.wait_for_timeout(500)
        await pg.wait_for_timeout(700)
        pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
        check('the most-viewed reel read with its speech says so in the post view', found and 'also count what’s said in the video' in pv, pv[:160])
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark'), (768, 'light')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('posts', 'people'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
