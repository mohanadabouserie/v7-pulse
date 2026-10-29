"""Speech to text with ElevenLabs Scribe v2 (26 Oct 2026, DECISIONS #194).

Why: invideoiq (Whisper-like) is poor on Egyptian Arabic and invents text over music. Published tests put Scribe v2 at 13.1% word error
on Egyptian Arabic mixed with English, against about 50-59% for Whisper large-v3. Price: USD 0.22 an hour of audio (about 0.004 a minute).

Key: .env.elevenlabs at the repo root, ELEVENLABS_API_KEY=… (git-ignored, like every .env.*). Never print it.

    python3 stt_elevenlabs.py test [--keyterms]    # the 5 TikToks (--keyterms: with the product names, KEYTERMS) that have TikTok's own Arabic subtitles: Scribe's text against them, word error rate

The pipeline's speech to text since 29 Oct (DECISIONS #197), in place of invideoiq (Facebook) and apple_yang (Instagram), and new for TikTok
and YouTube; new posts only (posts in vis_baseline.json keep the speech they have). speech() writes its results in the format the
replaced scrapers wrote, so normalize.py and collect.attempts() read them as before:
- Facebook reels and video links (/reel/, /videos/, watch?v=), TikTok and YouTube: ElevenLabs fetches the video by its link (tested 29 Oct);
- Instagram reels and Facebook /posts/ links can't be fetched by link: Instagram's video file comes from fresh media links (media_links.py),
  Facebook post links go through collect.py fbinner, which finds the videos' own links.
"""
import http.cookiejar, json, os, pathlib, re, sys, tempfile, time, unicodedata, urllib.error, urllib.request, uuid

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
API = os.environ.get('ELEVENLABS_API', 'https://api.elevenlabs.io/v1/speech-to-text')   # (pipeline tests point it at a stand-in)
MODEL = 'scribe_v2'
USD_PER_MIN = 0.22 / 60
MAX_USD = 2.0   # ElevenLabs spending a pipeline step may reach (its own account, not Apify's budget)
# 29 Oct (DECISIONS #201): an unclear video (not yet known to be about V7) longer than LONG_SECONDS is read in two steps: its first
# SAMPLE_SECONDS, then the rest only when they talk about drinks, V7 or its competitors (PROMISING). A long show or series costs 3 minutes.
LONG_SECONDS, SAMPLE_SECONDS = 300, 180
LINK_UNCLEAR_MAX_SECONDS = 900   # 29 Oct: an unclear video read by link (YouTube, Facebook videos inside a post) can't be cut; read whole up to 15 minutes, longer ones left out
# 29 Oct (DECISIONS #196, #197): names Scribe should spell right (20% more a minute; under 100 terms, so no 20-second minimum a video).
# Each in English letters and in Arabic letters: V7's brands, its flavours, and the competitors people compare it with in Egypt.
KEYTERMS = [
    # V7's brands
    'V7', 'V Cola', 'V Cola Diet', 'V Super Soda', 'V Lemon', 'V Orange', 'Cream Soda', 'Summer Edition', 'Vitality',
    'ڤي سڤن', 'ڤي كولا', 'ڤي كولا دايت', 'ڤي سوبر صودا', 'سوبر صودا', 'ڤي ليمون', 'ڤي أورانج', 'كريم صودا', 'سمر إديشن',
    # V7's flavours (the English and Arabic names people use)
    'Pomegranate', 'Piña Colada', 'Lemon Mint', 'Blueberry', 'Pineapple', 'Pink Lemonade', 'Pineapple Malt', 'Apple Malt',
    'بينا كولادا', 'ليمون نعناع', 'بلوبيري', 'بينك ليموناد', 'شعير بالأناناس', 'شعير بالتفاح',
    # competitors and other drinks named in reviews
    'Pepsi', 'Coca-Cola', '7UP', 'Sprite', 'Fanta', 'Mirinda', 'Schweppes', 'Mountain Dew', 'Fayrouz', 'Birell', 'Moussy',
    'Barbican', 'Spiro Spathis', "Will's Kitchen", 'Red Bull', 'Sting',
    'بيبسي', 'كوكاكولا', 'سفن أب', 'سبرايت', 'فانتا', 'ميرندا', 'شويبس', 'ماونتن ديو', 'فيروز', 'بيريل', 'موسي',
    'باربيكان', 'سبيرو سباتس', 'ويلز كيتشن', 'ريد بول', 'ستينج',
]
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}

