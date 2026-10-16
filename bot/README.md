# V7 Pulse on Telegram (@v7_pulse_bot)

The bot sends the marketing team what the dashboard shows:
- **the daily brief** at 09:00 Cairo time. Each chat gets each day's brief once, so when the dashboard has no new day of data, nothing is sent;
- **"Act now" alerts** as soon as they're found (checked every 2 hours), once per chat. Watch and Opportunity alerts are in the brief;
- **answers to questions**, the same as Ask V7 Pulse on the website (its built-in answers).

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
It talks to a stand-in for Telegram, so it needs no token and sends nothing. It reads the real dashboard.

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
