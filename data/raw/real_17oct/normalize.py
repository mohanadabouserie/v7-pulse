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
OWN_TT, OWN_FB_NAMES, OWN_YT = {'v7.egypt'}, {'v7egypt', 'vsupersoda'}, {'v7egypt', '@v7egypt'}


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
    for p in load('yt_posts'):
        vid = re.search(r'(?:v=|shorts/)([\w-]{11})', p.get('url') or '')
        pg = pages.get(vid.group(1) if vid else '', {})
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
    for p in load('ig_tags'):
        u = (p.get('ownerUsername') or '').lower()
        if u in OWN_IG | ABROAD_IG:
            WHY_OUT['V7 itself in the search'] += 1; continue
        add({'id': 'ig:' + str(p.get('shortCode') or p.get('id')), 'kind': 'post', 'src': 'ugc', 'pl': 'ig', 'date': iso(p.get('timestamp')), 'text': clean(p.get('caption')),
             'url': p.get('url'), 'author': {'name': p.get('ownerFullName'), 'handle': p.get('ownerUsername')}, 'likes': num(p.get('likesCount')),
             'comments': num(p.get('commentsCount')), 'shares': None, 'views': num(p.get('videoPlayCount')) or num(p.get('videoViewCount')), 'fmt': fmt_ig(p),
             'hashtags': p.get('hashtags') or [], 'place': p.get('locationName')}, 'ig_tags')
    for p in load('tt_search'):
        am = p.get('authorMeta') or {}
        if (am.get('name') or '').lower() in OWN_TT:
            WHY_OUT['V7 itself in the search'] += 1; continue
        add({'id': 'tt:' + str(p.get('id')), 'kind': 'post', 'src': 'ugc', 'pl': 'tt', 'date': iso(p.get('createTimeISO')), 'text': clean(p.get('text')),
             'url': p.get('webVideoUrl'), 'author': {'name': am.get('nickName'), 'handle': am.get('name'), 'followers': num(am.get('fans')), 'verified': bool(am.get('verified'))},
             'likes': num(p.get('diggCount')), 'comments': num(p.get('commentCount')), 'shares': num(p.get('shareCount')), 'views': num(p.get('playCount')),
             'fmt': 'Video', 'hashtags': [h.get('name') for h in p.get('hashtags') or [] if h.get('name')], 'region': p.get('locationCreated'),
             'query': p.get('searchQuery')}, 'tt_search')
    for p in load('yt_search'):
        if (p.get('channelUsername') or '').lower() in OWN_YT or (p.get('channelName') or '') == 'V7 Egypt':
            WHY_OUT['V7 itself in the search'] += 1; continue
        vid = re.search(r'(?:v=|shorts/)([\w-]{11})', p.get('url') or '')
        add({'id': 'yt:' + (vid.group(1) if vid else str(p.get('id'))), 'kind': 'post', 'src': 'ugc', 'pl': 'yt', 'date': iso(p.get('date')),
             'text': clean((p.get('title') or '') + ('\n' + p['text'][:600] if p.get('text') else '')), 'url': p.get('url'),
             'author': {'name': p.get('channelName'), 'handle': p.get('channelUsername'), 'followers': num(p.get('numberOfSubscribers')), 'url': p.get('channelUrl')},
             'likes': num(p.get('likes')), 'comments': num(p.get('commentsCount')), 'shares': None, 'views': num(p.get('viewCount')),
             'fmt': 'Short' if '/shorts/' in (p.get('url') or '') else 'Video', 'query': (p.get('input') or p.get('fromYTUrl'))}, 'yt_search')
    for p in load('reddit'):
        kind = 'comment' if p.get('dataType') == 'comment' else 'post'
        add({'id': 'rd:' + str(p.get('id') or p.get('url')), 'kind': 'post', 'src': 'ugc', 'pl': 'rd', 'date': iso(p.get('createdAt')),
             'text': clean(((p.get('title') or '') + '\n' + (p.get('body') or '')).strip()), 'url': p.get('url'),
             'author': {'name': 'Reddit user', 'handle': None}, 'likes': num(p.get('upVotes')), 'comments': num(p.get('numberOfComments')), 'shares': None,
             'views': None, 'fmt': 'Text', 'subreddit': p.get('communityName') or p.get('parsedCommunityName'), 'reddit_kind': kind}, 'reddit')


if __name__ == '__main__':
    own_posts(); comments(); ugc()
    out = list(ITEMS.values())
    json.dump({'made': datetime.date.today().isoformat(), 'window': [SINCE, UNTIL], 'items': out}, open(HERE / 'items.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    c = collections.Counter((i['src'], i['kind'], i['pl']) for i in out)
    for k in sorted(c):
        print('%-7s %-8s %-3s %5d' % (k + (c[k],)))
    print('total', len(out), '| left out:', dict(WHY_OUT))
    print('V7 replies:', sum(1 for i in out if i.get('by_v7')), '| replies linked:', sum(1 for i in out if i.get('reply_to')))
