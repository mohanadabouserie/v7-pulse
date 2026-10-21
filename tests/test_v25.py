"""Version 25: real data everywhere but Market (collected 17 Oct 2026). V7's posts and every comment on them, the pages abroad, and the public
posts about V7 from six platforms, 20 Apr to 16 Oct, each read and labelled by Claude. No demo generators, no estimated reach, views on the day
the post went up, profile visits and follower details gone, private people anonymous."""
import asyncio, json, os, pathlib, re, urllib.parse
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails = 0
def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))
VIEWS = ['overview', 'posts', 'products', 'voice', 'people', 'hashtags', 'owned', 'brief', 'alerts', 'radar', 'events', 'abroad', 'stores', 'restaurants', 'trends']
MARKET = ('stores', 'restaurants', 'trends')
OFFICIAL = {'v7egypt', 'v7.egypt', 'vsupersoda', 'v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco'}
async def main():
    html = open(urllib.parse.unquote(urllib.parse.urlparse(SRC).path), encoding='utf-8').read()
    d = json.loads(re.search(r'/\*REAL_DATA\*/var REAL_DATA=(.*?);/\*END_REAL_DATA\*/', html, re.S).group(1))
    check('the real data block: checked 17 Oct, 20 Apr to 16 Oct', d['meta']['checked'] == '2026-10-17' and d['meta']['window'] == ['2026-04-20', '2026-10-16'], d['meta'].get('window'))
    check('thousands of real comments and hundreds of public posts', len(d['cm']) > 2500 and len(d['ugc']) > 100, (len(d['cm']), len(d['ugc'])))
    check('V7’s replies are in (V7 Egypt and V Super Soda)', sum(1 for c in d['cm'] if c.get('by') == 'v7') > 300 and any(c.get('by') == 'vss' for c in d['cm']))
    anon = [a for a in d['au'] if a.get('anon')]
    check('private people: no name, handle or link', all(a['name'].endswith(' user') and not a.get('handle') and not a.get('url') for a in anon), len(anon))
    named = [a for a in d['au'] if not a.get('anon')]
    check('named accounts are pages, creators, news, businesses posting, or 10K+ followers', all(a.get('type') in ('creator', 'page', 'news', 'business') or (a.get('followers') or 0) >= 1000 for a in named), [a['name'] for a in named if a['type'] == 'person' and (a.get('followers') or 0) < 1000][:3])
    texts = [c.get('text', '') for c in d['cm'] if 'by' not in c] + [u.get('text', '') for u in d['ugc'] if u.get('seg') not in ('creator', 'page', 'news', 'business')]   # empty fields are left out of the data
    leaks = [m for t in texts for m in re.findall(r'@([\w.]+)', t) if m.lower() not in OFFICIAL]
    check('@mentions of private people are masked', not leaks, leaks[:5])
    check('no demo generator left (templates, made-up people, profile visits)', not any(x in html for x in ('var TPLC=', 'var V7_REPLY=', 'function makePost(', 'function makeIntlPost(', 'var VISITS=', 'var FOLLOWERS_IN=', 'var CREATORS=[')))
    check('the made-up “Mention spike on TikTok” event is gone', "id:'ev10'" not in html)
    check('the dashboard runs to 16 Oct 2026', 'END=Date.UTC(2026,9,16)' in html)
    # The artifact publish guard (Claude Code) takes a page for a code-review page, and refuses it above 512 KB, when an `id=` is followed by
    # a value it can't read: more than 2048 characters with no space, as with a Facebook link ending in &id=… before its image data.
    guard = re.compile(r'''(?<!-)\bid[\t\n\f\r ]*=[\t\n\f\r ]*(?:"([^"]{0,2048})"|'([^']{0,2048})'|([^\t\n\f\r >"'][^\t\n\f\r >]{0,2048})(?=[\t\n\f\r >]|$)|([\s\S]))''', re.I)
    trips = [html[max(0, m.start() - 60):m.start() + 20] for m in guard.finditer(html) if m.group(4) not in (None, '>') or '&#' in (m.group(1) or m.group(2) or m.group(3) or '')]
    trips += re.findall(r'(?i)(?<!-)\bid\s*=\s*["\']?prr-(?:anchor|decisions|stamp)', html)
    check('the publish guard won’t take the page for a code-review page', not trips, trips[:2])
    media = json.loads(re.search(r'/\*MEDIA\*/var MEDIA=(.*?);/\*END_MEDIA\*/', html, re.S).group(1))
    # Since Version 32 no image key may carry an &id= link (and since 21 Oct the images are files, not data: URIs), so the escaping is checked
    # on the post links themselves: every image key is a post's link, and the links with &id= read back whole though none is written raw.
    own = ''.join(re.search(r'/\*%s\*/(.*?)/\*END_%s\*/' % (b, b), html, re.S).group(1) for b in ('REAL_OWN', 'REAL_OWN_X'))
    links = {json.loads('"%s"' % u) for u in re.findall(r"url:'([^']*)'", own)} | {u['url'] for u in d['ugc'] if u.get('url')}
    check('image keys read back as the real post links, and links with &id= are written escaped',
          all(k in links for k in media) and sum('&id=' in u for u in links) >= 5 and '&id=' not in html, (sum(k not in links for k in media), sum('&id=' in u for u in links)))
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e))); J = pg.evaluate
        await pg.goto(SRC); await pg.wait_for_timeout(2500)
        per = await J("document.getElementById('period').textContent")
        check('the period ends on 16 Oct 2026', '16 Oct 2026' in per, per)
        foot = await J("document.querySelector('.side-foot').textContent")
        check('the sidebar says all data is real', foot.startswith('All data is real.') and 'collected on 17–20 Oct' in foot, foot)
        bad = []
        for v in VIEWS:
            await J(f"document.querySelector('.side .nav[data-view={v}]').click()"); await pg.wait_for_timeout(500)
            badge = await J("document.getElementById('dataBadge').textContent")
            txt = await J("document.getElementById('content').innerText")
            if badge != 'Real data': bad.append((v, 'badge ' + badge))
            if v not in MARKET and re.search(r'\bdemo\b', txt, re.I): bad.append((v, 'says demo: ' + re.search(r'.{0,40}\bdemo\b.{0,40}', txt, re.I).group(0)))
            m = re.search(r'.{0,30}(Real post\b(?!s)|~\d[\d.,KM]* reach|by reach|Most reach|\d reach\b).{0,30}', txt)
            if v not in MARKET and m: bad.append((v, 'reach or Real post: ' + m.group(0)))
        check('every tab is real data, with no demo wording, no estimated reach and no “Real post” tags', not bad, bad[:4])
        await J("document.querySelector('.side .nav[data-view=overview]').click()"); await pg.wait_for_timeout(600)
        h2 = await J("[...document.querySelectorAll('#content h2')].map(h=>h.textContent)")
        check('Overview: top posts sorted by views', any(x.startswith('Top ') and 'by views' in x for x in h2), h2)
        await J("document.querySelector('.side .nav[data-view=owned]').click()"); await pg.wait_for_timeout(700)
        h2 = await J("[...document.querySelectorAll('#content h2')].map(h=>h.textContent)")
        check('Our content: no profile visits or follower details', not any(x.startswith('Profile visits') or x.startswith('Who follows us') or x.startswith('When our followers') for x in h2), h2)
        check('Our content: “When people comment”, from the real comments', any(x.startswith('When people comment') for x in h2), h2)
        tiles = await J("[...document.querySelectorAll('#content .tile')].map(t=>t.innerText.replace(/\\s+/g,' '))")
        ans = [t for t in tiles if t.lower().startswith('answered')]
        check('Our content: the “Answered” share comes from V7’s real replies', ans and re.search(r'\d+ of \d+', ans[0]), ans)
        hint = await J("[...document.querySelectorAll('.panel')].find(p=>p.querySelector('h2')&&p.querySelector('h2').textContent==='Our posts').querySelector('.hint').textContent")
        check('Our posts: every post real, counts as of 17 Oct', 'counts as of 17 Oct' in hint and 'demo' not in hint, hint)
        # a V7 post with comments opens with its real comments and V7's replies
        await J("document.querySelector('#rangeSeg [data-r=\"90\"]').click()"); await pg.wait_for_timeout(800)
        pv = ''
        for k in range(8):   # V7 answers on some posts and not others: open V7's posts with comments until one shows a reply
            if k == 0: await J("(()=>{const b=document.querySelector('[data-act=ownall]');if(b&&!/fewer/.test(b.textContent))b.click();})()"); await pg.wait_for_timeout(600)   # Version 38: Our posts is a grid
            ok = await J(f"(()=>{{const r=[...document.querySelectorAll('#content .gc')].filter(t=>!t.classList.contains('gcm')&&+(([...t.querySelectorAll('.gs')].find(x=>/ comments$/.test(x.title))||{{title:'0'}}).title.replace(/[^0-9]/g,''))>5)[{k}];if(!r)return false;r.querySelector('[data-act=postview]').click();return true;}})()")
            if not ok: break
            await pg.wait_for_timeout(600)
            await J("(()=>{const b=document.querySelector('#drBody [data-act=postall]');if(b)b.click();})()"); await pg.wait_for_timeout(600)
            pv = await J("document.getElementById('drBody')?document.getElementById('drBody').innerText:''")
            if 'replied after' in pv: break
            await J("document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        check('the post view shows the real comments, and V7’s replies under them', 'comments' in pv.lower() and 'replied after' in pv and 'demo data' not in pv.lower(), pv[:200])
        await J("document.getElementById('drClose')&&document.getElementById('drClose').click()"); await pg.wait_for_timeout(300)
        # Ask V7 Pulse knows the data is real
        rules = re.search(r"function aiRules\(\)\{(.*?)\n\}", html, re.S).group(1)
        check('Ask V7 Pulse: all real, today is 17 Oct', 'ALL REAL' in rules and 'Today is 17 Oct 2026' in rules and 'DEMO' not in rules)
        await pg.close()
        for w, cs in ((390, 'light'), (390, 'dark'), (768, 'light')):
            q = await b.new_page(viewport={'width': w, 'height': 900}, color_scheme=cs); q.on('pageerror', lambda e: errs.append(str(e)))
            for v in ('overview', 'owned', 'voice', 'abroad'):
                await q.goto(SRC + '#' + v); await q.wait_for_timeout(1200)
                sw = await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
                check(f'[{w} {cs}] {v} fits', sw <= w, sw)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL', fails)
asyncio.run(main())
