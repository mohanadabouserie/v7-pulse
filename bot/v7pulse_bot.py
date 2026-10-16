"""V7 Pulse on Telegram (@v7_pulse_bot).

What it does
- The daily brief at 09:00 Cairo time, as on the dashboard's Daily brief tab. Each chat gets each day's brief once, so
  when the dashboard has no new day of data, nothing is sent.
- "Act now" alerts as soon as they're found (checked every 2 hours), once per chat. Watch and Opportunity alerts are in
  the brief.
- Any question is answered by Claude the way Ask V7 Pulse answers it on claude.ai: Claude Code gets the dashboard's own
  instructions and its eight read-only tools (claude_tools_mcp.py), and nothing else. Until Claude is signed in (the
  bot's own login in bot/state/claude, or ANTHROPIC_API_KEY in .env.anthropic), questions get the built-in answers.
  /brief and /alerts on demand.
Everything is read from the dashboard itself (dashboard_reader.py), so Telegram and the website always agree.

Access
- People join with the private link t.me/v7_pulse_bot?start=<join code>. The first person to join is the admin.
  A chat that joins gets a welcome, the latest brief and any open "Act now" alerts.
- A group joins when someone types /start <join code> in it after adding the bot.
- Anyone else, for example someone who finds the bot in Telegram search or on the public website, gets a short note and
  nothing else.
- A chat that blocks the bot, or is deleted, is taken off the list.

Secrets and state
- .env.telegram in the project folder (git-ignored): TELEGRAM_BOT_TOKEN and TELEGRAM_JOIN_CODE. Never printed or logged.
  The same names set in the environment take precedence (the tests use this).
- bot/state/ (git-ignored; V7_BOT_STATE picks another folder): subscribers.json (chats, names, the last brief and the
  alerts each has had), sent.json (Telegram's update offset, the day of the last 09:00 run), claude_use.json (questions
  to Claude today), claude_tools.json, claude/ (the bot's Claude sign-in), bot.log, bot.pid.

Run: python3 bot/v7pulse_bot.py   (keeps running; stop it with Ctrl+C or kill $(cat bot/state/bot.pid)). One copy at a time.
Sign Claude in once: CLAUDE_CONFIG_DIR="$PWD/bot/state/claude" claude auth login   (see bot/README.md)
"""
import datetime, fcntl, glob, html, json, os, pathlib, re, shutil, signal, subprocess, sys, tempfile, time, traceback, urllib.error, urllib.request, zoneinfo
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dashboard_reader as dash

ROOT = HERE.parent
STATE = pathlib.Path(os.environ.get('V7_BOT_STATE') or HERE / 'state')
CAIRO = zoneinfo.ZoneInfo('Africa/Cairo')
BRIEF_AT = datetime.time(9, 0)
ALERT_EVERY = 2 * 3600
SITE = dash.SITE
SEV_MARK = {'Act now': '🔴', 'Watch': '🟡', 'Opportunity': '🟢', 'All clear': '✅'}
GONE = ('blocked', 'deactivated', 'chat not found', 'kicked', 'not a member')   # Telegram's errors for a chat that's gone
# Claude Code answers questions. V7_CLAUDE_CLI, V7_CLAUDE_MODEL, V7_CLAUDE_EFFORT and V7_CLAUDE_PER_DAY change the defaults.
CLAUDE_CLI = (os.environ.get('V7_CLAUDE_CLI') or shutil.which('claude')
              or (sorted(glob.glob(os.path.expanduser('~/.nvm/versions/node/*/bin/claude'))) or [''])[-1])
CLAUDE_HOME = STATE / 'claude'                                          # the bot's own Claude sign-in
CLAUDE_WORK = pathlib.Path(tempfile.gettempdir()) / 'v7pulse-bot'       # an empty folder: no project files or settings
CLAUDE_MODEL = os.environ.get('V7_CLAUDE_MODEL', 'claude-opus-5-5')
CLAUDE_EFFORT = os.environ.get('V7_CLAUDE_EFFORT', 'medium')
CLAUDE_PER_DAY = int(os.environ.get('V7_CLAUDE_PER_DAY', '100'))      # questions to Claude a day, for the plan's limits
CLAUDE_TIMEOUT = 180
CLAUDE_AT_ONCE = 2


