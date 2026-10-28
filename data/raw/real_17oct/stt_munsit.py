"""Speech to text with Munsit (CNTXT AI, Arabic-only), tested against ElevenLabs Scribe v2 (29 Oct 2026, DECISIONS #195).

Price: 100 credits a minute, 20,000 credits = USD 1, so USD 0.005 a minute; the free plan starts with 10,000 credits (about 100 minutes).
Models: `munsit` (Arabic only) and `munsit-en-ar` (Arabic mixed with English). Docs: https://docs.munsit.com/speech-to-text/transcribe

Key: .env.munsit at the repo root, MUNSIT_API_KEY=… (git-ignored, like every .env.*). Never print it.

    data/.venv/bin/python stt_munsit.py test    # the same 5 TikToks as stt_elevenlabs.py test, three ways (VARIANTS)
"""
import json, os, pathlib, re, subprocess, sys, tempfile, time, urllib.error, urllib.request, uuid

import stt_elevenlabs as E   # the TikTok download, the subtitles and the word comparison

API = 'https://api.munsit.com/api/v1/audio/transcribe'
MODELS = ('munsit', 'munsit-en-ar')
# 29 Oct test: each video three ways. Sentiment and gender are paid options (10 credits a minute each); hotwords are free.
HOTWORDS = 'V7, V Cola, ڤي سڤن, ڤي كولا, Cream Soda, كريم صودا, V Super Soda, سوبر صودا'   # 16 words: munsit-en-ar reads the first 20
VARIANTS = {'ar': ('munsit', {'return_sentiment': 'true', 'return_gender': 'true'}),
            'en_ar': ('munsit-en-ar', {'return_sentiment': 'true', 'return_gender': 'true'}),
            'en_ar_hot': ('munsit-en-ar', {'hotwords': HOTWORDS})}
USD_PER_MIN = 100 / 20000


def key():
    k = os.environ.get('MUNSIT_API_KEY')
    p = E.ROOT / '.env.munsit'
    if not k and p.exists():
        m = re.search(r'^\s*MUNSIT_API_KEY\s*=\s*"?([^"\s]+)', p.read_text(), re.M)
        k = m and m.group(1)
    if not k or 'PASTE' in k:
        sys.exit('no Munsit key: put MUNSIT_API_KEY=… in .env.munsit at the repo root')
    return k


def transcribe(audio, model='munsit', extra=None):
    """Munsit's transcript of a local audio file: its 'data' ({'transcription', 'duration', 'stats', 'turns', 'analysis', …}).
    extra: more form fields (return_sentiment, return_gender, hotwords, …)."""
    b = '----v7pulse' + uuid.uuid4().hex
    fields = [('model', model)] + ([('language', 'auto')] if model == 'munsit-en-ar' else []) + list((extra or {}).items())
    body = b''.join(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, n, v)).encode() for n, v in fields)
    body += ('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: audio/mpeg\r\n\r\n'
             % (b, pathlib.Path(audio).name)).encode() + pathlib.Path(audio).read_bytes() + ('\r\n--%s--\r\n' % b).encode()
    req = urllib.request.Request(API, data=body, method='POST', headers={'x-api-key': key(), 'Content-Type': 'multipart/form-data; boundary=' + b})
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))['data']
    except urllib.error.HTTPError as e:
        raise RuntimeError('Munsit %d: %s' % (e.code, e.read().decode('utf-8', 'replace')[:300])) from None


def test():
    import imageio_ffmpeg   # data/.venv
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out, credits = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for url in E.TEST:
            row = {'url': url}
            try:
                video, subs = E.tiktok_page(url)
                v, a = pathlib.Path(tmp) / 'v.mp4', pathlib.Path(tmp) / (url.rstrip('/').split('/')[-1] + '.mp3')
                v.write_bytes(video)
                subprocess.run([ff, '-loglevel', 'error', '-y', '-i', str(v), '-vn', '-ac', '1', '-b:a', '64k', str(a)], check=True)
                row['tiktok_subtitles'] = subs
                for name, (m, extra) in VARIANTS.items():
                    d = transcribe(a, m, extra)
                    credits += (d.get('stats') or {}).get('creditsConsumed') or 0
                    row[name] = {'text': d.get('transcription'), 'analysis': d.get('analysis'),
                                 'turns': [{k: x.get(k) for k in ('text', 'sentiment', 'gender')} for x in d.get('turns') or []],
                                 'wer_vs_tiktok': round(E.wer(subs, d.get('transcription')), 3) if subs else None}
                row['seconds'] = d.get('duration')
            except Exception as e:
                row['error'] = str(e)
                print('%-22s failed: %s' % (url.split('/')[3], e))
                out.append(row)
                continue
            out.append(row)
            print('%-22s %5.0fs  word difference vs TikTok: %s' % (url.split('/')[3], row['seconds'] or 0,
                  '  '.join('%s %.0f%%' % (n, 100 * row[n]['wer_vs_tiktok']) for n in VARIANTS) if subs else 'no subtitles'))
    p = E.HERE / 'raw' / ('stt_munsit_test_%s.json' % time.strftime('%Y%m%d%H%M%S'))
    json.dump({'variants': {n: [m, x] for n, (m, x) in VARIANTS.items()}, 'items': out}, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%d credits (about USD %.3f); saved %s' % (credits, credits / 20000, p.relative_to(E.ROOT)))


if __name__ == '__main__':
    test() if sys.argv[1:] == ['test'] else sys.exit(__doc__)
