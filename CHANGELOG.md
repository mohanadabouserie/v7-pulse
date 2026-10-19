# V7 Pulse: changelog

Newest at the bottom. Dashboard versions are the published artifact's version numbers (https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc). Saved copies of versions 3 to 13 are in `archive/dashboard_versions/` (each saved before the next edit).

## 3 Oct 2026: research, first tests, proposal, dashboard versions 1 to 3
- **Research:**
  - Feature ideas beyond sentiment and chat.
  - How Apify works.
  - Alternatives compared: Bright Data, Phantombuster, ScraperAPI/Zyte, official APIs, self-hosted Crawlee/Playwright and listening tools. Firecrawl is useful only for news and websites.
- **Apify connected:**
  - Free plan, USD 5 a month.
  - The token is stored in `.env.apify` and `.gitignore` was added.
- **First real pulls (USD 0.021 in total):**
  - 3 posts from the V7Egypt Facebook page (apify/facebook-posts-scraper);
  - 3 posts from @v7egypt on Instagram (apify/instagram-post-scraper);
  - a Facebook keyword search for "V7 Cream Soda" (scraper_one/facebook-posts-search). It found Mon3esh's post with 7,444 reactions, and 2 of the 3 results were noise.
- **Proposal page:** `V7_Pulse_Proposal.html` (artifact 5vu6KEfGcuAqHi6j9M1b2g).
  - The "Tested" box was removed.
  - The sidebar buttons were made clickable.
- **Dashboard Version 1:** `V7_Pulse_Dashboard.html`, the real dashboard with demo data and no competitors. Tabs: Overview, All posts, Products, Customer voice, People, Groups, Hashtags, Our content, Alerts. A product filter works across every tab.
- **Version 2:** Outside Egypt tab, with export facts from online research (48 countries, exports tripled in 2024, a UK supplier). The product list was corrected, and sorting and labels were fixed after a review as the marketing manager.
- **Version 3:** Rumors & attacks tab with the fact sheet, campaigns, coordination score, risk, suggested replies and actions.

## 4 Oct 2026: research and the proposal email
- Explained how to send the dashboard file, and that the published link is private.
- **Profile visits research:** they're available only from V7's own insights (Instagram `profile_views`, Facebook `page_views_total`, TikTok by export).
- **Proposal email:** drafted, revised three times from the user's feedback, and sent to the user's AUC address. Subject: "Proposal: a social listening dashboard for V7".
- **Location research and tests (USD 0.13):** location fields checked on every platform.
- **Governorate test:** 114 real posts read as the LLM would. A governorate was found for 14 of the 45 Egypt consumer posts.
- **Paid Apify plans don't unlock governorate.** They add only X's "based in" and Instagram's about-account country.
- **E-commerce tests (USD 0.26):**
  - Amazon.eg, Carrefour and Noon work.
  - Talabat gives restaurants only.
  - Jumia has no V7.
  - Malt isn't new, and 3 products were missing from the list.
