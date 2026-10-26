"""19 Oct 2026: downloads the media of Instagram posts (fetched fresh by link with Apify's post scraper) and takes frames from videos,
so the text on them can be read (vis_read.py). Photos: the full-size image of each slide. Videos: a frame every 2 seconds, up to 60 (2 minutes; 12 until 26 Oct),
plus the cover. One request a second. Files go to vis/<shortcode>/ (local only: they're people's media).
Usage: data/.venv/bin/python vis_media.py raw/<post-scraper file>.json [more files]
       data/.venv/bin/python vis_media.py --fb [photos|videos]   (19 Oct: public Facebook posts about V7 that are photos or albums, or videos with little or no
       speech, from the media links their search rows carried; folders vis/fb_<post id>/)
       data/.venv/bin/python vis_media.py --new   (26 Oct: every new public post labelled about V7, on every platform; DECISIONS #183)
       add --refresh-usd N to any of these: links that expired get fresh ones by the post's link (media_links.py), at most USD N"""
import json, pathlib, subprocess, sys, time, urllib.request
import socket
_gai = socket.getaddrinfo
def _v4_first(*a, **k):   # this network often can't reach IPv6 (as in fetch_media.py): use IPv4 when the host has it
    rs = _gai(*a, **k); v4 = [r for r in rs if r[0] == socket.AF_INET]
    return v4 or rs
socket.getaddrinfo = _v4_first
import imageio_ffmpeg
import media_links   # 26 Oct (DECISIONS #181): general server names first, fresh links for expired ones
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'vis'
FF = imageio_ffmpeg.get_ffmpeg_exe()
MAX_FRAMES = 60   # a frame every 2 seconds: the first 2 minutes of a video (26 Oct, DECISIONS #182; until then 12, the first 24 seconds)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}


def get(url, path):
    b = media_links.download(url)
    if path.suffix == '.jpg' and not (b[:3] == b'\xff\xd8\xff' or b[:8] == b'\x89PNG\r\n\x1a\n' or b[:4] == b'RIFF' or b[:6] in (b'GIF87a', b'GIF89a')):
        raise ValueError('not an image (an expired link or a login page)')   # 19 Oct: some Facebook links return an HTML page
    path.write_bytes(b)


def refresh_usd():
    a = sys.argv
    return float(a[a.index('--refresh-usd') + 1]) if '--refresh-usd' in a else 0.0


def save(d, m):
    """A post's media into folder d: frames of its video, else its images, else its cover."""
    if m.get('video'):
        frames(d, m['video'], m.get('cover'))
    elif m.get('images'):
        for n, u in enumerate(m['images'][:7], 1):
            get(u, d / ('p_%02d.jpg' % n))
    elif m.get('cover'):
        get(m['cover'], d / '00_cover.jpg')
    else:
        raise ValueError('no media link')


def retry(expired):
    """26 Oct: the posts whose links expired, with fresh links by the post's link (at most --refresh-usd USD), tried once more."""
    usd = refresh_usd()
    if expired and not usd:
        print('  %d posts with expired links; run again with --refresh-usd N to fetch fresh ones' % len(expired))
    if not expired or not usd:
        return 0
    fresh = media_links.refresh([(u, pl) for u, pl, d in expired], usd)
    done = 0
    for u, pl, d in expired:
        m = fresh.get(u)
        if not m:
            print('  %s: no fresh link' % u); continue
        for f in d.glob('*'): f.unlink()
        try:
            save(d, m); done += 1
        except Exception as e:
            print('  %s: the fresh link failed too: %s' % (u, str(e)[:100]))
    print('fresh links: media saved for %d of %d posts' % (done, len(expired)))
    return done


