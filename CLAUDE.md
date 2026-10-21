# V7 Pulse: working notes for Claude

V7 Pulse is a social listening and market dashboard for **V7**, an Egyptian vitamin soda (V7 flavours, V Cola, V Cola Diet, malt drinks). The brand belongs to **Benefit**; **Vitality** is its manufacturing arm. Mohanad Abouserie (GitHub `mohanadabouserie`) is pitching it to V7's marketing manager as an internal employee. The deliverable is a working dashboard: real data where it can be collected, clearly labelled demo data where it can't yet.

## Read first, every session
1. `PROJECT_MEMORY.md`: what the project is, current state, data sources, findings, Apify spend, open items.
2. `DECISIONS.md`: every decision and why. Don't reverse one without asking the user.
3. `CHANGELOG.md`: what changed and when, newest at the bottom.
4. `DESIGN.md`: the V7 brand design system. Every visual change follows it.

## Keep them current
After every change (dashboard edit, publish, data pull, new finding, user decision), in the same turn and before reporting back:
- add an entry to `CHANGELOG.md` (date, version, what changed, files touched);
- add new decisions to `DECISIONS.md` (number, date, decision, why, source);
- update the affected parts of `PROJECT_MEMORY.md` (state, numbers, Apify spend, open items);
- save raw data from any new collection under `data/raw/` (never only in a temp folder).

## How the user likes to work
- Asked for ideas: give ideas only. Build only when asked.
- A real working dashboard with demo data, not a report.
- Everything the dashboard shows must be obtainable from real data. Check with a tiny real call first (Apify `resultsLimit` 3 to 5, a cost cap on every run). Remove what can't be covered. Label real and demo data clearly.
- Before calling work done:
  - review as V7's marketing manager and as a UI/UX reviewer;
  - run the tests in `tests/` (desktop, tablet, phone, dark mode).
- Dashboard copy must not read as AI-written:
  - no "AI" in the interface;
  - no greetings, hype words, em dashes or "in the live version" notes.
- Emails to V7:
  - written as an internal employee proposing to the marketing manager;
  - no "I've built", no demo request, no mention of attachments;
  - don't name the dashboard, and use a plain greeting.

