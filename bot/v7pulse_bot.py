"""V7 Pulse on Telegram (@v7_pulse_bot).

What it does
- Every morning at 09:00 Cairo time: the daily brief, as on the dashboard's Daily brief tab.
- "Act now" alerts as soon as they're found (checked every 2 hours); Watch and Opportunity alerts are in the brief.
- Any question gets Ask V7 Pulse's answer, the same as on the website. /brief and /alerts on demand.
Everything is read from the dashboard itself (dashboard_reader.py), so Telegram and the website always agree.

Access
- People join with the private link t.me/v7_pulse_bot?start=<join code>. The first person to join is the admin.
- A group joins when someone types /start <join code> in it after adding the bot.
- Anyone else, for example someone who finds the bot on the public website, gets a short note and nothing else.

Secrets and state
- .env.telegram in the project folder (git-ignored): TELEGRAM_BOT_TOKEN and TELEGRAM_JOIN_CODE. Never printed or logged.
- bot/state/ (git-ignored): subscribers.json (chat ids and names), sent.json (alerts already sent, last brief), bot.log.

Run: python3 bot/v7pulse_bot.py      (keeps running; stop it with Ctrl+C)
"""
import datetime, html, json, os, pathlib, re, sys, time, traceback, urllib.error, urllib.request, zoneinfo
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dashboard_reader as dash

ROOT = HERE.parent
STATE = HERE / 'state'
CAIRO = zoneinfo.ZoneInfo('Africa/Cairo')
BRIEF_AT = datetime.time(9, 0)
ALERT_EVERY = 2 * 3600
SITE = dash.SITE
SEV_MARK = {'Act now': '🔴', 'Watch': '🟡', 'Opportunity': '🟢', 'All clear': '✅'}


def read_env():
    e = {}
    for line in open(ROOT / '.env.telegram', encoding='utf-8'):
        if '=' in line:
            k, v = line.strip().split('=', 1); e[k] = v
    return e


ENV = read_env()
TOKEN, CODE = ENV['TELEGRAM_BOT_TOKEN'], ENV.get('TELEGRAM_JOIN_CODE', '')


def safe(x):
    """Any text that goes to the log, with the token removed."""
    return str(x).replace(TOKEN, '<token>')


def log(*a):
    STATE.mkdir(exist_ok=True)
    line = datetime.datetime.now(CAIRO).strftime('%Y-%m-%d %H:%M:%S') + '  ' + safe(' '.join(str(x) for x in a))
    print(line, flush=True)
    with open(STATE / 'bot.log', 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def load(name, default):
    try:
        return json.load(open(STATE / name, encoding='utf-8'))
    except Exception:
        return default


def save(name, data):
    STATE.mkdir(exist_ok=True)
    tmp = STATE / (name + '.tmp')
    json.dump(data, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, STATE / name)


def api(method, **params):
    req = urllib.request.Request('https://api.telegram.org/bot%s/%s' % (TOKEN, method), data=json.dumps(params).encode(),
                                 headers={'Content-Type': 'application/json'})
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=75))['result']
        except urllib.error.HTTPError as e:
            body = json.loads(e.read() or b'{}')
            if e.code == 429:
                time.sleep(body.get('parameters', {}).get('retry_after', 5)); continue
            raise RuntimeError('Telegram %s failed: %s' % (method, body.get('description', e.code)))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e; time.sleep(5)
    raise RuntimeError('Telegram %s: no connection (%s)' % (method, safe(last)))


def send(chat, text):
    """Sends HTML text, split at paragraph breaks to stay under Telegram's 4,096 characters."""
    parts, cur = [], ''
    for para in text.split('\n\n'):
        if len(cur) + len(para) + 2 > 3900 and cur:
            parts.append(cur); cur = ''
        cur = (cur + '\n\n' + para) if cur else para
    if cur:
        parts.append(cur)
    for p in parts:
        api('sendMessage', chat_id=chat, text=p, parse_mode='HTML', disable_web_page_preview=True)


def esc(t):
    return html.escape(str(t), quote=False)


