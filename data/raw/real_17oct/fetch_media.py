"""17 Oct 2026 (Version 25), widened 18 Oct (Version 26): cover images for the real posts that have none yet, so they can be seen, not only linked.
Which: every post in the dashboard without one (V7 Egypt, the pages abroad, then the public posts about V7 by views; until 21 Oct only
the top 40 abroad and top 80 public posts). Image links come from the 17 Oct pulls in raw/ (Facebook, Instagram and X give one with the post;
TikTok covers expire within hours, so a fresh link is read from each video's public page; YouTube thumbnails come from i.ytimg.com).
One request at a time, 1 second apart. Each image is shrunk to 640 px on its long side (JPEG quality 72; 300 px, quality 52 until 21 Oct) and saved, like the 13 Oct ones,
in ../media_13oct/img/ with ../media_13oct/index.json, which ../media_13oct/build_media.py --inject turns into the MEDIA block.
Usage: python3 fetch_media.py"""
import hashlib, io, json, os, pathlib, re, socket, time, urllib.request
from PIL import Image
_gai = socket.getaddrinfo
def _v4_first(*a, **k):   # this network often can't reach IPv6: use IPv4 when the host has it
    rs = _gai(*a, **k); v4 = [r for r in rs if r[0] == socket.AF_INET]
    return v4 or rs
socket.getaddrinfo = _v4_first
HERE = pathlib.Path(__file__).resolve().parent
MED = HERE.parent / 'media_13oct'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}
raw = lambda n: json.load(open(HERE / 'raw' / (n + '.json'), encoding='utf-8'))['items'] if (HERE / 'raw' / (n + '.json')).exists() else []
idx_path = MED / 'index.json'
idx = json.load(open(idx_path, encoding='utf-8'))
have = {u for u, v in idx.items() if 'file' in v}
data = json.load(open(HERE / 'real_dashboard.json', encoding='utf-8'))
dash = (HERE.parents[2] / 'V7_Pulse_Dashboard.html').read_text(encoding='utf-8')
own_urls = re.findall(r"url:'(https://[^']+)'\}", dash[dash.index('/*REAL_OWN*/'):dash.index('/*END_REAL_OWN*/')])
x_rows = re.findall(r"likes:(\d+),comments:(\d+),views:\d+,fmt:'\w+',prods:\[[^\]]*\],url:'(https://[^']+)'\}", dash[dash.index('/*REAL_OWN_X*/'):dash.index('/*END_REAL_OWN_X*/')])

img_of = {}    # post link -> (image link or None, kind, platform)
for x in raw('fb_posts'):
    m = (x.get('media') or [{}])[0] if x.get('media') else {}
    img_of[x['url']] = (m.get('thumbnail') or (m.get('photo_image') or {}).get('uri') or (m.get('image') or {}).get('uri'), 'video' if '/reel/' in x['url'] or x.get('isVideo') else 'image', 'fb')
for name in ('ig_posts', 'abroad_posts', 'ig_tags', 'ig_tags2', 'ig_tagged_v7', 'ig_tagged_v7_full', 'ig_tagged_vss', 'ig_google_posts', 'ig_google2_posts') + tuple(f.stem for f in sorted((HERE / 'raw').glob('vis_posts_*.json'))):
    for x in raw(name):
        if x.get('url'):
            img_of[x['url']] = (x.get('displayUrl'), {'Video': 'video', 'Sidecar': 'carousel'}.get(x.get('type'), 'image'), 'ig')
for f in sorted((HERE / 'raw').glob('igkw_*.json')):   # 19 Oct on: Instagram keyword search with apidojo
    for x in json.load(open(f, encoding='utf-8'))['items']:
        if x.get('url'):
            img_of[x['url']] = ((x.get('image') or {}).get('url'), 'carousel' if x.get('isCarousel') else 'video' if x.get('isVideo') else 'image', 'ig')
for f in sorted((HERE / 'raw').glob('igreels_*.json')):   # 19 Oct on: Instagram's Reels search with dami_studio
    for x in json.load(open(f, encoding='utf-8'))['items']:
        if x.get('reelUrl'):
            img_of[x['reelUrl']] = (x.get('thumbnailUrl'), 'video', 'ig')
for x in raw('ig_kw_wide'):          # 18 Oct: Instagram keyword search (its own field names)
    if x.get('url'):
        img_of[x['url']] = (x.get('displayUrl'), {'reel': 'video', 'video': 'video', 'carousel': 'carousel'}.get(x.get('type'), 'image'), 'ig')
