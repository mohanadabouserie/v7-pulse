"""19 Oct 2026: downloads the media of Instagram posts (fetched fresh by link with Apify's post scraper) and takes frames from videos,
so the text on them can be read (vis_read.py). Photos: the full-size image of each slide. Videos: a frame every 2 seconds, up to 12,
plus the cover. One request a second. Files go to vis/<shortcode>/ (local only: they're people's media).
Usage: data/.venv/bin/python vis_media.py raw/<post-scraper file>.json [more files]
       data/.venv/bin/python vis_media.py --fb [photos|videos]   (19 Oct: public Facebook posts about V7 that are photos or albums, or videos with little or no
       speech, from the media links their search rows carried; folders vis/fb_<post id>/)"""
import json, pathlib, subprocess, sys, time, urllib.request
import socket
_gai = socket.getaddrinfo
def _v4_first(*a, **k):   # this network often can't reach IPv6 (as in fetch_media.py): use IPv4 when the host has it
    rs = _gai(*a, **k); v4 = [r for r in rs if r[0] == socket.AF_INET]
    return v4 or rs
socket.getaddrinfo = _v4_first
import imageio_ffmpeg
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'vis'
FF = imageio_ffmpeg.get_ffmpeg_exe()
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}


def get(url, path):
    b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read(); time.sleep(1)
    if path.suffix == '.jpg' and not (b[:3] == b'\xff\xd8\xff' or b[:8] == b'\x89PNG\r\n\x1a\n' or b[:4] == b'RIFF' or b[:6] in (b'GIF87a', b'GIF89a')):
        raise ValueError('not an image (an expired link or a login page)')   # 19 Oct: some Facebook links return an HTML page
    path.write_bytes(b)


def main(files):
    done = 0
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
                    subprocess.run([FF, '-loglevel', 'error', '-i', str(d / 'video.mp4'), '-vf', 'fps=1/2,scale=720:-2', '-frames:v', '12', str(d / 'f_%02d.jpg')], check=True)
                    (d / 'video.mp4').unlink()
                else:
                    urls = x.get('images') or [c.get('displayUrl') for c in x.get('childPosts') or [] if c.get('displayUrl')] or [x.get('displayUrl')]
                    for n, u in enumerate([u for u in urls if u], 1):
                        get(u, d / ('p_%02d.jpg' % n))
                done += 1
            except Exception as e:
                print('  %s: %s' % (code, str(e)[:120]))
    print('media saved for %d posts in %s' % (done, OUT))


def frames(d, video_url, cover=None):
    if cover: get(cover, d / '00_cover.jpg')
    get(video_url, d / 'video.mp4')
    subprocess.run([FF, '-loglevel', 'error', '-i', str(d / 'video.mp4'), '-vf', 'fps=1/2,scale=720:-2', '-frames:v', '12', str(d / 'f_%02d.jpg')], check=True)
    (d / 'video.mp4').unlink()


def facebook(only=None):
    """Public Facebook posts about V7 whose pictures say more than their text: photos and albums, and reels and videos with less than
    20 characters of speech. Their media links come from the search rows (normalize.py keeps them as media)."""
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    done = 0
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
        except Exception as e:
            print('  %s: %s' % (it['id'], str(e)[:120]))
    print('media saved for %d Facebook posts in %s' % (done, OUT))


if __name__ == '__main__':
    facebook(next((a for a in sys.argv if a in ('photos', 'videos')), None)) if '--fb' in sys.argv else main(sys.argv[1:])