- **Amazon sales ranks found** (V Cola Diet is #1 in Cola) and a first Google Trends test run.
- **Reddit and Quora investigated:** Reddit through RSS only, Quora skipped. Google News RSS and the YouTube API are free sources.

## 5 Oct 2026
### Version 4
- **Added:**
  - Reddit as a platform, with 2 real Cream Soda reviews;
  - Online stores tab (real, collected 4 Oct);
  - Search trends tab (real Google Trends).
- **Removed** because it can't be obtained: city and governorate splits, commenter country, private groups, and hidden metrics.
- **Real data added:** the 12-product range, Benefit as the owner, real follower counts, and the 4 real V7 pages abroad.
- Apify spend: USD 1.41.

### Version 5
- **Reach and views:**
  - Posts are sorted by reach.
  - Views and engagement count on the day they happen.
- **Our content:** profile visits added.
- **Events tab:** suggestions wait for approval, and the team can add events.
- **Overview:** "Accounts posting" removed.
- **New switches:** UGC / BGC / All, and Posts / Comments / Both.
- Follower city and age, and reply rate and reply time, added (demo until Meta access).

### Version 6
- Removed the "Pepsi 8 · 7UP 3 …" line.
- The usage limit was hit partway through.
- Apify spend: USD 1.66.

### Version 7
- **Restaurants tab:** 546 real Talabat menus from 10 Cairo areas, with shares by company.
- **Online stores:** competitor include/exclude switch.
- **Ask V7 Pulse:**
  - Claude answers through the `sample` capability, with 8 read-only tools and suggestion cards for web searches and Apify runs.
  - The hosted package was written in `Ask_V7_Pulse/`.
- Apify spend: USD 2.80.

### Version 8
- **Online stores:**
  - Noon ratings, with an Amazon / Noon / Both selector.
  - Stock monitoring.
  - Rankings and history (real from 4 Oct; `data/store_history/`, `data/collect_store_history.py`).
- **Search trends:** company series merged and noise removed; product searches with spelling variants; pulled directly from Google Trends.
- **Date filter:** custom from–to dates.
- Apify spend: USD 3.22.

### Version 9
- **Copy pass so nothing reads as AI-written:**
  - No "AI" in the interface; no greetings or prototype notes; costs removed from Restaurants.
  - The English demo posts were made casual.
  - A voice rule was added to Ask V7 Pulse and `Ask_V7_Pulse/system_prompt.md`.
- Two stale "Noon shows no stock" notes were fixed.
- Broken "all flavors" captions on V7's own posts were fixed.

### Version 10
- Removed "Split by spelling" from Search trends: one company line, and one row in the terms table.

### Version 11
- **Restaurant links fixed:** they now use Talabat's menu URL format (the old links gave "Page Not Found").
- **Restaurant location:**
  - The area under each name is now the branch's own area from Talabat's menu pages (222 restaurants, read directly, no Apify).
  - The area filter is labelled "delivery areas".
- **Show less:** every "Show all" (tables, post lists, rumor campaigns, governorates) now has "Show less", and the list stays on screen when it collapses.
- **Products:** the detail panel opens on the most-discussed product instead of always on Cream Soda, and says it shows one product at a time.

### Project records
- **Hashtag test (USD 0.022):**
  - `#اشرب_اي` returned nothing about V7 (Instagram: no public posts; TikTok: 5 unrelated videos).
  - The earlier `#v7egypt` test (4 Oct) gave 5 of 5 posts about V7.
  - Apify spend: USD 3.24.
- **Tracking files created:** `CLAUDE.md`, `PROJECT_MEMORY.md`, `DECISIONS.md`, `CHANGELOG.md`.
- **Copied from the temporary session folder into the project:**
  - raw data → `data/raw/`;
  - scripts → `scripts/`;
  - tests → `tests/`;
  - dashboard versions 3 to 11 → `archive/dashboard_versions/`.

### Version 12
- **Restaurant links:** re-checked after the user asked. All 222 links in the two tables use Talabat's menu format, every one returned its menu page, and 20 of 20 random links opened the menu in a real browser.
- **Brand detection rebuilt** (`data/raw/talabat/brands2.py`, `rest_rebuild.py`):
  - **Descriptions:** brands are now read in item names and descriptions, so meal deals count. 114 V7 items were named only in descriptions, for example "1 republic + 1 v.cola + 1 coleslaw".
  - **More spellings:** V-Seven, V DIET COLA, V Soda, Fi/Fay Cola, Papsi, Pepesi, Coka, Sprit, Miranda and Big-Cola.
  - **New local brands:** Maxi Cola and Green Cola.
- **Photos checked by eye** against official can photos from Amazon and Noon:
  - 36 V7 items with an unclear flavour, 160 generic soft-drink photos ("Soft drink", "Cans", "مشروب غازي"…) and 52 unbranded "Cola" photos.
  - Photos only count when they show one company's products.
  - Contact sheets and photos are in `data/raw/talabat/img/`.
- **"V7 Lemon" fixed:**
  - Menus use the name for two products: 9 photos show V Lemon (Lemon-Lime) and 4 show Lemon Mint.
  - "Flavour not named" fell from 14 restaurants to 0.
  - "V7 Diet" with a 7UP Free photo is counted as 7UP, and "7UP Super Soda Diet Cola" with a V Cola Diet photo as V Cola Diet.
  - The "V 7" item described as coffee shows three V7 cans, and "Boba V7" is made with V7 Blueberry. Both now count; the coffee/boba exclusion was removed.
- **New numbers (546 menus):**

  | | Before | After |
  |---|---|---|
  | V7 | 12% (67 restaurants) | 16% (85) |
  | Coca-Cola Co. | 15% (83) | 21% (112) |
  | PepsiCo | 21% (113) | 26% (140) |
  | V7 with no rival | 47 | 56 |
  | Most visible restaurants with V7 | 26% | 33% (Coca-Cola 33%, PepsiCo 32%) |
  | V7 median menu price | EGP 35 | EGP 32 (Pepsi 35, Coca-Cola 40) |
- **Wording:** method notes, Help and the assistant's restaurant tool text updated. A stale "47 restaurants" example was removed from the assistant's rules.

### Version 13
- **Search trends, total only:**
  - Removed the "Noise removed" and "V Cola share" tiles, the "Searches by product" chart and the product rows of the terms table.
  - Removed the "Removed as noise" list and every noise percentage, including in the built-in answer, the assistant's tool and Help.
  - The product series and noise data were deleted from the page.
- **Search trends, governorates checked:**
  - "في سفن" is about 2% of company searches, and its map doesn't match the "سفن" (ships) map (rank agreement 0.09).
  - English "v7" and the V Cola spellings rank governorates alike (0.68), and a repeat pull gave identical ranks.
  - The map now says it shows V7's share of each governorate's searches (not counts), that Matrouh includes the North Coast, and that no bar means too few searches.
- **Restaurants:**
  - **Al Dahan:** its "V DIET COLA" had already been fixed in Version 12, and the live Talabat menu matches our data.
  - **A loose review of every menu** found "V Lemon" (6), "V Lemon Lime" (2), "V Pineapple" and "V barley drink" (Apple Malt). They're now matched: Lemon-Lime 10 → 11, Pineapple 4 → 5, Apple Malt 2 → 3.
  - **Cuisine groups now use the restaurant's main (first-listed) cuisine.** 132 restaurants moved; for example, Al Dahan moved from "Burgers & fried chicken" to "Egyptian & grills".
  - **Completeness:** 30 random scraped menus against Talabat's live pages all found the same drink brands.
  - **Blind spot:** in 4 restaurants, the brand behind a generic "Soft drink" item is hidden in options we can't see.
- **Tests:** now run from `tests/`. `test_v13.py` added and `test_v8.py` updated.

### Version 14: Online stores redesign
Reviewed as V7's marketing manager and as a UI/UX reviewer. The old default view was 5,076 px and 1,639 words, with competitor numbers crammed into every tile, three panels repeating the same prices, and competitor rows outnumbering V7's.

- **New sub-tabs:** Summary (default) · Prices · Sales & ranks · Stock · Ratings.
- **Summary** (1,368 px, about 430 words, with competitors on):
  - 4 V7 tiles: Amazon sales, best-seller rank, shelf price, rating.
  - **Needs attention:** real issues at the latest check, each with a next step. Noon pricing, Piña Colada low on Noon, Apple Malt sold only in 3-packs, and missing listings.
  - **Where V7 is sold:** products × stores, price with a stock dot, red when above EGP 15.
  - **Against competitors:** V7 vs PepsiCo vs Coca-Cola on sales, top-20 places, rating and price per 100 ml, with a computed takeaway.
- **Prices:** one drink type at a time in the per-100-ml chart. The can-price table shows V7 and the 8 main rival brands, with 9 more on demand. The V7 price detail opens on demand.
- **Sales & ranks:** "What sells on Amazon.eg" (top 10, then show all), the top 20 as a company bar with V7's places, and ranks over time with the Amazon/Noon switch. Competitor rows open on demand.
- **Stock and Ratings:** V7 listings first, and competitor listings open on demand. Stars are a column in the ratings table, and each store notes what isn't listed there.
- **Phone:** both Summary tables fit a 390 px screen. Checked at 390, 820 and 1440 px and in dark mode.
- **Fixed:** the top-20 chip for #5 now says Pineapple Malt (it read "V7 pineapple").
- **Tests:** `tests/test_v14.py` added (21 checks). `test_v8.py` and `test_market.py` updated for the new layout.

## 6 Oct 2026
- **Sharing question:** a viewer of the shared dashboard saw hashtags and other data missing. It was resolved with no change to the page. Notes on what to check are in `PROJECT_MEMORY.md`, section 2.
- **Meta access token:**
  - Gave the steps for a Page token, and detailed steps for a system-user token in Meta Business Settings (option B).
  - `CLAUDE.md` now says the token goes in `.env.meta` and must never be printed or put in the dashboard.
- **Cost calculator:** new page `V7_Pulse_Costs.html`, published privately at https://claude.ai/artifact/7W1HvsWL1brdpe7eNxEx4P (Version 1).
  - **Costs it covers:**
    - Fixed costs, on yearly plans: Hostinger VPS, .com domain, Apify plan.
    - Variable costs: Claude for answers, for reading posts and comments, and for analysis runs, plus Apify data collection above what the plan includes.
  - **Controls:**
    - questions a day, the Claude model and the share of questions that search the web;
    - social refresh rate, store checks, and the Talabat check and its coverage;
    - analysis runs, and posts and comments a day;
    - VPS plan, Apify plan (or the cheapest plan that fits), domain, other fixed costs and the EGP rate.
    - Advanced assumptions (tokens per answer, Apify prices per 1,000 results, noise share) can be edited.
  - **Presets:**

    | Preset | Year one (USD) | Notes |
    |---|---|---|
    | Lean | 902 | |
    | Recommended | 2,497 | EGP 130,573, about USD 208 a month, USD 2,569 from year two when hosting renews |
    | Heavy | 11,792 | |

  - **Recommended, line by line (USD a year):**

    | Line | USD |
    |---|---|
    | Hosting (KVM 2) | 108 |
    | Domain | 20 |
    | Apify Starter | 204 |
    | Answers | 1,228 |
    | Reading posts and comments | 86 |
    | Analysis runs | 122 |
    | Data collection above the plan | 728 |
    | **Fixed** | **332** |
    | **Variable** | **2,165** |

  - **The two big levers:**
    - Refreshing social media every hour instead of every 6 hours adds about USD 3,040 a year.
    - Sonnet 5 instead of Opus 5 for answers and analysis saves about USD 793.
  - **Prices (checked 6 Oct 2026):**
    - Hostinger KVM 1, 2 and 4 cost USD 6.49, 8.99 and 12.99 a month on a yearly plan. They renew at 11.99, 14.99 and 28.99.
    - A .com domain is USD 19.99 a year.
    - Apify Starter is USD 17 a month and Scale USD 179 a month, billed yearly.
    - Claude per million input/output tokens: Opus 5 USD 5/25, Opus 5.5 4/20, Sonnet 5 2/10, Haiku 4.5 1/5. Web search is USD 10 per 1,000 searches.
    - USD 1 = EGP 52.3.
  - **Checked:** at 1440 px and 390 px, in light and dark, with no script errors.
- **Hosted package (`Ask_V7_Pulse/`):**
  - `tools.json`: the web tools are now `web_search_20260209` and `web_fetch_20260209`, the current documented versions. `20260318` isn't a listed version.
  - `README.md`:
    - The default model is now `claude-opus-5`, at about USD 0.17 a question.
    - `claude-opus-5-5` is listed as the newer, cheaper-per-token option.
    - `claude-sonnet-5` is the cheaper option for everyday answers, at about USD 0.07 a question.
    - The sample code and tool names were updated to match.
- **Cost calculator Version 2: analysis runs get their own Claude model** (user request). Version 1 is saved in `archive/costs_versions/`.
  - **New control:** "Claude model for analysis runs" under "Analysis runs per day". Before, analysis runs used the answers model.
  - **Presets unchanged:** Lean USD 902, Recommended USD 2,497 and Heavy USD 11,792. Lean uses Sonnet 5 for analysis; Recommended and Heavy use Opus 5.
  - **What-if table:** it's now "If the Claude model changes", with one column for answers and one for analysis. Each cell shows the change to the year-one total, and the current pick is highlighted. For Recommended, Sonnet 5 saves about USD 719 on answers and USD 73 on analysis.
  - **Per unit:** a new "One analysis run" card (USD 0.168 on Opus 5, 0.067 on Sonnet 5). The answer card is now labelled "One question" so it fits on a phone. The cards are 4 across on wide screens and 2 across otherwise.
  - **Saved settings:** settings saved before this change keep analysis on the answers model they had.
  - **Tests:** new `tests/test_costs.py` (25 checks: presets, the analysis model, saved settings, and 390, 820 and 1100 px in USD and EGP). All pass.
- **Cost calculator Version 3: all Claude model choices in one panel** (user request). Version 2 is saved in `archive/costs_versions/`.
  - **New "Claude models" panel** (after "How much people talk about V7") with three pickers: Ask V7 Pulse answers, Analysis runs, and Reading posts and comments. The reading model and "Read in batches" checkbox moved up from the assumptions; the answers and analysis pickers moved here from their panels.
  - **Choices:** every picker offers Opus 5, Opus 5.5, Sonnet 5 and Haiku 4.5. Before, reading offered only Haiku 4.5 and Sonnet 5. Prices are stated once, per million input / output tokens.
  - **Batches:** the help line says most batches finish within an hour and the limit is 24 hours, per Anthropic's Batch API docs.
  - **Presets** now set the reading model (Haiku 4.5) and batches (on). Their totals are unchanged.
  - **What-if table:** a Reading column was added. The cells drop the currency sign so four columns fit a phone, and the caption names the currency. On Recommended, reading on Opus 5 would add USD 344 and on Sonnet 5 USD 86.
  - **Order:** the variable cost lines and the per-unit cards follow the picker order (answers, analysis, reading).
  - **Tests:** `tests/test_costs.py` now has 39 checks, including the Heavy preset in EGP at 390 px. All pass.

## 7 Oct 2026
- **GitHub Pages copy of the cost calculator prepared, not hosted yet.**
  - `deploy/build_costs_site.py` builds `deploy/v7-pulse-costs/index.html` from `V7_Pulse_Costs.html`. It adds the page skeleton that the artifact viewer normally supplies (doctype, UTF-8, mobile viewport) and a `noindex, nofollow` tag.
  - Why the skeleton matters: on a phone, the raw file renders in quirks mode at 980 px wide. The built copy renders at 390 px in standards mode.
  - `tests/test_costs.py` can now target the hosted copy with `COSTS_SRC=...`. All 39 checks pass on it.
  - Not hosted yet:
    - this session has no GitHub connector (only Claude Docs, Gmail, visualize);
    - `gh` isn't installed;
    - git has no GitHub credentials.
  - The user was given two routes: install `gh` and sign in so Claude can create the repo and turn on Pages, or upload the file on github.com.
- **Cost calculator hosted on GitHub Pages (public):** https://mohanadabouserie.github.io/v7-pulse-costs/
  - **Set-up:** the user installed `gh` (2.45.0, from Ubuntu's packages) and signed in as `mohanadabouserie`; the login is kept in the system keyring.
  - **Repo:** https://github.com/mohanadabouserie/v7-pulse-costs (public). It holds only `index.html` and `.nojekyll`, first commit `0ca61f1`.
  - **Pages:** served from `main`, at the root, with HTTPS enforced.
  - **Checked on the live site:**
    - the file served is identical to `deploy/v7-pulse-costs/index.html`;
    - all 39 checks in `tests/test_costs.py` pass;
    - phone emulation shows standards mode at 390 px, fonts loaded and no errors.
- **Dashboard copy for GitHub Pages prepared, not published yet** (user asked to host the dashboard too).
  - **Build script:** `deploy/build_sites.py` replaces `deploy/build_costs_site.py` and builds both pages (`costs`, `dashboard`, or both). The calculator's output is byte-for-byte unchanged.
  - **Dashboard copy:** `deploy/v7-pulse/index.html`. It adds the doctype, charset, viewport and `noindex`. The dashboard already has its own `[hidden]` rule.
  - **Chat line:** the public copy says "Short built-in answers. Full answers from Claude aren’t available in this copy." instead of telling visitors to open it in claude.ai. The `sample` capability only exists inside claude.ai.
  - **Checked:**
    - all 8 dashboard test suites pass on the copy;
    - on a phone, all 15 tabs fit 390 px in standards mode (the raw file would render at 980 px);
    - the chat answers with built-in answers and no errors.
  - **Waiting on the user:** whether to publish it publicly, given that the demo rumors include made-up claims about V7 (for example "V7 is unsafe and made people sick") and the demo label is a small badge.
- **Dashboard hosted on GitHub Pages, public, as it is** (the user chose this over adding a demo banner or keeping it private): https://mohanadabouserie.github.io/v7-pulse/
  - **Repo:** https://github.com/mohanadabouserie/v7-pulse (public). It holds only `index.html` and `.nojekyll`; first commit `e08290e`; served from `main`, at the root, with HTTPS enforced.
  - **Checked on the live site:**
    - the file served is identical to `deploy/v7-pulse/index.html`;
    - all 8 dashboard test suites pass against the live address;
    - on a phone, all 15 tabs fit 390 px in standards mode, fonts load and there are no errors.

### Version 15: V7 brand redesign (7 Oct 2026)
The user didn't like the old look and asked for V7's theme, with research into best practices.

- **Research:**
  - V7's site (v7-benefits.com): green `#0A7F40`, Avenir, uppercase headlines, green pill buttons.
  - Can colors per flavor, sampled from the official can images and the retail photos in `data/raw/talabat/img/ref/`.
  - V Cola's navy, silver and gold.
  - NN/g's dashboard guidance, dashboard UX guides, and how Sprout Social organizes listening screens.
- **Audit of Version 14:**
  - nothing looked like V7;
  - monospace type everywhere;
  - positive-sentiment blue matched PepsiCo blue;
  - all KPIs had equal weight, with "What changed" in a side column;
  - three rows of mixed filter controls filled a phone's first screen;
  - the sidebar note was clipped at 900 px.
- **Direction:** A (V7 green master brand) chosen by the user over B (V Cola navy), from side-by-side mockups.
- **Changes:**
  - **Color tokens for light and dark:**
    - V7 green for the brand and good news, a deeper green sidebar, V Cola navy for quantities and Super Soda gold for events;
    - green / grey / red sentiment, and V7 green vs PepsiCo blue vs Coca-Cola red;
    - a deep forest-green dark mode.
    - Every text pair was checked to WCAG AA. Two fixes came out of that: a deeper sidebar `#08703A` and a lighter green tint.
  - **Type:** Nunito Sans (the closest free match to Avenir) with IBM Plex Sans Arabic; the monospace font is gone. Page titles are uppercase in the 900 weight; labels are uppercase in 800.
  - **Product colors:** each product has its can color (`PRODUCTS[].c`). A dot appears next to product names in chips, the product filter, product lists, the People table and the product details title. Product cards have a can-color strip.
  - **Shapes:** pill buttons, chips and badges; 16 px cards; quieter segmented controls (grey track, white selected pill with green text); deltas as tinted pills.
  - **Sidebar:** green with a white pill for the current tab and a new "pulse V" logo mark. It's regrouped into Conversation, **To act on** (Alerts, Rumors & attacks, Events), Market and International. It now fits a 900 px screen.
  - **Overview:** "What changed this period" comes first, on the left next to the daily chart, and the rumor line has a red edge. Sparklines and line charts are navy.
  - **Phones:** the filters fold behind a Filters button (with a dot when they differ from the defaults), so the KPIs show in the first screen. The help button is icon-only there.
  - **Copy:** "Blue leans positive" became "Green leans positive".
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 14 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v14.html`);
  - new `DESIGN.md` (the design system) and `tests/test_v15.py` (30 checks);
  - `tests/test_v5.py` and `tests/test_v11.py` now find the chart panel and product title by content, not position.
- **Checks:** all 9 dashboard test suites pass. Every tab was reviewed at 1440 px, in dark mode and at 390 px, with no script errors.
- **Published:** to the same artifact as Version 15. The public GitHub Pages copy still shows Version 14 until the user OKs a push.
- **Version 15 pushed to the public GitHub Pages copy** (user OK, 7 Oct): https://mohanadabouserie.github.io/v7-pulse/, commit `9cf4de4`.
  - Before pushing, all 9 dashboard test suites passed on the built copy.
  - After the push, the live file is identical to `deploy/v7-pulse/index.html`.
  - Against the live site, `test_v15`, `test_v14` and `test_reg5` pass.
  - A phone check of the live site shows standards mode at 390 px, fonts loaded, the green sidebar, the Filters button, KPIs from 191 px, and no errors.

## 11 Oct 2026
- **Noon scraper replaced with a Claude call** (user request: "noon scraper is not working anymore").
  - **Cause:**
    - `crawlerbros/noon-scraper` returns 404 "Actor was not found" on Apify, so it was removed from the Store.
    - The account's last Noon runs (5 Oct) had succeeded.
    - The ratings actor (scrapesmith) still exists and is used.
  - **New `data/noon_llm.py`:**
    - curl fetches Noon's Soft Drinks page sorted by popularity. Plain Python requests hang on Noon; HTTP/2 works.
    - The page is reduced to visible text with a `[SKU ...]` marker per product: 38 products, about 18,000 characters.
    - Claude (`claude-opus-5-5`, effort low, JSON-schema output, `fallbacks: "default"`) returns SKU, name, price, rating, rating count and stock warning.
    - Each value is kept only if it appears in that product's own text. The price must be an "EGP x" figure, not the per-100 ml one. Rank is the page position, and unknown SKUs are dropped.
    - Refusals and cut-off answers stop the run. Each day's page and result are saved under `data/raw/stores/noon_llm/<date>/`.
  - **`data/collect_store_history.py`:**
    - Noon runs first, so a Claude problem stops the run before any Apify spend.
    - Star ratings come from the page. The ratings actor only covers gaps and tracked listings outside the top 20.
    - The snapshot's sources name Claude. The estimate went from about USD 0.30 to 0.28 a day.
  - **Environment:** the Anthropic SDK 1.13.0 is in a project environment, `data/.venv` (Ubuntu blocks system pip installs), which is added to `.gitignore`.
  - **Tests:** new `tests/test_noon_llm.py`, with 26 checks.
    - It runs the real SDK request path against a local stand-in for the API, on the real page saved in `data/raw/stores/noon_llm_tests/`.
    - It plants a made-up SKU, a per-100 ml price and an invented stock warning, and all three are caught.
    - It also checks the collector wiring with Apify stubbed. All checks pass.
  - **Not yet run live:** this machine has no Anthropic API key. Cost today: USD 0 (only free Apify status reads and two free page loads).

### Version 16: Online stores in plain words (11 Oct 2026)
The user found Stock ugly and hard to read, Ranks over time confusing, the Prices table and the Summary's "Where V7 is sold" table hard to understand. They also asked for rating rows, and the small "Over the period" charts, to open details.

- **Stock:**
  - The tab now opens with one sentence, for example "All 24 V7 listings can be bought right now. Running low: Piña Colada on Noon (Only 8 left)", plus the latest check date for each store.
  - Below it, a "Where each V7 flavour can be bought now" grid (products × stores) with pills: ✓ In stock, Low · 8 left, ✕ Out, Not sold here.
  - Then "Stock problems": only listings with out, low or not-listed days. Each row says what happened in words (for example "Out of stock 10 days · 19–28 Sep", with a demo tag) and has a slim day strip: in-stock days pale green, problems coloured, demo days lighter. A line counts the listings that were in stock every day. Competitor problems open on demand.
  - The 720-cell hatched grid and the tiles are gone.
- **Best-seller ranks** (replaces Ranks over time):
  - Columns: Rank now, Change since the start of the period, Best, Days at #1, and a rank line whose top is #1 (demo dashed, real solid).
  - Tiles: #1 right now, top 10, moved up or down.
  - Rows open a panel with the full daily chart, what the rank means, the category's current top products, and the listing link.
- **Ratings:** product rows (Enter works too) open a details panel with:
  - both stores, and Amazon's real star split with about how many people gave each star;
  - a callout when 1–2 star ratings are 10% or more;
  - a full "Ratings over the period" chart and new ratings per full week;
  - the rank among V7 products, and a comparison with other products in the category on Amazon;
  - links to the reviews or the Noon listing.
- **Prices:** "Can prices by store" is replaced by "<drink type>: price in each store", which follows the drink-type switch.
  - V7 comes first, then rivals ordered by price per 100 ml.
  - Each cell shows the price, size and per-100 ml price, and the cheapest store in each row is shaded.
  - The last column gives the lowest per-100 ml price and how it compares with V7 ("35% less than V7"). — means not listed.
- **Summary:** "Where V7 is sold" is now "V7 price and stock in each store".
  - Cells show "EGP 20" with "EGP 5 over shelf price" in red, "a can, sold as 3-pack", and stock in words only when low or out.
  - The dots are gone, and product names have can-colour dots.
  - On phones, the EGP prefix moves to the note and the pack text shortens.
- **Fix:** the stock strips and rating bars used the class `demo`, which the "Demo data" badge already styles. That's why the old grid cells had dashed borders and couldn't shrink; they now use `dm`.
- **Phone:** the Summary and Stock grids fit 390 px (Stock shows ✓ and — with a key). Wider data tables scroll inside their card, and the page never scrolls sideways.
- **Tests:** new `tests/test_v16.py` (21 checks). `test_v8.py` and `test_v14.py` were updated for the new layouts. All 10 suites pass.
- **Files:** `V7_Pulse_Dashboard.html` (Version 15 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v15.html`) and `DESIGN.md`. Published as artifact Version 16.
- **Not yet public:** the GitHub Pages copy still shows Version 15.

### Rumors data pull (11 Oct 2026)
For the user's request to fill Rumors & attacks with real data. Budget agreed: up to USD 1.50 on Apify; the posts are read and labelled by Claude in the chat (the user's choice), not through the API.
- **Searches** (`data/raw/social/rumors_11oct/collect.py`, cap USD 1.50, a cost cap on every run):
  - X (kaitoeasyapi tweet scraper): owner, quality, malt, price, giveaway and general V7 searches, 279 posts.
  - Facebook (scraper_one posts search): owner, Coca-Cola, quality, malt, giveaway and general searches, 87 posts.
  - Instagram (`#v7egypt` hashtag), 23 posts; TikTok (clockworks, rumor searches), 24 videos.
  - 413 posts in all, saved as `x_*.json`, `fb_*.json`, `ig_v7.json`, `tt_rumor.json`, with tiny test runs in `t_*.json` and the run log in `run.log`.