class TG(HTMLParser):
    """The dashboard's answer HTML as Telegram HTML: bold, italics and links kept; lists as bullets; buttons dropped."""
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0; self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ('button', 'svg', 'style', 'script'):
            self.skip += 1; return
        if self.skip:
            return
        a = dict(attrs)
        if tag in ('b', 'strong'): self.out.append('<b>')
        elif tag in ('i', 'em'): self.out.append('<i>')
        elif tag == 'a':
            ok = a.get('href', '').startswith('http'); self.links.append(ok)
            if ok: self.out.append('<a href="%s">' % html.escape(a['href']))
        elif tag == 'li': self.out.append('\n• ')
        elif tag == 'br': self.out.append('\n')
        elif tag in ('p', 'div', 'ul', 'ol', 'h3', 'h4', 'table', 'tr'): self.out.append('\n')

    def handle_endtag(self, tag):
        if tag in ('button', 'svg', 'style', 'script'):
            self.skip = max(0, self.skip - 1); return
        if self.skip:
            return
        if tag in ('b', 'strong'): self.out.append('</b>')
        elif tag in ('i', 'em'): self.out.append('</i>')
        elif tag == 'a':
            if self.links and self.links.pop(): self.out.append('</a>')
        elif tag in ('p', 'div', 'ul', 'ol', 'h3', 'h4', 'table'): self.out.append('\n')
        elif tag in ('td', 'th'): self.out.append('  ')

    def handle_data(self, d):
        if not self.skip:
            self.out.append(esc(d))


