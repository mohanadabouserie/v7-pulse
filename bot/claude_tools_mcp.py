"""The dashboard's eight read-only Claude tools (get_overview, search_posts, …) as an MCP server on stdio.

The Telegram bot starts Claude Code with this as its only tool server, so Claude answers from the same data and the
same tools as Ask V7 Pulse on claude.ai. The tools run in a headless copy of the dashboard, which loads on the first
call. Their names and descriptions come from V7_TOOLS_FILE (written by the bot), so the handshake is instant.
Every tool only reads the page's data; nothing here writes anything or reaches the internet.
"""
import json, os, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dashboard_reader as dash

TOOLS = json.load(open(os.environ['V7_TOOLS_FILE'], encoding='utf-8'))
NAMES = {t['name'] for t in TOOLS}
page = None


def reply(mid, result=None, error=None):
    msg = {'jsonrpc': '2.0', 'id': mid}
    if error:
        msg['error'] = error
    else:
        msg['result'] = result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + '\n')
    sys.stdout.flush()


def text(t, error=False):
    return {'content': [{'type': 'text', 'text': t}], 'isError': error}


def call(name, args):
    global page
    if page is None:
        page = dash.tool_page()
    return dash.run_tool(page, name, args)


def main():
    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        mid, method, params = msg.get('id'), msg.get('method'), msg.get('params') or {}
        if mid is None:   # a notification, such as notifications/initialized
            continue
        if method == 'initialize':
            reply(mid, {'protocolVersion': params.get('protocolVersion', '2025-06-18'), 'capabilities': {'tools': {}},
                        'serverInfo': {'name': 'v7pulse', 'version': '1.0'}})
        elif method == 'tools/list':
            reply(mid, {'tools': TOOLS})
        elif method == 'tools/call':
            name = params.get('name')
            if name not in NAMES:
                reply(mid, text('No tool called %s.' % name, True)); continue
            try:
                reply(mid, text(call(name, params.get('arguments') or {})))
            except Exception as e:
                reply(mid, text('The dashboard could not run %s: %s' % (name, e), True))
        elif method == 'ping':
            reply(mid, {})
        else:
            reply(mid, error={'code': -32601, 'message': 'Method not found: %s' % method})
    dash.close()


if __name__ == '__main__':
    main()
