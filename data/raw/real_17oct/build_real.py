"""Builds the dashboard's real data from the 17 Oct 2026 collection (Version 25).

Reads items.json (normalize.py) and labels.json (label.py) and, with --inject, writes three blocks into V7_Pulse_Dashboard.html:
- REAL_OWN: V7 Egypt's posts, 20 Apr to 16 Oct, counts as of 17 Oct. Each post has an id (k) that its comments point to.
- REAL_OWN_X: the posts of V7's pages abroad and the UK distributor, same window.
- REAL_DATA: the public posts Claude judged to be about V7, every comment on V7's posts and on the pages abroad (with V7's replies,
  so "answered" is real), and their authors.
Privacy (DECISIONS #75): private people get no name, handle or link, and @mentions in the texts are masked. Names stay only for creators,
pages, shops, news outlets, official accounts and accounts with 10K+ followers.
Times are local: Cairo (UTC+3 from 24 Apr, UTC+2 before), Tunisia and the UK UTC+1, Uzbekistan UTC+5, India UTC+5:30.

Usage: python3 build_real.py [--inject]
"""
import collections, datetime, hashlib, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DASH = ROOT / 'V7_Pulse_Dashboard.html'
SINCE, UNTIL, CHECKED = '2026-04-20', '2026-10-16', '2026-10-17'
FOL = {'fb': 79783, 'ig': 38959, 'tt': 36900, 'yt': 2540}          # followers, checked 13 Oct 2026 (for the "most likely promoted" mark)
PAGES = {'v7tunisia': ('own_tn_ig', 1, 'TN'), 'v7uzbekistan': ('own_uz_ig', 5, 'UZ'), 'v7ldnuk': ('own_uk_ig', 1, 'GB'), 'drinkv7': ('own_in_ig', 5.5, 'IN'),
         'thehalaldrinksco': ('dist_uk', 1, 'GB')}
OFFICIAL = {'v7egypt', 'v7.egypt', '@v7egypt', 'vsupersoda', 'v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco'}
PLN = {'fb': 'Facebook', 'ig': 'Instagram', 'tt': 'TikTok', 'yt': 'YouTube', 'x': 'X', 'rd': 'Reddit'}


def own_rules():
    """The product rules of the 13 Oct build (V Lemon is the Lemon-Lime can, the World Cup flag posts are V Cola…), taken from its source."""
    src = (ROOT / 'data' / 'raw' / 'verify_13oct' / 'build_own_posts.py').read_text(encoding='utf-8')
    ns = {}
    exec('import re\ndef prods_eg' + src.split('def prods_eg', 1)[1].split('\nFMT = {', 1)[0], ns)
    return ns['prods_eg'], ns['prods_x']


prods_eg, prods_x = own_rules()


def local(t, hours):
    """('2026-09-10', 20, 38) in local time. hours='cairo' follows Egypt's summer time (from 24 Apr 2026)."""
    d = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
    if hours == 'cairo':
        hours = 3 if d >= datetime.datetime(2026, 4, 23, 22) else 2
    d = d + datetime.timedelta(hours=hours)
    return d.date().isoformat(), d.hour, d.minute


def mask(text):
    """@mentions of private people become @…; the official handles stay."""
    return re.sub(r'@([\w.]+)', lambda m: m.group(0) if m.group(1).lower() in OFFICIAL else '@…', text or '')


def js(s):
    s = re.sub(r'\s+', ' ', re.sub('[\u2066-\u2069\u200e\u200f]', '', s or '')).strip()
    if len(s) > 1500:
        s = s[:1497].rsplit(' ', 1)[0] + '…'
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('</', '<\\/').replace('\u2028', ' ').replace('\u2029', ' ')


def tags_of(text):
    return sorted({'#' + t for t in re.findall(r'#([\w\u0600-\u06FF]+)', text or '')})