def to_tg(h):
    p = TG(); p.feed(h)
    s = ''.join(p.out)
    s = re.sub(r'<a href="[^"]*">\s*</a>', '', s)
    s = re.sub(r'[ \t]+\n', '\n', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()


# ---------------------------------------------------------------- messages

def brief_text(day=0):
    b = dash.brief(day)
    out = ['<b>%s</b>' % esc(b['subject'])]
    for s in b['sections']:
        title, items = s['title'], s['items']
        mark = {'Red flags': '🚩 ', 'Positive signals': '👍 ', 'Worth amplifying': '📣 ', 'Recommended actions': '🎯 '}.get(title, '')
        block = ['<b>%s%s</b>' % (mark, esc(title))]
        for k, it in enumerate(items):
            lines = [x.strip() for x in it.split('\n') if x.strip()]
            if not lines:
                continue
            if title == 'Brand health':
                block.append(esc(' '.join(lines)))
            elif title == 'Recommended actions':
                block.append('%d. %s' % (k + 1, esc(' '.join(lines))))
            else:
                block.append('• <b>%s</b>' % esc(lines[0]) + ''.join('\n   ' + esc(x) for x in lines[1:]))
        out.append('\n'.join(block))
    out.append('<a href="%s#brief">Open the brief in V7 Pulse</a>' % SITE)
    return '\n\n'.join(out)


def alert_text(a, full=False):
    t = '%s <b>%s: %s</b>' % (SEV_MARK.get(a['sev'], '•'), esc(a['sev']), esc(a['title']))
    if a.get('when'):
        t += '  <i>%s</i>' % esc(a['when'])
    t += '\n' + esc(a['detail'])
    if full and a.get('why'):
        t += '\n<b>Why it matters:</b> ' + esc(a['why'])
    if a.get('next'):
        t += '\n<b>Next step:</b> ' + esc(a['next']) + (' (%s)' % esc(a['owner']) if a.get('owner') else '')
    if full and a.get('reply'):
        t += '\n<b>Suggested reply:</b>\n' + esc(a['reply'])
    return t


def alerts_text():
    rows = dash.alerts()
    order = {'Act now': 0, 'Watch': 1, 'Opportunity': 2, 'All clear': 3}
    rows.sort(key=lambda r: order.get(r['sev'], 4))
    if not rows:
        return 'No alerts right now.'
    return '<b>Alerts in Egypt, last 30 days</b>\n\n' + '\n\n'.join(alert_text(a) for a in rows) + '\n\n<a href="%s#alerts">Open Alerts in V7 Pulse</a>' % SITE


HELP = ('<b>V7 Pulse</b> sends the daily brief at 09:00 and “Act now” alerts as soon as they’re found.\n\n'
        '/brief  today’s brief\n/alerts  what needs attention, with next steps\n/ask <i>question</i>  or just type a question\n'
        '/stop  stop the brief and alerts\n\nQuestions get the same answers as Ask V7 Pulse on the website. '
        '<a href="%s">Open V7 Pulse</a>' % SITE)
NOT_MEMBER = ('This bot sends V7’s marketing alerts and reports to V7’s team. '
              'To join, ask the person who runs V7 Pulse for the join link.')


# ---------------------------------------------------------------- commands

def handle(msg, subs):
    chat = msg['chat']; cid = str(chat['id']); text = (msg.get('text') or '').strip()
    if not text:
        return
    name = chat.get('title') or ' '.join(x for x in (chat.get('first_name'), chat.get('last_name')) if x) or chat.get('username') or cid
    cmd, _, arg = text.partition(' ')
    cmd = cmd.split('@')[0].lower() if cmd.startswith('/') else ''
    member = cid in subs
    is_admin = member and subs[cid].get('role') == 'admin'
    if cmd == '/start':
        if member:
            send(cid, HELP); return
        if CODE and arg.strip() == CODE:
            role = 'member' if any(s.get('role') == 'admin' for s in subs.values()) else 'admin'
            subs[cid] = {'name': name, 'type': chat.get('type'), 'role': role, 'since': datetime.datetime.now(CAIRO).isoformat(timespec='minutes')}
            save('subscribers.json', subs)
            log('joined:', cid, chat.get('type'), role)
            send(cid, 'You’re in. ' + HELP + ('\n\nYou’re the admin: /subscribers lists who gets the reports, /remove <i>id</i> takes someone off, /test sends you a sample alert.' if role == 'admin' else ''))
            for k, s in subs.items():
                if s.get('role') == 'admin' and k != cid:
                    send(k, '%s joined V7 Pulse on Telegram.' % esc(name))
            return
        send(cid, NOT_MEMBER); log('refused /start from', cid); return
    if not member:
        if chat.get('type') == 'private':
            send(cid, NOT_MEMBER)
        return
    if cmd == '/help':
        send(cid, HELP)
    elif cmd == '/brief':
        send(cid, '…'); send(cid, brief_text(int(arg) if arg.strip().isdigit() and int(arg) < 7 else 0))
    elif cmd == '/alerts':
        send(cid, alerts_text())
    elif cmd == '/stop':
        subs.pop(cid, None); save('subscribers.json', subs); log('left:', cid)
        send(cid, 'Done: no more briefs or alerts here. Use the join link to come back.')
    elif cmd == '/subscribers' and is_admin:
        send(cid, '<b>Getting V7 Pulse</b>\n' + '\n'.join('• %s (%s, %s) <code>%s</code>' % (esc(s['name']), esc(s.get('type')), esc(s.get('role')), k) for k, s in subs.items()))
    elif cmd == '/remove' and is_admin:
        k = arg.strip()
        if k in subs and k != cid:
            subs.pop(k); save('subscribers.json', subs); send(cid, 'Removed.'); log('removed:', k)
        else:
            send(cid, 'Send /remove with an id from /subscribers.')
    elif cmd == '/test' and is_admin:
        rows = [r for r in dash.alerts() if r.get('preview')]
        if rows:
            send(cid, '<i>Sample of an alert as it arrives (test, sent only to you):</i>\n\n' + alert_text(rows[0], full=True))
    else:   # a question, with /ask or without
        q = arg if cmd == '/ask' else ('' if cmd else text)
        if not q:
            send(cid, 'Type a question, for example: what are the main complaints?'); return
        send(cid, to_tg(dash.ask(q)) or 'No answer for that one. Try /brief or /alerts.')


# ---------------------------------------------------------------- the schedule

def due_brief(st):
    now = datetime.datetime.now(CAIRO)
    return now.time() >= BRIEF_AT and st.get('last_brief') != now.date().isoformat()


def run():
    me = api('getMe'); log('running as @%s' % me['username'])
    subs = load('subscribers.json', {}); st = load('sent.json', {})
    offset = st.get('offset', 0); last_check = 0
    while True:
        try:
            for u in api('getUpdates', offset=offset, timeout=50, allowed_updates=['message']):
                offset = u['update_id'] + 1; st['offset'] = offset; save('sent.json', st)
                if u.get('message'):
                    try:
                        handle(u['message'], subs)
                    except Exception as e:
                        log('error handling a message:', safe(e)); traceback.print_exc(file=sys.stdout)
            if subs and due_brief(st):
                text = brief_text(0)
                for k in list(subs):
                    send(k, text)
                st['last_brief'] = datetime.datetime.now(CAIRO).date().isoformat(); save('sent.json', st); log('brief sent to', len(subs))
            if subs and time.time() - last_check > ALERT_EVERY:
                last_check = time.time(); sent = set(st.get('alerts', []))
                for a in dash.alerts():
                    key = a['sev'] + '|' + a['title']
                    if a['sev'] == 'Act now' and key not in sent:
                        for k in list(subs):
                            send(k, alert_text(a, full=True) + '\n\n<a href="%s#alerts">Open in V7 Pulse</a>' % SITE)
                        sent.add(key); log('alert sent:', a['title'])
                st['alerts'] = sorted(sent); save('sent.json', st)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log('loop error:', safe(e)); time.sleep(15)
    dash.close()


if __name__ == '__main__':
    run()