def main(files):
    done = 0
    expired = []
    for f in files:
        for x in json.load(open(f, encoding='utf-8'))['items']:
            code = x.get('shortCode')
            if not code:
                continue
            d = OUT / code; d.mkdir(parents=True, exist_ok=True)
            if any(d.glob('*.jpg')):
                continue
            try:
                if x.get('videoUrl'):
                    if x.get('displayUrl'): get(x['displayUrl'], d / '00_cover.jpg')
                    get(x['videoUrl'], d / 'video.mp4')
                    subprocess.run([FF, '-loglevel', 'error', '-i', str(d / 'video.mp4'), '-vf', 'fps=1/2,scale=720:-2', '-frames:v', str(MAX_FRAMES), str(d / 'f_%02d.jpg')], check=True)
                    (d / 'video.mp4').unlink()
                else:
                    urls = x.get('images') or [c.get('displayUrl') for c in x.get('childPosts') or [] if c.get('displayUrl')] or [x.get('displayUrl')]
                    for n, u in enumerate([u for u in urls if u], 1):
                        get(u, d / ('p_%02d.jpg' % n))
                done += 1
            except media_links.Expired:
                expired.append((x.get('url') or 'https://www.instagram.com/p/%s/' % code, 'ig', d))
            except Exception as e:
                print('  %s: %s' % (code, str(e)[:120]))
    done += retry(expired)
    print('media saved for %d posts in %s' % (done, OUT))


def frames(d, video_url, cover=None):
    if cover: get(cover, d / '00_cover.jpg')
    get(video_url, d / 'video.mp4')
    subprocess.run([FF, '-loglevel', 'error', '-i', str(d / 'video.mp4'), '-vf', 'fps=1/2,scale=720:-2', '-frames:v', str(MAX_FRAMES), str(d / 'f_%02d.jpg')], check=True)
    (d / 'video.mp4').unlink()


def facebook(only=None):
    """Public Facebook posts about V7 whose pictures say more than their text: photos and albums, and reels and videos with less than
    20 characters of speech. Their media links come from the search rows (normalize.py keeps them as media)."""
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    done = 0
    expired = []
    for it in items:
        if it['pl'] != 'fb' or it['src'] != 'ugc' or it['kind'] != 'post' or not (labels.get(it['id']) or {}).get('about'):
            continue
        m = it.get('media') or {}
        video = it.get('fmt') in ('Reel', 'Video')
        if video and len(it.get('speech') or '') >= 20 or (only == 'photos' and video) or (only == 'videos' and not video):
            continue
        d = OUT / ('fb_' + it['id'][3:]); d.mkdir(parents=True, exist_ok=True)
        if any(d.glob('*.jpg')):
            continue
        try:
            if video and m.get('video'):
                try:
                    frames(d, m['video'], m.get('cover'))
                except Exception as e:   # an expired or audio-only link: the cover or the post's images instead
                    for f in d.glob('*'): f.unlink()
                    if not (m.get('cover') or m.get('images')):
                        raise
                    print('  %s: video failed (%s), pictures instead' % (it['id'], str(e)[:60]))
                    for n, u in enumerate(([m['cover']] if m.get('cover') else []) + (m.get('images') or [])[:6], 1):
                        get(u, d / ('p_%02d.jpg' % n))
            elif m.get('images'):
                for n, u in enumerate(m['images'][:7], 1):
                    get(u, d / ('p_%02d.jpg' % n))
            elif m.get('cover'):
                get(m['cover'], d / '00_cover.jpg')
            else:
                d.rmdir(); continue
            done += 1
        except media_links.Expired:
            expired.append((it['url'], 'fb', d))
        except Exception as e:
            print('  %s: %s' % (it['id'], str(e)[:120]))
    done += retry(expired)
    print('media saved for %d Facebook posts in %s' % (done, OUT))


BASELINE = HERE / 'vis_baseline.json'