def read_env():
    e, f = {}, ROOT / '.env.telegram'
    if f.exists():
        for line in open(f, encoding='utf-8'):
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1); e[k] = v
    e.update({k: os.environ[k] for k in ('TELEGRAM_BOT_TOKEN', 'TELEGRAM_JOIN_CODE', 'CLAUDE_BLOCKED_ORGS') if os.environ.get(k)})
    return e


ENV = read_env()
TOKEN, CODE = ENV.get('TELEGRAM_BOT_TOKEN', ''), ENV.get('TELEGRAM_JOIN_CODE', '')
# Claude accounts the bot never uses, by organization or email (comma-separated, in .env.telegram; DECISIONS #112)
BLOCKED_ORGS = [x.strip().lower() for x in ENV.get('CLAUDE_BLOCKED_ORGS', '').split(',') if x.strip()]
if not TOKEN:
    sys.exit('No bot token: put TELEGRAM_BOT_TOKEN=… in .env.telegram (see bot/README.md).')


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
    last = None
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=75))['result']
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read() or b'{}')
            except ValueError:
                body = {}
            if e.code == 429 or e.code >= 500:   # too many requests, or Telegram briefly down: wait and try again
                last = e; time.sleep(body.get('parameters', {}).get('retry_after', 5)); continue
            raise RuntimeError('Telegram %s failed: %s' % (method, body.get('description', e.code)))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e; time.sleep(5)
    raise RuntimeError('Telegram %s: no answer (%s)' % (method, safe(last)))


def chunks(text, n=3900):
    """The text in pieces under Telegram's 4,096 characters: split at paragraph breaks, then at line breaks."""
    out, cur = [], ''

    def add(piece, sep):
        nonlocal cur
        if cur and len(cur) + len(sep) + len(piece) > n:
            out.append(cur); cur = ''
        cur = cur + sep + piece if cur else piece
    for para in text.split('\n\n'):
        if len(para) <= n:
            add(para, '\n\n')
        else:
            for k, line in enumerate(para.split('\n')):
                for i in range(0, max(len(line), 1), n):
                    add(line[i:i + n], '' if i else '\n' if k else '\n\n')
    if cur:
        out.append(cur)
    return out


def send(chat, text):
    """Sends Telegram HTML. A piece Telegram can't read as HTML (a tag cut by a split) goes again as plain text."""
    for part in chunks(text):
        try:
            api('sendMessage', chat_id=chat, text=part, parse_mode='HTML', disable_web_page_preview=True)
        except RuntimeError as e:
            if "can't parse entities" not in str(e):
                raise
            api('sendMessage', chat_id=chat, text=html.unescape(re.sub(r'<[^>]+>', '', part)), disable_web_page_preview=True)


def typing(chat):
    """Shows "typing…" while the dashboard is read (a few seconds)."""
    try:
        api('sendChatAction', chat_id=chat, action='typing')
    except Exception:
        pass


def deliver(chat, text, subs):
    """Sends to one chat on the list; True if it arrived. A chat that blocked the bot or is gone is taken off."""
    try:
        send(chat, text); return True
    except RuntimeError as e:
        log('could not send to', chat, ':', safe(e))
        if any(g in str(e) for g in GONE):
            subs.pop(chat, None); save('subscribers.json', subs); log('taken off the list:', chat)
        return False


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


