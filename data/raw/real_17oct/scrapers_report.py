"""Writes SCRAPERS.md: every Apify run of the real-data collection (17 and 18 Oct 2026) with the scraper's link, the input it was
given, what came back, what the dashboard kept, and the cost. Read from raw/ (each run's saved input, run record and items),
items.json (what fell inside the window) and labels.json (what Claude judged to be about V7). Counts only: no names.
Usage: python3 scrapers_report.py"""
import collections, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
ACTORS = {   # actor id -> (Apify Store link, what it is)
    'FB_POSTS': ('apify/facebook-posts-scraper', 'Facebook page posts'),
    'FB_COMMENTS': ('apify/facebook-comments-scraper', 'Facebook comments'),
    'FB_SEARCH': ('scraper_one/facebook-posts-search', 'Facebook keyword search'),
    'IG_POSTS': ('apify/instagram-post-scraper', 'Instagram posts of a profile, or posts by link'),
    'IG_COMMENTS': ('apify/instagram-comment-scraper', 'Instagram comments'),
    'IG_TAGS': ('apify/instagram-hashtag-scraper', 'Instagram hashtags (and Instagram keyword search)'),
    'IG_TAGGED': ('apify/instagram-tagged-scraper', 'Instagram posts that tag a profile'),
    'IG_SCRAPER': ('apify/instagram-scraper', 'Instagram (here: posts that mention a profile)'),
    'IG_KW': ('seemuapps/instagram-keyword-posts-scraper', 'Instagram keyword search with a date range'),
    'TT': ('clockworks/tiktok-scraper', 'TikTok profiles, hashtags, keyword search, videos by link'),
    'TT_COMMENTS': ('clockworks/tiktok-comments-scraper', 'TikTok comments'),
    'YT': ('streamers/youtube-scraper', 'YouTube keyword search'),
    'YT_CHANNEL': ('streamers/youtube-channel-scraper', 'YouTube channel videos'),
    'YT_COMMENTS': ('apidojo/youtube-comments-scraper', 'YouTube comments'),
    'YT_COMMENTS2': ('calm_builder/youtube-scraper', 'YouTube videos (and comments)'),
    'X': ('kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest', 'X (Twitter) search'),
    'REDDIT': ('trudax/reddit-scraper-lite', 'Reddit search'),
    'GOOGLE': ('apify/google-search-scraper', 'Google search'),
    'APIDOJO': ('apidojo/instagram-scraper-api', 'Instagram keyword search (posts)'),
    'DAMI': ('dami_studio/instagram-reels-search-scraper', 'Instagram Reels search'),
    'MEMO23': ('memo23/instagram-reels-search-scraper', 'Instagram Reels search, exact phrases'),
    'BOOLEAN': ('scraping_solutions/instagram-boolean-search-scraper-posts-reels', 'Instagram search, exact phrases'),
    'DATASLAYER': ('data-slayer/instagram-search-reels', 'Instagram Reels search'),
    'IGSEARCH': ('apify/instagram-search-scraper', 'Instagram popular reels for a keyword'),
    'SPEECH': ('apple_yang/instagram-transcripts-scraper', 'What is said in Instagram reels (speech to text)'),
    'PROFILES': ('apify/instagram-profile-scraper', 'Instagram accounts (follower counts)'),
}
RUNS = [   # run name (raw/<name>.json) -> actor, why
    ('t_fb_posts', 'FB_POSTS', '17 Oct test: 3 of V7 Egypt’s Facebook posts'),
    ('t_fb_comments', 'FB_COMMENTS', '17 Oct test: comments on 2 V7 posts'),
    ('t_ig_posts', 'IG_POSTS', '17 Oct test: 3 of V7 Egypt’s Instagram posts'),
    ('t_ig_comments', 'IG_COMMENTS', '17 Oct test: comments on 2 V7 posts'),
    ('t_tt_comments', 'TT_COMMENTS', '17 Oct test: comments on a V7 TikTok video'),
    ('t_x', 'X', '17 Oct test: X search'),
    ('t_fb_search', 'FB_SEARCH', '17 Oct test: Facebook keyword search'),
    ('t_ig_tag', 'IG_TAGS', '17 Oct test: one Instagram hashtag'),
    ('t_tt_search', 'TT', '17 Oct test: TikTok keyword search'),
    ('t_yt_search', 'YT', '17 Oct test: YouTube keyword search'),
    ('t_reddit', 'REDDIT', '17 Oct test: Reddit search'),
    ('fb_posts', 'FB_POSTS', 'V7 Egypt’s Facebook posts since 20 Apr'),
    ('ig_posts', 'IG_POSTS', 'V7 Egypt’s Instagram posts since 20 Apr'),
    ('tt_posts', 'TT', 'V7 Egypt’s TikTok videos since 20 Apr'),
    ('yt_posts', 'YT_CHANNEL', 'V7 Egypt’s YouTube videos and Shorts'),
    ('fb_comments', 'FB_COMMENTS', 'every comment on V7 Egypt’s Facebook posts'),
    ('ig_comments', 'IG_COMMENTS', 'every comment on V7 Egypt’s Instagram posts'),
    ('tt_comments', 'TT_COMMENTS', 'every comment on V7 Egypt’s TikTok videos'),
    ('abroad_posts', 'IG_POSTS', 'the posts of V7’s pages abroad'),
    ('abroad_comments', 'IG_COMMENTS', 'comments on the pages abroad (stopped at 829 of 1,837 for the budget)'),
    ('x_drink', 'X', 'public posts: V7 + drink words'), ('x_vcola', 'X', 'public posts: the V Cola line'),
    ('x_talk', 'X', 'public posts: V7 + taste and price words'), ('x_en', 'X', 'public posts: English phrases'),
    ('x_brand', 'X', 'public posts: V7 + company and boycott words'),
] + [('fb_search_%02d' % i, 'FB_SEARCH', 'public posts: Facebook keyword search') for i in range(12)] + [
    ('ig_tags', 'IG_TAGS', 'public posts: 8 Instagram hashtags'),
    ('tt_search', 'TT', 'public posts: TikTok keyword search with TikTok’s date filter (returned unrelated videos)'),
    ('yt_search', 'YT', 'public posts: YouTube keyword search'),
    ('reddit', 'REDDIT', 'public posts: Reddit search'),
    ('t2_ig_tagged', 'IG_TAGGED', '18 Oct test: posts tagging @v7egypt'),
    ('t2_ig_kw_posts', 'IG_TAGS', '18 Oct test: Instagram keyword search, posts'),
    ('t2_ig_kw_reels', 'IG_TAGS', '18 Oct test: Instagram keyword search, reels'),
    ('t2_tt_search_eg', 'TT', '18 Oct test: TikTok keyword search from Egypt'),
    ('t2_tt_top_eg', 'TT', '18 Oct test: TikTok “Top” search from Egypt'),
    ('t2_tt_tags_eg', 'TT', '18 Oct test: TikTok hashtags from Egypt'),
    ('t2_tt_6m_eg', 'TT', '18 Oct test: TikTok’s 6-month date filter from Egypt (unrelated videos)'),
    ('t2_tt_month_eg', 'TT', '18 Oct test: TikTok’s past-month date filter (nothing)'),
    ('t2_ig_mentions', 'IG_SCRAPER', '18 Oct test: posts mentioning @v7egypt'),
    ('t2_ig_kw_dated', 'IG_KW', '18 Oct test: Instagram keyword search inside the window'),
    ('t2_google', 'GOOGLE', '18 Oct test: Google search of instagram.com and tiktok.com'),
    ('ig_tagged_v7', 'IG_TAGGED', 'public posts: Instagram posts tagging @v7egypt'),
    ('ig_tagged_vss', 'IG_TAGGED', 'public posts: Instagram posts tagging @vsupersoda'),
    ('ig_kw_wide', 'IG_KW', 'public posts: Instagram keyword search, 24 spellings, inside the window'),
    ('google_ig', 'GOOGLE', 'public posts: Google search of instagram.com, 18 spellings, past 6 months'),
    ('google_tt', 'GOOGLE', 'public posts: Google search of tiktok.com, 18 spellings, past 6 months'),
    ('ig_google_posts', 'IG_POSTS', 'the Instagram posts Google found (new and inside the window), by link'),
    ('tt_google_posts', 'TT', 'the TikTok videos Google found (new and inside the window), by link'),
] + [('fb_search_%02d' % i, 'FB_SEARCH', 'public posts: Facebook keyword search, more spellings') for i in range(12, 18)] + [
    ('x_extra', 'X', 'public posts: more spellings on X'),
    ('tt_tags_wide', 'TT', 'public posts: 5 TikTok hashtags, browsed from Egypt'),
    ('tt_wide', 'TT', 'public posts: TikTok keyword search from Egypt, 10 keywords (stopped at its cap after 8)'),
    ('yt_recent', 'YT', 'public posts: YouTube keyword search, newest first'),
    ('t3_yt_comments_apidojo', 'YT_COMMENTS', '18 Oct test: 20 comments from Kareem Elsayed’s video'),
    ('t3_yt_comments_calm', 'YT_COMMENTS2', '18 Oct test: the same with calm_builder (returned the video only)'),
    ('yt_own_check', 'YT_COMMENTS2', 'are comments on on V7 Egypt’s 28 videos? (27 yes, 1 off)'),
    ('yt_comments_own', 'YT_COMMENTS', 'comments on V7 Egypt’s YouTube videos'),
    ('yt_comments_public', 'YT_COMMENTS', 'comments on the public YouTube videos about V7'),
] + [('kw_apidojo_%d' % i, 'APIDOJO', '19 Oct comparison: keyword %d of 3' % i) for i in (1, 2, 3)] + [
    ('kw_apify_search', 'IGSEARCH', '19 Oct comparison: the 3 keywords'), ('kw_memo23', 'MEMO23', '19 Oct comparison: the 3 keywords in quotes'),
] + [('kw_boolean_%d' % i, 'BOOLEAN', '19 Oct comparison: keyword %d of 3 in quotes' % i) for i in (1, 2, 3)] + [
] + [('kw_dataslayer_%d' % i, 'DATASLAYER', '19 Oct comparison: keyword %d of 3' % i) for i in (1, 2, 3)] + [
    ('kw_dami', 'DAMI', '19 Oct comparison: the 3 keywords'), ('kw_seemuapps', 'IG_KW', '19 Oct comparison: the 3 keywords'),
    ('kw_apidojo_deep', 'APIDOJO', '19 Oct: 40 results for "V7 soda" (depth check)'),
    ('kw_refetch_test', 'IG_POSTS', '19 Oct: the 25 posts apidojo returned without a caption or likes, fetched by link'),
    ('kw_transcript_test', 'SPEECH', '19 Oct test: speech of 3 Egyptian Arabic reels'),
    ('ig_profiles', 'PROFILES', 'follower counts of the 175 Instagram accounts that posted about V7 without one'),
    ('igspeech_about', 'SPEECH', 'speech of the 163 Instagram reels about V7'),
    ('igspeech_tagged', 'SPEECH', 'speech of the 32 reels that tag V7 but whose caption alone did not show it'),
]


