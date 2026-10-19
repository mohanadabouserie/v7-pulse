"""Version 30 (19 Oct 2026): Facebook, the same work as Instagram. More public posts about V7 (30 keywords on three search backends,
Facebook's reel and video searches, public groups, Google month by month), reels and videos told apart from photos, their plays and
what's said in them, the pictures of photo posts read, the followers of the pages that posted, and the comments under the posts.
Private people stay anonymous."""
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
    fb = [u for u in d['ugc'] if u['pl'] == 'fb']
    check('Facebook public posts about V7: 400+ (124 before)', len(fb) >= 400, len(fb))
    vids = [u for u in fb if u.get('fmt') in ('Reel', 'Video')]
    check('reels and videos are told apart from photos', len(vids) >= 100 and not any('/reel/' in u['url'] and u.get('fmt') not in ('Reel', 'Video') for u in fb), len(vids))
    check('most Facebook videos have their plays', sum(1 for u in vids if u.get('views')) >= 0.7 * len(vids), (sum(1 for u in vids if u.get('views')), len(vids)))
    ids = {u['id'] for u in fb}
    fbc = [c for c in d['cm'] if c['pl'] == 'fb' and c['parent'] in ids]
    check('comments under public Facebook posts about V7', len(fbc) >= 1000, len(fbc))
    check('they never count as waiting for V7', not any(c.get('needsReply') for c in fbc))
    au = {a['id']: a for a in d['au']}
    check('their writers are anonymous unless public', all(au[c['a']].get('anon') or au[c['a']].get('type') in ('creator', 'page', 'news', 'business') or (au[c['a']].get('followers') or 0) >= 10000
                                                          for c in fbc if c.get('a')))
    sp, vs = [u for u in fb if u.get('sp')], [u for u in fb if u.get('vs')]
    check('Facebook videos read with their speech', len(sp) >= 60, len(sp))
    check('Facebook photos and silent videos read from their pictures', len(vs) >= 80, len(vs))
    named = [a for a in d['au'] if a['pl'] == 'fb' and not a.get('anon') and a.get('type') in ('page', 'creator', 'business', 'news')]
    check('Facebook pages that posted about V7 have follower counts', sum(1 for a in named if a.get('followers')) >= 100, (sum(1 for a in named if a.get('followers')), len(named)))
    check('the data sources say Facebook videos were read', 'For Instagram and Facebook reels and videos it also read' in html)
    check('the help says Facebook comments under public posts are collected', 'the comments on public Instagram and Facebook posts and YouTube videos about V7 are collected' in html)
    own = set(re.findall(r"url:'(https://[^']+)'", html[html.index('/*REAL_OWN*/'):html.index('/*END_REAL_OWN*/')]))   # a public post that V7 also posted shows as V7's
    eg = [u for u in sp if u.get('cty') in ('EG', 'XX') and u['url'] not in own]   # the Posts tab opens on Egypt
    top = max(eg, key=lambda u: (u.get('views') or 0, u.get('likes') or 0)) if eg else None
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e))); J = pg.evaluate
        await pg.goto(SRC); await pg.wait_for_timeout(2500)
        await J("document.getElementById('customBtn').click()"); await pg.wait_for_timeout(300)
        await pg.fill('#dFrom', '2026-04-20'); await pg.fill('#dTo', '2026-10-16')
        await J("document.getElementById('dateForm').requestSubmit()"); await pg.wait_for_timeout(900)
        await J("document.querySelector('.side .nav[data-view=posts]').click()"); await pg.wait_for_timeout(900)
        await J("[...document.querySelectorAll('button')].find(x=>x.textContent.trim()==='Facebook').click()"); await pg.wait_for_timeout(900)
        found = False
        for _ in range(40):
            found = await J(f"(()=>{{const b=document.querySelector('[data-act=postview][data-v=\"{top['id'] if top else ''}\"]');if(!b)return false;b.click();return true;}})()")
            if found: break
            more = await J("(()=>{const b=[...document.querySelectorAll('#content button')].find(x=>/^Show \\d+ more|^Show more|^Show all/.test(x.textContent));if(!b)return false;b.click();return true;})()")
            if not more: break
            await pg.wait_for_timeout(300)
        await pg.wait_for_timeout(700)
        pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
        check('a Facebook video read with its speech says so in the post view', found and 'also count what’s said' in pv, pv[:160])
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark'), (768, 'light')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('overview', 'posts', 'people', 'voice'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
