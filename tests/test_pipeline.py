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
    'apify~facebook-posts-scraper': {'facebookUrl': 'https://www.facebook.com/shop/posts/pfbid0ABC', 'url': 'https://www.facebook.com/shop/posts/pfbid0XYZ',
                                     'media': [{'__typename': 'Photo', 'id': '1'}, {'__typename': 'Video', 'id': '777000111'}]},
    'apify~instagram-post-scraper': {'shortCode': 'ABC123', 'url': 'https://www.instagram.com/p/ABC123/', 'displayUrl': 'https://scontent.cdninstagram.com/new.jpg',
                                     'videoUrl': 'https://scontent.cdninstagram.com/new.mp4'},
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
P.HERE = C.RAW.parent   # the reports read this run's files, not the real collection's
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
share = {'id': 'fb:1', 'url': 'https://www.facebook.com/x/posts/1', 'date': '2026-10-13T12:00:00Z', 'comments': 2, 'is_share': True, 'pl': 'fb', 'kind': 'post', 'src': 'ugc', 'fmt': 'Video'}
plain = {'id': 'fb:2', 'url': 'https://www.facebook.com/y/posts/2', 'date': '2026-10-01T12:00:00Z', 'comments': 3, 'pl': 'fb', 'kind': 'post', 'src': 'ugc'}
odd = {'id': 'fb:3', 'url': 'https://www.facebook.com/z/posts/3', 'date': '2026-10-12T12:00:00Z', 'comments': 4, 'pl': 'fb', 'kind': 'post', 'src': 'ugc'}
out = {'reason': [K.reason(share, ['2026-10-14T00:00:00Z'], 'thedoor'), K.reason(share, ['2026-10-14T00:00:00Z'], 'apify'),
                  K.reason(odd, ['2026-10-10T09:00:00Z', '2026-10-12T13:00:00Z'], 'apify'), K.reason(plain, ['2026-10-02T00:00:00Z'] * 60, 'apify'),
                  K.reason(plain, ['2026-10-02T00:00:00Z'] * 3 + [1791000000], 'thedoor')]}
# the cheap scraper is never asked for a share's comments
orig = {'id': 'fb:8', 'url': 'https://www.facebook.com/reel/88888888/', 'date': '2026-10-10T12:00:00Z', 'comments': 0, 'pl': 'fb', 'kind': 'post', 'src': 'ugc',
        'fmt': 'Reel', 'text': '😂', 'found_by': ['fbd_posts_shared_t']}
C._fb_public = lambda: ([share, plain, odd, orig], dict({p['id']: {'about': True} for p in (share, plain, odd)}, **{'fb:8': {'about': False}}))
sent = []
C.parallel = lambda todo, line: sent.extend(todo)
C.stage_fbfill()
out['door_asked'] = [u for name, actor, inp, cap, n in sent if 'thedoor' in actor for u in inp['postUrls']]
out['speech_asked'] = [u for name, actor, inp, cap, n in sent if 'transcriber' in actor for u in inp['video_urls']]
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
check('a share’s video is never sent for speech; a post fetched because it was shared is, even when its first label says not about V7 (DECISIONS #188, #190)',
      s.get('speech_asked', []) == ['https://www.facebook.com/reel/88888888/'], s.get('speech_asked'))
check('shares are never sent to thedoor', s.get('door_asked') == ['https://www.facebook.com/y/posts/2', 'https://www.facebook.com/z/posts/3'], s.get('door_asked'))
check('Apify’s own scraper is asked for the share and for the post whose thedoor comments were rejected, not for the one whose comments fit',
      s.get('official_asked') == [['apify~facebook-comments-scraper', ['https://www.facebook.com/x/posts/1', 'https://www.facebook.com/z/posts/3']]], s.get('official_asked'))
