"""Downloading a post's picture or video from Instagram's and Facebook's file servers (26 Oct 2026, DECISIONS #181).

Two problems, both seen on reel Deg3MlyIF6T:
- **Regional servers:** a media link names the file server nearest the scraper that fetched it (Apify's machines abroad), for example
  instagram.fcps4-1.fna.fbcdn.net, and some of those names don't exist from Egypt. The same file is served under the platform's general
  name (scontent.cdninstagram.com, scontent.xx.fbcdn.net), which picks a reachable server: download() tries that first, then the link as
  given. (26 Oct test: fresh Instagram and Facebook links worked under both names.)
- **Expiry:** media links are signed for a few days, then refused (HTTP 403 or 410). download() raises Expired; refresh() asks Apify for
  fresh links by the post's own link, which doesn't expire (Instagram's post scraper, danek's Facebook posts by link; about USD 0.0023 a
  post), at most twice per post, under a spending line. Searches aren't affected: this only changes where a file already found is fetched.
"""
import json, time, urllib.error, urllib.parse, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}
GENERAL_IG, GENERAL_FB = 'scontent.cdninstagram.com', 'scontent.xx.fbcdn.net'
TRIES = 2   # fresh links asked for per post, in all runs


class Expired(Exception):
    """The file server refused the link (expired, or no longer allowed): a fresh link may work."""


def candidates(url):
    """The link under the platform's general server name first, then as given."""
    p = urllib.parse.urlparse(url or '')
    h = (p.hostname or '').lower()
    general = GENERAL_IG if h.endswith('cdninstagram.com') or (h.startswith('instagram.') and h.endswith('fbcdn.net')) else \
        GENERAL_FB if h.endswith('fbcdn.net') else None
    out = [p._replace(netloc=general).geturl()] if general and general != h else []
    return out + [url]


def download(url, timeout=30, pause=1.0):
    """The file's bytes. Raises Expired when every server refused the link, else the last error (unreachable, timeout, …)."""
    refused, last = False, None
    for u in candidates(url):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read()
            time.sleep(pause)
            return b
        except urllib.error.HTTPError as e:
            refused = refused or e.code in (403, 410)
            last = e
        except Exception as e:   # a server name that doesn't resolve here, a timeout, a dropped connection
            last = e
    if refused:
        raise Expired('link refused (expired)')
    raise last or ValueError('no link')


def _asked(raw, prefix):
    """How many times each post link was already sent for fresh media links (the inputs saved with every run)."""
    n = {}
    for f in raw.glob(prefix + '*.json'):
        inp = json.load(open(f, encoding='utf-8')).get('input') or {}
        for u in inp.get('username') or [x.get('url') for x in inp.get('direct_urls') or []]:
            n[u] = n.get(u, 0) + 1
    return n


def _fb_ids(urls):
    """The post ids we know for these Facebook links (items.json: a post's id and every link it was found under)."""
    import pathlib
    p = pathlib.Path(__file__).resolve().parent / 'items.json'
    ids = {}
    if p.exists():
        want = set(urls)
        for it in json.load(open(p, encoding='utf-8'))['items']:
            if it.get('pl') == 'fb' and it.get('kind') == 'post':
                for u in [it.get('url')] + it.get('urls', []):
                    if u in want:
                        ids[u] = it['id'][3:].lstrip('v')
    return ids


def _ig_media(x):
    imgs = x.get('images') or [c.get('displayUrl') for c in x.get('childPosts') or [] if c.get('displayUrl')] or [x.get('displayUrl')]
    return {'cover': x.get('displayUrl'), 'video': x.get('videoUrl'), 'images': [i for i in imgs if i], 'code': x.get('shortCode')}


def _uri(v):
    """A media field that is a link, or an object holding one ({'uri': …} or {'url': …})."""
    return v if isinstance(v, str) and v.startswith('http') else (v.get('uri') or v.get('url')) if isinstance(v, dict) else None


