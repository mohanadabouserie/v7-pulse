"""The refresh pipeline (data/raw/real_17oct/pipeline.py), against a stand-in for Apify's API and one for Telegram: no token, no cost.
It checks that a failed run or a changed output format sends the job to a standby scraper, that Apify's 502s are retried, that the
budget guard skips runs that don't fit, that one run at a time holds, that the admin gets a Telegram message, and that no token is
ever written to a file or printed. It also checks that the gap fillers' runs that don't start (over the budget line, or refused by
Apify) reach the report, and that runs started together can't pass the line between them."""
import http.server, json, os, pathlib, shutil, subprocess, sys, tempfile, threading, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PIPE = ROOT / 'data' / 'raw' / 'real_17oct' / 'pipeline.py'
FAKE_APIFY, FAKE_TG = 'fake-apify-token-31337', '987654:fake-telegram-token-abcdefghijklmnop'
fails = 0


def check(name, ok, info=''):
    global fails
    if not ok: fails += 1
    print(('  ok ' if ok else 'FAIL ') + name + (' :: ' + str(info) if info != '' else ''))


ROWS = {   # one valid row in each scraper's output format
    'silentflow~facebook-search-scraper': {'post_id': '111', 'url': 'https://www.facebook.com/a/posts/111', 'timestamp': 1786817284, 'message': 'V7 soda'},
    'scrapeforge~facebook-search-posts': {'post_id': '112', 'url': 'https://www.facebook.com/a/posts/112', 'timestamp': 1786817284, 'message': 'V7 soda'},
    'topapi~facebook-search-posts-scraper': {'post_id': '113', 'url': 'https://www.facebook.com/a/posts/113', 'timestamp': 1786817284, 'message': 'V7'},
    'scraper_one~facebook-posts-search': {'postId': '221', 'url': 'https://www.facebook.com/b/posts/221', 'timestamp': 1786817284000, 'postText': 'V7'},
    'fetch_cat~facebook-post-search-scraper': {'postId': '222', 'url': 'https://www.facebook.com/b/posts/222', 'timestamp': 1786817284000, 'postText': 'V7'},
}


class Fake:
    behavior, usage, limit, calls, runs, sent, gets502, posts = {}, 1.0, 100.0, [], {}, [], set(), []


class Apify(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def reply(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b))); self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        Fake.calls.append(('GET', path))
        if path == '/v2/users/me/limits':
            return self.reply(200, {'data': {'current': {'monthlyUsageUsd': Fake.usage}, 'limits': {'maxMonthlyUsageUsd': Fake.limit}}})
        if path.startswith('/v2/actor-runs/'):
            rid = path.rsplit('/', 1)[-1]
            r = Fake.runs[rid]
            if Fake.behavior.get(r['actor']) == '502' and rid not in Fake.gets502:
                Fake.gets502.add(rid)
                return self.reply(502, {'error': 'Bad Gateway'})
            return self.reply(200, {'data': {'id': rid, 'status': r['status'], 'defaultDatasetId': 'd' + rid, 'usageTotalUsd': 0.01,
                                             'chargedEventCounts': {}, 'startedAt': '2026-10-19T10:00:00Z', 'finishedAt': '2026-10-19T10:00:05Z'}})
        if path.startswith('/v2/datasets/'):
            rid = path.split('/')[3][1:]
            return self.reply(200, Fake.runs[rid]['items'])
        self.reply(404, {'error': 'not found'})

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        Fake.calls.append(('POST', path))
        n = int(self.headers.get('Content-Length') or 0); self.rfile.read(n)
        if path.startswith('/v2/acts/') and path.endswith('/runs'):
            actor = path.split('/')[3]
            b = Fake.behavior.get(actor, 'ok')
            cap = float((urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('maxTotalChargeUsd') or ['0'])[0])
            Fake.posts.append((actor, cap))
            if b == 'minimum' and cap < 0.5:
                return self.reply(400, {'error': {'type': 'max-total-charge-usd-below-minimum',
                                                  'message': 'Maximum cost per run is less than the allowed minimum of $0.50'}})
            if b == 'refuse':
                return self.reply(403, {'error': {'type': 'actor-is-not-rented', 'message': 'rent it first'}})
            rid = str(len(Fake.runs) + 1)
            row = ROWS.get(actor, {'x': 1})
            items = [] if b in ('fail', 'empty') else [{'foo': 'bar'}, {'foo': 'baz'}] if b == 'bad' else [row]
            Fake.runs[rid] = {'actor': actor, 'status': 'FAILED' if b == 'fail' else 'SUCCEEDED', 'items': items}
            Fake.usage += 0.01
            return self.reply(201, {'data': {'id': rid, 'status': 'RUNNING', 'defaultDatasetId': 'd' + rid}})
        self.reply(404, {'error': 'not found'})