def tiktok(d, url):
    """A TikTok video's frames and cover, from its public page (26 Oct: the page's video link downloads with the page's cookies; free)."""
    import http.cookiejar, re
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    page = op.open(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'replace'); time.sleep(1)
    v = re.search(r'"playAddr":"(https:[^"]+)"', page) or re.search(r'"downloadAddr":"(https:[^"]+)"', page)
    c = re.search(r'"(?:cover|originCover)":"(https:[^"]+)"', page)
    if c:
        get(json.loads('"' + c.group(1) + '"'), d / '00_cover.jpg')
    if not v:
        raise ValueError('no video on the page (removed, private or region-locked)')
    (d / 'video.mp4').write_bytes(op.open(urllib.request.Request(json.loads('"' + v.group(1) + '"'), headers=dict(UA, Referer='https://www.tiktok.com/')), timeout=60).read())
    subprocess.run([FF, '-loglevel', 'error', '-i', str(d / 'video.mp4'), '-vf', 'fps=1/2,scale=720:-2', '-frames:v', str(MAX_FRAMES), str(d / 'f_%02d.jpg')], check=True)
    (d / 'video.mp4').unlink()


def youtube(d, url):
    """A YouTube video's cover and the three frames YouTube publishes from inside it (about a quarter, half and three quarters in); free."""
    import re
    vid = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', url).group(1)
    for n, name in enumerate(('hqdefault', 'hq1', 'hq2', 'hq3')):
        get('https://i.ytimg.com/vi/%s/%s.jpg' % (vid, name), d / ('%02d_%s.jpg' % (n, name)))


def new_posts():
    """26 Oct (DECISIONS #183): every new public post labelled about V7 by the first pass (caption and author) gets its pictures or frames,
    so label.py checks it again with them: Facebook from the media links its rows carried, Instagram from fresh links by the post's link
    (its rows keep none), TikTok from its public page, YouTube from its published frames. Posts in vis_baseline.json (collected before
    26 Oct) are left as they were. Folders: vis/<shortcode> (Instagram), vis/fb_<id>, vis/tt_<id>, vis/yt_<id>."""
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    base = set(json.load(open(BASELINE, encoding='utf-8'))['posts']) if BASELINE.exists() else set()
    shared_orig = lambda i: any(str(r).startswith('fbd_posts_shared_') for r in i.get('found_by') or [])   # DECISIONS #190
    todo = [i for i in items if i['kind'] == 'post' and i['src'] == 'ugc' and i['id'] not in base and ((labels.get(i['id']) or {}).get('about') or shared_orig(i))
            and i['pl'] in ('fb', 'ig', 'tt', 'yt') and i.get('fmt') != 'Text']
    ids = {i['id'] for i in items}
    urls = {u.split('?')[0].rstrip('/') for i in items if i['kind'] == 'post' for u in [i.get('url')] + i.get('urls', []) if u}
    # 26 Oct (DECISIONS #188): a share whose shared post is in the collection gets no frames of its own: they'd be the same video, read once
    def has_original(i):
        return bool(i.get('shared_id')) and 'fb:' + i['shared_id'] in ids or (i.get('shared_url') or '').split('?')[0].rstrip('/') in urls
    todo = [i for i in todo if not (i.get('is_share') and has_original(i))]
    done, expired = 0, []
    for it in todo:
        pl = it['pl']
        d = OUT / (it['id'][3:] if pl == 'ig' else pl + '_' + it['id'][3:])
        if d.exists() and any(d.glob('*.jpg')):
            continue
        d.mkdir(parents=True, exist_ok=True)
        try:
            if pl == 'fb':
                save(d, it.get('media') or {})
            elif pl == 'ig':
                expired.append((it['url'], 'ig', d)); continue
            elif pl == 'tt':
                tiktok(d, it['url'])
            else:
                youtube(d, it['url'])
            done += 1
        except media_links.Expired:
            expired.append((it['url'], pl, d))
        except Exception as e:
            print('  %s: %s' % (it['id'], str(e)[:120]))
    done += retry(expired)
    print('new posts about V7: %d to check, media saved for %d' % (len(todo), done))


if __name__ == '__main__':
    if '--new' in sys.argv:
        new_posts()
    elif '--fb' in sys.argv:
        facebook(next((a for a in sys.argv if a in ('photos', 'videos')), None))
    else:
        main([a for a in sys.argv[1:] if a.endswith('.json')])
