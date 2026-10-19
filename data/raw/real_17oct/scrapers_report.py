"""Writes SCRAPERS.md: every Apify run of the real-data collection (17 to 19 Oct 2026) with the scraper's link, the input it was
given, what came back, what the dashboard kept, and the cost. Read from raw/ (each run's saved input, run record and items),
items.json (what fell inside the window) and labels.json (what Claude judged to be about V7). Counts only: no names.
Usage: python3 scrapers_report.py"""
import collections, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
ACTORS = {   # actor id -> (Apify Store link, what it is)
    'FB_POSTS': ('apify/facebook-posts-scraper', 'Facebook page posts, or posts by link'),
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
    'AFANASENKO': ('afanasenko/instagram-reel-script-extractor', 'On-screen text and speech of Instagram reels'),
    'IG_CM_CHEAP': ('scrapesmith/instagram-comments-scraper', 'Instagram comments (cheaper, but returned nothing for half the posts)'),
    'FB_SILENT': ('silentflow/facebook-search-scraper', 'Facebook keyword search'),
    'FB_FORGE': ('scrapeforge/facebook-search-posts', 'Facebook keyword search'),
    'FB_APIFY_SEARCH': ('apify/facebook-search-scraper', 'Facebook keyword search (posts and reels)'),
    'FB_DANEK_SEARCH': ('danek/facebook-search-ppr', 'Facebook keyword search'),
    'FB_POWERAI': ('powerai/facebook-post-search-scraper', 'Facebook keyword search (aborted)'),
    'FB_ALIEN': ('alien_force/facebook-search-scraper', 'Facebook keyword search'),
    'FB_FETCHCAT': ('fetch_cat/facebook-post-search-scraper', 'Facebook keyword search'),
    'FB_MINA': ('mina_safwat/facebook-search-actor', 'Facebook keyword search (no dates)'),
    'FB_IGVIEW': ('igview-owner/facebook-old-posts-search', 'Facebook keyword search'),
    'FB_TOPAPI': ('topapi/facebook-search-posts-scraper', 'Facebook keyword search'),
    'FB_HEADPLY': ('headply/facebook-post-search-scraper', 'Facebook keyword search'),
    'FB_V_APIFY': ('apify/facebook-video-search-scraper', 'Facebook video search'),
    'FB_V_POWERAI': ('powerai/facebook-video-search-scraper', 'Facebook video search'),
    'FB_V_HEADPLY': ('headply/facebook-video-search-scraper', 'Facebook video search'),
    'FB_V_AXESSO': ('axesso_data/facebook-video-search-scraper', 'Facebook video search'),
    'FB_TAGS': ('apify/facebook-hashtag-scraper', 'Facebook hashtags (returned nothing)'),
    'FB_GROUPS': ('lofomachines/facebook-groups-posts-search-scraper', 'Facebook public groups search'),
    'FB_POST_LINK': ('danek/facebook-posts-fast', 'Facebook posts, reels and videos by link'),
    'FB_PLAYS': ('social_developer/facebook-playcount-scraper', 'Facebook video plays'),
    'FB_REEL_DETAILS': ('alpha-scraper/facebook-reels-details-scraper-pro', 'Facebook reel details'),
    'FB_SPEECH': ('invideoiq/video-transcriber', 'What is said in Facebook videos (speech to text)'),
    'FB_SP_PIOTR': ('piotrv1001/facebook-video-transcript-scraper', 'Facebook captions and speech to text'),
    'FB_SP_CODENEST': ('codenest/facebook-video-transcript-scraper', "Facebook's own captions"),
    'FB_SP_VIRAL': ('viralanalyzer/video-transcriber', 'Speech to text (Whisper small)'),
    'FB_SP_ALPHA': ('alpha-scraper/facebook-transcript-subtitle-scraper', 'Facebook subtitles (returned none)'),
    'FB_CM_CHEAP': ('thedoor/facebook-comment-scraper', 'Facebook comments (cheaper)'),
    'FB_PAGES': ('apify/facebook-pages-scraper', 'Facebook pages (followers, category)'),
    'FB_V_IGVIEW': ('igview-owner/facebook-search-scraper', 'Facebook video search'),
    'FB_V_LEXIS': ('lexis-solutions/facebook-videos-watch-scraper', 'Facebook Watch search'),
    'FB_V_EASYAPI': ('easyapi/facebook-videos-scraper', 'Facebook Watch search (returned nothing)'),
    'FB_V_SASKY': ('sasky/facebook-keyword-videos-urls-scraper', 'Facebook video links by keyword'),
    'FB_V_NATANIEL': ('natanielsantos/facebook-video-search-scraper', 'Facebook video search'),
    'FB_V_THENETAJI': ('thenetaji/facebook-video-search-scraper', 'Facebook video search'),
    'FB_V_AUTOLAB': ('automation-lab/facebook-public-video-search-results', 'Facebook video search'),
    'GOOGLE_SHORTS': ('simple.actor/google-short-videos', "Google's short videos (here: Facebook reels)"),
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
    ('vis_posts', 'IG_POSTS', '19 Oct test: 8 sample posts fetched again by link, for their full-size pictures and videos'),
    ('vis_afanasenko', 'AFANASENKO', '19 Oct test: on-screen text of 3 music reels, to compare with Claude reading their frames'),
    ('vis_cm_scrapesmith', 'IG_CM_CHEAP', '19 Oct test: the comments on the 8 sample posts'),
    ('vis_cm_apify', 'IG_COMMENTS', '19 Oct test: the same comments with Apify’s own scraper'),
    ('cov_audio', 'APIDOJO', '19 Oct test: reels that use the audio of V7’s own ads'),
    ('cov_google_month', 'GOOGLE', '19 Oct test: Google limited to one month (June)'),
    ('cov_tags', 'IG_TAGS', '19 Oct test: 4 hashtags not tried before'),
    ('ig_google_months', 'GOOGLE', 'public posts: Google search of instagram.com, 12 exact phrases, one month at a time'),
    ('ig_google2_posts', 'IG_POSTS', 'the new Instagram posts Google found month by month, by link'),
    ('ig_tagged_v7_full', 'IG_TAGGED', 'public posts: every Instagram post tagging @v7egypt back to 20 Apr'),
    ('ig_tags2', 'IG_TAGS', 'public posts: 8 more Instagram hashtags'),
    ('ig_kw_wide2', 'IG_KW', 'public posts: one more Instagram keyword sample, 9 phrases, inside the window'),
] + [('igkw_20260420_%02d' % i, 'APIDOJO', 'public posts: Instagram keyword search, phrase %d of 15, since 20 Apr' % (i + 1)) for i in range(15)] + [
    ('igkw_20260420_refetch', 'IG_POSTS', 'the posts that keyword search returned without a caption or likes, by link'),
] + [('igreels_20260420_%02d' % i, 'DAMI', 'public posts: Instagram Reels search, phrases %d to %d of 15, since 20 Apr' % (3 * i + 1, 3 * i + 3)) for i in range(5)] + [
    ('vis_posts_202610190625', 'IG_POSTS', 'fresh media links for the photos and silent reels Claude read (stopped at 775 of 1,230 when the choice was narrowed)'),
    ('vis_posts_202610190636', 'IG_POSTS', 'fresh media links for the rest, narrowed to posts about V7 or tagging it'),
    ('igspeech_about_202610190625', 'SPEECH', 'speech of the new Instagram reels about V7'),
    ('igspeech_tagged_202610190625', 'SPEECH', 'speech of the new reels that tag V7'),
    ('ig_profiles_202610190635', 'PROFILES', 'follower counts of the new Instagram accounts'),
    ('igcm_202610190646', 'IG_CM_CHEAP', 'comments under the public Instagram posts about V7, up to 100 a post (nothing back for 137 of 251 posts)'),
    ('igcm_official_202610190652', 'IG_COMMENTS', 'comments under the posts scrapesmith returned nothing for'),
] + [(f'fbkw_{n}_{i}', a, f'19 Oct Facebook comparison: keyword {i} of 3') for n, a in (('scraperone', 'FB_SEARCH'), ('scrapeforge', 'FB_FORGE'), ('apify', 'FB_APIFY_SEARCH'),
      ('danek', 'FB_DANEK_SEARCH'), ('powerai', 'FB_POWERAI'), ('alienforce', 'FB_ALIEN'), ('fetchcat', 'FB_FETCHCAT'), ('mina', 'FB_MINA'), ('igview', 'FB_IGVIEW'),
      ('silentflow', 'FB_SILENT')) for i in (1, 2, 3)] + [
] + [(f'fbvs_{n}_{i}', a, f'19 Oct Facebook comparison: video search, keyword {i} of 3') for n, a in (('apify', 'FB_V_APIFY'), ('powerai', 'FB_V_POWERAI')) for i in (1, 2, 3)] + [
] + [(f'fbreels_apify_{i}', 'FB_APIFY_SEARCH', f'19 Oct Facebook comparison: reel search, keyword {i} of 3') for i in (1, 2, 3)] + [
    ('fbkw_topapi', 'FB_TOPAPI', '19 Oct Facebook comparison: the 3 keywords'), ('fbkw_headply', 'FB_HEADPLY', '19 Oct Facebook comparison: the 3 keywords'),
    ('fbvs_headply', 'FB_V_HEADPLY', '19 Oct Facebook comparison: video search, the 3 keywords'), ('fbvs_axesso', 'FB_V_AXESSO', '19 Oct Facebook comparison: video search, the 3 keywords'),
    ('fbtags_apify', 'FB_TAGS', '19 Oct Facebook comparison: 4 hashtags'), ('fbgroups_lofo', 'FB_GROUPS', '19 Oct Facebook comparison: public groups, 2 keywords'),
    ('fbgoogle_month', 'GOOGLE', '19 Oct Facebook comparison: Google of facebook.com one month at a time'),
    ('fbdeep_silentflow_top', 'FB_SILENT', '19 Oct depth: 60 results for ڤي سڤن'), ('fbdeep_silentflow_recent', 'FB_SILENT', '19 Oct depth: 60 most recent for ڤي سڤن'),
    ('fbdeep_topapi_top', 'FB_TOPAPI', '19 Oct depth: 60 results for ڤي سڤن'), ('fbdeep_topapi_recent', 'FB_TOPAPI', '19 Oct depth: 60 most recent for ڤي سڤن'),
    ('fbdeep_scrapeforge_top', 'FB_FORGE', '19 Oct depth: 60 results for ڤي سڤن'), ('fbdeep_month_silentflow', 'FB_SILENT', '19 Oct depth: June only'),
    ('fbdeep_month_topapi', 'FB_TOPAPI', '19 Oct depth: June only'), ('fbgap_topapi_details', 'FB_TOPAPI', '19 Oct gap test: with post details'),
    ('fbgap_danek', 'FB_POST_LINK', '19 Oct gap test: 8 posts by link'), ('fbgap_apifyposts', 'FB_POSTS', '19 Oct gap test: 8 posts by link, with captions'),
    ('fbgap_playcount', 'FB_PLAYS', '19 Oct gap test: plays of 5 reels'), ('fbgap_reeldetails', 'FB_REEL_DETAILS', '19 Oct gap test: details of 5 reels'),
    ('fbsp_piotr', 'FB_SP_PIOTR', '19 Oct speech test: 5 reels'), ('fbsp_invideo', 'FB_SPEECH', '19 Oct speech test: 5 reels'), ('fbsp_codenest', 'FB_SP_CODENEST', '19 Oct speech test: 5 reels'),
    ('fbsp_viral', 'FB_SP_VIRAL', '19 Oct speech test: 5 reels'), ('fbsp_alpha', 'FB_SP_ALPHA', '19 Oct speech test: 5 reels'),
    ('fbcm_apify', 'FB_COMMENTS', '19 Oct comment test: 3 posts'), ('fbcm_thedoor', 'FB_CM_CHEAP', '19 Oct comment test: 3 posts'), ('fbpages_apify', 'FB_PAGES', '19 Oct page test: 5 pages'),
] + [(f'fbc_silent_{i:02d}', 'FB_SILENT', 'Facebook public posts: keyword %d of 30' % (i + 1)) for i in range(30)] + [
] + [(f'fbc_one_{i:02d}', 'FB_SEARCH', 'Facebook public posts: keyword %d of 30' % (i + 1)) for i in range(30)] + [
] + [(f'fbc_apify_{i:02d}', 'FB_APIFY_SEARCH', 'Facebook public posts: keyword %d of 30' % (i + 1)) for i in range(30)] + [
] + [(f'fbc_reels_{i:02d}', 'FB_APIFY_SEARCH', 'Facebook reel search: keyword %d of 12' % (i + 1)) for i in range(12)] + [
] + [(f'fbc_vapify_{i:02d}', 'FB_V_APIFY', 'Facebook video search: keyword %d of 12' % (i + 1)) for i in range(12)] + [
    ('fbc_vheadply', 'FB_V_HEADPLY', 'Facebook video search: 12 keywords'), ('fbc_vaxesso', 'FB_V_AXESSO', 'Facebook video search: 12 keywords'),
    ('fbc_groups', 'FB_GROUPS', 'Facebook public groups: 12 keywords (stopped after 62 posts)'),
    ('fbc_google_months', 'GOOGLE', 'Google of facebook.com, 12 exact phrases, one month at a time (stopped at its cap after 114 of 168 pages)'),
    ('fbd_posts', 'FB_POST_LINK', 'the new reels, videos and Google finds, by link'),
    ('fbcm_door_202610191228', 'FB_CM_CHEAP', 'comments under the public Facebook posts about V7, up to 100 a post'),
    ('fbcm_official_202610191241', 'FB_COMMENTS', 'comments under the posts thedoor returned nothing for'),
    ('fbf_pages_202610191228', 'FB_PAGES', 'followers and category of the pages, creators, businesses and news outlets that posted about V7'),
    ('fbf_plays_202610191228', 'FB_PLAYS', 'plays of the Facebook reels and videos about V7 without a view count'),
    ('fbf_speech_202610191228', 'FB_SPEECH', 'what is said in the Facebook reels and videos about V7, and in those whose text is too short to tell'),
    ('fbd_posts_views', 'FB_POST_LINK', 'the video posts about V7 behind a post link, by link, for their plays'),
    ('fbd_posts_names', 'FB_POST_LINK', 'the posts whose search row came without the account name, by link'),
] + [(f'fbrt_{n}_{i}', a, f'19 Oct reel comparison: keyword {i} of 4') for n, a in (('apifyreels', 'FB_APIFY_SEARCH'), ('alien', 'FB_ALIEN'), ('apifyvideo', 'FB_V_APIFY'),
      ('igview', 'FB_V_IGVIEW'), ('lexis', 'FB_V_LEXIS'), ('easyapi', 'FB_V_EASYAPI')) for i in (1, 2, 3, 4)] + [
    ('fbrt_headply', 'FB_V_HEADPLY', '19 Oct reel comparison: the 4 keywords'), ('fbrt_axesso', 'FB_V_AXESSO', '19 Oct reel comparison: the 4 keywords'),
    ('fbrt_sasky', 'FB_V_SASKY', '19 Oct reel comparison: the 4 keywords'), ('fbrt_nataniel', 'FB_V_NATANIEL', '19 Oct reel comparison: the 4 keywords'),
    ('fbrt_thenetaji', 'FB_V_THENETAJI', '19 Oct reel comparison: the 4 keywords'), ('fbrt_autolab', 'FB_V_AUTOLAB', '19 Oct reel comparison: the 4 keywords'),
    ('fbrt_google', 'GOOGLE_SHORTS', '19 Oct reel comparison: the 4 keywords, Facebook only'),
    ('fbd_posts_reeltest', 'FB_POST_LINK', 'the reels the comparison found that the collection lacked, by link'),
    ('fbr_google', 'GOOGLE_SHORTS', "Facebook reels: Google's short videos for the 30 keywords"),
] + [(f'fbr_alien_{i:02d}', 'FB_ALIEN', 'Facebook reels: reels-only search, keyword %d of 15' % (i + 1)) for i in range(15)] + [
    ('fbd_posts_reels2', 'FB_POST_LINK', 'the new reels from that search, by link'),
    ('fbf_plays_202610191508', 'FB_PLAYS', 'plays of the new Facebook videos about V7'), ('fbf_speech_202610191508', 'FB_SPEECH', 'what is said in the new Facebook videos'),
    ('fbf_pages_202610191508', 'FB_PAGES', 'followers of the new pages'), ('fbcm_door_202610191508', 'FB_CM_CHEAP', 'comments under the new Facebook posts about V7'),
    ('fbcm_official_202610191510', 'FB_COMMENTS', 'comments under the new posts thedoor returned nothing for'),
    ('fbd_posts_views_202610191511', 'FB_POST_LINK', 'the new video posts behind a post link, for their plays'),
] + [(f'fbm_forge_{i:02d}', 'FB_FORGE', 'Facebook public posts, a fourth search: keyword %d of 30' % (i + 1)) for i in range(30)] + [
] + [(f'fbm_fetchcat_{i:02d}', 'FB_FETCHCAT', 'Facebook public posts, a fifth search: keyword %d of 30' % (i + 1)) for i in range(30)] + [
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
              '- Claude (`label.py`, through Claude Code on the user’s plan) read and labelled every public post and comment.',
              '- `vis_media.py`: the pictures of Instagram photos and albums, and a frame every 2 seconds of silent and music reels, downloaded from the '
              'links Apify’s post scraper returned (free). `vis_read.py`: Claude (Claude Code on the user’s plan, reading images only) wrote down '
              'the text on them and what they show. On the 19 Oct sample it read as well as afanasenko’s extractor, which costs USD 0.075 a reel.', '']
    (HERE / 'SCRAPERS.md').write_text('\n'.join(lines), encoding='utf-8')
    print('SCRAPERS.md: %d runs, %d scrapers, USD %.2f' % (len(rows), len(by_actor), tot))


if __name__ == '__main__':
    main()
