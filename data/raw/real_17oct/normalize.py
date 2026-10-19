"""One list of every real post and comment (17 Oct 2026), from the raw Apify files in raw/ and yt_pages.json.

Writes items.json: posts and comments in one shape, deduplicated, inside the window (20 Apr to 16 Oct 2026, Cairo time).
- src: own (V7 Egypt's posts), abroad (V7's pages abroad and the UK distributor) or ugc (anyone else's public posts).
- kind: post or comment. A comment has parent (its post's id); a reply also has reply_to (the comment it answers).
- by_v7: a comment written by one of V7's own accounts (its replies).
- X's filler rows ("From KaitoEasyAPI, a reminder…") and V7's own accounts in the search results are dropped.
Nothing here judges meaning: Claude labels the items next (label.py).

Usage: python3 normalize.py
"""
import collections, datetime, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
SINCE, UNTIL = '2026-04-20', '2026-10-16'
# V Super Soda is Benefit's page for the V Cola line; it answers comments under V7Egypt's posts like V7's own team (17 Oct check)
OWN_IG = {'v7egypt', 'vsupersoda'}
ABROAD_IG = {'v7tunisia', 'v7uzbekistan', 'v7ldnuk', 'drinkv7', 'thehalaldrinksco'}
OWN_TT, OWN_FB_NAMES, OWN_YT = {'v7.egypt', 'v.super.soda'}, {'v7egypt', 'vsupersoda'}, {'v7egypt', '@v7egypt'}


def load(name):
    p = RAW / (name + '.json')
    return json.load(open(p, encoding='utf-8'))['items'] if p.exists() else []


def num(x):
    try:
        v = int(float(x))
        return v if v >= 0 else None      # Instagram shows -1 when likes are hidden
    except (TypeError, ValueError):
        return None


def clean(s):
    return re.sub(r'[ \t]+', ' ', re.sub('[⁦-⁩‎‏​]', '', str(s or '').replace('\ufffd', ''))).strip()   # U+FFFD: a character the platform already lost


NOT_A_NAME = re.compile(r'access delayed|only the owner of the page', re.I)   # 19 Oct: the tagged scraper puts this where it couldn't read a full name