for name in ('tt_posts', 'tt_search', 'tt_google_posts', 'tt_tags_wide', 'tt_wide'):
    for x in raw(name):
        if x.get('webVideoUrl'):
            img_of[x['webVideoUrl']] = (None, 'video', 'tt')
for name in ('yt_posts', 'yt_search', 'yt_recent'):
    for x in raw(name):
        vid = re.search(r'(?:v=|shorts/)([\w-]{11})', x.get('url') or '')
        if vid: img_of[x['url']] = ('https://i.ytimg.com/vi/%s/hqdefault.jpg' % vid.group(1), 'video', 'yt')
for f in sorted((HERE / 'raw').glob('x_*.json')):
    for t in json.load(open(f, encoding='utf-8'))['items']:
        med = ((t.get('extendedEntities') or {}).get('media') or [{}])[0]
        if t.get('url') and med.get('media_url_https'):
            img_of[t['url']] = (med['media_url_https'], 'video' if med.get('type') in ('video', 'animated_gif') else 'image', 'x')
for f in sorted((HERE / 'raw').glob('fb_search_*.json')):
    for p in json.load(open(f, encoding='utf-8'))['items']:
        att = [a for a in p.get('attachments') or [] if isinstance(a, dict) and a.get('url', '').startswith('https://scontent')]
        if att and p.get('url'):
            img_of[p['url']] = (att[0]['url'], 'video' if att[0].get('type') == 'video' else 'image', 'fb')

for it in json.load(open(HERE / 'items.json', encoding='utf-8'))['items']:   # 19 Oct on: Facebook from every route (normalize.py keeps each post's media links)
    m = it.get('media') or {}
    if it['pl'] == 'fb' and it['src'] == 'ugc' and it['kind'] == 'post' and (m.get('cover') or m.get('images')):
        k = 'video' if it.get('fmt') in ('Reel', 'Video') else 'carousel' if it.get('fmt') == 'Album' else 'image'
        for u in [it['url']] + it.get('urls', []):
            if u not in img_of or not img_of[u][0]:
                img_of[u] = (m.get('cover') or m['images'][0], k, 'fb')

want = [u for u in own_urls if u not in have]
want += [u for lk, cm, u in sorted(x_rows, key=lambda r: -(int(r[0]) + int(r[1]))) if u not in have]
ugc = sorted(data['ugc'], key=lambda r: (-(r.get('views') or 0), -(r.get('likes', 0) + r.get('comments', 0) + r.get('shares', 0))))   # zero counts are left out of the data
want += [r['url'] for r in ugc if r['url'] not in have and r['url'] in img_of]   # 21 Oct: every post, no top-80 limit (DECISIONS #170)
print(len(want), 'images to fetch')

def get(u, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read()
done = fail = 0
for post in want:
    img, kind, pl = img_of.get(post, (None, 'image', '?'))
    try:
        if pl == 'tt':   # a fresh cover link from the video's page
            page = get(post).decode('utf-8', 'replace'); m = re.search(r'"(?:cover|originCover)":"(https:[^"]+)"', page)
            img = json.loads('"' + m.group(1) + '"') if m else None; time.sleep(1)
        if not img: raise ValueError('no image link')
        im = Image.open(io.BytesIO(get(img))).convert('RGB'); w, h = im.size
        if pl == 'yt' and h and abs(w / h - 4 / 3) < .05:   # YouTube pads 16:9 frames to 4:3 with black bars
            im = im.crop((0, int(h * .125), w, int(h * .875)))
        im.thumbnail((640, 640)); out = io.BytesIO(); im.save(out, 'JPEG', quality=72, optimize=True, progressive=True)   # 21 Oct: 300 px / q52 until the images left the page (DECISIONS #172)
        name = hashlib.sha1(post.encode()).hexdigest()[:12] + '.jpg'
        (MED / 'img' / name).write_bytes(out.getvalue())
        idx[post] = {'file': name, 'w': im.size[0], 'h': im.size[1], 'kind': kind, 'pl': pl, 'bytes': len(out.getvalue()), 'added': '2026-10-17'}; done += 1
    except Exception as e:
        idx[post] = {'error': str(e)[:120], 'pl': pl}; fail += 1
    json.dump(idx, open(idx_path, 'w', encoding='utf-8'), indent=1)
    time.sleep(1)
ok = [v for v in idx.values() if 'file' in v]
print(f'{done} saved now, {fail} failed; {len(ok)} images in all, {sum(v["bytes"] for v in ok)/1024:.0f} KB')
