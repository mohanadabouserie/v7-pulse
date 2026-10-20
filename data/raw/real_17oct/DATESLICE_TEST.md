# Date slices: a test (20 Oct 2026)

The user's idea: search one day at a time so each search returns that day's posts. Tested on August 2026. **New** means no earlier route had found the post; **about V7** is Claude's label. Cost is Apify's charge for the search runs; fetching the new finds by link is counted apart.

## Google's site search, August

| Search | Searches | Pages | Cost (USD) | Posts found | In the collection | Found before | New | New, about V7 | Of the month search's finds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Google, Instagram, the month (19 Oct) | 5 |  | (19 Oct) | 79 | 73 | 73 | 0 | 0 |  |
| Google, Instagram, a week at a time | 25 | 45 | 0.110 | 164 | 156 | 60 | 96 | 7 | 55 of 79 |
| Google, Instagram, a day at a time | 155 | 177 | 0.428 | 375 | 365 | 70 | 295 | 10 | 58 of 79 |
| Google, Facebook, the month (19 Oct) | 6 |  | (19 Oct) | 52 | 41 | 41 | 0 | 0 |  |
| Google, Facebook, a week at a time | 30 | 52 | 0.128 | 226 | 197 | 53 | 144 | 8 | 33 of 52 |
| Google, Facebook, a day at a time | 186 | 188 | 0.468 | 206 | 170 | 45 | 125 | 1 | 23 of 52 |

Posts found = distinct post links in the results, V7's own pages left out. In the collection = fetched and kept (posted 20 Apr to 16 Oct). The 19 Oct month search read 3 pages (Instagram) or 2 (Facebook) for each phrase.

## Facebook's own search, one day at a time

| Day | Keyword | Scraper | Rows | On that day | About V7 | New, about V7 | Of that day's posts collected before |
|---|---|---|---:|---:|---:|---:|---:|
| 2026-10-15 | ڤي كولا | scraper_one, latest | 10 | 9 | 2 | 0 | 2 of 14 |
| 2026-10-15 | ڤي كولا | silentflow, top | 10 | 10 | 3 | 1 | 2 of 14 |
| 2026-10-15 | V7 كريم صودا | scraper_one, latest | 10 | 5 | 2 | 0 | 2 of 14 |
| 2026-10-15 | V7 كريم صودا | silentflow, top | 7 | 7 | 2 | 0 | 2 of 14 |
| 2026-10-15 | ڤي سڤن | scraper_one, latest | 10 | 10 | 0 | 0 | 0 of 14 |
| 2026-10-15 | ڤي سڤن | silentflow, top | 4 | 4 | 0 | 0 | 0 of 14 |
| 2026-08-15 | ڤي كولا | scraper_one, latest | 9 | 9 | 8 | 7 | 1 of 12 |
| 2026-08-15 | ڤي كولا | silentflow, top | 10 | 10 | 1 | 0 | 1 of 12 |
| 2026-08-15 | V7 كريم صودا | scraper_one, latest | 10 | 5 | 7 | 3 | 2 of 12 |
| 2026-08-15 | V7 كريم صودا | silentflow, top | 2 | 2 | 1 | 0 | 1 of 12 |
| 2026-08-15 | ڤي سڤن | scraper_one, latest | 0 | 0 | 0 | 0 | 0 of 12 |
| 2026-08-15 | ڤي سڤن | silentflow, top | 0 | 0 | 0 | 0 | 0 of 12 |
| 2026-08-04 | ڤي كولا | scraper_one, latest | 5 | 0 | 0 | 0 | 0 of 9 |
| 2026-08-04 | ڤي كولا | silentflow, top | 5 | 5 | 1 | 1 | 0 of 9 |
| 2026-08-04 | V7 كريم صودا | scraper_one, latest | 3 | 3 | 0 | 0 | 0 of 9 |
| 2026-08-04 | V7 كريم صودا | silentflow, top | 0 | 0 | 0 | 0 | 0 of 9 |
| 2026-08-04 | ڤي سڤن | scraper_one, latest | 5 | 4 | 4 | 0 | 4 of 9 |
| 2026-08-04 | ڤي سڤن | silentflow, top | 0 | 0 | 0 | 0 | 0 of 9 |

Facebook's own search, all 18 runs: 100 rows, 25 distinct posts about V7, 12 of them new; USD 0.271.

## Fetching the new finds by link

- Instagram: 355 posts, USD 0.817. Facebook: 267 posts, USD 0.622.

## What it shows (20 Oct)

- **Facebook's own search, one day at a time, did best:** 12 new posts about V7 for USD 0.27, 10 of them from scraper_one sorted by latest on 15 Aug. 6 of the 12 are different people posting the same copy-and-paste text ("choose V Cola, an Egyptian product"). Both scrapers keep to a one-day window (scraper_one 5 to 10 of 10 rows on the day). A month sorted by top (the 19 Oct June test) returned filler instead.
- **Google, a week at a time:** 7 new Instagram and about 7 new Facebook posts about V7 in August, about USD 0.05 to 0.07 a post with fetching. Most of what it finds is off topic.
- **Google, a day at a time:** results keep to the day, but quiet days are filled with near matches (Cambodia's V-Cola, other colas, random posts): Instagram 10 of 295 new finds about V7, Facebook 1 of 125. About USD 0.11 to 0.76 a post. Not worth it.
- **The snippet can't pre-filter Google's finds:** the phrase is missing from it for 6 of the 14 new Instagram posts about V7 and 5 of the 7 Facebook ones.
- **Whole test:** USD 2.87 on Apify's meter (71.83 to 74.70); 661 new posts collected and labelled, 33 about V7 (Instagram 14, Facebook 19), 32 of them from August. Not in the dashboard yet.

