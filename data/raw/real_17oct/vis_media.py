"""19 Oct 2026: downloads the media of Instagram posts (fetched fresh by link with Apify's post scraper) and takes frames from videos,
so the text on them can be read (vis_read.py). Photos: the full-size image of each slide. Videos: a frame every 2 seconds, up to 12,
plus the cover. One request a second. Files go to vis/<shortcode>/ (local only: they're people's media).
Usage: data/.venv/bin/python vis_media.py raw/<post-scraper file>.json [more files]"""
import json, pathlib, subprocess, sys, time, urllib.request
import imageio_ffmpeg
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'vis'
FF = imageio_ffmpeg.get_ffmpeg_exe()
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}


def get(url, path):
    path.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()); time.sleep(1)


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


if __name__ == '__main__':
    main(sys.argv[1:])