def short_input(inp):
    """The input as given, with long lists of links counted rather than printed."""
    out = {}
    for k, v in (inp or {}).items():
        if isinstance(v, list) and len(v) > 12:
            out[k] = '[%d %s]' % (len(v), 'links' if any('http' in json.dumps(x) for x in v[:3]) else 'items')
        elif isinstance(v, str) and len(v) > 400:
            out[k] = v[:400] + '… (%d characters)' % len(v)
        elif k.startswith('shouldDownload'):
            continue
        else:
            out[k] = v
    return json.dumps(out, ensure_ascii=False)


def final_runs():
    """Each run's final record from Apify (a run's charge is settled after it ends, so the copy saved with the items can show 0).
    Needs APIFY_API_TOKEN in the environment; kept in runs_final.json so it's fetched once."""
    import os, urllib.request
    cache = HERE / 'runs_final.json'
    got = json.load(open(cache, encoding='utf-8')) if cache.exists() else {}
    tok = os.environ.get('APIFY_API_TOKEN')
    for name, _, _ in RUNS:
        f = RAW / (name + '.json')
        if name in got or not f.exists() or not tok:
            continue
        rid = (json.load(open(f, encoding='utf-8')).get('run') or {}).get('id')
        if rid:
            r = json.load(urllib.request.urlopen(urllib.request.Request('https://api.apify.com/v2/actor-runs/' + rid, headers={'Authorization': 'Bearer ' + tok}), timeout=40))['data']
            got[name] = {k: r.get(k) for k in ('id', 'status', 'startedAt', 'finishedAt', 'usageTotalUsd', 'chargedEventCounts')}
    json.dump(got, open(cache, 'w', encoding='utf-8'), indent=1)
    return got