- **Cost:** about USD 0.47 by the run log. Apify's monthly usage now reads USD 3.83 of 5, up from 3.24 on 5 Oct.

### Version 17: stock in its own column (11 Oct 2026)
The user found price and stock in the same cells confusing.
- **Summary, "V7 price and stock in each store":**
  - The store columns show only the price: red when above the EGP 15 shelf price, with "EGP 5 over shelf price" and "a can, sold as 3-pack" under it.
  - A new last column, Stock, says "✓ In stock" or names each problem with its store ("Low on Noon · 8 left", "Out on Carrefour").
  - The table now spans the full width. "Needs attention" and "Against competitors" sit side by side above it, so each price note fits on one line.
- **Phones:** the Stock column is hidden and problems show under the product name, with the note "Everything is in stock unless a problem is shown under the product." Over-price notes shorten to "+5", and the can dot stays next to the name.
- **Fixes:** the phone rule for header padding also padded the product names (`.smx th span` is now `.smx thead th span`), and "3-pack" no longer breaks at the hyphen.
- **Tests:** `test_v14.py` reads the Stock column, and the Summary height limit is now 1,700 px (1,698 → 1,642 px after the layout change). `test_v16.py` has 3 new checks (stock column, prices alone in the store columns, phone lines). All 10 suites pass.
- **Files:** `V7_Pulse_Dashboard.html` (Version 16 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v16.html`, taken from the published artifact), `DESIGN.md`. Published as artifact Version 17.

### Version 18: Rumors & attacks from real posts (11 Oct 2026)
The user asked to pull real data and run the real backend for Rumors & attacks. The AI step was Claude in the chat (the user's choice), and the Apify budget was USD 1.50.
- **Second, targeted search:** X, 20 Apr to 25 May 2024, for the Coca-Cola sale story (`collect.py extra`, capped at USD 0.10). It returned only posts already found, plus the actor's filler rows. Those rows are now dropped in `normalize.py`.
- **Reading:** all 368 unique posts were read.
  - 177 are about V7. The rest are Haval V7 cars, the V7 climbing grade, software and crypto "v7", Toyota Corolla adverts, other brands' contests and Cambodia's V-Cola.
  - Labels are saved by post in `data/raw/social/rumors_11oct/labels.json`: claim, what the post does (spread, question, debunk), kind, sentiment and an English note.
- **What the posts show:**
  - **Price confusion, active:** 38 posts from Nov 2023 to 10 Oct 2026. 25 say shops charge EGP 17 to 26 (one restaurant charged 50). Some name an "official" price of EGP 8, 9.75 or 12. 5 ask the real price, and 8 give the right one. On 27 Jan 2026 Cairo 24 quoted V7 saying shops charging EGP 20 are individual traders. The top post had 149K views (Jul 2024).
  - **"V7 was sold to Coca-Cola", contained:** 2 to 4 May 2024. Cairo 24 covered it, the founder denied it on 3 May, and V7 issued a statement on 4 May. The posts that spread it weren't found.
  - **"V7 Malt tastes like alcohol", watching:** one joke, 23 Sep 2026.
  - **Also worth a look:** one post saying every V7 flavour is sugar-free (9.2K views, May 2024). News of the factory opening (11 May 2026) calls the brand "Seven Cola" (Mazid, 54.7K views). A UK dessert shop's TikTok, "5 reasons why you shouldn't buy V7 drinks" (Aug 2025).
  - **Not found:** fake V7 pages or giveaway scams, coordinated accounts (none of 40 X accounts was under 30 days old, no copied text), health or safety claims.
  - **Context:** 21 of the 177 posts name V7 as an Egyptian alternative to Pepsi and Coca-Cola. The most-viewed post, 408K views, says "Buy V Cola, it tastes better than Coca-Cola" (Apr 2024).
- **Backend:** `build_rumors.py` turns `posts.json` and `labels.json` into `rumors_dashboard.json`. With `--inject`, it writes the `RUMOR_DATA` block into the dashboard.
  - Private people are shown as "X user" and so on. Names are kept for news outlets, shops, creators and accounts with 10K+ followers.
  - Self-declared locations aren't used.
- **Dashboard:**
  - The Rumors page opens with a status sentence and five numbers from the real posts.
  - Then the claim cards. Status comes from the real dates: Active means posted about in the last 30 days, and Watching means only one or two posts. Risk uses reach, recent posts, how many repeat the claim, and harm.
  - The claim detail has a monthly or daily chart with V7's response, coordination checks from what each platform shows, who is posting, the most-viewed posts, the suggested reply and actions, and every post (newest first, with an English "In short" note).
  - New sections: "Also worth a look", "Nothing found", and "How the posts were found" (searches by platform, cost).
  - The date filters are hidden there (the posts span 2023 to 2026), and the header badge says Real data.
- **Demo rumors removed everywhere:** the five demo campaigns and their generated posts, the demo Coca-Cola event (ev8), and the "false campaign" wording.
  - Alerts now show "Price confusion" to watch and "No false rumors spreading".
  - The Overview has no rumor line, and the sidebar has no rumor count.
  - The built-in chat answer and the chat's data tool use the real claims.
- **Fact sheet:** ownership is now sourced to the founder's denial (Cairo 24, May 2024). The price fact adds V7's line that EGP 20 shops are individual traders.
- **Tests:** new `tests/test_v18.py` (23 checks). `test_v5.py` (events and filters) and `test_v15.py` (no rumor line) are updated. All 11 dashboard suites, `test_noon_llm.py` and `test_costs.py` pass.
- **Cost:** USD 0 more (the second search only returned posts already found). Apify's usage reads USD 3.84 of 5.
- **Files:** `V7_Pulse_Dashboard.html` (Version 17 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v17.html`). In `data/raw/social/rumors_11oct/`: `collect.py`, `normalize.py`, `labels.json`, `build_rumors.py`, `posts.json`, `rumors_dashboard.json`. Also `DESIGN.md`. Published as artifact Version 18.

### The whole project on GitHub (11 Oct 2026)
At the user's request, for a collaborator: everything is pushed to https://github.com/mohanadabouserie/v7-pulse (public), with a CLAUDE.md for other Claude sessions.
- **Repo:** the project folder is now a git repo on top of the existing Pages history (commits e08290e and 9cf4de4, then 922b6a7).
  - Included: the dashboard, calculator and proposal; `data/` (collectors and all raw data); `tests/`; `archive/`; `Ask_V7_Pulse/`; `scripts/`; the tracking files.
  - Not included (`.gitignore`): `.env.*`, `apify_key`, `data/.venv/`, test screenshots, the local Pages clones in `deploy/`, and `Reference docs/` (third-party PDFs).
  - A full secret scan found the Apify token only in the two ignored key files.
- **Public site:** GitHub Pages now serves `docs/` instead of the repo root. `deploy/build_sites.py dashboard` writes `docs/index.html` and `docs/.nojekyll`.
  - The switch was done in two pushes, so the site never went down.
  - The live copy now shows Version 18.
- **Path-independent:** tests find the dashboard relative to `tests/`. `DASH_SRC` (and `COSTS_SRC` for the calculator) runs them on a public copy.
- **CLAUDE.md** was rewritten for any Claude session: repository map, machine setup (Playwright, the venv, which `.env` files to create), code map, tests, publishing, data pipelines, secrets, known quirks. `README.md` was added.
- **Files:** `.gitignore`, `deploy/build_sites.py`, `tests/*.py` (source paths), `CLAUDE.md`, `README.md`, `docs/`.

### Old Pages clone removed (12 Oct 2026)
- At the user's request, the local folder `deploy/v7-pulse/` was deleted.
  - It was the old clone of the Pages repo, now replaced by `docs/` in this repo.
  - It had no unpushed commits or changes. Its last state (Version 15) is in the repo history (commit 9cf4de4).
- **Files:** `.gitignore` (its ignore line removed), `PROJECT_MEMORY.md`.

### Version 19: price and stock for each store (12 Oct 2026)
The user found the single Stock column confusing: with Amazon.eg, Carrefour and Noon in one table, it didn't say which store it meant.
- **Summary, "V7 price and stock in each store":** each store now has its own two columns, Price and Stock, under the store's name.
  - A ✓ means in stock at that store.
  - Low stock shows as a gold pill under that store ("8 left" under Noon for Piña Colada), and out of stock as "✕ Out".
  - When a store doesn't sell a product, one "—" spans both of its columns.
  - Thin lines separate the stores, and the key under the table adds "✓: in stock".
