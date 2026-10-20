# Scrapers used for the real data (17–19 Oct 2026)

Every Apify run of `data/raw/real_17oct/`, written by `scrapers_report.py` from the saved runs. **Returned** is what the scraper gave back; **in window** is what fell between 20 Apr and 16 Oct 2026 after duplicates were merged (an item found by two runs counts for both); **kept** is what the dashboard shows (public posts and comments Claude judged to be about V7, emoji reactions and friend tags under V7’s posts, and every V7 post and reply). Runs that add to posts already collected (follower counts, the speech of reels, posts fetched by link to fill a gap) and the 19 Oct comparison runs keep nothing of their own, so their kept is 0. Cost is Apify’s charge for the run.

## By scraper

| Scraper | Used for | Runs | Returned | Kept | Cost (USD) |
|---|---|---:|---:|---:|---:|
| [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber) | What is said in Facebook videos (speech to text) | 4 | 261 | 0 | 9.90 |
| [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper) | Instagram comments | 5 | 3,506 | 2,997 | 8.06 |
| [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper) | Instagram posts of a profile, or posts by link | 13 | 2,547 | 442 | 5.86 |
| [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper) | Facebook keyword search | 22 | 342 | 0 | 3.90 |
| [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search) | Facebook keyword search | 62 | 1,196 | 498 | 3.59 |
| [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper) | Facebook keyword search | 33 | 592 | 282 | 3.55 |
| [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast) | Facebook posts, reels and videos by link | 9 | 1,431 | 232 | 3.33 |
| [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper) | Facebook keyword search (posts and reels) | 52 | 610 | 104 | 3.10 |
| [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper) | Facebook pages (followers, category) | 4 | 343 | 0 | 2.81 |
| [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper) | TikTok profiles, hashtags, keyword search, videos by link | 11 | 659 | 124 | 2.57 |
| [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper) | Facebook comments | 5 | 995 | 923 | 2.56 |
| [apify/google-search-scraper](https://apify.com/apify/google-search-scraper) | Google search | 13 | 869 | 0 | 2.06 |
| [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper) | Facebook comments (cheaper) | 4 | 4,115 | 3,164 | 2.06 |
| [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper) | Instagram posts that tag a profile | 4 | 765 | 424 | 1.76 |
| [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper) | What is said in Instagram reels (speech to text) | 6 | 311 | 0 | 1.59 |
| [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper) | Facebook keyword search | 46 | 718 | 307 | 1.58 |
| [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts) | Facebook keyword search | 34 | 594 | 215 | 1.54 |
| [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper) | Facebook video search | 19 | 284 | 0 | 1.42 |
| [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper) | Instagram keyword search with a date range | 4 | 676 | 143 | 1.36 |
| [clockworks/tiktok-comments-scraper](https://apify.com/clockworks/tiktok-comments-scraper) | TikTok comments | 2 | 887 | 872 | 0.89 |
| [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper) | Facebook video plays | 4 | 208 | 0 | 0.83 |
| [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper) | Facebook Watch search (returned nothing) | 4 | 0 | 0 | 0.73 |
| [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper) | Instagram accounts (follower counts) | 3 | 315 | 0 | 0.72 |
| [scrapesmith/instagram-comments-scraper](https://apify.com/scrapesmith/instagram-comments-scraper) | Instagram comments (cheaper, but returned nothing for half the posts) | 3 | 1,383 | 1,140 | 0.69 |
| [powerai/facebook-video-search-scraper](https://apify.com/powerai/facebook-video-search-scraper) | Facebook video search | 3 | 30 | 0 | 0.69 |
| [simple.actor/google-short-videos](https://apify.com/simple.actor/google-short-videos) | Google's short videos (Facebook reels; one Instagram test) | 3 | 523 | 0 | 0.65 |
| [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper) | Instagram hashtags (and Instagram keyword search) | 6 | 283 | 25 | 0.65 |
| [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper) | Facebook Watch search | 4 | 31 | 0 | 0.63 |
| [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper) | YouTube keyword search | 3 | 203 | 30 | 0.61 |
| [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper) | YouTube comments | 3 | 1,093 | 731 | 0.46 |
| [headply/facebook-video-search-scraper](https://apify.com/headply/facebook-video-search-scraper) | Facebook video search | 3 | 181 | 16 | 0.42 |
| [lofomachines/facebook-groups-posts-search-scraper](https://apify.com/lofomachines/facebook-groups-posts-search-scraper) | Facebook public groups search | 2 | 72 | 19 | 0.35 |
| [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api) | Instagram keyword search (posts) | 20 | 222 | 87 | 0.33 |
| [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper) | Facebook keyword search | 5 | 113 | 59 | 0.28 |
| [powerai/facebook-post-search-scraper](https://apify.com/powerai/facebook-post-search-scraper) | Facebook keyword search (aborted) | 3 | 0 | 0 | 0.27 |
| [trudax/reddit-scraper-lite](https://apify.com/trudax/reddit-scraper-lite) | Reddit search | 2 | 58 | 2 | 0.26 |
| [afanasenko/instagram-reel-script-extractor](https://apify.com/afanasenko/instagram-reel-script-extractor) | On-screen text and speech of Instagram reels | 1 | 3 | 0 | 0.23 |
| [thenetaji/facebook-video-search-scraper](https://apify.com/thenetaji/facebook-video-search-scraper) | Facebook video search | 1 | 80 | 0 | 0.22 |
| [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper) | Facebook page posts, or posts by link | 3 | 45 | 34 | 0.22 |
| [igview-owner/facebook-old-posts-search](https://apify.com/igview-owner/facebook-old-posts-search) | Facebook keyword search | 3 | 32 | 25 | 0.20 |
| [viralanalyzer/video-transcriber](https://apify.com/viralanalyzer/video-transcriber) | Speech to text (Whisper small) | 1 | 5 | 0 | 0.19 |
| [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper) | Facebook video search | 4 | 56 | 0 | 0.19 |
| [natanielsantos/facebook-video-search-scraper](https://apify.com/natanielsantos/facebook-video-search-scraper) | Facebook video search | 1 | 35 | 0 | 0.13 |
| [danek/facebook-search-ppr](https://apify.com/danek/facebook-search-ppr) | Facebook keyword search | 3 | 33 | 22 | 0.13 |
| [automation-lab/facebook-public-video-search-results](https://apify.com/automation-lab/facebook-public-video-search-results) | Facebook video search | 1 | 28 | 0 | 0.12 |
| [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels) | Instagram search, exact phrases | 3 | 1 | 0 | 0.11 |
| [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper) | Instagram Reels search | 6 | 177 | 73 | 0.11 |
| [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest) | X (Twitter) search | 7 | 465 | 76 | 0.10 |
| [axesso_data/facebook-video-search-scraper](https://apify.com/axesso_data/facebook-video-search-scraper) | Facebook video search | 3 | 327 | 0 | 0.08 |
| [piotrv1001/facebook-video-transcript-scraper](https://apify.com/piotrv1001/facebook-video-transcript-scraper) | Facebook captions and speech to text | 1 | 5 | 0 | 0.07 |
| [headply/facebook-post-search-scraper](https://apify.com/headply/facebook-post-search-scraper) | Facebook keyword search | 1 | 30 | 13 | 0.07 |
| [mina_safwat/facebook-search-actor](https://apify.com/mina_safwat/facebook-search-actor) | Facebook keyword search (no dates) | 3 | 30 | 0 | 0.06 |
| [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels) | Instagram Reels search | 3 | 24 | 0 | 0.06 |
| [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper) | YouTube videos (and comments) | 2 | 29 | 0 | 0.05 |
| [sasky/facebook-keyword-videos-urls-scraper](https://apify.com/sasky/facebook-keyword-videos-urls-scraper) | Facebook video links by keyword | 1 | 11 | 0 | 0.04 |
| [streamers/youtube-channel-scraper](https://apify.com/streamers/youtube-channel-scraper) | YouTube channel videos | 1 | 28 | 28 | 0.03 |
| [apify/instagram-search-scraper](https://apify.com/apify/instagram-search-scraper) | Instagram popular reels for a keyword | 1 | 12 | 0 | 0.03 |
| [codenest/facebook-video-transcript-scraper](https://apify.com/codenest/facebook-video-transcript-scraper) | Facebook's own captions | 1 | 5 | 0 | 0.02 |
| [alpha-scraper/facebook-reels-details-scraper-pro](https://apify.com/alpha-scraper/facebook-reels-details-scraper-pro) | Facebook reel details | 1 | 5 | 5 | 0.02 |
| [alpha-scraper/facebook-transcript-subtitle-scraper](https://apify.com/alpha-scraper/facebook-transcript-subtitle-scraper) | Facebook subtitles (returned none) | 1 | 5 | 0 | 0.01 |
| [apify/instagram-scraper](https://apify.com/apify/instagram-scraper) | Instagram (here: posts that mention a profile) | 1 | 5 | 0 | 0.01 |
| [apify/facebook-hashtag-scraper](https://apify.com/apify/facebook-hashtag-scraper) | Facebook hashtags (returned nothing) | 1 | 2 | 0 | 0.01 |
| [memo23/instagram-reels-search-scraper](https://apify.com/memo23/instagram-reels-search-scraper) | Instagram Reels search, exact phrases | 1 | 2 | 0 | 0.00 |

Total for these runs: USD 74.62 (Apify’s meter for the month also counts platform usage).

## Every run

### t_fb_posts
- **Scraper:** [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper), 2026-10-16
- **Why:** 17 Oct test: 3 of V7 Egypt’s Facebook posts
- **Input:** `{"startUrls": "[1 link]", "resultsLimit": 3, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0160

### t_fb_comments
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on 2 V7 posts
- **Input:** `{"startUrls": "[2 links]", "resultsLimit": 3, "includeNestedComments": true}`
- **Output:** 17 returned · 0 in window · 0 kept · USD 0.0350

### t_ig_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-16
- **Why:** 17 Oct test: 3 of V7 Egypt’s Instagram posts
- **Input:** `{"username": "[1 account]", "resultsLimit": 3, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0069

### t_ig_comments
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on 2 V7 posts
- **Input:** `{"directUrls": "[2 links]", "resultsLimit": 3, "includeNestedComments": true}`
- **Output:** 12 returned · 0 in window · 0 kept · USD 0.0276

### t_tt_comments
- **Scraper:** [clockworks/tiktok-comments-scraper](https://apify.com/clockworks/tiktok-comments-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on a V7 TikTok video
- **Input:** `{"postURLs": "[1 link]", "commentsPerPost": 4, "maxRepliesPerComment": 2}`
- **Output:** 4 returned · 0 in window · 0 kept · USD 0.0040

### t_x
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** 17 Oct test: X search
- **Input:** `{"twitterContent": "(V7 OR \"في سفن\" OR \"ڤي سڤن\") (مشروب OR كانز OR صودا) -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 20, "queryType": "Latest"}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0033

### t_fb_search
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** 17 Oct test: Facebook keyword search
- **Input:** `{"query": "V7 مشروب", "resultsCount": 3, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0091

### t_ig_tag
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-16
- **Why:** 17 Oct test: one Instagram hashtag
- **Input:** `{"hashtags": ["v7egypt"], "resultsLimit": 3, "keywordSearch": false}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0069

### t_tt_search
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-16
- **Why:** 17 Oct test: TikTok keyword search
- **Input:** `{"searchQueries": ["V7 مشروب"], "resultsPerPage": 3}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0100

### t_yt_search
- **Scraper:** [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper), 2026-10-16
- **Why:** 17 Oct test: YouTube keyword search
- **Input:** `{"searchQueries": ["V7 مشروب"], "maxResults": 3, "maxResultsShorts": 0, "maxResultStreams": 0}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0090

### t_reddit
- **Scraper:** [trudax/reddit-scraper-lite](https://apify.com/trudax/reddit-scraper-lite), 2026-10-16
- **Why:** 17 Oct test: Reddit search
- **Input:** `{"searches": ["V7 soda"], "searchPosts": true, "searchComments": false, "sort": "new", "maxItems": 3, "maxPostCount": 3, "maxComments": 0, "postDateLimit": "2026-04-20"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0000

### fb_posts
- **Scraper:** [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper), 2026-10-16
- **Why:** V7 Egypt’s Facebook posts since 20 Apr
- **Input:** `{"startUrls": "[1 link]", "resultsLimit": 80, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 34 returned · 34 in window · 34 kept · USD 0.1710

### ig_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-16
- **Why:** V7 Egypt’s Instagram posts since 20 Apr
- **Input:** `{"username": "[1 account]", "resultsLimit": 120, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 51 returned · 51 in window · 51 kept · USD 0.1173

### tt_posts
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-16
- **Why:** V7 Egypt’s TikTok videos since 20 Apr
- **Input:** `{"profiles": "[1 account]", "profileSorting": "latest", "oldestPostDateUnified": "2026-04-20", "resultsPerPage": 60}`
- **Output:** 19 returned · 19 in window · 19 kept · USD 0.0770

### yt_posts
- **Scraper:** [streamers/youtube-channel-scraper](https://apify.com/streamers/youtube-channel-scraper), 2026-10-16
- **Why:** V7 Egypt’s YouTube videos and Shorts
- **Input:** `{"startUrls": "[1 link]", "maxResults": 40, "maxResultsShorts": 60, "maxResultStreams": 0, "oldestPostDate": "2026-04-20"}`
- **Output:** 28 returned · 28 in window · 28 kept · USD 0.0280

### fb_comments
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-16
- **Why:** every comment on V7 Egypt’s Facebook posts
- **Input:** `{"startUrls": "[31 links]", "resultsLimit": 1500, "includeNestedComments": true, "onlyCommentsNewerThan": "2026-04-20"}`
- **Output:** 898 returned · 898 in window · 877 kept · USD 2.3600

### ig_comments
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-16
- **Why:** every comment on V7 Egypt’s Instagram posts
- **Input:** `{"directUrls": "[36 links]", "resultsLimit": 1500, "includeNestedComments": true}`
- **Output:** 1,141 returned · 1,141 in window · 1,086 kept · USD 2.6243

### tt_comments
- **Scraper:** [clockworks/tiktok-comments-scraper](https://apify.com/clockworks/tiktok-comments-scraper), 2026-10-16
- **Why:** every comment on V7 Egypt’s TikTok videos
- **Input:** `{"postURLs": "[17 links]", "commentsPerPost": 1500, "maxRepliesPerComment": 50}`
- **Output:** 883 returned · 883 in window · 872 kept · USD 0.8830

### abroad_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-16
- **Why:** the posts of V7’s pages abroad
- **Input:** `{"username": "[5 accounts]", "resultsLimit": 60, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 195 returned · 194 in window · 194 kept · USD 0.4485

### abroad_comments
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-16
- **Why:** comments on the pages abroad (stopped at 829 of 1,837 for the budget)
- **Input:** `{"directUrls": "[94 links]", "resultsLimit": 800, "includeNestedComments": true}`
- **Output:** 829 returned · 828 in window · 692 kept · USD 1.9067

### x_drink
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** public posts: V7 + drink words
- **Input:** `{"twitterContent": "(V7 OR \"في سفن\" OR \"ڤي سڤن\" OR \"فى سفن\") (مشروب OR مشروبات OR كانز OR صودا OR soda OR drink OR بيبسي OR كوكاكولا OR رمان OR \"بينا كولادا\" OR بيناكولادا OR \"ليمون نعناع\" OR \"كريم صودا\" OR \"cream soda\" OR شعير OR malt OR بلوبيري OR أناناس OR \"بينك ليموناد\") -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 250, "queryType": "Latest"}`
- **Output:** 43 returned · 43 in window · 22 kept · USD 0.0095

### x_vcola
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** public posts: the V Cola line
- **Input:** `{"twitterContent": "(\"في كولا\" OR \"ڤي كولا\" OR \"V Cola\" OR VCola OR \"ڤي ليمون\" OR \"V Lemon\" OR \"V Orange\" OR \"ڤي أورانج\" OR \"في أورانج\") -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 200, "queryType": "Latest"}`
- **Output:** 200 returned · 200 in window · 25 kept · USD 0.0440

### x_talk
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** public posts: V7 + taste and price words
- **Input:** `{"twitterContent": "(V7 OR \"في سفن\" OR \"ڤي سڤن\" OR \"فى سفن\") (طعم OR طعمها OR جربت OR حلوة OR حلو OR وحشة OR غالية OR غالي OR سعر OR فين OR \"مش لاقي\" OR سكر OR فيتامين OR فيتامينات) -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 200, "queryType": "Latest"}`
- **Output:** 41 returned · 41 in window · 20 kept · USD 0.0090

### x_en
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** public posts: English phrases
- **Input:** `{"twitterContent": "(\"V7 drink\" OR \"V7 soda\" OR \"V7 Egypt\" OR \"V7 cream soda\" OR \"V7 pomegranate\" OR \"v7 7elwa\" OR \"v7 gamda\" OR \"V7 malt\") -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 120, "queryType": "Latest"}`
- **Output:** 15 returned · 7 in window · 7 kept · USD 0.0033

### x_brand
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-16
- **Why:** public posts: V7 + company and boycott words
- **Input:** `{"twitterContent": "(V7 OR \"في سفن\" OR \"ڤي سڤن\" OR \"فى سفن\") (بينيفت OR فيتاليتي OR \"منتج مصري\" OR \"صناعة مصرية\" OR مقاطعة OR بديل) -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 150, "queryType": "Latest"}`
- **Output:** 15 returned · 11 in window · 2 kept · USD 0.0033

### fb_search_00
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 مشروب", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 25 in window · 1 kept · USD 0.0900

### fb_search_01
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 29 in window · 25 kept · USD 0.0900

### fb_search_02
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "في سفن مشروب", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 2 kept · USD 0.0900

### fb_search_03
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 29 in window · 21 kept · USD 0.0900

### fb_search_04
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 رمان", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 29 in window · 9 kept · USD 0.0900

### fb_search_05
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 بينا كولادا", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 2 kept · USD 0.0900

### fb_search_06
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 شعير", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 11 kept · USD 0.0900

### fb_search_07
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "في كولا", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 1 kept · USD 0.0900

### fb_search_08
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "ڤي كولا", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 25 kept · USD 0.0900

### fb_search_09
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "ڤي ليمون", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 29 in window · 4 kept · USD 0.0900

### fb_search_10
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "V7 Egypt", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 28 in window · 0 kept · USD 0.0900

### fb_search_11
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-16
- **Why:** public posts: Facebook keyword search
- **Input:** `{"query": "مشروب V7 غازي", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 29 in window · 17 kept · USD 0.0900

### ig_tags
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-16
- **Why:** public posts: 8 Instagram hashtags
- **Input:** `{"hashtags": ["v7egypt", "فى_سفن", "في_سفن", "vcola", "في_كولا", "ڤي_كولا", "vlemon", "v7creamsoda"], "resultsLimit": 40, "keywordSearch": false}`
- **Output:** 137 returned · 46 in window · 13 kept · USD 0.3151

### tt_search
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-16
- **Why:** public posts: TikTok keyword search with TikTok’s date filter (returned unrelated videos)
- **Input:** `{"searchQueries": ["V7 مشروب", "في سفن", "ڤي سڤن", "V7 كريم صودا", "V7 رمان", "ڤي كولا", "في كولا", "V7 drink", "مشروب V7", "V7 شعير"], "searchSection": "/video", "videoSearchDateFilter": "LAST_6_MONTHS", "resultsPerPage": 30}`
- **Output:** 299 returned · 293 in window · 16 kept · USD 1.2000

### yt_search
- **Scraper:** [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper), 2026-10-16
- **Why:** public posts: YouTube keyword search
- **Input:** `{"searchQueries": ["V7 مشروب", "ڤي سڤن", "V7 cream soda", "في كولا", "V7 soda", "مشروب ڤي سڤن"], "maxResults": 20, "maxResultsShorts": 10, "maxResultStreams": 0, "dateFilter": "year", "sortingOrder": "relevance"}`
- **Output:** 124 returned · 63 in window · 20 kept · USD 0.3720

### reddit
- **Scraper:** [trudax/reddit-scraper-lite](https://apify.com/trudax/reddit-scraper-lite), 2026-10-16
- **Why:** public posts: Reddit search
- **Input:** `{"searches": ["V7 soda", "V7 drink", "V7 cream soda", "في سفن"], "searchPosts": true, "searchComments": true, "sort": "new", "maxItems": 60, "maxPostCount": 15, "maxComments": 0, "postDateLimit": "2026-04-20"}`
- **Output:** 58 returned · 56 in window · 2 kept · USD 0.2604

### t2_ig_tagged
- **Scraper:** [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper), 2026-10-18
- **Why:** 18 Oct test: posts tagging @v7egypt
- **Input:** `{"username": "[1 account]", "resultsLimit": 5}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0115

### t2_ig_kw_posts
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-18
- **Why:** 18 Oct test: Instagram keyword search, posts
- **Input:** `{"hashtags": ["ڤي سڤن", "V7 مشروب"], "keywordSearch": true, "resultsType": "posts", "resultsLimit": 4}`
- **Output:** 8 returned · 0 in window · 0 kept · USD 0.0184

### t2_ig_kw_reels
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-18
- **Why:** 18 Oct test: Instagram keyword search, reels
- **Input:** `{"hashtags": ["ڤي سڤن", "V7 مشروب"], "keywordSearch": true, "resultsType": "reels", "resultsLimit": 4}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0115

### t2_tt_search_eg
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** 18 Oct test: TikTok keyword search from Egypt
- **Input:** `{"searchQueries": ["ڤي سڤن", "في سفن مشروب"], "searchSection": "/video", "resultsPerPage": 5, "proxyCountryCode": "EG"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0410

### t2_tt_top_eg
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** 18 Oct test: TikTok “Top” search from Egypt
- **Input:** `{"searchQueries": ["V7 مشروب"], "searchSection": "", "resultsPerPage": 5, "proxyCountryCode": "EG"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0210

### t2_tt_tags_eg
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** 18 Oct test: TikTok hashtags from Egypt
- **Input:** `{"hashtags": ["v7egypt", "ڤي_سڤن"], "resultsPerPage": 5, "proxyCountryCode": "EG"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0410

### t2_tt_6m_eg
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** 18 Oct test: TikTok’s 6-month date filter from Egypt (unrelated videos)
- **Input:** `{"searchQueries": ["ڤي سڤن"], "searchSection": "/video", "videoSearchDateFilter": "LAST_6_MONTHS", "resultsPerPage": 5, "proxyCountryCode": "EG"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0260

### t2_tt_month_eg
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** 18 Oct test: TikTok’s past-month date filter (nothing)
- **Input:** `{"searchQueries": ["V7 مشروب"], "searchSection": "/video", "videoSearchDateFilter": "PAST_MONTH", "resultsPerPage": 5, "proxyCountryCode": "EG"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0010

### t2_ig_mentions
- **Scraper:** [apify/instagram-scraper](https://apify.com/apify/instagram-scraper), 2026-10-18
- **Why:** 18 Oct test: posts mentioning @v7egypt
- **Input:** `{"directUrls": "[1 link]", "resultsType": "mentions", "resultsLimit": 5}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0115

### t2_ig_kw_dated
- **Scraper:** [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper), 2026-10-18
- **Why:** 18 Oct test: Instagram keyword search inside the window
- **Input:** `{"keywords": ["ڤي سڤن", "V7 drink"], "maxPostsPerKeyword": 5, "dateFrom": "2026-04-20", "dateTo": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0240

### t2_google
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-18
- **Why:** 18 Oct test: Google search of instagram.com and tiktok.com
- **Input:** `{"queries": "\"ڤي سڤن\" site:instagram.com\n\"ڤي سڤن\" site:tiktok.com", "quickDateRange": "m6", "countryCode": "eg", "maxPagesPerQuery": 1}`
- **Output:** 2 returned · 0 in window · 0 kept · USD 0.0050

### ig_tagged_v7
- **Scraper:** [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper), 2026-10-18
- **Why:** public posts: Instagram posts tagging @v7egypt
- **Input:** `{"username": "[1 account]", "resultsLimit": 180}`
- **Output:** 180 returned · 176 in window · 148 kept · USD 0.4140

### ig_tagged_vss
- **Scraper:** [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper), 2026-10-18
- **Why:** public posts: Instagram posts tagging @vsupersoda
- **Input:** `{"username": "[1 account]", "resultsLimit": 60}`
- **Output:** 60 returned · 54 in window · 48 kept · USD 0.1380

### ig_kw_wide
- **Scraper:** [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper), 2026-10-18
- **Why:** public posts: Instagram keyword search, 24 spellings, inside the window
- **Input:** `{"keywords": "[24 items]", "maxPostsPerKeyword": 30, "dateFrom": "2026-04-20", "dateTo": "2026-10-16"}`
- **Output:** 381 returned · 308 in window · 69 kept · USD 0.7500

### google_ig
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-18
- **Why:** public posts: Google search of instagram.com, 18 spellings, past 6 months
- **Input:** `{"queries": "\"ڤي سڤن\" site:instagram.com\n\"في سفن\" site:instagram.com\n\"فى سفن\" site:instagram.com\n\"فيسفن\" site:instagram.com\n\"V7 drink\" site:instagram.com\n\"V7 soda\" site:instagram.com\n\"V7 Egypt\" site:instagram.com\n\"ڤي كولا\" site:instagram.com\n\"في كولا\" site:instagram.com\n\"V Cola\" مصر site:instagram.com\n\"ڤي اورانج\" site:instagram.com\n\"V Orange\" site:instagram.com\n\"V Super Soda\" site:instagram.com\n\"V7 cream soda\"… (542 characters)", "quickDateRange": "m6", "countryCode": "eg", "maxPagesPerQuery": 3}`
- **Output:** 50 returned · 0 in window · 0 kept · USD 0.1001

### google_tt
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-18
- **Why:** public posts: Google search of tiktok.com, 18 spellings, past 6 months
- **Input:** `{"queries": "\"ڤي سڤن\" site:tiktok.com\n\"في سفن\" site:tiktok.com\n\"فى سفن\" site:tiktok.com\n\"فيسفن\" site:tiktok.com\n\"V7 drink\" site:tiktok.com\n\"V7 soda\" site:tiktok.com\n\"V7 Egypt\" site:tiktok.com\n\"ڤي كولا\" site:tiktok.com\n\"في كولا\" site:tiktok.com\n\"V Cola\" مصر site:tiktok.com\n\"ڤي اورانج\" site:tiktok.com\n\"V Orange\" site:tiktok.com\n\"V Super Soda\" site:tiktok.com\n\"V7 cream soda\" site:tiktok.com\n\"V7 كريم صودا\" site:ti… (488 characters)", "quickDateRange": "m6", "countryCode": "eg", "maxPagesPerQuery": 2}`
- **Output:** 32 returned · 0 in window · 0 kept · USD 0.0625

### ig_google_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-18
- **Why:** the Instagram posts Google found (new and inside the window), by link
- **Input:** `{"username": "[108 links]"}`
- **Output:** 108 returned · 105 in window · 54 kept · USD 0.2484

### tt_google_posts
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** the TikTok videos Google found (new and inside the window), by link
- **Input:** `{"postURLs": "[83 links]"}`
- **Output:** 83 returned · 70 in window · 38 kept · USD 0.2500

### fb_search_12
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "فى سفن", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 0 kept · USD 0.0900

### fb_search_13
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "فيسفن", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 3 returned · 3 in window · 0 kept · USD 0.0091

### fb_search_14
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "ڤي اورانج", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.0600

### fb_search_15
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "V Orange", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 21 in window · 0 kept · USD 0.0900

### fb_search_16
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "V Super Soda", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 28 in window · 6 kept · USD 0.0900

### fb_search_17
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-18
- **Why:** public posts: Facebook keyword search, more spellings
- **Input:** `{"query": "V7 بينك ليمونيد", "resultsCount": 30, "searchType": "latest", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 30 returned · 30 in window · 13 kept · USD 0.0900

### x_extra
- **Scraper:** [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest), 2026-10-18
- **Why:** public posts: more spellings on X
- **Input:** `{"twitterContent": "(فيسفن OR ڤيسڤن OR \"ڤى سڤن\" OR \"في سيفن\" OR Vseven OR \"V Orange\" OR \"ڤي اورانج\" OR \"ڤي أورانج\" OR \"V Super Soda\" OR \"ڤي سوبر صودا\") -هافال -Haval -Raptor -midjourney -Vivo -Honor -Jaecoo -Chery since:2026-04-20 until:2026-10-17", "maxItems": 200, "queryType": "Latest"}`
- **Output:** 136 returned · 131 in window · 0 kept · USD 0.0299

### tt_tags_wide
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** public posts: 5 TikTok hashtags, browsed from Egypt
- **Input:** `{"hashtags": ["v7egypt", "ڤي_سڤن", "فيسفن", "vseven", "ڤي_اورانج"], "resultsPerPage": 25, "proxyCountryCode": "EG"}`
- **Output:** 101 returned · 16 in window · 11 kept · USD 0.4050

### tt_wide
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-18
- **Why:** public posts: TikTok keyword search from Egypt, 10 keywords (stopped at its cap after 8)
- **Input:** `{"searchQueries": ["ڤي سڤن", "في سفن مشروب", "فيسفن", "V7 مشروب", "V7 drink", "ڤي كولا", "ڤي اورانج", "V7 كريم صودا", "V7 cream soda", "V7 بينك ليمونيد"], "searchSection": "/video", "resultsPerPage": 30, "proxyCountryCode": "EG"}`
- **Output:** 124 returned · 62 in window · 40 kept · USD 0.4970

### yt_recent
- **Scraper:** [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper), 2026-10-18
- **Why:** public posts: YouTube keyword search, newest first
- **Input:** `{"searchQueries": ["ڤي سڤن", "في سفن مشروب", "V7 drink", "ڤي كولا", "V7 cream soda"], "maxResults": 10, "maxResultsShorts": 10, "maxResultStreams": 0, "dateFilter": "year", "sortingOrder": "date"}`
- **Output:** 76 returned · 30 in window · 10 kept · USD 0.2280

### t3_yt_comments_apidojo
- **Scraper:** [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper), 2026-10-18
- **Why:** 18 Oct test: 20 comments from Kareem Elsayed’s video
- **Input:** `{"startUrls": "[1 link]", "sort": "top", "maxItems": 20, "includeReplies": false}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.0010

### t3_yt_comments_calm
- **Scraper:** [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper), 2026-10-18
- **Why:** 18 Oct test: the same with calm_builder (returned the video only)
- **Input:** `{"startUrls": "[1 link]", "maxResults": 1, "maxComments": 20, "commentsSortBy": "top", "maxReplyDepth": 1, "maxRepliesPerComment": 3}`
- **Output:** 1 returned · 0 in window · 0 kept · USD 0.0194

### yt_own_check
- **Scraper:** [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper), 2026-10-18
- **Why:** are comments on on V7 Egypt’s 28 videos? (27 yes, 1 off)
- **Input:** `{"startUrls": "[28 links]", "maxResults": 1, "maxComments": 0}`
- **Output:** 28 returned · 0 in window · 0 kept · USD 0.0346

### yt_comments_own
- **Scraper:** [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper), 2026-10-18
- **Why:** comments on V7 Egypt’s YouTube videos
- **Input:** `{"startUrls": "[7 links]", "sort": "top", "maxItems": 115, "includeReplies": true}`
- **Output:** 58 returned · 58 in window · 55 kept · USD 0.0115

### yt_comments_public
- **Scraper:** [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper), 2026-10-18
- **Why:** comments on the public YouTube videos about V7
- **Input:** `{"startUrls": "[14 links]", "sort": "top", "maxItems": 1407, "includeReplies": false}`
- **Output:** 1,015 returned · 999 in window · 676 kept · USD 0.4435

### kw_apidojo_1
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-18
- **Why:** 19 Oct comparison: keyword 1 of 3
- **Input:** `{"keywords": ["V7 soda"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0150

### kw_apidojo_2
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-18
- **Why:** 19 Oct comparison: keyword 2 of 3
- **Input:** `{"keywords": ["ڤي سڤن"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0150

### kw_apidojo_3
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-18
- **Why:** 19 Oct comparison: keyword 3 of 3
- **Input:** `{"keywords": ["V7 كريم صودا"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0155

### kw_apify_search
- **Scraper:** [apify/instagram-search-scraper](https://apify.com/apify/instagram-search-scraper), 2026-10-18
- **Why:** 19 Oct comparison: the 3 keywords
- **Input:** `{"search": "V7 soda, ڤي سڤن, V7 كريم صودا", "searchType": "popular", "searchLimit": 10}`
- **Output:** 12 returned · 0 in window · 0 kept · USD 0.0276

### kw_memo23
- **Scraper:** [memo23/instagram-reels-search-scraper](https://apify.com/memo23/instagram-reels-search-scraper), 2026-10-18
- **Why:** 19 Oct comparison: the 3 keywords in quotes
- **Input:** `{"queries": ["\"V7 soda\"", "\"ڤي سڤن\"", "\"V7 كريم صودا\""], "maxResultsPerQuery": 10, "oldestPostDate": "2026-04-20", "newestPostDate": "2026-10-16", "contentType": "posts_and_reels"}`
- **Output:** 2 returned · 0 in window · 0 kept · USD 0.0027

### kw_boolean_1
- **Scraper:** [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 1 of 3 in quotes
- **Input:** `{"searchQuery": "\"V7 soda\"", "resultsLimit": 10, "contentType": "posts_and_reels", "oldestPostDate": "2026-04-20", "newestPostDate": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0400

### kw_boolean_2
- **Scraper:** [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 2 of 3 in quotes
- **Input:** `{"searchQuery": "\"ڤي سڤن\"", "resultsLimit": 10, "contentType": "posts_and_reels", "oldestPostDate": "2026-04-20", "newestPostDate": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0300

### kw_boolean_3
- **Scraper:** [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 3 of 3 in quotes
- **Input:** `{"searchQuery": "\"V7 كريم صودا\"", "resultsLimit": 10, "contentType": "posts_and_reels", "oldestPostDate": "2026-04-20", "newestPostDate": "2026-10-16"}`
- **Output:** 1 returned · 0 in window · 0 kept · USD 0.0415

### kw_dataslayer_1
- **Scraper:** [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "maxPages": 1}`
- **Output:** 12 returned · 0 in window · 0 kept · USD 0.0280

### kw_dataslayer_2
- **Scraper:** [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "maxPages": 1}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0020

### kw_dataslayer_3
- **Scraper:** [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels), 2026-10-18
- **Why:** 19 Oct comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "maxPages": 1}`
- **Output:** 12 returned · 0 in window · 0 kept · USD 0.0280

### kw_dami
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-18
- **Why:** 19 Oct comparison: the 3 keywords
- **Input:** `{"searchQueries": ["V7 soda", "ڤي سڤن", "V7 كريم صودا"], "maxReelsPerTerm": 10, "maxReels": 30, "newerThan": "2026-04-20"}`
- **Output:** 26 returned · 0 in window · 0 kept · USD 0.0180

### kw_seemuapps
- **Scraper:** [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper), 2026-10-18
- **Why:** 19 Oct comparison: the 3 keywords
- **Input:** `{"keywords": ["V7 soda", "ڤي سڤن", "V7 كريم صودا"], "maxPostsPerKeyword": 10, "dateFrom": "2026-04-20", "dateTo": "2026-10-16"}`
- **Output:** 24 returned · 0 in window · 0 kept · USD 0.0585

### kw_apidojo_deep
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-18
- **Why:** 19 Oct: 40 results for "V7 soda" (depth check)
- **Input:** `{"keywords": ["V7 soda"], "maxItems": 40, "until": "2026-04-20"}`
- **Output:** 40 returned · 0 in window · 0 kept · USD 0.0315

### kw_refetch_test
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-18
- **Why:** 19 Oct: the 25 posts apidojo returned without a caption or likes, fetched by link
- **Input:** `{"username": "[25 links]"}`
- **Output:** 25 returned · 0 in window · 0 kept · USD 0.0575

### kw_transcript_test
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-18
- **Why:** 19 Oct test: speech of 3 Egyptian Arabic reels
- **Input:** `{"bulkUrls": "[3 links]", "resultsLimit": 3}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0205

### ig_profiles
- **Scraper:** [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper), 2026-10-18
- **Why:** follower counts of the 175 Instagram accounts that posted about V7 without one
- **Input:** `{"usernames": "[175 accounts]"}`
- **Output:** 175 returned · 0 in window · 0 kept · USD 0.4025

### igspeech_about
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-18
- **Why:** speech of the 163 Instagram reels about V7
- **Input:** `{"bulkUrls": "[163 links]", "resultsLimit": 163}`
- **Output:** 163 returned · 0 in window · 0 kept · USD 0.8175

### igspeech_tagged
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-18
- **Why:** speech of the 32 reels that tag V7 but whose caption alone did not show it
- **Input:** `{"bulkUrls": "[32 links]", "resultsLimit": 32}`
- **Output:** 32 returned · 0 in window · 0 kept · USD 0.1790

### vis_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** 19 Oct test: 8 sample posts fetched again by link, for their full-size pictures and videos
- **Input:** `{"username": "[8 links]"}`
- **Output:** 8 returned · 0 in window · 0 kept · USD 0.0184

### vis_afanasenko
- **Scraper:** [afanasenko/instagram-reel-script-extractor](https://apify.com/afanasenko/instagram-reel-script-extractor), 2026-10-19
- **Why:** 19 Oct test: on-screen text of 3 music reels, to compare with Claude reading their frames
- **Input:** `{"reelUrls": "[3 links]", "maxItemsMode1": 3}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.2250

### vis_cm_scrapesmith
- **Scraper:** [scrapesmith/instagram-comments-scraper](https://apify.com/scrapesmith/instagram-comments-scraper), 2026-10-19
- **Why:** 19 Oct test: the comments on the 8 sample posts
- **Input:** `{"postUrls": "[8 links]", "maxCommentsPerPost": 20, "sortOrder": "popular"}`
- **Output:** 86 returned · 0 in window · 0 kept · USD 0.0431

### vis_cm_apify
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-19
- **Why:** 19 Oct test: the same comments with Apify’s own scraper
- **Input:** `{"directUrls": "[8 links]", "resultsLimit": 20}`
- **Output:** 86 returned · 0 in window · 0 kept · USD 0.1978

### cov_audio
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** 19 Oct test: reels that use the audio of V7’s own ads
- **Input:** `{"startUrls": "[2 links]", "maxItems": 20}`
- **Output:** 2 returned · 0 in window · 0 kept · USD 0.0100

### cov_google_month
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-19
- **Why:** 19 Oct test: Google limited to one month (June)
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 1, "countryCode": "eg"}`
- **Output:** 2 returned · 0 in window · 0 kept · USD 0.0050

### cov_tags
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-19
- **Why:** 19 Oct test: 4 hashtags not tried before
- **Input:** `{"hashtags": ["ڤي_سڤن", "vsupersoda", "vorange", "v7drink"], "resultsLimit": 5, "keywordSearch": false}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.0460

### ig_google_months
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-19
- **Why:** public posts: Google search of instagram.com, 12 exact phrases, one month at a time
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 3, "countryCode": "eg"}`
- **Output:** 190 returned · 0 in window · 0 kept · USD 0.4476

### ig_google2_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** the new Instagram posts Google found month by month, by link
- **Input:** `{"username": "[882 links]"}`
- **Output:** 882 returned · 857 in window · 97 kept · USD 2.0286

### ig_tagged_v7_full
- **Scraper:** [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper), 2026-10-19
- **Why:** public posts: every Instagram post tagging @v7egypt back to 20 Apr
- **Input:** `{"username": "[1 account]", "resultsLimit": 520}`
- **Output:** 520 returned · 264 in window · 228 kept · USD 1.1960

### ig_tags2
- **Scraper:** [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper), 2026-10-19
- **Why:** public posts: 8 more Instagram hashtags
- **Input:** `{"hashtags": ["ڤي_سڤن", "vsupersoda", "vorange", "v7drink", "v7creamsoda", "ڤي_كولا", "vcolaegypt", "ڤي_اورانج"], "resultsLimit": 30, "keywordSearch": false}`
- **Output:** 110 returned · 13 in window · 12 kept · USD 0.2530

### ig_kw_wide2
- **Scraper:** [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper), 2026-10-19
- **Why:** public posts: one more Instagram keyword sample, 9 phrases, inside the window
- **Input:** `{"keywords": ["V Super Soda", "V7 cream soda", "V7 كريم صودا", "V7 pink lemonade", "V7 بينك ليمونيد", "V7 رمان", "V7 بلوبيري", "V7 شعير", "V7 كانز"], "maxPostsPerKeyword": 30, "dateFrom": "2026-04-20", "dateTo": "2026-10-16"}`
- **Output:** 261 returned · 196 in window · 74 kept · USD 0.5310

### igkw_20260420_00
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 1 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 soda"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 9 kept · USD 0.0150

### igkw_20260420_01
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 2 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 drink"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 9 kept · USD 0.0150

### igkw_20260420_02
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 3 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 Egypt"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 10 in window · 9 kept · USD 0.0165

### igkw_20260420_03
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 4 of 15, since 20 Apr
- **Input:** `{"keywords": ["مشروب V7"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 7 in window · 3 kept · USD 0.0170

### igkw_20260420_04
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 5 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 كانز"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 10 in window · 7 kept · USD 0.0150

### igkw_20260420_05
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 6 of 15, since 20 Apr
- **Input:** `{"keywords": ["V Cola"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 3 in window · 0 kept · USD 0.0150

### igkw_20260420_06
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 7 of 15, since 20 Apr
- **Input:** `{"keywords": ["V Orange"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 7 in window · 2 kept · USD 0.0155

### igkw_20260420_07
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 8 of 15, since 20 Apr
- **Input:** `{"keywords": ["V Super Soda"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 8 in window · 6 kept · USD 0.0180

### igkw_20260420_08
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 9 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 cream soda"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 9 kept · USD 0.0150

### igkw_20260420_09
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 10 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 كريم صودا"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 7 kept · USD 0.0150

### igkw_20260420_10
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 11 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 pink lemonade"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 4 kept · USD 0.0195

### igkw_20260420_11
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 12 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 بينك ليمونيد"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 10 in window · 7 kept · USD 0.0150

### igkw_20260420_12
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 13 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 رمان"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 3 kept · USD 0.0200

### igkw_20260420_13
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 14 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 بلوبيري"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 10 in window · 7 kept · USD 0.0200

### igkw_20260420_14
- **Scraper:** [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api), 2026-10-19
- **Why:** public posts: Instagram keyword search, phrase 15 of 15, since 20 Apr
- **Input:** `{"keywords": ["V7 شعير"], "maxItems": 10, "until": "2026-04-20"}`
- **Output:** 10 returned · 9 in window · 5 kept · USD 0.0150

### igkw_20260420_refetch
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** the posts that keyword search returned without a caption or likes, by link
- **Input:** `{"username": "[45 links]"}`
- **Output:** 45 returned · 43 in window · 28 kept · USD 0.1035

### igreels_20260420_00
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-19
- **Why:** public posts: Instagram Reels search, phrases 1 to 3 of 15, since 20 Apr
- **Input:** `{"searchQueries": ["V7 soda", "V7 drink", "V7 Egypt"], "maxReelsPerTerm": 30, "maxReels": 90, "newerThan": "2026-04-20"}`
- **Output:** 42 returned · 37 in window · 31 kept · USD 0.0239

### igreels_20260420_01
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-19
- **Why:** public posts: Instagram Reels search, phrases 4 to 6 of 15, since 20 Apr
- **Input:** `{"searchQueries": ["مشروب V7", "V7 كانز", "V Cola"], "maxReelsPerTerm": 30, "maxReels": 90, "newerThan": "2026-04-20"}`
- **Output:** 37 returned · 21 in window · 10 kept · USD 0.0184

### igreels_20260420_02
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-19
- **Why:** public posts: Instagram Reels search, phrases 7 to 9 of 15, since 20 Apr
- **Input:** `{"searchQueries": ["V Orange", "V Super Soda", "V7 cream soda"], "maxReelsPerTerm": 30, "maxReels": 90, "newerThan": "2026-04-20"}`
- **Output:** 39 returned · 33 in window · 20 kept · USD 0.0235

### igreels_20260420_03
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-19
- **Why:** public posts: Instagram Reels search, phrases 10 to 12 of 15, since 20 Apr
- **Input:** `{"searchQueries": ["V7 كريم صودا", "V7 pink lemonade", "V7 بينك ليمونيد"], "maxReelsPerTerm": 30, "maxReels": 90, "newerThan": "2026-04-20"}`
- **Output:** 30 returned · 29 in window · 12 kept · USD 0.0196

### igreels_20260420_04
- **Scraper:** [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper), 2026-10-19
- **Why:** public posts: Instagram Reels search, phrases 13 to 15 of 15, since 20 Apr
- **Input:** `{"searchQueries": ["V7 رمان", "V7 بلوبيري", "V7 شعير"], "maxReelsPerTerm": 30, "maxReels": 90, "newerThan": "2026-04-20"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0034

### vis_posts_202610190625
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** fresh media links for the photos and silent reels Claude read (stopped at 775 of 1,230 when the choice was narrowed)
- **Input:** `{"note": "stopped: the selection was too wide (1,230 posts); what it fetched is kept"}`
- **Output:** 775 returned · 0 in window · 0 kept · USD 1.7825

### vis_posts_202610190636
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** fresh media links for the rest, narrowed to posts about V7 or tagging it
- **Input:** `{"username": "[82 links]"}`
- **Output:** 82 returned · 0 in window · 0 kept · USD 0.1886

### igspeech_about_202610190625
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-19
- **Why:** speech of the new Instagram reels about V7
- **Input:** `{"bulkUrls": "[100 links]", "resultsLimit": 100}`
- **Output:** 100 returned · 0 in window · 0 kept · USD 0.5095

### igspeech_tagged_202610190625
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-19
- **Why:** speech of the new reels that tag V7
- **Input:** `{"bulkUrls": "[8 links]", "resultsLimit": 8}`
- **Output:** 8 returned · 0 in window · 0 kept · USD 0.0395

### ig_profiles_202610190635
- **Scraper:** [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper), 2026-10-19
- **Why:** follower counts of the new Instagram accounts
- **Input:** `{"usernames": "[110 accounts]"}`
- **Output:** 110 returned · 0 in window · 0 kept · USD 0.2530

### igcm_202610190646
- **Scraper:** [scrapesmith/instagram-comments-scraper](https://apify.com/scrapesmith/instagram-comments-scraper), 2026-10-19
- **Why:** comments under the public Instagram posts about V7, up to 100 a post (nothing back for 137 of 251 posts)
- **Input:** `{"postUrls": "[251 links]", "maxCommentsPerPost": 100, "sortOrder": "popular"}`
- **Output:** 1,221 returned · 1,211 in window · 1,082 kept · USD 0.6106

### igcm_official_202610190652
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-19
- **Why:** comments under the posts scrapesmith returned nothing for
- **Input:** `{"directUrls": "[137 links]", "resultsLimit": 100, "includeNestedComments": false}`
- **Output:** 1,438 returned · 1,422 in window · 1,219 kept · USD 3.3074

### fbkw_scraperone_1
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 8 in window · 2 kept · USD 0.0301

### fbkw_scraperone_2
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 9 kept · USD 0.0301

### fbkw_scraperone_3
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0301

### fbkw_scrapeforge_1
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "search_type": "posts", "max_results": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 8 kept · USD 0.0260

### fbkw_scrapeforge_2
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_results": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 9 returned · 9 in window · 7 kept · USD 0.0234

### fbkw_scrapeforge_3
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_results": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 9 returned · 9 in window · 8 kept · USD 0.0234

### fbkw_apify_1
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"categories": ["V7 soda"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 7 in window · 7 kept · USD 0.0510

### fbkw_apify_2
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"categories": ["ڤي سڤن"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 4 in window · 4 kept · USD 0.0510

### fbkw_apify_3
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"categories": ["V7 كريم صودا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0510

### fbkw_danek_1
- **Scraper:** [danek/facebook-search-ppr](https://apify.com/danek/facebook-search-ppr), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 11 returned · 9 in window · 5 kept · USD 0.0440

### fbkw_danek_2
- **Scraper:** [danek/facebook-search-ppr](https://apify.com/danek/facebook-search-ppr), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 11 returned · 10 in window · 8 kept · USD 0.0440

### fbkw_danek_3
- **Scraper:** [danek/facebook-search-ppr](https://apify.com/danek/facebook-search-ppr), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 11 returned · 11 in window · 9 kept · USD 0.0440

### fbkw_powerai_1
- **Scraper:** [powerai/facebook-post-search-scraper](https://apify.com/powerai/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0900

### fbkw_powerai_2
- **Scraper:** [powerai/facebook-post-search-scraper](https://apify.com/powerai/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0900

### fbkw_powerai_3
- **Scraper:** [powerai/facebook-post-search-scraper](https://apify.com/powerai/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0900

### fbkw_alienforce_1
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"search_type": "posts", "keyword": "V7 soda", "results_limit": 10, "start_date": "2026-04-20", "end_date": "2026-10-16", "follow_post_scraping": true}`
- **Output:** 6 returned · 0 in window · 0 kept · USD 0.0727

### fbkw_alienforce_2
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"search_type": "posts", "keyword": "ڤي سڤن", "results_limit": 10, "start_date": "2026-04-20", "end_date": "2026-10-16", "follow_post_scraping": true}`
- **Output:** 4 returned · 0 in window · 0 kept · USD 0.0524

### fbkw_alienforce_3
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"search_type": "posts", "keyword": "V7 كريم صودا", "results_limit": 10, "start_date": "2026-04-20", "end_date": "2026-10-16", "follow_post_scraping": true}`
- **Output:** 7 returned · 0 in window · 0 kept · USD 0.0847

### fbkw_fetchcat_1
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0600

### fbkw_fetchcat_2
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0600

### fbkw_fetchcat_3
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 10, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 9 kept · USD 0.0600

### fbkw_mina_1
- **Scraper:** [mina_safwat/facebook-search-actor](https://apify.com/mina_safwat/facebook-search-actor), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "limit": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0201

### fbkw_mina_2
- **Scraper:** [mina_safwat/facebook-search-actor](https://apify.com/mina_safwat/facebook-search-actor), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "limit": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0201

### fbkw_mina_3
- **Scraper:** [mina_safwat/facebook-search-actor](https://apify.com/mina_safwat/facebook-search-actor), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "limit": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0201

### fbkw_igview_1
- **Scraper:** [igview-owner/facebook-old-posts-search](https://apify.com/igview-owner/facebook-old-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "maxResults": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 10 returned · 8 in window · 8 kept · USD 0.0633

### fbkw_igview_2
- **Scraper:** [igview-owner/facebook-old-posts-search](https://apify.com/igview-owner/facebook-old-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "maxResults": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 11 returned · 9 in window · 8 kept · USD 0.0682

### fbkw_igview_3
- **Scraper:** [igview-owner/facebook-old-posts-search](https://apify.com/igview-owner/facebook-old-posts-search), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "maxResults": 10, "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 11 returned · 10 in window · 9 kept · USD 0.0680

### fbkw_silentflow_1
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 1 of 3
- **Input:** `{"query": "V7 soda", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0221

### fbkw_silentflow_2
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0221

### fbkw_silentflow_3
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 10 in window · 9 kept · USD 0.0221

### fbvs_apify_1
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 1 of 3
- **Input:** `{"searchTerm": "V7 soda", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0500

### fbvs_apify_2
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 2 of 3
- **Input:** `{"searchTerm": "ڤي سڤن", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0500

### fbvs_apify_3
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 3 of 3
- **Input:** `{"searchTerm": "V7 كريم صودا", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0500

### fbvs_powerai_1
- **Scraper:** [powerai/facebook-video-search-scraper](https://apify.com/powerai/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 1 of 3
- **Input:** `{"query": "V7 soda", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.2299

### fbvs_powerai_2
- **Scraper:** [powerai/facebook-video-search-scraper](https://apify.com/powerai/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 2 of 3
- **Input:** `{"query": "ڤي سڤن", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.2299

### fbvs_powerai_3
- **Scraper:** [powerai/facebook-video-search-scraper](https://apify.com/powerai/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, keyword 3 of 3
- **Input:** `{"query": "V7 كريم صودا", "maxResults": 10, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.2299

### fbreels_apify_1
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: reel search, keyword 1 of 3
- **Input:** `{"categories": ["V7 soda"], "searchType": "reels", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbreels_apify_2
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: reel search, keyword 2 of 3
- **Input:** `{"categories": ["ڤي سڤن"], "searchType": "reels", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbreels_apify_3
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: reel search, keyword 3 of 3
- **Input:** `{"categories": ["V7 كريم صودا"], "searchType": "reels", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbkw_topapi
- **Scraper:** [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: the 3 keywords
- **Input:** `{"searchQueries": ["V7 soda", "ڤي سڤن", "V7 كريم صودا"], "sortBy": "top", "startDate": "2026-04-20", "endDate": "2026-10-16", "maxPostsPerQuery": 10, "includePostDetails": false}`
- **Output:** 30 returned · 30 in window · 29 kept · USD 0.0720

### fbkw_headply
- **Scraper:** [headply/facebook-post-search-scraper](https://apify.com/headply/facebook-post-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: the 3 keywords
- **Input:** `{"searchQueries": ["V7 soda", "ڤي سڤن", "V7 كريم صودا"], "searchSort": "top", "maxItemsPerTarget": 10, "mode": "postSearch"}`
- **Output:** 30 returned · 13 in window · 13 kept · USD 0.0700

### fbvs_headply
- **Scraper:** [headply/facebook-video-search-scraper](https://apify.com/headply/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, the 3 keywords
- **Input:** `{"searchQueries": ["V7 soda", "ڤي سڤن", "V7 كريم صودا"], "maxItemsPerTarget": 10, "mode": "videoSearch"}`
- **Output:** 22 returned · 9 in window · 7 kept · USD 0.0516

### fbvs_axesso
- **Scraper:** [axesso_data/facebook-video-search-scraper](https://apify.com/axesso_data/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: video search, the 3 keywords
- **Input:** `{"input": [{"keyword": "V7 soda", "sort": "RELEVANCE", "maxPosts": 10}, {"keyword": "ڤي سڤن", "sort": "RELEVANCE", "maxPosts": 10}, {"keyword": "V7 كريم صودا", "sort": "RELEVANCE", "maxPosts": 10}]}`
- **Output:** 30 returned · 0 in window · 0 kept · USD 0.0075

### fbtags_apify
- **Scraper:** [apify/facebook-hashtag-scraper](https://apify.com/apify/facebook-hashtag-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: 4 hashtags
- **Input:** `{"keywordList": ["v7egypt", "ڤي_سڤن", "vsupersoda", "ڤيسڤن"], "resultsLimit": 10}`
- **Output:** 2 returned · 0 in window · 0 kept · USD 0.0100

### fbgroups_lofo
- **Scraper:** [lofomachines/facebook-groups-posts-search-scraper](https://apify.com/lofomachines/facebook-groups-posts-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: public groups, 2 keywords
- **Input:** `{"keywords": ["V7 drink", "ڤي سڤن"], "afterDate": "this_year", "maxPosts": 10, "countryCode": "eg"}`
- **Output:** 10 returned · 9 in window · 6 kept · USD 0.0699

### fbgoogle_month
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-19
- **Why:** 19 Oct Facebook comparison: Google of facebook.com one month at a time
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 2, "countryCode": "eg"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0100

### fbdeep_silentflow_top
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct depth: 60 results for ڤي سڤن
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 60, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 22 returned · 22 in window · 10 kept · USD 0.0485

### fbdeep_silentflow_recent
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct depth: 60 most recent for ڤي سڤن
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 60, "recent_posts": true, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 33 returned · 33 in window · 10 kept · USD 0.0726

### fbdeep_topapi_top
- **Scraper:** [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper), 2026-10-19
- **Why:** 19 Oct depth: 60 results for ڤي سڤن
- **Input:** `{"searchQueries": ["ڤي سڤن"], "sortBy": "top", "startDate": "2026-04-20", "endDate": "2026-10-16", "maxPostsPerQuery": 60}`
- **Output:** 26 returned · 26 in window · 10 kept · USD 0.0624

### fbdeep_topapi_recent
- **Scraper:** [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper), 2026-10-19
- **Why:** 19 Oct depth: 60 most recent for ڤي سڤن
- **Input:** `{"searchQueries": ["ڤي سڤن"], "sortBy": "recent", "startDate": "2026-04-20", "endDate": "2026-10-16", "maxPostsPerQuery": 60}`
- **Output:** 30 returned · 30 in window · 10 kept · USD 0.0720

### fbdeep_scrapeforge_top
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** 19 Oct depth: 60 results for ڤي سڤن
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_results": 60, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 32 returned · 32 in window · 6 kept · USD 0.0829

### fbdeep_month_silentflow
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct depth: June only
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 30, "start_date": "2026-06-01", "end_date": "2026-06-30"}`
- **Output:** 19 returned · 19 in window · 1 kept · USD 0.0419

### fbdeep_month_topapi
- **Scraper:** [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper), 2026-10-19
- **Why:** 19 Oct depth: June only
- **Input:** `{"searchQueries": ["ڤي سڤن"], "sortBy": "top", "startDate": "2026-06-01", "endDate": "2026-06-30", "maxPostsPerQuery": 30}`
- **Output:** 17 returned · 17 in window · 1 kept · USD 0.0408

### fbgap_topapi_details
- **Scraper:** [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper), 2026-10-19
- **Why:** 19 Oct gap test: with post details
- **Input:** `{"searchQueries": ["V7 كريم صودا"], "sortBy": "top", "startDate": "2026-04-20", "endDate": "2026-10-16", "maxPostsPerQuery": 10, "includePostDetails": true}`
- **Output:** 10 returned · 10 in window · 9 kept · USD 0.0340

### fbgap_danek
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** 19 Oct gap test: 8 posts by link
- **Input:** `{"direct_urls": "[8 links]"}`
- **Output:** 8 returned · 8 in window · 8 kept · USD 0.0187

### fbgap_apifyposts
- **Scraper:** [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper), 2026-10-19
- **Why:** 19 Oct gap test: 8 posts by link, with captions
- **Input:** `{"startUrls": "[8 links]", "captionText": true}`
- **Output:** 8 returned · 0 in window · 0 kept · USD 0.0330

### fbgap_playcount
- **Scraper:** [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper), 2026-10-19
- **Why:** 19 Oct gap test: plays of 5 reels
- **Input:** `{"startUrls": "[5 links]"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0202

### fbgap_reeldetails
- **Scraper:** [alpha-scraper/facebook-reels-details-scraper-pro](https://apify.com/alpha-scraper/facebook-reels-details-scraper-pro), 2026-10-19
- **Why:** 19 Oct gap test: details of 5 reels
- **Input:** `{"startUrls": "[5 links]"}`
- **Output:** 5 returned · 5 in window · 5 kept · USD 0.0189

### fbsp_piotr
- **Scraper:** [piotrv1001/facebook-video-transcript-scraper](https://apify.com/piotrv1001/facebook-video-transcript-scraper), 2026-10-19
- **Why:** 19 Oct speech test: 5 reels
- **Input:** `{"pages": [], "videoUrls": "[5 links]", "transcribeWithAI": true, "language": "auto", "maxResults": 5}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0751

### fbsp_invideo
- **Scraper:** [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber), 2026-10-19
- **Why:** 19 Oct speech test: 5 reels
- **Input:** `{"video_urls": "[5 links]"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.1750

### fbsp_codenest
- **Scraper:** [codenest/facebook-video-transcript-scraper](https://apify.com/codenest/facebook-video-transcript-scraper), 2026-10-19
- **Why:** 19 Oct speech test: 5 reels
- **Input:** `{"post_urls": "[5 links]"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0245

### fbsp_viral
- **Scraper:** [viralanalyzer/video-transcriber](https://apify.com/viralanalyzer/video-transcriber), 2026-10-19
- **Why:** 19 Oct speech test: 5 reels
- **Input:** `{"mediaUrls": "[5 links]", "language": "ar", "model": "small", "maxMinutesPerItem": 5}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.1945

### fbsp_alpha
- **Scraper:** [alpha-scraper/facebook-transcript-subtitle-scraper](https://apify.com/alpha-scraper/facebook-transcript-subtitle-scraper), 2026-10-19
- **Why:** 19 Oct speech test: 5 reels
- **Input:** `{"videoUrls": "[5 links]", "outputFormat": "all_type"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0129

### fbcm_apify
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-19
- **Why:** 19 Oct comment test: 3 posts
- **Input:** `{"startUrls": "[3 links]", "resultsLimit": 30, "includeNestedComments": false}`
- **Output:** 26 returned · 0 in window · 0 kept · USD 0.0530

### fbcm_thedoor
- **Scraper:** [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper), 2026-10-19
- **Why:** 19 Oct comment test: 3 posts
- **Input:** `{"postUrls": "[3 links]", "targetComments": 30, "includeReplies": false, "orderingMode": "MOST_RELEVANT"}`
- **Output:** 25 returned · 0 in window · 0 kept · USD 0.0126

### fbpages_apify
- **Scraper:** [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper), 2026-10-19
- **Why:** 19 Oct page test: 5 pages
- **Input:** `{"startUrls": "[5 links]"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0410

### fbc_silent_00
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 1 of 30
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 10 kept · USD 0.0441

### fbc_silent_01
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 2 of 30
- **Input:** `{"query": "ڤيسڤن", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.0441

### fbc_silent_02
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 3 of 30
- **Input:** `{"query": "مشروب ڤي سڤن", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 14 returned · 14 in window · 2 kept · USD 0.0309

### fbc_silent_03
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 4 of 30
- **Input:** `{"query": "ڤي سڤن كريم صودا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 6 kept · USD 0.0441

### fbc_silent_04
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 5 of 30
- **Input:** `{"query": "ڤي سڤن رمان", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 1 returned · 1 in window · 1 kept · USD 0.0023

### fbc_silent_05
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 6 of 30
- **Input:** `{"query": "ڤي سڤن بينا كولادا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 4 kept · USD 0.0441

### fbc_silent_06
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 7 of 30
- **Input:** `{"query": "ڤي سڤن شعير", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 2 kept · USD 0.0397

### fbc_silent_07
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 8 of 30
- **Input:** `{"query": "ڤي سڤن ليمون نعناع", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.0441

### fbc_silent_08
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 9 of 30
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.0441

### fbc_silent_09
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 10 of 30
- **Input:** `{"query": "ڤي كولا دايت", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 11 kept · USD 0.0441

### fbc_silent_10
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 11 of 30
- **Input:** `{"query": "ڤي اورانج", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.0441

### fbc_silent_11
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 12 of 30
- **Input:** `{"query": "ڤي ليمون", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 3 kept · USD 0.0441

### fbc_silent_12
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 13 of 30
- **Input:** `{"query": "ڤي سوبر صودا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 8 kept · USD 0.0441

### fbc_silent_13
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 14 of 30
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 17 kept · USD 0.0441

### fbc_silent_14
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 15 of 30
- **Input:** `{"query": "V7 cream soda", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 20 kept · USD 0.0441

### fbc_silent_15
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 16 of 30
- **Input:** `{"query": "V7 مشروب", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 9 kept · USD 0.0441

### fbc_silent_16
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 17 of 30
- **Input:** `{"query": "مشروب V7", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 8 kept · USD 0.0441

### fbc_silent_17
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 18 of 30
- **Input:** `{"query": "V7 رمان", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.0441

### fbc_silent_18
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 19 of 30
- **Input:** `{"query": "V7 بينا كولادا", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 18 kept · USD 0.0441

### fbc_silent_19
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 20 of 30
- **Input:** `{"query": "V7 بلوبيري", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 4 kept · USD 0.0441

### fbc_silent_20
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 21 of 30
- **Input:** `{"query": "V7 شعير", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 1 kept · USD 0.0441

### fbc_silent_21
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 22 of 30
- **Input:** `{"query": "V7 بينك ليمونيد", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 8 kept · USD 0.0441

### fbc_silent_22
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 23 of 30
- **Input:** `{"query": "V7 pink lemonade", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.0441

### fbc_silent_23
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 24 of 30
- **Input:** `{"query": "V7 Egypt", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 2 kept · USD 0.0441

### fbc_silent_24
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 25 of 30
- **Input:** `{"query": "V7 soda", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 20 kept · USD 0.0441

### fbc_silent_25
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 26 of 30
- **Input:** `{"query": "V7 drink", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 5 kept · USD 0.0441

### fbc_silent_26
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 27 of 30
- **Input:** `{"query": "V Cola", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 7 kept · USD 0.0441

### fbc_silent_27
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 28 of 30
- **Input:** `{"query": "V Orange", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 2 kept · USD 0.0441

### fbc_silent_28
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 29 of 30
- **Input:** `{"query": "V Super Soda", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 16 in window · 16 kept · USD 0.0441

### fbc_silent_29
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 30 of 30
- **Input:** `{"query": "V7 كانز", "search_type": "posts", "max_posts": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 13 kept · USD 0.0441

### fbc_one_00
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 1 of 30
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 17 kept · USD 0.0600

### fbc_one_01
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 2 of 30
- **Input:** `{"query": "ڤيسڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 13 in window · 0 kept · USD 0.0600

### fbc_one_02
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 3 of 30
- **Input:** `{"query": "مشروب ڤي سڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 5 kept · USD 0.0600

### fbc_one_03
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 4 of 30
- **Input:** `{"query": "ڤي سڤن كريم صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 15 returned · 15 in window · 6 kept · USD 0.0450

### fbc_one_04
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 5 of 30
- **Input:** `{"query": "ڤي سڤن رمان", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 17 in window · 17 kept · USD 0.0600

### fbc_one_05
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 6 of 30
- **Input:** `{"query": "ڤي سڤن بينا كولادا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 3 kept · USD 0.0600

### fbc_one_06
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 7 of 30
- **Input:** `{"query": "ڤي سڤن شعير", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 8 kept · USD 0.0600

### fbc_one_07
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 8 of 30
- **Input:** `{"query": "ڤي سڤن ليمون نعناع", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 11 kept · USD 0.0600

### fbc_one_08
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 9 of 30
- **Input:** `{"query": "ڤي كولا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 19 kept · USD 0.0600

### fbc_one_09
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 10 of 30
- **Input:** `{"query": "ڤي كولا دايت", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 11 kept · USD 0.0600

### fbc_one_10
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 11 of 30
- **Input:** `{"query": "ڤي اورانج", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 0 kept · USD 0.0600

### fbc_one_11
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 12 of 30
- **Input:** `{"query": "ڤي ليمون", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 14 in window · 0 kept · USD 0.0600

### fbc_one_12
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 13 of 30
- **Input:** `{"query": "ڤي سوبر صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 3 kept · USD 0.0600

### fbc_one_13
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 14 of 30
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 17 kept · USD 0.0600

### fbc_one_14
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 15 of 30
- **Input:** `{"query": "V7 cream soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 18 kept · USD 0.0600

### fbc_one_15
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 16 of 30
- **Input:** `{"query": "V7 مشروب", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 19 kept · USD 0.0600

### fbc_one_16
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 17 of 30
- **Input:** `{"query": "مشروب V7", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 19 kept · USD 0.0600

### fbc_one_17
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 18 of 30
- **Input:** `{"query": "V7 رمان", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 15 kept · USD 0.0600

### fbc_one_18
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 19 of 30
- **Input:** `{"query": "V7 بينا كولادا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 19 kept · USD 0.0600

### fbc_one_19
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 20 of 30
- **Input:** `{"query": "V7 بلوبيري", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 0 kept · USD 0.0600

### fbc_one_20
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 21 of 30
- **Input:** `{"query": "V7 شعير", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 20 kept · USD 0.0600

### fbc_one_21
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 22 of 30
- **Input:** `{"query": "V7 بينك ليمونيد", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 7 kept · USD 0.0600

### fbc_one_22
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 23 of 30
- **Input:** `{"query": "V7 pink lemonade", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 8 kept · USD 0.0600

### fbc_one_23
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 24 of 30
- **Input:** `{"query": "V7 Egypt", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 3 kept · USD 0.0600

### fbc_one_24
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 25 of 30
- **Input:** `{"query": "V7 soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 18 kept · USD 0.0600

### fbc_one_25
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 26 of 30
- **Input:** `{"query": "V7 drink", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 16 kept · USD 0.0600

### fbc_one_26
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 27 of 30
- **Input:** `{"query": "V Cola", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 16 in window · 8 kept · USD 0.0600

### fbc_one_27
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 28 of 30
- **Input:** `{"query": "V Orange", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 0 kept · USD 0.0600

### fbc_one_28
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 29 of 30
- **Input:** `{"query": "V Super Soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 11 in window · 11 kept · USD 0.0600

### fbc_one_29
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-19
- **Why:** Facebook public posts: keyword 30 of 30
- **Input:** `{"query": "V7 كانز", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.0600

### fbc_apify_00
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 1 of 30
- **Input:** `{"categories": ["ڤي سڤن"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 2 in window · 2 kept · USD 0.0510

### fbc_apify_01
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 2 of 30
- **Input:** `{"categories": ["ڤيسڤن"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 5 in window · 0 kept · USD 0.0510

### fbc_apify_02
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 3 of 30
- **Input:** `{"categories": ["مشروب ڤي سڤن"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 5 in window · 1 kept · USD 0.0510

### fbc_apify_03
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 4 of 30
- **Input:** `{"categories": ["ڤي سڤن كريم صودا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 4 kept · USD 0.0510

### fbc_apify_04
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 5 of 30
- **Input:** `{"categories": ["ڤي سڤن رمان"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbc_apify_05
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 6 of 30
- **Input:** `{"categories": ["ڤي سڤن بينا كولادا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 1 kept · USD 0.0510

### fbc_apify_06
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 7 of 30
- **Input:** `{"categories": ["ڤي سڤن شعير"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 2 in window · 2 kept · USD 0.0510

### fbc_apify_07
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 8 of 30
- **Input:** `{"categories": ["ڤي سڤن ليمون نعناع"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 0 kept · USD 0.0510

### fbc_apify_08
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 9 of 30
- **Input:** `{"categories": ["ڤي كولا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 5 in window · 4 kept · USD 0.0510

### fbc_apify_09
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 10 of 30
- **Input:** `{"categories": ["ڤي كولا دايت"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 3 kept · USD 0.0510

### fbc_apify_10
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 11 of 30
- **Input:** `{"categories": ["ڤي اورانج"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 0 kept · USD 0.0510

### fbc_apify_11
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 12 of 30
- **Input:** `{"categories": ["ڤي ليمون"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 4 in window · 2 kept · USD 0.0510

### fbc_apify_12
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 13 of 30
- **Input:** `{"categories": ["ڤي سوبر صودا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 2 in window · 2 kept · USD 0.0510

### fbc_apify_13
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 14 of 30
- **Input:** `{"categories": ["V7 كريم صودا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0510

### fbc_apify_14
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 15 of 30
- **Input:** `{"categories": ["V7 cream soda"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 10 in window · 10 kept · USD 0.0510

### fbc_apify_15
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 16 of 30
- **Input:** `{"categories": ["V7 مشروب"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 1 in window · 1 kept · USD 0.0510

### fbc_apify_16
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 17 of 30
- **Input:** `{"categories": ["مشروب V7"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 2 kept · USD 0.0510

### fbc_apify_17
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 18 of 30
- **Input:** `{"categories": ["V7 رمان"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 3 kept · USD 0.0510

### fbc_apify_18
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 19 of 30
- **Input:** `{"categories": ["V7 بينا كولادا"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 7 in window · 7 kept · USD 0.0510

### fbc_apify_19
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 20 of 30
- **Input:** `{"categories": ["V7 بلوبيري"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 3 kept · USD 0.0510

### fbc_apify_20
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 21 of 30
- **Input:** `{"categories": ["V7 شعير"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 0 kept · USD 0.0510

### fbc_apify_21
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 22 of 30
- **Input:** `{"categories": ["V7 بينك ليمونيد"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 3 kept · USD 0.0510

### fbc_apify_22
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 23 of 30
- **Input:** `{"categories": ["V7 pink lemonade"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 3 in window · 3 kept · USD 0.0510

### fbc_apify_23
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 24 of 30
- **Input:** `{"categories": ["V7 Egypt"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 2 in window · 0 kept · USD 0.0510

### fbc_apify_24
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 25 of 30
- **Input:** `{"categories": ["V7 soda"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 6 kept · USD 0.0510

### fbc_apify_25
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 26 of 30
- **Input:** `{"categories": ["V7 drink"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 2 kept · USD 0.0510

### fbc_apify_26
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 27 of 30
- **Input:** `{"categories": ["V Cola"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 8 in window · 3 kept · USD 0.0510

### fbc_apify_27
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 28 of 30
- **Input:** `{"categories": ["V Orange"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 2 kept · USD 0.0510

### fbc_apify_28
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 29 of 30
- **Input:** `{"categories": ["V Super Soda"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 6 in window · 6 kept · USD 0.0510

### fbc_apify_29
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook public posts: keyword 30 of 30
- **Input:** `{"categories": ["V7 كانز"], "searchType": "posts", "resultsLimit": 10}`
- **Output:** 10 returned · 1 in window · 1 kept · USD 0.0510

### fbc_reels_00
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 1 of 12
- **Input:** `{"categories": ["ڤي سڤن"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_01
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 2 of 12
- **Input:** `{"categories": ["مشروب ڤي سڤن"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_02
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 3 of 12
- **Input:** `{"categories": ["ڤي كولا"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_03
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 4 of 12
- **Input:** `{"categories": ["ڤي اورانج"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_04
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 5 of 12
- **Input:** `{"categories": ["V7 كريم صودا"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_05
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 6 of 12
- **Input:** `{"categories": ["V7 cream soda"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_06
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 7 of 12
- **Input:** `{"categories": ["V7 مشروب"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbc_reels_07
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 8 of 12
- **Input:** `{"categories": ["V7 رمان"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_08
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 9 of 12
- **Input:** `{"categories": ["V7 Egypt"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_09
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 10 of 12
- **Input:** `{"categories": ["V7 drink"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0510

### fbc_reels_10
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 11 of 12
- **Input:** `{"categories": ["V Cola"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_reels_11
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reel search: keyword 12 of 12
- **Input:** `{"categories": ["V Super Soda"], "searchType": "reels", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0760

### fbc_vapify_00
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 1 of 12
- **Input:** `{"searchTerm": "ڤي سڤن", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_01
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 2 of 12
- **Input:** `{"searchTerm": "مشروب ڤي سڤن", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_02
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 3 of 12
- **Input:** `{"searchTerm": "ڤي كولا", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_03
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 4 of 12
- **Input:** `{"searchTerm": "ڤي اورانج", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_04
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 5 of 12
- **Input:** `{"searchTerm": "V7 كريم صودا", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_05
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 6 of 12
- **Input:** `{"searchTerm": "V7 cream soda", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_06
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 7 of 12
- **Input:** `{"searchTerm": "V7 مشروب", "resultsLimit": 15}`
- **Output:** 10 returned · 0 in window · 0 kept · USD 0.0500

### fbc_vapify_07
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 8 of 12
- **Input:** `{"searchTerm": "V7 رمان", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_08
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 9 of 12
- **Input:** `{"searchTerm": "V7 Egypt", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_09
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 10 of 12
- **Input:** `{"searchTerm": "V7 drink", "resultsLimit": 15}`
- **Output:** 14 returned · 0 in window · 0 kept · USD 0.0700

### fbc_vapify_10
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 11 of 12
- **Input:** `{"searchTerm": "V Cola", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vapify_11
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: keyword 12 of 12
- **Input:** `{"searchTerm": "V Super Soda", "resultsLimit": 15}`
- **Output:** 15 returned · 0 in window · 0 kept · USD 0.0750

### fbc_vheadply
- **Scraper:** [headply/facebook-video-search-scraper](https://apify.com/headply/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: 12 keywords
- **Input:** `{"searchQueries": ["ڤي سڤن", "مشروب ڤي سڤن", "ڤي كولا", "ڤي اورانج", "V7 كريم صودا", "V7 cream soda", "V7 مشروب", "V7 رمان", "V7 Egypt", "V7 drink", "V Cola", "V Super Soda"], "maxItemsPerTarget": 20, "mode": "videoSearch"}`
- **Output:** 120 returned · 35 in window · 9 kept · USD 0.2770

### fbc_vaxesso
- **Scraper:** [axesso_data/facebook-video-search-scraper](https://apify.com/axesso_data/facebook-video-search-scraper), 2026-10-19
- **Why:** Facebook video search: 12 keywords
- **Input:** `{"input": [{"keyword": "ڤي سڤن", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "مشروب ڤي سڤن", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "ڤي كولا", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "ڤي اورانج", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 كريم صودا", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 cream soda", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 مشروب", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 رمان", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 Egypt", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 drink", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V Cola", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V Super Soda", "sort": "RELEVANCE", "maxPosts": 20}]}`
- **Output:** 217 returned · 0 in window · 0 kept · USD 0.0543

### fbc_groups
- **Scraper:** [lofomachines/facebook-groups-posts-search-scraper](https://apify.com/lofomachines/facebook-groups-posts-search-scraper), 2026-10-19
- **Why:** Facebook public groups: 12 keywords (stopped after 62 posts)
- **Input:** `{"keywords": ["ڤي سڤن", "ڤي كولا", "V7 كريم صودا", "مشروب V7", "V7 drink", "V Cola", "ڤي اورانج", "V7 رمان", "V7 شعير", "V Super Soda", "ڤي سڤن سعر", "ڤي سڤن جملة"], "afterDate": "this_year", "maxPosts": 25, "countryCode": "eg"}`
- **Output:** 62 returned · 35 in window · 13 kept · USD 0.2774

### fbc_google_months
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-19
- **Why:** Google of facebook.com, 12 exact phrases, one month at a time (stopped at its cap after 114 of 168 pages)
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 2, "countryCode": "eg"}`
- **Output:** 121 returned · 0 in window · 0 kept · USD 0.2851

### fbd_posts
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the new reels, videos and Google finds, by link
- **Input:** `{"direct_urls": "[610 links]"}`
- **Output:** 602 returned · 450 in window · 117 kept · USD 1.4027

### fbcm_door_202610191228
- **Scraper:** [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper), 2026-10-19
- **Why:** comments under the public Facebook posts about V7, up to 100 a post
- **Input:** `{"postUrls": "[283 links]", "targetComments": 100, "includeReplies": false, "orderingMode": "MOST_RELEVANT"}`
- **Output:** 3,665 returned · 3,535 in window · 2,833 kept · USD 1.8327

### fbcm_official_202610191241
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-19
- **Why:** comments under the posts thedoor returned nothing for
- **Input:** `{"startUrls": "[12 links]", "resultsLimit": 100, "includeNestedComments": false}`
- **Output:** 50 returned · 44 in window · 43 kept · USD 0.1010

### fbf_pages_202610191228
- **Scraper:** [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper), 2026-10-19
- **Why:** followers and category of the pages, creators, businesses and news outlets that posted about V7
- **Input:** `{"startUrls": "[245 links]"}`
- **Output:** 245 returned · 0 in window · 0 kept · USD 2.0090

### fbf_plays_202610191228
- **Scraper:** [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper), 2026-10-19
- **Why:** plays of the Facebook reels and videos about V7 without a view count
- **Input:** `{"startUrls": "[143 links]"}`
- **Output:** 143 returned · 0 in window · 0 kept · USD 0.5722

### fbf_speech_202610191228
- **Scraper:** [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber), 2026-10-19
- **Why:** what is said in the Facebook reels and videos about V7, and in those whose text is too short to tell
- **Input:** `{"video_urls": "[237 links]"}`
- **Output:** 202 returned · 0 in window · 0 kept · USD 7.8400

### fbd_posts_views
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the video posts about V7 behind a post link, by link, for their plays
- **Input:** `{"direct_urls": "[25 links]"}`
- **Output:** 25 returned · 25 in window · 25 kept · USD 0.0583

### fbd_posts_names
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the posts whose search row came without the account name, by link
- **Input:** `{"direct_urls": "[5 links]"}`
- **Output:** 5 returned · 3 in window · 3 kept · USD 0.0117

### fbrt_apifyreels_1
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"categories": ["V7 كريم صودا"], "searchType": "reels", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1010

### fbrt_apifyreels_2
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"categories": ["V7 cream soda"], "searchType": "reels", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1010

### fbrt_apifyreels_3
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"categories": ["ڤي كولا"], "searchType": "reels", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1010

### fbrt_apifyreels_4
- **Scraper:** [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"categories": ["ڤي سڤن"], "searchType": "reels", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1010

### fbrt_alien_1
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"search_type": "posts", "keyword": "V7 كريم صودا", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2234

### fbrt_alien_2
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"search_type": "posts", "keyword": "V7 cream soda", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2220

### fbrt_alien_3
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"search_type": "posts", "keyword": "ڤي كولا", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2229

### fbrt_alien_4
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"search_type": "posts", "keyword": "ڤي سڤن", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0094

### fbrt_apifyvideo_1
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"searchTerm": "V7 كريم صودا", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1000

### fbrt_apifyvideo_2
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"searchTerm": "V7 cream soda", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1000

### fbrt_apifyvideo_3
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"searchTerm": "ڤي كولا", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1000

### fbrt_apifyvideo_4
- **Scraper:** [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"searchTerm": "ڤي سڤن", "resultsLimit": 20}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.1000

### fbrt_igview_1
- **Scraper:** [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"query": "V7 كريم صودا", "maxPages": 2}`
- **Output:** 14 returned · 0 in window · 0 kept · USD 0.0509

### fbrt_igview_2
- **Scraper:** [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"query": "V7 cream soda", "maxPages": 2}`
- **Output:** 14 returned · 0 in window · 0 kept · USD 0.0475

### fbrt_igview_3
- **Scraper:** [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"query": "ڤي كولا", "maxPages": 2}`
- **Output:** 14 returned · 0 in window · 0 kept · USD 0.0470

### fbrt_igview_4
- **Scraper:** [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"query": "ڤي سڤن", "maxPages": 2}`
- **Output:** 14 returned · 0 in window · 0 kept · USD 0.0471

### fbrt_lexis_1
- **Scraper:** [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"query": "V7 كريم صودا", "maxItems": 20}`
- **Output:** 7 returned · 0 in window · 0 kept · USD 0.1334

### fbrt_lexis_2
- **Scraper:** [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"query": "V7 cream soda", "maxItems": 20}`
- **Output:** 11 returned · 0 in window · 0 kept · USD 0.1815

### fbrt_lexis_3
- **Scraper:** [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"query": "ڤي كولا", "maxItems": 20}`
- **Output:** 6 returned · 0 in window · 0 kept · USD 0.1590

### fbrt_lexis_4
- **Scraper:** [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"query": "ڤي سڤن", "maxItems": 20}`
- **Output:** 7 returned · 0 in window · 0 kept · USD 0.1603

### fbrt_easyapi_1
- **Scraper:** [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 1 of 4
- **Input:** `{"query": "V7 كريم صودا", "maxItems": 20}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.1833

### fbrt_easyapi_2
- **Scraper:** [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 2 of 4
- **Input:** `{"query": "V7 cream soda", "maxItems": 20}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.1809

### fbrt_easyapi_3
- **Scraper:** [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 3 of 4
- **Input:** `{"query": "ڤي كولا", "maxItems": 20}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.1820

### fbrt_easyapi_4
- **Scraper:** [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: keyword 4 of 4
- **Input:** `{"query": "ڤي سڤن", "maxItems": 20}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.1838

### fbrt_headply
- **Scraper:** [headply/facebook-video-search-scraper](https://apify.com/headply/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"searchQueries": ["V7 كريم صودا", "V7 cream soda", "ڤي كولا", "ڤي سڤن"], "maxItemsPerTarget": 20, "mode": "videoSearch"}`
- **Output:** 39 returned · 0 in window · 0 kept · USD 0.0907

### fbrt_axesso
- **Scraper:** [axesso_data/facebook-video-search-scraper](https://apify.com/axesso_data/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"input": [{"keyword": "V7 كريم صودا", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "V7 cream soda", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "ڤي كولا", "sort": "RELEVANCE", "maxPosts": 20}, {"keyword": "ڤي سڤن", "sort": "RELEVANCE", "maxPosts": 20}]}`
- **Output:** 80 returned · 0 in window · 0 kept · USD 0.0201

### fbrt_sasky
- **Scraper:** [sasky/facebook-keyword-videos-urls-scraper](https://apify.com/sasky/facebook-keyword-videos-urls-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"keywords": ["V7 كريم صودا", "V7 cream soda", "ڤي كولا", "ڤي سڤن"], "date": "last-6-months", "limit": "80"}`
- **Output:** 11 returned · 0 in window · 0 kept · USD 0.0417

### fbrt_nataniel
- **Scraper:** [natanielsantos/facebook-video-search-scraper](https://apify.com/natanielsantos/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"searchTerms": ["V7 كريم صودا", "V7 cream soda", "ڤي كولا", "ڤي سڤن"], "maxItems": 20}`
- **Output:** 35 returned · 0 in window · 0 kept · USD 0.1331

### fbrt_thenetaji
- **Scraper:** [thenetaji/facebook-video-search-scraper](https://apify.com/thenetaji/facebook-video-search-scraper), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"searchQuery": ["V7 كريم صودا", "V7 cream soda", "ڤي كولا", "ڤي سڤن"], "maxItems": 20}`
- **Output:** 80 returned · 0 in window · 0 kept · USD 0.2240

### fbrt_autolab
- **Scraper:** [automation-lab/facebook-public-video-search-results](https://apify.com/automation-lab/facebook-public-video-search-results), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords
- **Input:** `{"searchQueries": ["V7 كريم صودا", "V7 cream soda", "ڤي كولا", "ڤي سڤن"], "maxItems": 80, "maxScrolls": 8}`
- **Output:** 28 returned · 0 in window · 0 kept · USD 0.1170

### fbrt_google
- **Scraper:** [simple.actor/google-short-videos](https://apify.com/simple.actor/google-short-videos), 2026-10-19
- **Why:** 19 Oct reel comparison: the 4 keywords, Facebook only
- **Input:** `{"queries": ["\"V7 كريم صودا\"", "\"V7 cream soda\"", "\"ڤي كولا\"", "\"ڤي سڤن\""], "maxItems": 24, "platform": "facebook", "timeRange": "year", "country": "EG", "language": "ar"}`
- **Output:** 81 returned · 0 in window · 0 kept · USD 0.0888

### fbd_posts_reeltest
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the reels the comparison found that the collection lacked, by link
- **Input:** `{"direct_urls": "[208 links]"}`
- **Output:** 204 returned · 69 in window · 12 kept · USD 0.4754

### fbr_google
- **Scraper:** [simple.actor/google-short-videos](https://apify.com/simple.actor/google-short-videos), 2026-10-19
- **Why:** Facebook reels: Google's short videos for the 30 keywords
- **Input:** `{"queries": "[30 items]", "maxItems": 24, "platform": "facebook", "timeRange": "year", "country": "EG", "language": "ar"}`
- **Output:** 353 returned · 0 in window · 0 kept · USD 0.4625

### fbr_alien_00
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 1 of 15
- **Input:** `{"search_type": "posts", "keyword": "ڤي سڤن", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2261

### fbr_alien_01
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 2 of 15
- **Input:** `{"search_type": "posts", "keyword": "مشروب ڤي سڤن", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0036

### fbr_alien_02
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 3 of 15
- **Input:** `{"search_type": "posts", "keyword": "ڤي كولا", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2227

### fbr_alien_03
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 4 of 15
- **Input:** `{"search_type": "posts", "keyword": "ڤي اورانج", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2314

### fbr_alien_04
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 5 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 كريم صودا", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2236

### fbr_alien_05
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 6 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 cream soda", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2244

### fbr_alien_06
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 7 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 مشروب", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 0 in window · 0 kept · USD 0.2102

### fbr_alien_07
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 8 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 رمان", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2259

### fbr_alien_08
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 9 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 Egypt", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16", "cookies": [], "filter_by_recent_posts": false, "fetch_reaction_map": false, "since": "all_times", "min_wait_time_in_sec": 1, "max_wait_time_in_sec": 4, "proxyConfiguration": {"useApifyProxy": true}}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2306

### fbr_alien_09
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 10 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 drink", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 6 returned · 0 in window · 0 kept · USD 0.0734

### fbr_alien_10
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 11 of 15
- **Input:** `{"search_type": "posts", "keyword": "V Cola", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2279

### fbr_alien_11
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 12 of 15
- **Input:** `{"search_type": "posts", "keyword": "V Super Soda", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2288

### fbr_alien_12
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 13 of 15
- **Input:** `{"search_type": "posts", "keyword": "ڤي سڤن كريم صودا", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2256

### fbr_alien_13
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 14 of 15
- **Input:** `{"search_type": "posts", "keyword": "V7 بينك ليمونيد", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2240

### fbr_alien_14
- **Scraper:** [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper), 2026-10-19
- **Why:** Facebook reels: reels-only search, keyword 15 of 15
- **Input:** `{"search_type": "posts", "keyword": "V Orange", "only_reels": true, "follow_post_scraping": true, "results_limit": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.2294

### fbd_posts_reels2
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the new reels from that search, by link
- **Input:** `{"direct_urls": "[292 links]"}`
- **Output:** 287 returned · 242 in window · 25 kept · USD 0.6688

### fbf_plays_202610191508
- **Scraper:** [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper), 2026-10-19
- **Why:** plays of the new Facebook videos about V7
- **Input:** `{"startUrls": "[43 links]"}`
- **Output:** 43 returned · 0 in window · 0 kept · USD 0.1722

### fbf_speech_202610191508
- **Scraper:** [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber), 2026-10-19
- **Why:** what is said in the new Facebook videos
- **Input:** `{"video_urls": "[86 links]"}`
- **Output:** 51 returned · 0 in window · 0 kept · USD 1.7850

### fbf_pages_202610191508
- **Scraper:** [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper), 2026-10-19
- **Why:** followers of the new pages
- **Input:** `{"startUrls": "[66 links]"}`
- **Output:** 66 returned · 0 in window · 0 kept · USD 0.5412

### fbcm_door_202610191508
- **Scraper:** [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper), 2026-10-19
- **Why:** comments under the new Facebook posts about V7
- **Input:** `{"postUrls": "[43 links]", "targetComments": 100, "includeReplies": false, "orderingMode": "MOST_RELEVANT"}`
- **Output:** 348 returned · 346 in window · 254 kept · USD 0.1741

### fbcm_official_202610191510
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-19
- **Why:** comments under the new posts thedoor returned nothing for
- **Input:** `{"startUrls": "[1 link]", "resultsLimit": 100, "includeNestedComments": false}`
- **Output:** 4 returned · 4 in window · 3 kept · USD 0.0090

### fbd_posts_views_202610191511
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** the new video posts behind a post link, for their plays
- **Input:** `{"direct_urls": "[16 links]"}`
- **Output:** 16 returned · 16 in window · 16 kept · USD 0.0373

### fbm_forge_00
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 1 of 30
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 13 returned · 13 in window · 8 kept · USD 0.0337

### fbm_forge_01
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 2 of 30
- **Input:** `{"query": "ڤيسڤن", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 0 kept · USD 0.0467

### fbm_forge_02
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 3 of 30
- **Input:** `{"query": "مشروب ڤي سڤن", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 17 returned · 17 in window · 1 kept · USD 0.0441

### fbm_forge_03
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 4 of 30
- **Input:** `{"query": "ڤي سڤن كريم صودا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 4 kept · USD 0.0519

### fbm_forge_04
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 5 of 30
- **Input:** `{"query": "ڤي سڤن رمان", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 5 returned · 5 in window · 0 kept · USD 0.0130

### fbm_forge_05
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 6 of 30
- **Input:** `{"query": "ڤي سڤن بينا كولادا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 1 kept · USD 0.0519

### fbm_forge_06
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 7 of 30
- **Input:** `{"query": "ڤي سڤن شعير", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 15 returned · 15 in window · 2 kept · USD 0.0389

### fbm_forge_07
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 8 of 30
- **Input:** `{"query": "ڤي سڤن ليمون نعناع", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.0519

### fbm_forge_08
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 9 of 30
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 19 kept · USD 0.0519

### fbm_forge_09
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 10 of 30
- **Input:** `{"query": "ڤي كولا دايت", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 10 kept · USD 0.0519

### fbm_forge_10
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 11 of 30
- **Input:** `{"query": "ڤي اورانج", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 19 in window · 0 kept · USD 0.0493

### fbm_forge_11
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 12 of 30
- **Input:** `{"query": "ڤي ليمون", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 17 in window · 3 kept · USD 0.0493

### fbm_forge_12
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 13 of 30
- **Input:** `{"query": "ڤي سوبر صودا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 19 in window · 9 kept · USD 0.0493

### fbm_forge_13
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 14 of 30
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 19 in window · 15 kept · USD 0.0493

### fbm_forge_14
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 15 of 30
- **Input:** `{"query": "V7 cream soda", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 6 kept · USD 0.0467

### fbm_forge_15
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 16 of 30
- **Input:** `{"query": "V7 مشروب", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 16 returned · 16 in window · 8 kept · USD 0.0415

### fbm_forge_16
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 17 of 30
- **Input:** `{"query": "مشروب V7", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 9 kept · USD 0.0467

### fbm_forge_17
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 18 of 30
- **Input:** `{"query": "V7 رمان", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 12 kept · USD 0.0467

### fbm_forge_18
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 19 of 30
- **Input:** `{"query": "V7 بينا كولادا", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 14 kept · USD 0.0519

### fbm_forge_19
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 20 of 30
- **Input:** `{"query": "V7 بلوبيري", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 4 kept · USD 0.0519

### fbm_forge_20
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 21 of 30
- **Input:** `{"query": "V7 شعير", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 12 returned · 12 in window · 1 kept · USD 0.0311

### fbm_forge_21
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 22 of 30
- **Input:** `{"query": "V7 بينك ليمونيد", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 3 kept · USD 0.0519

### fbm_forge_22
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 23 of 30
- **Input:** `{"query": "V7 pink lemonade", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 19 returned · 18 in window · 8 kept · USD 0.0493

### fbm_forge_23
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 24 of 30
- **Input:** `{"query": "V7 Egypt", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 1 kept · USD 0.0467

### fbm_forge_24
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 25 of 30
- **Input:** `{"query": "V7 soda", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 16 kept · USD 0.0519

### fbm_forge_25
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 26 of 30
- **Input:** `{"query": "V7 drink", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 3 kept · USD 0.0519

### fbm_forge_26
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 27 of 30
- **Input:** `{"query": "V Cola", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 4 kept · USD 0.0519

### fbm_forge_27
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 28 of 30
- **Input:** `{"query": "V Orange", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 13 returned · 13 in window · 1 kept · USD 0.0337

### fbm_forge_28
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 29 of 30
- **Input:** `{"query": "V Super Soda", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 20 returned · 16 in window · 16 kept · USD 0.0519

### fbm_forge_29
- **Scraper:** [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts), 2026-10-19
- **Why:** Facebook public posts, a fourth search: keyword 30 of 30
- **Input:** `{"query": "V7 كانز", "search_type": "posts", "max_results": 20, "start_date": "2026-04-20", "end_date": "2026-10-16"}`
- **Output:** 18 returned · 18 in window · 8 kept · USD 0.0467

### fbm_fetchcat_00
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 1 of 30
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 10 kept · USD 0.1200

### fbm_fetchcat_01
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 2 of 30
- **Input:** `{"query": "ڤيسڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.1200

### fbm_fetchcat_02
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 3 of 30
- **Input:** `{"query": "مشروب ڤي سڤن", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 15 returned · 15 in window · 2 kept · USD 0.0900

### fbm_fetchcat_03
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 4 of 30
- **Input:** `{"query": "ڤي سڤن كريم صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 7 kept · USD 0.1200

### fbm_fetchcat_04
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 5 of 30
- **Input:** `{"query": "ڤي سڤن رمان", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 1 returned · 1 in window · 1 kept · USD 0.0060

### fbm_fetchcat_05
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 6 of 30
- **Input:** `{"query": "ڤي سڤن بينا كولادا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 5 kept · USD 0.1200

### fbm_fetchcat_06
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 7 of 30
- **Input:** `{"query": "ڤي سڤن شعير", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 15 returned · 15 in window · 2 kept · USD 0.0900

### fbm_fetchcat_07
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 8 of 30
- **Input:** `{"query": "ڤي سڤن ليمون نعناع", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.1200

### fbm_fetchcat_08
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 9 of 30
- **Input:** `{"query": "ڤي كولا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 19 kept · USD 0.1200

### fbm_fetchcat_09
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 10 of 30
- **Input:** `{"query": "ڤي كولا دايت", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 12 kept · USD 0.1200

### fbm_fetchcat_10
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 11 of 30
- **Input:** `{"query": "ڤي اورانج", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 0 kept · USD 0.1200

### fbm_fetchcat_11
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 12 of 30
- **Input:** `{"query": "ڤي ليمون", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 18 in window · 2 kept · USD 0.1200

### fbm_fetchcat_12
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 13 of 30
- **Input:** `{"query": "ڤي سوبر صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 8 kept · USD 0.1200

### fbm_fetchcat_13
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 14 of 30
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 18 kept · USD 0.1200

### fbm_fetchcat_14
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 15 of 30
- **Input:** `{"query": "V7 cream soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 20 kept · USD 0.1200

### fbm_fetchcat_15
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 16 of 30
- **Input:** `{"query": "V7 مشروب", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 17 returned · 17 in window · 7 kept · USD 0.1020

### fbm_fetchcat_16
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 17 of 30
- **Input:** `{"query": "مشروب V7", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 8 kept · USD 0.1200

### fbm_fetchcat_17
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 18 of 30
- **Input:** `{"query": "V7 رمان", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.1200

### fbm_fetchcat_18
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 19 of 30
- **Input:** `{"query": "V7 بينا كولادا", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 18 kept · USD 0.1200

### fbm_fetchcat_19
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 20 of 30
- **Input:** `{"query": "V7 بلوبيري", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 4 kept · USD 0.1200

### fbm_fetchcat_20
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 21 of 30
- **Input:** `{"query": "V7 شعير", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 1 kept · USD 0.1200

### fbm_fetchcat_21
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 22 of 30
- **Input:** `{"query": "V7 بينك ليمونيد", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 5 kept · USD 0.1200

### fbm_fetchcat_22
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 23 of 30
- **Input:** `{"query": "V7 pink lemonade", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 17 kept · USD 0.1200

### fbm_fetchcat_23
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 24 of 30
- **Input:** `{"query": "V7 Egypt", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 2 kept · USD 0.1200

### fbm_fetchcat_24
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 25 of 30
- **Input:** `{"query": "V7 soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 20 kept · USD 0.1200

### fbm_fetchcat_25
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 26 of 30
- **Input:** `{"query": "V7 drink", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 14 returned · 14 in window · 5 kept · USD 0.0840

### fbm_fetchcat_26
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 27 of 30
- **Input:** `{"query": "V Cola", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 11 kept · USD 0.1200

### fbm_fetchcat_27
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 28 of 30
- **Input:** `{"query": "V Orange", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 19 in window · 2 kept · USD 0.1200

### fbm_fetchcat_28
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 29 of 30
- **Input:** `{"query": "V Super Soda", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 17 in window · 17 kept · USD 0.1200

### fbm_fetchcat_29
- **Scraper:** [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper), 2026-10-19
- **Why:** Facebook public posts, a fifth search: keyword 30 of 30
- **Input:** `{"query": "V7 كانز", "resultsCount": 20, "searchType": "top", "startDate": "2026-04-20", "endDate": "2026-10-16"}`
- **Output:** 20 returned · 20 in window · 13 kept · USD 0.1200

### igst_google
- **Scraper:** [simple.actor/google-short-videos](https://apify.com/simple.actor/google-short-videos), 2026-10-19
- **Why:** 19 Oct test: Google's short videos limited to Instagram, 6 exact phrases (36 reels about V7, 4 of them new)
- **Input:** `{"queries": ["\"V7 soda\"", "\"V7 cream soda\"", "\"V7 كريم صودا\"", "\"V Cola\"", "\"ڤي سڤن\"", "\"ڤي كولا\""], "maxItems": 24, "platform": "instagram", "timeRange": "year", "country": "EG", "language": "ar"}`
- **Output:** 89 returned · 0 in window · 0 kept · USD 0.1004

### igst_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** the new Instagram reels from that test, by link
- **Input:** `{"username": "[11 links]"}`
- **Output:** 11 returned · 11 in window · 4 kept · USD 0.0253

### fbf_plays_202610191732
- **Scraper:** [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper), 2026-10-19
- **Why:** pipeline fill run (pipeline.py): plays of the Facebook videos still without a view count
- **Input:** `{"startUrls": "[17 links]"}`
- **Output:** 17 returned · 0 in window · 0 kept · USD 0.0682

### fbcm_door_202610191732
- **Scraper:** [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper), 2026-10-19
- **Why:** pipeline fill run: comments under the Facebook posts that had none collected
- **Input:** `{"postUrls": "[3 links]", "targetComments": 100, "includeReplies": false, "orderingMode": "MOST_RELEVANT"}`
- **Output:** 77 returned · 77 in window · 77 kept · USD 0.0386

### fbf_speech_202610191732
- **Scraper:** [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber), 2026-10-19
- **Why:** pipeline fill run: a second try for the 35 videos the transcriber had returned nothing for (3 read). The budget guard had skipped it, and the old fallback started it with a USD 0.50 cap; fixed the same day
- **Input:** `{"video_urls": "[35 links]"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.1050

### fbf_pages_202610191732
- **Scraper:** [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper), 2026-10-19
- **Why:** pipeline fill run: followers of the pages still without them
- **Input:** `{"startUrls": "[27 links]"}`
- **Output:** 27 returned · 0 in window · 0 kept · USD 0.2214

### fbd_posts_views_202610191733
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-19
- **Why:** pipeline fill run: video posts behind a post link, for their plays
- **Input:** `{"direct_urls": "[17 links]"}`
- **Output:** 17 returned · 17 in window · 17 kept · USD 0.0397

### igspeech_about_202610191734
- **Scraper:** [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper), 2026-10-19
- **Why:** pipeline fill run: speech of the new Instagram reels about V7
- **Input:** `{"bulkUrls": "[5 links]", "resultsLimit": 5}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0225

### ig_profiles_202610191735
- **Scraper:** [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper), 2026-10-19
- **Why:** pipeline fill run: follower counts of the Instagram accounts still without one
- **Input:** `{"usernames": "[30 accounts]"}`
- **Output:** 30 returned · 0 in window · 0 kept · USD 0.0690

### igcm_202610191736
- **Scraper:** [scrapesmith/instagram-comments-scraper](https://apify.com/scrapesmith/instagram-comments-scraper), 2026-10-19
- **Why:** pipeline fill run: comments under the Instagram posts that had none collected
- **Input:** `{"postUrls": "[40 links]", "maxCommentsPerPost": 100, "sortOrder": "popular"}`
- **Output:** 76 returned · 76 in window · 58 kept · USD 0.0381

### vis_posts_202610191737
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-19
- **Why:** pipeline fill run: fresh media links for the Instagram posts whose pictures were not read yet
- **Input:** `{"username": "[7 links]"}`
- **Output:** 7 returned · 0 in window · 0 kept · USD 0.0161

### fbp_one_dst_1015_1
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test, check: one day (15 Oct), 3 results
- **Input:** `{"query": "ڤي كولا", "resultsCount": 3, "searchType": "latest", "startDate": "2026-10-15", "endDate": "2026-10-15"}`
- **Output:** 3 returned · 3 in window · 2 kept · USD 0.0091

### fbp_sf_dst_1015_1
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test, check: one day (15 Oct), 3 results
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_posts": 3, "start_date": "2026-10-15", "end_date": "2026-10-15"}`
- **Output:** 3 returned · 3 in window · 1 kept · USD 0.0066

### fbl_dst_google
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test, check: Google of facebook.com for one day
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 1, "countryCode": "eg"}`
- **Output:** 1 returned · 0 in window · 0 kept · USD 0.0026

### igl_dst_google2
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test, check: Google for one day and one week, Instagram and Facebook
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 1, "countryCode": "eg"}`
- **Output:** 4 returned · 0 in window · 0 kept · USD 0.0100

### igl_ds_day
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Google of instagram.com one day at a time, August, 5 phrases
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 2, "countryCode": "eg"}`
- **Output:** 177 returned · 0 in window · 0 kept · USD 0.4275

### igl_ds_week
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Google of instagram.com one week at a time, August, 5 phrases
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 3, "countryCode": "eg"}`
- **Output:** 45 returned · 0 in window · 0 kept · USD 0.1100

### fbl_ds_day
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Google of facebook.com one day at a time, August, 6 phrases
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 2, "countryCode": "eg"}`
- **Output:** 188 returned · 0 in window · 0 kept · USD 0.4676

### fbl_ds_week
- **Scraper:** [apify/google-search-scraper](https://apify.com/apify/google-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Google of facebook.com one week at a time, August, 6 phrases
- **Input:** `{"queries": "[1 link]", "maxPagesPerQuery": 3, "countryCode": "eg"}`
- **Output:** 52 returned · 0 in window · 0 kept · USD 0.1275

### fbp_one_ds_1015_1
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-10-15", "endDate": "2026-10-15"}`
- **Output:** 10 returned · 9 in window · 2 kept · USD 0.0301

### fbp_sf_ds_1015_1
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_posts": 10, "start_date": "2026-10-15", "end_date": "2026-10-15"}`
- **Output:** 10 returned · 10 in window · 3 kept · USD 0.0221

### fbp_one_ds_1015_2
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-10-15", "endDate": "2026-10-15"}`
- **Output:** 10 returned · 5 in window · 2 kept · USD 0.0301

### fbp_sf_ds_1015_2
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 10, "start_date": "2026-10-15", "end_date": "2026-10-15"}`
- **Output:** 7 returned · 7 in window · 2 kept · USD 0.0155

### fbp_one_ds_1015_3
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 10, "searchType": "latest", "startDate": "2026-10-15", "endDate": "2026-10-15"}`
- **Output:** 10 returned · 10 in window · 0 kept · USD 0.0301

### fbp_sf_ds_1015_3
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/10), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 10, "start_date": "2026-10-15", "end_date": "2026-10-15"}`
- **Output:** 4 returned · 4 in window · 0 kept · USD 0.0089

### fbp_one_ds_0815_1
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-15", "endDate": "2026-08-15"}`
- **Output:** 9 returned · 9 in window · 8 kept · USD 0.0271

### fbp_sf_ds_0815_1
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-15", "end_date": "2026-08-15"}`
- **Output:** 10 returned · 10 in window · 1 kept · USD 0.0221

### fbp_one_ds_0815_2
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-15", "endDate": "2026-08-15"}`
- **Output:** 10 returned · 10 in window · 7 kept · USD 0.0301

### fbp_sf_ds_0815_2
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-15", "end_date": "2026-08-15"}`
- **Output:** 2 returned · 2 in window · 1 kept · USD 0.0044

### fbp_one_ds_0815_3
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-15", "endDate": "2026-08-15"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0001

### fbp_sf_ds_0815_3
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (15/08), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-15", "end_date": "2026-08-15"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0001

### fbp_one_ds_0804_1
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-04", "endDate": "2026-08-04"}`
- **Output:** 5 returned · 0 in window · 0 kept · USD 0.0150

### fbp_sf_ds_0804_1
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 1 of 3
- **Input:** `{"query": "ڤي كولا", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-04", "end_date": "2026-08-04"}`
- **Output:** 5 returned · 5 in window · 1 kept · USD 0.0111

### fbp_one_ds_0804_2
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-04", "endDate": "2026-08-04"}`
- **Output:** 3 returned · 3 in window · 0 kept · USD 0.0091

### fbp_sf_ds_0804_2
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 2 of 3
- **Input:** `{"query": "V7 كريم صودا", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-04", "end_date": "2026-08-04"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0001

### fbp_one_ds_0804_3
- **Scraper:** [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "resultsCount": 10, "searchType": "latest", "startDate": "2026-08-04", "endDate": "2026-08-04"}`
- **Output:** 5 returned · 4 in window · 4 kept · USD 0.0150

### fbp_sf_ds_0804_3
- **Scraper:** [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper), 2026-10-20
- **Why:** 20 Oct date-slice test: Facebook's own search limited to one day (04/08), keyword 3 of 3
- **Input:** `{"query": "ڤي سڤن", "search_type": "posts", "max_posts": 10, "start_date": "2026-08-04", "end_date": "2026-08-04"}`
- **Output:** 0 returned · 0 in window · 0 kept · USD 0.0001

### igp_post_ds_links
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-20
- **Why:** the new Instagram posts the date slices found, by link
- **Input:** `{"username": "[355 links]"}`
- **Output:** 355 returned · 350 in window · 14 kept · USD 0.8165

### fbp_sf_ds_links
- **Scraper:** [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), 2026-10-20
- **Why:** the new Facebook links the date slices found, by link
- **Input:** `{"direct_urls": "[278 links]"}`
- **Output:** 267 returned · 256 in window · 9 kept · USD 0.6222

## Without Apify

- `yt_pages.py`: V7 Egypt’s YouTube watch pages, read directly for exact dates and counts (free). Its “comments turned off” reading was wrong: the words are in every page’s text. The 18 Oct check with calm_builder found comments on for 27 of the 28 videos.
- Claude (`label.py`, through Claude Code on the user’s plan) read and labelled every public post and comment.
- `vis_media.py`: the pictures of Instagram photos and albums, and a frame every 2 seconds of silent and music reels, downloaded from the links Apify’s post scraper returned (free). `vis_read.py`: Claude (Claude Code on the user’s plan, reading images only) wrote down the text on them and what they show. On the 19 Oct sample it read as well as afanasenko’s extractor, which costs USD 0.075 a reel.
