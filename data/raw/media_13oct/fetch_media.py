"""15 Oct 2026 (Version 23): the cover image of every real post the dashboard shows, so posts can be seen, not only linked.
Sources: the 13 Oct pulls (../verify_13oct, ../own_backfill_13oct). Facebook and Instagram give an image link with the post
(valid for a few days); TikTok covers expire within hours, so a fresh link is read from each video's public page;
YouTube thumbnails come from i.ytimg.com. One request at a time, 1 second apart. Each image is shrunk to 360 px on its long
side (JPEG quality 55, about 10-20 KB) and saved in img/; index.json maps each post's link to its file.
Usage: python3 fetch_media.py"""
import hashlib, io, json, os, re, socket, time, urllib.parse, urllib.request
from PIL import Image
_gai = socket.getaddrinfo   # this network often can't reach IPv6 addresses: use IPv4 only
def _v4_first(*a, **k):   # this network often can't reach IPv6: use IPv4 when the host has it, otherwise whatever it has
    rs = _gai(*a, **k); v4 = [r for r in rs if r[0] == socket.AF_INET]
    return v4 or rs
socket.getaddrinfo = _v4_first
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.join(HERE, '..', 'verify_13oct'); B = os.path.join(HERE, '..', 'own_backfill_13oct')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}
def load(folder, name):
    p = os.path.join(folder, name); return json.load(open(p, encoding='utf-8'))['items'] if os.path.exists(p) else []
want = {}   # post link -> (image link or None, kind, platform)
for x in load(V, 'fb_page.json') + load(B, 'fb_backfill.json') + load(B, 'fb_test.json'):
    m = (x.get('media') or [{}])[0] if x.get('media') else {}
    u = m.get('thumbnail') or (m.get('photo_image') or {}).get('uri') or (m.get('image') or {}).get('uri')
    want.setdefault(x['url'], (u, 'video' if '/reel/' in x['url'] or x.get('isVideo') else 'image', 'fb'))
for p in load(V, 'ig_profiles.json'):
    for x in p['latestPosts']:
        want.setdefault(x['url'], (x.get('displayUrl'), {'Video': 'video', 'Sidecar': 'carousel'}.get(x['type'], 'image'), 'ig'))
for x in load(B, 'ig_backfill.json'):
    want.setdefault(x['url'], (x.get('displayUrl'), {'Video': 'video', 'Sidecar': 'carousel'}.get(x['type'], 'image'), 'ig'))
for x in load(V, 'tt_profile10.json') + load(B, 'tt_backfill.json') + load(B, 'tt_test.json'):
    want.setdefault(x['webVideoUrl'], (None, 'video', 'tt'))
for x in load(V, 'yt_videos.json') + load(B, 'yt_backfill.json'):
    vid = re.search(r'(?:v=|shorts/)([\w-]{11})', x['url']).group(1)
    want.setdefault(x['url'], ('https://i.ytimg.com/vi/%s/hqdefault.jpg' % vid, 'video', 'yt'))
idx_path = os.path.join(HERE, 'index.json')
idx = json.load(open(idx_path, encoding='utf-8')) if os.path.exists(idx_path) else {}
def get(u, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read()
done = fail = 0
for post, (img, kind, pl) in want.items():
    if post in idx and 'file' in idx[post]: continue   # retries earlier failures
    try:
        if pl == 'tt':   # TikTok's oEmbed service doesn't answer from here; the video page carries a fresh cover link
            page = get(post).decode('utf-8', 'replace'); m = re.search(r'"(?:cover|originCover)":"(https:[^"]+)"', page)
            img = json.loads('"' + m.group(1) + '"') if m else None; time.sleep(1)
        if not img: raise ValueError('no image link')
        im = Image.open(io.BytesIO(get(img))).convert('RGB'); w, h = im.size
        if pl == 'yt' and h and abs(w / h - 4 / 3) < .05:   # YouTube pads 16:9 frames to 4:3 with black bars
            im = im.crop((0, int(h * .125), w, int(h * .875))); w, h = im.size
        im.thumbnail((360, 360)); out = io.BytesIO(); im.save(out, 'JPEG', quality=55, optimize=True, progressive=True)
        name = hashlib.sha1(post.encode()).hexdigest()[:12] + '.jpg'
        open(os.path.join(HERE, 'img', name), 'wb').write(out.getvalue())
        idx[post] = {'file': name, 'w': im.size[0], 'h': im.size[1], 'kind': kind, 'pl': pl, 'bytes': len(out.getvalue())}; done += 1
    except Exception as e:
        idx[post] = {'error': str(e)[:120], 'pl': pl}; fail += 1
    json.dump(idx, open(idx_path, 'w', encoding='utf-8'), indent=1)
    time.sleep(1)
ok = [v for v in idx.values() if 'file' in v]
print(f'{done} saved now, {fail} failed; {len(ok)} images in all, {sum(v["bytes"] for v in ok)/1024:.0f} KB')
