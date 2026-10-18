"""Version 27: likes an Instagram account hid say "likes hidden" instead of "0 likes" (19 Oct 2026). Public posts whose like count no
source returned carry `lh`; post cards and the post view say "likes hidden" (Instagram) or "… not shown" (other platforms), and the
guide explains it."""
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
    lh = [u for u in d['ugc'] if u.get('lh')]
    check('Instagram posts whose likes are hidden are flagged', sum(1 for u in lh if u['pl'] == 'ig') >= 30, len(lh))
    check('a flagged post carries no like count', all(not u.get('likes') for u in lh))
    check('the guide explains “likes hidden”', 'Likes hidden</dt>' in html)
    top = max((u for u in lh if u['pl'] == 'ig'), key=lambda u: (u.get('views') or 0, u.get('comments') or 0))
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
        card = ''
        for _ in range(12):   # the most-viewed post with hidden likes, shown further down the list
            card = await J(f"(()=>{{const b=document.querySelector('[data-act=postview][data-v=\"{top['id']}\"]');if(!b)return '';const c=b.closest('article,.pc,.card,.post')||b.parentElement.parentElement;return c.innerText;}})()")
            if card: break
            more = await J("(()=>{const b=[...document.querySelectorAll('#content button')].find(x=>/^Show more|^Show all/.test(x.textContent));if(!b)return false;b.click();return true;})()")
            if not more: break
            await pg.wait_for_timeout(500)
        check('its post card says “likes hidden”, not “0 likes”', 'likes hidden' in card and not re.search(r'(?<![\d.,])0 likes', card), card[-160:])
        await J(f"document.querySelector('[data-act=postview][data-v=\"{top['id']}\"]')&&document.querySelector('[data-act=postview][data-v=\"{top['id']}\"]').click()"); await pg.wait_for_timeout(700)
        pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
        check('its post view says “likes hidden”', 'likes hidden' in pv and not re.search(r'(?<![\d.,])0 likes', pv), pv[:200])
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            await q.goto(SRC + '#posts'); await q.wait_for_timeout(1200)
            sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
            check(f'[{w} {cs}] posts fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
