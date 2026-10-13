# V7 Pulse

A social listening and market dashboard for V7, the Egyptian vitamin soda.

- **Live copy:** https://mohanadabouserie.github.io/v7-pulse/
  - Ask V7 Pulse gives short built-in answers here.
  - The full version with Claude answers runs as a private claude.ai artifact.
- **What's real:**
  - online stores (Amazon.eg, Carrefour Egypt, Noon);
  - restaurant menus (Talabat, 10 Cairo areas);
  - Google search trends;
  - Rumors & attacks (public posts from X, Facebook, Instagram and TikTok, read one by one);
  - V7's own posts on Facebook, Instagram, TikTok and YouTube since April, and its follower counts;
  - V7's pages abroad and their latest posts.
- **What's demo:** the other social posts are generated for illustration and labelled as demo in the dashboard.

## Files
- `V7_Pulse_Dashboard.html`: the dashboard. One file, open it in any browser.
- `docs/`: the public copy, built by `python3 deploy/build_sites.py dashboard`.
- `V7_Pulse_Costs.html`: yearly cost calculator for a hosted version.
- `data/`: collectors and raw data.
- `tests/`: browser checks (Playwright).
- `PROJECT_MEMORY.md`, `DECISIONS.md`, `CHANGELOG.md`, `DESIGN.md`: the project's state, decisions, history and design system.
- `CLAUDE.md`: working notes for Claude Code sessions. Read it first if you edit with Claude.

## Run the checks
```bash
pip install playwright && python3 -m playwright install chromium
python3 tests/test_v22.py
```
Each test prints `FAIL 0` when everything passes.

API keys aren't in the repo. See `CLAUDE.md`, "Setting up a machine".
