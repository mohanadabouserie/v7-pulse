"""Version 29 (19 Oct 2026): the Instagram gaps, closed as far as public data allows. More public posts about V7 (Google month by month,
every post tagging @v7egypt since 20 Apr, more hashtags and keyword samples, Instagram's Reels search), the comments under those posts,
and Claude reading the pictures of photos and silent reels (the text on them and what they show). Private people stay anonymous."""
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
    ig = [u for u in d['ugc'] if u['pl'] == 'ig']
    check('Instagram public posts about V7: 400+ (283 before)', len(ig) >= 400, len(ig))
    ids = {u['id'] for u in d['ugc']}
    igc = [c for c in d['cm'] if c['pl'] == 'ig' and c['parent'] in ids]
    check('comments under public Instagram posts about V7', len(igc) >= 1000, len(igc))
    check('they never count as waiting for V7', not any(c.get('needsReply') for c in igc))
    au = {a['id']: a for a in d['au']}
    check('their writers are anonymous unless public', all(au[c['a']].get('anon') or au[c['a']].get('type') in ('creator', 'page', 'news', 'business') or (au[c['a']].get('followers') or 0) >= 10000
                                                          for c in igc if c.get('a')))
    check('no scraper placeholder shows as an account name', not any(re.search(r'access delayed|only the owner of the page', a['name'], re.I) for a in d['au']))
    check('posts first collected on 19 Oct say so', sum(1 for u in ig if u.get('asof') == 19) >= 150)
    check('the sidebar and the post view say collected on 17–19 Oct', 'collected on 17–19 Oct.' in html and html.count('collected on 17–19 Oct 2026') == 2)
    check('Ask V7 Pulse knows comments under public Instagram posts are collected', 'only the comments on public Instagram and Facebook posts and YouTube videos about V7 are collected' in html
          and 'Comments under other people’s posts aren’t collected' not in html)
    vs = [u for u in ig if u.get('vs')]
    check('photos and silent reels read from their pictures', len(vs) >= 100, len(vs))
    check('the data sources say pictures were read', 'the text written on them and what they show (19 Oct)' in html)
    check('the help says Instagram comments under public posts are collected', 'the comments on public Instagram and Facebook posts and YouTube videos about V7 are collected' in html)
    top = max(vs, key=lambda u: (u.get('views') or 0, u.get('likes') or 0))
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
        for _ in range(20):
            found = await J(f"(()=>{{const b=document.querySelector('[data-act=postview][data-v=\"{top['id']}\"]');if(!b)return false;b.click();return true;}})()")
            if found: break
            more = await J("(()=>{const b=[...document.querySelectorAll('#content button')].find(x=>/^Show more|^Show all/.test(x.textContent));if(!b)return false;b.click();return true;})()")
            if not more: break
            await pg.wait_for_timeout(500)
        await pg.wait_for_timeout(700)
        pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
        check('a post read from its pictures says so in the post view', found and re.search(r'also count what’s (said and written in the video|written or shown in its (video|pictures))', pv), pv[:160])
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark'), (768, 'light')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('overview', 'posts', 'voice'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
