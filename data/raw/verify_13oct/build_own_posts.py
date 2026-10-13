"""Builds the dashboard's real V7 posts from the 13 Oct 2026 pulls (Versions 21 and 22).

  own_pull.py   ig_profiles.json (V7 Egypt and the 4 V7 pages abroad, 12 latest posts each, plus the UK distributor),
                fb_page.json (V7Egypt's 15 latest posts), tt_profile10.json (@v7.egypt's 10 latest), yt_channel.json
  own_pull2.py  yt_videos.json (likes and exact dates for the 12 YouTube videos), fb_pageinfo.json (page followers),
                fb_orange.json and ig_orange.json (the first comments on the V Orange launch)
  ../own_backfill_13oct/  pull.py (V7 Egypt's older posts back to 16 Apr: fb_backfill, tt_backfill, ig_backfill, yt_backfill)
                and yt_pages.py (exact dates and likes for those YouTube videos, read from their public pages)
  this file     the REAL_OWN block (V7 Egypt on Facebook, Instagram, TikTok and YouTube) and the REAL_OWN_X block
                (V7's pages abroad), written between their /*REAL_OWN*/ and /*REAL_OWN_X*/ markers with --inject

Counts are as of the pull. Products are tagged from the caption (V Lemon is the Lemon-Lime can). Posts with views 20+
times the account's followers get the "boost" view curve (most likely promoted). Times are local: Cairo UTC+3 until the
end of October and UTC+2 before 24 Apr, Tunisia and the UK UTC+1, Uzbekistan UTC+5, India UTC+5:30. Instagram's backfill
stopped at its 45-post cap, so Instagram is real from 27 May; the other platforms from 16 Apr, the dashboard's first day.

Usage: python3 build_own_posts.py [--inject]
"""
import datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BACK = os.path.join(HERE, '..', 'own_backfill_13oct')
DASH = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'V7_Pulse_Dashboard.html'))
FOL = {'fb': 79783, 'ig': 38959, 'tt': 36900, 'yt': 2540}       # 13 Oct 2026
COVER = {'fb': '2026-04-16', 'ig': '2026-05-27', 'tt': '2026-04-16', 'yt': '2026-04-16'}   # real from these dates on
START = '2026-04-16'                                                                          # the dashboard's first day
PAGES = {'v7tunisia': ('own_tn_ig', 1), 'v7uzbekistan': ('own_uz_ig', 5), 'v7ldnuk': ('own_uk_ig', 1), 'drinkv7': ('own_in_ig', 5.5)}


def load(name, folder=HERE):
    path = os.path.join(folder, name)
    return json.load(open(path, encoding='utf-8'))['items'] if os.path.exists(path) else []


def js(s):
    s = re.sub(r'\s+', ' ', re.sub('[\u2066-\u2069\u200e\u200f]', '', s or '')).strip()
    if len(s) > 240:
        s = s[:237].rsplit(' ', 1)[0] + '…'
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('</', '<\\/').replace('\u2028', ' ').replace('\u2029', ' ')


def local(iso, hours):
    t = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00'))
    if t.tzinfo: t = t.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    if hours == 'cairo': hours = 3 if t >= datetime.datetime(2026, 4, 23, 22) else 2   # Egypt's summer time from 24 Apr 2026
    t = t + datetime.timedelta(hours=hours)
    return t.date().isoformat(), t.hour, t.minute


def prods_eg(text):
    t = (text or '').lower()
    if 'orange' in t or 'برتقان' in t: return ['orange']
    if 'super soda diet' in t: return ['dcola']
    if any(k in t for k in ('v lemon', 'super lemon', 'ڤي ليمون', 'hit reset', 'put out the heat', 'spicy food', 'heavy workload')): return ['llime']
    if any(k in t for k in ('cream', 'كريم', 'bringing back the magic', "guess what's coming", 'guess what’s coming')): return ['cream']
    if 'flavored malt' in t or 'شعير بطعم الأناناس' in t: return ['pmalt']
    if 'malt' in t or 'شعير' in t: return ['pmalt', 'amalt']
    if 'pomegranate' in t and 'on the run' not in t: return ['pom']
    # V Cola's "Raise the flag" World Cup campaign (28 May to 7 Jul): flag, national team and cheering posts belong to it
    if re.search(r'\bv[ -]?cola\b|ve kola|[ڤف][يى] ?كولا|world cup|العلم|العَلم|منتخب|يلا يا مصر|للتشجيع', t): return ['cola']
    return ['ALL']


def prods_x(text):
    t = (text or '').lower(); out = []
    for rx, pid in ((r'pi[nñ]a ?colada', 'pina'), (r'pomegranate|grenade', 'pom'), (r'blueberry|myrtille', 'blue'),
                    (r'(lemon|limon)[ -]?mint', 'lmint'), (r'pink ?lemonade', 'pink'), (r'pine?apple[ -]?malt', 'pmalt'), (r'\bv ?cola\b', 'cola')):
        if re.search(rx, t) and pid not in out: out.append(pid)
    return out or ['ALL']


FMT = {'Video': 'Reel', 'Image': 'Image', 'Sidecar': 'Carousel'}
own, seen = [], set()
def add(r):
    if r['url'] in seen or r['d'] < START or r['d'] > '2026-10-12': return
    seen.add(r['url']); own.append(r)
