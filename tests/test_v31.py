"""Version 31 (19 Oct 2026): Facebook reels and more searches together, to cover more. The reel and video searches were compared on the same
keywords (fbreel_report.py): Google's short videos limited to Facebook and alien_force's reels-only search find reels Facebook's own searches
miss. Two more post searches (scrapeforge, fetch_cat) join the three of Version 30. Pictures that turned out to be login pages don't count
as read."""
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
    check('Facebook public posts about V7: 550+ (520 in Version 30)', len(fb) >= 550, len(fb))
    reels = [u for u in fb if u.get('fmt') == 'Reel']
    check('Facebook reels about V7: 180+ (152 in Version 30)', len(reels) >= 180, len(reels))
    vids = [u for u in fb if u.get('fmt') in ('Reel', 'Video')]
    check('85% of Facebook videos have their plays', sum(1 for u in vids if u.get('views')) >= 0.85 * len(vids), (sum(1 for u in vids if u.get('views')), len(vids)))
    check('Facebook videos read with their speech: 180+', sum(1 for u in fb if u.get('sp')) >= 180, sum(1 for u in fb if u.get('sp')))
    check('every public post has an account', all(u.get('a') for u in d['ugc']))
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        for w, cs in ((1440, 'light'), (390, 'dark')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('overview', 'posts', 'abroad'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
