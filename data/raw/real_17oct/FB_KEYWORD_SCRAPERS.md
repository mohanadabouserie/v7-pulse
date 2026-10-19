# Facebook scrapers compared (19 Oct 2026)

The same work as for Instagram (`KEYWORD_SCRAPERS.md`), at the user's request: "do the same with facebook … getting all keyword search
scrapers, comparing them, then getting best or combine multiple then see data gaps and fill it".

## 1. Keyword search: 19 scrapers and routes on the same three keywords

The three Instagram keywords (V7 soda, ڤي سڤن, V7 كريم صودا), up to 10 results each, the 20 Apr to 16 Oct window where the scraper takes
dates (`collect.py fbtest`, scored by `fbtest_report.py`; raw results in `raw/fbkw_*`, `raw/fbvs_*`, kept local). **Useful** = about V7
(its text, hashtags or account name V7, its Arabic name with ڤ or its V Cola line), posted inside the window, not V7's own pages.
Test cost USD 2.72.

| Scraper | Store track record | Useful / posts | V7 soda | ڤي سڤن | V7 كريم صودا | Numbers | Cost per useful post |
|---|---|---|---|---|---|---|---|
| [silentflow/facebook-search-scraper](https://apify.com/silentflow/facebook-search-scraper) | 3,483 users, 67,556 runs in 30 days, 100% | 30 / 30 | 10/10 | 10/10 | 10/10 | reactions, comments, shares; views on few videos | USD 0.0022 |
| [topapi/facebook-search-posts-scraper](https://apify.com/topapi/facebook-search-posts-scraper) | 100 users, 99% | 30 / 30 | 10/10 | 10/10 | 10/10 | + views on videos | USD 0.0024 |
| [scrapeforge/facebook-search-posts](https://apify.com/scrapeforge/facebook-search-posts) | 65,776 users, 957,992 runs, 100%, 3.6 (10 reviews) | 25 / 28 | 8/10 | 8/9 | 9/9 | reactions, comments, shares | USD 0.0029 |
| [scraper_one/facebook-posts-search](https://apify.com/scraper_one/facebook-posts-search) (used since 17 Oct) | 23,363 users, 100%, 4.2 (14) | 21 / 30 | 2/10 | 9/10 | 10/10 | reactions, comments, shares | USD 0.0043 |
| [danek/facebook-search-ppr](https://apify.com/danek/facebook-search-ppr) | 54,170 users, 100%, 4.1 (18) | 24 / 32 | 5/11 | 9/10 | 10/11 | reactions, comments, shares | USD 0.0055 |
| [fetch_cat/facebook-post-search-scraper](https://apify.com/fetch_cat/facebook-post-search-scraper) | 194 users, 96% | 30 / 30 | 10/10 | 10/10 | 10/10 | reactions, comments, shares, page or person | USD 0.0060 |
| [igview-owner/facebook-old-posts-search](https://apify.com/igview-owner/facebook-old-posts-search) | 3,037 users, 100%, 4.8 (3) | 26 / 27 | 8/8 | 8/9 | 10/10 | reactions, comments, shares | USD 0.0077 |
| [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper) (posts) | 18,864 users, 100%, 5.0 (28) | 19 / 30 | 7/10 | 4/10 | 8/10 | + views on all videos; no date filter | USD 0.0081 |
| [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper) | 2,136 users, 98%, 5.0 (3) | 15 / 16 | 6/6 | 4/4 | 5/6 | reactions, comments, shares | USD 0.0140 |
| [headply/facebook-post-search-scraper](https://apify.com/headply/facebook-post-search-scraper) | 2 users | 12 / 30 | | | | no date filter (posts from 2024) | USD 0.0058 |
| [mina_safwat/facebook-search-actor](https://apify.com/mina_safwat/facebook-search-actor) | 3,817 users, 100% | 0 / 30 | | | | no dates in its rows | - |
| [powerai/facebook-post-search-scraper](https://apify.com/powerai/facebook-post-search-scraper) | 7,950 users, 92% | 0 / 0 | | | | aborted three times | - |
| Video search: [headply](https://apify.com/headply/facebook-video-search-scraper) | 13 users, 86% | 7 / 22 | | | | reactions, comments, shares, length, video file | USD 0.0074 |
| Video search: [apify](https://apify.com/apify/facebook-video-search-scraper) | 1,468 users, 100%, 4.6 (9) | 6 / 24 | 2/5 | 0/10 | 4/9 | views; some rows broken | USD 0.0250 |
| Video search: [powerai](https://apify.com/powerai/facebook-video-search-scraper) | 413 users, 84% | 8 / 30 | 6/10 | 1/10 | 1/10 | views | USD 0.0862 |
| Video search: [axesso](https://apify.com/axesso_data/facebook-video-search-scraper) | 5 users | 3 / 30 | 3/10 | 0/10 | 0/10 | views, day without year | USD 0.0025 |
| Reel search: [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper) (reels) | as above | 14 about V7, no dates | | | | caption and length only | - |
| Hashtags: [apify/facebook-hashtag-scraper](https://apify.com/apify/facebook-hashtag-scraper) | 5,052 users, 98% | 0 | | | | "Empty or private data" for all 4 tags | - |
| Public groups: [lofomachines](https://apify.com/lofomachines/facebook-groups-posts-search-scraper) (2 other keywords) | 361 users, 80% | 8 / 10 | | | | reactions, comments, shares, group | USD 0.0087 |

- **They mostly return the same posts:** the post searches all use Facebook's own search. Together they found 68 useful posts; no post
  search found more than 30, and most found nothing the others missed. scraper_one ranks differently (6 posts no other found), Apify's
  search found 1 more, the video searches 6 more, and the public-group search 8 posts no post search found.
- **Arabic works on Facebook** (unlike Instagram): ڤي سڤن and V7 كريم صودا returned 9-10 of 10 about V7.
- **Google's site search** (one month at a time, exact phrases) found big pages' posts and videos the searches missed: Seoudi Supermarket,
  Talabat, Oscar Grand Stores, Cairo 360, El Dostor, and buy-and-sell group posts.

## 2. Depth: past 10-15 results Facebook's search is noise

`collect.py fbtest2`: 60 results for ڤي سڤن (USD 0.6). silentflow returned 22 (top) and 33 (most recent), topapi 26 and 30, scrapeforge 32;
each had the same 10 posts about V7 and then unrelated ones (a clothes shop called "Seven", people with ڤ in their names). One month at a
time (June) returned 17-19 posts, 1 about V7. Most recent and top gave the same 10. **So depth and month slices don't help on Facebook;
more keywords, other backends and other surfaces do.**

## 3. Filling the gaps (five creators' V7 reels and three photo posts)

| Gap | Tested | Result | Pick |
|---|---|---|---|
| Views of reels and videos | social_developer play counts; alpha-scraper reel details; danek and Apify's posts scraper by link | play counts for 5 of 5 (exact, e.g. 15,787); alpha gave rounded views in the title; danek "15K"; Apify none | [social_developer/facebook-playcount-scraper](https://apify.com/social_developer/facebook-playcount-scraper), USD 0.004 a video |
| What's said in videos | invideoiq transcriber; Facebook's own captions (codenest, piotrv1001); Whisper small (viralanalyzer); alpha subtitles | invideoiq: 5 of 5, faithful Egyptian Arabic ("بي سيفن كريم صودا بسعر 15 جنيه … ريحة فانيليا وجوز هند"). Captions: 3 of 5. Whisper small: turned the dialect into garbled formal Arabic. alpha: empty | [invideoiq/video-transcriber](https://apify.com/invideoiq/video-transcriber), USD 0.035 a video |
| Text on photos and silent videos | Claude reading the pictures (as for Instagram) | | `vis_media.py --fb`, `vis_read.py` |
| Comments under public posts | thedoor; Apify's own comment scraper | thedoor 25 of Apify's 26 comments, on all 3 posts, a quarter of the price | [thedoor/facebook-comment-scraper](https://apify.com/thedoor/facebook-comment-scraper) USD 0.0005, Apify's for posts it misses |
| Page followers and category | Apify's page scraper | 5 of 5: followers, category (Supermarket, Blogger, Website…), creation date | [apify/facebook-pages-scraper](https://apify.com/apify/facebook-pages-scraper), USD 0.0082 a page |
| Details of reels and Google's links | danek posts by link; alpha reel details; Apify's posts scraper | danek: text, time, counts and plays for reels and posts | [danek/facebook-posts-fast](https://apify.com/danek/facebook-posts-fast), USD 0.0023 |
| Reels and videos marked as photos | the 17 Oct reader | all 20 Facebook videos about V7 were "Image" | fixed in `normalize.py` |

Gap test cost USD 1.10 (meter 34.13).

## 4. What runs (`collect.py fbcover`, `fbdetails`, `fbfill`, `fbfill2`)

- 30 keywords (ڤ spellings, mixed and English; not the ف ones) on silentflow (20 each), scraper_one (20) and Apify's search (10).
- Facebook's reel search and three video searches (12 keywords), public groups (12 keywords), Google one month at a time (12 phrases x 7).
- New reels, videos and Google links fetched by link (danek).
- Then plays, speech, page followers, comments and the pictures read, for the posts about V7.

## 5. Outcome of the full run (19 Oct, Version 30)

- **Facebook public posts about V7: 124 to 520** (Image 181, Reel 152, Text 107, Album 54, Video 26).
- **By route:** scraper_one 290 (196 found by no other route), silentflow 183 (68), the reel, video and Google links fetched by link 117 (all new), Apify's search 70 (4), video search 25 (3), public groups 13 (11).
- **Filled:** plays on 158 of 178 videos; speech on 163 posts; 267 posts read from their pictures; 2,797 comments under the posts; followers for 210 of 302 named pages.
- **Coverage:** Facebook's keyword search can surface about 600 posts about V7 in the window (capture-recapture between scraper_one and silentflow: 290 and 183 found, 88 by both); we have about 390 of those. The reel, video and Google route found 155 posts with almost no overlap (24), so far more reels and page videos exist than any search shows.
- **Cost:** USD 24.88 in all (`SCRAPERS.md`).

## 6. Reels: 13 searches on the same four keywords (19 Oct, after the user asked about overlapping scrapers)

The user: "u didn't use overlapping scrapers like we did with instagram to test it?" Right: the first comparison scored Apify's reel
search without dates. `collect.py fbreeltest` ran every Facebook reel and video search on V7 كريم صودا, V7 cream soda, ڤي كولا and
ڤي سڤن (20 results each); the 208 reels the collection lacked were fetched by link and labelled; `fbreel_report.py` scores them.
**Useful** = a reel about V7, posted 20 Apr to 16 Oct, not by V7's own pages. Test cost USD 4.23.

| Search | Reels returned | Useful | Found by no other | Cost |
|---|---|---|---|---|
| [simple.actor/google-short-videos](https://apify.com/simple.actor/google-short-videos) (Google's short videos, Facebook only) | 63 | 25 | **17** | USD 0.09 |
| [alien_force/facebook-search-scraper](https://apify.com/alien_force/facebook-search-scraper) (reels only) | 60 | 27 | 6 | USD 0.68 |
| [apify/facebook-search-scraper](https://apify.com/apify/facebook-search-scraper) (reels) | 80 | 19 | 0 | USD 0.40 |
| [apify/facebook-video-search-scraper](https://apify.com/apify/facebook-video-search-scraper) | 60 | 16 | 1 | USD 0.40 |
| [igview-owner/facebook-search-scraper](https://apify.com/igview-owner/facebook-search-scraper) | 56 | 14 | 0 | USD 0.19 |
| [axesso_data/facebook-video-search-scraper](https://apify.com/axesso_data/facebook-video-search-scraper) | 80 | 14 | 0 | USD 0.02 |
| [automation-lab/facebook-public-video-search-results](https://apify.com/automation-lab/facebook-public-video-search-results) | 28 | 13 | 0 | USD 0.12 |
| [natanielsantos/facebook-video-search-scraper](https://apify.com/natanielsantos/facebook-video-search-scraper) | 35 | 11 | 0 | USD 0.13 |
| [thenetaji/facebook-video-search-scraper](https://apify.com/thenetaji/facebook-video-search-scraper) | 80 | 11 | 1 | USD 0.22 |
| [lexis-solutions/facebook-videos-watch-scraper](https://apify.com/lexis-solutions/facebook-videos-watch-scraper) | 31 | 7 | 0 | USD 0.63 |
| [headply/facebook-video-search-scraper](https://apify.com/headply/facebook-video-search-scraper) | 39 | 4 | 0 | USD 0.09 |
| [sasky/facebook-keyword-videos-urls-scraper](https://apify.com/sasky/facebook-keyword-videos-urls-scraper) | 11 | 4 | 1 | USD 0.04 |
| [easyapi/facebook-videos-scraper](https://apify.com/easyapi/facebook-videos-scraper) | 0 | 0 | 0 | USD 0.73 |

- **54 useful reels in all; 11 were new** to the Version 30 collection.
- **Facebook's own searches overlap:** alien_force and Apify's reel search share 16 of their 27 and 19.
- **Google doesn't:** its 25 share 8 with the 37 all Facebook searches found together; capture-recapture puts these four keywords at about 110 reels, so the Version 30 run had about half of them.
- **Pick:** Google's short videos (Facebook) for all 30 keywords, plus alien_force's reels-only search for the 15 most reel-heavy keywords (`collect.py fbreels`).

## 7. More scrapers together, to cover more (19 Oct)

The user: "i meant depending on multiple to cover more". On the comparison's three keywords, with Claude's labels: all 11 post scrapers
together found 49 posts about V7; the three used in the full run (scraper_one, silentflow, Apify's search) found 43. Adding scrapeforge
brings it to 47 and fetch_cat to 49, everything the 11 found. So `collect.py fbmore` runs scrapeforge and fetch_cat on all 30 keywords
(20 each), next to the reel search (`fbreels`: Google's short videos and alien_force's reels-only search).

## 8. Outcome (Version 31)

- **Facebook public posts about V7: 520 to 590**; reels 152 to 192.
- **Found only by:** scraper_one 184, Version 30's reel, video and Google links 109, the new reel searches (Google short videos, alien_force) 33, fetch_cat 16, scrapeforge 15, groups 11, silentflow 8, Apify's search 3, video search 3.
- **Coverage:** scraper_one against the silentflow family (silentflow, scrapeforge, fetch_cat): 290 and 242 found, 101 both, so about 690 posts can be surfaced by Facebook's post search; the five found 434. Reels: the reel, video and Google routes found 125, the post searches 88, 21 both, so perhaps 500 reels; we have 192.
- **Cost of this round:** USD 15.87 (comparison 4.23, reel search and fetch 4.14, two post searches 4.76, filling 2.72).
