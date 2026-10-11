"""Builds the Rumors & attacks data for the dashboard.

Pipeline (11 Oct 2026):
  1. collect.py full / extra   public posts from X, Facebook, Instagram and TikTok (Apify)
  2. normalize.py              one flat, deduplicated list: posts.json
  3. labels.json               every post about V7, read and labelled by Claude in the chat:
                               the claim it touches, what it does (spread / question / debunk), a short note
  4. build_rumors.py           this file: rumors_dashboard.json, and with --inject the RUMOR_DATA block
                               in V7_Pulse_Dashboard.html

Privacy: private people are shown as "X user", "Facebook user" and so on. Names are kept only for news outlets,
shops, creators, official pages and accounts with 10,000+ followers. The link to each post is kept so the team can act on it.

Usage: python3 build_rumors.py [--inject]
"""
import hashlib, json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
DASH = os.path.join(ROOT, 'V7_Pulse_Dashboard.html')
CHECKED = '2026-10-11'

P = json.load(open(os.path.join(HERE, 'posts.json'), encoding='utf-8'))
LB = json.load(open(os.path.join(HERE, 'labels.json'), encoding='utf-8'))['posts_about_v7']
key = lambda r: r['pl'] + ':' + str(r['id'])

def day(s):
    return datetime.date.fromisoformat(s[:10])


def post(r, lb):
    who = lb.get('who') or 'person'
    fol = r.get('fol')
    named = who in ('news', 'business', 'creator', 'official') or (fol or 0) >= 10000
    age = None
    if r['pl'] == 'x' and r.get('au_created'):
        age = (day(r['d']) - day(r['au_created'])).days       # account age when it posted
    text = (r.get('text') or '').strip() or (r.get('shared_text') or '').strip()
    return {'id': key(r), 'pl': r['pl'], 'date': r['d'][:10], 'time': r['d'][11:16] or '12:00',
            'text': re.sub(r'https://t\.co/\S+', '', text).strip(), 'url': r['url'],
            'views': r.get('views'), 'likes': r.get('likes'), 'comments': r.get('comments'), 'shares': r.get('shares'),
            'claim': lb['claim'], 'stance': lb['stance'], 'note': lb['note'], 's': lb['s'], 'who': who,
            'name': (r.get('au') or '').strip() if named else None, 'fol': fol, 'age': age,
            'ak': hashlib.md5((r['pl'] + ':' + str(r.get('handle'))).encode()).hexdigest()[:8],   # same author, same key; not shown
            'lang': 'ar' if re.search(r'[؀-ۿ]', text) else 'en'}


about = {k: v for k, v in LB.items()}
by_pl = {}
for r in P:
    b = by_pl.setdefault(r['pl'], {'found': 0, 'about': 0})
    b['found'] += 1
    b['about'] += key(r) in about

posts = [post(r, LB[key(r)]) for r in P if key(r) in LB and LB[key(r)]['claim']]
posts.sort(key=lambda p: (p['date'], p['time']))

kinds = {}
for v in LB.values():
    kinds[v['kind']] = kinds.get(v['kind'], 0) + 1
dates = sorted(r['d'][:10] for r in P if key(r) in LB)
ctx = max((r for r in P if key(r) in LB and LB[key(r)]['kind'] in ('praise', 'boycott')), key=lambda r: r.get('views') or 0)

cost = 0.0
for line in open(os.path.join(HERE, 'run.log'), encoding='utf-8'):
    m = re.search(r'run cost ~\$([\d.]+)', line)
    if m:
        cost += float(m.group(1))

SEARCHES = {
    'x': 'V7 with words about owners (Coca-Cola, sold, boycott), quality (poisoning, harmful, fake), malt and alcohol, price and giveaways, plus general V7 talk. Then the Coca-Cola story in Apr–May 2024',
    'fb': '“V Cola sold”, “V7 Coca-Cola”, “V7 poisoning”, “V7 malt alcohol”, “V7 contest” and V7’s Arabic name',
    'ig': '#v7egypt, #vcola and #في_كولا',
    'tt': '“V7 boycott”, “V Cola Coca-Cola” and “V7 harmful drink”',
}
data = {
    'checked': CHECKED,
    'cost_usd': round(cost, 2),
    'found': len(P), 'about': len(LB), 'oldest': dates[0], 'newest': dates[-1],
    'kinds': kinds,
    'boycott': kinds.get('boycott', 0),
    'top': {'date': ctx['d'][:10], 'views': ctx.get('views'), 'url': ctx['url'], 'note': LB[key(ctx)]['note']},
    'searches': [{'pl': pl, 'what': SEARCHES[pl], **by_pl[pl]} for pl in ('x', 'fb', 'ig', 'tt')],
    'noise': 'Haval V7 cars, the V7 climbing grade, software and crypto “v7” releases, Toyota Corolla adverts, other brands’ contests and Cambodia’s V-Cola',
    'posts': posts,
}
json.dump(data, open(os.path.join(HERE, 'rumors_dashboard.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"{len(posts)} posts on claims, {len(LB)} about V7 of {len(P)} found, oldest {dates[0]}, cost about USD {cost:.2f}")

if '--inject' in sys.argv:
    html = open(DASH, encoding='utf-8').read()
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    new, n = re.subn(r'/\*RUMOR_DATA\*/.*?/\*END_RUMOR_DATA\*/', lambda m: '/*RUMOR_DATA*/var RUMOR_DATA=' + blob + ';/*END_RUMOR_DATA*/', html, flags=re.S)
    if n != 1:
        sys.exit('RUMOR_DATA block not found in the dashboard')
    open(DASH, 'w', encoding='utf-8').write(new)
    print('injected into', os.path.basename(DASH))
