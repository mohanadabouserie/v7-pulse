"""The Telegram bot (bot/v7pulse_bot.py) against a stand-in for Telegram: no token, no network, nothing is sent.
It reads the real dashboard (the source file, or DASH_SRC), so the messages checked are the real ones."""
import datetime, html, os, pathlib, re, shutil, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP = tempfile.mkdtemp(prefix='v7bot_')
os.environ.update({'TELEGRAM_BOT_TOKEN': '000:test-token-for-the-tests', 'TELEGRAM_JOIN_CODE': 'join-test', 'V7_BOT_STATE': TMP,
                   'DASH_URL': os.environ.get('DASH_SRC', (ROOT / 'V7_Pulse_Dashboard.html').as_uri())})
sys.path.insert(0, str(ROOT / 'bot'))
import v7pulse_bot as b

fails = 0
def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))

TAGS = {'b', 'strong', 'i', 'em', 'u', 'ins', 's', 'strike', 'del', 'a', 'code', 'pre', 'tg-spoiler', 'blockquote'}
def tg_html_ok(t):
    """Telegram's HTML rules: only its tags, each closed in order, and every other <, > and & escaped."""
    stack = []
    for close, tag in re.findall(r'<(/?)([a-zA-Z-]+)[^>]*>', t):
        if tag not in TAGS: return False
        if close:
            if not stack or stack.pop() != tag: return False
        else: stack.append(tag)
    rest = re.sub(r'<(/?)([a-zA-Z-]+)[^>]*>', '', t)
    return not stack and '<' not in rest and '>' not in rest and not re.search(r'&(?!(lt|gt|amp|quot|#\d+|#x[0-9a-fA-F]+);)', rest)

calls, bad = [], []
BLOCKED = {'999'}
def fake_api(method, **p):
    """Telegram's answers, with its errors for a blocked chat, a message that's too long and HTML it can't read."""
    calls.append((method, p))
    if method == 'sendMessage':
        if str(p['chat_id']) in BLOCKED:
            raise RuntimeError('Telegram sendMessage failed: Forbidden: bot was blocked by the user')
        if len(p['text']) > 4096:
            raise RuntimeError('Telegram sendMessage failed: Bad Request: message is too long')
        if p.get('parse_mode') == 'HTML' and not tg_html_ok(p['text']):
            bad.append(p['text'][:300])
            raise RuntimeError("Telegram sendMessage failed: Bad Request: can't parse entities")
        return {'message_id': len(calls)}
    return {'getMe': {'username': 'v7_pulse_bot'}, 'getMyCommands': [], 'getMyDescription': {'description': ''},
            'getMyShortDescription': {'short_description': ''}}.get(method, True)
b.api = fake_api

subs = {}
def said(cid, since):
    return [p['text'] for m, p in calls[since:] if m == 'sendMessage' and str(p['chat_id']) == cid]
def say(cid, text, kind='private', first='Test'):
    chat = {'id': int(cid), 'type': kind, **({'first_name': first} if kind == 'private' else {'title': first})}
    n = len(calls); b.handle({'chat': chat, 'text': text}, subs); return said(cid, n)
def sends(since):
    return [p for m, p in calls[since:] if m == 'sendMessage']

# who can use it
out = say('111', '/start')
check('someone without the link gets the short note and nothing else', out == [b.NOT_MEMBER] and not subs, out)
out = say('111', 'what are the main complaints?')
check('… also when they ask a question', out == [b.NOT_MEMBER] and not subs, out)
out = say('111', '/start wrong-code')
check('a wrong join code is refused', out == [b.NOT_MEMBER] and not subs, out)
out = say('-100555', '/brief', kind='group', first='Some group')
check('a group that has not joined gets nothing', out == [], out)

