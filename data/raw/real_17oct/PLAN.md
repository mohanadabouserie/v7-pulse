# Real data everywhere (17 Oct 2026)

The user upgraded Apify and asked for real data in every tab except **Market** (Online stores, Restaurants, Search trends), which stays as it is. No demo data, no estimated numbers. Claude (the user's own Claude plan, through Claude Code) reads and labels everything.

## 1. Budget
- **Apify Starter:** USD 19 of usage a month, which is also the hard ceiling. The cycle runs 16 Oct to 15 Nov 2026. Used before this collection: USD 0.00.
- **Prices:** at the Starter level (Apify's BRONZE tier), read from the Apify API on 17 Oct:

| What | Actor | USD per item |
|---|---|---|
| V7's Facebook posts | apify/facebook-posts-scraper | 0.004 (+0.001 date filter) |
| Facebook comments, with replies | apify/facebook-comments-scraper | 0.002 |
| V7's Instagram posts | apify/instagram-post-scraper | 0.0015 |
| Instagram comments, with replies | apify/instagram-comment-scraper | 0.0023 |
| TikTok videos (profile or search) | clockworks/tiktok-scraper | 0.003 (+0.001 date filter) |
| TikTok comments | clockworks/tiktok-comments-scraper | 0.001 |
| YouTube videos (channel or search) | streamers/youtube-scraper | 0.003 |
| X posts (search) | kaitoeasyapi/…-cheapest | 0.00022 |
| Facebook public posts (search) | scraper_one/facebook-posts-search | 0.003 |
| Instagram hashtags | apify/instagram-hashtag-scraper | 0.0023 |
| Reddit posts and comments | trudax/reddit-scraper-lite | 0.0038 (+0.02 a run) |

- **Split:** at most **USD 14** for this collection, with a cap on every run. The other **USD 5** stays in reserve for re-runs and a refresh before 15 Nov.
- **Claude:** the labelling runs on the user's Claude plan (the bot's sign-in, personal account), so there's no API cost.

## 2. The window: 180 days, 20 Apr to 16 Oct 2026
- It's the dashboard's full range, so the 7, 30 and 90-day views and their previous periods all rest on real data.
- **Comments on V7's own posts** are most of the cost: about 3,300 over 180 days (Facebook 1,100, Instagram 1,100 plus the posts before 27 May, TikTok 1,050; YouTube shows none). That's about USD 6.5 with replies.
- **Public posts are few.** The 11 Oct searches found about 1 to 2 a day across all platforms, so searching them costs about USD 4.
- **V7's posts** (to refresh the counts) and **the pages abroad** cost about USD 1.5.
- **Total:** about USD 12. With 90 days the total would be about USD 9, so the extra 90 days cost about USD 3.

## 3. Each tab
| Tab | Now | Real source after this |
|---|---|---|
| Overview, All posts, Products, Hashtags | demo public posts | public posts found on X, Facebook, Instagram, TikTok, YouTube and Reddit, plus V7's posts, each read and labelled by Claude |
| Customer voice | demo comments | every comment on V7's posts in the window, with V7's replies (so "answered" is real), labelled by Claude |
| People | demo authors | the real authors. Private people stay anonymous (DECISIONS #75) |
| Our content | real posts; demo profile visits and follower details | real posts with counts as of the check. Profile visits and follower details need V7's Meta and TikTok business access, so they're removed |
| Daily brief, Alerts | computed from demo | computed from the real data |
| Rumors & attacks | real (11 Oct) | real, with the new posts labelled for claims |
| Events | real list, demo evidence | the real list, with evidence counted from the real data |
| Outside Egypt | real pages abroad; demo posts | the pages abroad and the comments on them, plus public posts that state a country or are in a non-Egyptian dialect |
| Market | real | unchanged |

## 4. The collection (collect.py)
Stages run in this order. Each run saves `raw/<name>.json` with its input:
1. **test:** 3 to 5 items from each actor, to confirm prices, date filters and fields (about USD 0.15).
2. **own:** V7's posts on Facebook, Instagram, TikTok and YouTube since 20 Apr.
3. **comments:** every comment on those posts, with replies.
4. **abroad:** the posts of the 5 pages abroad, and their comments.
5. **ugc:** searches on X, Facebook, Instagram hashtags, TikTok, YouTube and Reddit for V7, its products and V Cola, in Arabic, English and Franco-Arabic, with date limits.

**News coverage:** found by Claude with web search, at no Apify cost.

## 5. Labels (Claude)
Each item gets the following labels:
- about V7, yes or no (it filters out the Haval V7 car and the like);
- one of the dashboard's classes (question, complaint, idea, praise…);
- sentiment (positive, neutral, negative or mixed) and emotion;
- the products named, and the language;
- the place, only when the text says it: a governorate or a country;
- for rumor-related items, the claim and the stance.

Batches go through `claude -p` with a JSON schema; the prompt and every label are saved.

## 6. Then
- Build the data blocks, and rebuild the dashboard on them (Version 25). Remove what can't be real.
- Update the tests that assumed demo data, review as the marketing manager and as a UI/UX reviewer, and publish privately. The public site only after the user's OK.

## Open questions for the user
- **#18:** views count "on the day they happen", but only one snapshot exists for the past. Count them on the day the post went up, as of the check date?
- **#17:** reach is estimated from engagement where a platform hides views. Use views where shown and engagement elsewhere, with no estimate?
