"""Writes the dashboard's MEDIA block: each real post's cover image (from fetch_media.py) as a small data: URI, keyed by
the post's link, with its kind (video, image or carousel). The dashboard stays one self-contained file.
Usage: python3 build_media.py [--inject]"""
import base64, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DASH = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'V7_Pulse_Dashboard.html'))
idx = json.load(open(os.path.join(HERE, 'index.json'), encoding='utf-8'))
media = {}
for url, v in idx.items():
    if 'file' not in v: continue
    b = open(os.path.join(HERE, 'img', v['file']), 'rb').read()
    media[url] = {'s': 'data:image/jpeg;base64,' + base64.b64encode(b).decode(), 'k': v['kind']}
blob = json.dumps(media, separators=(',', ':')).replace('</', '<\\/')
print(f'{len(media)} images, {len(blob)/1024:.0f} KB in the page')
if '--inject' in sys.argv:
    html = open(DASH, encoding='utf-8').read()
    new, n = re.subn(r'/\*MEDIA\*/.*?/\*END_MEDIA\*/', lambda m: '/*MEDIA*/var MEDIA=' + blob + ';/*END_MEDIA*/', html, flags=re.S)
    if n != 1: sys.exit('MEDIA block not found in the dashboard')
    open(DASH, 'w', encoding='utf-8').write(new); print('injected into', os.path.basename(DASH))