# joining
n = len(calls); out = say('111', '/start join-test', first='Admin Person')
check('the first to join is the admin', subs.get('111', {}).get('role') == 'admin', subs)
check('on joining: the welcome, then the latest brief', len(out) == 2 and out[0].startswith('You’re in.') and 'V7 daily brief' in out[1], [o[:70] for o in out])
check('the admin’s welcome lists the admin commands', out and '/subscribers' in out[0] and '/test' in out[0])
latest = subs.get('111', {}).get('brief', '')
check('the chat is marked as having had the latest brief', latest.startswith('V7 daily brief') and len(out) == 2 and latest in html.unescape(out[1]), latest)
check('"typing…" shows while the brief is read', any(m == 'sendChatAction' and str(p['chat_id']) == '111' for m, p in calls[n:]))
check('the brief links to the Daily brief tab', len(out) == 2 and b.SITE + '#brief' in out[1])
n = len(calls); out = say('222', '/start join-test', first='Team Member')
check('the next one to join is a member', subs.get('222', {}).get('role') == 'member', subs.get('222'))
check('… gets the welcome and the brief, without the admin commands', len(out) == 2 and '/subscribers' not in out[0], [o[:70] for o in out])
check('… and the admin hears who joined', 'Team Member joined V7 Pulse on Telegram.' in said('111', n), said('111', n))
out = say('-100123', '/start@v7_pulse_bot join-test', kind='group', first='V7 Marketing')
check('a group joins with /start@v7_pulse_bot and the code', subs.get('-100123', {}).get('name') == 'V7 Marketing' and len(out) == 2, [o[:60] for o in out])
out = say('111', '/start join-test')
check('/start again: the help, nothing sent twice', out == [b.HELP], [o[:60] for o in out])

# on demand
out = say('222', '/brief 1')
check('/brief 1 gives the day before', len(out) == 1 and 'Sun 11 Oct' in out[0], out[0][:80] if out else out)
check('… and the latest brief stays marked as had', subs['222'].get('brief') == latest)
out = say('222', '/alerts')
check('/alerts lists the alerts with next steps', len(out) == 1 and out[0].startswith('<b>Alerts in Egypt') and 'Next step:' in out[0] and b.SITE + '#alerts' in out[0], out[0][:200] if out else out)
out = say('222', 'what are the main complaints?')
check('a question gets Ask V7 Pulse’s answer', len(out) == 1 and len(out[0]) > 80 and 'No answer for that one' not in out[0], out[0][:200] if out else out)
out = say('222', '/ask how is V Cola doing?')
check('/ask works too', len(out) == 1 and len(out[0]) > 20, out[0][:120] if out else out)
out = say('222', '/test')
check('admin commands do nothing for members', len(out) == 1 and 'Sample' not in out[0], out)
out = say('111', '/test')
check('/test (admin) sends a sample alert in full', len(out) == 1 and 'Sample of an alert' in out[0] and 'Why it matters' in out[0] and 'Next step:' in out[0], out[0][:300] if out else out)
out = say('111', '/subscribers')
check('/subscribers lists every chat', len(out) == 1 and all(k in out[0] for k in ('111', '222', '-100123')), out)
out = say('111', '/remove -100123')
check('/remove takes a chat off', out == ['Removed.'] and '-100123' not in subs, out)

# the 09:00 run
st = {}
at = lambda d, h, m: datetime.datetime(2026, 10, d, h, m, tzinfo=b.CAIRO)
check('the brief is not due before 09:00', not b.due_brief(st, at(17, 8, 59)))
check('… and is due from 09:00', b.due_brief(st, at(17, 9, 0)))
n = len(calls); got = b.daily_brief(subs, st, at(17, 9, 0))
check('09:00 with no new day of data: nothing is sent again', got == [] and not sends(n), got)
check('… and it runs once a day', not b.due_brief(st, at(17, 9, 30)) and b.due_brief(st, at(18, 9, 0)))
subs['222']['brief'] = 'V7 daily brief, Sun 11 Oct'      # as if a new day of data came in after 222's last brief
subs['999'] = {'name': 'Gone', 'type': 'private', 'role': 'member'}
n = len(calls); got = b.daily_brief(subs, st, at(18, 9, 0))
check('a new day of data reaches each chat that has not had it, once', got == ['222'], got)
check('a chat that blocked the bot is taken off the list', '999' not in subs)

# Act now alerts (the real data has none open right now, so one is made up here)
real_alerts = b.dash.alerts
act = {'sev': 'Act now', 'title': 'Test alert: a price claim is spreading', 'detail': 'Posts <with> & signs', 'when': 'today',
       'next': 'Post the price card', 'owner': 'Social team', 'why': 'It is spreading fast', 'reply': 'Reply text', 'preview': True}
