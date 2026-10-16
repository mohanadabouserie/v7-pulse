"""Version 24: V7 Pulse on Telegram (16 Oct 2026). The dashboard links to @v7_pulse_bot (daily brief, alerts, questions),
alert previews show the Telegram message, links like …/#brief open that tab, and no bot token is ever in the page."""
import asyncio, os, pathlib, re, urllib.parse
from playwright.async_api import async_playwright
SRC = os.environ.get('DASH_SRC', pathlib.Path(__file__).resolve().parent.parent.joinpath('V7_Pulse_Dashboard.html').as_uri())
fails=0
def check(name,ok,info=''):
    global fails
    if not ok: fails+=1
    print(('  ok ' if ok else 'FAIL ')+name+(' :: '+str(info) if info!='' else ''))
async def main():
    html=open(urllib.parse.unquote(urllib.parse.urlparse(SRC).path),encoding='utf-8').read()
    check('no Telegram bot token in the page', not re.search(r'\d{8,10}:AA[\w-]{30,}',html))
    check('no private join link in the page', not re.search(r'v7_pulse_bot\?start=',html))
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        pg=await b.new_page(viewport={'width':1440,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e))); J=pg.evaluate
        async def click(sel,w=500): await J(f"document.querySelector({sel!r}).click()"); await pg.wait_for_timeout(w)
        # links that open a tab
        await pg.goto(SRC+'#brief'); await pg.wait_for_timeout(1500)
        check('…/#brief opens the Daily brief', await J("document.getElementById('vTitle').textContent")=='Daily brief')
        tg=await J("[...document.querySelectorAll('#content a[href=\"https://t.me/v7_pulse_bot\"]')].map(a=>a.textContent)")
        per=await J("document.getElementById('period').textContent")
        check('the brief says it’s on Telegram and links to the bot', tg and 'Telegram' in per, (tg,per))
        await pg.goto(SRC+'#alerts'); await pg.wait_for_timeout(1500)
        check('…/#alerts opens Alerts', await J("document.getElementById('vTitle').textContent")=='Alerts')
        rules=await J("[...document.querySelectorAll('.panel')].find(p=>p.textContent.startsWith('Alert rules')).innerText")
        check('alert rules: Act now on Telegram and by email; @v7_pulse_bot', 'Act now: on Telegram and by email right away' in rules and '@v7_pulse_bot' in rules, rules[-260:])
        await click('[data-act=alertprev]',600)
        pv=await J("[document.getElementById('drBody').innerText,document.querySelector('#drBody .ph-n').innerText]")
        check('the preview shows the Telegram message', 'TELEGRAM' in pv[1] and 'V7 Pulse' in pv[1], pv[1][:120])
        await click('#drClose',300)
        await pg.goto(SRC); await pg.wait_for_timeout(1200)
        check('a plain link still opens the Overview', await J("document.getElementById('vTitle').textContent")=='Overview')
        await click('#askBtn',400)
        chat=await J("(document.querySelector('.chat-tg')||{}).innerText||''")
        check('Ask V7 Pulse points to the same answers on Telegram', '@v7_pulse_bot' in chat, chat)
        await pg.close()
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC+'#brief'); await q.wait_for_timeout(1200)
            w=await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)")
            check(f'[390 {cs}] the brief with its Telegram button fits', w<=390, w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
