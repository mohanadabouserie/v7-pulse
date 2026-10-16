#!/usr/bin/env python3
"""A stand-in for Claude Code (`claude`) for tests/test_bot.py: no account, no network, nothing spent.

`auth status` says it's signed in. `-p` first checks that the bot locked Claude Code down (no built-in tools, only the
v7pulse tool server, the bot's own sign-in folder, a clean environment, a folder outside the project), then runs the
real tool server from --mcp-config, calls get_overview and answers in Markdown with numbers from it.
The file fake_mode in the sign-in folder picks a failure: logged_out, other_org (signed in with an organization
the bot refuses), not_logged_in, limit, slow or no_opus (the plan refuses the model asked for).
"""
import json, os, subprocess, sys, time

args = sys.argv[1:]
home = os.environ.get('CLAUDE_CONFIG_DIR', '')
mode_file = os.path.join(home, 'fake_mode')
mode = open(mode_file).read().strip() if os.path.exists(mode_file) else ''


def out(result, error=False):
    print(json.dumps({'type': 'result', 'subtype': 'success', 'is_error': error, 'result': result, 'num_turns': 2}))
    sys.exit(1 if error else 0)


def opt(name):
    return args[args.index(name) + 1] if name in args else None


if args[:2] == ['auth', 'status']:
    print(json.dumps({'loggedIn': mode != 'logged_out', 'authMethod': 'claude.ai' if mode != 'logged_out' else 'none',
                      **({'email': 'someone@other.example', 'orgName': 'Other Co'} if mode == 'other_org' else {})}))
    sys.exit(0)
if mode == 'slow':
    time.sleep(60)
if mode == 'not_logged_in':
    out('Not logged in · Please run /login', True)
if mode == 'limit':
    out('Claude AI usage limit reached|1760000000', True)
if mode == 'no_opus' and '--model' in args:
    out('There\'s an issue with the selected model (%s). It may not exist or you may not have access to it.' % opt('--model'), True)

problems = []
if '-p' not in args: problems.append('not in print mode')
if opt('--tools') != '': problems.append('built-in tools are on')
if '--strict-mcp-config' not in args: problems.append('other tool servers can load')
if opt('--allowedTools') != 'mcp__v7pulse': problems.append('allowed tools: %s' % opt('--allowedTools'))
servers = json.loads(opt('--mcp-config') or '{}').get('mcpServers', {})
if list(servers) != ['v7pulse']: problems.append('tool servers: %s' % list(servers))
if os.path.basename(home) != 'claude': problems.append('sign-in folder: %s' % home)
leaks = sorted(k for k in os.environ if k not in ('HOME', 'LANG', 'PATH', 'CLAUDE_CONFIG_DIR', 'ANTHROPIC_API_KEY', 'PWD', 'SHLVL', '_'))
if leaks: problems.append('environment carries %s' % leaks)
project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.getcwd().startswith(project): problems.append('runs inside the project folder')
if problems:
    out('PROBLEMS: ' + '; '.join(problems))

prompt, system = sys.stdin.read(), opt('--system-prompt') or ''
srv = servers['v7pulse']
p = subprocess.Popen([srv['command']] + srv.get('args', []), stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                     env={**os.environ, **srv.get('env', {})})


def rpc(i, method, params=None):
    p.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': i, 'method': method, 'params': params or {}}) + '\n'); p.stdin.flush()
    return json.loads(p.stdout.readline())


rpc(1, 'initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'fake', 'version': '0'}})
p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n'); p.stdin.flush()
tools = [t['name'] for t in rpc(2, 'tools/list')['result']['tools']]
ov = json.loads(rpc(3, 'tools/call', {'name': 'get_overview', 'arguments': {}})['result']['content'][0]['text'])
p.stdin.close(); p.wait(timeout=60)
out('\n'.join([
    '**%d** mentions in %s, from get_overview.' % (ov['count'], ov['period']),
    '- Tools: %d; dashboard rules: %s; Telegram rules: %s' % (len(tools), 'V7 Pulse' in system, 'ON TELEGRAM' in system),
    '- Earlier turns: %s' % ('Earlier in this Telegram chat' in prompt),
    '  - a point under it',
    '| Product | **Posts** |', '|---|---|', '| V Cola | 12 |',
    '### Recommended actions', '1. Reply to the **12** questions about price <today> & tomorrow',
    'See [the dashboard](https://mohanadabouserie.github.io/v7-pulse/#voice).',
    '[[web: V7 price news | check for a price change]]', '[[apify: apify/instagram-scraper | new comments | $0.10]]']))
