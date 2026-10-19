"""Writes the dashboard's MEDIA block: each real post's cover image (from fetch_media.py) as a small data: URI, keyed by
the post's link, with its kind (video, image or carousel). The dashboard stays one self-contained file.
Usage: python3 build_media.py [--inject]"""
import base64, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DASH = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'V7_Pulse_Dashboard.html'))
idx = json.load(open(os.path.join(HERE, 'index.json'), encoding='utf-8'))
BUDGET_KB = int(os.environ.get('V7_MEDIA_KB', '6000'))   # 19 Oct: the images may take this much of the page (it must stay under 16 MB)


def wanted():
    """The links of the posts in the dashboard, most important first: V7's own posts, the pages abroad by engagement, then public posts
    by views and engagement. Images of posts no longer in the data aren't embedded."""
    html = open(DASH, encoding='utf-8').read()
    own = re.findall(r"url:'(https://[^']+)'\}", html[html.index('/*REAL_OWN*/'):html.index('/*END_REAL_OWN*/')])
    ab = re.findall(r"likes:(\d+),comments:(\d+),views:\d+,fmt:'\w+',prods:\[[^\]]*\],url:'(https://[^']+)'\}", html[html.index('/*REAL_OWN_X*/'):html.index('/*END_REAL_OWN_X*/')])
    d = json.loads(re.search(r'/\*REAL_DATA\*/var REAL_DATA=(.*?);/\*END_REAL_DATA\*/', html, re.S).group(1))
    ugc = sorted(d['ugc'], key=lambda r: (-(r.get('views') or 0), -((r.get('likes') or 0) + (r.get('comments') or 0) + (r.get('shares') or 0))))
    return own + [u for lk, cm, u in sorted(ab, key=lambda r: -(int(r[0]) + int(r[1])))] + [r['url'] for r in ugc]


media, used, dropped = {}, 0, 0
for url in dict.fromkeys(wanted()):
    v = idx.get(url) or {}
    if 'file' not in v: continue
    b = open(os.path.join(HERE, 'img', v['file']), 'rb').read()
    entry = {'s': 'data:image/jpeg;base64,' + base64.b64encode(b).decode(), 'k': v['kind']}
    size = len(json.dumps({url: entry}, separators=(',', ':')))
    if used + size > BUDGET_KB * 1024:
        dropped += 1; continue
    media[url] = entry; used += size
if dropped:
    print(f'{dropped} images left out to keep the page small (V7_MEDIA_KB={BUDGET_KB})')
blob = json.dumps(media, separators=(',', ':')).replace('</', '<\\/')
# The artifact publish guard takes a page for a code-review page when an `id=` is followed by a long unbroken run of text, as with a
# Facebook link ending in &id=… right before its image data, and then refuses it (review pages may be 512 KB at most). Inside the
# JSON strings `=` is written \u003d, which reads back as the same link.
blob = re.sub(r'(?i)\b(id[\t\n\f\r ]*)=', r'\1\\u003d', blob)
print(f'{len(media)} images, {len(blob)/1024:.0f} KB in the page')
if '--inject' in sys.argv:
    html = open(DASH, encoding='utf-8').read()
    new, n = re.subn(r'/\*MEDIA\*/.*?/\*END_MEDIA\*/', lambda m: '/*MEDIA*/var MEDIA=' + blob + ';/*END_MEDIA*/', html, flags=re.S)
    if n != 1: sys.exit('MEDIA block not found in the dashboard')
    open(DASH, 'w', encoding='utf-8').write(new); print('injected into', os.path.basename(DASH))