- **Phones:** unchanged from Version 17. Prices only; any stock problem is written under the product name with its store ("Low on Noon · 8 left").
- **Tests:** `test_v14.py` checks that the low pill sits in Noon's Stock column. `test_v16.py` checks the two header rows and one mark per listing (23 in stock, 1 low). All 11 dashboard suites pass.
- **Files:** `V7_Pulse_Dashboard.html` (Version 18 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v18.html`), `DESIGN.md`, `tests/test_v14.py`, `tests/test_v16.py`. Published as artifact Version 19.
- **Not yet public:** the GitHub copy (`docs/`) still shows Version 18.

### Version 20: page-by-page review, checked against real data (13 Oct 2026)
The user asked for an expert UI/UX pass over every page and element, with real Apify calls and Claude-in-chat reading to check that each thing can be filled, removing what can't be collected, is noise, or is misleading. Version 19 was pushed to the public site first (commit 7e77c42).
- **Checks run:** `data/raw/verify_13oct/run.py`, capped at USD 0.30. Apify charged USD 0.11 (TikTok's actor needs a USD 0.50 cap but charged cents).
  - **Facebook comments with replies** on V7's Cream Soda reel: V7Egypt answers comments, usually the next day (about 18 h, some within the hour). A follow-up asking for contact numbers and the nearest distributor (6 Oct) has no answer.
  - **Instagram comments:** the actor returns no replies, so the Instagram answer rate needs V7's own access.
  - **V7's TikTok:** the latest 5 videos (687 to 11.4M plays) and their 90 comments. Mostly flavour requests: watermelon (asked again and again), mango, mixed berry, a winter edition, iced coffee.
  - **X this week:** 2 of 20 results were about V7, one more "EGP 15 at the agency, 20 at the kiosk" post.
  - **Already on file and re-read:**
    - 50 real Facebook comments (4 Oct): praise, requests (sugar-free malt, peach, 1 L and 2 L bottles), 3 sales leads (fridges, distributor) and "can't reach V7".
    - The 5 Oct checks: a public Facebook group with 88K members posts about 790 times a day, so scraping groups to find V7 would cost about USD 4 a day per group.
    - Volumes from earlier pulls: about 1 to 2 public posts a day about V7.
  - **Web:** Meta retired Facebook page fan age, gender and city (2024 to Nov 2025; `page_follows_city` remains). Instagram still gives follower demographics and `online_followers` (last 30 days, 100+ followers).
- **Demo data recalibrated to what can be collected:**
  - Public posts went from about 33 a day to about 1.4 a day in Egypt (`pois(1.4×dayMult)`), and posts from abroad from about 7 a day to a few a month.
  - Posts and comments now show together by default ("Both"). About 97% of the conversation is comments under V7's own posts.
  - The comment mix and reply habits come from the real comments: replies are tracked on Facebook and YouTube only, answered about 65% of the time, mostly the next day. V7 thanks most Facebook praise.
  - Requests use the real asks: watermelon, mango, berries, sugar-free malt, bigger bottles. A new complaint, "Can't reach V7 (messages, complaints line)", is added. Sales leads include fridge requests.
  - Groups are rare in Facebook search results, so group posts are rare in the demo too. Most posts from abroad are businesses, and comments abroad are mostly from local people in the local language.
  - V7's own posts rotate through the range (weighted), so no product disappears by chance.
- **Removed:**
  - the Facebook groups tab and the "Facebook groups abroad" panel (group posts still show "in <group>");
  - emotion labels;
  - the "Words people use most" cloud, with the tab renamed Hashtags and generic tags (#fyp, #viral, #explore…) dropped;
  - Arabic dialect guesses (shown together as "Other Arabic");
  - "Core" badges (only Seasonal stays) and "Mentioned together with";
  - the "When your audience posts" heatmap;
  - the old social alert thresholds.
- **Changed:**
  - "Who follows us" is labelled as Instagram insights.
  - The heatmap is now "When our followers are online" (Instagram `online_followers`, demo until V7 connects).
  - "What people say under our posts" puts emoji-only comments and tags in one line.
  - A "Where it happens" split is added, and "Who posts publicly" counts posts only.
  - Changes under 10 show "+3", not a percentage. Net sentiment needs 5 or more items. "Biggest gain" shows a percentage only on a base of 10 or more.
  - Alerts:
    - "More public posts than usual" fires at 5 or more posts in a day and 3× the average.
    - "Negative day" needs 20 or more posts and comments and over 25% negative.
    - "Can't find it" counts comments too.
    - "Unanswered for a day" is on and flags questions waiting over a day.
  - The guide text is updated to match.
- **Real data added:** V7's four TikTok videos in the period (Summer of Colors, 11.4M plays) in Our posts. The Summer of Colors event mentions TikTok.
- **Tests:** new `tests/test_v20.py` (20 checks). `test_v5.py` (the day link opens posts and comments) and the view lists in `test_reg5.py`, `smoke5.py` and `copy_dump.py` are updated. All 12 suites pass.
- **Files:** `V7_Pulse_Dashboard.html` (Version 19 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v19.html`), `data/raw/verify_13oct/` (run.py, run.log, fb_replies, ig_replies, tt_profile, tt_comments, x_week), `DESIGN.md`, tests. Published as artifact Version 20.
- **Not yet public:** the GitHub copy shows Version 19.


### Version 21: the deeper pass, V7's own posts and V Orange (13 Oct 2026)
- **Why:** the user asked to dig deeper into the page-by-page review, checking each element against real data.
- **Real checks (Apify, capped; about USD 0.19, plus late charges from earlier runs; Apify reads USD 4.25 of 5):**
  - `data/raw/verify_13oct/own_pull.py`:
    - Instagram profiles of @v7egypt, the four V7 pages abroad and the UK distributor, with their 12 latest posts;
    - V7Egypt's 15 latest Facebook posts;
    - @v7.egypt's 10 latest TikTok videos;
    - the YouTube channel's 6 latest videos and 6 Shorts.
  - `own_pull2.py`:
    - YouTube likes and exact dates for those 12;
    - the Facebook page's follower count (79,783) and ad status ("isn't currently running ads");
    - the first 34 comments on the V Orange launch, on Facebook and Instagram. Claude labelled them in the chat.
- **Findings:**
  - V7 launched **V Orange** on 11 Oct: 528K Facebook views and a 97K YouTube Short in two days, 154 comments. It isn't on TikTok yet. Most comments are excitement and friend tags; about 1 in 6 ask when and where it will be sold; others ask for 1 L and 2 L bottles and other flavours.
  - Cream Soda's 2026 summer edition launched on **6 Aug** (teaser 2 Aug), not 1 May. The dashboard said May.
  - "V Lemon" in V7's July reels is the Lemon-Lime can (Carrefour's listing is "V Lemon").
  - V7 posted 10 times in the last 30 days, against 24 in the 30 days before.
  - Partnerships found in V7's posts: Circle K × V7 Mixology Menu (30 Jul), V7 × Cairokee night (17 Aug), On the Run × V7 Refreshment Menu (30 Aug).
  - Pages abroad:
    - V7_UK hasn't posted since 3 Sep, and V7 Tunisia posted twice in 30 days.
    - V7 Uzbekistan is active, lists its shops (Makro, Andalus, Assorti, Baraka, Cool) and on 13 Oct asked for regional distributors. Its 8 Oct posts say "0% Shakar" (0% sugar).
    - V7 India was at Anuga Select India in Mumbai (late Sep).
    - Halal Drinks Co (UK) launched V7 6-packs on 3 Oct.
  - YouTube shows no comments on any of V7's 12 latest videos.
- **Dashboard (Version 21):**
  - **Dates:**
    - The data now runs to 12 Oct 2026 (was 2 Oct), so the V Orange launch is in range.
    - Store alerts keep their real 4–5 Oct dates.
    - The custom date range allows the full period.
  - **Products:**
    - V Orange is added (V Cola line, new, can colour `#EE6A1F`), and Cream Soda's launch is 6 Aug.
    - For a new product's first 4 weeks, "Can't find it" reads "Looking for it", and the status line says "day N since launch".
    - A new category, "Excited to try it", covers launch reactions, so "Tried it" stays for people who tasted it. For V Orange it's 0.
  - **Our content:**
    - All 50 V7 posts from late July are real (Facebook, Instagram, TikTok, YouTube), with counts as of 13 Oct. Demo posts fill only the days before each platform's first real post.
    - Followers are the 13 Oct counts: 79,783 on Facebook, 38,959 on Instagram, 36,900 on TikTok, 2,540 on YouTube.
    - The header badge reads "Partly real".
    - The posts table says how many rows are real.
    - "Positive comments" shows "—" under 5 comments.
    - Generated comments follow each post's real comment count, up to 120 (was 60).
  - **Comments on a launch post** follow the 34 real V Orange comments: excitement, tags, "when will it be in stores?", sizes and flavours. There are new templates, and V7 has a reply for "when will it be sold".
  - **Outside Egypt, V7 pages abroad:**
    - The table is real, from each page's 12 latest posts: followers, posts in the last 30 days ("12+" when the 12 don't reach back that far), average engagement rate, average video views, last post and best post. Older pinned posts are left out of the averages.
    - "Positive comments" is gone.
    - The demo posts on V7's pages abroad are replaced by the real ones, and the panel shows the latest post from each page.
    - The UK distributor's 3 V7 posts are real posts abroad.
  - **Outside Egypt, Countries:**
    - "Main issue" uses short names, with the full label on hover.
    - "Asking to buy" says when nobody asked.
  - **Events:**
    - The V Orange launch is the pending suggestion, found from the jump in posts and comments (about 56× the week before).
    - The unsupported demo "Pomegranate post reshared" suggestion is removed.
    - The Cream Soda launch, Circle K menu, Cairokee night and On the Run menu are added as real team events.
    - Event evidence counts posts and comments, and names every platform V7 posted on.
  - **Alerts:**
    - A new product's "when and where" questions get their own alert ("V Orange launch: 24 people asking when and where to buy it") and a "Launch questions" rule. They no longer trigger "More people can't find V7".
    - The Overview's "Can't find it" panel leaves them out, with a link to read them.
    - The period line reads "public posts and comments".
  - **Online stores:**
    - Tables list only products that existed at the 4–5 Oct check. A note says V Orange launched after it.
  - **Commenters' follower counts** show only where a platform gives them (post authors on X and TikTok, and pages and creators). Comment tools don't return them (`folKnown`).
  - **Charts:** the last date label on a line chart ends at the edge instead of being cut off.
  - **Copy:**
    - The sidebar, the guide and the Ask V7 Pulse system prompt say V7's own posts are real.
    - The prompt says today is 13 Oct, and that the data runs to 12 Oct.
    - The prompt counts the real posts.
