"""Version 34 (21 Oct 2026): a creator speaking Egyptian Arabic counts in the Egypt views wherever the video is filmed. Kareem Elsayed's
reel about V7 (1.46M views on Facebook, 903K on Instagram) says it was filmed in England, so since the reels' speech was read it had
been filed under Outside Egypt, United Kingdom, and the user couldn't find it. Businesses abroad, Egyptians abroad and local people keep
their country (DECISIONS #168)."""
import asyncio, json, os, pathlib, re, urllib.parse
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
KAREEM = ('facebook.com/reel/2374066166742658', 'instagram.com/p/DeRGJd2gP0M', 'facebook.com/reel/925912510369940')
fails = 0
def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))
async def main():
    html = open(urllib.parse.unquote(urllib.parse.urlparse(SRC).path), encoding='utf-8').read()
    d = json.loads(re.search(r'/\*REAL_DATA\*/var REAL_DATA=(.*?);/\*END_REAL_DATA\*/', html, re.S).group(1))
    au = {a['id']: a for a in d['au']}
    k = [u for u in d['ugc'] if any(x in (u.get('url') or '') for x in KAREEM)]
    check("Kareem Elsayed's three reels are in the Egypt views", len(k) == 3 and all(u['cty'] == 'EG' for u in k), [(u.get('url'), u['cty']) for u in k])
    eg_creators = [u for u in d['ugc'] if u.get('lang') == 'ar' and u.get('seg') == 'creator']
    check('every creator posting in Egyptian Arabic is in Egypt', all(u['cty'] == 'EG' for u in eg_creators), [u['url'] for u in eg_creators if u['cty'] != 'EG'][:3])
    check('a business abroad writing in Egyptian Arabic keeps its country (the rule is for creators only)',
          any(u.get('lang') == 'ar' and u.get('seg') == 'business' and u['cty'] not in ('EG', 'XX') for u in d['ugc']))
    check('comments by Egyptians abroad keep their country (where they found V7, where they want it)',
          sum(1 for c in d['cm'] if c.get('lang') == 'ar' and c.get('cty') not in (None, 'EG', 'XX')) >= 20)
    under = {u['id'] for u in k}
    check('the comments under his reels that name no country of their own are in Egypt too',
          all(c.get('cty') in (None, 'EG') for c in d['cm'] if c.get('parent') in under and c.get('seg') != 'diaspora' and c.get('c', '')[:2] != 'x_'))
    check('his own reply is shown under his name', any(au.get(c.get('a'), {}).get('name', '').startswith('Kareem Elsayed') for c in d['cm'] if c.get('parent') in under))
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        for w, cs in ((1440, 'light'), (390, 'dark')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('people', 'posts', 'abroad'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1300)
                if v == 'people':   # Creators & pages, by followers: with 4.8M he leads it
                    await q.click('[data-act="seg"][data-v="infl"]'); await q.wait_for_timeout(700)
                txt = await q.evaluate("document.getElementById('content').innerText")
                if v == 'abroad':
                    check(f'[{w} {cs}] Outside Egypt no longer lists his reels', 'Kareem Elsayed' not in txt)
                else:
                    check(f'[{w} {cs}] {v} (Egypt{", Creators & pages" if v == "people" else ""}) shows Kareem Elsayed', 'Kareem Elsayed' in txt)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