def main():
    final = final_runs()
    items = json.load(open(HERE / 'items.json', encoding='utf-8'))['items']
    labels = json.load(open(HERE / 'labels.json', encoding='utf-8'))
    found = collections.defaultdict(list)
    for i in items:
        for r in i.get('found_by') or []:
            found[r].append(i)

    def kept(i):
        if i['kind'] == 'post' and i['src'] in ('own', 'abroad'): return True
        if i.get('by_v7'): return True
        lab = labels.get(i['id'])
        if not lab: return False
        return bool(lab['about']) or (i['kind'] == 'comment' and lab['c'] in ('n_emoji', 'n_tag'))

    rows, by_actor = [], collections.defaultdict(lambda: collections.Counter())
    for name, actor, why in RUNS:
        f = RAW / (name + '.json')
        if not f.exists():
            continue
        body = json.load(open(f, encoding='utf-8'))
        run = final.get(name) or body.get('run') or {}
        n = len(body.get('items') or [])
        inwin = found.get(name, [])
        k = sum(1 for i in inwin if kept(i))
        cost = run.get('usageTotalUsd') if run.get('usageTotalUsd') is not None else body.get('cost_usd')
        rows.append((name, actor, why, (run.get('startedAt') or '')[:10], short_input(body.get('input')), n, len(inwin), k, cost or 0))
        a = by_actor[actor]; a['runs'] += 1; a['items'] += n; a['kept'] += k; a['cost'] += round((cost or 0) * 10000)
    lines = ['# Scrapers used for the real data (17–19 Oct 2026)', '',
             'Every Apify run of `data/raw/real_17oct/`, written by `scrapers_report.py` from the saved runs. **Returned** is what the scraper gave back; '
             '**in window** is what fell between 20 Apr and 16 Oct 2026 after duplicates were merged (an item found by two runs counts for both); '
             '**kept** is what the dashboard shows (public posts and comments Claude judged to be about V7, emoji reactions and friend tags under V7’s posts, '
             'and every V7 post and reply). Runs that add to posts already collected (follower counts, the speech of reels, posts fetched by link to fill a gap) and the 19 Oct comparison runs keep nothing of their own, so their kept is 0. Cost is Apify’s charge for the run.', '',
             '## By scraper', '', '| Scraper | Used for | Runs | Returned | Kept | Cost (USD) |', '|---|---|---:|---:|---:|---:|']
    for actor, c in sorted(by_actor.items(), key=lambda kv: -kv[1]['cost']):
        link, what = ACTORS[actor]
        lines.append('| [%s](https://apify.com/%s) | %s | %d | %s | %s | %.2f |' % (link, link, what, c['runs'], format(c['items'], ','), format(c['kept'], ','), c['cost'] / 10000))
    tot = sum(r[8] for r in rows)
    lines += ['', 'Total for these runs: USD %.2f (Apify’s meter for the month also counts platform usage).' % tot, '', '## Every run', '']
    for name, actor, why, day, inp, n, w, k, cost in rows:
        link = ACTORS[actor][0]
        lines += ['### %s' % name, '- **Scraper:** [%s](https://apify.com/%s), %s' % (link, link, day),
                  '- **Why:** %s' % why, '- **Input:** `%s`' % inp.replace('`', "'"),
                  '- **Output:** %s returned · %s in window · %s kept · USD %.4f' % (format(n, ','), format(w, ','), format(k, ','), cost), '']
    lines += ['## Without Apify', '',
              '- `yt_pages.py`: V7 Egypt’s YouTube watch pages, read directly for exact dates and counts (free). Its “comments turned off” reading was wrong: '
              'the words are in every page’s text. The 18 Oct check with calm_builder found comments on for 27 of the 28 videos.',
              '- Claude (`label.py`, through Claude Code on the user’s plan) read and labelled every public post and comment.', '']
    (HERE / 'SCRAPERS.md').write_text('\n'.join(lines), encoding='utf-8')
    print('SCRAPERS.md: %d runs, %d scrapers, USD %.2f' % (len(rows), len(by_actor), tot))


if __name__ == '__main__':
    main()
