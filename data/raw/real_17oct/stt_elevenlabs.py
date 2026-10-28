"""Speech to text with ElevenLabs Scribe v2 (26 Oct 2026, DECISIONS #194).

Why: invideoiq (Whisper-like) is poor on Egyptian Arabic and invents text over music. Published tests put Scribe v2 at 13.1% word error
on Egyptian Arabic mixed with English, against about 50-59% for Whisper large-v3. Price: USD 0.22 an hour of audio (about 0.004 a minute).

Key: .env.elevenlabs at the repo root, ELEVENLABS_API_KEY=… (git-ignored, like every .env.*). Never print it.

    python3 stt_elevenlabs.py test [--keyterms]    # the 5 TikToks (--keyterms: with the product names, KEYTERMS) that have TikTok's own Arabic subtitles: Scribe's text against them, word error rate
"""
import http.cookiejar, json, os, pathlib, re, sys, tempfile, time, unicodedata, urllib.error, urllib.request, uuid

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
API = 'https://api.elevenlabs.io/v1/speech-to-text'
MODEL = 'scribe_v2'
USD_PER_MIN = 0.22 / 60
# 29 Oct (DECISIONS #196): product names, in English and Arabic letters, so Scribe spells them right (20% more per minute)
KEYTERMS = ['V7', 'V Cola', 'Cream Soda', 'V Super Soda', 'ڤي سڤن', 'ڤي كولا', 'كريم صودا', 'سوبر صودا']
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


def transcribe(media, language='ara', keyterms=None):
    """Scribe v2's transcript of a local audio or video file: {'text', 'language_code', 'language_probability', 'words', …}.
    keyterms: words to recognise more accurately (one form field each)."""
    b = '----v7pulse' + uuid.uuid4().hex
    parts = []
    for name, val in [('model_id', MODEL), ('language_code', language), ('tag_audio_events', 'false')] + [('keyterms', k) for k in keyterms or []]:
        parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, name, val)).encode())
    parts.append(('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n'
                  % (b, pathlib.Path(media).name)).encode() + pathlib.Path(media).read_bytes() + b'\r\n')
    parts.append(('--%s--\r\n' % b).encode())
    req = urllib.request.Request(API, data=b''.join(parts), method='POST',
                                 headers={'xi-api-key': key(), 'Content-Type': 'multipart/form-data; boundary=' + b})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        raise RuntimeError('ElevenLabs %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300])) from None


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
            secs = max([w.get('end') or 0 for w in r.get('words') or []] + [0])
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
