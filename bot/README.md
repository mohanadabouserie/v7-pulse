# V7 Pulse on Telegram (@v7_pulse_bot)

The bot sends the marketing team what the dashboard shows:
- **the daily brief** every morning at 09:00 Cairo time;
- **"Act now" alerts** as soon as they're found (checked every 2 hours). Watch and Opportunity alerts are in the brief;
- **answers to questions**, the same as Ask V7 Pulse on the website.

It reads everything from the dashboard itself (`dashboard_reader.py` opens it in a headless browser), so Telegram and the website always agree.

## Commands
| Command | What it does |
|---|---|
| `/brief` | Today's brief. `/brief 1` is yesterday's, up to `/brief 6`. |
| `/alerts` | What needs attention, with next steps and owners |
| `/ask question`, or just type | Ask V7 Pulse's answer |
| `/stop` | Stop the brief and alerts in this chat |
| `/subscribers`, `/remove id`, `/test` | Admin only: who gets the reports, take someone off, send yourself a sample alert |

## Who can use it
- **Joining:** people join with the private link `https://t.me/v7_pulse_bot?start=<join code>`. The first person to join becomes the admin.
- **Groups:** add the bot to a group, then type `/start <join code>` in it.
- **Everyone else** gets a short note and nothing else. That includes people who find the bot through the public website.

## Secrets and state (never committed)
- **`.env.telegram`** in the project folder:
  - `TELEGRAM_BOT_TOKEN=…` from BotFather;
  - `TELEGRAM_JOIN_CODE=…`.
  - To change the join code, edit it there and restart the bot.
- **`bot/state/`:**
  - `subscribers.json` (chat ids and names);
  - `sent.json` (alerts already sent, the last brief);
  - `bot.log`.
  - The log never contains the token.
- **If the token leaks:** in Telegram, open @BotFather, then `/revoke`. Put the new token in `.env.telegram` and restart the bot.

## Run it
```bash
python3 bot/v7pulse_bot.py
```
It needs Python 3.12 with Playwright (`pip install playwright`, then `python3 -m playwright install chromium`).

By default it reads the website's copy in `docs/index.html`. Set `DASH_URL` to read another copy, for example the hosted one.

## Keep it running
It runs while the computer it's on is awake.

**On this machine, as a user service:**
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