check('normalize keeps the comments that fit and lists the rest', s.get('kept') == ['fb:2'] and s.get('rejected') == ['fb:1', 'fb:3'], (s.get('kept'), s.get('rejected')))
check('the run report names the rejected posts', s.get('problems') and 'rejected as not their post' in s['problems'][0] and 'fb:1' in s['problems'][0], s.get('problems'))
# 25 Oct (DECISIONS #179): the posts that shares point to are fetched by link when the collection doesn't have them, once
ORIGINS = r'''
import json
import collect as C
have = {'id': 'fb:9', 'url': 'https://www.facebook.com/page/posts/9', 'pl': 'fb'}
s1 = {'id': 'fb:1', 'url': 'https://www.facebook.com/a/posts/1', 'is_share': True, 'shared_url': 'https://www.facebook.com/page/posts/9', 'shared_id': '9'}
s2 = {'id': 'fb:2', 'url': 'https://www.facebook.com/b/posts/2', 'is_share': True, 'shared_url': 'https://www.facebook.com/other/posts/7', 'shared_id': '7'}
s3 = {'id': 'fb:3', 'url': 'https://www.facebook.com/c/posts/3', 'is_share': True, 'shared_url': 'https://www.facebook.com/off/posts/5', 'shared_id': '5'}
s4 = {'id': 'fb:4', 'url': 'https://www.facebook.com/d/posts/4', 'is_share': True, 'shared_url': 'https://www.facebook.com/new/posts/6', 'shared_id': '6'}
labels = {'fb:1': {'about': True}, 'fb:2': {'about': True}, 'fb:3': {'about': False}, 'fb:4': {'about': False}}
import pathlib; C.HERE = pathlib.Path(C.RAW).parent
json.dump({'posts': ['fb:9', 'fb:1', 'fb:2', 'fb:3']}, open(C.HERE / 'vis_baseline.json', 'w'))
C._fb_public = lambda: ([have, s1, s2, s3, s4], labels)
asked = []
C.run = lambda name, actor, inp, *a, **k: asked.append((name.rsplit('_', 1)[0], actor, [x['url'] for x in inp['direct_urls']]))
C.stage_fbshareorigins()
json.dump({'input': {'direct_urls': [{'url': 'https://www.facebook.com/new/posts/6'}, {'url': 'https://www.facebook.com/other/posts/7'}]}, 'items': []}, open(C.RAW / 'fbd_posts_shared_t.json', 'w'))
C.stage_fbshareorigins()
print('ORIGINS ' + json.dumps(asked))
'''
code, led, rep, out, files = scenario({}, [], code=ORIGINS)
o = json.loads(out.split('ORIGINS ', 1)[1].splitlines()[0]) if 'ORIGINS ' in out else None
check('a share’s original post is fetched by link when the collection lacks it: for every new share (DECISIONS #187), for an older one only when about V7; not when it’s already in, and only once',
      o == [['fbd_posts_shared', 'danek~facebook-posts-fast', ['https://www.facebook.com/new/posts/6', 'https://www.facebook.com/other/posts/7']]], (o, out[-300:]))
# 26 Oct (DECISIONS #192): the videos inside a post link get speech through each video's own link
INNER = r"""
import json
import collect as C
p = {'id': 'fb:5', 'url': 'https://www.facebook.com/shop/posts/pfbid0ABC', 'fmt': 'Video', 'pl': 'fb', 'kind': 'post', 'src': 'ugc', 'found_by': ['x']}
r = {'id': 'fb:6', 'url': 'https://www.facebook.com/reel/123456789/', 'fmt': 'Reel', 'pl': 'fb', 'kind': 'post', 'src': 'ugc', 'found_by': ['x']}
sh = dict(p, id='fb:7', url='https://www.facebook.com/x/posts/pfbid0SH', is_share=True)
C._fb_public = lambda: ([p, r, sh], {'fb:5': {'about': True}, 'fb:6': {'about': True}, 'fb:7': {'about': True}})
asked = []
real = C.run
def fake(name, actor, inp, *a, **k):
    asked.append((actor, inp)); return real(name, actor, inp, *a, **k)
C.run = fake
C.stage_fbinner()
C.stage_fbinner()
m = json.load(open(next(C.RAW.glob('fbinner_*.json'))))['items']
print('INNER ' + json.dumps({'asked': [(a, i.get('startUrls') or i.get('video_urls')) for a, i in asked], 'map': m}))
"""
code, led, rep, out, files = scenario({}, [], code=INNER)
n = json.loads(out.split('INNER ', 1)[1].splitlines()[0]) if 'INNER ' in out else {}
check('a post link holding a video: Apify’s posts scraper finds the video, its own link goes for speech, once; not a reel link, not a share (DECISIONS #192)',
      n.get('asked') == [['apify~facebook-posts-scraper', [{'url': 'https://www.facebook.com/shop/posts/pfbid0ABC'}]], ['invideoiq~video-transcriber', ['https://www.facebook.com/watch/?v=777000111']]]
      and n.get('map') == [{'post': 'https://www.facebook.com/shop/posts/pfbid0ABC', 'videos': ['https://www.facebook.com/watch/?v=777000111']}], (n, out[-300:]))
