# Scrapers used for the real data (17–19 Oct 2026)

Every Apify run of `data/raw/real_17oct/`, written by `scrapers_report.py` from the saved runs. **Returned** is what the scraper gave back; **in window** is what fell between 20 Apr and 16 Oct 2026 after duplicates were merged (an item found by two runs counts for both); **kept** is what the dashboard shows (public posts and comments Claude judged to be about V7, emoji reactions and friend tags under V7’s posts, and every V7 post and reply). Runs that add to posts already collected (follower counts, the speech of reels, posts fetched by link to fill a gap) and the 19 Oct comparison runs keep nothing of their own, so their kept is 0. Cost is Apify’s charge for the run.

## By scraper

| Scraper | Used for | Runs | Returned | Kept | Cost (USD) |
|---|---|---:|---:|---:|---:|
| [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper) | Instagram comments | 3 | 1,982 | 1,778 | 4.56 |
| [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper) | TikTok profiles, hashtags, keyword search, videos by link | 11 | 659 | 124 | 2.57 |
| [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper) | Facebook comments | 2 | 915 | 877 | 2.40 |
| [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search) | Facebook keyword search | 19 | 506 | 138 | 1.52 |
| [apple_yang/instagram-transcripts-scraper](https://apify.com/apple_yang/instagram-transcripts-scraper) | What is said in Instagram reels (speech to text) | 3 | 198 | 0 | 1.02 |
| [clockworks/tiktok-comments-scraper](https://apify.com/clockworks/tiktok-comments-scraper) | TikTok comments | 2 | 887 | 872 | 0.89 |
| [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper) | Instagram posts of a profile, or posts by link | 5 | 382 | 300 | 0.88 |
| [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper) | Instagram keyword search with a date range | 3 | 415 | 69 | 0.83 |
| [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper) | YouTube keyword search | 3 | 203 | 30 | 0.61 |
| [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper) | Instagram posts that tag a profile | 3 | 245 | 178 | 0.56 |
| [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper) | YouTube comments | 3 | 1,093 | 731 | 0.46 |
| [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper) | Instagram accounts (follower counts) | 1 | 175 | 0 | 0.40 |
| [apify/instagram-hashtag-scraper](https://apify.com/apify/instagram-hashtag-scraper) | Instagram hashtags (and Instagram keyword search) | 4 | 153 | 12 | 0.35 |
| [trudax/reddit-scraper-lite](https://apify.com/trudax/reddit-scraper-lite) | Reddit search | 2 | 58 | 2 | 0.26 |
| [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper) | Facebook page posts | 2 | 37 | 34 | 0.19 |
| [apify/google-search-scraper](https://apify.com/apify/google-search-scraper) | Google search | 3 | 84 | 0 | 0.17 |
| [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels) | Instagram search, exact phrases | 3 | 1 | 0 | 0.11 |
| [kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest](https://apify.com/kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest) | X (Twitter) search | 7 | 465 | 76 | 0.10 |
| [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api) | Instagram keyword search (posts) | 4 | 70 | 0 | 0.08 |
| [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels) | Instagram Reels search | 3 | 24 | 0 | 0.06 |
| [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper) | YouTube videos (and comments) | 2 | 29 | 0 | 0.05 |
| [streamers/youtube-channel-scraper](https://apify.com/streamers/youtube-channel-scraper) | YouTube channel videos | 1 | 28 | 28 | 0.03 |
| [apify/instagram-search-scraper](https://apify.com/apify/instagram-search-scraper) | Instagram popular reels for a keyword | 1 | 12 | 0 | 0.03 |
| [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper) | Instagram Reels search | 1 | 26 | 0 | 0.02 |
| [apify/instagram-scraper](https://apify.com/apify/instagram-scraper) | Instagram (here: posts that mention a profile) | 1 | 5 | 0 | 0.01 |
| [memo23/instagram-reels-search-scraper](https://apify.com/memo23/instagram-reels-search-scraper) | Instagram Reels search, exact phrases | 1 | 2 | 0 | 0.00 |

Total for these runs: USD 18.15 (Apify’s meter for the month also counts platform usage).

## Every run

### t_fb_posts
- **Scraper:** [apify/facebook-posts-scraper](https://apify.com/apify/facebook-posts-scraper), 2026-10-16
- **Why:** 17 Oct test: 3 of V7 Egypt’s Facebook posts
- **Input:** `{"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "resultsLimit": 3, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0160

### t_fb_comments
- **Scraper:** [apify/facebook-comments-scraper](https://apify.com/apify/facebook-comments-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on 2 V7 posts
- **Input:** `{"startUrls": [{"url": "https://www.facebook.com/V7Egypt/posts/pfbid02Sqn37RqfHGdQXGMrdMUNfqyzCZ4k91JY3yut9mMo5AHY1qrCj3pZwSrCyfGjN9Ajl"}, {"url": "https://www.facebook.com/reel/1583808776758074/"}], "resultsLimit": 3, "includeNestedComments": true}`
- **Output:** 17 returned · 0 in window · 0 kept · USD 0.0350

### t_ig_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-16
- **Why:** 17 Oct test: 3 of V7 Egypt’s Instagram posts
- **Input:** `{"username": ["v7egypt"], "resultsLimit": 3, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0069

### t_ig_comments
- **Scraper:** [apify/instagram-comment-scraper](https://apify.com/apify/instagram-comment-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on 2 V7 posts
- **Input:** `{"directUrls": ["https://www.instagram.com/p/DdG_sWYEi_T/", "https://www.instagram.com/p/DZ2uClLMq8p/"], "resultsLimit": 3, "includeNestedComments": true}`
- **Output:** 12 returned · 0 in window · 0 kept · USD 0.0276

### t_tt_comments
- **Scraper:** [clockworks/tiktok-comments-scraper](https://apify.com/clockworks/tiktok-comments-scraper), 2026-10-16
- **Why:** 17 Oct test: comments on a V7 TikTok video
- **Input:** `{"postURLs": ["https://www.tiktok.com/@v7.egypt/video/7678406422190624008"], "commentsPerPost": 4, "maxRepliesPerComment": 2}`
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
- **Input:** `{"startUrls": [{"url": "https://www.facebook.com/V7Egypt/"}], "resultsLimit": 80, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 34 returned · 34 in window · 34 kept · USD 0.1710

### ig_posts
- **Scraper:** [apify/instagram-post-scraper](https://apify.com/apify/instagram-post-scraper), 2026-10-16
- **Why:** V7 Egypt’s Instagram posts since 20 Apr
- **Input:** `{"username": ["v7egypt"], "resultsLimit": 120, "onlyPostsNewerThan": "2026-04-20"}`
- **Output:** 51 returned · 51 in window · 51 kept · USD 0.1173

### tt_posts
- **Scraper:** [clockworks/tiktok-scraper](https://apify.com/clockworks/tiktok-scraper), 2026-10-16
- **Why:** V7 Egypt’s TikTok videos since 20 Apr
- **Input:** `{"profiles": ["v7.egypt"], "profileSorting": "latest", "oldestPostDateUnified": "2026-04-20", "resultsPerPage": 60}`
- **Output:** 19 returned · 19 in window · 19 kept · USD 0.0770

### yt_posts
- **Scraper:** [streamers/youtube-channel-scraper](https://apify.com/streamers/youtube-channel-scraper), 2026-10-16
- **Why:** V7 Egypt’s YouTube videos and Shorts
- **Input:** `{"startUrls": [{"url": "https://www.youtube.com/@V7Egypt"}], "maxResults": 40, "maxResultsShorts": 60, "maxResultStreams": 0, "oldestPostDate": "2026-04-20"}`
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
- **Input:** `{"username": ["v7tunisia", "v7uzbekistan", "v7ldnuk", "drinkv7", "thehalaldrinksco"], "resultsLimit": 60, "onlyPostsNewerThan": "2026-04-20"}`
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
- **Output:** 30 returned · 29 in window · 20 kept · USD 0.0900

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
- **Output:** 30 returned · 30 in window · 26 kept · USD 0.0900

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
- **Output:** 137 returned · 46 in window · 12 kept · USD 0.3151

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
- **Input:** `{"username": ["v7egypt"], "resultsLimit": 5}`
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
- **Input:** `{"directUrls": ["https://www.instagram.com/v7egypt/"], "resultsType": "mentions", "resultsLimit": 5}`
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
- **Input:** `{"username": ["v7egypt"], "resultsLimit": 180}`
- **Output:** 180 returned · 176 in window · 136 kept · USD 0.4140

### ig_tagged_vss
- **Scraper:** [apify/instagram-tagged-scraper](https://apify.com/apify/instagram-tagged-scraper), 2026-10-18
- **Why:** public posts: Instagram posts tagging @vsupersoda
- **Input:** `{"username": ["vsupersoda"], "resultsLimit": 60}`
- **Output:** 60 returned · 54 in window · 42 kept · USD 0.1380

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
- **Output:** 108 returned · 105 in window · 55 kept · USD 0.2484

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
- **Output:** 30 returned · 29 in window · 7 kept · USD 0.0900

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
- **Input:** `{"startUrls": [{"url": "https://www.youtube.com/watch?v=i9PVV4QqtXE"}], "sort": "top", "maxItems": 20, "includeReplies": false}`
- **Output:** 20 returned · 0 in window · 0 kept · USD 0.0010

### t3_yt_comments_calm
- **Scraper:** [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper), 2026-10-18
- **Why:** 18 Oct test: the same with calm_builder (returned the video only)
- **Input:** `{"startUrls": [{"url": "https://www.youtube.com/watch?v=i9PVV4QqtXE"}], "maxResults": 1, "maxComments": 20, "commentsSortBy": "top", "maxReplyDepth": 1, "maxRepliesPerComment": 3}`
- **Output:** 1 returned · 0 in window · 0 kept · USD 0.0194

### yt_own_check
- **Scraper:** [calm_builder/youtube-scraper](https://apify.com/calm_builder/youtube-scraper), 2026-10-18
- **Why:** are comments on on V7 Egypt’s 28 videos? (27 yes, 1 off)
- **Input:** `{"startUrls": "[28 links]", "maxResults": 1, "maxComments": 0}`
- **Output:** 28 returned · 0 in window · 0 kept · USD 0.0346

### yt_comments_own
- **Scraper:** [apidojo/youtube-comments-scraper](https://apify.com/apidojo/youtube-comments-scraper), 2026-10-18
- **Why:** comments on V7 Egypt’s YouTube videos
- **Input:** `{"startUrls": [{"url": "https://www.youtube.com/watch?v=kFBGmVsoIl0"}, {"url": "https://www.youtube.com/watch?v=VnwmP0cikgY"}, {"url": "https://www.youtube.com/watch?v=Wf5eeMBgnTM"}, {"url": "https://www.youtube.com/shorts/wVXIkk3rep4"}, {"url": "https://www.youtube.com/shorts/-tPy_PzO7ts"}, {"url": "https://www.youtube.com/shorts/E_T3XQDQyoI"}, {"url": "https://www.youtube.com/shorts/ylarnKrzju4"}], "sort": "top", "maxItems": 115, "includeReplies": true}`
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
- **Input:** `{"bulkUrls": ["https://www.instagram.com/p/DeRGJd2gP0M/", "https://www.instagram.com/reel/Db0cx1pMQ37/", "https://www.instagram.com/p/DbymwFMIxIz/"], "resultsLimit": 3}`
- **Output:** 3 returned · 0 in window · 0 kept · USD 0.0205

### ig_profiles
- **Scraper:** [apify/instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper), 2026-10-18
- **Why:** follower counts of the 175 Instagram accounts that posted about V7 without one
- **Input:** `{"usernames": "[175 items]"}`
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

## Without Apify

- `yt_pages.py`: V7 Egypt’s YouTube watch pages, read directly for exact dates and counts (free). Its “comments turned off” reading was wrong: the words are in every page’s text. The 18 Oct check with calm_builder found comments on for 27 of the 28 videos.
- Claude (`label.py`, through Claude Code on the user’s plan) read and labelled every public post and comment.
