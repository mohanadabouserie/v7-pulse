import re, html, time, json, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
UA = "V7PulseResearch/0.1 (social listening test)"
ns = {'a': 'http://www.w3.org/2005/Atom'}
queries = [("all", "V7 drink"), ("all", "V7 Egypt"), ("all", "\"في سفن\""), ("all", "V cola Egypt"), ("all", "V7 cream soda"), ("Egypt", "V7"), ("Cairo", "V7"), ("Alexandria", "V7"), ("ExEgypt", "V7")]
out = []
time.sleep(60)
for sub, q in queries:
    if sub == "all":
        url = "https://www.reddit.com/search.rss?" + urllib.parse.urlencode({'q': q, 'limit': 50, 'sort': 'relevance', 't': 'all'})
    else:
        url = f"https://www.reddit.com/r/{sub}/search.rss?" + urllib.parse.urlencode({'q': q, 'restrict_sr': 'on', 'limit': 50, 'sort': 'new'})
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30).read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(45); continue
            raw = None; print(sub, q, 'HTTP', e.code); break
    else:
        raw = None; print(sub, q, 'still 429')
    if raw:
        root = ET.fromstring(raw)
        for e in root.findall('a:entry', ns):
            cat = e.find('a:category', ns)
            link = e.find('a:link', ns)
            out.append(dict(q=q, scope=sub, title=e.findtext('a:title', default='', namespaces=ns), sub=cat.get('label') if cat is not None else '',
                            date=(e.findtext('a:updated', default='', namespaces=ns) or '')[:10], url=link.get('href') if link is not None else '',
                            author=(e.findtext('a:author/a:name', default='', namespaces=ns)),
                            text=re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', e.findtext('a:content', default='', namespaces=ns) or '')))[:600]))
        print(f'[{sub}] "{q}": {len(root.findall("a:entry", ns))} results', flush=True)
    time.sleep(20)
json.dump(out, open('reddit_rss_results.json', 'w'), ensure_ascii=False, indent=1)
print('saved', len(out))