def iso(t):
    """Any of the actors' time formats as UTC ISO ('2026-09-10T17:38:16Z')."""
    if t is None or t == '':
        return None
    if isinstance(t, (int, float)) or re.fullmatch(r'\d{10,13}', str(t)):
        v = float(t)
        return datetime.datetime.fromtimestamp(v / 1000 if v > 1e11 else v, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    s = str(t)
    for fmt in ('%a %b %d %H:%M:%S %z %Y',):       # X: 'Wed Oct 14 10:12:06 +0000 2026'
        try:
            return datetime.datetime.strptime(s, fmt).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            pass
    try:
        d = datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
        if d.tzinfo:
            d = d.astimezone(datetime.timezone.utc)
        return d.strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return None


def cairo_day(t):
    """The date in Cairo: UTC+3 from 24 Apr 2026 (summer time), UTC+2 before."""
    d = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
    return (d + datetime.timedelta(hours=3 if d >= datetime.datetime(2026, 4, 23, 22) else 2)).date().isoformat()


def in_window(t):
    return bool(t) and SINCE <= cairo_day(t) <= UNTIL


ITEMS = collections.OrderedDict()
WHY_OUT = collections.Counter()


def add(it, run):
    if not it['date']:
        WHY_OUT['no date'] += 1; return
    if not in_window(it['date']):
        WHY_OUT[f'outside the window ({it["src"]} {it["kind"]})'] += 1; return
    if NOT_A_NAME.search((it.get('author') or {}).get('name') or ''):
        it['author']['name'] = None
    old = ITEMS.get(it['id'])
    if old:
        old['found_by'] = sorted(set(old['found_by']) | {run})
        # the same post from another source fills what the first one missed (apidojo's caption-less rows, shares from dami_studio)
        for k in ('text', 'likes', 'comments', 'shares', 'views', 'place', 'fmt'):
            if old.get(k) in (None, '') and it.get(k) not in (None, ''):
                old[k] = it[k]; old.setdefault('filled', []).append(k + ':' + run)
        if it.get('fmt') in ('Reel', 'Video') and old.get('fmt') in ('Image', 'Text'):   # 19 Oct: a video search knows it's a video
            old['fmt'] = it['fmt']
        if it.get('url') and it['url'] != old.get('url') and it['url'] not in old.get('urls', []):
            old.setdefault('urls', []).append(it['url'])
        for k in ('cover', 'video'):
            if it.get('media') and it['media'].get(k) and not (old.get('media') or {}).get(k):
                old.setdefault('media', {'images': []})[k] = it['media'][k]
        if it.get('media') and it['media'].get('images') and not (old.get('media') or {}).get('images'):
            old.setdefault('media', {})['images'] = it['media']['images']
        if it.get('duration') and not old.get('duration'):
            old['duration'] = it['duration']
        for k, v in (it.get('author') or {}).items():
            if (old.get('author') or {}).get(k) in (None, '') and v not in (None, ''):
                old.setdefault('author', {})[k] = v
        return
    it['found_by'] = [run]
    it['counts_from'] = run           # the run whose numbers it carries (the first that found it)
    ITEMS[it['id']] = it


def fmt_ig(p):
    t = (p.get('type') or '').lower()
    return 'Album' if t == 'sidecar' else 'Reel' if t == 'video' else 'Image'


# ---------------------------------------------------------------- V7's own posts and the pages abroad
def own_posts():
    for p in load('fb_posts'):
        add({'id': 'fb:' + str(p.get('postId') or p['url']), 'kind': 'post', 'src': 'own', 'pl': 'fb', 'date': iso(p.get('time')), 'text': clean(p.get('text')),
             'url': p.get('url'), 'author': {'name': 'V7Egypt', 'handle': 'V7Egypt'}, 'likes': num(p.get('likes')), 'comments': num(p.get('comments')),
             'shares': num(p.get('shares')), 'views': num(p.get('viewsCount')), 'fmt': 'Reel' if p.get('isVideo') else 'Image'}, 'fb_posts')
    for name, src in (('ig_posts', 'own'), ('abroad_posts', 'abroad')):
        for p in load(name):
            # A collaboration post shows on the V7 page's profile under the partner's name: file it under the page it came from
            page = (p.get('inputUrl') or '').rstrip('/').split('/')[-1] or p.get('ownerUsername')
            owner = p.get('ownerUsername') or ''
            author = {'name': p.get('ownerFullName'), 'handle': page}
            if owner.lower() != (page or '').lower():
                author['collab'] = owner
            add({'id': 'ig:' + str(p.get('shortCode') or p.get('id')), 'kind': 'post', 'src': src, 'pl': 'ig', 'date': iso(p.get('timestamp')),
                 'text': clean(p.get('caption')), 'url': p.get('url'), 'author': author,
                 'likes': num(p.get('likesCount')), 'comments': num(p.get('commentsCount')), 'shares': None,
                 'views': num(p.get('videoPlayCount')) or num(p.get('videoViewCount')), 'fmt': fmt_ig(p), 'hashtags': p.get('hashtags') or [],
                 'place': p.get('locationName')}, name)
    for p in load('tt_posts'):
        add({'id': 'tt:' + str(p.get('id')), 'kind': 'post', 'src': 'own', 'pl': 'tt', 'date': iso(p.get('createTimeISO')), 'text': clean(p.get('text')),
             'url': p.get('webVideoUrl'), 'author': {'name': 'V7 Egypt', 'handle': 'v7.egypt'}, 'likes': num(p.get('diggCount')),
             'comments': num(p.get('commentCount')), 'shares': num(p.get('shareCount')), 'views': num(p.get('playCount')), 'fmt': 'Video',
             'hashtags': [h.get('name') for h in p.get('hashtags') or [] if h.get('name')]}, 'tt_posts')
    pages = {v['id']: v for v in json.load(open(HERE / 'yt_pages.json', encoding='utf-8'))['videos']} if (HERE / 'yt_pages.json').exists() else {}
    # 18 Oct: calm_builder's rows give each video's original title (the 17 Oct scraper returned English machine translations) and its
    # real comment count (yt_pages.py read every video as "comments turned off", which only one of the 28 is)
    chk = {}
    for x in load('yt_own_check'):
        v = re.search(r'(?:v=|shorts/)([\w-]{11})', x.get('url') or '')
        if v: chk[v.group(1)] = x
    for p in load('yt_posts'):
        vid = re.search(r'(?:v=|shorts/)([\w-]{11})', p.get('url') or '')
        pg = dict(pages.get(vid.group(1) if vid else '', {}))
        ck = chk.get(vid.group(1) if vid else '')
        if ck:
            p = dict(p, title=ck.get('title') or p.get('title'))
            pg['comments'] = num(ck.get('commentCount'))
        add({'id': 'yt:' + (vid.group(1) if vid else p.get('id')), 'kind': 'post', 'src': 'own', 'pl': 'yt', 'date': iso(pg.get('published')),
             'text': clean(p.get('title')), 'url': p.get('url'), 'author': {'name': 'V7 Egypt', 'handle': '@V7Egypt'},
             'likes': pg.get('likes') if pg.get('likes') is not None else num(p.get('likes')), 'comments': pg.get('comments') if pg.get('comments') is not None else num(p.get('commentsCount')),
             'shares': None, 'views': pg.get('views') or num(p.get('viewCount')), 'fmt': 'Short' if (p.get('type') or '').lower().startswith('short') or '/shorts/' in (p.get('url') or '') else 'Video'},
            'yt_posts')


# ---------------------------------------------------------------- comments on V7's posts (and the pages abroad)
def post_id_for(url):
    """The item id of the post a comment belongs to, from its URL."""
    u = url or ''
    m = re.search(r'instagram\.com/(?:[\w.]+/)?(?:p|reel)/([\w-]+)', u)
    if m: return 'ig:' + m.group(1)
    m = re.search(r'tiktok\.com/@[\w.]+/video/(\d+)', u)
    if m: return 'tt:' + m.group(1)
    for it in ITEMS.values():
        if it['kind'] == 'post' and it['pl'] == 'fb' and it['url'] and u.split('?')[0].rstrip('/') == it['url'].split('?')[0].rstrip('/'):
            return it['id']
    return None


def comments():
    fb_parents = {}
    for c in load('fb_comments'):
        pid = post_id_for(c.get('facebookUrl') or c.get('inputUrl'))
        if not pid: WHY_OUT['FB comment on an unknown post'] += 1; continue
        cu = c.get('commentUrl') or ''
        reply = re.search(r'reply_comment_id=(\d+)', cu)
        top = re.search(r'comment_id=(\d+)', cu)
        cid = 'fbc:' + str(c.get('id') or c.get('commentId'))
        depth = num(c.get('threadingDepth')) or 0
        name = (c.get('profileName') or '')
        it = {'id': cid, 'kind': 'comment', 'src': ITEMS[pid]['src'], 'pl': 'fb', 'date': iso(c.get('date')), 'text': clean(c.get('text')), 'url': cu or c.get('facebookUrl'),
              'author': {'name': name, 'id': c.get('profileId'), 'url': c.get('profileUrl')}, 'likes': num(c.get('likesCount')),
              'comments': num(c.get('commentsCount')), 'shares': None, 'views': None, 'parent': pid, 'depth': depth,
              'by_v7': name.replace(' ', '').lower() in OWN_FB_NAMES, 'has_media': bool(c.get('attachments'))}
        if top: fb_parents[(pid, top.group(1))] = fb_parents.get((pid, top.group(1))) or (cid if depth == 0 else None)
        it['_top'] = top.group(1) if top else None
        it['_reply'] = bool(reply) or depth > 0
        add(it, 'fb_comments')
    for it in ITEMS.values():          # a Facebook reply answers the top comment in its thread
        if it['pl'] == 'fb' and it['kind'] == 'comment':
            if it.pop('_reply') and it.get('_top'):
                it['reply_to'] = fb_parents.get((it['parent'], it['_top']))
            it.pop('_top', None)
    for name in ('ig_comments', 'abroad_comments'):
        for c in load(name):
            pid = post_id_for(c.get('postUrl') or c.get('commentUrl'))
            if not pid or pid not in ITEMS: WHY_OUT['IG comment on an unknown post'] += 1; continue
            base = {'kind': 'comment', 'src': ITEMS[pid]['src'], 'pl': 'ig', 'parent': pid, 'shares': None, 'views': None}

            def ig(x, reply_to=None):
                u = (x.get('ownerUsername') or (x.get('owner') or {}).get('username') or '')
                it = dict(base, id='igc:' + str(x.get('id')), date=iso(x.get('timestamp')), text=clean(x.get('text')), url=x.get('commentUrl') or c.get('postUrl'),
                          author={'name': u, 'handle': u, 'verified': (x.get('owner') or {}).get('is_verified')}, likes=num(x.get('likesCount')),
                          comments=num(x.get('repliesCount')), by_v7=u.lower() in OWN_IG | ABROAD_IG)
                if reply_to: it['reply_to'] = reply_to
                add(it, name)
            m = re.search(r'/c/(\d+)/r/(\d+)', c.get('commentUrl') or '')   # a reply's link: …/c/<the comment it answers>/r/<the reply>
            ig(c, 'igc:' + m.group(1) if m else None)
            for r in c.get('replies') or []:                                    # (the actor lists replies as items, not nested)
                ig(r, 'igc:' + str(c.get('id')))
    for c in load('tt_comments'):
        pid = post_id_for(c.get('videoWebUrl'))
        if not pid or pid not in ITEMS: WHY_OUT['TikTok comment on an unknown post'] += 1; continue
        u = c.get('uniqueId') or ''
        it = {'id': 'ttc:' + str(c.get('cid')), 'kind': 'comment', 'src': ITEMS[pid]['src'], 'pl': 'tt', 'parent': pid, 'date': iso(c.get('createTimeISO')),
              'text': clean(c.get('text')), 'url': c.get('videoWebUrl'), 'author': {'name': u, 'handle': u}, 'likes': num(c.get('diggCount')),
              'comments': num(c.get('replyCommentTotal')), 'shares': None, 'views': None, 'by_v7': u.lower() in OWN_TT,
              'liked_by_v7': bool(c.get('likedByAuthor')), 'pinned': bool(c.get('pinnedByAuthor'))}
        if c.get('repliesToId'): it['reply_to'] = 'ttc:' + str(c['repliesToId'])
        add(it, 'tt_comments')


# ---------------------------------------------------------------- public posts by anyone else (UGC)
def ugc():
    for f in sorted(RAW.glob('x_*.json')):
        for t in json.load(open(f, encoding='utf-8'))['items']:
            text = clean(t.get('text'))
            if not t.get('id') or 'kaitoeasyapi' in text.lower() or t.get('type') not in (None, 'tweet'):
                WHY_OUT['X filler or not a post'] += 1; continue
            a = t.get('author') or {}
            add({'id': 'x:' + str(t['id']), 'kind': 'post', 'src': 'ugc', 'pl': 'x', 'date': iso(t.get('createdAt')), 'text': text, 'url': t.get('url') or t.get('twitterUrl'),
                 'author': {'name': a.get('name'), 'handle': a.get('userName'), 'followers': num(a.get('followers')), 'verified': bool(a.get('isBlueVerified') or a.get('isVerified')),
                            'url': a.get('url')}, 'likes': num(t.get('likeCount')), 'comments': num(t.get('replyCount')),
                 'shares': (num(t.get('retweetCount')) or 0) + (num(t.get('quoteCount')) or 0), 'views': num(t.get('viewCount')), 'fmt': 'Text',
                 'is_reply': bool(t.get('isReply')), 'reply_to_user': t.get('inReplyToUsername'), 'lang_hint': t.get('lang')}, f.stem)
    for f in sorted(RAW.glob('fb_search_*.json')):
        body = json.load(open(f, encoding='utf-8'))
        for p in body['items']:
            a = p.get('author') or {}
            if (a.get('name') or '').replace(' ', '').lower() in OWN_FB_NAMES:
                WHY_OUT['V7 itself in the search'] += 1; continue
            fb_post(fb_one_item(p, body), f.stem)   # 19 Oct: the shared Facebook reader (reels and videos told apart from photos)
    # Instagram: the 17 Oct hashtags, then (18 Oct) posts tagging V7's accounts, Google's finds and Instagram's keyword search
    for name in ('ig_tags', 'ig_tags2', 'ig_tagged_v7', 'ig_tagged_v7_full', 'ig_tagged_vss', 'ig_google_posts', 'ig_google2_posts', 'ig_kw_wide', 'ig_kw_wide2') + tuple(f.stem for f in sorted(RAW.glob('igkw_*_refetch.json'))):
        kw = name.startswith('ig_kw_wide')           # seemuapps' keyword search names its fields differently
        for p in load(name):
            code = p.get('shortcode') if kw else p.get('shortCode')
            if not code:
                WHY_OUT['not a post (an error row)'] += 1; continue
            u = (p.get('ownerUsername') or '').lower()
            if u in OWN_IG | ABROAD_IG:
                WHY_OUT['V7 itself in the search'] += 1; continue
            if kw:
                add({'id': 'ig:' + code, 'kind': 'post', 'src': 'ugc', 'pl': 'ig', 'date': iso(p.get('takenAt')), 'text': clean(p.get('caption')), 'url': p.get('url'),
                     'author': {'name': p.get('ownerFullName'), 'handle': p.get('ownerUsername'), 'followers': num(p.get('ownerFollowerCount')),
                                'verified': bool(p.get('ownerIsVerified'))}, 'likes': num(p.get('likeCount')), 'comments': num(p.get('commentCount')),
                     'shares': None, 'views': num(p.get('playCount')), 'fmt': {'carousel': 'Album', 'reel': 'Reel', 'video': 'Reel'}.get(p.get('type'), 'Image'),
                     'hashtags': p.get('hashtags') or [], 'place': p.get('locationName'), 'query': p.get('keyword')}, name)
                continue
            add({'id': 'ig:' + code, 'kind': 'post', 'src': 'ugc', 'pl': 'ig', 'date': iso(p.get('timestamp')), 'text': clean(p.get('caption')),
                 'url': p.get('url'), 'author': {'name': p.get('ownerFullName'), 'handle': p.get('ownerUsername')}, 'likes': num(p.get('likesCount')),
                 'comments': num(p.get('commentsCount')), 'shares': num(p.get('sharesCount')), 'views': num(p.get('videoPlayCount')) or num(p.get('videoViewCount')),
                 'fmt': fmt_ig(p), 'hashtags': p.get('hashtags') or [], 'place': p.get('locationName')}, name)
    for f in sorted(RAW.glob('igkw_*.json')):      # 19 Oct on: Instagram keyword search with apidojo (DECISIONS #133)
        if f.stem.endswith('_refetch'):
            continue                               # (read above, with the other post-scraper files)
        for p in json.load(open(f, encoding='utf-8'))['items']:
            code, o = p.get('code'), p.get('owner') or {}
            if not code:
                WHY_OUT['not a post (an error row)'] += 1; continue
            if (o.get('username') or '').lower() in OWN_IG | ABROAD_IG:
                WHY_OUT['V7 itself in the search'] += 1; continue
            cap = clean(p.get('caption'))
            add({'id': 'ig:' + code, 'kind': 'post', 'src': 'ugc', 'pl': 'ig', 'date': iso(p.get('createdAt')), 'text': cap, 'url': p.get('url'),
                 'author': {'name': o.get('fullName'), 'handle': o.get('username'), 'verified': bool(o.get('isVerified'))},
                 'likes': num(p.get('likeCount')), 'comments': num(p.get('commentCount')), 'shares': None, 'views': num((p.get('video') or {}).get('playCount')),
                 'fmt': 'Album' if p.get('isCarousel') else 'Reel' if p.get('isVideo') else 'Image', 'hashtags': re.findall(r'#(\w+)', cap),
                 'place': (p.get('location') or {}).get('name') if isinstance(p.get('location'), dict) else None, 'query': p.get('inputSource')}, f.stem)
    for f in sorted(RAW.glob('igreels_*.json')):   # 19 Oct on: Instagram's Reels search with dami_studio (DECISIONS #134)
        for p in json.load(open(f, encoding='utf-8'))['items']:
            if p.get('recordType') != 'instagram_reel' or not p.get('shortcode'):
                WHY_OUT['not a post (a run summary or error row)'] += 1; continue
            if (p.get('authorUsername') or '').lower() in OWN_IG | ABROAD_IG:
                WHY_OUT['V7 itself in the search'] += 1; continue
            add({'id': 'ig:' + p['shortcode'], 'kind': 'post', 'src': 'ugc', 'pl': 'ig', 'date': iso(p.get('timestamp')), 'text': clean(p.get('caption')),
                 'url': p.get('reelUrl'), 'author': {'name': p.get('authorFullName'), 'handle': p.get('authorUsername'), 'verified': bool(p.get('authorIsVerified'))},
                 'likes': num(p.get('likeCount')), 'comments': num(p.get('commentCount')), 'shares': num(p.get('shareCount')), 'views': num(p.get('playCount')),
                 'fmt': 'Reel', 'hashtags': p.get('hashtags') or [], 'place': p.get('locationName'), 'query': p.get('sourceQuery') or p.get('sourceHashtag')}, f.stem)
    for name in ('tt_search', 'tt_google_posts', 'tt_tags_wide', 'tt_wide'):
        for p in load(name):
            if not p.get('id') or not p.get('webVideoUrl'):
                WHY_OUT['not a post (an error row)'] += 1; continue
            am = p.get('authorMeta') or {}
            if (am.get('name') or '').lower() in OWN_TT:
                WHY_OUT['V7 itself in the search'] += 1; continue
            add({'id': 'tt:' + str(p.get('id')), 'kind': 'post', 'src': 'ugc', 'pl': 'tt', 'date': iso(p.get('createTimeISO')), 'text': clean(p.get('text')),
                 'url': p.get('webVideoUrl'), 'author': {'name': am.get('nickName'), 'handle': am.get('name'), 'followers': num(am.get('fans')), 'verified': bool(am.get('verified'))},
                 'likes': num(p.get('diggCount')), 'comments': num(p.get('commentCount')), 'shares': num(p.get('shareCount')), 'views': num(p.get('playCount')),
                 'fmt': 'Video', 'hashtags': [h.get('name') for h in p.get('hashtags') or [] if h.get('name')], 'region': p.get('locationCreated'),
                 'query': p.get('searchQuery') or p.get('input')}, name)
    for name in ('yt_search', 'yt_recent'):
        for p in load(name):
            if (p.get('channelUsername') or '').lower() in OWN_YT or (p.get('channelName') or '') == 'V7 Egypt':
                WHY_OUT['V7 itself in the search'] += 1; continue
            vid = re.search(r'(?:v=|shorts/)([\w-]{11})', p.get('url') or '')
            add({'id': 'yt:' + (vid.group(1) if vid else str(p.get('id'))), 'kind': 'post', 'src': 'ugc', 'pl': 'yt', 'date': iso(p.get('date')),
                 'text': clean((p.get('title') or '') + ('\n' + p['text'][:600] if p.get('text') else '')), 'url': p.get('url'),
                 'author': {'name': p.get('channelName'), 'handle': p.get('channelUsername'), 'followers': num(p.get('numberOfSubscribers')), 'url': p.get('channelUrl')},
                 'likes': num(p.get('likes')), 'comments': num(p.get('commentsCount')), 'shares': None, 'views': num(p.get('viewCount')),
                 'fmt': 'Short' if '/shorts/' in (p.get('url') or '') else 'Video', 'query': (p.get('input') or p.get('fromYTUrl'))}, name)
    for p in load('reddit'):
        kind = 'comment' if p.get('dataType') == 'comment' else 'post'
        add({'id': 'rd:' + str(p.get('id') or p.get('url')), 'kind': 'post', 'src': 'ugc', 'pl': 'rd', 'date': iso(p.get('createdAt')),
             'text': clean(((p.get('title') or '') + '\n' + (p.get('body') or '')).strip()), 'url': p.get('url'),
             'author': {'name': 'Reddit user', 'handle': None}, 'likes': num(p.get('upVotes')), 'comments': num(p.get('numberOfComments')), 'shares': None,
             'views': None, 'fmt': 'Text', 'subreddit': p.get('communityName') or p.get('parsedCommunityName'), 'reddit_kind': kind}, 'reddit')


# ---------------------------------------------------------------- YouTube comments (18 Oct), on V7's videos and on public videos about V7
V7_YT_CHANNEL = 'UC35wXwTFBY5IeytYYkGc89g'


def yt_when(text, ran):
    """A YouTube comment's day from what the page shows. YouTube gives the day for recent comments ("8 days ago") and only the
    month for older ones ("4 months ago"); the scraper turns some of each into a date, a month's on the day of the run (18 May,
    18 Jun …). Returns (day, None) for a known day, (estimated day, 'm' or 'w') when only the month or week is known."""
    t = re.sub(r'\s*\(edited\)', '', str(text or '')).strip()
    run_day = datetime.date.fromisoformat(ran[:10])
    m = re.match(r'(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago$', t)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        if unit in ('second', 'minute', 'hour'): return run_day, None
        if unit == 'day': return run_day - datetime.timedelta(days=n), None
        if unit == 'week': return run_day - datetime.timedelta(days=7 * n), 'w'
        if unit == 'month':
            y, mo = divmod(run_day.year * 12 + run_day.month - 1 - n, 12)
            return datetime.date(y, mo + 1, min(run_day.day, 28)), 'm'
        return None, None
    m = re.match(r'(\d{4}-\d\d-\d\d)', t)
    if m:
        day = datetime.date.fromisoformat(m.group(1))
        return day, ('m' if day.day == run_day.day and (run_day - day).days >= 28 else None)
    return None, None


def ago_text(day, approx, ran):
    """How long before the run YouTube said the comment was: '4 months', '3 weeks'."""
    r = datetime.date.fromisoformat(ran[:10])
    n = (r.year * 12 + r.month) - (day.year * 12 + day.month) if approx == 'm' else (r - day).days // 7
    return '%d %s%s' % (n, 'month' if approx == 'm' else 'week', '' if n == 1 else 's')


def yt_comments():
    for name in ('yt_comments_own', 'yt_comments_public'):
        body = json.load(open(RAW / (name + '.json'), encoding='utf-8')) if (RAW / (name + '.json')).exists() else {'items': [], 'run': {}}
        ran = (body.get('run') or {}).get('startedAt') or '2026-10-18'
        for c in body['items']:
            vid = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', c.get('inputSource') or '')
            pid = 'yt:' + vid.group(1) if vid else None
            if not pid or pid not in ITEMS or not c.get('id'):
                WHY_OUT['YouTube comment on an unknown video'] += 1; continue
            a = c.get('author') or {}
            cid = str(c['id'])
            day, approx = yt_when(c.get('publishedTime'), ran)
            it = {'id': 'ytc:' + cid, 'kind': 'comment', 'src': ITEMS[pid]['src'], 'pl': 'yt', 'parent': pid,
                  'date': day.isoformat() + 'T09:00:00Z' if day else None,      # the day only (09:00 UTC is noon in Cairo, so the day doesn't shift)
                  'date_day_only': True, 'date_approx': approx, 'ago': ago_text(day, approx, ran) if approx else None, 'text': clean(c.get('text')), 'url': ITEMS[pid]['url'], 'author': {'name': a.get('name'), 'handle': a.get('name')},
                  'likes': num(c.get('likeCount')), 'comments': num(c.get('replyCount')), 'shares': None, 'views': None,
                  'by_v7': a.get('id') == V7_YT_CHANNEL}
            if '.' in cid: it['reply_to'] = 'ytc:' + cid.split('.')[0]      # a reply's id is <the comment it answers>.<its own key>
            add(it, name)


# ---------------------------------------------------------------- 19 Oct: reels' speech and Instagram follower counts
def extras():
    speech = {}
    for f in [RAW / 'kw_transcript_test.json'] + sorted(RAW.glob('igspeech_*.json')):
        if f.exists():
            for x in json.load(open(f, encoding='utf-8'))['items']:
                t = clean(x.get('text'))
                if x.get('code') and t:
                    speech[x['code']] = t
    prof = {}
    for f in sorted(RAW.glob('ig_profiles*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            if x.get('username'): prof[x['username'].lower()] = x
    n_sp = n_fol = n_name = 0
    for it in ITEMS.values():
        if it['pl'] != 'ig':
            continue
        if it['kind'] == 'post' and it['id'][3:] in speech:
            it['speech'] = speech[it['id'][3:]]; n_sp += 1
        a = it.get('author') or {}
        pr = prof.get((a.get('handle') or '').lower())
        if pr:
            if a.get('followers') is None and pr.get('followersCount') is not None:
                a['followers'] = num(pr['followersCount']); n_fol += 1
            if not a.get('verified') and pr.get('verified'):
                a['verified'] = True
            if not a.get('name') and clean(pr.get('fullName')):
                a['name'] = clean(pr['fullName']); n_name += 1
            it['author'] = a
    print('speech attached to %d Instagram posts | follower counts filled on %d Instagram items | names from profiles on %d' % (n_sp, n_fol, n_name))


def ig_ugc_comments():
    """19 Oct: comments under public Instagram posts (scrapesmith), anonymous like the others; V7's own accounts count as V7's replies."""
    for f in sorted(RAW.glob('igcm_*.json')):
        for c in json.load(open(f, encoding='utf-8'))['items']:
            code = (c.get('postUrl') or '').rstrip('/').split('/')[-1]
            pid = 'ig:' + code
            cid = c.get('commentId') or c.get('id')       # scrapesmith names it commentId, Apify's own scraper id
            if not cid or pid not in ITEMS:
                WHY_OUT['IG comment on an unknown post'] += 1; continue
            u = c.get('username') or c.get('ownerUsername') or ''
            add({'id': 'igc:' + str(cid), 'kind': 'comment', 'src': ITEMS[pid]['src'], 'pl': 'ig', 'parent': pid, 'date': iso(c.get('timestamp')),
                 'text': clean(c.get('text')), 'url': c.get('commentUrl') or ITEMS[pid]['url'], 'author': {'name': u, 'handle': u, 'verified': bool(c.get('isVerified'))},
                 'likes': num(c.get('likesCount')), 'comments': num(c.get('repliesCount')), 'shares': None, 'views': None, 'by_v7': u.lower() in OWN_IG | ABROAD_IG}, f.stem)


# ---------------------------------------------------------------- 19 Oct: Facebook from every route (collect.py fbcover, fbdetails, fbfill)
# The same Facebook post comes back under its post id from the post searches and under its video id from the video and reel searches.
# Rows that carry both (a post id and a /reel/ or /videos/ link) link the two, so a post is counted once: fb:<post id> when it's known,
# fb:v<video id> otherwise.
FB_ALIAS = {}


def fb_files(*patterns):
    """The raw files of one Facebook format: the 19 Oct collection and the comparison runs that share its format."""
    out = []
    for pat in patterns:
        out += sorted(RAW.glob(pat + '.json'))
    return list(dict.fromkeys(out))


FB_SILENT_FILES = ('fbc_silent_*', 'fbd_posts*', 'fbkw_silentflow_*', 'fbkw_scrapeforge_*', 'fbkw_danek_*', 'fbkw_igview_*', 'fbdeep_silentflow_*',
                   'fbdeep_scrapeforge_top', 'fbdeep_month_*', 'fbgap_danek', 'fbkw_topapi', 'fbdeep_topapi_*', 'fbgap_topapi_details', 'fbm_forge_*')
FB_ONE_FILES = ('fbc_one_*', 'fbkw_scraperone_*', 'fbkw_fetchcat_*', 'fbm_fetchcat_*')
FB_APIFY_FILES = ('fbc_apify_*', 'fbkw_apify_*')
FB_HEADPLY_FILES = ('fbc_vheadply', 'fbvs_headply', 'fbkw_headply')
FB_ALPHA_FILES = ('fbd_reels*', 'fbd_videos*', 'fbgap_reeldetails')
FB_LOFO_FILES = ('fbc_groups', 'fbgroups_lofo')


def fb_vid(url):
    m = re.search(r'(?:/reel/|/videos/(?:[^/?]+/)?|[?&]v=)(\d{8,})', url or '')
    return m.group(1) if m else None


def fb_pnum(url):
    m = re.search(r'(?:/posts/(?:[^/?]+/)?|story_fbid=|/permalink/|[?&]fbid=)(\d{8,})', url or '')
    return m.group(1) if m else None


def fb_alias(post_id, url=None, video_id=None):
    vid = str(video_id) if video_id else fb_vid(url)
    if post_id and vid and str(post_id) != vid:
        FB_ALIAS.setdefault(vid, str(post_id))


def fb_key(post_id=None, url=None, video_id=None):
    vid = str(video_id) if video_id else fb_vid(url)
    pid = str(post_id) if post_id else fb_pnum(url)
    if pid and pid != vid:
        return 'fb:' + pid
    if vid:
        return 'fb:' + FB_ALIAS[vid] if vid in FB_ALIAS else 'fb:v' + vid
    if pid:
        return 'fb:' + pid
    return 'fb:' + (url or '').split('?')[0].rstrip('/') if url else None


def fb_fmt(url, typ=None, video=False, n_images=0):
    u, t = url or '', str(typ or '').lower()
    if '/reel/' in u or t == 'reel':
        return 'Reel'
    if video or t in ('video', 'search_video') or '/videos/' in u or 'watch' in u:
        return 'Video'
    return 'Album' if n_images > 1 else 'Image' if n_images == 1 or t in ('photo', 'image') else 'Text'


OWN_FB_IDS = set()   # V7's own pages' account ids, read from any row that names them (a search row can come without the name)


def fb_own(name, url=None, aid=None):
    return ((name or '').replace(' ', '').lower() in OWN_FB_NAMES or bool(re.search(r'facebook\.com/(?:V7Egypt|Vsupersoda)(?:[/?]|$)', url or '', re.I))
            or bool(aid and str(aid) in OWN_FB_IDS))


def fb_post(it, run):
    """Adds a public Facebook post; V7's own pages are left out (collected as V7's posts)."""
    a = it.get('author') or {}
    if fb_own(a.get('name'), a.get('url'), a.get('id')):
        WHY_OUT['V7 itself in the search'] += 1; return
    if not it['id']:
        WHY_OUT['not a post (an error row)'] += 1; return
    g = re.search(r'facebook\.com/groups/([\w.]+)/', it.get('url') or '')
    it.setdefault('group', {'id': g.group(1)} if g else None)
    it.update(kind='post', src='ugc', pl='fb')
    add(it, run)


def fb_aliases():
    """First pass: every row that has a post id and a video id, and the account ids of V7's own pages."""
    for f in sorted(RAW.glob('fb_search_*.json')) + sorted(RAW.glob('fb*.json')):
        for p in json.load(open(f, encoding='utf-8')).get('items', []):
            if isinstance(p, dict):
                for a in (p.get('author'), p.get('user'), {'name': p.get('authorName'), 'id': p.get('authorId')}, p.get('owner')):
                    if isinstance(a, dict) and a.get('id') and (a.get('name') or '').replace(' ', '').lower() in OWN_FB_NAMES:
                        OWN_FB_IDS.add(str(a['id']))
    for f in sorted(RAW.glob('fb_search_*.json')) + fb_files(*FB_ONE_FILES, *FB_APIFY_FILES, *FB_HEADPLY_FILES):
        for p in json.load(open(f, encoding='utf-8'))['items']:
            fb_alias(p.get('postId'), p.get('url'))
    for f in fb_files(*FB_SILENT_FILES):
        for p in json.load(open(f, encoding='utf-8'))['items']:
            fb_alias(p.get('post_id'), p.get('url'), p.get('video_id'))
    for f in fb_files(*FB_ALPHA_FILES):
        for p in json.load(open(f, encoding='utf-8'))['items']:
            v = p.get('video') or {}
            fb_alias((p.get('post') or {}).get('post_id'), v.get('url'), v.get('id'))


def fb_ugc():
    """Public Facebook posts about V7 from the 19 Oct routes. Rows without an exact time (the reel search, two video searches) were
    fetched again by link (fbd_*) and are read from there."""
    for f in fb_files(*FB_SILENT_FILES):   # silentflow's search, danek's posts by link and topapi: one format
        body = json.load(open(f, encoding='utf-8'))
        for p in body['items']:
            if not isinstance(p, dict) or not p.get('timestamp'):
                WHY_OUT['not a post (an error row)'] += 1; continue
            a = p.get('author') or {}
            url = p.get('url') or (p.get('browser_video') or {}).get('url') or ('https://www.facebook.com/reel/%s/' % p['video_id'] if p.get('video_id') else None)
            album = [x.get('image_file_uri') or x.get('uri') for x in p.get('album_preview') or [] if isinstance(x, dict)]
            vfile = (p.get('video_files') or {}).get('video_sd_file') if isinstance(p.get('video_files'), dict) else None
            reps = [r.get('base_url') or r.get('url') for r in p.get('representations') or [] if isinstance(r, dict) and 'video' in str(r.get('mime_type', 'video'))]
            video = vfile or (p.get('video') if isinstance(p.get('video'), str) and p.get('video').startswith('http') else None) or (reps[0] if reps else None)
            imgs = [u for u in ([p.get('image')] if isinstance(p.get('image'), str) and p.get('image') else []) + [u for u in album if u]
                    + [x if isinstance(x, str) else (x or {}).get('uri') or (x or {}).get('url') for x in p.get('images') or []] if u]
            plays = p.get('video_view_count') or p.get('play_count_text')
            fb_post({'id': fb_key(p.get('post_id'), url, p.get('video_id')), 'date': iso(p['timestamp']), 'text': clean(p.get('message') or p.get('description')),
                     'url': url, 'author': {'name': a.get('name'), 'id': a.get('id'), 'url': a.get('url')}, 'likes': num(p.get('reactions_count')),
                     'comments': num(p.get('comments_count')), 'shares': num(p.get('reshare_count')), 'views': fb_count(plays),
                     'fmt': fb_fmt(url, p.get('type'), bool(video or p.get('video_id')), len(set(imgs))), 'is_share': bool(p.get('attached_post')),
                     'media': {'cover': p.get('video_thumbnail') or p.get('thumbnail_uri') or None, 'video': video, 'images': list(dict.fromkeys(imgs))},
                     'query': (body.get('input') or {}).get('query')}, f.stem)
    for f in fb_files(*FB_ONE_FILES):                                             # scraper_one (the 17 Oct format) and fetch_cat
        body = json.load(open(f, encoding='utf-8'))
        for p in body['items']:
            fb_post(fb_one_item(p, body), f.stem)
    for f in fb_files(*FB_APIFY_FILES):                                           # Apify's own search
        body = json.load(open(f, encoding='utf-8'))
        for p in body['items']:
            if not p.get('postId') or not p.get('timestamp'):
                WHY_OUT['not a post (an error row)'] += 1; continue
            u = p.get('user') or {}
            med = [m for m in p.get('media') or [] if isinstance(m, dict)]
            imgs = [((m.get('photo_image') or {}).get('uri') or m.get('thumbnail')) for m in med if m.get('__typename') == 'Photo' or m.get('photo_image')]
            fb_post({'id': fb_key(p.get('postId'), p.get('url')), 'date': iso(p.get('timestamp')), 'text': clean(p.get('text')), 'url': p.get('url'),
                     'author': {'name': u.get('name') or (p.get('pageName') or {}).get('name'), 'id': u.get('id'), 'url': u.get('profileUrl')},
                     'likes': num(p.get('likes')), 'comments': num(p.get('comments')), 'shares': num(p.get('shares')), 'views': num(p.get('videoPostViewCount')),
                     'fmt': fb_fmt(p.get('url'), None, bool(p.get('isVideo')), len([i for i in imgs if i])),
                     'media': {'cover': next((m.get('thumbnail') for m in med if m.get('thumbnail')), None), 'video': None, 'images': [i for i in imgs if i]},
                     'query': ((body.get('input') or {}).get('categories') or [None])[0]}, f.stem)
    for p, run in [(p, f.stem) for f in fb_files(*FB_HEADPLY_FILES) for p in json.load(open(f, encoding='utf-8'))['items']]:   # headply: exact times and counts
        if not p.get('postId') or not p.get('createdAt'):
            WHY_OUT['not a post (an error row)'] += 1; continue
        fb_post({'id': fb_key(p.get('postId'), p.get('url')), 'date': iso(p['createdAt']), 'text': clean(p.get('text')), 'url': p.get('url'),
                 'author': {'name': p.get('authorName'), 'id': p.get('authorId'), 'url': p.get('authorUrl')}, 'likes': num(p.get('reactionCount')),
                 'comments': num(p.get('commentCount')), 'shares': num(p.get('shareCount')), 'views': num(p.get('videoViewCount')),
                 'fmt': fb_fmt(p.get('url'), p.get('postType'), p.get('postType') in ('reel', 'video') or bool(p.get('videoUrl'))), 'duration': num(p.get('videoDurationSec')),
                 'media': {'cover': None, 'video': p.get('videoUrl'), 'images': []}, 'query': (p.get('source') or {}).get('target')}, run)
    for f in fb_files(*FB_ALPHA_FILES):                                           # reels and videos fetched by link (alpha-scraper)
        for p in json.load(open(f, encoding='utf-8'))['items']:
            v, e, o = p.get('video') or {}, p.get('engagement') or {}, p.get('owner') or {}
            if not v.get('id') or not v.get('upload_timestamp'):
                WHY_OUT['not a post (an error row)'] += 1; continue
            url = v.get('url') or p.get('_requested_url')
            fb_post({'id': fb_key((p.get('post') or {}).get('post_id'), url, v.get('id')), 'date': iso(v['upload_timestamp']),
                     'text': clean(v.get('description') or v.get('caption')), 'url': url,
                     'author': {'name': o.get('name'), 'id': o.get('id'), 'url': ('https://www.facebook.com/' + o['username']) if o.get('username') else None},
                     'likes': num(e.get('reactions_total') or e.get('likes')), 'comments': num(e.get('comments')), 'shares': num(e.get('shares')),
                     'views': fb_count(re.match(r'([\d.,]+[KMk]?) views', v.get('title') or '') and re.match(r'([\d.,]+[KMk]?) views', v['title']).group(1)),
                     'fmt': 'Reel' if v.get('is_reel') or '/reel/' in (url or '') else 'Video', 'duration': num(v.get('duration_seconds')),
                     'music': (p.get('music') or {}).get('track_name'),
                     'media': {'cover': (p.get('media') or {}).get('thumbnail_url'), 'video': v.get('direct_video_url') or v.get('video_only_url'), 'images': []}}, f.stem)
    for p, run in [(p, f.stem) for f in fb_files(*FB_LOFO_FILES) for p in json.load(open(f, encoding='utf-8'))['items']]:   # public groups (lofomachines)
        url = p.get('post_url')
        if not url or not p.get('date'):
            WHY_OUT['not a post (an error row)'] += 1; continue
        g = re.search(r'/groups/(\d+)/', url)
        fb_post({'id': fb_key(None, url), 'date': iso(p['date']), 'text': clean(p.get('text')), 'url': url,
                 'author': {'name': p.get('author_name'), 'id': p.get('author_id')}, 'likes': num(p.get('reaction_count')), 'comments': num(p.get('comment_count')),
                 'shares': num(p.get('share_count')), 'views': None, 'fmt': 'Image' if p.get('image_url') else 'Text',
                 'group': {'id': g.group(1) if g else None, 'name': clean(html_unescape(p.get('group_name')))},
                 'media': {'cover': None, 'video': None, 'images': [p['image_url']] if p.get('image_url') else []}, 'query': p.get('searchKeyword')}, run)


def html_unescape(s):
    import html
    return html.unescape(s or '')


def fb_count(v):
    """'15K', '1.2M', '2,345' or a number."""
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        return int(v)
    m = re.match(r'\s*([\d.,]+)\s*([KkMm]?)', str(v))
    if not m:
        return None
    n = float(m.group(1).replace(',', ''))
    return int(n * {'k': 1e3, 'm': 1e6, '': 1}[m.group(2).lower()])


def fb_one_item(p, body):
    """A scraper_one row (17-19 Oct). Reels and videos are told apart from photos by the link and the attachment type."""
    a = p.get('author') or {}
    att = [x for x in p.get('attachments') or [] if isinstance(x, dict)]
    vids = [x for x in att if x.get('type') == 'video']
    imgs = [x.get('url') for x in att if x.get('type') == 'photo' and x.get('url')]
    return {'id': fb_key(p.get('postId'), p.get('url')), 'date': iso(p.get('timestamp')),
            'text': clean(p.get('postText') or (p.get('sharedPost') or {}).get('postText')), 'url': p.get('url'),
            'author': {'name': a.get('name'), 'id': a.get('id'), 'url': a.get('url') or a.get('profileUrl')}, 'likes': num(p.get('reactionsCount')),
            'comments': num(p.get('commentsCount')), 'shares': num(p.get('sharesCount')), 'views': None,
            'fmt': fb_fmt(p.get('url'), None, bool(vids), len(imgs)), 'is_share': bool(p.get('isReshare')),
            'media': {'cover': None, 'video': vids[0].get('url') if vids else None, 'images': imgs}, 'query': (body.get('input') or {}).get('query')}


def fb_ugc_comments():
    """19 Oct: comments under public Facebook posts about V7 (thedoor first, Apify's own scraper for the posts it returned nothing for),
    anonymous like the others; V7's own pages count as V7's replies."""
    by_url = {}
    for it in ITEMS.values():
        if it['pl'] == 'fb' and it['kind'] == 'post' and it['src'] == 'ugc':
            for u in [it.get('url')] + it.get('urls', []):
                if u: by_url[u.split('?')[0].rstrip('/') if 'story_fbid' not in u else u] = it['id']
    def parent(u):
        u = u or ''
        return by_url.get(u.split('?')[0].rstrip('/') if 'story_fbid' not in u else u) or (fb_key(None, u) if fb_key(None, u) in ITEMS else None)
    for f in sorted(RAW.glob('fbcm_door_*.json')):
        for c in json.load(open(f, encoding='utf-8'))['items']:
            pid = parent(c.get('post_url'))
            if not c.get('id') or not pid:
                WHY_OUT['FB comment on an unknown post'] += 1; continue
            name = c.get('author_name') or ''
            it = {'id': 'fbc:' + str(c['id']), 'kind': 'comment', 'src': 'ugc', 'pl': 'fb', 'parent': pid, 'date': iso(c.get('timestamp') or c.get('comment_time')),
                  'text': clean(c.get('text')), 'url': c.get('comment_url') or c.get('post_url'),
                  'author': {'name': name, 'id': c.get('author_id'), 'url': c.get('author_profile_url')}, 'likes': num(c.get('reactions_count')),
                  'comments': num(c.get('replies_count')), 'shares': None, 'views': None, 'by_v7': fb_own(name, c.get('author_profile_url'), c.get('author_id')),
                  'has_media': bool(c.get('media') or c.get('image_url'))}
            add(it, f.stem)
    for f in sorted(RAW.glob('fbcm_official_*.json')):
        for c in json.load(open(f, encoding='utf-8'))['items']:
            pid = parent(c.get('facebookUrl') or c.get('inputUrl'))
            cid = c.get('id') or c.get('commentId')
            if not cid or not pid:
                WHY_OUT['FB comment on an unknown post'] += 1; continue
            name = c.get('profileName') or ''
            add({'id': 'fbc:' + str(cid), 'kind': 'comment', 'src': 'ugc', 'pl': 'fb', 'parent': pid, 'date': iso(c.get('date')), 'text': clean(c.get('text')),
                 'url': c.get('commentUrl') or c.get('facebookUrl'), 'author': {'name': name, 'id': c.get('profileId'), 'url': c.get('profileUrl')},
                 'likes': num(c.get('likesCount')), 'comments': num(c.get('commentsCount')), 'shares': None, 'views': None,
                 'by_v7': fb_own(name, c.get('profileUrl'), c.get('profileId')), 'has_media': bool(c.get('attachments'))}, f.stem)


def fb_extras():
    """19 Oct: what fbfill added to public Facebook posts: exact plays for videos and reels, what's said in them (invideoiq's
    transcriber), and the followers and category of the pages that posted."""
    plays, speech, pages = {}, {}, {}
    for f in sorted(RAW.glob('fbf_plays_*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            if x.get('video_id') and x.get('play_count') not in (None, ''):
                plays[str(x['video_id'])] = fb_count(x['play_count'])
    for f in sorted(RAW.glob('fbf_speech_*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            t = clean(x.get('transcript') or x.get('text') or '')
            u = x.get('video_url') or x.get('url') or x.get('input_url') or ''
            if t and u: speech[u.split('?')[0].rstrip('/')] = t
    for f in sorted(RAW.glob('fbf_pages_*.json')):
        for x in json.load(open(f, encoding='utf-8'))['items']:
            for u in (x.get('facebookUrl'), x.get('pageUrl'), x.get('inputUrl')):
                if u: pages[u.split('?')[0].rstrip('/').lower()] = x
    n_p = n_s = n_f = 0
    for it in ITEMS.values():
        if it['pl'] != 'fb' or it['src'] != 'ugc' or it['kind'] != 'post':
            continue
        vid = fb_vid(it.get('url')) or (it['id'][4:] if it['id'].startswith('fb:v') else None)
        vids = {vid} | {v for v, p in FB_ALIAS.items() if 'fb:' + p == it['id']}
        pc = [plays[v] for v in vids if v in plays]
        if pc and not it.get('views'):
            it['views'] = max(pc); n_p += 1
        for u in [it.get('url')] + it.get('urls', []):
            if u and u.split('?')[0].rstrip('/') in speech:
                it['speech'] = speech[u.split('?')[0].rstrip('/')]; n_s += 1; break
        a = it.get('author') or {}
        pg = pages.get((a.get('url') or '').split('?')[0].rstrip('/').lower())
        if pg:
            a['followers'] = a.get('followers') or num(pg.get('followers')); a['category'] = pg.get('category'); n_f += 1
            if not a.get('name') and pg.get('title'):   # the search row came without the page's name
                a['name'] = clean(pg['title'])
    print('Facebook: plays on %d posts, speech on %d, page followers on %d' % (n_p, n_s, n_f))


def seen():
    """19 Oct: what Claude read in a post's pictures (vis_read.json): the text written on them, what they show, whether V7 is visible."""
    p = HERE / 'vis_read.json'
    res = json.load(open(p, encoding='utf-8')) if p.exists() else {}
    n = 0
    for it in ITEMS.values():
        r = (res.get(it['id'][3:]) if it['pl'] == 'ig' else res.get('fb_' + it['id'][3:]) if it['pl'] == 'fb' else None) if it['kind'] == 'post' else None
        if r:
            it['seen'] = {k: r[k] for k in ('text', 'shows', 'v7_visible', 'products')}; n += 1
    print('pictures read for %d Instagram and Facebook posts' % n)


if __name__ == '__main__':
    own_posts(); comments(); fb_aliases(); ugc(); fb_ugc(); yt_comments(); ig_ugc_comments(); fb_ugc_comments(); extras(); fb_extras(); seen()
    out = list(ITEMS.values())
    json.dump({'made': datetime.date.today().isoformat(), 'window': [SINCE, UNTIL], 'items': out}, open(HERE / 'items.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    c = collections.Counter((i['src'], i['kind'], i['pl']) for i in out)
    for k in sorted(c):
        print('%-7s %-8s %-3s %5d' % (k + (c[k],)))
    print('total', len(out), '| left out:', dict(WHY_OUT))
    print('V7 replies:', sum(1 for i in out if i.get('by_v7')), '| replies linked:', sum(1 for i in out if i.get('reply_to')))