class Telegram(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0)
        body = json.loads(self.rfile.read(n) or b'{}')
        Fake.sent.append((self.path, body))
        b = json.dumps({'ok': True, 'result': {}}).encode()
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b))); self.end_headers()
        self.wfile.write(b)


def serve(handler):
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


apify, tg = serve(Apify), serve(Telegram)


def scenario(behavior, args, usage=1.0, limit=100.0, seed_ledger=None, lock=False, code=None):
    Fake.behavior, Fake.usage, Fake.limit, Fake.calls, Fake.runs, Fake.sent, Fake.gets502, Fake.posts = behavior, usage, limit, [], {}, [], set(), []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='v7pipe-'))
    for d in ('raw', 'state', 'bot'):
        (tmp / d).mkdir()
    (tmp / 'bot' / 'subscribers.json').write_text(json.dumps({'4242': {'role': 'admin', 'name': 'Admin'}, '5151': {'role': 'member'}}))
    if seed_ledger:
        (tmp / 'state' / 'pipeline_ledger.json').write_text(json.dumps(seed_ledger))
    if lock:
        (tmp / 'state' / 'pipeline.lock').write_text(str(os.getpid()))
    env = dict(os.environ, APIFY_API_TOKEN=FAKE_APIFY, APIFY_API_BASE='http://127.0.0.1:%d/v2' % apify.server_address[1], V7_RAW=str(tmp / 'raw'),
               V7_RUNLOG=str(tmp / 'run.log'), V7_PIPELINE_STATE=str(tmp / 'state'), V7_BOT_STATE=str(tmp / 'bot'), V7_POLL='0.02', V7_RETRY_WAIT='0.02',
               V7_TG_API='http://127.0.0.1:%d' % tg.server_address[1], TELEGRAM_BOT_TOKEN=FAKE_TG)
    cmd = [sys.executable, '-c', code] if code else [sys.executable, str(PIPE)] + args
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(PIPE.parent), timeout=300)
    ledger = json.loads((tmp / 'state' / 'pipeline_ledger.json').read_text()) if (tmp / 'state' / 'pipeline_ledger.json').exists() else []
    reports = sorted((tmp / 'state' / 'pipeline_runs').glob('*.json')) if (tmp / 'state' / 'pipeline_runs').exists() else []
    rep = json.loads(reports[-1].read_text()) if reports else {}
    files = ''.join(p.read_text(errors='ignore') for p in tmp.rglob('*') if p.is_file())
    out = r.stdout + r.stderr
    shutil.rmtree(tmp)
    return r.returncode, ledger, rep, out, files


ONE = ['run', '--mode', 'sweep', '--keywords', 'V7 soda', '--no-chain']

code, led, rep, out, files = scenario({}, ONE + ['--jobs', 'fb_posts_sf,fb_posts_one'])
check('healthy runs: both searches succeed on their main scraper', code == 0 and sorted((r['actor'], r['ok']) for r in led) == [('scraper_one', True), ('silentflow', True)], (code, led, out[-300:]))
check('no standby is used when nothing failed', rep.get('standbys') == [] and rep.get('problems') == [], rep.get('problems'))
check('the admin gets a Telegram message, and only the admin', len(Fake.sent) == 1 and Fake.sent[0][1].get('chat_id') == '4242', Fake.sent)
check('the message says everything ran', 'Everything ran without a problem' in (Fake.sent[0][1].get('text') if Fake.sent else ''), Fake.sent[:1])
check('no token is written to any file or printed', FAKE_APIFY not in files + out and FAKE_TG not in files + out)

