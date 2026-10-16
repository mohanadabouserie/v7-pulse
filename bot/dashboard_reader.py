"""Reads V7 Pulse the way a person does: it opens the dashboard in a headless browser and takes the daily brief, the
alerts and Ask V7 Pulse's answers from the page. The Telegram bot and the website therefore always say the same thing,
from the same data and the same logic.

DASH_URL (env) picks the dashboard: the website's copy in docs/ by default. On a server it can be the live address.
"""
import os, pathlib, re, threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DASH_URL = os.environ.get('DASH_URL', (ROOT / 'docs' / 'index.html').as_uri())
SITE = 'https://mohanadabouserie.github.io/v7-pulse/'

_lock = threading.Lock()
_pw = _browser = None


def _page():
    global _pw, _browser
    if _browser is None or not _browser.is_connected():   # first use, or the browser crashed: start a new one
        close()
        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch()
    pg = _browser.new_page(viewport={'width': 1280, 'height': 900})
    try:
        pg.goto(DASH_URL)
        pg.wait_for_function("document.querySelector('#content .panel')!==null", timeout=30000)
    except Exception:
        pg.close(); raise
    return pg


def _nav(pg, view):
    pg.evaluate(f"document.querySelector('.side .nav[data-view={view}]').click()")
    pg.wait_for_timeout(500)


def brief(day_index=0):
    """The daily brief as the email shows it. day_index 0 is the latest day, 1 the day before, up to 6."""
    with _lock:
        pg = _page()
        try:
            _nav(pg, 'brief')
            if day_index:
                pg.evaluate(f"const s=document.getElementById('briefSel');s.selectedIndex={int(day_index)};s.dispatchEvent(new Event('change'))")
                pg.wait_for_timeout(500)
            pg.evaluate("document.querySelector('[data-act=briefmail]').click()")
            pg.wait_for_timeout(500)
            return pg.evaluate("""(()=>{
              const head=[...document.querySelectorAll('#drBody .mail-h div')].find(d=>d.textContent.startsWith('Subject'));
              const out={subject:head?head.querySelector('b').textContent:'',sections:[]};let cur=null;
              for(const el of document.querySelector('#drBody .mail-b').children){
                if(el.classList.contains('mail-k')){cur={title:el.textContent.trim(),items:[]};out.sections.push(cur);continue;}
                if(!cur||el.querySelector('.btn'))continue;
                if(el.tagName==='UL'||el.tagName==='OL'){for(const li of el.children){const c=li.cloneNode(true),tg=c.querySelector('.tg');let o='';if(tg){o=tg.textContent.trim();tg.remove();}cur.items.push(c.innerText.trim()+(o?' ('+o+')':''));}}
                else if(el.innerText.trim())cur.items.push(el.innerText.trim());
              }
              return out;})()""")
        finally:
            pg.close()


def alerts():
    """The alerts the Alerts tab shows, each with its next step and owner, plus the email's extra detail."""
    with _lock:
        pg = _page()
        try:
            _nav(pg, 'alerts')
            rows = pg.evaluate("""[...document.querySelectorAll('.alist .al')].map((a,i)=>({i:i,sev:a.querySelector('.sev').textContent.trim(),
              title:a.querySelector('.t1').innerText.trim(),detail:a.querySelector('.t2').innerText.trim(),when:(a.querySelector('.when')||{}).textContent||'',
              next:(()=>{const t=a.querySelector('.t3');if(!t)return '';const c=t.cloneNode(true);c.querySelectorAll('.tg').forEach(x=>x.remove());return c.textContent.replace(/^\\s*Next step:\\s*/,'').trim();})(),
              owner:(a.querySelector('.t3 .tg')||{}).textContent||'',preview:!!a.querySelector('[data-act=alertprev]')}))""")
            for r in rows:
                if not r['preview']:
                    continue
                pg.evaluate(f"document.querySelectorAll('.alist .al')[{r['i']}].querySelector('[data-act=alertprev]').click()")
                pg.wait_for_timeout(300)
                r.update(pg.evaluate("""(()=>{const b=document.querySelector('#drBody .mail-b'),o={why:'',reply:''};
                  for(const p of b.querySelectorAll('p')){if(p.textContent.startsWith('Why it matters:'))o.why=p.textContent.replace('Why it matters:','').trim();}
                  const r=b.querySelector('.mail-reply');if(r)o.reply=r.textContent.trim();return o;})()"""))
                pg.evaluate("document.getElementById('drClose').click()")
                pg.wait_for_timeout(150)
            return rows
        finally:
            pg.close()


def ask(question):
    """Ask V7 Pulse's answer to a question, as the website gives it (built-in answers)."""
    with _lock:
        pg = _page()
        try:
            pg.evaluate("document.getElementById('askBtn').click()")
            pg.wait_for_timeout(300)
            n = pg.evaluate("document.querySelectorAll('#chatLog .msg.bot').length")
            pg.fill('#askInput', question)
            pg.evaluate("document.getElementById('askForm').requestSubmit()")
            pg.wait_for_function(f"document.querySelectorAll('#chatLog .msg.bot').length>{n}", timeout=15000)
            pg.wait_for_timeout(300)
            return pg.evaluate("document.querySelector('#chatLog .msg.bot:last-child').innerHTML")
        finally:
            pg.close()


def close():
    global _pw, _browser
    for stop in (lambda: _browser and _browser.close(), lambda: _pw and _pw.stop()):
        try:
            stop()
        except Exception:
            pass
    _pw = _browser = None
