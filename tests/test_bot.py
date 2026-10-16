"""The Telegram bot (bot/v7pulse_bot.py) against stand-ins for Telegram and for Claude Code (tests/fake_claude.py):
no token, no account, no network, nothing is sent or spent. It reads the real dashboard (the source file, or DASH_SRC)
and runs the real tool server, so the messages and the tool results checked are the real ones."""
import datetime, html, json, os, pathlib, re, shutil, subprocess, sys, tempfile, time
ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP = tempfile.mkdtemp(prefix='v7bot_')
FAKE = ROOT / 'tests' / 'fake_claude.py'
os.chmod(FAKE, 0o755)
os.environ.update({'TELEGRAM_BOT_TOKEN': '000:test-token-for-the-tests', 'TELEGRAM_JOIN_CODE': 'join-test', 'V7_BOT_STATE': TMP,
                   'DASH_URL': os.environ.get('DASH_SRC', (ROOT / 'V7_Pulse_Dashboard.html').as_uri()), 'V7_CLAUDE_CLI': str(FAKE),
                   'CLAUDE_BLOCKED_ORGS': 'Other Co, blocked.example'})
def fake_mode(m):
    """What the stand-in for Claude Code does next: '' answers, or logged_out, not_logged_in, limit, slow."""
    (pathlib.Path(TMP) / 'claude').mkdir(parents=True, exist_ok=True)
    (pathlib.Path(TMP) / 'claude' / 'fake_mode').write_text(m)
    if 'b' in globals(): b._claude.update(at=0, ok=False)
fake_mode('logged_out')
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
check('/start again: the help, nothing sent twice', out == [b.help_text()], [o[:60] for o in out])

# on demand
out = say('222', '/brief 1')
check('/brief 1 gives the day before', len(out) == 1 and 'Sun 11 Oct' in out[0], out[0][:80] if out else out)
check('… and the latest brief stays marked as had', subs['222'].get('brief') == latest)
out = say('222', '/alerts')
check('/alerts lists the alerts with next steps', len(out) == 1 and out[0].startswith('<b>Alerts in Egypt') and 'Next step:' in out[0] and b.SITE + '#alerts' in out[0], out[0][:200] if out else out)
out = say('222', 'what are the main complaints?')
check('before Claude is signed in, a question gets the built-in answer, saying so', len(out) == 1 and out[0].startswith('<i>Claude isn’t connected yet') and 'Top complaints' in out[0], out[0][:200] if out else out)
check('… and the help says so too', 'same answers as Ask V7 Pulse on the website' in b.help_text())
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

# questions answered by Claude (the stand-in runs the real tool server and the real dashboard tools)
def wait_jobs(limit=120):
    t = time.time()
    while (b.JOBS or b.WAITING) and time.time() - t < limit:
        b.check_jobs(); time.sleep(0.3)
fake_mode('other_org')
out = say('222', 'what are the main complaints?')
check('signed in with an organization the bot refuses: the built-in answer, saying so', not b.JOBS and len(out) == 1 and out[0].startswith('<i>Claude is signed in with an account the bot doesn’t use'), out[0][:120] if out else out)
check('… and nothing goes to Claude', b._claude['ok'] is False and b._claude['blocked'] is True)
fake_mode('')
check('signed in, the help says Claude answers', 'Claude answers questions' in b.help_text())
n = len(calls); out = say('222', 'how many mentions this month?')
check('the question goes to Claude in the background: nothing yet, "typing…" on', out == [] and len(b.JOBS) == 1, out)
job = b.JOBS[0] if b.JOBS else {}
wait_jobs(); out = said('222', n)
ans = out[0] if out else ''
check('Claude’s answer arrives', len(out) == 1 and 'mentions in' in ans, out)
check('Claude Code ran locked down: no built-in tools, only the dashboard’s tools, its own sign-in, clean environment, outside the project', 'PROBLEMS' not in ans, ans[:300])
check('… with the dashboard’s instructions, the Telegram rules and all 8 tools', 'Tools: 8; dashboard rules: True; Telegram rules: True' in ans, ans[:300])
ov = json.loads(b.dash.run_tool(b.dash.tool_page(), 'get_overview', {}))
check('… and the number comes from the real dashboard tool', '<b>%d</b> mentions' % ov['count'] in ans, (ov['count'], ans[:80]))
check('"typing…" shows while Claude works', any(m == 'sendChatAction' and str(p['chat_id']) == '222' for m, p in calls[n:]))
check('Markdown becomes Telegram text: bullets, sub-points, a table as lines, a heading, steps, a link',
      all(x in ans for x in ('• Tools: 8', '    ◦ a point under it', '<b>Product · Posts</b>', '• V Cola · 12', '<b>Recommended actions</b>',
                             '1. Reply to the <b>12</b> questions', '<a href="https://mohanadabouserie.github.io/v7-pulse/#voice">the dashboard</a>')), ans)
check('… with < and & escaped, and the suggestions as lines', '&lt;today&gt; &amp; tomorrow' in ans and '🔎 <i>Worth a web search:</i> V7 price news (check for a price change)' in ans
      and '📥 <i>New data to collect, needs approval:</i> apify/instagram-scraper · new comments · $0.10' in ans, ans[-400:])