code, led, rep, out, files = scenario({'silentflow~facebook-search-scraper': 'fail'}, ONE + ['--jobs', 'fb_posts_sf'])
check('a failed run goes to the standby scraper', [(r['actor'], r['status'], r.get('standby_for')) for r in led] == [('silentflow', 'FAILED', None), ('scrapeforge', 'SUCCEEDED', 'silentflow')], led)
check('the report and the message name the standby', rep.get('standbys') and 'scrapeforge' in rep['standbys'][0] and 'Standbys used' in (Fake.sent[0][1]['text'] if Fake.sent else ''), rep.get('standbys'))

code, led, rep, out, files = scenario({'scraper_one~facebook-posts-search': 'bad'}, ONE + ['--jobs', 'fb_posts_one'])
check('rows in a changed format send the job to the standby', [(r['actor'], r['ok']) for r in led] == [('scraper_one', False), ('fetch_cat', True)], led)

code, led, rep, out, files = scenario({'silentflow~facebook-search-scraper': '502'}, ONE + ['--jobs', 'fb_posts_sf'])
check("Apify's 502s are retried, with no standby needed", [(r['actor'], r['ok']) for r in led] == [('silentflow', True)] and not rep.get('errors'), (led, rep.get('errors')))

code, led, rep, out, files = scenario({}, ONE + ['--jobs', 'fb_posts_sf,fb_posts_one'], usage=99.99, limit=100.0)
check('the budget guard skips runs that would pass the limit', all(r['status'] == 'SKIPPED (budget)' for r in led) and not any(c[0] == 'POST' for c in Fake.calls), led)
check('the message reports the runs that did not start', 'Runs not started' in (Fake.sent[0][1]['text'] if Fake.sent else ''), Fake.sent[:1])

seed = [{'job': 'fb_posts_sf', 'actor': 'silentflow', 'rows': 12, 'ok': True, 'status': 'SUCCEEDED', 'name': 'old', 'time': '2026-10-18T09:00:00'}]
code, led, rep, out, files = scenario({'silentflow~facebook-search-scraper': 'empty'}, ONE + ['--jobs', 'fb_posts_sf'], seed_ledger=seed)
check('a job that comes back empty, though it found posts before, is tried on its standby', any(r['actor'] == 'scrapeforge' and r.get('standby_for') == 'silentflow' for r in led[1:]), led)

code, led, rep, out, files = scenario({}, ONE + ['--jobs', 'fb_posts_sf'], lock=True)
check('one run at a time: a held lock stops the second', code == 2 and not Fake.calls, (code, Fake.calls[:3]))

code, led, rep, out, files = scenario({}, ['run', '--mode', 'daily', '--no-chain'])
check("dates past the dashboard's window need --beyond-window", code == 3 and not Fake.calls and 'past the dashboard' in out, (code, out[-200:]))

code, led, rep, out, files = scenario({}, ['plan', '--mode', 'daily'])
check('a plan spends nothing and calls nothing', code == 0 and not Fake.calls and 'about USD' in out, (code, Fake.calls[:3]))
FILL = r'''
import json
import pipeline as P
C = P.C
P.step = lambda rep, label, cmd, timeout=7200: rep['steps'].append({'step': label, 'ok': True}) or True   # no normalize, label or build
C.stage_t_over = lambda: C.parallel([('fbf_speech_t', 'invideoiq~video-transcriber', {'video_urls': []}, 0.9, 1)], C.BUDGET_FB)
C.stage_t_refused = lambda: C.run('fbf_pages_t', 'apify~facebook-pages-scraper', {'startUrls': []}, 0.05, budget=C.BUDGET_FB)
C.stage_t_min = lambda: C.run('fbf_tt_t', 'clockworks~tiktok-scraper', {'postURLs': []}, 0.1, budget=C.BUDGET_FB)
C.stage_t_fine = lambda: C.run('fbf_plays_t', 'social_developer~facebook-playcount-scraper', {'urls': []}, 0.05, budget=C.BUDGET_FB)
P.FILL = ['t_over', 't_refused', 't_min', 't_fine']
class O: no_build = True
rep = {'since': '2026-04-20', 'until': '2026-10-16', 'problems': [], 'steps': [], 'started_ts': 0, 'budget_line': C.spent() + 0.6}
P.chain(O, rep)
print('PROBLEMS ' + json.dumps(rep['problems']))
'''
code, led, rep, out, files = scenario({'apify~facebook-pages-scraper': 'refuse', 'clockworks~tiktok-scraper': 'minimum'}, [], code=FILL)
probs = json.loads(out.split('PROBLEMS ', 1)[1].splitlines()[0]) if 'PROBLEMS ' in out else []
check("the gap fillers' runs that don't start are reported: one over the budget line, one refused by Apify",
      len(probs) == 1 and 'fill steps, 2 runs not started' in probs[0] and 'fbf_speech_t (over the budget line)' in probs[0]
      and 'fbf_pages_t (could not start: HTTP 403)' in probs[0] and 'fbf_plays_t' not in probs[0], (probs, out[-400:]))
