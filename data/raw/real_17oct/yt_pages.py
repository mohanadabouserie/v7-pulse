"""17 Oct 2026: exact upload dates, likes, views and comment counts for V7 Egypt's YouTube videos in raw/yt_posts.json.
The channel list gives only relative dates ("1mo ago"), so each video's public watch page is read instead (free).
Polite: one request at a time, 2 seconds apart. Writes yt_pages.json. (Same method as ../own_backfill_13oct/yt_pages.py.)"""
import json, os, re, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
out = []
for x in json.load(open(os.path.join(HERE, 'raw', 'yt_posts.json'), encoding='utf-8'))['items']:
    vid = re.search(r'(?:v=|shorts/)([\w-]{11})', x['url']).group(1)
    req = urllib.request.Request('https://www.youtube.com/watch?v=' + vid, headers={'User-Agent': UA, 'Accept-Language': 'en-US,en;q=0.9'})
    try:
        h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')
        pub = re.search(r'"publishDate":"([^"]+)"', h) or re.search(r'itemprop="datePublished" content="([^"]+)"', h) or re.search(r'"uploadDate":"([^"]+)"', h)
        like = re.search(r'like this video along with ([\d,]+) other (?:people|person)', h) or re.search(r'"likeCount":"?(\d+)', h)
        views = re.search(r'"viewCount":"(\d+)"', h)
        coms = re.search(r'"commentCount":\{"simpleText":"([\d,]+)"', h)
        off = re.search(r'Comments are turned off', h)
        rec = {'id': vid, 'url': x['url'], 'title': x.get('title'), 'list_date': x.get('date'), 'published': pub.group(1) if pub else None,
               'likes': int(like.group(1).replace(',', '')) + (1 if 'along with' in like.group(0) else 0) if like else None,
               'views': int(views.group(1)) if views else None, 'comments': int(coms.group(1).replace(',', '')) if coms else (0 if off else None),
               'comments_off': bool(off)}
    except Exception as e:
        rec = {'id': vid, 'url': x['url'], 'title': x.get('title'), 'error': str(e)[:120]}
    out.append(rec)
    time.sleep(2)
json.dump({'checked': '2026-10-17', 'videos': out}, open(os.path.join(HERE, 'yt_pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'videos read |', sum(1 for r in out if r.get('published')), 'with dates |', sum(1 for r in out if r.get('error')), 'errors |',
      'comments off on', sum(1 for r in out if r.get('comments_off')))
