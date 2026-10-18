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
| `V7_Pulse_Dashboard.html` | **The dashboard.** One self-contained HTML file (about 4,600 lines, 8.0 MB with the 431 images): CSS, data and a vanilla-JS app in one IIFE. No build step and no dependencies apart from Google Fonts. |
| `V7_Pulse_Costs.html` | Yearly cost calculator for the hosted version (fixed plus variable costs, three Claude model pickers). |
| `V7_Pulse_Proposal.html` | The first proposal page (3 Oct 2026; its cost box is out of date). |
| `docs/` | The **public copy** of the dashboard, built by `deploy/build_sites.py`. GitHub Pages serves this folder. Never edit it by hand. |
| `deploy/build_sites.py` | Builds `docs/index.html` (adds doctype, viewport and noindex, and swaps the claude.ai-only chat line) and the calculator copy in `deploy/v7-pulse-costs/` (a separate clone of `mohanadabouserie/v7-pulse-costs`, not in this repo). |
| `archive/dashboard_versions/`, `archive/costs_versions/` | Every earlier published version, saved before the next edit. |
| `tests/` | Playwright checks, one file per version that changed something (`test_v5.py` … `test_v24.py`), plus `test_ai.py`, `test_market.py`, `test_reg5.py`, `test_costs.py`, `test_noon_llm.py`, `test_bot.py` (with `fake_claude.py`, a stand-in for Claude Code). `test_v25.py` checks the real data, the privacy rules and that no demo is left outside Market; `test_v26.py` the wider search and the YouTube comments. |
| `data/collect_store_history.py`, `data/noon_llm.py` | The daily online-store check (Amazon.eg, Carrefour, Noon). Noon is read by Claude from the page. Not scheduled. |
| `data/store_history/` | One JSON snapshot per real check (from 4 Oct 2026). |
| `data/raw/` | Raw data from every test and collection, with the scripts that made it. The map is in `PROJECT_MEMORY.md` section 10. |
| `data/raw/social/rumors_11oct/` | The Rumors & attacks pipeline (see "Data pipelines"). |
| `data/raw/real_17oct/` | **The real social data (Versions 25 and 26):** `PLAN.md` (budget and window), `collect.py`, `normalize.py`, `label.py` (Claude), `build_real.py --inject`, raw files in `raw/`, and `SCRAPERS.md` (every scraper's link, input, output and cost, written by `scrapers_report.py`). See "Data pipelines". |
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
  - `/*MEDIA*/…/*END_MEDIA*/` (each real post's image as a data: URI, keyed by the post link) is written by `data/raw/media_13oct/build_media.py --inject`;
  - `/*REAL_OWN*/`, `/*REAL_OWN_X*/` and `/*REAL_DATA*/…/*END_REAL_DATA*/` (public posts, comments, anonymous authors) are written by `data/raw/real_17oct/build_real.py --inject` since Version 25.
- **The file has very long lines** (one data line is 137K characters). Edit with exact-match replacements, not by retyping lines. Read with offsets.
- **Class names:** never reuse `demo`, `real`, `st` or `pill` for new elements; they're badge styles (DECISIONS #69).

## Running the tests
- **All dashboard suites** (each prints `FAIL 0` when clean):
  `for t in test_v5 test_v8 test_v11 test_v13 test_v14 test_v15 test_v16 test_v18 test_v20 test_v21 test_v22 test_v23 test_v24 test_v25 test_v26 test_ai test_market test_reg5; do python3 tests/$t.py | tail -1; done`
- **The public copy:** prefix with `DASH_SRC=file://$PWD/docs/index.html`.
- **The calculator:** `python3 tests/test_costs.py`. Prefix with `COSTS_SRC=…` for its hosted copy.
- **The Noon reader:** `data/.venv/bin/python tests/test_noon_llm.py`. It uses a local stand-in for the API, so it needs no key and costs nothing.
- **The Telegram bot:** `python3 tests/test_bot.py`. Stand-ins for Telegram and for Claude Code, so it needs no token or account and spends nothing. It reads the real dashboard; prefix with `DASH_SRC=file://$PWD/docs/index.html` for the copy the live bot reads.
- Tests find the dashboard relative to the `tests/` folder, so they run from any checkout.

## Publishing
- **The private, full version** is a claude.ai artifact owned by Mohanad: https://claude.ai/artifact/JLUFSZEvjwCY3GVepHc7oc (declares the `sample` capability for Ask V7 Pulse).
  - Only a session with access to that artifact can republish it. Publish to the same URL and omit `capabilities`, so the stored declaration carries forward.
  - Before editing, copy the current file to `archive/dashboard_versions/V7_Pulse_Dashboard_vN.html` (N = the published version you're replacing).
- **The public copy** is https://mohanadabouserie.github.io/v7-pulse/, served from `docs/` in this repo.
  - Steps: run `python3 deploy/build_sites.py dashboard`, run the dashboard tests (also with `DASH_SRC` on `docs/index.html`), then commit and push.
  - Pushing changes a public site, so ask the user first.
  - The build swaps the chat line that points to claude.ai. If that text changes, update the swap in `deploy/build_sites.py`; the build stops if it can't find it.
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
  2. `yt_pages.py`: exact dates for V7's YouTube videos from their public pages (free).
  3. `normalize.py`: one list (`items.json`), Cairo time, deduplicated; collaboration posts filed under their V7 page; replies linked. V Super Soda counts as V7 (DECISIONS #118).
  4. `label.py`: Claude Code with the bot's sign-in (the user's personal Max plan), Opus 5.5 at low effort, 40 items a batch, JSON schema; resumable. `labels.json` holds every label.
  5. `build_real.py --inject`: writes the three blocks. Private people anonymous, @mentions masked (DECISIONS #122); off-topic comments dropped but emoji and tags kept (#120).
  6. `fetch_media.py`, then `../media_13oct/build_media.py --inject`: images for V7's posts, the top abroad posts and the top 80 public posts.
  7. `scrapers_report.py` (with the Apify token in the environment): `SCRAPERS.md` and `runs_final.json`, each run's final charge.
  - `raw/`, `items.json` and `labels.json` name private people, so they're git-ignored and stay on this machine. Never commit them: the repo is public.
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
- **Apify budget:** the Starter plan has USD 19 a month, which is also the hard ceiling (the cycle resets on the 16th). The spend so far is in `PROJECT_MEMORY.md` section 9. Test with 3 to 5 results first, and put a cost cap on every run.
- **Polite fetching:** fetch talabat.com and other sites one request at a time, at least 1 second apart.

## Known quirks
- The artifact viewer adds the page skeleton when publishing, so the source HTML has no doctype or viewport. Standalone copies get them from `build_sites.py`.
- X actor (`kaitoeasyapi`):
  - returns at least 20 items a run, padding with filler rows ("From KaitoEasyAPI, a reminder…");
  - its search reaches back years, so check dates.
- TikTok actor (`clockworks`): rejects a cost cap under USD 0.50.
- "V7" collides with:
  - the Haval V7 car, the V7 climbing grade, and software and crypto "v7" releases;
  - "في سفن" means "in ships", and in Saudi posts "سفن" is 7UP;
  - Cambodia has its own "V-Cola".
- Self-declared profile locations are unreliable. Don't use them to place posts (DECISIONS #76).
- TikTok (`clockworks`): its own date filter (`videoSearchDateFilter`) returns unrelated videos. Search with `proxyCountryCode: "EG"` and no date filter, then check dates.
- Instagram: the hashtag #vcola is mostly Cambodia's V-Cola. Its keyword search returns the top results for a word (a few hundred), so add the posts that tag @v7egypt and Google's finds.
  - The keyword search (seemuapps, 19 Oct check) matches loosely: Arabic spellings returned almost nothing about V7 (ڤي سڤن 1 of 30, في سفن 0 of 30: ships, Starbucks, BTS's "V"); English and mixed phrases worked (V7 soda 24 of 30, V7 Egypt 22, مشروب V7 19). Use English or mixed phrases there; its counts matched Apify's own scrapers.
- YouTube:
  - `streamers/youtube-channel-scraper` returns English machine translations of V7's Arabic titles; `calm_builder/youtube-scraper` gives the originals.
  - Comment dates are relative ("8 days ago", "4 months ago"); apidojo turns some into a date on the run's day of the month (18 May …), which is still month-only.
- Minimum cost caps: USD 0.50 for TikTok, Google search and calm_builder.
- The artifact publish guard:
  - it takes a page for a code-review page, and refuses it over 512 KB, when an `id=` is followed by more than 2,048 characters with no space (a Facebook link ending in `&id=…` before image data did it);
  - the data builders write that `=` as `\u003d`, and `test_v25.py` checks the page (DECISIONS #124);
  - it also refuses U+FFFD characters, which `normalize.py` strips.

## Open items
See `PROJECT_MEMORY.md` section 11.