b.dash.alerts = lambda: [act, {'sev': 'Watch', 'title': 'A watch item', 'detail': 'd', 'preview': False}]
n = len(calls); b.push_alerts(subs); out = sends(n)
check('an Act now alert goes to every chat on the list', sorted(str(p['chat_id']) for p in out) == sorted(subs), [p['chat_id'] for p in out])
check('… with why it matters, the next step, the owner and the suggested reply', out and all(all(s in p['text'] for s in ('Why it matters', 'Next step:', '(Social team)', 'Suggested reply')) for p in out))
check('… with its text escaped', out and '&lt;with&gt; &amp; signs' in out[0]['text'])
n = len(calls); b.push_alerts(subs)
check('… only once; Watch alerts wait for the brief', not sends(n))
out = say('333', '/start join-test', first='Late Joiner')
check('someone who joins later also gets the open Act now alert', len(out) == 3 and 'Test alert' in out[2], [o[:60] for o in out])
b.dash.alerts = real_alerts
out = say('333', '/stop')
check('/stop takes the chat off the list', '333' not in subs and len(out) == 1 and out[0].startswith('Done'), out)
out = say('333', 'hello')
check('… and after that it gets only the short note', out == [b.NOT_MEMBER], out)

# sending
long = '\n\n'.join('Paragraph %d ' % i + 'x' * 500 for i in range(30))
parts = b.chunks(long)
check('long messages are split under 4,096 characters, at paragraph breaks', len(parts) > 1 and all(len(p) <= 3900 for p in parts) and '\n\n'.join(parts) == long, [len(p) for p in parts])
parts = b.chunks('y' * 9000)
check('… even a single very long line', all(len(p) <= 3900 for p in parts) and ''.join(parts) == 'y' * 9000, [len(p) for p in parts])
check('every message so far follows Telegram’s HTML rules', not bad, bad[:2])
n = len(calls); b.send('111', '<b>an unclosed tag and 5 &lt; 6'); out = sends(n)
check('a message Telegram can’t read as HTML goes again as plain text', len(out) == 2 and 'parse_mode' not in out[1] and out[1]['text'] == 'an unclosed tag and 5 < 6', [p['text'] for p in out])
check('no message carries the token or the join code', not any(b.TOKEN in p['text'] or 'join-test' in p['text'] for p in sends(0)))

# the bot's menu and texts
n = len(calls); b.setup_profile(); made = {m: p for m, p in calls[n:]}
check('the command menu and the descriptions are set where empty', {'setMyCommands', 'setMyDescription', 'setMyShortDescription'} <= set(made), list(made))
check('the menu: brief, alerts, ask, help, stop', [c['command'] for c in made.get('setMyCommands', {}).get('commands', [])] == ['brief', 'alerts', 'ask', 'help', 'stop'])
b.api = lambda m, **p: (calls.append((m, p)), {'getMyCommands': [{'command': 'x', 'description': 'y'}], 'getMyDescription': {'description': 'by hand'},
                                               'getMyShortDescription': {'short_description': 'by hand'}}.get(m, True))[1]
n = len(calls); b.setup_profile()
check('… and never overwritten once set, so edits in @BotFather stay', not [m for m, p in calls[n:] if m.startswith('set')])
b.api = fake_api
check('Telegram’s limits: description 512, about 120, command text 256', len(b.DESCRIPTION) <= 512 and len(b.ABOUT) <= 120 and all(len(d) <= 256 for c, d in b.COMMANDS))
copy = ' '.join([b.HELP, b.ADMIN_NOTE, b.NOT_MEMBER, b.DESCRIPTION, b.ABOUT] + [d for c, d in b.COMMANDS])
check('bot copy: no "AI", no em dashes, no greetings', '—' not in copy and not re.search(r'\bAI\b', copy) and not re.search(r'\b(Hi|Hello|Welcome|Dear)\b', copy))

# secrets and running
b.log('a line with the token', b.TOKEN)
logtext = (pathlib.Path(TMP) / 'bot.log').read_text(encoding='utf-8')
check('the token never reaches the log', b.TOKEN not in logtext and '<token>' in logtext)
lock = b.single_instance()
try:
    b.single_instance(); second = 'a second copy started'
except SystemExit as e:
    second = str(e)
check('only one copy runs at a time', 'already running' in second, second)
lock.close(); b.dash.close(); shutil.rmtree(TMP, ignore_errors=True)
print('FAIL', fails)
