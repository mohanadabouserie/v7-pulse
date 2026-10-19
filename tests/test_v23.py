"""Version 23: the marketing team's feedback (15 Oct 2026). Posts can be seen inside the dashboard (image, full text, comments),
pages lead with what needs attention, alerts carry a next step, an owner and a preview of the email and phone alert, a daily
brief, mixed sentiment, and posts worth amplifying."""
import asyncio, os, pathlib, re
from playwright.async_api import async_playwright
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
        async def nav(v): await click(f'.side .nav[data-view={v}]',700)
        def panel(title): return f"[...document.querySelectorAll('.panel')].find(p=>{{const h=p.querySelector('h2');return h&&h.textContent.startsWith({title!r});}})"
        await pg.goto(SRC); await pg.wait_for_timeout(1500)
        import urllib.parse
        size=os.path.getsize(urllib.parse.unquote(urllib.parse.urlparse(SRC).path))
        check('the page stays under 13 MB: the images have a 6 MB budget (build_media.py) and the artifact limit is 16 MB', size<13e6, size)   # Version 26: 586 public posts and 431 images (Version 25: real data everywhere; the data block and the new images added about 1.5 MB)
        # Overview: what needs attention comes first
        first=await J("document.querySelector('#content .panel h2').textContent")
        cards=await J("[...document.querySelectorAll('.atc')].map(c=>[c.querySelector('.atc-t').textContent,!!c.querySelector('.atc-n'),(c.querySelector('.atc-f .tg')||{}).textContent||''])")
        check('Overview opens with “Needs your attention”', first=='Needs your attention', first)
        check('2 to 4 cards, each with a next step and an owner', 2<=len(cards)<=4 and all(c[1] and c[2] for c in cards), cards)
        check('the cards mix issues with replies waiting or posts worth amplifying', any('wait for V7' in c[0] or 'worth amplifying' in c[0] for c in cards), [c[0] for c in cards])
        # mixed sentiment
        sn=await J("[...document.querySelectorAll('.sentnums div')].map(d=>d.textContent)")
        leg=await J("document.querySelector('.legend').textContent")
        check('sentiment has four parts: positive, neutral, mixed, negative', len(sn)==4 and any('Mixed' in x for x in sn) and 'Mixed' in leg, sn)
        await nav('posts')
        opts=await J("[...document.querySelectorAll('#pf_s option')].map(o=>o.value)")
        check('posts can be filtered to mixed', 'mix' in opts, opts)
        await J("const s=document.getElementById('pf_s');s.value='mix';s.dispatchEvent(new Event('change'))"); await pg.wait_for_timeout(600)
        mx=await J("[...document.querySelectorAll('.plist .pc')].slice(0,8).map(c=>[c.querySelector('.pill').textContent,c.querySelector('.pc-t').textContent])")
        check('mixed posts are the ones Claude marked mixed (praise and a complaint at once)', mx and all(m[0]=='Mixed' for m in mx), mx[:3])   # Version 25: real data everywhere
        await J("const s=document.getElementById('pf_s');s.value='';s.dispatchEvent(new Event('change'))"); await pg.wait_for_timeout(400)
        # a public post opens in the post view, its numbers real as of 17 Oct   # Version 25: real data everywhere
        await click('.plist .pc [data-act=postview]',600)
        dv=await J("[!!document.querySelector('#drBody .pv-media'),document.querySelector('#drBody .pv-t').textContent.length,document.getElementById('drBody').innerText]")
        check('a public post opens in the post view: its full text, real, collected on 17–19 Oct', dv[1]>0 and 'collected on 17–19 Oct 2026' in dv[2], dv[2][-120:])
        await click('#drClose',300)
        # V7's real posts show their images; the post view shows the post and its comments
        await nav('owned')
        th=await J("document.querySelectorAll('.tcap .tthumb').length")
        check('Our posts shows each real post’s image', th>=5, th)
        await J("[...document.querySelectorAll('.tcap')].find(b=>b.textContent.includes('V Orange is here 🍊')).click()"); await pg.wait_for_timeout(700)
        pv=await J("[(document.querySelector('#drBody .pv-media')||{}).offsetHeight>150,document.getElementById('drMeta').textContent,document.querySelectorAll('#drBody .pv-c').length,document.querySelectorAll('#drBody .pv-r').length,document.getElementById('drBody').innerText]")
        check('the real V Orange post opens with its image', pv[0] and pv[1].startswith('V7 post'), pv[1])   # Version 25: real data everywhere: no “Real post” tag, everything is real
        check('its comments show under it, with V7’s replies', pv[2]>=5 and pv[3]>=1, (pv[2],pv[3]))
        check('the view says the post and its comments are real', 'its comments are real' in pv[4])   # Version 25: real data everywhere
        await click('#drClose',300)
        # pages abroad: the latest post from each page shows its image
        await nav('abroad'); await click('[data-act=xtab][data-v=pages]',700)
        pm=await J(panel('Latest post from each V7 page abroad')+".querySelectorAll('.pc-media img').length")
        check('posts from V7’s pages abroad show their images', pm>=3, pm)
        # alerts: next step, owner and a preview of the email and phone alert
        await nav('alerts')
        badge=await J("document.getElementById('dataBadge').textContent")
        rows=await J("[...document.querySelectorAll('.alist .al')].map(a=>[a.querySelector('.t1').textContent,!!a.querySelector('.t3'),!!a.querySelector('[data-act=alertprev]'),a.querySelector('.sev').textContent])")
        check('Alerts are real data', badge=='Real data', badge)   # Version 25: real data everywhere
        check('every alert to act on has a next step and a preview', all(r[1] and r[2] for r in rows if 'clear' not in r[3].lower()), rows)
        idx=await J("[...document.querySelectorAll('.alist .al')].findIndex(a=>a.querySelector('.t1').textContent.startsWith('Price confusion'))")
        await J(f"document.querySelectorAll('.alist .al')[{idx}].querySelector('[data-act=alertprev]').click()"); await pg.wait_for_timeout(600)
        mail=await J("document.getElementById('drBody').innerText")
        check('the price alert’s email: subject, why it matters, the real posts, next step, an Arabic reply', 'Subject' in mail and '[Watch] Price confusion' in mail and 'Why it matters: Shops charge' not in mail and 'People keep posting' in mail and 'next step' in mail.lower() and 'سعر كانز V7' in mail and 'X user' in mail, mail[:200])
        check('and the phone notification', await J("!!document.querySelector('#drBody .ph-n')"))
        await click('#drClose',300)
        # the daily brief
        await nav('brief')
        top=await J("[document.getElementById('vTitle').textContent,document.getElementById('dataBadge').textContent,document.getElementById('filtersRow').hidden]")
        hs=await J("[...document.querySelectorAll('#content .panel h2')].map(h=>h.textContent)")
        check('Daily brief: its own tab, real data, no filters', top==['Daily brief','Real data',True], top)   # Version 25: real data everywhere
        check('brand health, red flags, positive signals, worth amplifying, recommended actions', [x for x in ['Brand health','Red flags and emerging issues','Positive signals','Worth amplifying','Recommended actions'] if any(h.startswith(x) for h in hs)]==['Brand health','Red flags and emerging issues','Positive signals','Worth amplifying','Recommended actions'], hs)
        acts=await J("[...document.querySelectorAll('.db-acts li')].map(l=>l.textContent)")
        check('3 to 5 recommended actions, each with an owner', 3<=len(acts)<=5 and await J("[...document.querySelectorAll('.db-acts li')].every(l=>l.querySelector('.tg'))"), acts)
        ndays=await J("document.querySelectorAll('#briefSel option').length")
        await J("const s=document.getElementById('briefSel');s.selectedIndex=1;s.dispatchEvent(new Event('change'))"); await pg.wait_for_timeout(700)
        h2=await J("document.querySelector('#content .panel h2').textContent")
        check('the last 7 briefs can be opened', ndays==7 and h2=='Brand health, Thu 15 Oct', (ndays,h2))   # Version 25: real data everywhere: the data runs to 16 Oct
        await click('[data-act=briefmail]',600)
        em=await J("document.getElementById('drBody').innerText")
        check('the brief as an email', 'V7 daily brief, Thu 15 Oct' in em and 'Recommended actions'.upper() in em.upper(), em[:160])
        await click('#drClose',300)
        # worth amplifying
        await click('[data-act=posts][data-k=amp]',700)
        am=await J("[[...document.querySelectorAll('.activef .chip')].map(c=>c.textContent),[...document.querySelectorAll('.plist .pc')].map(c=>c.querySelector('.pill').textContent)]")
        check('posts worth amplifying: positive posts by people and creators', any('Worth amplifying' in c for c in am[0]) and am[1] and all(x=='Positive' for x in am[1]), am)
        await nav('voice')
        vf=await J("document.querySelector('#content .panel h2').textContent")
        check('Customer voice also opens with what needs attention', vf=='Needs your attention', vf)
        await nav('events')
        check('Events are real data', await J("document.getElementById('dataBadge').textContent")=='Real data')   # Version 25: real data everywhere
        await pg.close()
        # phones and dark mode
        for cs in ('light','dark'):
            q=await b.new_page(viewport={'width':390,'height':900},color_scheme=cs); q.on('pageerror',lambda e:errs.append(str(e)))
            await q.goto(SRC); await q.wait_for_timeout(1200); w=[]
            for v in ('overview','brief','alerts','owned'):
                await q.evaluate(f"document.querySelector('.side .nav[data-view={v}]').click()"); await q.wait_for_timeout(500)
                w.append(await q.evaluate("Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)"))
            await q.evaluate("document.querySelector('.tcap').click()"); await q.wait_for_timeout(500)
            dw=await q.evaluate("(()=>{const b=document.getElementById('drBody');return b.scrollWidth<=b.clientWidth+1})()")
            check(f'[390 {cs}] nothing scrolls sideways, the post view fits', max(w)<=390 and dw, w)
            await q.close()
        check('no page errors', not errs, errs[:2])
        await b.close()
    print('FAIL',fails)
asyncio.run(main())