# 26 Oct (DECISIONS #184): the second check drops a new post with no V7 in its pictures, speech or caption by name
CHECK2 = r'''
import json
import label as L
L.HERE = __import__('pathlib').Path(__import__('collect').RAW).parent
json.dump({'posts': ['fb:old']}, open(L.HERE / 'vis_baseline.json', 'w'))
P = lambda i, **k: dict({'id': i, 'kind': 'post', 'src': 'ugc', 'pl': 'fb', 'text': ''}, **k)
items = {'fb:flavour': P('fb:flavour', text='البينك ليمونيد بيليق مع الفول؟', seen={'v7_visible': False, 'text': ''}),
         'fb:can': P('fb:can', text='cold drinks', seen={'v7_visible': True}),
         'fb:speech': P('fb:speech', text='review', speech='دي سفن كريم صودا بسعر 15'),
         'fb:caption': P('fb:caption', text='Buffalo combo with V Cola', seen={'v7_visible': False}),
         'fb:nopics': P('fb:nopics', text='Pink Lemonade'),
         'fb:old': P('fb:old', text='Pink Lemonade', seen={'v7_visible': False}),
         'fb:o1': P('fb:o1', text='Pink Lemonade with fava beans?'), 'fb:o2': P('fb:o2', text='V7 Cream Soda review'),
         'fb:s1': P('fb:s1', text='sugarr ❤️', is_share=True, shared_id='o1'), 'fb:s2': P('fb:s2', text='😍', is_share=True, shared_id='o2'),
         'fb:s3': P('fb:s3', text='my V7 favourite', is_share=True, shared_id='o1'),
         'fb:txt': P('fb:txt', text='Pink Lemonade is the best', fmt='Text'), 'x:vcola': P('x:vcola', pl='x', text='ڤي كولا احسن من بيبسي', fmt='Text')}
labels = {k: {'about': True} for k in items}
labels['fb:o1'] = {'about': False}
n = L.second_check(items, labels)
print('CHECK2 ' + json.dumps({'n': n, 'about': {k: v['about'] for k, v in labels.items()}}))
'''
code, led, rep, out, files = scenario({}, [], code=CHECK2)
c = json.loads(out.split('CHECK2 ', 1)[1].splitlines()[0]) if 'CHECK2 ' in out else {}
check('the second check drops a new post with only a flavour name; keeps a V7 can, V7 in the speech, V7 named in the caption, a post not yet checked and an old post',
      {k: c.get('about', {}).get(k) for k in ('fb:flavour', 'fb:can', 'fb:speech', 'fb:caption', 'fb:nopics', 'fb:old')}
      == {'fb:flavour': False, 'fb:can': True, 'fb:speech': True, 'fb:caption': True, 'fb:nopics': True, 'fb:old': True}, (c, out[-300:]))
check('a text post naming only a flavour is dropped at once; one naming V Cola stays (DECISIONS #186)',
      {k: c.get('about', {}).get(k) for k in ('fb:txt', 'x:vcola')} == {'fb:txt': False, 'x:vcola': True}, c.get('about'))
check('a new share follows the post it shares: dropped when that post isn’t about V7, kept when it is, kept when the sharer names V7 (DECISIONS #185)',
      {k: c.get('about', {}).get(k) for k in ('fb:s1', 'fb:s2', 'fb:s3')} == {'fb:s1': False, 'fb:s2': True, 'fb:s3': True}, c.get('about'))
# 26 Oct (DECISIONS #181): media files through the platforms' general server names; links that expired are refreshed, at most twice a post
MEDIA = r"""
import http.server, json, threading
import media_links as M
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        code = 403 if 'old' in self.path else 200
        self.send_response(code); self.end_headers()
        if code == 200: self.wfile.write(b'\xff\xd8\xff img')
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d/' % srv.server_address[1]
out = {'ig': M.candidates('https://instagram.fcps4-1.fna.fbcdn.net/v/x.jpg?oe=1'), 'fb': M.candidates('https://scontent-atl3-1.xx.fbcdn.net/v/y.jpg?oe=2'),
       'other': M.candidates('https://i.ytimg.com/vi/z/hq.jpg')}
out['ok'] = M.download(base + 'fresh.jpg', pause=0) == b'\xff\xd8\xff img'
try:
    M.download(base + 'old.jpg', pause=0); out['expired'] = False
except M.Expired:
    out['expired'] = True
post = 'https://www.instagram.com/p/ABC123/'
out['reuse'] = [M.refresh([(post, 'ig')], 0.5).get(post, {}).get('video') for _ in range(3)]
import collect as C
out['runs_after_reuse'] = len(list(C.RAW.glob('vis_posts_refresh_*.json')))
out['refresh'] = [M.refresh([(post, 'ig')], 0.5, reuse_days=0).get(post, {}).get('video') for _ in range(2)]
print('MEDIA ' + json.dumps(out))
"""
code, led, rep, out, files = scenario({}, [], code=MEDIA)
m = json.loads(out.split('MEDIA ', 1)[1].splitlines()[0]) if 'MEDIA ' in out else {}
check('media links: the general server name first, then the link as given; other hosts untouched',
      m.get('ig') == ['https://scontent.cdninstagram.com/v/x.jpg?oe=1', 'https://instagram.fcps4-1.fna.fbcdn.net/v/x.jpg?oe=1']
      and m.get('fb') == ['https://scontent.xx.fbcdn.net/v/y.jpg?oe=2', 'https://scontent-atl3-1.xx.fbcdn.net/v/y.jpg?oe=2']
      and m.get('other') == ['https://i.ytimg.com/vi/z/hq.jpg'], (m, out[-300:]))
check('a refused link is reported as expired; a working one downloads', m.get('ok') is True and m.get('expired') is True, m)
check('fresh links fetched in the last 2 days are reused, not paid for again', m.get('reuse') == ['https://scontent.cdninstagram.com/new.mp4'] * 3 and m.get('runs_after_reuse') == 1, m)
check('without a reusable result, a post is asked for fresh links at most twice', m.get('refresh') == ['https://scontent.cdninstagram.com/new.mp4', None], m.get('refresh'))
print('FAIL', fails)
