"""Reads V7 Pulse the way a person does: it opens the dashboard in a headless browser and takes the daily brief, the
alerts and Ask V7 Pulse's answers from the page. The Telegram bot and the website therefore always say the same thing,
from the same data and the same logic.

DASH_URL (env) picks the dashboard: the website's copy in docs/ by default. On a server it can be the live address.
"""
import os, pathlib, re, threading, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DASH_URL = os.environ.get('DASH_URL', (ROOT / 'docs' / 'index.html').as_uri())
SITE = 'https://mohanadabouserie.github.io/v7-pulse/'

_lock = threading.Lock()
_pw = _browser = None


def _page(init=None):
    global _pw, _browser
    if _browser is None or not _browser.is_connected():   # first use, or the browser crashed: start a new one
        close()
        _pw = sync_playwright().start()
        _browser = _pw.chromium.launch()
    pg = _browser.new_page(viewport={'width': 1280, 'height': 900})
    try:
        if init:
            pg.add_init_script(init)
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


# ---------------------------------------------------------------- Ask V7 Pulse with Claude
# On claude.ai the dashboard gets Claude through window.claude.use('sample') and hands it standing instructions and eight
# read-only tools over its own data. This stand-in for that runtime takes them over instead, so the bot can give Claude
# exactly what the dashboard gives it (claude_tools_mcp.py runs the tools; v7pulse_bot.py runs Claude Code).
FAKE_CLAUDE = """
window.__v7cap = null; window.__v7tools = {}; window.__v7ready = false;
window.claude = {use: async function (name) {
  if (name !== 'sample') return null;
  var sample = function (input, opts) {
    var tools = (opts && opts.tools) || [];
    tools.forEach(function (t) { window.__v7tools[t.name] = t.execute; });
    window.__v7cap = {input: input, tools: tools.map(function (t) {
      return {name: t.name, description: t.description, inputSchema: t.inputSchema || {type: 'object', properties: {}}}; })};
    return new Promise(function () {});   // the page keeps waiting: the answer goes to Telegram, not to this page
  };
  sample.limits = async function () { setTimeout(function () { window.__v7ready = true; }, 0); return {tools: {maxCount: 8}}; };
  return sample;
}};
"""
_ai = {}


def _ai_page():
    """A dashboard page that has handed over its Claude instructions and tools (window.__v7cap, window.__v7tools)."""
    pg = _page(FAKE_CLAUDE)
    try:
        pg.wait_for_function('window.__v7ready === true', timeout=15000)
        pg.evaluate("document.getElementById('askInput').value = 'What happened this week?'; document.getElementById('askForm').requestSubmit()")
        pg.wait_for_function('window.__v7cap !== null', timeout=15000)
    except Exception:
        pg.close(); raise
    return pg


def _stamp():
    """When the dashboard file last changed (None for a web address), so the cached instructions follow a new version."""
    if DASH_URL.startswith('file:'):
        try:
            return os.path.getmtime(urllib.parse.unquote(urllib.parse.urlparse(DASH_URL).path))
        except OSError:
            return None
    return None


def ai_setup():
    """{'rules', 'tools'}: the instructions and the eight read-only tools the dashboard gives Claude on claude.ai."""
    with _lock:
        if 'rules' not in _ai or _ai.get('stamp') != _stamp():
            pg = _ai_page()
            try:
                cap = pg.evaluate('window.__v7cap')
            finally:
                pg.close()
            _ai.update(stamp=_stamp(), rules=cap['input'][0]['content'], tools=cap['tools'])
        return {'rules': _ai['rules'], 'tools': _ai['tools']}


def tool_page():
    """A page whose dashboard tools run_tool can call."""
    with _lock:
        return _ai_page()


def run_tool(pg, name, args):
    """Runs one of the dashboard's read-only tools in the page; returns its result as JSON text."""
    with _lock:
        return pg.evaluate("""async ([n, i]) => { const f = window.__v7tools[n];
            if (!f) throw new Error('no tool called ' + n); return JSON.stringify(await f(i || {})); }""", [name, args or {}])


def close():
    global _pw, _browser
    for stop in (lambda: _browser and _browser.close(), lambda: _pw and _pw.stop()):
        try:
            stop()
        except Exception:
            pass
    _pw = _browser = None