for x in load('fb_page.json') + load('fb_backfill.json', BACK) + load('fb_test.json', BACK):
    d, hh, _ = local(x['time'], 'cairo')
    url = x['url']; text = (x.get('text') or '').strip()
    if not text and isinstance(x.get('sharedPost'), dict):   # a shared news post (the factory opening)
        sp = x['sharedPost']; text = 'Shared from ' + ((sp.get('pageName') or {}).get('name') or 'a page') + ': ' + (sp.get('text') or '')
    add(dict(d=d, h=hh, pl='fb', text=text, likes=x.get('likes') or 0, comments=x.get('comments') or 0, shares=x.get('shares') or 0,
             views=x.get('viewsCount') or 0, fmt='Reel' if '/reel/' in url else ('Video' if x.get('isVideo') else 'Image'), url=url))
abroad = []
for p in load('ig_profiles.json'):
    if p['username'] == 'v7egypt':
        for x in p['latestPosts']:
            d, hh, _ = local(x['timestamp'], 'cairo')
            add(dict(d=d, h=hh, pl='ig', text=x.get('caption'), likes=max(0, x.get('likesCount') or 0), comments=x.get('commentsCount') or 0,
                     shares=0, views=x.get('videoViewCount') or 0, fmt=FMT[x['type']], url=x['url']))
    elif p['username'] in PAGES:
        aid, off = PAGES[p['username']]
        for x in p['latestPosts']:
            d, hh, mi = local(x['timestamp'], off)
            abroad.append("  {a:'%s',d:D('%s'),h:%d,mi:%d,text:'%s',likes:%d,comments:%d,views:%d,fmt:'%s',prods:[%s],%surl:'%s'}" % (
                aid, d, hh, mi, js(x.get('caption')), max(0, x.get('likesCount') or 0), x.get('commentsCount') or 0, x.get('videoViewCount') or 0,
                FMT[x['type']], ','.join("'%s'" % q for q in prods_x(x.get('caption'))), 'pin:1,' if x.get('isPinned') else '', x['url']))
for x in load('ig_backfill.json', BACK):
    d, hh, _ = local(x['timestamp'], 'cairo')
    add(dict(d=d, h=hh, pl='ig', text=x.get('caption'), likes=max(0, x.get('likesCount') or 0), comments=x.get('commentsCount') or 0,
             shares=0, views=x.get('videoViewCount') or 0, fmt=FMT.get(x['type'], 'Image'), url=x['url']))
for x in load('tt_profile10.json') + load('tt_backfill.json', BACK) + load('tt_test.json', BACK):
    d, hh, _ = local(x['createTimeISO'], 'cairo')
    add(dict(d=d, h=hh, pl='tt', text=x.get('text'), likes=x.get('diggCount') or 0, comments=x.get('commentCount') or 0,
             shares=x.get('shareCount') or 0, views=x.get('playCount') or 0, fmt='Video', url=x['webVideoUrl']))
for x in load('yt_videos.json'):
    d, hh, _ = local(x['date'], 'cairo')
    add(dict(d=d, h=hh, pl='yt', text=x.get('title'), likes=x.get('likes') or 0, comments=x.get('commentsCount') or 0, shares=0,
             views=x.get('viewCount') or 0, fmt='Short' if x.get('type') == 'shorts' else 'Video', url=x['url']))
yp = os.path.join(BACK, 'yt_pages.json')
for x in (json.load(open(yp, encoding='utf-8'))['videos'] if os.path.exists(yp) else []):
    if not x.get('published'): continue
    d, hh, _ = local(x['published'], 'cairo')
    add(dict(d=d, h=hh, pl='yt', text=x.get('title'), likes=x.get('likes') or 0, comments=x.get('comments') or 0, shares=0,
             views=x.get('views') or x.get('list_views') or 0, fmt='Short' if x.get('type') == 'shorts' else 'Video', url=x['url']))
own.sort(key=lambda r: (r['d'], r['h']))

lines = ["  {d:D('%s'),h:%d,pl:'%s',prods:[%s],text:'%s',likes:%d,comments:%d,shares:%d,views:%d,fmt:'%s',%surl:'%s'}" % (
    r['d'], r['h'], r['pl'], ','.join("'%s'" % q for q in prods_eg(r['text'])), js(r['text']), r['likes'], r['comments'], r['shares'], r['views'],
    r['fmt'], 'boost:true,' if r['views'] >= 20 * FOL[r['pl']] else '', r['url']) for r in own]
REAL_OWN = ('/*REAL_OWN*//* V7 Egypt’s real posts (checked 13 Oct 2026): Facebook, TikTok and YouTube from 16 Apr (the first day), Instagram from 27 May.\n'
            '   Counts are as of 13 Oct. Demo posts fill only Instagram before 27 May. Posts with views 20+ times the followers were most likely promoted.\n'
            '   Built by data/raw/verify_13oct/build_own_posts.py */\n'
            'var REAL_OWN=[\n' + ',\n'.join(lines) + '\n];\n'
            "var OWN_REAL_FROM={" + ','.join("%s:D('%s')" % (k, v) for k, v in COVER.items()) + "};/*END_REAL_OWN*/")
REAL_OWN_X = ('/*REAL_OWN_X*/var REAL_OWN_X=[\n' + ',\n'.join(abroad) + '\n];/*END_REAL_OWN_X*/')
print(f'{len(own)} V7 Egypt posts, {sum(1 for r in own if r["views"] >= 20 * FOL[r["pl"]])} most likely promoted; {len(abroad)} posts from the pages abroad')

if '--inject' in sys.argv:
    html = open(DASH, encoding='utf-8').read()
    for name, block in (('REAL_OWN', REAL_OWN), ('REAL_OWN_X', REAL_OWN_X)):
        html, n = re.subn(r'/\*%s\*/.*?/\*END_%s\*/' % (name, name), lambda m: block, html, flags=re.S)
        if n != 1:
            sys.exit(f'{name} block not found in the dashboard')
    open(DASH, 'w', encoding='utf-8').write(html)
    print('injected into', os.path.basename(DASH))
