# V7 Pulse on Telegram (@v7_pulse_bot)

The bot sends the marketing team what the dashboard shows:
- **the daily brief** at 09:00 Cairo time. Each chat gets each day's brief once, so when the dashboard has no new day of data, nothing is sent;
- **"Act now" alerts** as soon as they're found (checked every 2 hours), once per chat. Watch and Opportunity alerts are in the brief;
- **answers to any question**, from Claude, the way Ask V7 Pulse answers on claude.ai (see below). Until Claude is signed in, the website's built-in answers.

It reads everything from the dashboard itself (`dashboard_reader.py` opens it in a headless browser), so Telegram and the website always agree.

## Commands
The bot's menu in Telegram lists the first five.

| Command | What it does |
|---|---|
| `/brief` | The latest brief. `/brief 1` is the day before, up to `/brief 6`. |
| `/alerts` | What needs attention, with next steps and owners |
| `/ask question`, or just type | Ask V7 Pulse's answer |
| `/help` | What the bot sends |
| `/stop` | Stop the brief and alerts in this chat |
| `/subscribers`, `/remove id`, `/test` | Admin only: who gets the reports, take someone off, send yourself a sample alert |

## Questions answered by Claude
Any question goes to Claude Code, which gets the dashboard's own instructions and its eight read-only tools (`claude_tools_mcp.py`: overview, posts, breakdowns, V7's accounts, stores, restaurants, risks and events, outside Egypt). The answer arrives in the chat in about 10 to 60 seconds, while the bot keeps working. Follow-up questions see that chat's last three questions and answers, kept in memory for two hours and never saved.

**Sign the bot in to Claude, once.** From the project folder:
```bash
CLAUDE_CONFIG_DIR="$PWD/bot/state/claude" claude auth login
```
- Pick your own Claude account in the browser, not your work account. If the browser is signed in to another account on claude.ai, open the link the command prints in a private window instead, and paste the code it shows back into the terminal.
- To switch accounts later, sign the bot out first: the same command with `logout` instead of `login`.
- The bot refuses any organization listed in `CLAUDE_BLOCKED_ORGS` in `.env.telegram` (comma-separated). A question then gets the built-in answer, with a line saying why.
- The sign-in stays in `bot/state/claude/` (ignored by git). The bot notices it within a minute, without a restart.
- Questions then count toward that account's Claude plan.

**Once there's an API key:** put `ANTHROPIC_API_KEY=…` in `.env.anthropic`. The bot then uses the API instead of the plan.

**Locked down:** Claude Code runs with:
- no built-in tools (no files, shell or web);
- no other tool servers, settings or plugins;
- an empty folder and a clean environment, so no tokens from this machine;
- only the dashboard's eight read-only tools.

**Limits and fallbacks:**
- 100 questions a day (`V7_CLAUDE_PER_DAY`), two at a time, one at a time per chat, three minutes each.
- Model: Opus 5.5 at medium effort (`V7_CLAUDE_MODEL`, `V7_CLAUDE_EFFORT`). If the plan doesn't include it, the plan's default model.
- When Claude can't answer (not signed in, the plan's limit reached, too slow), the built-in answer comes instead, with a line saying why.

## Who can use it
- **Joining:** people join with the private link `https://t.me/v7_pulse_bot?start=<join code>`. The first person to join becomes the admin and hears whenever someone else joins.
- **On joining:** a welcome, the latest brief, and any Act now alert that's open.
- **Groups:** add the bot to a group, then type `/start <join code>` in it.
- **Everyone else** gets a short note and nothing else. That includes people who find the bot in Telegram search or on the public website.
- **If the link leaks:** change `TELEGRAM_JOIN_CODE` in `.env.telegram` and restart the bot. The old link stops working; take anyone unwanted off with `/remove`.
- A chat that blocks the bot, or is deleted, is taken off the list.

## Secrets and state (never committed)
- **`.env.telegram`** in the project folder:
  - `TELEGRAM_BOT_TOKEN=…` from BotFather;
  - `TELEGRAM_JOIN_CODE=…`.
- **`bot/state/`:**
  - `subscribers.json` (chat ids and names, plus the last brief and the alerts each chat has had);
  - `sent.json` (Telegram's update offset, the day of the last 09:00 run);
  - `claude/` (the bot's Claude sign-in: never copy or share it), `claude_use.json` (questions to Claude today), `claude_tools.json`;
  - `bot.log`, and `bot.pid` (the running copy's process id).
  - The log never contains the token.
- **If the token leaks:** in Telegram, open @BotFather, then `/revoke`. Put the new token in `.env.telegram` and restart the bot.

## Run it
```bash
python3 bot/v7pulse_bot.py
```
It needs Python 3.12 with Playwright (`pip install playwright`, then `python3 -m playwright install chromium`).

By default it reads the website's copy in `docs/index.html`. Set `DASH_URL` to read another copy, for example the hosted one.

Only one copy runs at a time: a second one stops with "already running". Don't run it on two machines with the same token, because both would send the brief.

To stop it:
```bash
kill $(cat bot/state/bot.pid)
```

To start it in the background, detached from the terminal:
```bash
setsid nohup python3 bot/v7pulse_bot.py >> bot/state/stdout.log 2>&1 < /dev/null &
```

## Test it
```bash
python3 tests/test_bot.py
```
It talks to stand-ins for Telegram and for Claude Code (`tests/fake_claude.py`), so it needs no token or account and spends nothing. It reads the real dashboard and runs the real tool server.

## Keep it running
It runs while the computer it's on is awake. If the computer sleeps through 09:00, the brief goes out when it wakes.

**On this machine, as a user service:**
- Stop the copy that's running (see above).
- Copy `v7pulse-bot.service` to `~/.config/systemd/user/`.
- Enable and start it:
  ```bash
  systemctl --user enable --now v7pulse-bot
  ```
- See its log:
  ```bash
  journalctl --user -u v7pulse-bot -f
  ```

**On the planned VPS:** the same service file, with the paths changed. The bot needs no open ports: it asks Telegram for messages (long polling), so no webhook or domain is needed.
