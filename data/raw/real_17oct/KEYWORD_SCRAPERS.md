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
