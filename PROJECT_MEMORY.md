# V7 Pulse: project memory

Last updated: 18 Oct 2026 (dashboard Version 26: the wider search, 586 public posts about V7, and YouTube comments; Version 25: real data everywhere but Market, 20 Apr to 16 Oct 2026, labelled by Claude)

## 1. What this is
V7 Pulse is a social listening and market dashboard for V7's marketing team. Mohanad (the user, an internal employee) is proposing it to V7's marketing manager.

- Today it's a working prototype in one HTML file.
- Since Version 26 (18 Oct 2026) public posts are searched with many Arabic and English spellings and workarounds, and YouTube comments are in.
- Since Version 25 (17 Oct 2026) every tab uses real data: V7's posts and every comment on them, the pages abroad, and the public posts about V7 from six platforms (20 Apr to 16 Oct 2026), each labelled by Claude. Market (stores, restaurants, search trends) is real too, apart from the store history before 4 Oct, which the user asked to leave as it is.
- The plan is to host it later (Hostinger or a VPS), with daily data collection through Apify and Claude answering questions about the data.
- The project started on 3 Oct 2026 with the request "use Apify to make a daily or weekly report about V7, like the reference docs". The reference docs are dima's sample listening reports, in `Reference docs/`.

## 2. Deliverables and where they are
| What | Where |
|---|---|
| Dashboard (main deliverable) | `V7_Pulse_Dashboard.html`, published privately at https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc (Version 31, 19 Oct 2026) |
| Design system | `DESIGN.md`: V7 brand colors, can color per product, type, shapes, layout and chart rules. Guarded by `tests/test_v15.py` |
| Dashboard, public site | https://mohanadabouserie.github.io/v7-pulse/ (GitHub Pages, public, noindex; Version 30 since 19 Oct). Served from `docs/` of https://github.com/mohanadabouserie/v7-pulse, which is now **this whole project folder** (pushed 11 Oct for a collaborator). Built by `python3 deploy/build_sites.py dashboard`. Ask V7 Pulse gives built-in answers only there. The old clone `deploy/v7-pulse/` was deleted on 12 Oct |
| Earlier proposal page | `V7_Pulse_Proposal.html`, https://claude.ai/artifact/5vu6KEfGcuAqHi6j9M1b2g |
| Cost calculator | `V7_Pulse_Costs.html`, published privately at https://claude.ai/artifact/7W1HvsWL1brdpe7eNxEx4P (Version 3). Yearly fixed and variable costs. The controls include questions a day, refresh rate, and a "Claude models" panel with a model for answers, analysis runs and reading posts and comments, plus batches. Old versions are in `archive/costs_versions/`; test: `tests/test_costs.py` |
| Cost calculator, public site | https://mohanadabouserie.github.io/v7-pulse-costs/ (GitHub Pages, public, noindex). Repo https://github.com/mohanadabouserie/v7-pulse-costs, local clone `deploy/v7-pulse-costs/`. Built from `V7_Pulse_Costs.html` by `deploy/build_sites.py` |
| Proposal email | Sent 4 Oct 2026 to the user's AUC address, subject "Proposal: a social listening dashboard for V7" |
| Ask V7 Pulse, hosted setup | `Ask_V7_Pulse/`: `system_prompt.md`, `tools.json` (14 tools), `apify_allowlist.json`, `README.md` |
| Daily store checker | `data/collect_store_history.py` (not scheduled, see open items). Noon is read by Claude through `data/noon_llm.py`. Runs with `data/.venv/bin/python`. Tests: `tests/test_noon_llm.py` |
| Store history | `data/store_history/YYYY-MM-DD.json` (real from 4 Oct 2026) |
| Raw data from every test and collection | `data/raw/` (map in section 10) |
| Old dashboard versions | `archive/dashboard_versions/V7_Pulse_Dashboard_v3.html` to `_v30.html` (the current version is the main file) |
| Helper scripts | `scripts/` (Apify runners) |
| Browser tests | `tests/` (Playwright) |

The dashboard artifact is private. People can't open it until it's shared from the page's Share menu. The file also opens offline in any browser.

**Sharing notes (6 Oct 2026):**
- Every viewer gets the same built-in data; only the Ask V7 Pulse chat differs, because each viewer allows Claude on their own plan.
- If something looks missing for a viewer, check two things:
  - on narrow screens, the menu becomes a strip that scrolls sideways;
  - browsers older than 2023 don't support `color-mix()` and show some bars blank.
- A viewer's "missing hashtags" report was resolved with no change to the page.