- **Tests:**
  - New `tests/test_v21.py` (25 checks).
  - `test_v5.py` uses the new pending event.
  - `test_v11.py` includes V Orange and fixes the Lemon-Lime id.
  - `test_v15.py` expects 13 can colours.
  - `test_v20.py`:
    - expects about 70% of the conversation under V7's posts;
    - checks the launch alert instead of "waiting over a day", which doesn't fire at V7's real posting volume;
    - reads Customer voice over 90 days.
  - All 13 suites pass, on the file and on `docs/index.html`.
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 20 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v20.html`; the new `REAL_OWN` and `REAL_OWN_X` blocks are written by `data/raw/verify_13oct/build_own_posts.py --inject`);
  - `data/raw/verify_13oct/`: `own_pull.py`, `own_pull2.py` and their JSON, `build_own_posts.py`;
  - `DESIGN.md` (V Orange's colour);
  - tests, CLAUDE.md, README.md.
  - Published as artifact Version 21.
- **Not yet public:** the GitHub copy shows Version 19 (Versions 20 and 21 are committed locally).

### Public copy: Version 21 (13 Oct 2026)
- **Why:** the user's OK ("yes push it").
- `deploy/build_sites.py dashboard` rebuilt `docs/index.html`, and all 13 suites passed on it (`DASH_SRC`).
- Pushed `main` (commits 6eb7235 Version 20, ea37ea4 Version 21, 992409f public copy). https://mohanadabouserie.github.io/v7-pulse/ serves Version 21.

### Version 22: V7's own posts back to 16 Apr (13 Oct 2026)
- **Why:** the user approved the 180-day backfill ("go ahead with the 180-day backfill").
- **Real data (Apify, every run capped, after 3-post tests of the Facebook and TikTok date filters):** USD 0.39 by Apify's run records, against the USD 0.30 estimated first and the 0.35–0.40 estimated before the runs. Apify reads USD 4.64 of 5, so USD 0.36 is left until 2 Nov.
  - `data/raw/own_backfill_13oct/pull.py`:
    - Facebook 16 Apr – 20 Jul: 21 posts, date filter;
    - TikTok 16 Apr – 1 Aug: 9 videos, date filter;
    - Instagram: the 45 latest posts, back to 27 May. The run hit its cap, so Instagram before 27 May stays demo;
    - YouTube channel since 16 Apr: 30 videos and Shorts.
  - `yt_pages.py`: exact dates and likes for 18 older YouTube videos, read free from their public pages, 2 seconds apart.
- **Findings in V7's older posts:**
  - **V Lemon relaunch (19–20 May):** "It's now V Lemon" reels got 19.4M views on Facebook, and a YouTube Short 5.5M.
  - **V Cola's "Raise the flag" World Cup campaign (28 May to 7 Jul):** Egypt's flag on cans and trucks, with Seoudi, Breadfast, Talabat, Oscar Grand Stores, Buffalo Burger, ESLSCA, clubs and Ahl Masr hospital joining in. The launch reel got 4.7M views on Facebook and 685K on Instagram.
  - **New can design ("Hello Summer. New Design", 21 Jun):** 4,719 reactions and 150 comments on Facebook.
  - **Smaller items:**
    - a Breadfast giveaway (top 10 V Cola orders win prizes, June);
    - the Cafex Egypt exhibition (7 May);
    - Playa booth (16–21 Jul);
    - factory-opening posts and shares (11 and 14 May).
- **Dashboard:**
  - **Our content:** 129 real V7 posts in Egypt (Facebook 36, Instagram 45, TikTok 19, YouTube 29). Demo posts remain only on Instagram before 27 May; 10 of them show over the full 180 days.
  - **Rebuild script:** `build_own_posts.py` merges both pulls. Times are converted to Cairo time (summer time from 24 Apr). Flag, national-team and "V Cola" posts are tagged V Cola, and shared news posts get their source as text.
  - **New real events:** the V Lemon relaunch (19 May), the "Raise the flag" campaign (28 May) and the new can design (21 Jun). The Summer of Colors event text is corrected: the new cans were first shown on 21 Jun.
  - **Demo public posts** follow these campaigns, with more V Lemon from 19 May and more V Cola from 28 May to 7 Jul.
  - **A new product's first week** has no tasting categories: excitement, where and when, price, "is it worth trying?", flavour ideas.
  - **Engagement rate and Best formats** leave out posts with views 20+ times the followers (most likely promoted). Promoted YouTube Shorts showed 47.5% engagement on a 2,540-subscriber channel.
  - **Profile visits:** the busiest-day note names the V7 post that drew the most views that day, not just an event the day before.
  - **Copy:** the guide, the "Partly real" tooltip and the Ask V7 Pulse prompt say V7's posts are real from 16 Apr (Instagram from 27 May).
- **Tests:**
  - New `tests/test_v22.py` (10 checks).
  - `test_v21.py`: 90 days are now all real.
  - `test_v20.py`: the share under V7's posts must be over half (55–75% depending on the demo draw).
  - All 14 suites pass, on the file and on `docs/index.html`.
- **Files:** `V7_Pulse_Dashboard.html` (Version 21 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v21.html`), `data/raw/own_backfill_13oct/`, `data/raw/verify_13oct/build_own_posts.py`, tests. Published as artifact Version 22.

### Public copy: Version 22 (13 Oct 2026)
- **Why:** the user's OK ("yes push it").
- `deploy/build_sites.py dashboard` rebuilt `docs/index.html`. All 14 suites had passed on this build before the Version 22 commit, and test_v22, test_v21, test_v18 and test_v5 were run again on the rebuild.
- Pushed `main` (52fd85f Version 22, ce56aa8 public copy). https://mohanadabouserie.github.io/v7-pulse/ serves Version 22.

### Marketing team feedback (15 Oct 2026)
- V7's marketing team sent feedback for the development phase: posts viewable inside the dashboard, a more intuitive and actionable interface, immediate email and mobile alerts with recommended actions, a daily executive summary (with mixed sentiment and UGC worth amplifying), and a competitor overview of Pepsi and Schweppes.
- Recorded in `PROJECT_MEMORY.md` section 11. No dashboard change yet; next steps are being proposed to the user.

