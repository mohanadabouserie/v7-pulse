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
| `V7_Pulse_Dashboard.html` | **The dashboard.** One self-contained HTML file (about 4,400 lines, 680 KB): CSS, data and a vanilla-JS app in one IIFE. No build step and no dependencies apart from Google Fonts. |
| `V7_Pulse_Costs.html` | Yearly cost calculator for the hosted version (fixed plus variable costs, three Claude model pickers). |
| `V7_Pulse_Proposal.html` | The first proposal page (3 Oct 2026; its cost box is out of date). |
| `docs/` | The **public copy** of the dashboard, built by `deploy/build_sites.py`. GitHub Pages serves this folder. Never edit it by hand. |
| `deploy/build_sites.py` | Builds `docs/index.html` (adds doctype, viewport and noindex, and swaps the claude.ai-only chat line) and the calculator copy in `deploy/v7-pulse-costs/` (a separate clone of `mohanadabouserie/v7-pulse-costs`, not in this repo). |
| `archive/dashboard_versions/`, `archive/costs_versions/` | Every earlier published version, saved before the next edit. |
| `tests/` | Playwright checks, one file per version that changed something (`test_v5.py` … `test_v18.py`), plus `test_ai.py`, `test_market.py`, `test_reg5.py`, `test_costs.py`, `test_noon_llm.py`. |
| `data/collect_store_history.py`, `data/noon_llm.py` | The daily online-store check (Amazon.eg, Carrefour, Noon). Noon is read by Claude from the page. Not scheduled. |
| `data/store_history/` | One JSON snapshot per real check (from 4 Oct 2026). |
| `data/raw/` | Raw data from every test and collection, with the scripts that made it. The map is in `PROJECT_MEMORY.md` section 10. |
| `data/raw/social/rumors_11oct/` | The Rumors & attacks pipeline (see "Data pipelines"). |
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
  - the Rumors & attacks view (`vRadar`), Events, drawers, Ask V7 Pulse;
  - global controls (`onAct` switch on `data-act`), then `render()`.
- **Views:** the `VIEWS` map routes each sidebar `data-view` to its function. Each view writes `content.innerHTML`. Charts that need sizes are pushed to `HOOKS` and run after render.
- **Interaction:** any element with `data-act="…" data-v="…"` is handled in `onAct`. Rows that open details carry `tabindex=0`, so Enter and Space work.
- **Real or demo:**
  - Real: follower counts, V7 pages abroad, Online stores, Restaurants, Search trends, Rumors & attacks, the export facts, and the posts marked "Real post".
  - Everything else is seeded demo data.
  - The header badge (`#dataBadge`) switches per view. Keep it honest when you add a view.
- **Generated block, don't hand-edit:** `/*RUMOR_DATA*/…/*END_RUMOR_DATA*/` is written by `build_rumors.py --inject`.
- **The file has very long lines** (one data line is 137K characters). Edit with exact-match replacements, not by retyping lines. Read with offsets.
- **Class names:** never reuse `demo`, `real`, `st` or `pill` for new elements; they're badge styles (DECISIONS #69).

## Running the tests
- **All dashboard suites** (each prints `FAIL 0` when clean):
  `for t in test_v5 test_v8 test_v11 test_v13 test_v14 test_v15 test_v16 test_v18 test_ai test_market test_reg5; do python3 tests/$t.py | tail -1; done`
- **The public copy:** prefix with `DASH_SRC=file://$PWD/docs/index.html`.
- **The calculator:** `python3 tests/test_costs.py`. Prefix with `COSTS_SRC=…` for its hosted copy.
- **The Noon reader:** `data/.venv/bin/python tests/test_noon_llm.py`. It uses a local stand-in for the API, so it needs no key and costs nothing.
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

## Secrets and spending
- **Apify:** the token is in `.env.apify` and `apify_key` (both gitignored). Never print, copy or commit it. Load it into the environment only.
- **Meta and Anthropic:** the Meta token goes in `.env.meta` as `META_SYSTEM_USER_TOKEN=…`. It's a system-user token; scripts get the Page token from it at run time with `/me/accounts`. The Anthropic key goes in `.env.anthropic`. The same rules apply to both: never print them, never put them in the dashboard file, and never ask anyone to paste them in chat.
- **GitHub:** never print a `gh` token (`gh auth token`, `gh auth status -t`). Creating repos, changing access or settings, or pushing anything public needs the user's OK.
- **Apify budget:** the free plan has USD 5 a month (the cycle resets on the 2nd). The spend so far is in `PROJECT_MEMORY.md` section 9. Test with 3 to 5 results first, and put a cost cap on every run.
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

## Open items
See `PROJECT_MEMORY.md` section 11.