check('… and a link to the dashboard under it', ans.rstrip().endswith('<a href="%s">Open V7 Pulse</a>' % b.SITE))
check('the first question has no earlier turns', '- Earlier turns: False' in html.unescape(ans) or 'Earlier turns: False' in ans)
n = len(calls); say('222', 'and last week?'); say('222', 'and the week before?')
check('two questions from one chat wait their turn', len(b.JOBS) == 1 and len(b.WAITING) == 1, (len(b.JOBS), len(b.WAITING)))
wait_jobs(); out = said('222', n)
check('… both are answered, with the chat so far as context', len(out) == 2 and all('Earlier turns: True' in o for o in out), [o[:60] for o in out])
fake_mode('not_logged_in')
b._claude.update(at=time.time(), ok=True)      # the bot still thinks it's signed in
n = len(calls); say('222', 'what are the main complaints?'); wait_jobs(); out = said('222', n)
check('if the sign-in has gone: the built-in answer, saying Claude couldn’t answer', len(out) == 1 and out[0].startswith('<i>Claude couldn’t answer just now') and 'Top complaints' in out[0], out[0][:150] if out else out)
check('… and the sign-in is checked again before the next question', b._claude['ok'] is False and b._claude['at'] == 0)
fake_mode('limit')
n = len(calls); say('222', 'what are the main complaints?'); wait_jobs(); out = said('222', n)
check('when the plan’s usage limit is reached: the built-in answer, saying so', len(out) == 1 and out[0].startswith('<i>Claude’s usage limit is reached'), out[0][:150] if out else out)
fake_mode('no_opus')
n = len(calls); say('222', 'how many mentions this month?'); wait_jobs(); out = said('222', n)
check('if the plan doesn’t include the model asked for, the question goes again on the plan’s default model', len(out) == 1 and 'mentions in' in out[0] and b._claude['model'] == '', (b._claude['model'], out[0][:80] if out else out))
b._claude['model'] = b.CLAUDE_MODEL
fake_mode('slow'); b.CLAUDE_TIMEOUT = 7
n = len(calls); say('222', 'what are the main complaints?'); proc = b.JOBS[0]['proc'] if b.JOBS else None; wait_jobs(); out = said('222', n)
check('"typing…" is renewed while Claude works', sum(1 for m, p in calls[n:] if m == 'sendChatAction' and str(p['chat_id']) == '222') >= 2)
check('an answer that takes too long is stopped, and the built-in answer goes instead', proc is not None and proc.returncode is not None and len(out) == 1 and out[0].startswith('<i>Claude couldn’t answer just now'), out[0][:150] if out else out)
b.CLAUDE_TIMEOUT = 180; fake_mode(''); keep = b.CLAUDE_PER_DAY; b.CLAUDE_PER_DAY = 0
out = say('222', 'what are the main complaints?')
check('after the day’s questions to Claude: the built-in answer, saying so', len(out) == 1 and out[0].startswith('<i>Today’s 0 questions to Claude are used up'), out[0][:150] if out else out)
b.CLAUDE_PER_DAY = keep

# the tool server on its own (what Claude Code talks to)
srv = subprocess.Popen([sys.executable, str(ROOT / 'bot' / 'claude_tools_mcp.py')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                       env={**os.environ, 'V7_TOOLS_FILE': str(pathlib.Path(TMP) / 'claude_tools.json')})
def rpc(i, method, params=None):
    srv.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': i, 'method': method, 'params': params or {}}) + '\n'); srv.stdin.flush()
    return json.loads(srv.stdout.readline())
r = rpc(1, 'initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}})
check('tool server: the handshake answers the client’s protocol version', r['result']['protocolVersion'] == '2025-06-18' and 'tools' in r['result']['capabilities'], r)
names = [t['name'] for t in rpc(2, 'tools/list')['result']['tools']]
check('… lists the dashboard’s 8 read-only tools', names == ['get_overview', 'search_posts', 'get_breakdown', 'get_our_accounts', 'get_market', 'get_restaurants', 'get_risks_and_events', 'get_outside_egypt'], names)
r = rpc(3, 'tools/call', {'name': 'search_posts', 'arguments': {'query': 'price'}})
check('… runs one in the dashboard and returns its data', not r['result'].get('isError') and json.loads(r['result']['content'][0]['text']), str(r)[:200])
r = rpc(4, 'tools/call', {'name': 'run_shell', 'arguments': {'cmd': 'ls'}})
check('… refuses any other tool', r['result'].get('isError') is True, r)
r = rpc(5, 'resources/list')
check('… and anything else MCP offers', r.get('error', {}).get('code') == -32601, r)
srv.stdin.close(); srv.wait(timeout=60)

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
fake_mode('logged_out'); h1 = b.help_text(); fake_mode(''); h2 = b.help_text()
copy = ' '.join([h1, h2, b.ADMIN_NOTE, b.NOT_MEMBER, b.DESCRIPTION, b.ABOUT, b.TELEGRAM_RULES] + [d for c, d in b.COMMANDS])
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