def _fb_media(x):
    album = [a.get('image_file_uri') or a.get('uri') for a in x.get('album_preview') or [] if isinstance(a, dict)]
    vf = x.get('video_files') if isinstance(x.get('video_files'), dict) else {}
    reps = [r.get('base_url') or r.get('url') for r in x.get('representations') or [] if isinstance(r, dict) and 'video' in str(r.get('mime_type', 'video'))]
    video = vf.get('video_sd_file') or (x.get('video') if isinstance(x.get('video'), str) and x['video'].startswith('http') else None) or (reps[0] if reps else None)
    image = _uri(x.get('image'))   # 26 Oct: often {'uri': …}
    return {'cover': _uri(x.get('video_thumbnail')) or _uri(x.get('thumbnail_uri')) or image,
            'video': video, 'images': [i for i in ([image] if image else []) + album if i]}


def _match(rows, ig, fb, fb_ids):
    """Fresh media for the asked links, from scraper rows. Instagram rows by shortcode; Facebook rows by link, post id or video id
    (26 Oct: a pfbid link holds no number, so the post id comes from items.json)."""
    out = {}
    for x in rows:
        code = x.get('shortCode')
        if code:
            u = next((p for p in ig if code in p), None)
            if u:
                out[u] = _ig_media(x)
            continue
        ids = {str(i) for i in (x.get('post_id'), x.get('video_id')) if i}
        u = next((p for p in fb if p == x.get('url') or fb_ids.get(p) in ids or any(i in p for i in ids)), None)
        if u:
            out[u] = _fb_media(x)
    return out


def refresh(posts, max_usd, reuse_days=2):
    """Fresh media links for posts whose links expired: {post link: {'cover', 'video', 'images'}}. posts: [(post link, 'ig' or 'fb')].
    Rows fetched in the last reuse_days (links last a few days) are used first, at no cost; the rest are asked from Apify, spending at
    most max_usd (collect.py's budget guard); a post already asked for TRIES times is skipped."""
    import collect as C   # needs APIFY_API_TOKEN
    ig = sorted({u for u, pl in posts if pl == 'ig'})
    fb = sorted({u for u, pl in posts if pl == 'fb'})
    fb_ids = _fb_ids(fb)
    saved = []
    for f in list(C.RAW.glob('vis_posts_refresh_*.json')) + list(C.RAW.glob('fbd_posts_refresh_*.json')):
        if time.time() - f.stat().st_mtime < reuse_days * 86400:
            saved += json.load(open(f, encoding='utf-8')).get('items', [])
    out = _match(saved, ig, fb, fb_ids)
    line = C.spent() + max_usd
    tag = time.strftime('%Y%m%d%H%M%S') + '_%06d' % (time.time_ns() // 1000 % 1000000)   # unique: a saved run with the same name would be reused
    ig_n, fb_n = _asked(C.RAW, 'vis_posts_refresh_'), _asked(C.RAW, 'fbd_posts_refresh_')
    ig_ask = [u for u in ig if u not in out and ig_n.get(u, 0) < TRIES]
    fb_ask = [u for u in fb if u not in out and fb_n.get(u, 0) < TRIES]
    if ig_ask:
        rows = C.run('vis_posts_refresh_' + tag, C.IG_POSTS, {"username": ig_ask}, round(len(ig_ask) * 0.0023 * 1.3 + 0.05, 2), len(ig_ask) + 2, budget=line) or []
        out.update(_match(rows, ig_ask, [], {}))
    if fb_ask:
        rows = C.run('fbd_posts_refresh_' + tag, C.FB_POST_LINK, {"direct_urls": [{"url": u} for u in fb_ask]}, round(len(fb_ask) * 0.00233 * 1.3 + 0.05, 2),
                     len(fb_ask) + 2, budget=line) or []
        out.update(_match(rows, [], fb_ask, fb_ids))
    return out