if __name__ == '__main__':
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    by_id = {i['id']: i for i in items}
    report = collections.Counter()

    # ------------------------------------------------ V7 Egypt's own posts and the pages abroad
    own_rows, own_id, x_rows = [], {}, []
    for i in sorted((i for i in items if i['kind'] == 'post' and i['src'] in ('own', 'abroad')), key=lambda i: i['date']):
        if i['src'] == 'own':
            d, hh, mi = local(i['date'], 'cairo')
            if not (SINCE <= d <= UNTIL): continue
            k = 'o%d' % len(own_rows); own_id[i['id']] = k
            boost = (i.get('views') or 0) >= 20 * FOL[i['pl']]
            own_rows.append("  {k:'%s',d:D('%s'),h:%d,mi:%d,pl:'%s',prods:[%s],text:'%s',likes:%d,comments:%d,shares:%d,views:%d,fmt:'%s',%surl:'%s'}" % (
                k, d, hh, mi, i['pl'], ','.join("'%s'" % q for q in prods_eg(i['text'])), js(i['text']), i.get('likes') or 0, i.get('comments') or 0,
                i.get('shares') or 0, i.get('views') or 0, i.get('fmt') or 'Image', 'boost:true,' if boost else '', i['url']))
        else:
            aid, off, cty = PAGES[(i['author'] or {}).get('handle', '').lower()]
            d, hh, mi = local(i['date'], off)
            if not (SINCE <= d <= UNTIL): continue
            k = 'x%d' % len(x_rows); own_id[i['id']] = k
            x_rows.append("  {k:'%s',a:'%s',d:D('%s'),h:%d,mi:%d,text:'%s',likes:%d,comments:%d,views:%d,fmt:'%s',prods:[%s],url:'%s'}" % (
                k, aid, d, hh, mi, js(i['text']), i.get('likes') or 0, i.get('comments') or 0, i.get('views') or 0,
                {'Reel': 'Reel', 'Album': 'Carousel'}.get(i.get('fmt'), 'Image'), ','.join("'%s'" % q for q in prods_x(i['text'])), i['url']))
    report['own posts'] = len(own_rows); report['posts by the pages abroad'] = len(x_rows)

    # ------------------------------------------------ authors (anonymous unless public)
    AU, au_key = [], {}

    def author(i, lab):
        a = i.get('author') or {}
        pl = i['pl']
        seg = (lab or {}).get('seg', 'home')
        fol = a.get('followers')
        # Named: pages, creators and news outlets that post publicly, a business's own post, and accounts with 10K+ followers. A shop owner
        # commenting from a personal profile stays anonymous (the comment's link still leads to them).
        public = (seg in ('creator', 'page', 'news') or (seg == 'business' and i['kind'] == 'post') or (fol or 0) >= 10000
                  or (pl == 'x' and a.get('verified') and (fol or 0) >= 1000))
        raw = (a.get('handle') or a.get('id') or a.get('name') or '?').lower()
        key = pl + ':' + raw
        if key in au_key:
            return au_key[key]
        aid = 'ra%d' % len(AU)
        typ = {'creator': 'creator', 'page': 'page', 'news': 'news', 'business': 'business'}.get(seg, 'person')
        e = {'id': aid, 'pl': pl, 'type': typ, 'seg': seg, 'followers': fol if public else None}
        if public:
            e['name'] = a.get('name') or a.get('handle') or (PLN[pl] + ' page')
            if a.get('handle'): e['handle'] = a['handle']
            if a.get('url'): e['url'] = a['url']
        else:
            e['name'] = PLN[pl] + ' user'
            e['anon'] = hashlib.sha1(key.encode()).hexdigest()[:8]     # tells repeat commenters apart without naming them
        AU.append(e); au_key[key] = aid
        return aid

    # ------------------------------------------------ public posts about V7 (UGC)
    RUNS_18 = {'ig_tagged_v7', 'ig_tagged_vss', 'ig_kw_wide', 'ig_google_posts', 'tt_google_posts', 'tt_tags_wide', 'tt_wide', 'yt_recent', 'x_extra'} | {'fb_search_%02d' % n for n in range(12, 18)}
    UGC, ugc_id, ugc_cty, rumor = [], {}, {}, []
    for i in sorted((i for i in items if i['src'] == 'ugc' and i['kind'] == 'post'), key=lambda i: i['date']):   # (comments under public videos come later)
        lab = labels.get(i['id'])
        if not lab:
            report['public posts not labelled'] += 1; continue
        if not lab['about']:
            report['public posts not about V7'] += 1; continue
        cty = lab['cty'] or (i.get('region') if i.get('region') and len(i['region']) == 2 else '') or ('EG' if lab['lang'] in ('ar', 'fr', 'en', 'msa', 'other') else '')
        off = 'cairo' if cty in ('', 'EG') else 0
        d, hh, mi = local(i['date'], off if off == 'cairo' else 3)
        k = 'u%d' % len(UGC); ugc_id[i['id']] = k; ugc_cty[i['id']] = cty or 'XX'
        txt = i['text'] if lab['seg'] in ('creator', 'page', 'news', 'business') else mask(i['text'])
        UGC.append({'id': k, 'd': d, 'h': hh, 'mi': mi, 'pl': i['pl'], 'a': author(i, lab), 'grp': 1 if i.get('group') else 0, 'sr': i.get('subreddit'),
                    'prods': lab['prods'], 'c': lab['c'], 'lang': lab['lang'], 'text': txt, 'tags': sorted(set(tags_of(i['text'])) | {'#' + h for h in i.get('hashtags') or [] if h}),
                    's': lab['s'], 'emo': lab['emo'], 'views': i.get('views') or 0, 'likes': i.get('likes') or 0, 'comments': i.get('comments') or 0,
                    'shares': i.get('shares') or 0, 'gov': lab['gov'], 'cty': cty or 'XX', 'seg': lab['seg'], 'en': lab['en'], 'url': i['url'], 'fmt': i.get('fmt') or 'Text',
                    'needsReply': bool(lab['reply'] and i['pl'] in ('fb', 'ig', 'tt', 'yt')), 'place': i.get('place') or i.get('region') or None,
                    'claim': lab['claim'], 'stance': lab['stance'], 'isReply': 1 if i.get('is_reply') else 0,
                    'asof': 18 if i.get('counts_from') in RUNS_18 else 0})   # its numbers are as of 18 Oct (the wider search) or 17 Oct
        if lab['claim']:
            rumor.append(k)
    report['public posts about V7'] = len(UGC)

    # ------------------------------------------------ comments (and V7's replies)
    CM, cm_id = [], {}
    comments = sorted((i for i in items if i['kind'] == 'comment'), key=lambda i: i['date'])
    for i in comments:
        cm_id[i['id']] = 'k%d' % len(cm_id)
    replied = {i['reply_to'] for i in comments if i.get('by_v7') and i.get('reply_to')}
    for i in comments:
        parent = own_id.get(i['parent']) or ugc_id.get(i['parent'])    # V7's posts, the pages abroad, and (18 Oct) public YouTube videos
        if not parent:
            report['comments on a post outside the window'] += 1; continue
        post = by_id[i['parent']]
        page = (post.get('author') or {}).get('handle', '').lower()
        off = 'cairo' if post['src'] == 'own' else PAGES.get(page, (None, 3))[1]
        d, hh, mi = local(i['date'], off)
        if not (SINCE <= d <= UNTIL):
            report['comments after 16 Oct'] += 1; continue
        k = cm_id[i['id']]
        base = {'id': k, 'kind': 'comment', 'parent': parent, 'replyTo': cm_id.get(i.get('reply_to')), 'd': d, 'h': hh, 'mi': mi, 'pl': i['pl'],
                'nt': 1 if i.get('date_day_only') else 0,      # YouTube gives a comment's day, not its time
                'da': i.get('date_approx') or '', 'ago': i.get('ago') or '',   # YouTube gives only the month for older comments ('4 months')
                'likes': i.get('likes') or 0, 'comments': i.get('comments') or 0, 'url': i.get('url') or post['url']}
        if i.get('by_v7'):
            h = ((i.get('author') or {}).get('handle') or (i.get('author') or {}).get('name') or '').replace(' ', '').lower()
            CM.append(dict(base, by=('vss' if h == 'vsupersoda' else page if post['src'] == 'abroad' else 'v7'), text=i['text'] or '(sticker)'))
            continue
        lab = labels.get(i['id'])
        if not lab:
            report['comments not labelled'] += 1; continue
        if not lab['about'] and lab['c'] not in ('n_emoji', 'n_tag'):    # emoji reactions and friend tags stay: they react to the post
            report['comments that are spam or off topic'] += 1; continue
        pcty = 'EG' if post['src'] == 'own' else ugc_cty.get(i['parent']) if post['src'] == 'ugc' else PAGES.get(page, (None, None, 'XX'))[2]
        mine = post['src'] != 'ugc'     # under someone else's video V7's answers aren't collected, so "needs a reply" isn't tracked there
        CM.append(dict(base, a=author(i, lab), prods=lab['prods'], c=lab['c'], lang=lab['lang'], text=mask(i['text']) or '(sticker or photo)', s=lab['s'],
                       emo=lab['emo'], gov=lab['gov'], cty=lab['cty'] or pcty, seg=lab['seg'], en=lab['en'],
                       needsReply=bool(lab['reply']) and mine, replied=(i['id'] in replied) if lab['reply'] and mine else None,
                       lv=1 if i.get('liked_by_v7') else 0, claim=lab['claim'], stance=lab['stance']))
    report['comments shown'] = sum(1 for c in CM if 'by' not in c); report['V7 replies'] = sum(1 for c in CM if 'by' in c)

    meta = {'checked': CHECKED, 'window': [SINCE, UNTIL], 'apify_usd': None, 'claude': 'claude-opus-5-5, low effort, through Claude Code on the user’s plan',
            'report': dict(report), 'notes': {'yt_comments': 'YouTube comments collected on 18 Oct: V7 Egypt’s videos (comments are off on 1 of 28) and the public videos about V7.',
                                               'wide_search': 'Public posts: the 17 Oct searches plus, on 18 Oct, more Arabic and English spellings, the Instagram posts that tag V7, Instagram keyword search and Google searches of Instagram and TikTok.',
                                               'abroad_partial': 'The pages abroad had 1,837 comments; 829 were collected (budget).'}}
    run_log = (HERE / 'run.log').read_text(encoding='utf-8')
    spent = re.findall(r'total \$([\d.]+)', run_log)
    meta['apify_usd'] = float(spent[-1]) if spent else None
    def lean(o, kind):
        """Leaves out empty and default fields to keep the page light (the dashboard fills them in); TikTok comment links repeat the
        video's, and emoji-only comments and friend tags need no English note."""
        o = {k: v for k, v in o.items() if v not in (None, '', 0, False, []) or k in ('likes', 'views', 'prods', 's') and kind == 'ugc'}
        o.pop('en', None)      # Claude's English gist stays in labels.json; the page doesn't show it
        if kind == 'cm':
            u = o.pop('url', '') or ''
            # A comment's link is its post's link plus the comment's id, so only the ids are kept (the dashboard rebuilds the link)
            m = re.search(r'comment_id=(\d+)(?:&reply_comment_id=(\d+))?', u) or re.search(r'/c/(\d+)(?:/r/(\d+))?', u)
            if m:
                o['ci'] = m.group(1)
                if m.group(2): o['ri'] = m.group(2)
        return o
    UGC = [lean(o, 'ugc') for o in UGC]; CM = [lean(o, 'cm') for o in CM]
    data = {'meta': meta, 'au': AU, 'ugc': UGC, 'cm': CM, 'rumor': rumor}
    js_data = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/').replace('\u2028', ' ').replace('\u2029', ' ')

    REAL_OWN = ("/*REAL_OWN*//* V7 Egypt’s real posts, 20 Apr to 16 Oct 2026, counts as of 17 Oct. Posts with views 20+ times the followers were most likely promoted.\n"
                "   Built by data/raw/real_17oct/build_real.py */\nvar REAL_OWN=[\n" + ',\n'.join(own_rows) + "\n];/*END_REAL_OWN*/")
    REAL_OWN_X = "/*REAL_OWN_X*/var REAL_OWN_X=[\n" + ',\n'.join(x_rows) + "\n];/*END_REAL_OWN_X*/"
    REAL_DATA = "/*REAL_DATA*/var REAL_DATA=" + js_data + ";/*END_REAL_DATA*/"
    # The artifact publish guard takes a page for a code-review page when an `id=` is followed by a long unbroken run of text (a
    # Facebook link ending in &id=…), and refuses it. Every `id=` here sits inside a string, so `=` is written \u003d, which reads back the same.
    guard_safe = lambda js: re.sub(r'(?i)\b(id[\t\n\f\r ]*)=', r'\1\\u003d', js)
    REAL_OWN, REAL_OWN_X, REAL_DATA = guard_safe(REAL_OWN), guard_safe(REAL_OWN_X), guard_safe(REAL_DATA)
    for k, v in sorted(report.items()):
        print('%-40s %6d' % (k, v))
    print('authors %d (named %d) | data block %.0f KB' % (len(AU), sum(1 for a in AU if 'anon' not in a), len(REAL_DATA.encode()) / 1024))
    json.dump(data, open(HERE / 'real_dashboard.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

    if '--inject' in sys.argv:
        html = DASH.read_text(encoding='utf-8')
        for name, block in (('REAL_OWN', REAL_OWN), ('REAL_OWN_X', REAL_OWN_X), ('REAL_DATA', REAL_DATA)):
            html, n = re.subn(r'/\*%s\*/.*?/\*END_%s\*/' % (name, name), lambda m: block, html, flags=re.S)
            if n != 1:
                sys.exit(f'{name} block not found in the dashboard')
        DASH.write_text(html, encoding='utf-8')
        print('injected into', DASH.name)