TEST = [   # TikToks about V7 with TikTok's own Arabic subtitles (26 Oct check)
    'https://www.tiktok.com/@mon3esh.zone/video/7674323187026513169',
    'https://www.tiktok.com/@rahaf_elshami/video/7677165994103622913',
    'https://www.tiktok.com/@mariameladl/video/7674707543544859925',
    'https://www.tiktok.com/@sensawyy/video/7672000531979586834',
    'https://www.tiktok.com/@rawan_abdelfatah0/video/7677662316783013138',
]


def key():
    k = os.environ.get('ELEVENLABS_API_KEY')
    p = ROOT / '.env.elevenlabs'
    if not k and p.exists():
        m = re.search(r'^\s*ELEVENLABS_API_KEY\s*=\s*"?([^"\s]+)', p.read_text(), re.M)
        k = m and m.group(1)
    if not k:
        sys.exit('no ElevenLabs key: put ELEVENLABS_API_KEY=… in .env.elevenlabs at the repo root')
    return k


def _post(fields, media=None):
    b = '----v7pulse' + uuid.uuid4().hex
    parts = [('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, n, v)).encode() for n, v in fields]
    if media:
        parts.append(('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n'
                      % (b, pathlib.Path(media).name)).encode() + pathlib.Path(media).read_bytes() + b'\r\n')
    parts.append(('--%s--\r\n' % b).encode())
    req = urllib.request.Request(API, data=b''.join(parts), method='POST', headers={'xi-api-key': key(), 'Content-Type': 'multipart/form-data; boundary=' + b})
    try:
        return json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as e:
        raise RuntimeError('ElevenLabs %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300])) from None


def transcribe(media, language='ara', keyterms=None, url=None):
    """Scribe v2's transcript of a local audio or video file, or of a video ElevenLabs fetches by its link (url):
    {'text', 'language_code', 'language_probability', 'words', …}. keyterms: words to recognise more accurately (one form field each)."""
    fields = [('model_id', MODEL), ('language_code', language), ('tag_audio_events', 'false')] + [('keyterms', k) for k in keyterms or []]
    return _post(fields + ([('source_url', url)] if url else []), None if url else media)


PROMISING = re.compile('|'.join([re.escape(k) for k in KEYTERMS] + [
    r'\bv\s*-?\s*7\b', r'في\s*سفن', r'فى\s*سفن', r'في\s*كولا', r'مشروب', r'صود[اه]', r'سود[اه]', r'كولا', r'كوكا', r'بيبسي', r'سفن\s*[أا]ب', r'عصير', r'كانز',
    r'ندوق', r'اطعم', r'طعمه?ا?', r'نجرب', r'\bdrinks?\b', r'\bsoda\b', r'\bcola\b', r'\bpepsi\b', r'\bcoke\b', r'\btaste\b']), re.I)


def ffmpeg():
    """The ffmpeg that comes with the project venv (data/.venv, imageio-ffmpeg): the pipeline itself runs on the system Python."""
    import subprocess
    exe = os.environ.get('V7_FFMPEG')
    if not exe:
        venv = ROOT / 'data' / '.venv' / 'bin' / 'python'
        exe = subprocess.run([str(venv), '-c', 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'], capture_output=True, text=True).stdout.strip()
        os.environ['V7_FFMPEG'] = exe
    return exe


def length(path):
    """A local video's length in seconds (None if ffmpeg can't tell)."""
    import subprocess
    err = subprocess.run([ffmpeg(), '-hide_banner', '-i', str(path)], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', err)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None


def cut(path, start, dur=None):
    """The audio of a local video from start (seconds), dur seconds long (to the end if None), as an mp3 next to it."""
    import subprocess
    out = pathlib.Path(str(path) + '.%d.mp3' % start)
    subprocess.run([ffmpeg(), '-loglevel', 'error', '-y', '-ss', str(start)] + (['-t', str(dur)] if dur else []) + ['-i', str(path), '-vn', '-ac', '1', '-b:a', '64k', str(out)], check=True)
    return out


def yt_length(url):
    """A YouTube video's length in seconds, from its public page (free); None if the page doesn't say."""
    try:
        page = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'replace'); time.sleep(1)
        m = re.search(r'"lengthSeconds":"(\d+)"', page)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def seconds(r):
    return max([w.get('end') or 0 for w in r.get('words') or [] if isinstance(w, dict)] + [0])


def speech(kind, jobs, max_usd=MAX_USD):
    """Speech for the pipeline. jobs: [(post or video link, source)] or [{'link', 'src', 'unclear', 'seconds'}]; source a link ElevenLabs
    fetches itself or a local video file (a job's 'max_seconds' sets how long an unclear link may be). An unclear video (not yet known to be about V7) over LONG_SECONDS is read in two steps: its first
    SAMPLE_SECONDS, then the rest only if they're PROMISING (DECISIONS #201); that needs a local file, or a link whose length is known and
    short. kind 'fbf_speech' (Facebook), 'igspeech' (Instagram) or 'ttyt_speech' (TikTok and YouTube) names the raw file,
    raw/<kind>_el_<tag>.json, written like the scrapers it replaces (input: the links asked; items: one row a link, with its text or the
    error). Stops before max_usd of ElevenLabs time; each link asked is counted by collect.attempts(), so a failing one is tried at most twice."""
    raw = pathlib.Path(os.environ['V7_RAW']) if os.environ.get('V7_RAW') else HERE / 'raw'
    tag = time.strftime('%Y%m%d%H%M%S') + '_%06d' % (time.time_ns() // 1000 % 1000000)
    asked, rows, usd, skipped = [], [], 0.0, 0
    price = lambda s: max(s, 1) / 60 * USD_PER_MIN * 1.2
    for j in jobs:
        j = j if isinstance(j, dict) else {'link': j[0], 'src': j[1]}
        link, src, unclear = j['link'], str(j['src']), j.get('unclear')
        local = not src.startswith('http')
        if usd >= max_usd:
            print('  ElevenLabs: stopped at USD %.2f (line USD %.2f); the rest wait for the next run' % (usd, max_usd))
            break
        known = length(src) if local else j.get('seconds')
        if unclear and not local and (known is None or known > j.get('max_seconds', LONG_SECONDS)):
            skipped += 1   # an unclear video that can't be cut: read only when its length is known and short
            continue
        asked.append(link)
        row = {'scraper': 'elevenlabs ' + MODEL}
        row['video_url' if kind == 'fbf_speech' else 'url'] = link
        if kind == 'igspeech':
            m = re.search(r'/(?:p|reel|reels|tv)/([^/?#]+)', link)
            row['code'] = m.group(1) if m else None
        try:
            if unclear and local and known and known > LONG_SECONDS:
                r = transcribe(cut(src, 0, SAMPLE_SECONDS), keyterms=KEYTERMS)
                usd += price(min(known, SAMPLE_SECONDS))
                text = (r.get('text') or '').strip()
                if PROMISING.search(text):
                    r2 = transcribe(cut(src, SAMPLE_SECONDS), keyterms=KEYTERMS)
                    usd += price(known - SAMPLE_SECONDS)
                    text = (text + ' ' + (r2.get('text') or '')).strip()
                    row['read'] = 'the first %d seconds, then the rest' % SAMPLE_SECONDS
                else:
                    row['read'] = 'the first %d seconds of %d: nothing about drinks or V7, the rest not read' % (SAMPLE_SECONDS, known)
                s = known
            else:
                r = transcribe(src if local else None, keyterms=KEYTERMS, url=None if local else src)
                s = seconds(r) or known or 0
                usd += price(s)
                text = (r.get('text') or '').strip()
            row.update({'transcript' if kind == 'fbf_speech' else 'text': text, 'language': r.get('language_code'), 'seconds': round(s or 0, 1)})
        except Exception as e:
            row['error'] = str(e)[:300]
        rows.append(row)
    if skipped:
        print('  ElevenLabs %s: %d unclear videos left out (no file to cut and no known short length)' % (kind, skipped))
    if asked:
        key_in = 'bulkUrls' if kind == 'igspeech' else 'video_urls'
        p = raw / ('%s_el_%s.json' % (kind, tag))
        json.dump({'input': {key_in: asked}, 'items': rows}, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('  ElevenLabs %s: %d of %d videos read, about USD %.3f (%s)' % (kind, sum(1 for r in rows if not r.get('error')), len(asked), usd, p.name))
    return rows


def tiktok_page(url):
    """The public page's video (downloaded with the page's cookies) and its Arabic subtitles, if TikTok made any. Free."""
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    page = op.open(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'replace'); time.sleep(1)
    v = re.search(r'"playAddr":"(https:[^"]+)"', page) or re.search(r'"downloadAddr":"(https:[^"]+)"', page)
    if not v:
        raise ValueError('no video on the page (removed, private or region-locked)')
    video = op.open(urllib.request.Request(json.loads('"' + v.group(1) + '"'), headers=dict(UA, Referer='https://www.tiktok.com/')), timeout=60).read()
    subs = None
    m = re.search(r'"subtitleInfos":(\[.*?\])', page)
    for s in json.loads(m.group(1)) if m else []:
        if str(s.get('LanguageCodeName', '')).startswith('ara') and s.get('Url'):
            vtt = op.open(urllib.request.Request(s['Url'], headers=dict(UA, Referer='https://www.tiktok.com/')), timeout=30).read().decode('utf-8', 'replace')
            subs = ' '.join(l.strip() for l in vtt.splitlines()
                            if l.strip() and l.strip() != 'WEBVTT' and '-->' not in l and not l.strip().isdigit())
            break
    return video, subs


def norm(t):
    """Words for comparing Arabic transcripts: no diacritics or punctuation, one form of alef, yaa and taa marbuta."""
    t = ''.join(c for c in unicodedata.normalize('NFKD', t or '') if not unicodedata.combining(c))
    t = re.sub('[إأآٱ]', 'ا', t).replace('ى', 'ي').replace('ة', 'ه').replace('ـ', '')
    return re.sub(r'[^\w\s]', ' ', t.lower()).split()


def wer(ref, hyp):
    """Word error rate of hyp against ref (edit distance over words / words in ref)."""
    r, h = norm(ref), norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(len(r), 1)


def test(keyterms=None):
    out, cost = [], 0.0
    with tempfile.TemporaryDirectory() as tmp:
        for url in TEST:
            try:
                video, subs = tiktok_page(url)
                f = pathlib.Path(tmp) / (url.rstrip('/').split('/')[-1] + '.mp4')
                f.write_bytes(video)
                r = transcribe(f, keyterms=keyterms)
            except Exception as e:
                print('%-45s failed: %s' % (url.split('/')[3], e))
                out.append({'url': url, 'error': str(e)})
                continue
            secs = seconds(r)
            cost += secs / 60 * USD_PER_MIN * (1.2 if keyterms else 1)
            row = {'url': url, 'tiktok_subtitles': subs, 'scribe': r.get('text'), 'language': r.get('language_code'),
                   'seconds': round(secs, 1), 'wer_vs_tiktok': round(wer(subs, r.get('text')), 3) if subs else None}
            out.append(row)
            print('%-22s %5.0fs  word error vs TikTok: %s' % (url.split('/')[3], secs, '%.0f%%' % (100 * row['wer_vs_tiktok']) if subs else 'no subtitles'))
    p = HERE / 'raw' / ('stt_elevenlabs_test_%s%s.json' % ('keyterms_' if keyterms else '', time.strftime('%Y%m%d%H%M%S')))
    json.dump({'model': MODEL, 'keyterms': keyterms, 'items': out}, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('about USD %.3f; saved %s' % (cost, p.relative_to(ROOT)))


if __name__ == '__main__':
    if sys.argv[1:2] == ['test']:
        test(KEYTERMS if sys.argv[2:] == ['--keyterms'] else None)
    else:
        sys.exit(__doc__)