### Version 23: the marketing team's feedback (15 Oct 2026)
- **Why:** V7's marketing team asked for:
  - posts viewable inside the dashboard;
  - a more intuitive, actionable interface;
  - immediate alerts with recommended actions;
  - a daily executive summary.

  The user asked to build all of it as one version. Competitors are on hold (DECISIONS #98).
- **Real images (free, no Apify):**
  - `data/raw/media_13oct/fetch_media.py` saved the cover image of 183 of 190 real posts:
    - Instagram 105 (V7 Egypt, the pages abroad, the distributor);
    - YouTube 30 (i.ytimg.com);
    - Facebook 29;
    - TikTok 19, read from each video's public page, because TikTok's oEmbed service doesn't answer from this network.
  - Images are shrunk to 360 px (JPEG quality 55). The fetch ran one request a second, over IPv4 when the host has it, since this network often can't reach IPv6.
  - Missing: 4 Facebook images on hosts reachable only over IPv6, and 3 Facebook text posts or shares.
  - `build_media.py --inject` writes them into a new `/*MEDIA*/` block (about 2.4 MB). The page is now 3.25 MB.
- **Dashboard:**
  - **Posts you can see:**
    - Post cards show the image with a video or album mark, and "View post".
    - "Our posts" shows a thumbnail in each row.
    - The new post view shows the image, full text (captions now kept up to 1,500 characters), numbers and links, then the comments with V7's replies, and says what's real.
  - **Needs your attention:** Overview and Customer voice open with up to 4 action cards: severity, evidence, next step, owner. On phones they swipe sideways.
  - **Alerts:**
    - Every alert to act on gets a next step and an owner.
    - Rumor alerts use the fact sheet's actions and replies. Launch questions come with a reply to fill in (date, places).
    - "Preview the email and phone alert" shows:
      - the email: subject, why it matters, the posts behind it (real rumor posts or posts with their images), next step and a suggested Arabic and English reply with a copy button;
      - the phone notification.
    - "How they're sent": Act now goes by email and phone right away; the rest by email and in the daily brief.
  - **Daily brief (new tab under To act on):**
    - Sections: brand health (mentions against the 7-day average, the four-part sentiment, replies waiting, V7's posts), red flags, positive signals, worth amplifying (each with a suggested step) and 3–5 recommended actions with owners.
    - Any of the last 7 days can be opened, and "See the email" shows the morning email.
  - **Mixed sentiment:**
    - A fourth class (orange `--mix`) in the stats, charts, legends, tooltips, pills, the posts filter and the Ask V7 Pulse tools.
    - In the demo, some complaints and requests come with a word of praise ("Love it, but…"), using their own random numbers: about 7% of the conversation.
  - **Worth amplifying:** positive, original posts by people and creators with some engagement. It's a posts filter, an attention card and a brief section, each post with a suggested step: thank, ask to repost with permission, or invite a creator.
  - **Smaller changes:**
    - Alerts and Events, like the brief, are marked "Partly real".
    - The guide defines Mixed, Worth amplifying, Needs your attention and Daily brief.
    - The sidebar note is shorter, so the sidebar fits 900 px.
- **Tests:**
  - New `tests/test_v23.py` (27 checks).
  - `test_v15.py`: the To act on group includes Daily brief; on phones, attention then KPIs start in the first screen.
  - All 15 suites pass on the file and on `docs/index.html`.
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 22 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v22.html`);
  - `data/raw/media_13oct/`;
  - `data/raw/verify_13oct/build_own_posts.py` (full captions);
  - `DESIGN.md`, tests.
  - Published as artifact Version 23.

### Public copy: Version 23 (15 Oct 2026)
- **Why:** the user's OK ("yes push it").
- `deploy/build_sites.py dashboard` rebuilt `docs/index.html`. All 15 suites had passed on this build before the Version 23 commit, and test_v23, v22, v21, v18, v15 and v5 were run again on the rebuild.
- Pushed `main` (1c1d43d Version 23, 84473e9 public copy). https://mohanadabouserie.github.io/v7-pulse/ serves Version 23.

### Version 24: V7 Pulse on Telegram (16 Oct 2026)
- **Why:** the user wants the alerts and reports on Telegram, and the dashboard's assistant connected to a Telegram bot. They created @v7_pulse_bot and gave the token in a file.
- **Security first:**
  - The token file `telegram_key` wasn't git-ignored in a public repo. It's now ignored, with `bot/state/`.
  - The token was copied to `.env.telegram` (ignored, mode 600) and is never printed or logged.
  - A private join code was added in the same file.
  - `getMe` confirmed the bot: V7 Pulse, @v7_pulse_bot.
- **The bot (`bot/`):**
  - `v7pulse_bot.py` runs on long polling (no webhook or open ports).
  - **Daily brief:** at 09:00 Cairo time.
  - **Act now alerts:** as soon as they're found (checked every 2 hours).
  - **Commands:** `/brief`, `/alerts`, and questions with `/ask` or plain text.
  - **Access:** people join with the private link `t.me/v7_pulse_bot?start=<code>`, and the first to join is the admin (`/subscribers`, `/remove`, `/test`). Anyone else gets a short note.
  - **Source:** `dashboard_reader.py` reads the brief, the alerts and Ask V7 Pulse's built-in answers from the website copy (`docs/index.html`) in a headless browser. Telegram and the website say the same thing.
  - **Docs:** `README.md`, plus a systemd user service file.
  - **Running:** it runs on this machine since 16 Oct, 21:59.
- **Dashboard (Version 24):**
  - Alert rules say Act now goes on Telegram and by email right away, the rest in the daily brief, with a link to @v7_pulse_bot.
  - The alert preview shows the Telegram message.
  - The Daily brief says it's sent on Telegram and by email, with an "Open in Telegram" button.
  - Ask V7 Pulse points to the same answers on Telegram.
  - Links like `…/v7-pulse/#brief` or `#alerts` open that tab, on load and on hash change, so the bot's links land on the right tab.
  - The guide explains Telegram.
- **Tests:**
  - New `tests/test_v24.py`. It also checks that no bot token or join link is ever in the page.
  - All 16 suites pass.
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 23 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v23.html`);
  - `bot/`, `.gitignore`, tests.
  - Published as artifact Version 24.

### Telegram bot update (16 Oct 2026, dashboard stays Version 24)
- **Why:** a review before anyone joined. The data stops at 12 Oct, so the 09:00 run would have sent the same brief every morning, and the bot was tied to the shell that started it.
- **The bot (`bot/v7pulse_bot.py`):**
  - Each chat gets each day's brief once; with no new day of data, nothing is sent (DECISIONS #108).
  - A chat that joins gets the welcome, the latest brief and any open Act now alert. Act now alerts are tracked per chat, so later joiners get them too.
  - "typing…" shows while the dashboard is read, instead of a "…" message.
  - A chat that blocks the bot or is deleted is taken off the list, and the others still get their messages.
  - Long messages split at line breaks too; a piece Telegram can't read as HTML goes again as plain text. Telegram 5xx answers are retried.
  - Its menu (brief, alerts, ask, help, stop) and descriptions are set where empty (DECISIONS #109).
  - One copy at a time (`bot/state/bot.pid`); it stops cleanly on SIGTERM; `V7_BOT_STATE` and the token in the environment let the test run on its own.
- **`bot/dashboard_reader.py`:** starts a new browser if the old one crashed.
- **Running:** restarted detached at 22:20 (own session), so it no longer depends on the tool shell.
- **Tests:** new `tests/test_bot.py` (49 checks) against a stand-in for Telegram and the real dashboard; FAIL 0 on the source and on `docs/index.html`.
- **Files:** `bot/v7pulse_bot.py`, `bot/dashboard_reader.py`, `bot/README.md`, `tests/test_bot.py`, `CLAUDE.md`, `PROJECT_MEMORY.md`, `DECISIONS.md`.

### Public copy: Version 24 (16 Oct 2026)
- **Why:** the user's OK ("yes push it").
- Checked first: no bot token or join code in any commit pushed or any tracked file.
- `deploy/build_sites.py dashboard` rebuilt `docs/index.html`. All 16 dashboard suites and `test_bot.py` passed on the rebuild (`DASH_SRC`).
- Pushed `main` (aaf5737 Version 24, 450a534 the bot update, 341c196 public copy). https://mohanadabouserie.github.io/v7-pulse/ serves Version 24: the links to @v7_pulse_bot are there, the join link isn't.
- The live bot reads `docs/index.html`, so its brief, alerts and answers now come from Version 24.

### Telegram bot: questions answered by Claude (16 Oct 2026, dashboard stays Version 24)
- **Why:** the user: "connect it to my claude sessions until I get an llm api key… so that the bot on telegram can answer any question".
- **How it works:**
  - The bot opens the dashboard with a stand-in for claude.ai's runtime, so the page hands over what it gives Claude on claude.ai: its standing instructions and eight read-only tools (`dashboard_reader.ai_setup`, `tool_page`, `run_tool`).
  - `bot/claude_tools_mcp.py` serves those tools to Claude Code over MCP (stdio). They run in a headless copy of the dashboard.
  - Each question starts Claude Code in the background (`claude -p`, JSON out, the question on stdin). The bot keeps answering other commands, shows "typing…", then sends the answer as Telegram text: Markdown, tables as lines, the web and Apify suggestions as lines, and a link to the dashboard.
  - Follow-ups see the chat's last three exchanges, kept in memory for two hours.
- **Locked down (DECISIONS #111):**
  - no built-in tools, only the dashboard's tool server (`--tools ""`, `--strict-mcp-config`, `--allowedTools mcp__v7pulse`);
  - its own sign-in folder, a clean environment, and an empty folder outside the project;
  - 100 questions a day, two at a time, one per chat, three minutes each.
- **Fallbacks:** when Claude can't answer (not signed in, the plan's limit, too slow), the built-in answer, with a line saying why. If the plan doesn't include Opus 5.5, the plan's default model.
- **Sign-in:**
  - The CLI's default login on this machine is the user's work account (another company's Team plan), so it isn't used (DECISIONS #112). The bot needs its own sign-in: `CLAUDE_CONFIG_DIR="$PWD/bot/state/claude" claude auth login`.
  - The user's first sign-in (23:07) went to the work account too, because the browser was signed in to it on claude.ai. The bot now refuses any organization listed in `CLAUDE_BLOCKED_ORGS` in `.env.telegram` (set to the work organization; the name stays out of the public repo). Restarted at 23:08; no question went to Claude in between.
  - A question then gets the built-in answer, with a line saying Claude is signed in with an account the bot doesn't use.
- **Checked:**
  - The real CLI accepts every option the bot passes; with no sign-in it stops at "Not logged in".
  - `tests/test_bot.py` now has 77 checks, with `tests/fake_claude.py` (a stand-in for Claude Code that runs the real tool server). FAIL 0 on the source and on `docs/index.html`.
- **Running:** the bot restarted at 23:04 with the new code. The user joined as the admin at 22:39.
- **Files:** `bot/v7pulse_bot.py`, `bot/dashboard_reader.py`, `bot/claude_tools_mcp.py` (new), `bot/README.md`, `tests/test_bot.py`, `tests/fake_claude.py` (new), `CLAUDE.md`, `DECISIONS.md`, `PROJECT_MEMORY.md`.

### Telegram bot: signed in to Claude (16 Oct 2026)
- Three sign-ins went to the work account, because the browser was signed in to it on claude.ai; the bot refused it each time (one question, at 23:50, got the built-in answer). With the work account signed out of the browser, the fourth went to the user's personal account (Max plan) at 23:55.
- First real question, run through the bot's own code: "What are the main complaints this month, and what should we do about them?"
  - 18 seconds, `claude-opus-5-5`, 4 turns (the dashboard's tools), exit 0;
  - 1,722 characters of Telegram text, balanced HTML, no em dashes;
  - it named price and availability, tied the price complaints to the real Noon price, said the counts are demo data, and gave four actions with owners;
  - the API would have charged about USD 0.16 for it.
- The live bot needed no restart: its next sign-in check finds the new account.

### Real data everywhere: the collection (17 Oct 2026)
- **Why:** the user upgraded Apify to Starter and asked for real data in every tab but Market, with Claude (their own plan) reading everything, no dummy data and no assumed numbers.
- **Plan:** `data/raw/real_17oct/PLAN.md`. Window 20 Apr to 16 Oct 2026 (180 days); at most USD 14 of the USD 19 cycle, USD 5 in reserve; a cap on every run; 3-item tests first (USD 0.06).
- **Collected** (`collect.py`, raw files in `raw/`):
  - V7 Egypt's posts: Facebook 34, Instagram 51, TikTok 19, YouTube 28 (exact YouTube dates and likes from the public pages, `yt_pages.py`; comments are turned off on all of them).
  - Every comment on those posts, with replies: Facebook 898, Instagram 1,141, TikTok 883. V7's replies: 632, counting V Super Soda's (DECISIONS #118).
  - The pages abroad and the UK distributor: 194 posts, and 829 of their 1,837 comments (stopped by hand for the budget, DECISIONS #121).
  - Public posts: X 314, Facebook search 12 queries, Instagram hashtags 137, TikTok 299, YouTube 124, Reddit 58.
- **Spend:** USD 11.62 by the run records, 12.05 by Apify's meter. Lessons: Facebook's comment date filter is charged per comment (about USD 0.56 wasted); comment counts on pages abroad were much higher than their latest posts suggested.
- **Merged** (`normalize.py`): one list in `items.json`, Cairo time, deduplicated, X's filler rows dropped, collaboration posts filed under their V7 page, replies linked to the comments they answer.
- **Labelled** (`label.py`): Claude Code with the bot's sign-in (the user's personal Max plan), Opus 5.5 at low effort, 40 items a batch, JSON schema (DECISIONS #116, #117). 3,395 comments and X posts first, in 83 batches with no failures; then the public posts.
- **Built** (`build_real.py --inject`): the REAL_OWN, REAL_OWN_X and new REAL_DATA blocks. Private people anonymous, @mentions masked (DECISIONS #122).

### Version 25: real data everywhere (17 Oct 2026)
- **Why:** the user asked for real data in every tab but Market, with no demo data and no assumed numbers.
- **The data:** see "Real data everywhere: the collection" above. The dashboard now runs 20 Apr to 16 Oct 2026 (`END` moved from 12 to 16 Oct).
- **Out:**
  - **The demo generators:** made-up creators, pages, people and groups, the post and comment templates, the abroad posts, and the mixed-sentiment rewrite.
  - **The demo account insights:** profile visits and "Who follows us", with Ask V7 Pulse's lookups and built-in answer on them (DECISIONS #119).
  - **Estimated reach:** "~ reach" marks and reach estimates. "Top … by reach" becomes "by views" (DECISIONS #115).
  - **Views spread over the days after a post:** views and engagement now count on the day the post went up (DECISIONS #114).
  - **Leftover demo pieces:**
    - the made-up event ev10;
    - "Real post", "Real account" and "Real" tags;
    - "demo" wording in the brief, the post view, the guide and Ask V7 Pulse's rules.
- **In:**
  - **Loaders:** for V7's posts, the pages abroad (with collaboration posts) and the new REAL_DATA block, which holds public posts, comments with replies and anonymous authors.
  - **Classes:** p_ad, n_contest, q_job and n_other (DECISIONS #117).
  - **V Super Soda** counts as V7, both its authors and its replies (DECISIONS #118).
  - **"When people comment":** replaces the online-followers heatmap, built from the real comment times.
  - **Wording:** "in a Facebook group" on cards; Facebook, Instagram and TikTok named where replies are tracked.
  - **Badge and footer:** "Real data" on every tab, with the check date; the sidebar footer says all data is real.
  - **Outside Egypt pages table:** every post since 20 Apr and exact counts. The "12+" mark is gone.
- **Images:** `data/raw/real_17oct/fetch_media.py` added 129 covers (300 px). 312 images in all; the page is 6.4 MB.
- **Ask V7 Pulse rules:** "today is 17 Oct", every source real, what isn't available.
- **Tests:**
  - New `tests/test_v25.py`: the real data block, privacy, no demo outside Market, no estimated reach, Our content, the post view with V7's replies, phone, tablet and dark mode.
  - Updated v18, v20, v21, v22, v23 and test_bot to the real data. The 7 MB page limit replaces 5 MB.
- **Files:** `V7_Pulse_Dashboard.html` (Version 24 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v24.html`), `data/raw/real_17oct/`, `data/raw/media_13oct/index.json` and `img/`, tests, `CLAUDE.md`, `DESIGN.md`, `DECISIONS.md`, `PROJECT_MEMORY.md`.

### Version 25 published (17 Oct 2026)
- **Published** privately to https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc (version id 1792192011-9c1f), with the `sample` capability carried forward. The public site and the Telegram bot still show Version 24 until a push.
- **What blocked the publish, and the fixes:**
  - Replacement characters (U+FFFD) in a few scraped texts were refused. `normalize.py`'s `clean()` now strips them.
  - The publish guard took the page for a code-review page and refused it: review pages may be 512 KB at most. The trigger was nine Facebook links ending in `&id=…`. Each sits in the MEDIA block right before its image data, and the guard reads an `id=` followed by more than 2,048 characters with no space as review markup. `build_media.py` and `build_real.py` now write that `=` as `\u003d` inside the data strings, which reads back as the same link (DECISIONS #124).
- **Lighter page (DECISIONS #125):**
  - The page no longer carries Claude's English gist for each post and comment. It wasn't shown, and it stays in `labels.json`.
  - Comment links are stored as their ids (`ci`, `ri`) and rebuilt in the page from the post's link. All 2,867 Facebook and Instagram comment links were checked to come out identical.
  - The images keep their earlier quality. The page is 6.2 MB.
- **Tests:** `test_v25.py` checks that the guard won't take the page for a review page, and that the image keys read back as the real links. All 17 suites pass.
- **Files:** `V7_Pulse_Dashboard.html`, `data/raw/media_13oct/build_media.py`, `data/raw/real_17oct/build_real.py`, `data/raw/real_17oct/normalize.py`, `tests/test_v25.py`, `CLAUDE.md`, `DECISIONS.md`, `PROJECT_MEMORY.md`.

### Public copy: Version 25 (17 Oct 2026)
- **Pushed** at the user's request: `docs/index.html` rebuilt with `deploy/build_sites.py dashboard`, so https://mohanadabouserie.github.io/v7-pulse/ shows the real data. The push also carries the two Telegram bot commits from 16 and 17 Oct (any question answered by Claude through Claude Code).
- **Tests on the public copy:** all 17 dashboard suites and `test_bot.py` pass with `DASH_SRC` on `docs/index.html`.
- **Telegram bot:** it had stopped when the machine shut down (02:47) and was started again at 05:48. It reads the new copy.
- **Daily views (decision only, DECISIONS #126):** once a daily check runs, each day gets the views added that day. Days before the first check keep the counts on the day the post went up.
- **Files:** `docs/index.html`, `CHANGELOG.md`, `DECISIONS.md`, `PROJECT_MEMORY.md`.

### Version 26: the wider search and YouTube comments (18 Oct 2026)
- **Why:** the user saw one Instagram post about V7 by other people in the last 7 days and asked for many Arabic and English keywords, workarounds beyond hashtags, a TikTok keyword search, and YouTube comments (they found the scrapers).
- **What was wrong on 17 Oct:**
  - Instagram had only 8 hashtags; most results were Cambodia's own V-Cola or years old (12 posts kept).
  - TikTok's own date filter returns unrelated videos, so no TikTok post was kept for the last 30 days.
  - "Comments are turned off on V7's YouTube videos" was wrong: `yt_pages.py` matched words that are in every page. They're on for 27 of 28.
  - V7's YouTube titles were English machine translations, and their comment counts were 0.
- **Tested first (USD 0.23):** Instagram keyword search (two scrapers), posts tagging @v7egypt, posts mentioning it, Google searches of instagram.com and tiktok.com, TikTok searched and browsed from Egypt, and YouTube comments with apidojo and calm_builder.
- **Collected (`collect.py test2`, `wide`, `ttkw`, `ytcheck`, `ytc`):**
  - **Instagram:** posts tagging @v7egypt (180, back to 19 Jun) and @vsupersoda (60); keyword search with 15 of 24 spellings inside the window (381, stopped at its cap); Google's finds (159 links, 108 new, fetched by link).
  - **TikTok:** Google's finds (83 new, fetched by link); 5 hashtags (101) and a 10-keyword search (124, 8 keywords before its cap), both from Egypt.
  - **Facebook, X and YouTube:** 6 more Facebook spellings, one more X query (136 posts), YouTube newest-first (76).
  - **YouTube comments:** V7's videos (58) and the 14 public videos about V7 with comments (1,015).
  - **Image links:** dates read from Instagram shortcodes and TikTok ids, so only finds inside the window were fetched.
- **Labelled:** Claude labelled 2,065 new items, no failures (`label.py`).
- **Result:**
  - **Public posts about V7:** 586, up from 219: Instagram 280 (was 12), TikTok 96 (was 16), Facebook 124, X 63, YouTube 21, Reddit 2.
  - **Last 7 days:** Instagram 18 (was 1), TikTok 6 (was 0).
  - **YouTube comments:** 731, with 676 under public videos and 55 under V7's.
  - **Comments in all:** 4,257.
- **Dashboard:**
  - **Comments under public videos:** they show under the public YouTube videos about V7. They never count as waiting for V7.
  - **Comment times:** YouTube comments carry a day, not a time. They stay out of "When people comment" and out of the reply times.
  - **Month-only comments:** YouTube only gives the month for older comments ("4 months ago"). Those 120 are listed under their video as "about 4 months before 18 Oct", but not counted by day.
  - **V7's YouTube videos:** original Arabic titles and real comment counts.
  - **Wording:**
    - "as of 17 Oct" or "18 Oct" per post;
    - "collected on 17–18 Oct";
    - the help, the data sources and Ask V7 Pulse's rules no longer say YouTube comments are off;
    - "Comments under other people's posts" replaces "other posts".
  - **Needs your attention:** plain volume spikes now rank after questions waiting for V7; a negative day is still critical.
  - **Images:** 119 new images (431 in all). The page is 8.0 MB.
- **Findings:**
  - **Can't find V7:** the alert fires with 15 posts and comments this week. 10 are YouTube comments under Kareem Elsayed's and Youssef Bsheer's videos: not available everywhere, no fridges in working-class cafés, no ads or distribution in Upper Egypt, supply problems.
  - **Where the talk is:** over the last 30 days, comments under other people's posts are 59% of the conversation in Egypt (YouTube 60%, mostly Kareem Elsayed's video). Comments under V7's posts are 26% and public posts 15%.
- **Spend (Apify's final run charges):** the wider search USD 3.06, the TikTok keyword search 0.50, the YouTube check and comments 0.49, tests 0.23: USD 4.28 on 18 Oct. The cycle is at USD 16.33 of 19 by the meter; 2.67 is left until 15 Nov.
- **Tests:**
  - New `tests/test_v26.py`: Instagram and TikTok coverage, YouTube comments and their dates, "can't find V7" leaving launch questions out, the post view, phone, tablet and dark mode.
  - Updated: v20 (the conversation split), v21 (the launch alert), v23 (9 MB), v25 (the footer) and test_bot (an open Act now alert after the brief on joining).
- **New report:** `data/raw/real_17oct/SCRAPERS.md` (from `scrapers_report.py`) lists every scraper with its link, input, output and cost.
- **Files:**
  - **Dashboard:** `V7_Pulse_Dashboard.html` (Version 25 saved as `archive/dashboard_versions/V7_Pulse_Dashboard_v25.html`).
  - **Pipeline:** `data/raw/real_17oct/` (`collect.py`, `normalize.py`, `build_real.py`, `fetch_media.py`, `scrapers_report.py`, `SCRAPERS.md`, `runs_final.json`, `real_dashboard.json`, `run.log`), plus `data/raw/media_13oct/`.
  - **Tests:** `tests/`.
  - **Notes:** `CLAUDE.md`, `DECISIONS.md`, `PROJECT_MEMORY.md`.

### Public copy: Version 26 (18 Oct 2026)
- **Pushed** at the user's request: `docs/index.html` rebuilt with `deploy/build_sites.py dashboard`, so https://mohanadabouserie.github.io/v7-pulse/ shows the wider search and the YouTube comments.
- **Tests on the public copy:** all 18 dashboard suites and `test_bot.py` pass with `DASH_SRC` on `docs/index.html`.
- **Telegram bot:** it opens a fresh copy of the page for each brief, alert check and question, so it uses Version 26 without a restart. Its next check sends the open "Act now" alert ("More people can't find V7: 15 this week") to the subscribed chat.
- **Files:** `docs/index.html`, `CHANGELOG.md`, `PROJECT_MEMORY.md`.

### Check: the Instagram keyword scraper (19 Oct 2026)
- **Asked:** did seemuapps/instagram-keyword-posts-scraper work well, and do people say it's reliable?
- **On our data:**
  - **Dates:** it kept the dates asked (1 of 381 outside).
  - **Counts:** for the 28 posts another scraper also fetched, dates and captions matched, and likes, comments and plays matched within a few hours' growth.
  - **Duplicates:** 59 rows repeated a post another keyword had already found.
  - **Relevance:** English and mixed phrases were mostly about V7 (V7 soda 24 of 30, V7 Egypt 22, مشروب V7 19, V7 drink 17). Arabic spellings were almost never about V7 (ڤي سڤن 1, في سفن 0, مشروب ڤي سڤن 1).
  - **Value:** 67 posts about V7, 46 of them found by no other method.
- **Online:** no independent reviews. Created 6 Oct 2026, 41 users and no ratings; its page reports 99.9% of runs succeeded and says it searches "the same way the Instagram search bar does", ranked by relevance, not by date.
- **Files:** `CLAUDE.md`, `PROJECT_MEMORY.md`.
- **Arabic on every platform (follow-up question):** the spellings with ڤ work (ڤي سڤن 25 of 29 about V7 on Facebook, ڤي كولا 26 of 30 on Facebook and 10 of 13 on TikTok), and so does Arabic mixed with V7. The spellings with ف fail everywhere: في سفن is "in" + "ships" (في سفن مشروب 2 of 30 on Facebook, 0 of 13 on TikTok). Instagram's own search is the weak link; Google's exact-phrase search of instagram.com found 7 of 11 for "ڤي سڤن". The rule is in `CLAUDE.md` (Known quirks).
- **Google's site search, checked (follow-up):** "posts can take days to reach Google" was from general knowledge. On 18 Oct Google returned a TikTok video from the same day and an Instagram post from the day before, but only 1 of its 203 Instagram links was from the last 2 days. Online, Google gives no timeline for Instagram; a recap of a Google talk (Oct 2026) puts the typical discovery of a new web address at about 20 hours. Instagram lets search engines index only public posts and reels since 2020 from accounts that meet its criteria, so Google never sees private accounts or stories. Of the 280 Instagram posts about V7: posts tagging @v7egypt 133, keyword search 67, Google 55 (all new), tagging @vsupersoda 36, hashtags 12.

### Instagram keyword scrapers compared (19 Oct 2026)
- **Asked:** search the Apify Store for Instagram keyword scrapers and pick the strongest.
- **Store search:** over 80 Instagram scrapers mention search. Seven were tested on the same three keywords (V7 soda, ڤي سڤن, V7 كريم صودا), up to 10 results each (`collect.py kwtest`, `kwtest_report.py`). The test cost USD 0.26.
- **Result (`data/raw/real_17oct/KEYWORD_SCRAPERS.md`):**
  - The four keyword scrapers find nearly the same posts; Arabic is weak for all of them.
  - The exact-phrase scrapers find almost nothing, and Apify's own search scraper returns only old "popular" reels.
  - Reels are 59% of the Instagram posts about V7, so the reels-only scrapers miss about 4 in 10.
- **Pick:** apidojo/instagram-scraper-api for English and mixed keywords (2,811 users, 1.28M runs a month, 100% succeeded, 5.0 from 9 reviews; all formats, a date filter, USD 0.0035 per useful post). seemuapps stays as the fallback.
- **Files:** `data/raw/real_17oct/collect.py`, `kwtest_report.py`, `KEYWORD_SCRAPERS.md`; `CHANGELOG.md`, `PROJECT_MEMORY.md`.
- **Switched to apidojo (user's OK):** `collect.py igkw` runs apidojo/instagram-scraper-api per keyword with 15 English and mixed phrases (`KW_IG_EN`), 10 results each. `normalize.py` and `fetch_media.py` read its results, tested on a 40-post run (35 inside the window; V7's own left out). The 18 Oct stages still name seemuapps, which they used (`IG_KW_SEEMUAPPS`). DECISIONS #133. Nothing is collected until a refresh runs.
- **Follow-up checks (USD 0.03):**
  - apidojo found 8 of dami_studio's 13 useful reels.
  - A 40-result run found 1 of the 4 it had missed; the rest weren't there, because dami_studio searches Instagram's Reels search.
  - Two apidojo runs of the same keyword shared only 4 useful posts.
  - Past its first 10 results per keyword, apidojo's rows mostly lack captions and likes.
  - Details in `data/raw/real_17oct/KEYWORD_SCRAPERS.md`.
- **dami_studio added (user's OK):** `collect.py igkw` now also runs dami_studio's Reels search (15 phrases, 30 reels each, newer than --since; USD 0.0004 a reel). `normalize.py` reads it (run-summary rows skipped) and `fetch_media.py` takes its cover images. Tested with apidojo on the comparison files: 27 posts inside the window, 4 found by both. DECISIONS #134.
- **What apidojo returns:** everything a post needs within its first 10 results, except the account's follower count and the share count. Filling the follower counts of the 187 Instagram accounts without one would cost about USD 0.43 (Apify's profile scraper); not done.
- **The re-fetch (user's OK):** `collect.py igkw` re-fetches by link every apidojo row without a caption or likes (Apify's post scraper, USD 0.0023 a post). `normalize.py` now fills a post's missing fields from any second source; in today's data that adds 6 share counts and nothing else changes (7,220 items). Real test on the 25 posts the step picks (USD 0.044): all read, 25 captions, 24 like counts (1 hidden by its owner), comments, dates, accounts and plays complete. DECISIONS #135.
- **Not closed by it:** likes hidden by their owner (37 Instagram posts today, shown as 0 on the dashboard), follower counts (USD 0.43 to fill with the profile scraper), shares (only some reels show them), deleted or age-restricted posts.

### Version 27: likes hidden (19 Oct 2026)
- **Why:** 37 Instagram public posts about V7 have no like count because their accounts hid it, and the dashboard showed "0 likes" (also 2 Reddit posts without upvotes). User: "yes fix the hidden likes".
- **Change:**
  - `build_real.py` flags them (`lh`), and the loader keeps the flag.
  - Post cards and the post view say "likes hidden" on Instagram and "… not shown" elsewhere.
  - The guide's "What the numbers mean" explains it. DECISIONS #136.
- **Data:** rebuilt with `normalize.py`'s gap filling, which adds 6 share counts. Otherwise unchanged: 586 public posts, 3,625 comments shown.
- **Tests:** new `tests/test_v27.py` covers the flag, the most-viewed hidden-likes post's card and post view, phone, and dark mode. All 20 suites pass.
- **Published** privately to https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc (Version 27). The public site still shows Version 26 until a push.
- **Files:** `V7_Pulse_Dashboard.html` (Version 26 saved in `archive/dashboard_versions/`), `data/raw/real_17oct/build_real.py`, `tests/test_v27.py`, notes.

### Reels and sentiment: what's said in the video (19 Oct 2026)
- **Today:** sentiment, topic and products for a reel or video come only from its caption (for YouTube, the title and the start of the description). What's said in the video isn't read.
- **What can be added:**
  - **TikTok:** TikTok's own automatic subtitles come with the data already collected. 74 of the 96 TikTok videos about V7 have them, mostly Arabic, and they download free. Example: the caption "كل الاطعم من V كولا…" vs the speech "الشنطة دي اسمها شنطة المزاج… كل الاطعم بتاع شركة في كولا".
  - **Instagram:** apple_yang/instagram-transcripts-scraper (speech to text, about USD 0.0035 a chunk). The test on 3 Egyptian Arabic reels (USD 0.016) was good:
    - Kareem Elsayed's reel: 2,074 characters, a few word errors such as "دي 7" for V7.
    - A Cream Soda reel: "هي هي بالضبط طعم الكارامل مع سودا تحفة جربوها", where the caption only said it was back.
    - One reel is music only, so it has no speech.
    - All 166 Instagram reels about V7 would cost about USD 0.60 to 1.00.
  - **YouTube:** automatic subtitles, about USD 0.0016 a video (21 videos, about USD 0.03).
- **Then:** Claude would re-read those posts with the speech, free on the user's plan. Not done; it needs the user's OK.

### Public copy: Version 27 (19 Oct 2026)
- **Pushed** at the user's request ("yes push it"). All 20 suites pass on `docs/index.html`, and the live site serves Version 27 ("likes hidden").

### Version 28: what's said in reels, and Instagram follower counts (19 Oct 2026)
- **Why:** user: "add the video speech to be read in the analysis of the posts on instagram and also close the follower count gap using any instagram scraper that can get this".
- **Follower counts:** `collect.py igprofiles`, apify/instagram-profile-scraper.
  - 175 accounts that posted about V7 without one: 174 filled (USD 0.40).
  - Sizes: 66 under 1K, 46 at 1K–10K, 39 at 10K–100K, 23 at 100K+.
  - `normalize.py` adds them to every post by those accounts.
  - Effect: 410 accounts named (was 404, the 10K+ rule). "Big account: Cairo Spots (401K followers)" now shows for the V Orange launch post.
- **Speech:** `collect.py igspeech`, apple_yang/instagram-transcripts-scraper.
  - Reels covered: the 163 public reels about V7 (USD 0.79) and the 32 that tag V7 but whose caption alone didn't show it (USD 0.19). The 3 test reels were reused.
  - Results: 146 reels have speech (128 with 20+ characters); the rest are music or silent, and 4 failed on the transcriber's side.
  - `normalize.py` attaches it.
  - `label.py` sends it to Claude with the caption (rules explain recognition errors such as "دي 7") and labels such reels again (147 items, no failures; marked `sp`).
- **What the speech changed (146 reels):**
  - type 61, sentiment 38 (19 neutral → positive, 8 positive → neutral, 7 neutral → mixed, 2 to negative), products 35;
  - 6 reels now about V7, e.g. a "#pov #capcut" reel that is a Cream Soda taste review; 3 no longer.
- **Dashboard:**
  - A reel read with its speech says "Its sentiment and topic also count what's said in the video" in the post view.
  - The data sources and Ask V7 Pulse's rules mention the speech.
  - Public posts about V7: 589. Comments shown: 3,625.
- **Tests:** new `tests/test_v28.py` (speech flags, follower counts, privacy, the post-view note, phone, tablet and dark mode). All 21 suites pass.
- **Published** privately (Version 28). Public site: Version 27 until a push.
- **Spend:** USD 1.38 today (followers 0.40, speech 0.98). Apify's meter: USD 18.14 of 19, so about USD 0.86 is left until 15 Nov. `SCRAPERS.md` now lists 93 runs from 26 scrapers.
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 27 saved in `archive/dashboard_versions/`);
  - in `data/raw/real_17oct/`: `collect.py`, `normalize.py`, `label.py`, `build_real.py`, `scrapers_report.py`, `SCRAPERS.md`, `runs_final.json`, `real_dashboard.json`, `run.log`;
  - `tests/test_v28.py`; notes.

### Public copy: Version 28 (19 Oct 2026)
- **Pushed** at the user's request ("yes push it"). `docs/index.html` was rebuilt, and all 21 suites pass on it.
- **What the site now shows:** the reels' speech in the analysis and Instagram follower counts. The Telegram bot reads this copy.
- **Files:** `docs/index.html`, `CHANGELOG.md`, `PROJECT_MEMORY.md`.

### Check: is Instagram complete now? (19 Oct 2026)
- **No.**
- **Coverage:** 262 of the 283 Instagram posts about V7 were found by one method only. A rough capture-recapture estimate (tagged 144, keyword 65, both 21, for 19 Jun to 16 Oct) puts that period at about 445 posts; we have 229.
- **Sentiment:** 115 of 169 reels are read with real speech. On-screen text, text in photos, and the 4,115 comments under public posts aren't read, and labels haven't been checked by a person.
- **Missing info:** the re-fetch and the profile scraper fill most of it. Hidden likes, most shares, private accounts and Stories can't be had.
- **The official route:** V7's Business account through Meta's API covers tagged posts and @mentions completely. Details in PROJECT_MEMORY section 11.

### Version 29: the Instagram gaps, closed as far as public data allows (19 Oct 2026)
- **Why:** user: "close all the gaps in instagram ... also for music reels or albums, can we make an OCR or smth for them to read any text on them? ... maybe get an idea about the post from its comments ... investigate and see which is the most accurate". Apify's usage limit is now USD 100 (DECISIONS #139).
- **What reads music reels, photos and albums best (tests on 8 posts, `collect.py vistest`, `vistest2`, `covtest`):**
  - Claude reading the pictures (the photos, or the cover and a frame every 2 seconds of a reel; `vis_media.py`, `vis_read.py`): all the on-screen text afanasenko's extractor found, and more. It saw the V7 cup in a restaurant reel that the extractor called "V SPARKLING DRINK", and found no V7 in two DJ reels, which was right. Free on the Max plan. **Chosen** (DECISIONS #140).
  - afanasenko/instagram-reel-script-extractor: good text and a summary, but USD 0.075 a reel. Not used.
  - Comments: worth having for what people say, but they rarely say what a post shows. Instagram's alt text is generic. The audio pages of V7's ads returned 2 posts. None used to read posts.
- **More posts (DECISIONS #142):**
  - Google one month at a time, 12 exact phrases x 7 months: 882 new posts inside the window, fetched by link.
  - Every post tagging @v7egypt back to 20 Apr (520; the 18 Oct pull reached 19 Jun), 8 more hashtags, one more seemuapps sample, apidojo and dami_studio since 20 Apr (15 phrases each).
  - Instagram public posts about V7: 283 to **479**. Found by: posts tagging V7 250, Google 151, keyword search 112, Reels search 53, hashtags 22. 390 were found by one route only.
- **Read with more than the caption:** 202 reels with their speech, 423 posts from their pictures (359 of them about V7).
  - What the pictures changed: type 135, products 176, sentiment 72 (48 neutral to positive, 17 positive to neutral); 38 posts became about V7, 6 no longer.
- **Comments under public Instagram posts (DECISIONS #141):** 2,633 collected from 251 posts (up to 100 a post, most liked first) and labelled. 2,296 are about V7 and shown under their post: 1,518 positive, 454 neutral, 286 negative, 35 mixed. scrapesmith returned nothing for 137 posts, which Apify's own scraper filled.
- **Followers:** 110 more Instagram accounts.
- **Dashboard:**
  - a post read from its pictures says "Its sentiment and topic also count what's written or shown in its pictures" (or video) in the post view;
  - the data sources, the help and Ask V7 Pulse's rules mention the pictures and the comments under public Instagram posts;
  - public posts about V7: 785 (Instagram 479). Comments shown: 5,918, of them 2,296 under public Instagram posts. 546 images; the page is 10.2 MB.
- **Tests:** new `tests/test_v29.py` (more Instagram posts, comments under them, privacy, "never waiting for V7", the picture flags and post-view note, phone, tablet and dark mode). `test_v20.py` (volume range) and `test_v23.py` (size limit) allow the larger data; `test_v23.py` and `test_v25.py` expect "collected on 17–19 Oct". All 22 suites pass (the 21 dashboard suites and the bot).
- **Fixes on the way:** a labelling batch skipped 38 comments; they were labelled and added. The first choice of posts for pictures was too wide (1,230, with noisy Google finds): stopped at 775 and narrowed to posts about V7 or tagging it.
- **Found in the review (as V7's marketing manager):**
  - 21 Instagram accounts (talabat Egypt, Cairo 360, El-Shai and two V7 distributor pages among them) showed "Access delayed. Only the owner of the page can access this information" as their name: the tagged scraper's 19 Oct run put it in place of the full name on 201 of 520 posts. `normalize.py` now drops it and takes the name from the profile scraper, or shows the handle. `test_v29.py` checks it.
  - The page said the data was collected on 17–18 Oct. The sidebar, the post view, the help, the Real data badge and Ask V7 Pulse now say 17–19 Oct, and the 196 posts first collected on 19 Oct say "as of 19 Oct" (`build_real.py`).
  - The Overview's comment count and Ask V7 Pulse's rules still said comments under other people's posts aren't collected. They now name the comments under public Instagram posts and YouTube videos about V7.
  - People: the "Creators & pages" tile said "10K+ followers" for all 69, and the Creator size panel said "accounts with 10K+ followers" above Nano and Unknown bars. The count has always been every creator, page and news outlet; the tile now says "16 with 10K+ followers" and the panel "creators, pages and news outlets, by followers".
- **Published** privately (Version 29). Public site: Version 28 until a push.
- **Spend:** USD 12.13 today by the final run charges (more posts 4.89, comments 3.92, media links 1.97, tests 0.55, speech 0.55, followers 0.25). Apify's meter: USD 30.31 this cycle, so about USD 11.31 above the included USD 19 is billed as overage; the limit leaves USD 69.69. Labelling and reading pictures ran on the Max plan (no API charge). `SCRAPERS.md` lists 133 runs from 28 scrapers.
- **Still not possible:** private accounts, Stories, likes their owner hid, most share counts. No route finds every public post: by the closest pair (posts tagging V7 against Instagram's own search) there are about 780 in the window, so 479 is roughly 60%; other pairs say fewer. V7's own Business account through Meta's API would give every post that tags or @mentions it.
- **Files:**
  - `V7_Pulse_Dashboard.html` (Version 28 saved in `archive/dashboard_versions/`);
  - in `data/raw/real_17oct/`: `collect.py`, `normalize.py`, `label.py`, `build_real.py`, `fetch_media.py`, new `vis_media.py` and `vis_read.py`, `scrapers_report.py`, `SCRAPERS.md`, `runs_final.json`, `real_dashboard.json`, `run.log`;
  - `data/raw/media_13oct/` (115 new images, `index.json`); `.gitignore` (`vis/` and `vis_read.json` stay local);
  - `tests/test_v29.py`, `tests/test_v20.py`, `tests/test_v23.py`, `tests/test_v25.py`; notes.

### Version 30: Facebook, the same work as Instagram (19 Oct 2026)
- **Why:** user: "can you please do the same with facebook? everything we did with instagram starting with getting all keyword search scrapers, comparing them, then getting best or combine multiple then see data gaps and fill it … facebook have videos and reels as well".
- **Every Facebook search scraper compared** (`FB_KEYWORD_SCRAPERS.md`, `fbtest_report.py`; USD 2.72): 11 post-search scrapers, 4 video searches, the reel search, hashtags, public groups and Google, on the three Instagram keywords.
  - The post searches mostly share Facebook's own search and return the same posts (68 useful in all); scraper_one and Apify's search rank differently. Arabic with ڤ works on Facebook.
  - Not used: hashtags ("Empty or private data"), powerai (aborted 3 times), mina_safwat (no dates), headply's post search (no date filter).
- **Depth** (USD 1.10 with the gap tests): past the first 10-15 results per keyword Facebook returns unrelated posts, and one month at a time returns the same noise. So more keywords and other backends, not deeper searches (DECISIONS #143).
- **The search** (`collect.py fbcover`, USD 7.21): 30 keywords on silentflow, scraper_one and Apify's search; the reel search and three video searches (12 keywords); public groups (12 keywords; the run stopped after 62 posts); Google one month at a time (114 of 168 result pages before its cap). `fbdetails` fetched the 610 new reels, videos and Google links by link (danek, USD 1.40).
- **Facebook public posts about V7: 124 to 520** (Image 181, Reel 152, Text 107, Album 54, Video 26; Egypt 381, Syria 77). By route: scraper_one 290 (196 no other route found), silentflow 183 (68), the reel, video and Google links 117 (all new), Apify's search 70, groups 13 (11), video search 25.
- **Gaps filled** (`fbfill`, `fbfill2`, `fbviews`, `fbnames`):
  - reels and videos told apart from photos (the 17 Oct reader marked all 20 as photos; DECISIONS #144);
  - plays: 158 of 178 videos (social_developer, USD 0.57; danek by link for video posts behind a post link);
  - speech: 163 posts read with what's said in them (invideoiq, USD 7.84; it beat Facebook's captions and Whisper on the test; DECISIONS #145);
  - pictures: 267 photo posts, albums and quiet videos read by Claude (`vis_media.py --fb`, `vis_read.py`; DECISIONS #146). They changed the products of 54, the type of 20 and the sentiment of 26;
  - comments under the public posts: 2,797 shown (1,022 positive, 1,469 neutral, 259 negative, 38 mixed), from thedoor (271 of 286 posts, USD 1.87) and Apify's own scraper for 12 more (DECISIONS #147);
  - page followers and category: 210 of the 302 named pages, creators, businesses and news outlets (Apify's page scraper, USD 2.01); 34 have 100K+.
- **Found on the way:**
  - a 19.1-million-view reel came without its account's name; fetched by link, it was V Super Soda's (V7's own page). V7's own pages are now left out by their account ids too (15 posts), and 9 replies by V7's pages under public posts count as V7's;
  - the dashboard kept three posts entered by hand before Version 25 (a Mon3esh reel without its 1.36M views, and two Reddit reviews that showed twice). The collected records replace them;
  - one comment batch skipped some items; all labelled.
  - with the Facebook comments, two days in the last 30 passed 25% negative and both showed in "Needs your attention", pushing out "questions wait for V7". The panel now shows the latest negative day (the other is mentioned and stays in Alerts) and keeps one slot for replies waiting or posts worth amplifying.
- **Findings:** Kareem Elsayed's Facebook reel (1.46M views) and Mon3esh's (1.36M) are the biggest public Facebook posts; a viral post says Cream Soda "tastes like hair oil" (21,430 reactions); Facebook comments are mostly neutral tags and emoji, with price questions (213) and "not worth the hype" (158) the main complaints.
- **Dashboard:** public posts about V7 1,181 (Facebook 520, Instagram 479); comments shown 8,706 (was 5,918). The data sources, help, Ask V7 Pulse and the post view name Facebook's speech, pictures and comments. 708 images; the page is 13.4 MB.
- **Tests:** new `tests/test_v30.py`; `test_v23.py` allows 14 MB; `test_v28.py` accepts Facebook speech; `test_v29.py` follows the new wording. All 23 suites pass (22 dashboard suites and the bot).
- **Published** privately (Version 30). Public site: Version 28 until a push.
- **Spend:** USD 24.88 for Facebook today by the final run charges (tests 3.85, searches 4.58, reels, videos, groups and Google 2.63, by link 1.47, plays 0.57, speech 7.84, pages 2.01, comments 1.93). Apify's meter: USD 55.21 of the USD 100 limit (USD 36.21 above the included 19). Labelling (about 5,000 items) and picture reading ran on the Max plan. `SCRAPERS.md` lists 325 runs from 55 scrapers.
- **Still not possible:** private profiles and closed groups, Stories, most share counts, and many reels: Facebook's search surfaces about 600 posts about V7 (we have about 390 of those), while the reel, video and Google route found 155 posts that barely overlap with it (24), so far more reels and page videos exist than any search shows.
- **Files:** `V7_Pulse_Dashboard.html` (Version 29 saved in `archive/dashboard_versions/`); in `data/raw/real_17oct/`: `collect.py`, `normalize.py`, `build_real.py`, `fetch_media.py`, `vis_media.py`, `vis_read.py`, new `fbtest_report.py` and `FB_KEYWORD_SCRAPERS.md`, `scrapers_report.py`, `SCRAPERS.md`, `runs_final.json`, `real_dashboard.json`, `run.log`; `data/raw/media_13oct/` (162 new images); `tests/test_v30.py`, `tests/test_v23.py`, `tests/test_v29.py`; notes.