check('a run the budget guard skipped is never started, not even with a smaller cap', not any(a == 'invideoiq~video-transcriber' for a, c in Fake.posts), Fake.posts)
check('a scraper that refuses a cap under its minimum is asked again with that minimum',
      [c for a, c in Fake.posts if a == 'clockworks~tiktok-scraper'] == [0.1, 0.5] and 'fbf_tt_t' not in ' '.join(probs), Fake.posts)
check('the gap filler that fitted under the line ran', ('social_developer~facebook-playcount-scraper', 0.05) in Fake.posts, Fake.posts)
PAR = r'''
import json
import collect as C
line = C.spent() + 0.6
C.parallel([('par_a', 'invideoiq~video-transcriber', {'video_urls': []}, 0.4, 1),
            ('par_b', 'social_developer~facebook-playcount-scraper', {'urls': []}, 0.4, 1)], line)
print('SKIPS ' + json.dumps(C.SKIPS))
'''
code, led, rep, out, files = scenario({}, [], code=PAR)
check('runs started together hold their caps: of two USD 0.40 runs under a USD 0.60 line, only one starts',
      len(Fake.posts) == 1 and 'over the budget line' in out and 'held by runs going on' in out, (Fake.posts, out[-300:]))
WIDE = r'''
import json
import collect as C
runs = {'fbp_one_dd_0815_1': {"query": "x", "searchType": "latest", "startDate": "2026-08-15", "endDate": "2026-08-15"},
        'fbc_one_00': {"query": "x", "startDate": "2026-04-20", "endDate": "2026-10-16"},
        'fbc_apify_00': {"categories": ["x"], "searchType": "posts"},
        'fbp_sf_gw_links': {"direct_urls": [{"url": "https://www.facebook.com/a/posts/1"}]},
        'fbp_ap_acct_t1': {"startUrls": [{"url": "https://www.facebook.com/a"}], "resultsLimit": 15}}
for n, inp in runs.items():
    json.dump({'input': inp, 'items': []}, open(C.RAW / (n + '.json'), 'w'))
print('WIDE ' + json.dumps({n: C.wide_search(n) for n in runs}))
'''
code, led, rep, out, files = scenario({}, [], code=WIDE)
w = json.loads(out.split('WIDE ', 1)[1].splitlines()[0]) if 'WIDE ' in out else {}
check('a short video is transcribed only when a keyword search over a long window found it (not a one-day search, a link or an account feed)',
      w == {'fbp_one_dd_0815_1': False, 'fbc_one_00': True, 'fbc_apify_00': True, 'fbp_sf_gw_links': False, 'fbp_ap_acct_t1': False}, (w, out[-300:]))