def md_inline(s):
    s = esc(s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(^|[\s(])\*([^*\n]+)\*(?=[\s).,;:!?]|$)', r'\1<i>\2</i>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', lambda m: '<a href="%s">%s</a>' % (m.group(2).replace('"', '%22'), m.group(1)), s)


def md_to_tg(src):
    """Claude's Markdown (as the dashboard renders it) as Telegram HTML: bold, italics, code and links kept; headings as
    bold lines; bullets and steps as text; tables as bullet lines; [[web: …]] and [[apify: …]] suggestions as lines."""
    out, table = [], []

    def flush():
        rows = [[c.strip() for c in r.strip('|').split('|')] for r in table if not re.match(r'^\|?\s*:?-{2,}', r)]
        if rows:
            out.append('<b>%s</b>' % ' · '.join(md_inline(c.replace('**', '')) for c in rows[0]))
            out.extend('• ' + ' · '.join(md_inline(c) for c in r) for r in rows[1:])
        table.clear()
    for line in str(src).split('\n'):
        s = line.strip()
        if len(s) > 1 and s[0] == '|' and s[-1] == '|':
            table.append(s); continue
        flush()
        m = re.match(r'\[\[(web|apify):(.+)\]\]$', s, re.I)
        if m:
            f = [x.strip() for x in m.group(2).split('|') if x.strip()]
            out.append('🔎 <i>Worth a web search:</i> ' + esc(f[0]) + (' (%s)' % esc(f[1]) if len(f) > 1 else '') if m.group(1).lower() == 'web'
                       else '📥 <i>New data to collect, needs approval:</i> ' + esc(' · '.join(f)))
            continue
        m = re.match(r'#{1,4}\s+(.*)$', s)
        if m:
            out.append('<b>%s</b>' % md_inline(m.group(1).replace('**', ''))); continue
        m = re.match(r'[-*•]\s+(.*)$', s)
        if m:
            out.append(('    ◦ ' if len(line) - len(line.lstrip()) >= 2 else '• ') + md_inline(m.group(1))); continue
        out.append(md_inline(s))
    flush()
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()


# ---------------------------------------------------------------- messages

def brief_msg(day=0):
    """(subject, Telegram text) of the brief: day 0 is the latest day of data, 1 the day before, up to 6."""
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
    return b['subject'], '\n\n'.join(out)


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


def help_text():
    return ('<b>V7 Pulse</b> sends the daily brief at 09:00 and “Act now” alerts as soon as they’re found.\n\n'
            '/brief  the latest brief (/brief 1 for the day before)\n/alerts  what needs attention, with next steps\n'
            '/ask <i>question</i>  or just type a question\n/stop  stop the brief and alerts\n\n'
            + ('Claude answers questions from the dashboard’s data, the way Ask V7 Pulse does. ' if claude_ready()
               else 'Questions get the same answers as Ask V7 Pulse on the website. ')
            + '<a href="%s">Open V7 Pulse</a>' % SITE)


ADMIN_NOTE = ('\n\nYou’re the admin: /subscribers lists who gets the reports, /remove <i>id</i> takes someone off, '
              '/test sends you a sample alert. You’ll hear when someone joins.')
NOT_MEMBER = ('This bot sends V7’s marketing alerts and reports to V7’s team. '
              'To join, ask the person who runs V7 Pulse for the join link.')
# The menu and the texts people see before they tap Start; set once, so later edits in @BotFather stay.
COMMANDS = [('brief', 'The latest daily brief'), ('alerts', 'What needs attention, with next steps'),
            ('ask', 'Ask a question (or just type it)'), ('help', 'What V7 Pulse sends'),
            ('stop', 'Stop the brief and alerts in this chat')]
ABOUT = 'The daily brief and alerts from V7 Pulse, for V7’s marketing team.'
DESCRIPTION = ('V7 Pulse for V7’s marketing team: the daily brief at 09:00 Cairo time, alerts that need action as soon '
               'as they’re found, and answers to questions about what people say about V7 online.\n\n'
               'The team joins with a private link.')


# ---------------------------------------------------------------- commands

def give_brief(cid, subs, day=0):
    """Sends one chat the brief. The latest one is then marked as had, so 09:00 doesn't send it again."""
    subject, text = brief_msg(day)
    send(cid, text)
    if day == 0 and cid in subs:
        subs[cid]['brief'] = subject; save('subscribers.json', subs)


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
            send(cid, help_text()); return
        if CODE and arg.strip() == CODE:
            role = 'member' if any(s.get('role') == 'admin' for s in subs.values()) else 'admin'
            subs[cid] = {'name': name, 'type': chat.get('type'), 'role': role, 'since': datetime.datetime.now(CAIRO).isoformat(timespec='minutes')}
            save('subscribers.json', subs)
            log('joined:', cid, chat.get('type'), role)
            send(cid, 'You’re in. ' + help_text() + (ADMIN_NOTE if role == 'admin' else ''))
            for k in [k for k, s in subs.items() if s.get('role') == 'admin' and k != cid]:
                deliver(k, '%s joined V7 Pulse on Telegram.' % esc(name), subs)
            typing(cid)
            give_brief(cid, subs)          # the latest brief right away
            push_alerts(subs, only=cid)    # and any Act now alert that's open
            return
        send(cid, NOT_MEMBER); log('refused /start from', cid); return
    if not member:
        if chat.get('type') == 'private':
            send(cid, NOT_MEMBER)
        return
    if cmd == '/help':
        send(cid, help_text())
    elif cmd == '/brief':
        typing(cid)
        give_brief(cid, subs, int(arg) if arg.strip().isdigit() and int(arg) < 7 else 0)
    elif cmd == '/alerts':
        typing(cid); send(cid, alerts_text())
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
        typing(cid)
        rows = [r for r in dash.alerts() if r.get('preview')]
        if rows:
            send(cid, '<i>Sample of an alert as it arrives (test, sent only to you):</i>\n\n' + alert_text(rows[0], full=True))
    else:   # a question, with /ask or without
        q = arg if cmd == '/ask' else ('' if cmd else text)
        if not q:
            send(cid, 'Type a question, for example: what are the main complaints?'); return
        answer_question(cid, q)


# ---------------------------------------------------------------- questions answered by Claude
# Claude Code (the `claude` command) gets the dashboard's own instructions and its eight read-only tools through
# claude_tools_mcp.py, and nothing else: no built-in tools (files, shell, web), no other tool servers, no settings,
# an empty folder and a clean environment. It signs in with the bot's own login (bot/state/claude), or with
# ANTHROPIC_API_KEY from .env.anthropic once there is one. Answers run in the background, so the bot keeps working.

TELEGRAM_RULES = '\n'.join([
    'ON TELEGRAM',
    '- This chat is V7 Pulse’s Telegram bot (@v7_pulse_bot), not the dashboard page. The person asking is on V7’s team.',
    '- Keep it short for a phone: the answer first, then at most six bullets. Aim for under 1,200 characters.',
    '- No tables: Telegram can’t show them. Use bullets.',
    '- Name the dashboard tab to open; a link to the dashboard goes under your answer.',
    '- Earlier questions and answers from this chat, when there are any, come before the new question.'])
HIST = {}               # chat -> {'t': time, 'turns': [(question, answer), …]}: the last exchanges, kept in memory only
JOBS, WAITING = [], []
_claude = {'at': 0, 'ok': False, 'model': CLAUDE_MODEL}   # model: '' once the plan has refused CLAUDE_MODEL


def api_key():
    """ANTHROPIC_API_KEY from .env.anthropic, once there is one: Claude then bills the API instead of the bot's login."""
    f = ROOT / '.env.anthropic'
    if f.exists():
        for line in open(f, encoding='utf-8'):
            if line.startswith('ANTHROPIC_API_KEY=') and line.strip()[18:]:
                return line.strip()[18:]
    return ''


def claude_env():
    """Claude Code's whole environment: the bot's sign-in folder, and nothing else from this machine."""
    env = {'HOME': str(pathlib.Path.home()), 'LANG': 'C.UTF-8', 'CLAUDE_CONFIG_DIR': str(CLAUDE_HOME),
           'PATH': os.pathsep.join([os.path.dirname(CLAUDE_CLI), '/usr/local/bin', '/usr/bin', '/bin'])}
    if api_key():
        env['ANTHROPIC_API_KEY'] = api_key()
    return env


def claude_ready():
    """True when Claude can answer: an API key, or the bot signed in to Claude. Checked at most once a minute."""
    if not (CLAUDE_CLI and os.path.exists(CLAUDE_CLI)):
        return False
    if api_key():
        return True
    if time.time() - _claude['at'] > 60:
        _claude['at'] = time.time()
        CLAUDE_HOME.mkdir(parents=True, exist_ok=True); CLAUDE_WORK.mkdir(exist_ok=True)
        try:
            r = subprocess.run([CLAUDE_CLI, 'auth', 'status'], capture_output=True, text=True, timeout=30, env=claude_env(), cwd=CLAUDE_WORK)
            info = json.loads(r.stdout or '{}')
            who = ('%s %s' % (info.get('email') or '', info.get('orgName') or '')).lower()
            blocked = info.get('loggedIn') is True and any(o in who for o in BLOCKED_ORGS)
            if blocked and not _claude.get('blocked'):
                log('Claude is signed in with an account in CLAUDE_BLOCKED_ORGS; the bot won’t use it')
            _claude['blocked'] = blocked
            _claude['ok'] = info.get('loggedIn') is True and not blocked
        except Exception as e:
            _claude['ok'] = False; log('could not check the Claude sign-in:', safe(e))
    return _claude['ok']


def claude_quota():
    """Counts today's question to Claude; False once V7_CLAUDE_PER_DAY is reached."""
    day = datetime.datetime.now(CAIRO).date().isoformat()
    use = load('claude_use.json', {})
    if use.get('day') != day:
        use = {'day': day, 'n': 0}
    if use['n'] >= CLAUDE_PER_DAY:
        return False
    use['n'] += 1; save('claude_use.json', use)
    return True


def builtin_answer(cid, q, note=''):
    """The dashboard's built-in answer, after a short line on why it isn't Claude's."""
    typing(cid)
    text = to_tg(dash.ask(q)) or 'No answer for that one. Try /brief or /alerts.'
    send(cid, ('<i>%s</i>\n\n' % esc(note) if note else '') + text)


def answer_question(cid, q):
    """A question from a chat on the list: Claude answers in the background, or the built-in answer comes now."""
    if not claude_ready():
        return builtin_answer(cid, q, ('Claude is signed in with an account the bot doesn’t use' if _claude.get('blocked')
                                       else 'Claude isn’t connected yet') + ', so this is the dashboard’s built-in answer.')
    if not claude_quota():
        return builtin_answer(cid, q, 'Today’s %d questions to Claude are used up, so this is the dashboard’s built-in answer.' % CLAUDE_PER_DAY)
    WAITING.append({'cid': cid, 'q': q}); typing(cid)
    start_jobs()


def claude_prompt(cid, q):
    h = HIST.get(cid)
    turns = h['turns'] if h and time.time() - h['t'] < 2 * 3600 else []
    if not turns:
        return q
    past = '\n\n'.join('Question: %s\nYour answer: %s' % (a, b[:1500]) for a, b in turns)
    return 'Earlier in this Telegram chat:\n\n%s\n\nNew question: %s' % (past, q)


def start_claude(job):
    """Starts Claude Code on one question. The question goes in on stdin; the answer comes back as JSON."""
    ai = dash.ai_setup()
    save('claude_tools.json', ai['tools'])
    CLAUDE_HOME.mkdir(parents=True, exist_ok=True); CLAUDE_WORK.mkdir(exist_ok=True)
    env = claude_env()
    server = {'type': 'stdio', 'command': sys.executable, 'args': [str(HERE / 'claude_tools_mcp.py')],
              'env': {'V7_TOOLS_FILE': str(STATE / 'claude_tools.json'), 'DASH_URL': dash.DASH_URL,
                      'HOME': env['HOME'], 'LANG': env['LANG'], 'PATH': env['PATH']}}
    job['model'] = _claude['model']
    cmd = [CLAUDE_CLI, '-p', '--output-format', 'json'] + (['--model', job['model']] if job['model'] else []) + ['--effort', CLAUDE_EFFORT,
           '--system-prompt', ai['rules'] + '\n\n' + TELEGRAM_RULES, '--tools', '', '--strict-mcp-config',
           '--mcp-config', json.dumps({'mcpServers': {'v7pulse': server}}), '--allowedTools', 'mcp__v7pulse',
           '--no-session-persistence']
    with tempfile.TemporaryFile() as prompt:
        prompt.write(claude_prompt(job['cid'], job['q']).encode('utf-8')); prompt.seek(0)
        job['out'], job['err'] = tempfile.TemporaryFile(), tempfile.TemporaryFile()
        job['proc'] = subprocess.Popen(cmd, stdin=prompt, stdout=job['out'], stderr=job['err'], cwd=CLAUDE_WORK, env=env,
                                       start_new_session=True)
    job['started'] = time.time(); job['typing'] = time.time() + 4.5
    log('Claude is answering', job['cid'])


def start_jobs():
    """Starts waiting questions: one at a time per chat, CLAUDE_AT_ONCE in all."""
    for job in list(WAITING):
        if len(JOBS) >= CLAUDE_AT_ONCE:
            break
        if any(j['cid'] == job['cid'] for j in JOBS):
            continue
        WAITING.remove(job)
        try:
            start_claude(job); JOBS.append(job)
        except Exception as e:
            log('could not start Claude:', safe(e))
            builtin_answer(job['cid'], job['q'], 'Claude couldn’t be reached, so this is the dashboard’s built-in answer.')


def stop_job(job):
    try:
        os.killpg(job['proc'].pid, signal.SIGKILL)   # Claude Code, its tool server and that server's browser
    except OSError:
        pass
    job['proc'].wait()


def read_claude(raw, code):
    """(answer, None) from Claude Code's JSON output, or (None, why there's no answer)."""
    try:
        r = json.loads(raw)
    except ValueError:
        r = {}
    if r.get('type') == 'result' and not r.get('is_error') and str(r.get('result') or '').strip():
        return r['result'].strip(), None
    return None, str(r.get('result') or r.get('subtype') or 'no answer (exit code %s)' % code)[:200]


def finish(job, text, why=None):
    cid, q = job['cid'], job['q']
    if text:
        h = HIST.setdefault(cid, {'t': 0, 'turns': []})
        h['t'] = time.time(); h['turns'] = (h['turns'] + [(q, text)])[-3:]
        log('Claude answered', cid, 'in %d s' % (time.time() - job['started']))
        send(cid, md_to_tg(text) + '\n\n<a href="%s">Open V7 Pulse</a>' % SITE)
        return
    job['err'].seek(0)
    log('Claude did not answer', cid + ':', safe(why), '|', safe(job['err'].read().decode('utf-8', 'replace')[-200:]))
    if job['model'] and 'model' in why.lower():   # the plan doesn't include that model: use the plan's default from now on
        _claude['model'] = ''; WAITING.insert(0, {'cid': cid, 'q': q}); log('using the plan’s default model from now on')
        return
    if re.search(r'log ?in|auth', why, re.I):     # "Not logged in": check the sign-in again before the next question
        _claude.update(at=0, ok=False)
    builtin_answer(cid, q, ('Claude’s usage limit is reached for now' if 'limit' in why.lower() else 'Claude couldn’t answer just now')
                   + ', so this is the dashboard’s built-in answer.')


def check_jobs():
    """Sends the answers that are ready, keeps "typing…" on for the others, and starts waiting questions."""
    for job in list(JOBS):
        if job['proc'].poll() is None:
            if time.time() - job['started'] > CLAUDE_TIMEOUT:
                stop_job(job); JOBS.remove(job)
                result = (None, 'no answer after %d seconds' % CLAUDE_TIMEOUT)
            else:
                if time.time() >= job['typing']:
                    typing(job['cid']); job['typing'] = time.time() + 4.5
                continue
        else:
            JOBS.remove(job); job['out'].seek(0)
            result = read_claude(job['out'].read().decode('utf-8', 'replace'), job['proc'].returncode)
        try:
            finish(job, *result)
        except Exception as e:
            log('could not send the answer to', job['cid'], ':', safe(e))
    start_jobs()


# ---------------------------------------------------------------- the schedule

def due_brief(st, now=None):
    now = now or datetime.datetime.now(CAIRO)
    return now.time() >= BRIEF_AT and st.get('last_brief') != now.date().isoformat()


def daily_brief(subs, st, now=None):
    """The 09:00 run: the latest brief to every chat that hasn't had it. Returns the chats it reached."""
    subject, text = brief_msg(0)
    got = [k for k in list(subs) if subs.get(k, {}).get('brief') != subject and deliver(k, text, subs)]
    for k in got:
        subs[k]['brief'] = subject
    save('subscribers.json', subs)
    st['last_brief'] = (now or datetime.datetime.now(CAIRO)).date().isoformat(); save('sent.json', st)
    log('brief sent to %d: %s' % (len(got), subject) if got else 'brief: no new day of data (latest: %s)' % subject)
    return got


def push_alerts(subs, only=None):
    """Each "Act now" alert, once to each chat on the list (or only to the chat given). Returns those alerts."""
    rows = [a for a in dash.alerts() if a['sev'] == 'Act now']
    for a in rows:
        key = a['sev'] + '|' + a['title']
        for k in ([only] if only else list(subs)):
            s = subs.get(k)
            if s is None or key in s.get('alerts', []):
                continue
            if deliver(k, alert_text(a, full=True) + '\n\n<a href="%s#alerts">Open in V7 Pulse</a>' % SITE, subs):
                s['alerts'] = (s.get('alerts', []) + [key])[-200:]
                log('alert sent to', k + ':', a['title'])
    save('subscribers.json', subs)
    return rows


def setup_profile():
    """The command menu and the bot's descriptions, set only where empty."""
    if not api('getMyCommands'):
        api('setMyCommands', commands=[{'command': c, 'description': d} for c, d in COMMANDS])
    if not api('getMyDescription').get('description'):
        api('setMyDescription', description=DESCRIPTION)
    if not api('getMyShortDescription').get('short_description'):
        api('setMyShortDescription', short_description=ABOUT)


def single_instance():
    """Only one copy runs at a time: two would both answer and both send the brief. Keep the returned file open."""
    STATE.mkdir(exist_ok=True)
    f = open(STATE / 'bot.pid', 'a+')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.seek(0); sys.exit('The V7 Pulse bot is already running (process %s).' % (f.read().strip() or '?'))
    f.seek(0); f.truncate(); f.write(str(os.getpid())); f.flush()
    return f


def run():
    lock = single_instance()
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
    me = api('getMe'); log('running as @%s' % me['username'])
    try:
        setup_profile()
    except Exception as e:
        log('could not set the command menu:', safe(e))
    subs = load('subscribers.json', {}); st = load('sent.json', {})
    offset = st.get('offset', 0); next_check = 0
    try:
        while True:
            try:
                for u in api('getUpdates', offset=offset, timeout=2 if JOBS or WAITING else 50, allowed_updates=['message']):
                    offset = u['update_id'] + 1; st['offset'] = offset; save('sent.json', st)
                    if u.get('message'):
                        try:
                            handle(u['message'], subs)
                        except Exception as e:
                            log('error handling a message:', safe(e)); log(safe(traceback.format_exc()))
                check_jobs()
                if subs and due_brief(st):
                    daily_brief(subs, st)
                if subs and time.time() >= next_check:
                    next_check = time.time() + ALERT_EVERY
                    push_alerts(subs)
            except Exception as e:
                log('loop error:', safe(e)); time.sleep(15)
    except KeyboardInterrupt:
        pass
    finally:
        for job in JOBS:
            stop_job(job)
        dash.close(); log('stopped'); lock.close()


if __name__ == '__main__':
    run()
