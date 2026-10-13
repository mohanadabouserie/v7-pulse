"""13 Oct 2026: exact upload dates and like counts for the V7 Egypt YouTube videos in yt_backfill.json that aren't in
../verify_13oct/yt_videos.json. The channel list gives regular videos only a relative date ("4mo ago"), so each video's
public watch page is read instead (free). Polite: one request at a time, 2 seconds apart. Writes yt_pages.json."""
import json, os, re, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
have = {re.search(r'(?:v=|shorts/)([\w-]{11})', x['url']).group(1) for x in json.load(open(os.path.join(HERE, '..', 'verify_13oct', 'yt_videos.json'), encoding='utf-8'))['items']}
todo = []
for x in json.load(open(os.path.join(HERE, 'yt_backfill.json'), encoding='utf-8'))['items']:
    vid = re.search(r'(?:v=|shorts/)([\w-]{11})', x['url']).group(1)
    if vid not in have: todo.append((vid, x))
out = []
for vid, x in todo:
    req = urllib.request.Request('https://www.youtube.com/watch?v=' + vid, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9'})
    try:
        h = urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')
        pub = re.search(r'"publishDate":"([^"]+)"', h) or re.search(r'itemprop="datePublished" content="([^"]+)"', h) or re.search(r'"uploadDate":"([^"]+)"', h)
        like = re.search(r'like this video along with ([\d,]+) other (?:people|person)', h) or re.search(r'"likeCount":"?(\d+)', h)
        views = re.search(r'"viewCount":"(\d+)"', h)
        coms = re.search(r'"commentCount":\{"simpleText":"([\d,]+)"', h)
        rec = {'id': vid, 'url': x['url'], 'type': x.get('type'), 'title': x.get('title'), 'list_date': x.get('date'), 'list_views': x.get('viewCount'),
               'published': pub.group(1) if pub else None, 'likes': int(like.group(1).replace(',', '')) + (1 if like and 'along with' in like.group(0) else 0) if like else None,
               'views': int(views.group(1)) if views else None, 'comments': int(coms.group(1).replace(',', '')) if coms else None}
    except Exception as e:
        rec = {'id': vid, 'url': x['url'], 'title': x.get('title'), 'error': str(e)[:120]}
    out.append(rec); print(rec, flush=True)
    time.sleep(2)
json.dump({'checked': '2026-10-13', 'videos': out}, open(os.path.join(HERE, 'yt_pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'videos read')