## 3. About V7 (verified facts)
- **What it is:** an Egyptian vitamin soda.
- **Ownership:** the V7 and V Cola trademarks belong to Benefit (بينيفت). Vitality (ڤيتاليتي) is its manufacturing arm. Source: El Watan / SIS, May 2026.
- **Factory:** in Sadat City, Menofia, opened by PM Madbouly on 11 May 2026 (EGP 1.5B).
- **Exports:** 48 countries on 6 continents in 2026, with a target of 80+ by 2030. Exports tripled in 2024, when V7 was sold in 21 countries (Reuters).
- **13 products:**
  - flavours: Pomegranate, Piña Colada, Lemon Mint, Blueberry, Pineapple, Pink Lemonade (a 2025 summer edition, with a Dara's co-brand);
  - malts: Pineapple Malt and Apple Malt (Malt is not new; the Amazon pineapple malt listing has 539+ reviews);
  - Cream Soda, seasonal: the 2026 summer edition launched on 6 Aug (teaser 2 Aug), went off shelves on 10 Sep and is "back summer 2027";
  - the V Cola line: V Cola, V Cola Diet and Lemon-Lime (V Super Soda, April 2025). V7's July reels call the Lemon-Lime can "V Lemon", as Carrefour does;
  - **V Orange**, new in the V Cola line, launched on 11 Oct 2026 on Facebook, Instagram and YouTube (posted with the V Super Soda page). Not on TikTok yet, and not in the stores at the 4–5 Oct check (13 Oct).
- **Partnerships seen in V7's posts (2026):** Circle K × V7 Mixology Menu (30 Jul), V7 × Cairokee night at Masyaf Ras Alhekma (17 Aug), On the Run × V7 Refreshment Menu (30 Aug).
- **Shelf price:** about EGP 15 for a 300 ml can at Amazon.eg and Carrefour.
- **Official accounts:**

  | Account | Followers (real, 13 Oct) |
  |---|---|
  | facebook.com/V7Egypt | 79,783 (76,755 on 5 Oct). Ad Library: "isn't currently running ads" |
  | instagram.com/v7egypt | 38,959 |
  | tiktok.com/@v7.egypt | 36,900 (151.9K likes, 87 videos) |
  | youtube.com/@V7Egypt | 2,540 (35.8M channel views, 47 videos) |
- **V7 accounts abroad:**

  | Account | Followers (13 Oct) |
  |---|---|
  | @v7tunisia | 4,174 |
  | @v7uzbekistan | 1,808 |
  | @v7ldnuk (UK) | 355 |
  | @drinkv7 (India) | 112 |
  | @thehalaldrinksco (UK distributor) | 1,272 |

  The UK distributor is Halal Drinks Co (halaldrinksco.com).
- **Seen abroad:** a shop in Gaza, Malaysia, "V7 Mauritania".
- **Not yet confirmed by V7:**
  - the official price (EGP 15 is used as an example);
  - that Malt is alcohol-free;
  - batch testing and no recall;
  - the giveaway policy.

  The fact sheet in Rumors & attacks marks these as examples.
- **Naming traps in search:**
  - "V7" also means the Haval and Changan cars, Vivo and Honor phones, Midjourney V7 and the Dyson V7.
  - "في سفن" also means "in ships". Search "ڤي سڤن" or the exact phrase instead.

## 4. The dashboard today (Version 31)
**Look (since 7 Oct, see `DESIGN.md`):**
- V7's green master brand: a green sidebar with a white pill for the current tab, green pill buttons, uppercase titles in Nunito Sans.
- Navy for quantities, gold for events, green / grey / red for sentiment. V7 is green against PepsiCo blue and Coca-Cola red.
- Every product has its can color (dots and card strips).
- Navigation: Overview, then Conversation, To act on (Alerts, Rumors & attacks, Events), Market, International.
- On phones, the filters sit behind a Filters button.
- **Version 20, realistic demo:** about 1 to 2 public posts a day, and posts and comments shown together (most of it, about 75% since Version 21's real posts, is comments under V7's posts). No Facebook groups tab, emotions, word cloud or dialect split. Reply tracking is on Facebook and YouTube. Follower details and online times are Instagram insights. Alerts are sized for real volumes (DECISIONS #80–86).
- **Version 21, real own posts (DECISIONS #87–94):**
  - Data runs to 12 Oct 2026.
  - V7's own posts are real on all four platforms: 129 posts since 16 Apr; Instagram is real from 27 May (Version 22). Built by `data/raw/verify_13oct/build_own_posts.py --inject`. Followers are the 13 Oct counts.
  - Engagement-rate averages leave out posts with views 20+ times the followers.
  - V Orange is in, with launch handling: "Excited to try it", "Looking for it" and a "Launch questions" alert.
  - The V7 pages abroad table and their latest posts are real.
  - Real launches and partnerships are events, and the V Orange launch is the pending suggestion.
  - "Partly real" badge on Our content and V7 pages abroad.
- **Version 25, real data everywhere (DECISIONS #113–123; plan in `data/raw/real_17oct/PLAN.md`):**
  - **Collected 17 Oct for 20 Apr to 16 Oct 2026:**
    - V7 Egypt's 132 posts (Facebook 34, Instagram 51, TikTok 19, YouTube 28);
    - every comment on them: 2,894 shown, plus 632 replies by V7 and V Super Soda; 223 off topic dropped;
    - the pages abroad: 194 posts and 829 of 1,837 comments (budget);
    - 219 public posts about V7, out of 1,078 found (X 63, Facebook 106, YouTube 20, TikTok 16, Instagram 12, Reddit 2).
  - **Labels:** Claude labelled 4,196 items on the user's Max plan; the API would have charged about USD 15.
  - **Findings, 180 days:**
    - Comments: 60% positive, 4% negative, 1% mixed.
    - Most common in comments: emoji reactions (914), love the taste (302), flavour requests (234), excited to try (175), loves the ad (113), bigger bottles (106), sales leads (66).
    - V7 answered 167 of the 376 comments that needed a reply.
    - The biggest public post: Kareem Elsayed's YouTube video “Can an Egyptian company compete with Pepsi and Coca-Cola?” (9 Oct, 1.47M views).
    - Uzbekistan's giveaway posts drive most comments abroad.
    - No new rumor claim since the 11 Oct check.
  - **Removed:** the demo generators, profile visits and follower details (they need V7's account insights), estimated reach, the views spread over days, the demo groups, and a made-up event.
  - **Images:** 312 posts now have their cover image (V7 Egypt 129 of 132, pages abroad 98 of 194, public 75 of 219). The page is 6.2 MB.
  - **Published** privately on 17 Oct (DECISIONS #124 explains the publish guard fix), and on the public site the same day. The bot reads that copy.
- **Version 26, the wider search and YouTube comments (18 Oct, DECISIONS #127–132):**
  - **Why:** the user saw one Instagram post about V7 by other people in the last week. Instagram had only 8 hashtags, and TikTok's date filter returned unrelated videos.
  - **Searched:** many Arabic and English spellings, plus Instagram posts that tag V7, Instagram keyword search, Google searches of Instagram and TikTok, and TikTok from Egypt. Every scraper, input and output is in `data/raw/real_17oct/SCRAPERS.md`.
  - **Public posts about V7:** 586, up from 219: Instagram 280, Facebook 124, TikTok 96, X 63, YouTube 21, Reddit 2. In the last 7 days: Instagram 18 (was 1), TikTok 6 (was 0).
  - **YouTube comments:** 731 shown: 676 under the public videos about V7 (most under Kareem Elsayed's, 9 Oct) and 55 under V7's own. 120 date only to the month and are listed under their video.
  - **Corrections:** comments are on for 27 of V7's 28 YouTube videos (Version 25 said off). V7's YouTube titles are the original Arabic.
  - **Findings:**
    - "Can't find V7" now fires: 15 this week, 10 of them YouTube comments about availability (cafés' fridges, Upper Egypt, supply).
    - In Egypt over the last 30 days, comments under other people's posts are 59% of the conversation, comments under V7's posts 26%, public posts 15%.
  - **Page:** 8.0 MB with 431 images. Published privately and on the public site on 18 Oct; the bot reads that copy.
- **Versions 27 and 28 (19 Oct, DECISIONS #133–138):** likes an owner hid say "likes hidden"; Instagram keyword search moved to apidojo plus dami_studio's Reels search, with a re-fetch by link for missing captions and likes; what's said in reels is read with the caption (speech to text); Instagram accounts have follower counts. Both are on the public site.
- **Version 29, the Instagram gaps (19 Oct, DECISIONS #139–142):**
  - **Why:** the user asked to close every Instagram gap, to read the text in music reels and albums, and to find the most accurate way. Apify's usage limit is now USD 100.
  - **Most accurate way to read a post without speech:** Claude reading its pictures (photos, or a frame every 2 seconds of a reel). It matched or beat afanasenko's paid extractor on the test. Comments say what people think but rarely what a post shows; alt text is generic.
  - **Instagram public posts about V7:** 479 (was 283). Routes: posts tagging V7 250, Google month by month 151, keyword search 112, Reels search 53, hashtags 22; 390 found by one route only.
  - **Read:** 202 reels with their speech, 423 posts from their pictures. The pictures changed the type of 135, the products of 176 and the sentiment of 72; 38 became about V7.
  - **Comments under public Instagram posts:** 2,633 collected, 2,296 about V7 shown under their post (1,518 positive, 286 negative). Anonymous, never "waiting for V7".
  - **Totals:** 785 public posts about V7, 5,918 comments shown, 546 images, 10.2 MB.
  - **Coverage:** roughly 60% of the window's public Instagram posts by the closest pair of routes (about 780 estimated); other pairs say less. Private accounts, Stories, hidden likes and most shares can't be had.
  - **Review fixes:** 21 Instagram accounts had a scraper's "Access delayed…" text as their name (now their real name or handle); the page says collected on 17–19 Oct; the Overview and Ask V7 Pulse no longer say comments under other people's posts aren't collected. People's "Creators & pages" tile no longer claims all of them have 10K+ followers (16 of 69 do).
  - Published privately on 19 Oct, and on the public site the same day (with Version 30).
- **Version 30, Facebook (19 Oct, DECISIONS #143–148; `data/raw/real_17oct/FB_KEYWORD_SCRAPERS.md`):**
  - **Why:** the user asked for the same work on Facebook: compare every keyword scraper, combine the best, fill the gaps, and cover videos and reels.
  - **Compared:** 19 scrapers and routes. The post searches share Facebook's search; only the first 10-15 results per keyword are about V7. Arabic with ڤ works on Facebook.
  - **Facebook public posts about V7:** 520 (was 124): 152 reels, 26 videos, 181 photos, 54 albums, 107 text. Routes: scraper_one, silentflow and Apify's search (30 keywords), the reel and video searches, public groups, Google month by month.
  - **Filled:** plays on 158 of 178 videos; speech on 163 (invideoiq); 267 read from their pictures; 2,797 comments under the posts (thedoor); followers for 210 of 302 named pages (34 with 100K+).
  - **Fixed:** reels and videos had been marked as photos; a V Super Soda reel (19.1M views) had counted as public; three posts entered by hand before Version 25 hid or duplicated the collected ones; "Needs your attention" showed two negative days and lost the replies card.
  - **Totals:** 1,181 public posts about V7 (Facebook 520, Instagram 479), 8,706 comments shown, 708 images, 13.4 MB.
  - **Coverage:** about 390 of the roughly 600 posts Facebook's search can surface; the reel, video and Google route shows many more reels and page videos exist.
- **Version 31, Facebook reels and five post searches (19 Oct, DECISIONS #149–151):**
  - **Why:** the user asked whether overlapping scrapers were used for reels, as for Instagram, and to rely on several to cover more.
  - **Reels compared:** 13 reel and video searches on 4 keywords. Google's short videos (Facebook only) found 17 of its 25 V7 reels that no Facebook search found; alien_force's reels-only search 6.
  - **Added:** Google's short videos (30 keywords), alien_force reels (15 keywords), scrapeforge and fetch_cat post searches (30 keywords).
  - **Facebook public posts about V7:** 590 (was 520): 192 reels, 26 videos, 185 photos, 60 albums, 127 text. Plays on 201 of 218 videos, speech on 203, pictures on 265, 3,128 comments, followers for 248 pages.
  - **Coverage:** the post searches found 434 of about 690 posts Facebook's search can surface; reels about 192 of perhaps 500.
  - **Totals:** 1,251 public posts about V7, 9,037 comments shown, 774 images, 14.2 MB (near the 16 MB limit).
  - Published privately on 19 Oct. The public site is Version 30 until a push.
  - Published privately and on the public site on 19 Oct; the bot reads that copy.
- **Version 24, Telegram (DECISIONS #105–107):**
  - **@v7_pulse_bot** sends the daily brief at 09:00 and Act now alerts, and answers questions like Ask V7 Pulse. See `bot/README.md`.
  - Join link: `t.me/v7_pulse_bot?start=<code from .env.telegram>`.
  - It runs on the user's machine, so it's live while that machine is on. It stops when the machine shuts down: it stopped at 02:47 on 17 Oct and was started again at 05:48 after the restart (process id in `bot/state/bot.pid`).
  - Each chat gets each day's brief once: while the data stops at 12 Oct, the 09:00 run sends nothing new (DECISIONS #108). A chat that joins gets the welcome, the latest brief and any open Act now alert.
  - No alert is at Act now level in the current data (4 Watch, 2 Opportunity), so none is pushed; the admin's `/test` shows one.
  - Its Telegram menu (brief, alerts, ask, help, stop) and descriptions are set (DECISIONS #109).
  - Questions are answered by Claude through Claude Code, with the dashboard's own instructions and eight read-only tools (DECISIONS #110–112). Signed in since 16 Oct, 23:55 with the user's personal account (Max plan); the work account is refused (`CLAUDE_BLOCKED_ORGS`).
  - First real question ("main complaints this month, and what to do"): 18 seconds, Opus 5.5 at medium effort, 4 turns with the dashboard's tools, 1,722 characters with four recommended actions, labelled as demo data where it was. The API would have charged about USD 0.16 for it; on the Max plan it counts toward the plan's limits instead.
  - The user joined as the admin on 16 Oct, 22:39. Nobody else has joined yet.
  - The dashboard links to it, and `#brief` and `#alerts` links open those tabs.
- **Version 23, the marketing team's feedback (DECISIONS #99–104):**
  - 183 real posts carry their image, and a post view shows each post with its comments.
  - Overview and Customer voice open with "Needs your attention".
  - Alerts have a next step, an owner, a suggested reply, and an email and phone preview.
  - A Daily brief tab with the morning email.
  - Mixed sentiment, and "Worth amplifying" posts.
- **Rumors & attacks (Version 18): real posts only.** A status sentence, five numbers, three claims (price confusion, active; "V7 was sold to Coca-Cola", contained since May 2024; "V7 Malt tastes like alcohol", watching), the claim detail with every post, "Also worth a look", "Nothing found", how the posts were found, and the fact sheet. Data: `data/raw/social/rumors_11oct/` (see section 10). To refresh: run `collect.py`, `normalize.py`, label the new posts in `labels.json`, then `build_rumors.py --inject`.
- **Online stores (Versions 16 and 17):**
  - Summary: "Needs attention" next to "Against competitors", then "V7 price and stock in each store": each store has its own Price and Stock columns (Version 19).
  - Prices: one drink type at a time, compared per 100 ml with V7.
  - Sales & ranks: "Best-seller ranks" table; rows open the full chart.
  - Stock: a status sentence, a where-to-buy grid, and only the problems, with day strips.
  - Ratings: rows open a details panel (star split, charts, comparison).

**Filters**
- period: 7, 30 or 90 days, or Custom from–to;
- UGC / BGC / All;
- Posts / Comments / Both;
- products (several can be picked; a post can name several products or the whole range);
- platforms: Facebook, Instagram, TikTok, X, YouTube, Reddit.

**Tabs**

| Section | Tab | What it shows |
|---|---|---|
| (top) | Overview | Headline numbers, then "what changed" (left) next to the daily chart, sentiment, intents, topics |
| Conversation | All posts | Every post, sorted by reach |
| Conversation | Products | One card per product. The detail panel opens on the most-discussed product, or the one picked in the filter |
| Conversation | Customer voice | |
| Conversation | People | |
| Conversation | Hashtags | |
| Conversation | Our content | Includes profile visits, followers' city and age, and replies to comments |
| To act on | Alerts | |
| To act on | Events | Suggestions wait for admin approval |
| Market (real data) | Online stores | Sub-tabs: Summary (default: Needs attention, products × stores grid, V7 vs competitors), Prices, Sales & ranks, Stock, Ratings. V7 first; competitor detail opens on demand. Competitors include/exclude switch |
| Market (real data) | Restaurants | Talabat, 10 Cairo delivery areas |
| Market (real data) | Search trends | Google Trends, company total only: weekly line, governorates, related searches, terms used |
| To act on | Rumors & attacks | Fact sheet, campaigns, coordination score, suggested replies |
| International | Outside Egypt | Country level only |

**Other features**
- **Ask V7 Pulse (chat):** in claude.ai, Claude answers from the dashboard's data through 8 read-only page tools (the `sample` capability). Web searches and new Apify collections only show up as suggestion cards, because the published page has no internet access and must never hold the Apify key. Short built-in answers work without Claude.
- **Every "Show all"** has a "Show less".

**Real vs demo (since Version 25, 17 Oct 2026)**

| Real | Demo or not shown |
|---|---|
| V7 Egypt's 132 posts, 20 Apr to 16 Oct (the first is on 7 May; Instagram included), with counts as of 17 Oct | |
| Every comment on them, and V7's and V Super Soda's replies (YouTube from 18 Oct) | YouTube gives only the month for older comments: those are listed under their video, not counted by day |
| The comments under the 14 public YouTube videos about V7 that have comments (18 Oct), under 251 public Instagram posts and 283 public Facebook posts about V7 (19 Oct) | Comments under other people's TikTok and X posts aren't collected |
| The pages abroad: 194 posts and their counts | 829 of their 1,837 comments were collected (budget) |
| 1,181 public posts about V7 from Facebook, Instagram, TikTok, X, YouTube and Reddit (219 on 17 Oct, 586 on 18 Oct, 1,181 on 19 Oct) | |
| Follower counts (13 Oct) | Not shown: profile visits, followers' city and age, online times, reach (they need V7's own account insights) |
| Export facts, rumors and attacks | |
| Online stores | Store history before 4 Oct (shown hatched; left as it was at the user's request) |
| Restaurants | |
| Search trends | |

## 5. Data sources, methods and reliability
### Social platforms (through Apify)
| Platform | Actor (tested) | Notes |
|---|---|---|
| Facebook pages | apify/facebook-posts-scraper | Views, reactions, shares |
| Facebook keyword search | scraper_one/facebook-posts-search | Loose matching: 2 of 3 results were noise, so every post needs a relevance check |
| Facebook groups | apify/facebook-groups-scraper | Public groups only; private groups can't be collected |
| Instagram | apify/instagram-post-scraper, apify/instagram-hashtag-scraper | Views only on reels |
| TikTok | clockworks/tiktok-scraper | Country of a video only when the video URL is re-scraped. Needs a cost cap of at least USD 0.50 |
| X | apidojo/tweet-scraper, apidojo/twitter-user-scraper | "Account based in" on the free plan is limited to 5 runs a month, 10 accounts each |
| YouTube | streamers/youtube-scraper, or the free YouTube Data API | |
| Reddit | Free RSS, slow (about 1 request every 20 s) | The JSON API is blocked; the official API needs approval and a commercial licence. Volume is low: 3 of 215 results were about V7 |

- **Quora:** skipped. There's no API, and nothing about V7 was found.
- **Google News RSS:** free, and covers V7 in the press.

**Hashtag search**
- **What the dashboard has today:** its hashtags are demo data, generated with the demo posts.
- **In the real pipeline:** hashtags are pulled from the posts that the keyword searches and V7's own accounts return.
- **Searching by hashtag works for V7's real hashtags.** `#v7egypt` on Instagram (4 Oct) returned 5 of 5 posts about V7, including designers' concepts and @drinkv7 India.
- **`#اشرب_اي` returned nothing about V7** (5 Oct, USD 0.022): Instagram has no public posts for it, and TikTok gave 5 unrelated videos. We're waiting for the user to confirm V7's campaign hashtags.
- **Plan:** search a watchlist of V7 brand and campaign hashtags on Instagram, TikTok and X, alongside the keywords.

**Location**
- Platforms rarely give a location.
- **TikTok:** the video's country, only when re-scraped by URL.
- **X:** "account based in", country only.
- **Instagram:** place tags are rare (0 of 5), and the about-account country is on paid plans only, at USD 0.007 a profile.
- **YouTube:** channel country, set for 1 of 4 channels.
- **Facebook:** no location on posts.
- **Governorate test:** 114 real posts, of which 67 were about V7. A governorate was found for 14 of the 45 Egypt consumer posts, almost all from X profile locations.
- **Decision:** no city or governorate split of posts. Outside Egypt is decided only from positive foreign evidence (platform field, group or page context, place, currency or dialect in the text); everything else counts as Egypt.
- **Ideas kept for later:** a list of local Facebook groups by governorate, a per-author "home governorate" from accumulated clues, and a gazetteer for bios.

### Our own accounts (needs V7's access)
- **Profile visits:**
  - Facebook: `page_views_total`.
  - Instagram: `profile_views`, last 90 days only.
  - TikTok: profile views through TikTok Business, or an export.
  - YouTube: doesn't report profile visits.
- **Followers' city and age:** from Meta insights, for accounts with 100+ followers.
- **Status:** the user said the team will get access to V7's Meta accounts. Until then these are demo.

### Online stores (real, collected 4 to 5 Oct 2026)
**Amazon.eg**
- Actor: junglee/Amazon-crawler, about USD 0.005 a product. Never set `countryCode`; it adds USD 0.06 a product.
- Gives price, stock, rating, review count, "bought in past month" (rounded, for example 9K+) and best-seller ranks.

**Carrefour Egypt**
- Actor: blackfalcondata/carrefour-maf-scraper, market `mafegy`. Costs USD 0.01 a run plus USD 0.002 an item, and takes one search string per run.
- Gives price, regular price, offers and in or out of stock.

**Noon Egypt**
- **Top 20 by popularity (since 11 Oct 2026):** the crawlerbros/noon-scraper actor was removed from the Apify Store (404).
  - `data/noon_llm.py` replaces it. curl fetches the Soft Drinks page sorted by popularity (`?sort[by]=popularity&sort[dir]=desc`). Noon stalls HTTP/1.1 requests, but HTTP/2 works in about 0.6 s.
  - Claude (`claude-opus-5-5`, effort low, `fallbacks: "default"`) returns each product's SKU, name, price, rating, rating count and stock warning as JSON.
  - Every value is checked against that product's own text on the page. The rank is the page position. Anything Claude says that the page doesn't show is dropped.
  - One call reads about 18,000 characters of page text. Estimated cost is about USD 0.07 a run; this still needs measuring on the first live run.
  - The page gives the price, stars and rating count, "Only N left in stock", Noon's "#N in Soft Drinks" badge and "N+ sold recently". There's no exact stock and no sales numbers.
- **Ratings:** scrapesmith/noon-com-product-seller-scraper (still working), about USD 0.0002 a product, through `product_rating`. Now only used for tracked listings outside the top 20, and for top-20 rows that show no rating.
- **11 Oct 2026, on the page:** V7 Pink Lemonade is #1 (4.4 stars, 157 ratings, EGP 20). V7 Pomegranate shows "Only 9 left in stock".

**Not covered:** Jumia has no V7 (the search returned "V7" pens). Breadfast, Rabbit, Instashop and Talabat Mart have no public data or ready scraper.

**Daily history:** `data/collect_store_history.py`
- Reads the tracked listings from the last two snapshots.
  - It reads Noon through Claude first, so a Claude problem stops the run before any Apify spend.
  - Then it runs the Amazon, Carrefour and Noon-ratings actors with item and cost caps.
- Writes `data/store_history/<date>.json`.
- Run it with the project's Python: `data/.venv/bin/python data/collect_store_history.py`. It needs `APIFY_API_TOKEN` and `ANTHROPIC_API_KEY`.
- Estimated about USD 0.28 a day with competitors (USD 0.30 before).

### Restaurants (Talabat, real, 5 Oct 2026)
**Areas:** 10 Cairo delivery areas.

| Area | Talabat area ID |
|---|---|
| Zamalek | 8045 |
| Downtown | 7772 |
| Dokki | 8196 |
| Mohandessin | 7534 |
| Maadi | 7595 |
| Heliopolis | 7611 |
| Nasr City | 7676 |
| New Cairo | 7842 |
| Sheikh Zayed | 8062 |
| 6th of October | 10063 |

**Sample:** 5 random pages per area from Talabat's A–Z list (`talabat.com/egypt/restaurants/{aid}/{slug}?page=N&sort=a_z`, 15 per page). That gives 645 picks and 625 distinct restaurants, out of about 10,600 listed. 546 had a menu online.

**Menus:** read with memo23/talabat-scraper in `branchIds` mode, at USD 0.001 a restaurant.
- The actor's own area paging is broken: it always returns page 1.
- Free Apify runs are capped at 100 items.

**Brands (method v2, `brands2.py` and `rest_rebuild.py`):**
- Brands are found in item names AND descriptions, in English and Arabic, so meal deals count.
- Common misspellings are covered: Papsi, Pepesi, Coka, Sprit, Miranda, Fi/Fay Cola, V-Seven, V DIET COLA, V Soda.
- Local colas Big Cola, Maxi Cola and Green Cola are tracked as "other".

**V spellings:** "V Lemon" and "V Lemon Lime" are Lemon-Lime; "V Pineapple", "V barley" (malt) and "V-Seven" are V7.

**Loose review scan:** every rebuild runs a scan of every menu for V-like items that aren't matched, and the leftovers are reviewed by hand. On 5 Oct only "V Yellow" (an energy drink) and "V60" (coffee) were left.

**Cuisine group:** taken from the restaurant's main (first-listed) Talabat cuisine, skipping generic labels like Chicken, Sandwiches or International.

**Completeness and blind spot:**
- On 5 Oct, 30 random scraped menus were compared with Talabat's live pages, and the same drink brands were found in all 30.
- Blind spot: the options inside "has choices" items can't be read, because Talabat asks for a delivery address first. Only 4 restaurants have a generic "Soft drink" item whose brand is unknown: Maher El-Sharkawy, Meat Overdose, Gen Crepe and DUX.

**Photo check:** when a name doesn't say which drink or flavour ("V7", "Soft drink", "V7 Lemon", "Cola"), the item's photo was checked by eye against official can photos.
- Covered: 36 unclear V7 items, 160 generic soft-drink photos and 52 unbranded "Cola" photos.
- A photo counts only if it shows one company's products; mixed stock photos and mocktails don't count.
- The labels are written in `rest_rebuild.py`; contact sheets are in `img/sheets/`.
- In the hosted pipeline, Claude's vision should do this step automatically.

**V7 can designs:**
- Vitamin flavours: white cans with a green V7 and the fruit pictured.
- Malts: gold and black cans.
- The "V" line ("by the creators of V7"): V Cola (blue, "Super Soda Cola"), V Cola Diet (white), and V Lemon (green, "Refreshing Lemon-Lime taste").
- Menus call Lemon-Lime "V7 Lemon" or "V Lemon", but "V7 Lemon" is sometimes Lemon Mint (4 of 13 photos).

**Links:** checked on 5 Oct: all 222 table links returned their menu page, and 20 of 20 opened in a real browser. They must use Talabat's menu format, `https://www.talabat.com/egypt/restaurant/{branchId}/{branchSlug}?aid={areaId}`. The old `talabat.com/egypt/{branchSlug}` format gave "Page Not Found" (fixed in Version 11).

**Locations: two different things**
- **The area filter** shows restaurants Talabat lists for delivery in that area.
- **The area under a restaurant's name** is where the branch is, taken from Talabat's menu page (`initialMenuState.restaurant.areaName`). It was read for the 222 restaurants that appear in the tables, using direct, free requests to talabat.com.
- **How reliable branch names are:** Talabat's branch names (for example "Hunger, Nasr City - Makram Ebeid") matched Talabat's own area for 87% of the 234 checked, and differed in district for 13%. Hunger is really in Imbabah; Jurassic Burger is in Agouza, not Warraq.
- **When Talabat only says "Cairo" or "Giza"** (10 cases), the more specific branch-name area is kept.

**Full coverage** of the 10 areas would cost about USD 10.60 a check and needs a paid Apify plan. Talabat has about 1,700 delivery areas in Egypt.

### Google search trends (real, 5 Oct 2026)
- **How it's collected:** directly from Google Trends' own API (explore, then multiline, comparedgeo and relatedsearches), for free. The Apify actor cost about USD 0.30 a term because of residential proxies. The client is in `data/raw/google_trends/gtclient.py`.
- **Query rules:**
  - Each term is limited to 100 characters.
  - "+" means OR, "-word" excludes, and quotes give an exact phrase.
  - Terms in one request share a scale, so they can be added together.
  - The Food & Drink category (71) leaves V7 empty, so it isn't used.
- **The company series** is the sum of two terms from the same request:
  - `v7` minus the noise words;
  - the Arabic names as exact phrases, plus V Cola.
- **Noise:** 14% of raw "v7" searches are noise (Haval, Changan, Vivo, Honor, Midjourney, uuid). "في سفن" as a loose match is about 94% noise. "في كولا" is left out.
- **What the page shows (Version 13):** the company total only, with no product or flavour series, no spelling split and no noise figures. All three were removed at the user's request and shouldn't be added back.
- **Governorate check (5 Oct):**
  - "في سفن" (exact) is about 2% of company searches, and its map doesn't follow the "سفن" (ships) map (rank agreement 0.09).
  - English "v7" and the V Cola spellings rank governorates alike (0.68), and a repeat pull gave identical ranks.
  - The map shows V7's share of each governorate's searches, not counts.
  - Matrouh includes the North Coast, so summer visitors count there.
  - Six governorates have too few searches to report.
  - The data is in `data/raw/google_trends/geo_check.json`.

## 6. Key real findings
**Online stores**
- **Amazon.eg, bought last month:**
  - V Cola with V Cola Diet (one listing): 9K+, #1 in Cola;
  - Pink Lemonade: 3K+;
  - Pineapple Malt: 3K+;
  - Lemon Mint: 2K+;
  - Piña Colada: 2K+, #1 in Still Fruit Drinks;
  - Blueberry: 1K+;
  - Pomegranate: 1K+;
  - Lemon-Lime: 900+.
- **Amazon.eg, against competitors:** V7 listings 21.9K+ last month, PepsiCo 13K+, Coca-Cola Co. 1.7K+. V Cola Diet is the #1 fizzy drink, and V7 holds 3 of the top 20.
- **Price per 100 ml at Carrefour:** V7 EGP 5.0, Pepsi 4.2, Coca-Cola 4.8.
- **Noon:** sellers charge EGP 20 to 22.70 for a V7 can, against EGP 14.50 for Pepsi and 7UP. Pink Lemonade is #1 in Noon Soft Drinks. V7's Noon ratings are 4.1 to 4.4, on 145 to 215 ratings each; rivals have 1 to 29.

**Restaurants (546 menus, method v2, Version 12)**
- Share of menus: V7 16% (85 restaurants), Coca-Cola Co. 21% (112), PepsiCo 26% (140).
- 56 restaurants carry V7 and no rival brand.
- On the most visible restaurants (Talabat's first page), V7 is at 33%, Coca-Cola Co. 33% and PepsiCo 32%.
- Restaurants listing each V7 product (Version 13): V Cola 74, V Cola Diet 18, Lemon-Lime 11, Lemon Mint 10, Blueberry 8, Pomegranate 6, Pineapple 5, Apple Malt 3, Pink Lemonade 3, Piña Colada 3.
- Median menu price of a can: V7 EGP 32, Pepsi EGP 35, Coca-Cola EGP 40.
- V7 is 16% of the 866 branded drink items; PepsiCo 42%, Coca-Cola Co. 37%.
- Before v2, the figures were V7 12% (67), Coca-Cola 15%, PepsiCo 21% and 47 V7-only: names only, with no descriptions or photos.

**Rumors & attacks (real posts, checked 11 Oct 2026)**
- No false rumor is spreading. The live issue is price: 38 posts since Nov 2023 say shops charge EGP 17 to 26 (one restaurant charged 50), or ask the real price. V7 told Cairo 24 (27 Jan 2026) that EGP 20 shops are individual traders.
- "V7 was sold to Coca-Cola" ran 2 to 4 May 2024. The founder denied it, and V7 issued a statement on 4 May.
- Watch: a joke that the apple malt "tastes haram" (Sep 2026); a post saying every flavour is sugar-free (9.2K views); news calling the brand "Seven Cola" (May 2026).
- Not found: fake V7 pages, giveaway scams, coordinated accounts, safety claims.
- V7 is named as a boycott alternative in 21 of 177 posts. The top post, "Buy V Cola, it tastes better than Coca-Cola", has 408K views.

**Comments and volume (real checks, 13 Oct 2026)**
- Public posts about V7 are about 1 to 2 a day across X, Instagram, TikTok and Facebook; most of the conversation is comments under V7's own posts (25 to 177 a post).
- V7 answers most Facebook comments, usually the next day (about 18 h); a follow-up asking for contact numbers and the nearest distributor went unanswered for a week.
- What people ask for under V7's posts: new flavours (watermelon above all, then mango, mixed berry, peach, a winter edition, iced coffee), sugar-free malt, 1 L and 2 L bottles. Sales leads: fridge requests and would-be distributors.
- V7's TikTok "Summer of Colors" video (29 Jul) has 11.4M plays.

**V7's own posts and pages (real, 13 Oct 2026)**
- **Campaigns since April:**
  - **V Lemon relaunch (19–20 May):** 19.4M Facebook views on the "It's now V Lemon" reels, 5.5M on a YouTube Short.
  - **V Cola's "Raise the flag" World Cup campaign (28 May to 7 Jul):** flags on cans and trucks; Seoudi, Breadfast, Talabat, Oscar Grand Stores, Buffalo Burger, ESLSCA, clubs and Ahl Masr hospital took part; the launch reel got 4.7M Facebook views. A Breadfast giveaway ran in June.
  - **New can design (21 Jun):** shown in "Hello Summer. New Design".
  - **Smaller items:** the Cafex Egypt exhibition (7 May) and a Playa booth (16–21 Jul).
- V7 posted 10 times in the last 30 days (5 of them the V Orange launch on 11 Oct), against 24 in the 30 days before.
- **V Orange launch (11 Oct):**
  - 528K views on Facebook, 48K on Instagram and 97K on a YouTube Short in two days, with 154 comments (Facebook 99, Instagram 55).
  - Of 34 comments read, most are excitement and friend tags. About 1 in 6 ask when and where it will be sold ("will it be in every governorate?", "can I order it on Talabat?"). Others ask for 1 L and 2 L bottles, strawberry, peach, mandarin, green apple and sugar-free.
- **Biggest videos:**
  - Malt reel (8 Sep): 13.2M Facebook views, 2.7M on YouTube.
  - Summer of Colors (29 Jul): 12.5M Facebook, 11.4M TikTok, 3.1M YouTube.
  - Cream Soda launch (6 Aug): 6.7M TikTok, 2.6M Facebook, 1.1M YouTube.
  - Views 20+ times the followers point to promotion, but the Ad Library showed no ads running on 13 Oct.
- YouTube: no comments on any of the 12 latest videos.
- **Pages abroad:**
  - V7_UK hasn't posted since 3 Sep.
  - V7 Tunisia posted twice in 30 days.
  - V7 Uzbekistan posts every few days. It lists its shops (Makro, Andalus, Assorti, Baraka, Cool grocery) and on 13 Oct asked for regional distributors. Its 8 Oct posts say "0% Shakar" (0% sugar).
  - V7 India was at Anuga Select India in Mumbai (late Sep).
  - Halal Drinks Co (UK) launched V7 6-packs on 3 Oct and "Meet V Cola" on 10 Oct.

**Search**
- The busiest week was 9 Aug 2026.

**Reddit:** 2 real Cream Soda reviews (r/RateIT_T 9/10 "too sweet", r/EGYescapism "not worth the hype"), plus an r/Egypt thread listing V7 Cola among standout local brands.

## 7. What we can't get, and why
- **City or governorate of posts:** platforms don't expose it reliably.
- **Commenter country:** not exposed.
- **Private Facebook groups:** can't be collected. Public groups can, but finding V7 in them means scraping every post (one 88K group posts about 790 a day, about USD 4 a day per group), so the groups tab was removed.
- **Facebook follower age, gender and city:** retired by Meta (2024–2025); Instagram still reports them, and when followers are online.
- **Instagram and TikTok replies:** the comment actors don't show who replied; needs V7's own account access.
- **Emotions and Arabic dialects:** not reliable on short posts, so not shown.
- **Account age:** public only on X, TikTok and YouTube.
- **Follower counts for personal Facebook profiles and Reddit users:** not public.
- **Views on most Facebook posts, Instagram photos and Reddit:** hidden, so reach is estimated from engagement and capped at the audience.
- **Replies on X:** not collected yet.
- **YouTube comments:** V7's videos have none to collect (13 Oct).
- **A commenter's follower count:** comment tools don't return it; only post authors on X and TikTok, and pages and creators, show followers.
- **Exact stock and sales on Noon and Carrefour:** not shown by the stores.
- **Real sales numbers:** only V7's own data, or a retail audit firm such as NielsenIQ.

## 8. Hosted version plan
**Backend:** calls the Claude Messages API with `Ask_V7_Pulse/system_prompt.md` and `tools.json`.
- **Models:** `claude-opus-5` by default (about USD 0.17 a question), or `claude-sonnet-5` for cheaper everyday answers (about USD 0.07). `claude-opus-5-5` is listed as a newer option.
- **Web tools:** `web_search_20260209` (USD 10 per 1,000 searches) and `web_fetch_20260209`. Fixed on 6 Oct; the package had `20260318`, which isn't a listed version.
- **Dashboard-data tools:** 8 read-only tools.
- **Apify tools:** run only allowlisted actors, with item and cost caps. Runs above the auto-approve limit need an admin's approval.
- **Option B:** Apify's MCP server, with an allowlist. It's quicker to set up but has no per-run cost caps.

**Data collection:** daily runs through Apify. The store checker is ready but not scheduled.

**Alerts:** by email to the marketing team inbox.

**Running cost estimate (6 Oct, from `V7_Pulse_Costs.html`, prices checked 6 Oct 2026):**
- **Recommended setup:** about USD 2,497 in year one (EGP 130,573), or USD 208 a month. From year two it's USD 2,569, when hosting renews at the full price.
  - Fixed: USD 332 (hosting 108, domain 20, Apify Starter 204).
  - Variable: USD 2,165 (answers 1,228, reading posts and comments 86, analysis runs 122, data collection above the Apify plan 728).
- **Lean setup:** USD 902 a year. **Heavy setup:** USD 11,792 a year.
- **Biggest levers:**
  - An hourly social refresh adds about USD 3,040 a year.
  - Sonnet 5 instead of Opus 5 saves about USD 719 on answers and USD 73 on analysis runs. Reading posts and comments on Haiku 4.5 in batches costs USD 86; on Sonnet 5 it adds USD 86, on Opus 5 USD 344, and turning batches off doubles it. All three model pickers are in one panel since Version 3.
- This replaces the 3 Oct estimate of USD 60 to 130 a month.

## 9. Apify account and spend
- **Plan:** Starter since 16 Oct 2026: USD 19 of usage a month included. On 19 Oct the user raised the usage limit to USD 100; usage above USD 19 is billed as overage. The cycle runs 16 Oct to 15 Nov 2026. (Before: the Free plan, USD 4.64 of 5 spent by 13 Oct.)
- **Spent this cycle:** USD 16.33 by Apify's meter on 18 Oct (17 Oct: USD 12.04; 18 Oct: 4.28, by the final run charges). About USD 2.67 left until 15 Nov. Every run, with its input, output and cost: `data/raw/real_17oct/SCRAPERS.md`.
- **19 Oct:** a comparison of 7 Instagram keyword scrapers (`data/raw/real_17oct/KEYWORD_SCRAPERS.md`) cost USD 0.26 by the run records; with the follow-up checks (USD 0.03) and the re-fetch test (USD 0.04), Apify's meter reads USD 16.74 of 19. The transcript test (USD 0.016) brought it to USD 16.76. Version 28's follower counts (USD 0.40) and speech (USD 0.98) bring it to USD 18.14. Version 29 (USD 12.13 by the final run charges) brought it to USD 30.31. Version 30, Facebook (USD 24.88), brought it to USD 55.21. Version 31, Facebook reels and two more searches (USD 15.87), brings it to **USD 71.08**: USD 52.08 of overage so far, and USD 28.92 left under the USD 100 limit until 15 Nov.
- **Prices at Starter (BRONZE tier, checked 17 Oct):** Facebook posts USD 0.004 (+0.001 date filter), Facebook comments 0.002, Instagram posts 0.0015 (+0.0008 details), Instagram comments and hashtags 0.0023, TikTok 0.003 (+0.001 date filter), TikTok comments 0.001, YouTube 0.003, X 0.00022, Facebook search 0.003, Reddit 0.0038 (+0.02 a run). Facebook's comment date filter is charged per comment: don't use it when the posts are already in the window.

**Spend log**

| Date | What | Cost (USD) | Running total (USD) |
|---|---|---|---|
| 3 Oct | First tests | 0.021 | |
| 4 Oct | Location tests | 0.13 | |
| 4 Oct | Store tests | 0.26 | |
| 4 Oct | Trends and Reddit work | | |
| 5 Oct | Verification calls | | 1.41 |
| 5 Oct | Talabat menus and competitors | | 2.80 |
| 5 Oct | Noon and history | | 3.22 |
| 5 Oct | Hashtag test | 0.022 | 3.24 |
| 11 Oct | Rumors pull: X, Facebook, Instagram, TikTok (413 posts) | about 0.47 by the run log | 3.83 (Apify's reading) |
| 13 Oct | Review checks: Facebook and Instagram replies, V7's TikTok and its comments, X this week | 0.11 | 3.96 |
| 13 Oct | Deeper pass: V7's own posts on 4 platforms, the pages abroad, YouTube details, page followers, V Orange comments | about 0.19 by the run log | 4.25 (Apify's reading, with late charges from earlier runs) |
| 13 Oct | Backfill of V7's own posts to 16 Apr: Facebook 21, TikTok 9, Instagram 45, YouTube 30, plus two 3-post tests | 0.39 (run records) | 4.64 |
| 17 Oct (new cycle, Starter) | Real data for every tab but Market, 20 Apr to 16 Oct (`data/raw/real_17oct/`): tests 0.06; V7's 132 posts 0.26; 2,922 comments on them 5.82; the pages abroad's 194 posts and 829 of their comments 2.35; 1,292 public posts from X, Facebook, Instagram, TikTok, YouTube and Reddit 3.12 | 11.62 (run records) | 12.05 (Apify's meter) |
| 18 Oct | The wider search and YouTube comments (DECISIONS #127–132): tests 0.23; Instagram tags, keyword search and Google finds, TikTok from Egypt and Google finds, more Facebook, X and YouTube spellings 3.06; TikTok keyword search 0.50; YouTube comments and the check of V7's videos 0.49 | 4.28 (final run charges) | 16.33 (Apify's meter) |
| 19 Oct | Versions 27 and 28: the keyword scraper comparison and checks 0.33, the transcript test 0.02, follower counts 0.40, speech 0.98 | 1.73 | 18.14 (Apify's meter) |
| 19 Oct | Version 29, the Instagram gaps (DECISIONS #139–142): tests 0.55; more posts (Google by month, every tagged post, hashtags, keyword samples) 4.89; media links for reading pictures 1.97; speech 0.55; followers 0.25; comments under public posts 3.92 | 12.13 (final run charges) | 30.31 (Apify's meter; USD 100 limit) |
| 19 Oct | Version 30, Facebook (DECISIONS #143–148): tests 3.85; searches 4.58; reels, videos, groups and Google 2.63; by link 1.47; plays 0.57; speech 7.84; pages 2.01; comments 1.93 | 24.88 (final run charges) | 55.21 (Apify's meter; USD 100 limit) |
| 19 Oct | Version 31, Facebook reels and five post searches (DECISIONS #149–151): reel comparison 4.23; reel search 3.47 and fetch 0.67; scrapeforge and fetch_cat 4.76; filling the new posts 2.72 | 15.87 (Apify's meter) | 71.08 (Apify's meter; USD 100 limit) |

## 10. Raw data map (`data/raw/`)
| Folder | What's in it |
|---|---|
| `talabat/` | Photos and contact sheets (`img/`), brand rules v2 (`brands2.py`), the rebuild with photo labels (`rest_rebuild.py`, output `rest_v2.json`), area samples (`sample_listing.json`), menus (`menus_*.json`, `area_*.json`), Talabat's area names (`sitemap.html`), branch areas from menu pages (`menu_area.json`, `shoparea.json`), final restaurant records (`rest_final.json`), and the scripts that built them |
| `stores/competitors_5oct/` | Amazon, Carrefour and Noon competitor pulls |
| `stores/noon_tests_5oct/` | Noon ratings, popularity rank and stock tests |
| `stores/first_tests_4oct/` | First Amazon, Carrefour, Noon, Jumia and Google Trends tests |
| `verify_5oct/` | 5 Oct checks that each dashboard feature can be filled from real data |
| `google_trends/` | Direct Trends client and the pulled series (`final.json`, `related.json`) |
| `social/location_tests_4oct/` | Location fields per platform; includes the `#v7egypt` Instagram test |
| `social/governorate_test_4oct/` | 114 real posts and their labels |
| `social/reddit_quora_4oct/` | Reddit RSS and Quora results |
| `social/hashtag_test_5oct/` | `#اشرب_اي` on Instagram and TikTok |
| `verify_13oct/` | Review checks (13 Oct): Facebook comment replies (V7Egypt answers next day), Instagram comments (no replies returned), V7's 5 latest TikTok videos and 90 comments, X this week (`run.py`). Deeper pass: `own_pull.py` (Instagram profiles of V7 Egypt, the 4 pages abroad and the UK distributor; V7Egypt's 15 Facebook posts; 10 TikTok videos; YouTube channel), `own_pull2.py` (YouTube likes and dates, page followers and ad status, the first V Orange comments), and `build_own_posts.py --inject`, which writes the dashboard's `REAL_OWN` and `REAL_OWN_X` blocks |
| `media_13oct/` | The cover image of 183 real posts (`fetch_media.py`, 360 px JPEGs in `img/`, `index.json`) and `build_media.py --inject`, which writes the dashboard's MEDIA block |
| `own_backfill_13oct/` | V7 Egypt's older posts back to 16 Apr (`pull.py test|full`: Facebook and TikTok with date filters, Instagram 45 latest, YouTube channel) and `yt_pages.py` (exact dates and likes from the videos' public pages). Merged by `../verify_13oct/build_own_posts.py` |
| `social/rumors_11oct/` | Rumors & attacks, real. Raw pulls (`x_*`, `fb_*`, `ig_v7`, `tt_rumor`, `x_coke2024`), `collect.py` (full / extra / test), `run.log`, `normalize.py` → `posts.json` (368 unique), `labels.json` (177 posts about V7, labelled by Claude on 11 Oct), `build_rumors.py` → `rumors_dashboard.json` and the dashboard's `RUMOR_DATA` block |
| `real_17oct/` | The real social data since Version 25: `PLAN.md`, `collect.py` (every stage), `normalize.py` → `items.json`, `label.py` → `labels.json`, `vis_media.py` and `vis_read.py` (pictures → `vis_read.json`), `build_real.py --inject`, `fetch_media.py`, `scrapers_report.py` → `SCRAPERS.md`, `KEYWORD_SCRAPERS.md` (Instagram), `fbtest_report.py` → `FB_KEYWORD_SCRAPERS.md` (Facebook), `run.log`. `raw/`, `items.json`, `labels.json`, `vis/` and `vis_read.json` name or show private people and stay on this machine (git-ignored) |
| `apify_actor_pages/` | Apify Store pages for the actors we considered |

Scripts in `data/raw/*` were written to run from the old temporary folder, so paths may need adjusting before rerunning.

## 11. Open items
**V7 marketing team feedback (email, received 15 Oct 2026, shared as a phone screenshot; the first line and the end are cut off)**
- The first line seems to mention a kickoff at the beginning of January, "as agreed".
- Their points for the development phase:
  1. **Posts:** show the actual posts and their content inside the posts section, not links only. Make the interface more visually intuitive and easier to follow, with clear, actionable views.
  2. **Alerts:** send critical alerts immediately by email and mobile notification for severe or escalating issues, rumors and reputational risks. Include the relevant details and recommended actions.
  3. **Daily report:** an automated daily executive summary of V7's brand health. It covers total mentions; positive, negative, neutral and **mixed** sentiment; red flags and emerging issues; positive brand signals; **new UGC worth amplifying**; and recommended actions.
  4. **Competitors:** a clear overview of the main competitors, **Pepsi and Schweppes**: their brand sentiment, key conversations, … (cut off), summarized in a similar executive report.
- Status: points 1–3 are built in the demo (Version 23). **Point 4 (competitors) is on hold** at the user's request (DECISIONS #98).
- To agree with the team:
  - who receives alerts and the daily brief on Telegram (the channel is Telegram, DECISIONS #105);
  - the brief's time and language (Arabic, English or both);
  - what counts as critical for them, and how fast they want to respond;
  - their policy for reposting customers' content.

**Waiting on the user**
- Push Version 31 to the public site (needs the user's OK).
- Keep the real data fresh: USD 28.92 is left under the USD 100 limit until 15 Nov (above USD 19 is overage). A weekly refresh of new posts and comments (`collect.py` with a later `SINCE`, plus `igkw --since`, `igcomments`, `igvisfetch`, then `vis_media.py`, `vis_read.py`, `normalize.py`, `label.py`, `build_real.py --inject`) costs roughly USD 2 to 4 now that Instagram comments and pictures are included. Anything on a schedule needs the user's OK.
- Gaps left on 18 Oct: the posts tagging @v7egypt before 19 Jun and the Instagram spellings were closed in Version 29. Still open: 2 of the 10 TikTok keywords (فيسفن, V7 drink; about USD 0.15).
- Offered, not built: speech to text and picture reading for TikTok and YouTube (Instagram and Facebook so far); comments under public TikTok posts. Facebook reels are still under-covered (about 192 of perhaps 500, Version 31). The page is 14.2 MB, near the 16 MB limit: trim images before it grows.
- Done in Version 27: likes hidden by their owner now say "likes hidden" (37 Instagram posts).
- Done in Version 28: what's said in Instagram reels is read with the caption (146 reels), and Instagram accounts have follower counts (174 of 175).
- Not done: TikTok's own subtitles (74 of 96 videos about V7, free to download) and YouTube subtitles (about USD 0.03) could be read the same way.
- Instagram is not complete (19 Oct check):
  - Coverage: 262 of the 283 posts about V7 were found by one method only. For 19 Jun to 16 Oct the tagged list found 144, the keyword search 65, and both 21: a rough capture-recapture estimate of about 445 posts, and we have 229, so roughly half.
  - Sentiment: 54 of 169 reels have no usable speech, and on-screen text and text in 114 photos and albums aren't read. The 4,115 comments under these public posts aren't collected (about USD 9.50 with the comment scraper). Claude's labels haven't been checked against a person's.
  - Never available: hidden likes (37), most shares (135), private accounts, Stories, deleted posts.
  - Closest to complete: V7's own Instagram Business account through Meta's API: every post that tags V7 (`/tags`) and every caption that @mentions it (the mentions webhook), free once connected (`.env.meta`). Also weekly runs, since search results shuffle, and a spot-check of 50 labels by a person.
- Daily views (DECISIONS #126): a daily check of each post's totals, so each day shows the views added that day. About USD 0.10 a day for posts from the last 30 days. Not built; it needs the user's OK to schedule.
- Share the bot's join link with the team when ready.
- Keep the bot running when this app or machine restarts: the systemd user service in `bot/`, or the VPS later. Both need the user's OK.
- Add an Anthropic API key for the store check (Noon is now read by Claude). Save it in `.env.anthropic` as `ANTHROPIC_API_KEY=...`; never paste it in chat. Then do one live run of `data/noon_llm.py`, measure the real cost, and update the cost calculator's store-check price if it differs.
- Schedule the daily store check? It needs a paid Apify plan, at about USD 0.28 a day with competitors (Claude included).
- Which hashtags does V7 use for campaigns? `#اشرب_اي` returned nothing about V7, so we need the exact spelling or the source.
- Hosting choice and timeline.
- Add the collaborator to the repo: GitHub → mohanadabouserie/v7-pulse → Settings → Collaborators. The user does this; we need the collaborator's GitHub username to do it for them.
- From the rumors check, for V7:
  - confirm whether the fruit flavours contain sugar or honey;
  - send newsrooms the right brand name ("Seven Cola" appeared in the factory news);
  - publish a recommended price;
  - say when and where V Orange will be sold (people are asking under the launch post);
  - check V7 Uzbekistan's "0% sugar" claim, and V7_UK's page, quiet since 3 Sep.
- Which setup to budget for: questions a day and refresh rate, using the cost calculator.
- Update the proposal page's cost box? `V7_Pulse_Proposal.html` still shows the 3 Oct estimate of USD 60 to 130 a month. The lean setup (USD 75 a month) fits that range. The recommended setup (USD 208) is higher because it adds daily store checks, a monthly full Talabat check and 20 Opus questions a day.

**Questions for V7**
- Official price.
- Malt is alcohol-free.
- Giveaway policy.
- Product list and launch dates.
- Country pages and export markets.
- Monthly sales by product, even as an index.
- Read-only Meta Business access, and TikTok Business access.
  - 6 Oct: the user asked how to get a Meta Page token; the steps were given.
  - Next: when a token is saved in `.env.meta`, test with tiny read-only calls which Page and Instagram metrics still work (`page_views_total`, follower city and age, comments and reply times).

**Not built yet**
- Social share of voice against competitors (competitors exist only in the Market tabs).
- Hashtag watchlist search.
- Full Talabat coverage.
- X replies.
- Hosted backend.
