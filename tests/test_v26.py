"""Version 26: the wider search for public posts (18 Oct 2026) and YouTube comments.
The 17 Oct search found one Instagram post about V7 in its last week and no TikTok post in its last month: Instagram had only
8 hashtags, and TikTok's date filter returned unrelated videos. Version 26 adds Arabic and English spellings, the Instagram posts
that tag V7, Instagram keyword search, Google searches of Instagram and TikTok, TikTok searched from Egypt, and the comments on
V7's YouTube videos (they aren't turned off, as Version 25 said) and on the public YouTube videos about V7."""
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
    ugc = d['ugc']; cm = d['cm']
    last7 = lambda pl: sum(1 for u in ugc if u['pl'] == pl and '2026-10-10' <= u['d'] <= '2026-10-16')
    last30 = lambda pl: sum(1 for u in ugc if u['pl'] == pl and u['d'] >= '2026-09-17')
    check('Instagram: public posts about V7 in the last 7 days (1 before the wider search)', last7('ig') >= 10, last7('ig'))
    check('TikTok: public posts about V7 in the last 30 days (none before)', last30('tt') >= 5, last30('tt'))
    check('public posts about V7: many more than the 219 of 17 Oct', len(ugc) > 400, len(ugc))
    ytc = [c for c in cm if c['pl'] == 'yt']
    check('YouTube comments are in, each marked as having a day but no time', len(ytc) > 300 and all(c.get('nt') == 1 for c in ytc), (len(ytc), sum(1 for c in ytc if c.get('nt') != 1)))
    ids = {u['id']: u for u in ugc}
    on_public = [c for c in ytc if c['parent'] in ids]
    check('comments under public YouTube videos about V7 (Kareem Elsayed’s first)', len(on_public) > 200, len(on_public))
    check('comments under other people’s videos are never counted as waiting for V7', not any(c.get('needsReply') for c in on_public))
    on_own = [c for c in ytc if c['parent'].startswith('o')]
    check('comments under V7 Egypt’s own YouTube videos', len(on_own) >= 30, len(on_own))
    check('the data notes no longer say comments are off on V7’s videos', 'yt_comments_off' not in d['meta']['notes'] and 'yt_comments' in d['meta']['notes'])
    check('no page says V7 turned YouTube comments off', 'comments turned off on YouTube' not in html and 'Comments are turned off on V7' not in html)
    anon = [a for a in d['au'] if a.get('anon')]
    check('private people stay anonymous (YouTube commenters included)', all(a['name'].endswith(' user') and not a.get('handle') and not a.get('url') for a in anon), len(anon))
    texts = [c.get('text', '') for c in cm if 'by' not in c] + [u.get('text', '') for u in ugc if u.get('seg') not in ('creator', 'page', 'news', 'business')]
    leaks = [m for t in texts for m in re.findall(r'@([\w.]+)', t) if m.lower() not in {'v7egypt', 'v7.egypt', 'vsupersoda', 'v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco'}]
    check('@mentions of private people are masked', not leaks, leaks[:5])
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e))); J = pg.evaluate
        await pg.goto(SRC); await pg.wait_for_timeout(2500)
        # “Can’t find V7” counts this week's where-to-buy and availability posts and comments in Egypt, but not the questions about a
        # product in its launch weeks (those have their own alert): recount them from the data
        GAP = ('c_avail', 'q_where', 'q_launch', 'x_where', 'x_wish')
        rows = [r for r in ugc + cm if 'by' not in r and not r.get('da') and r.get('cty') == 'EG' and r.get('c') in GAP and '2026-10-10' <= r['d'] <= '2026-10-16']
        launch = [r for r in rows if r.get('c') in ('q_where', 'q_launch') and (r.get('prods') or [''])[0] == 'orange']
        await J("document.querySelector('.side .nav[data-view=alerts]').click()"); await pg.wait_for_timeout(800)
        al = await J("[...document.querySelectorAll('.al .t1')].map(x=>x.textContent)")
        cf = [a for a in al if a.startswith('More people can’t find V7')]
        n = int(re.search(r'(\d+) this week', cf[0]).group(1)) if cf else 0
        check('“can’t find V7” leaves out the V Orange launch questions (they have their own alert)', cf and n == len(rows) - len(launch) and launch and any(a.startswith('V Orange launch:') for a in al), (n, len(rows), len(launch)))
        # Our content: "When people comment" counts only comments with a time (YouTube gives the day only)
        await J("document.querySelector('.side .nav[data-view=owned]').click()"); await pg.wait_for_timeout(800)
        hint = await J("(()=>{const h=[...document.querySelectorAll('#content h2')].find(x=>x.textContent.startsWith('When people comment'));return h?h.closest('.panel').querySelector('.hint').textContent:''})()")
        check('“When people comment” is built from comments with a time', bool(re.search(r'from [\d,]+ comments', hint)), hint)
        # V7's YouTube video with the most comments (2 Jun) opens with them; YouTube dates them only to the month
        await J("document.getElementById('customBtn').click()"); await pg.wait_for_timeout(300)
        await pg.fill('#dFrom', '2026-04-20'); await pg.fill('#dTo', '2026-10-16')
        await J("document.getElementById('dateForm').requestSubmit()"); await pg.wait_for_timeout(900)
        await J("document.querySelector('.side .nav[data-view=owned]').click()"); await pg.wait_for_timeout(900)
        await J("(()=>{const b=document.querySelector('[data-act=ownall]');if(b)b.click();})()")   # Version 38: Our posts is a grid with Show all
        await pg.wait_for_timeout(600)
        found, pv = False, ''
        for k in range(6):    # V7 posted the same video on Instagram and YouTube: open the rows with its caption until the YouTube one
            ok = await J(f"(()=>{{const r=[...document.querySelectorAll('#content .gc')].filter(t=>t.textContent.includes('رفعوا علم'))[{k}];if(!r)return false;r.querySelector('[data-act=postview]').click();return true;}})()")
            if not ok: break
            await pg.wait_for_timeout(700)
            pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
            if 'Open on YouTube' in pv:
                found = True; break
            await J("document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        check('V7’s YouTube video opens with its comments, dated “about … months before 18 Oct”', found and 'months before 18 Oct' in pv and 'aren’t collected' not in pv, (found, pv[:160]))
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark'), (768, 'light')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('overview', 'posts', 'owned', 'voice'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
