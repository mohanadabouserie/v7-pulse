"""Writes the dashboard's MEDIA block: each real post's cover image (from fetch_media.py), keyed by the post's link, with its kind
(video, image or carousel). Since 21 Oct 2026 (DECISIONS #170) the block links to the image files instead of embedding them, with
no size budget: the paths are relative to the repo root (data/raw/media_13oct/img/…), so the dashboard shows them when opened from
this folder, and deploy/build_sites.py copies the files next to the published page and rewrites the paths (MEDIA_BASE).
Usage: python3 build_media.py [--inject]"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DASH = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'V7_Pulse_Dashboard.html'))
idx = json.load(open(os.path.join(HERE, 'index.json'), encoding='utf-8'))
IMG_BASE = 'data/raw/media_13oct/img/'   # relative to V7_Pulse_Dashboard.html


def wanted():
    """The links of the posts in the dashboard, most important first: V7's own posts, the pages abroad by engagement, then public posts
    by views and engagement. Images of posts no longer in the data aren't embedded."""
    html = open(DASH, encoding='utf-8').read()
    own = re.findall(r"url:'(https://[^']+)'\}", html[html.index('/*REAL_OWN*/'):html.index('/*END_REAL_OWN*/')])
    ab = re.findall(r"likes:(\d+),comments:(\d+),views:\d+,fmt:'\w+',prods:\[[^\]]*\],url:'(https://[^']+)'\}", html[html.index('/*REAL_OWN_X*/'):html.index('/*END_REAL_OWN_X*/')])
    d = json.loads(re.search(r'/\*REAL_DATA\*/var REAL_DATA=(.*?);/\*END_REAL_DATA\*/', html, re.S).group(1))
    ugc = sorted(d['ugc'], key=lambda r: (-(r.get('views') or 0), -((r.get('likes') or 0) + (r.get('comments') or 0) + (r.get('shares') or 0))))
    return own + [u for lk, cm, u in sorted(ab, key=lambda r: -(int(r[0]) + int(r[1])))] + [r['url'] for r in ugc]


media = {}
for url in dict.fromkeys(wanted()):
    v = idx.get(url) or {}
    if 'file' in v and os.path.exists(os.path.join(HERE, 'img', v['file'])):
        media[url] = {'s': IMG_BASE + v['file'], 'k': v['kind']}
        if v.get('w') and v.get('h'): media[url]['r'] = round(v['w'] / v['h'], 3)   # width / height, so the posts grid can size the card before the image loads
blob = json.dumps(media, separators=(',', ':')).replace('</', '<\\/')
# Post links with &id= are written \u003d inside the JSON strings (read back as the same link); kept from the claude.ai days, and
# tests/test_v25.py checks it.
blob = re.sub(r'(?i)\b(id[\t\n\f\r ]*)=', r'\1\\u003d', blob)
print(f'{len(media)} images, {len(blob)/1024:.0f} KB in the page')
if '--inject' in sys.argv:
    html = open(DASH, encoding='utf-8').read()
    new, n = re.subn(r'/\*MEDIA\*/.*?/\*END_MEDIA\*/', lambda m: '/*MEDIA*/var MEDIA=' + blob + ';/*END_MEDIA*/', html, flags=re.S)
    if n != 1: sys.exit('MEDIA block not found in the dashboard')
    open(DASH, 'w', encoding='utf-8').write(new); print('injected into', os.path.basename(DASH))
