# Instagram keyword scrapers compared (19 Oct 2026)

The same three keywords for each (V7 soda, ڤي سڤن, V7 كريم صودا; in quotes for the two that take exact phrases), up to 10 results each
(`collect.py kwtest`, scored by `kwtest_report.py`; raw results in `raw/kw_*.json`, kept local). **Useful** = about V7, posted 20 Apr to 16 Oct,
and not by one of V7's own accounts. Test cost USD 0.26.

| Scraper | Store track record | Useful / posts | V7 soda | ڤي سڤن | V7 كريم صودا | Formats | Counts complete | Cost per useful post |
|---|---|---|---|---|---|---|---|---|
| [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api) | 2,811 users, 1.28M runs in 30 days, 100% succeeded, 5.0 from 9 reviews | 13 / 29 | 9/10 | 0/10 | 4/9 | all | yes, except its Arabic results (no captions or likes) | USD 0.0035 |
| [dami_studio/instagram-reels-search-scraper](https://apify.com/dami_studio/instagram-reels-search-scraper) | 725 users, 100%, 5.0 from 1 review (since Jul 2026) | 13 / 25 | 9/10 | 1/7 | 4/8 | reels only | yes | USD 0.0014 |
| [seemuapps/instagram-keyword-posts-scraper](https://apify.com/seemuapps/instagram-keyword-posts-scraper) | 40 users, 100%, no reviews (since 6 Oct 2026) | 13 / 23 | 7/9 | 2/10 | 4/4 | all | yes | USD 0.0045 |
| [data-slayer/instagram-search-reels](https://apify.com/data-slayer/instagram-search-reels) | 3,046 users, 99%, 5.0 from 3 reviews | 12 / 22 | 10/12 | nothing | 4/10 | reels only | yes | USD 0.0048 |
| [memo23/instagram-reels-search-scraper](https://apify.com/memo23/instagram-reels-search-scraper) (exact phrases) | 543 users, 89%, 5.0 from 2 reviews | 2 / 2 | nothing | 1/1 | 1/1 | reels (+ posts) | yes | USD 0.0013 |
| [scraping_solutions/instagram-boolean-search-scraper-posts-reels](https://apify.com/scraping_solutions/instagram-boolean-search-scraper-posts-reels) (exact phrases) | 335 users, 98%, 3.9 from 4 reviews | 1 / 1 | nothing | nothing | 1/1 | posts and reels | yes | USD 0.11 |
| [apify/instagram-search-scraper](https://apify.com/apify/instagram-search-scraper) (popular reels) | 34,646 users, 90%, 4.8 from 32 reviews | 0 / 10 | 10 old (Mar 2026) | nothing | nothing | reels | yes | - |

- The four keyword scrapers find nearly the same posts: they all use Instagram's own search. Arabic is weak for all of them; exact-phrase scrapers are precise but find almost nothing.
- Reels are 59% of the Instagram posts about V7 (photos 62, albums 52 of 280), so reels-only scrapers miss about 4 in 10.
- Pick: apidojo/instagram-scraper-api for English and mixed keywords (track record, all formats, date filter, cost); seemuapps as the fallback.

## Follow-up: did apidojo find what dami_studio found? (19 Oct)
- **Overlap:** no. In the top 10 per keyword apidojo found 8 of dami_studio's 13 useful reels, and dami_studio found 8 of apidojo's 13. The four keyword scrapers together found 26 different useful posts; each alone 12 or 13.
- **Depth:** asking apidojo for 40 results for "V7 soda" (USD 0.03) found 1 of the 4 reels it had missed, at position 36. The other 3 weren't there: dami_studio searches Instagram's Reels search, another surface.
- **Shuffling:** Instagram's search changes between sessions. Two apidojo runs of "V7 soda" shared only 4 useful posts; together they had 13, and with dami_studio 17.
- **Completeness:** apidojo gives captions and likes for about its first 10 results per keyword; past that, mostly bare links (9 of 35 with captions). dami_studio, seemuapps and data-slayer were complete throughout.
- **What follows:** apidojo is set to 10 results per keyword (`collect.py igkw`). No single scraper finds everything; adding dami_studio's Reels search (USD 0.0004 a reel) would catch the reels apidojo misses.

## Does apidojo return everything a post needs? (19 Oct)
- **Yes, within its first 10 results per keyword:** link and exact time (20/20), caption (19/20), account name and handle, verified, likes and comments (19/20), plays for videos (20/20), format, image, location and collaborators when the post has them.
- **Missing:** the account's follower count and the share count.
  - dami_studio adds shares for reels.
  - Followers come from no keyword scraper except seemuapps. Today 187 of the 226 Instagram accounts that posted about V7 have none. Apify's own profile scraper fills them at USD 0.0023 an account (about USD 0.43 for all).
- **Where followers matter:** naming an account in public (10K+, DECISIONS #75), the "Big account" alert (100K+), and the creator size on the People tab. Without them, an account is named only when Claude judges it a creator, page, news outlet or business.
- **dami_studio added** next to apidojo (`collect.py igkw`, DECISIONS #134). Both readers were tested together: 27 posts inside the window, 4 found by both, 5 only by apidojo, 18 only by dami_studio.

## The re-fetch (19 Oct)
- **The step:** `collect.py igkw` picks the apidojo rows without a caption or likes, skipping V7's own accounts and reels dami_studio returned complete. It fetches them again by link with Apify's Instagram post scraper (USD 0.0023 a post; DECISIONS #135).
- **Real test:** the 25 posts it picked from the comparison runs, fetched for real (USD 0.044). All 25 were read: captions 25, likes 24 (the 25th hidden by its owner), comments 25, dates and accounts 25, plays on all 13 videos.
- **What it doesn't close:**
  - Likes the owner hid: Instagram shows them to no one. Today 37 Instagram posts about V7 have no like count, and the dashboard shows them as 0.
  - Follower counts: no keyword or post scraper returns them. Apify's profile scraper fills them (USD 0.0023 an account; 187 accounts, about USD 0.43).
  - Shares: apidojo and the post scraper don't return them; dami_studio does for its reels. Instagram shows shares only on some reels (135 Instagram posts have none today).
  - Deleted or age-restricted posts: they can't be read (2 of the 108 Google finds on 18 Oct).
