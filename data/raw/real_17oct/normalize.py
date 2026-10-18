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
    old = ITEMS.get(it['id'])
    if old:
        old['found_by'] = sorted(set(old['found_by']) | {run}); return
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
            g = re.search(r'facebook\.com/groups/([\w.]+)/', p.get('url') or '')
            add({'id': 'fb:' + str(p.get('postId') or p.get('url')), 'kind': 'post', 'src': 'ugc', 'pl': 'fb', 'date': iso(p.get('timestamp')),
                 'text': clean(p.get('postText') or (p.get('sharedPost') or {}).get('postText')), 'url': p.get('url'),
                 'author': {'name': a.get('name'), 'id': a.get('id'), 'url': a.get('url')}, 'likes': num(p.get('reactionsCount')),
                 'comments': num(p.get('commentsCount')), 'shares': num(p.get('sharesCount')), 'views': None,
                 'fmt': 'Text' if not p.get('attachments') else 'Image', 'group': {'id': g.group(1)} if g else None, 'is_share': bool(p.get('isReshare')),
                 'query': body['input'].get('query')}, f.stem)
    # Instagram: the 17 Oct hashtags, then (18 Oct) posts tagging V7's accounts, Google's finds and Instagram's keyword search
    for name in ('ig_tags', 'ig_tagged_v7', 'ig_tagged_vss', 'ig_google_posts', 'ig_kw_wide'):
        kw = name == 'ig_kw_wide'                     # seemuapps' keyword search names its fields differently
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


if __name__ == '__main__':
    own_posts(); comments(); ugc(); yt_comments()
    out = list(ITEMS.values())
    json.dump({'made': datetime.date.today().isoformat(), 'window': [SINCE, UNTIL], 'items': out}, open(HERE / 'items.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    c = collections.Counter((i['src'], i['kind'], i['pl']) for i in out)
    for k in sorted(c):
        print('%-7s %-8s %-3s %5d' % (k + (c[k],)))
    print('total', len(out), '| left out:', dict(WHY_OUT))
    print('V7 replies:', sum(1 for i in out if i.get('by_v7')), '| replies linked:', sum(1 for i in out if i.get('reply_to')))