## Repository map
| Path | What it is |
|---|---|
| `V7_Pulse_Dashboard.html` | **The dashboard.** One complete HTML page (about 4,600 lines, 5.9 MB): CSS, data and a vanilla-JS app in one IIFE. No dependencies apart from Google Fonts. Its post images are files it links to in `data/raw/media_13oct/img/` (no size budget since DECISIONS #170), so it shows them when opened from this folder. |
| `V7_Pulse_Costs.html` | Yearly cost calculator for the hosted version (fixed plus variable costs, three Claude model pickers). |
| `V7_Pulse_Proposal.html` | The first proposal page (3 Oct 2026; its cost box is out of date). |
| `docs/` | The **public site**: `index.html` (the dashboard with its image links pointed at `media/`) and `media/` (the post images), built by `deploy/build_sites.py`. GitHub Pages serves this folder. It's the whole site: see "Hosting". Never edit it by hand. |
| `deploy/build_sites.py` | `dashboard`: copies the dashboard to `docs/index.html` and the images it links to into `docs/media/`. `costs`: the calculator copy in `deploy/v7-pulse-costs/` (a separate clone of `mohanadabouserie/v7-pulse-costs`, not in this repo). |
| `archive/dashboard_versions/`, `archive/costs_versions/` | Earlier versions, saved before the next edit. Up to v33 they embed their images; v34 is the last copy published to claude.ai. |
| `tests/` | Playwright checks, one file per version that changed something (`test_v5.py` … `test_v24.py`), plus `test_ai.py`, `test_market.py`, `test_reg5.py`, `test_costs.py`, `test_noon_llm.py`, `test_bot.py` (with `fake_claude.py`, a stand-in for Claude Code). `test_v25.py` checks the real data, the privacy rules and that no demo is left outside Market; `test_v26.py` the wider search and the YouTube comments; `test_v27.py` "likes hidden"; `test_v28.py` the reels' speech and follower counts; `test_v29.py` the wider Instagram search, the comments under public Instagram posts and the pictures read; `test_v30.py` the same for Facebook; `test_v31.py` Facebook reels and the five post searches; `test_v34.py` creators speaking Egyptian Arabic in the Egypt views; `test_v37.py` the Posts & comments grid, name, default sort and filters; `test_pipeline.py` the refresh pipeline, against stand-ins for Apify and Telegram. |
| `data/collect_store_history.py`, `data/noon_llm.py` | The daily online-store check (Amazon.eg, Carrefour, Noon). Noon is read by Claude from the page. Not scheduled. |
| `data/store_history/` | One JSON snapshot per real check (from 4 Oct 2026). |
| `data/raw/` | Raw data from every test and collection, with the scripts that made it. The map is in `PROJECT_MEMORY.md` section 10. |
| `data/raw/social/rumors_11oct/` | The Rumors & attacks pipeline (see "Data pipelines"). |
| `data/raw/real_17oct/` | **The real social data (Versions 25 and 26):** `PLAN.md` (budget and window), `collect.py`, `normalize.py`, `label.py` (Claude), `build_real.py --inject`, raw files in `raw/`, `SCRAPERS.md` (every scraper's link, input, output and cost, written by `scrapers_report.py`), and `pipeline.py` (the refresh pipeline, `PIPELINE.md`). See "Data pipelines". |
| `bot/` | The Telegram bot @v7_pulse_bot: `v7pulse_bot.py` (daily brief, Act now alerts, questions), `dashboard_reader.py` (reads the website copy in a headless browser), `claude_tools_mcp.py` (the dashboard's eight read-only Claude tools for Claude Code, which answers questions), `README.md`, a systemd service file. State in `bot/state/` (ignored). One copy runs at a time; its process id is in `bot/state/bot.pid` |
| `Ask_V7_Pulse/` | Hosted-version setup for the chat: system prompt, 14 tool definitions, Apify allowlist. |
| `scripts/` | Apify helper runners from the first tests. |
| `Reference docs/` | Third-party PDFs. Kept locally only, and git-ignored. |

## Setting up a machine
- **Python 3.12** with Playwright for the tests: `pip install playwright` then `python3 -m playwright install chromium`.
- **Anthropic SDK** for the Noon reader. Ubuntu blocks system pip (PEP 668), so use the project venv:
  - create it with `python3 -m venv data/.venv` then `data/.venv/bin/pip install anthropic`;
  - run the Noon scripts with `data/.venv/bin/python`.
- **Secrets aren't in the repo.** Create these locally; `.gitignore` covers every `.env.*`:
  - `.env.apify` with `APIFY_API_TOKEN=…`. Load it with `set -a; . ./.env.apify; set +a`.
  - `.env.anthropic` with `ANTHROPIC_API_KEY=…`, for `data/noon_llm.py`.
  - `.env.meta` with `META_SYSTEM_USER_TOKEN=…`, when V7 connects its Facebook and Instagram accounts.
  - `.env.telegram` with `TELEGRAM_BOT_TOKEN=…` and `TELEGRAM_JOIN_CODE=…`, for the Telegram bot (the plain `telegram_key` file is ignored too).

## The dashboard code
- **One IIFE.** Nothing is global, so tests read the page through the DOM, not through JS variables.
- **Main sections, in file order** (search for the comment headers):
  - Utilities and Reference data: products (`PRODUCTS`, with can colours), `EVENTS`, countries;
  - demo post generation for Egypt and abroad;
  - **Rumors & attacks data:** `FACTS`, the generated `RUMOR_DATA` block, `CAMPS` (the real claims), and `CINFO` (status, risk and coordination signals);
  - comments, account insights, then State & filtering (`state`, `bounds()`);
  - renderers (`kpi`, `bars`, `sortTable`, `postCard`), charts, insight text;
  - the Egypt and Outside Egypt views;
  - Online stores (real snapshots plus the daily history engine), Restaurants (real Talabat), Search trends (real Google Trends);
  - the Rumors & attacks view (`vRadar`), the post view (`openPost`), alert plans and previews (`alertPlan`, `openAlertPreview`), "Needs your attention" (`attentionCards`), the Daily brief (`briefFor`, `vBrief`), Events, drawers, Ask V7 Pulse;
  - global controls (`onAct` switch on `data-act`), then `render()`.
- **Views:** the `VIEWS` map routes each sidebar `data-view` to its function. Each view writes `content.innerHTML`. Charts that need sizes are pushed to `HOOKS` and run after render.
- **Interaction:** any element with `data-act="…" data-v="…"` is handled in `onAct`. Rows that open details carry `tabindex=0`, so Enter and Space work.
- **Real data everywhere (Version 25):**
  - V7 Egypt's posts and every comment on them (with V7's and V Super Soda's replies), the pages abroad, the public posts about V7 from six platforms (searched widely since Version 26), and the comments under the public YouTube videos about V7, 20 Apr to 16 Oct 2026, each labelled by Claude. Followers checked 13 Oct.
  - YouTube comments carry a day but no time (`nt`); older ones only a month (`da`, shown as "about 4 months before 18 Oct" under their video and not counted by day).
  - The only demo left is inside Market, which the user asked to leave as it is: the store history before 4 Oct is drawn hatched and labelled demo.
  - Not shown, because they need V7's own account insights: profile visits and follower details.
  - The header badge (`#dataBadge`) says "Real data" on every view, with the check date in its tooltip. Keep it honest when you add a view.
  - Views and engagement count on the day the post went up (DECISIONS #114). No estimated reach: views, otherwise engagement (#115).
- **Generated blocks, don't hand-edit:**
  - `/*RUMOR_DATA*/…/*END_RUMOR_DATA*/` is written by `build_rumors.py --inject`;
  - `/*REAL_OWN*/…/*END_REAL_OWN*/` and `/*REAL_OWN_X*/…/*END_REAL_OWN_X*/` (V7's own posts, in Egypt and abroad) are written by `data/raw/verify_13oct/build_own_posts.py --inject`;
  - `/*MEDIA*/…/*END_MEDIA*/` (each real post's image file, `data/raw/media_13oct/img/…`, keyed by the post link) is written by `data/raw/media_13oct/build_media.py --inject`;
  - `/*REAL_OWN*/`, `/*REAL_OWN_X*/` and `/*REAL_DATA*/…/*END_REAL_DATA*/` (public posts, comments, anonymous authors) are written by `data/raw/real_17oct/build_real.py --inject` since Version 25.
- **The file has very long lines** (one data line is 137K characters). Edit with exact-match replacements, not by retyping lines. Read with offsets.
- **Class names:** never reuse `demo`, `real`, `st` or `pill` for new elements; they're badge styles (DECISIONS #69).

## Running the tests
- **All dashboard suites** (each prints `FAIL 0` when clean):
  `for t in test_v5 test_v8 test_v11 test_v13 test_v14 test_v15 test_v16 test_v18 test_v20 test_v21 test_v22 test_v23 test_v24 test_v25 test_v26 test_v27 test_v28 test_v29 test_v30 test_v31 test_v34 test_v37 test_ai test_market test_reg5; do python3 tests/$t.py | tail -1; done`
- **The public copy:** prefix with `DASH_SRC=file://$PWD/docs/index.html`.
- **The calculator:** `python3 tests/test_costs.py`. Prefix with `COSTS_SRC=…` for its hosted copy.
- **The Noon reader:** `data/.venv/bin/python tests/test_noon_llm.py`. It uses a local stand-in for the API, so it needs no key and costs nothing.
- **The refresh pipeline:** `python3 tests/test_pipeline.py`. Stand-ins for Apify and Telegram, so it needs no token and spends nothing.
- **The Telegram bot:** `python3 tests/test_bot.py`. Stand-ins for Telegram and for Claude Code, so it needs no token or account and spends nothing. It reads the real dashboard; prefix with `DASH_SRC=file://$PWD/docs/index.html` for the copy the live bot reads.
- Tests find the dashboard relative to the `tests/` folder, so they run from any checkout.

## Publishing
- **The dashboard is published only as the public site,** https://mohanadabouserie.github.io/v7-pulse/, served from `docs/` in this repo.
  - Steps: before editing, copy the dashboard to `archive/dashboard_versions/V7_Pulse_Dashboard_vN.html` (N = the version you're replacing); then run `python3 deploy/build_sites.py dashboard`, run the dashboard tests (also with `DASH_SRC` on `docs/index.html`), and commit and push.
  - Pushing changes a public site, so ask the user first.
- **The claude.ai copy is retired** (DECISIONS #170, 21 Oct 2026): https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc stays as Version 34 and is no longer updated. Nothing has to fit it any more: no 16 MB page limit, no embedded images, no missing doctype. Ask V7 Pulse's Claude path (`window.claude.use('sample')`) only worked there; on the site the chat gives its short built-in answers. Claude answers on the site would need a small server holding an API key (`Ask_V7_Pulse/`, `PROJECT_MEMORY.md` section 8).

## Hosting
The site must keep working wherever it's hosted (GitHub Pages now; perhaps V7's own domain later). Rules:
- **`docs/` is the whole site.** `index.html` and `media/` go together; the page needs nothing else from this repo or this machine. Its only outside requests are Google Fonts and the links people click.
- **Every link inside the site is relative** (`media/<file>.jpg`), so `docs/` can be copied to any web host or folder as it is. Never point the page at `data/…`, a local path (`/Users/…`, `file://`) or `localhost`; `build_sites.py` stops if a `data/raw/media_13oct/img/` path is left in the built page.
- **The images could move to a CDN or object storage** (S3, Cloudflare R2): upload `docs/media/` and build with `MEDIA_BASE=https://…/ python3 deploy/build_sites.py dashboard`.
- **Data is built in, not fetched.** Posts, comments and numbers are inside `index.html`; a data refresh means rebuilding and redeploying. A live site that refreshes itself would need the pipeline on a server and the data as a separate file or an API: a later step, not built.
- **Before a real launch:** remove `<meta name="robots" content="noindex, nofollow">` from the dashboard if it should appear in search engines; it's there because the site is a demo. And check the privacy rules (private people anonymous, DECISIONS #75, #122) still hold for a wider audience: the images of public posts show what their authors posted.
- **The calculator** is published privately at https://claude.ai/artifact/7W1HvsWL1brdpe7eNxEx4P, with a public copy at https://mohanadabouserie.github.io/v7-pulse-costs/ (its own repo, cloned to `deploy/v7-pulse-costs/`).
  - On a new machine, clone it first: `git clone https://github.com/mohanadabouserie/v7-pulse-costs deploy/v7-pulse-costs`.
  - Before editing, copy it to `archive/costs_versions/V7_Pulse_Costs_vN.html`.
  - Then republish, and run `python3 deploy/build_sites.py costs` and `tests/test_costs.py`. Commit and push in `deploy/v7-pulse-costs/` after the user's OK.
  - When prices or the setup change, update the prices in its script (with the checked date in the comment) and the estimate in `PROJECT_MEMORY.md` section 8.

## Data pipelines
- **Online stores** (`data/collect_store_history.py`):
  - one run checks every tracked listing on Amazon.eg and Carrefour through Apify, and Noon's top 20 through `data/noon_llm.py`;
  - it writes `data/store_history/<date>.json`;
  - about USD 0.28 a day with competitors;
  - it's not scheduled: anything that spends money on a schedule needs the user's explicit OK.
- **Noon** (`data/noon_llm.py`):
  - curl with `--http2` (Noon stalls HTTP/1.1 clients), then Claude (`claude-opus-5-5`, effort low, JSON schema, server-side fallbacks) reads the listing;
  - every value is checked against the page text before it's kept.
- **Rumors & attacks** (`data/raw/social/rumors_11oct/`):
  1. `collect.py full|extra|test`: Apify searches on X, Facebook, Instagram and TikTok, with a USD cap per run and in total.
  2. `normalize.py`: one deduplicated list, `posts.json`. It drops the X actor's filler rows.
  3. `labels.json`: every post about V7, read and labelled by Claude. Each has the claim (`price`, `owner`, `alcohol`, plus `ingred`, `name`, `odd` for single posts), the stance (`spread`, `question`, `debunk`), kind, sentiment and an English note. New posts need labels before they show.
  4. `build_rumors.py --inject`: writes `rumors_dashboard.json` and the dashboard's `RUMOR_DATA` block.
  - Privacy: private people show as "X user". Names stay only for news outlets, shops, creators, official pages and accounts with 10K+ followers (DECISIONS #75).
  - Claim copy (titles, replies, actions) lives in `CAMPS` in the dashboard. Statuses come from the real dates (DECISIONS #74).
- **Restaurants:** Talabat menus and the brand rules are in `data/raw/talabat/` (`brands2.py`, `rest_rebuild.py`, `rest_final.json`). Some scripts there were written for a temporary folder, so check paths before rerunning.
- **Search trends:** `data/raw/google_trends/` (direct requests to Google Trends, free).
- **Real social data** (`data/raw/real_17oct/`, Version 25; plan and budget in `PLAN.md`):
  1. `collect.py test|own|comments|abroad|ugc`, then (18 Oct) `test2|wide|ttkw|ytcheck|ytc`: Apify runs, each with a USD cap and a budget line (`BUDGET`, `BUDGET_WIDE`, `BUDGET_YTC`); raw files in `raw/` are kept and not run again. Never use Facebook's comment date filter when the posts are already in the window (it's charged per comment).
     - `wide`: Instagram posts tagging V7's accounts, Instagram keyword search inside the window (seemuapps), Google searches of instagram.com and tiktok.com (finds dated from their ids, then fetched by link), TikTok from Egypt, more spellings on Facebook, X and YouTube.
     - `ytc`: YouTube comments (apidojo) on V7's videos and on the public videos about V7.
     - `igkw`: Instagram keyword search (apidojo + dami_studio, re-fetch by link). `igprofiles`: follower counts. `igspeech`: what's said in reels (speech to text); `label.py` labels reels again once they have speech.
     - 19 Oct (Version 29): `igcover` (Google one month at a time, every post tagging @v7egypt since 20 Apr, 8 more hashtags, a seemuapps sample; with `igkw --since 2026-04-20`), `igcomments` then `igcomments2` (comments under the public Instagram posts about V7: scrapesmith, then Apify's own scraper for the posts it returned nothing for), `igvisfetch` (fresh media links for the posts whose pictures are read). `vistest`, `vistest2` and `covtest` were the tests.
     - 19 Oct (Version 30), Facebook (`FB_KEYWORD_SCRAPERS.md`, `fbtest_report.py`): `fbtest` and `fbtest2` were the tests; `fbcover` (30 keywords on silentflow, scraper_one and Apify's search, the reel search, three video searches, public groups, Google month by month), `fbdetails` (new reels, videos and Google links by link, danek), `fbfill` (plays, speech with invideoiq, page followers, comments with thedoor), `fbfill2` (Apify's comment scraper for the posts thedoor missed), `fbviews` (plays of video posts behind post links). Then `vis_media.py --fb` and `vis_read.py`.
     - Version 31: `fbreeltest` and `fbreeldetails` (13 reel searches compared, `fbreel_report.py`), `fbreels` (Google's short videos limited to Facebook and alien_force's reels-only search, new reels by link), `fbmore` (scrapeforge and fetch_cat on all 30 keywords), `fbnames` (account names a search row lacked).
     - Pictures: `vis_media.py` (run with `data/.venv/bin/python`, which has ffmpeg) downloads photos and a frame every 2 seconds of a video into `vis/`; `vis_read.py` has Claude Code (bot's sign-in, Read tool only) write the text on them and what they show to `vis_read.json`. `normalize.py` attaches it as `seen` and `label.py` labels the post again (`vs`).
  2. `yt_pages.py`: exact dates for V7's YouTube videos from their public pages (free).
  3. `normalize.py`: one list (`items.json`), Cairo time, deduplicated; collaboration posts filed under their V7 page; replies linked. V Super Soda counts as V7 (DECISIONS #118).
  4. `label.py`: Claude Code with the bot's sign-in (the user's personal Max plan), Opus 5.5 at low effort, 40 items a batch, JSON schema; resumable. `labels.json` holds every label.
  5. `build_real.py --inject`: writes the three blocks. Private people anonymous, @mentions masked (DECISIONS #122); off-topic comments dropped but emoji and tags kept (#120).
  6. `fetch_media.py`, then `../media_13oct/build_media.py --inject`: images for V7's posts, the top abroad posts and the top 80 public posts.
  7. `scrapers_report.py` (with the Apify token in the environment): `SCRAPERS.md` and `runs_final.json`, each run's final charge. It counts the links and accounts a run was given instead of printing them (DECISIONS #157).
  - 20 Oct (Version 33): `fbdays` (Facebook's own search one day at a time, sorted by latest, on the busiest days), `gweeks` (Google's site search one week at a time), `slicefetch` (their new finds by link), `igrepeat` and `accounts` (ideas 1 and 2, tried and not taken further). `routes_report.py` writes `ROUTES_20OCT.md`: what each route added.
  8. `pipeline.py plan|run|status` (`--mode sweep|daily|weekly|fill`, `--max-usd`, default 10): steps 1 to 6 for Facebook and Instagram in one command (`PIPELINE.md`, DECISIONS #152–158).
     - Each route has standby scrapers that write the same format, every run is health-checked, and each run has a spending line that the gap fillers obey too.
     - It also keeps a lock, a ledger and a report per run (git-ignored), and sends a Telegram message to the bot's admins. `plan` spends nothing.
     - Not scheduled: `daily` and `weekly` need the dashboard's window to roll past 16 Oct first, and the user's OK for the spending (DECISIONS #154). The systemd files in `deploy/` aren't installed.
  - `raw/`, `items.json`, `labels.json`, `vis/` and `vis_read.json` name or show private people, so they're git-ignored and stay on this machine. Never commit them: the repo is public.
- **V7's own posts** (`data/raw/verify_13oct/`):
  1. `own_pull.py`: Instagram profiles (V7 Egypt, the pages abroad, the UK distributor), V7Egypt's Facebook posts, TikTok and the YouTube channel.
  2. `own_pull2.py`: YouTube likes and dates, the page's followers, and launch comments. Older posts back to 16 Apr: `data/raw/own_backfill_13oct/pull.py` and `yt_pages.py`.
  3. `build_own_posts.py --inject`: writes the `REAL_OWN` and `REAL_OWN_X` blocks. When you pull again, update its follower counts (`FOL`) and first-post dates (`COVER`), and the followers in `OWN` and `OWN_X`.
  - Total cost about USD 0.20.

## Secrets and spending
- **Apify:** the token is in `.env.apify` and `apify_key` (both gitignored). Never print, copy or commit it. Load it into the environment only.
- **Telegram:**
  - The bot token is in `.env.telegram`. Never print it, log it, commit it, or put it in the dashboard; `test_v24.py` checks the page for it.
  - The join link is private too.
  - If the token leaks, revoke it in @BotFather.
  - The bot's Claude sign-in is in `bot/state/claude/` (ignored). Never print or copy its `.credentials.json`.
  - Don't sign the bot in with the user's work account (another company's Claude Team plan, and the CLI's default login on this machine): V7's data shouldn't go through another company's Claude account. The bot refuses any organization listed in `CLAUDE_BLOCKED_ORGS` in `.env.telegram` (DECISIONS #112). Never write that organization's name in a tracked file: the repo is public.
  - The bot runs on the user's machine. Restart it with `kill $(cat bot/state/bot.pid)`, then `setsid nohup python3 bot/v7pulse_bot.py >> bot/state/stdout.log 2>&1 < /dev/null &` (never `pkill -f`, which can match your own shell).
- **Meta and Anthropic:** the Meta token goes in `.env.meta` as `META_SYSTEM_USER_TOKEN=…`. It's a system-user token; scripts get the Page token from it at run time with `/me/accounts`. The Anthropic key goes in `.env.anthropic`. The same rules apply to both: never print them, never put them in the dashboard file, and never ask anyone to paste them in chat.
- **GitHub:** never print a `gh` token (`gh auth token`, `gh auth status -t`). Creating repos, changing access or settings, or pushing anything public needs the user's OK.
- **Apify budget:** the Starter plan includes USD 19 a month; since 19 Oct the user's usage limit is USD 100, and anything above USD 19 is billed as overage (the cycle resets on the 16th). The spend so far is in `PROJECT_MEMORY.md` section 9. Test with 3 to 5 results first, and put a cost cap on every run.
- **Polite fetching:** fetch talabat.com and other sites one request at a time, at least 1 second apart.

## Known quirks
- The dashboard has its own doctype and viewport since 21 Oct (DECISIONS #170). `V7_Pulse_Costs.html` still has none (the claude.ai viewer adds it); `build_sites.py costs` adds it for its public copy.
- X actor (`kaitoeasyapi`):
  - returns at least 20 items a run, padding with filler rows ("From KaitoEasyAPI, a reminder…");
  - its search reaches back years, so check dates.
- TikTok actor (`clockworks`): rejects a cost cap under USD 0.50.
- "V7" collides with:
  - the Haval V7 car, the V7 climbing grade, and software and crypto "v7" releases;
  - "في سفن" means "in ships", and in Saudi posts "سفن" is 7UP;
  - Cambodia has its own "V-Cola".
- Self-declared profile locations are unreliable. Don't use them to place posts (DECISIONS #76).
- A post's country comes from Claude's label, and reading a video's speech can move it abroad ("filmed here in England"). A creator posting in Egyptian Arabic still counts in Egypt (`build_real.py`, DECISIONS #168); businesses, Egyptians abroad and locals keep their country. Every Egypt view filters on `cty === 'EG'`.
- TikTok (`clockworks`): its own date filter (`videoSearchDateFilter`) returns unrelated videos. Search with `proxyCountryCode: "EG"` and no date filter, then check dates.
- Instagram: the hashtag #vcola is mostly Cambodia's V-Cola. Its keyword search returns the top results for a word (a few hundred), so add the posts that tag @v7egypt and Google's finds.
  - The keyword search (seemuapps, 19 Oct check) matches loosely: Arabic spellings returned almost nothing about V7 (ڤي سڤن 1 of 30, في سفن 0 of 30: ships, Starbucks, BTS's "V"); English and mixed phrases worked (V7 soda 24 of 30, V7 Egypt 22, مشروب V7 19). Use English or mixed phrases there; its counts matched Apify's own scrapers.
- Arabic spellings, on every platform (19 Oct check of the 17–18 Oct searches):
  - with ڤ they work: ڤي سڤن 25 of 29 about V7 on Facebook, ڤي كولا 26 of 30 on Facebook and 10 of 13 on TikTok; Arabic mixed with V7 too (V7 كريم صودا 20 of 30 on Facebook);
  - with ف they don't: في سفن is "in" + "ships" (and 7UP in Saudi posts), so في سفن مشروب got 2 of 30 on Facebook and 0 of 13 on TikTok, في كولا 1 of 30. Don't search the ف spellings;
  - for Arabic on Instagram use the posts that tag V7 and Google's exact-phrase search ("ڤي سڤن" site:instagram.com: 7 of 11), not Instagram's own keyword search.
- Instagram keyword search uses apidojo plus dami_studio's Reels search (`collect.py igkw`, DECISIONS #133–134): English and mixed phrases, 10 apidojo results and 30 reels per keyword (past 10, apidojo's rows lack captions and likes). Neither returns the account's follower count; apidojo has no share count. Rows without a caption or likes are re-fetched by link with Apify's post scraper (DECISIONS #135); that closes captions, likes, comments and plays, but not hidden likes, follower counts or shares. Instagram's search shuffles results between sessions, and its Reels search (dami_studio) finds reels the posts search misses. No scraper finds everything.
- Instagram comments: scrapesmith (USD 0.0005 a comment) matched Apify's own scraper on a small test but returned nothing for 137 of 251 posts at full scale. Check what came back per post and send the rest to `apify~instagram-comment-scraper`.
- apify/instagram-tagged-scraper (19 Oct run) returned "Access delayed. Only the owner of the page can access this information" as `ownerFullName` on 201 of 520 posts. `normalize.py` drops it (`NOT_A_NAME`) and takes the name from the profile scraper, else the handle.
- Facebook search (19 Oct tests): only the first 10-15 results per keyword are about V7; past that, and one month at a time, it returns unrelated posts (a shop called "Seven", people with ڤ in their names). More keywords and other backends help, depth doesn't. Arabic with ڤ works on Facebook. The post-search scrapers mostly share one backend (silentflow, scrapeforge, danek, igview, topapi, fetch_cat); scraper_one and Apify's search rank differently.
- Facebook gives the same post a post id (the searches) and a video id (/reel/<id>, /videos/<id>); `normalize.py` links them (`FB_ALIAS`) so it's counted once.
- Facebook reels: Facebook's own reel and video searches return mostly the same reels; Google's short-videos search limited to Facebook (`simple.actor/google-short-videos`, platform facebook) finds reels they don't. Use both (DECISIONS #149).
- Facebook media links expire within days, and some return a login page: `vis_media.py` refuses files that aren't images (DECISIONS #151).
- Apify's API can return a 502 mid-stage; `collect.py`'s `api()` retries reads. If a stage still stops, save the started run's items by its id instead of starting it again.
- Facebook hashtags: Apify's hashtag scraper returns "Empty or private data". Apify's video search returns some broken rows (`facebook.comundefined`). The public-group search (lofomachines) failed after 62 posts. invideoiq charges USD 0.035 more for each 10 minutes past the first.
- dami_studio's Reels search delivers at most 100 reels a run, so `igkw` splits the keywords into runs of three.
- Google one month at a time (`tbs=cdr:1,cd_min:…,cd_max:…`): share of finds that were new posts about V7, 19 Oct: "@v7egypt" 60%, "V7 cream soda" 41%, "V Cola" 37%, "مشروب V7" 31%, "ڤي سڤن" 24%, but "V7" 5% and "V Orange" 6%. Drop those two.
- `run()` in `collect.py` skips a run whose `raw/<name>.json` exists, so a stage run again needs a new name (the newer stages add a timestamp).
- Don't wrap a collect stage in a short `timeout`: the local script dies but the Apify run goes on and is billed. If it happens, save the run's items by its id rather than starting it again.
- Google's site search only covers what Instagram lets search engines index: public posts and reels since 1 Jan 2020 from accounts that meet Instagram's criteria (no private accounts, no stories). New posts usually reach it within about a day but can take days: on 18 Oct only 1 of its 203 Instagram links was from the last 2 days. Use it alongside the tagged posts and the keyword search, not instead.
- YouTube:
  - `streamers/youtube-channel-scraper` returns English machine translations of V7's Arabic titles; `calm_builder/youtube-scraper` gives the originals.
  - Comment dates are relative ("8 days ago", "4 months ago"); apidojo turns some into a date on the run's day of the month (18 May …), which is still month-only.
- Minimum cost caps: USD 0.50 for TikTok, Google search and calm_builder. `collect.run` asks again with the scraper's own minimum when a start is refused for that reason, and only if it fits under the budget line. Never retry a run the budget guard skipped.
- Date slices (20 Oct test, `DATESLICE_TEST.md`):
  - Facebook's own search takes a one-day window (start = end date) on scraper_one and silentflow. scraper_one sorted by latest found posts on a busy day that no search over the whole window had (15 Aug: 7 new from one keyword); a month sorted by top returns filler.
  - Google's site search with one-day ranges keeps to the day, but quiet days are filled with near matches (Cambodia's V-Cola, other colas): 10 of 295 new Instagram finds were about V7. Week ranges did better per dollar. The snippet can't pre-filter: the phrase is missing from it for about half the posts about V7.
- Runs started together (`parallel()`) each hold their cap against the budget line until they end (`collect.run`, DECISIONS #160).
- One-day Facebook searches pad their results with that day's other posts: only about a quarter are about V7. So a short-caption video is transcribed only when a keyword search over a long window found it (`collect.wide_search`, DECISIONS #164), and the comment fallbacks only take what the cheap scraper was asked about and missed (#165).
- scrapesmith (cheap Instagram comments) returned nothing for all 89 posts on 20 Oct; `igcomments2` sends those to Apify's own scraper.
- The Hashtags view drops generic tags by prefix (`GENERIC_RX`: #fyp, #foryou, #viral, #explore and their variants).
- Images: `fetch_media.py` downloads one for every post in the dashboard that has an image link, and `build_media.py` links every downloaded one (no budget since DECISIONS #170; until then 6,000 KB embedded, for the claude.ai limit). `test_v23.py` still holds the page under 13 MB.
- The artifact publish guard (claude.ai, retired; the escaping is kept and still tested):
  - it takes a page for a code-review page, and refuses it over 512 KB, when an `id=` is followed by more than 2,048 characters with no space (a Facebook link ending in `&id=…` before image data did it);
  - the data builders write that `=` as `\u003d`, and `test_v25.py` checks the page (DECISIONS #124);
  - it also refuses U+FFFD characters, which `normalize.py` strips.

## Open items
See `PROJECT_MEMORY.md` section 11.
