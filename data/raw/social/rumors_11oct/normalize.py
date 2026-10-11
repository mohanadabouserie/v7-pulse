"""One flat list of the pulled posts (posts.json), deduplicated, for labelling.
Usage: python3 normalize.py"""
import json, os, glob, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
def ts(v):
    if v is None: return None
    if isinstance(v, (int, float)): return datetime.datetime.fromtimestamp(v / 1000 if v > 1e11 else v, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
    for f in ('%a %b %d %H:%M:%S %z %Y', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
        try: return datetime.datetime.strptime(v, f).strftime('%Y-%m-%d %H:%M')
        except ValueError: pass
    return str(v)
def x(it, f):
    a = it.get('author') or {}
    return dict(pl='x', id=it['id'], url=it.get('url'), d=ts(it.get('createdAt')), text=it.get('text') or '', lang=it.get('lang'),
                au=a.get('name'), handle=a.get('userName'), fol=a.get('followers'), au_created=ts(a.get('createdAt')) if a.get('createdAt') else None,
                au_loc=a.get('location'), verified=a.get('isBlueVerified'), views=it.get('viewCount'), likes=it.get('likeCount'),
                comments=it.get('replyCount'), shares=(it.get('retweetCount') or 0) + (it.get('quoteCount') or 0),
                reply=it.get('isReply'), quoted=((it.get('quoted_tweet') or {}).get('text') if isinstance(it.get('quoted_tweet'), dict) else None),
                rt=((it.get('retweeted_tweet') or {}).get('text') if isinstance(it.get('retweeted_tweet'), dict) else None))
def fb(it, f):
    a = it.get('author') or {}
    sh = it.get('sharedPost') or {}
    return dict(pl='fb', id=it.get('postId'), url=it.get('url'), d=ts(it.get('timestamp')), text=it.get('postText') or '', au=a.get('name'), handle=a.get('id'),
                fol=None, views=None, likes=it.get('reactionsCount'), comments=it.get('commentsCount'), shares=it.get('sharesCount'),
                shared_text=(sh.get('postText') if isinstance(sh, dict) else None))
def ig(it, f):
    return dict(pl='ig', id=it.get('id'), url=it.get('url'), d=ts(it.get('timestamp')), text=it.get('caption') or '', au=it.get('ownerFullName'), handle=it.get('ownerUsername'),
                fol=None, views=it.get('videoPlayCount') or it.get('videoViewCount'), likes=it.get('likesCount'), comments=it.get('commentsCount'), shares=None,
                loc=it.get('locationName'), tag=it.get('inputUrl', '').rstrip('/').split('/')[-1], kind=it.get('type'))
def tt(it, f):
    a = it.get('authorMeta') or {}
    loc = it.get('locationMeta') or {}
    return dict(pl='tt', id=it.get('id'), url=it.get('webVideoUrl'), d=ts(it.get('createTimeISO')), text=it.get('text') or '', lang=it.get('textLanguage'),
                au=a.get('nickName'), handle=a.get('name'), fol=a.get('fans'), views=it.get('playCount'), likes=it.get('diggCount'), comments=it.get('commentCount'),
                shares=it.get('shareCount'), loc=loc.get('address'), q=it.get('searchQuery'), au_region=a.get('region'))
MAP = {'x_': x, 'fb': fb, 'ig': ig, 'tt': tt}
out, seen = [], {}
for path in sorted(glob.glob(os.path.join(HERE, '*.json'))):
    name = os.path.basename(path)[:-5]
    if name.startswith('t_') or name in ('posts', 'labels'): continue
    d = json.load(open(path, encoding='utf-8'))
    for it in d['items']:
        if not isinstance(it, dict) or it.get('error') or it.get('noResults'): continue
        if str(it.get('id')) == '-1' or (it.get('text') or '').startswith('From KaitoEasyAPI'): continue   # the X actor's filler rows
        r = MAP[name[:2]](it, name)
        key = r['pl'] + ':' + str(r['id'])
        if key in seen: seen[key]['found_by'].append(name); continue
        r['found_by'] = [name]; seen[key] = r; out.append(r)
for i, r in enumerate(out): r['k'] = i + 1
json.dump(out, open(os.path.join(HERE, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'unique posts;', {p: sum(1 for r in out if r['pl'] == p) for p in ('x', 'fb', 'ig', 'tt')})