# 24 Oct (DECISIONS #178): thedoor returned a shared post's comments for the share, and the dashboard showed them under the share
SHARES = r'''
import json, pathlib
import collect as C, comment_check as K, normalize as N, pipeline as P
share = {'id': 'fb:1', 'url': 'https://www.facebook.com/x/posts/1', 'date': '2026-10-13T12:00:00Z', 'comments': 2, 'is_share': True, 'pl': 'fb', 'kind': 'post', 'src': 'ugc'}
plain = {'id': 'fb:2', 'url': 'https://www.facebook.com/y/posts/2', 'date': '2026-10-01T12:00:00Z', 'comments': 3, 'pl': 'fb', 'kind': 'post', 'src': 'ugc'}
odd = {'id': 'fb:3', 'url': 'https://www.facebook.com/z/posts/3', 'date': '2026-10-12T12:00:00Z', 'comments': 4, 'pl': 'fb', 'kind': 'post', 'src': 'ugc'}
out = {'reason': [K.reason(share, ['2026-10-14T00:00:00Z'], 'thedoor'), K.reason(share, ['2026-10-14T00:00:00Z'], 'apify'),
                  K.reason(odd, ['2026-10-10T09:00:00Z', '2026-10-12T13:00:00Z'], 'apify'), K.reason(plain, ['2026-10-02T00:00:00Z'] * 60, 'apify'),
                  K.reason(plain, ['2026-10-02T00:00:00Z'] * 3 + [1791000000], 'thedoor')]}
# the cheap scraper is never asked for a share's comments
C._fb_public = lambda: ([share, plain, odd], {p['id']: {'about': True} for p in (share, plain, odd)})
sent = []
C.parallel = lambda todo, line: sent.extend(todo)
C.stage_fbfill()
out['door_asked'] = [u for name, actor, inp, cap, n in sent if 'thedoor' in actor for u in inp['postUrls']]
# Apify's own scraper gets the share and the post whose thedoor comments are older than it, not the post whose comments fit
row = lambda u, t: {'id': t, 'post_url': u, 'timestamp': t, 'text': 'x', 'author_name': 'a'}
json.dump({'input': {'postUrls': [plain['url'], odd['url']]}, 'items': [row(plain['url'], 1791000000), row(odd['url'], 1791000000)]},
          open(C.RAW / 'fbcm_door_t.json', 'w'))
C._fb_commented = lambda: set()
asked = []
C.run = lambda name, actor, inp, *a, **k: asked.append((actor, sorted(s['url'] for s in inp['startUrls'])))
C.stage_fbfill2()
out['official_asked'] = asked
# normalize keeps only the comments that fit their post, and lists the rest
N.RAW = C.RAW
for p in (share, plain, odd):
    N.ITEMS[p['id']] = dict(p, found_by=['t'])
json.dump({'input': {}, 'items': [row(share['url'], 1781000000), row(plain['url'], 1791000000), row(odd['url'], 1781000000)]}, open(C.RAW / 'fbcm_door_t.json', 'w'))
N.fb_ugc_comments()
out['kept'] = sorted(i['parent'] for i in N.ITEMS.values() if i['kind'] == 'comment')
out['rejected'] = sorted(r['post'] for r in N.REJECTS)
# the pipeline's report names the rejected posts
P.HERE = C.RAW.parent
json.dump({'rejects': N.REJECTS}, open(P.HERE / 'comment_rejects.json', 'w'))
rep = {'problems': [], 'started_ts': 0}
P.report_rejects(rep)
out['problems'] = rep['problems']
print('SHARES ' + json.dumps(out))
'''
code, led, rep, out, files = scenario({}, [], code=SHARES)
s = json.loads(out.split('SHARES ', 1)[1].splitlines()[0]) if 'SHARES ' in out else {}
r = s.get('reason') or [None] * 5
check('a share’s comments from thedoor are rejected; from Apify’s own scraper they are checked like any other', bool(r[0]) and r[1] is None, (r, out[-400:]))
check('comments older than their post are rejected, so are far more than the post shows; comments that fit pass',
      bool(r[2]) and 'older than the post' in r[2] and bool(r[3]) and r[4] is None, r)
check('shares are never sent to thedoor', s.get('door_asked') == ['https://www.facebook.com/y/posts/2', 'https://www.facebook.com/z/posts/3'], s.get('door_asked'))
check('Apify’s own scraper is asked for the share and for the post whose thedoor comments were rejected, not for the one whose comments fit',
      s.get('official_asked') == [['apify~facebook-comments-scraper', ['https://www.facebook.com/x/posts/1', 'https://www.facebook.com/z/posts/3']]], s.get('official_asked'))
check('normalize keeps the comments that fit and lists the rest', s.get('kept') == ['fb:2'] and s.get('rejected') == ['fb:1', 'fb:3'], (s.get('kept'), s.get('rejected')))
check('the run report names the rejected posts', s.get('problems') and 'rejected as not their post' in s['problems'][0] and 'fb:1' in s['problems'][0], s.get('problems'))
print('FAIL', fails)
