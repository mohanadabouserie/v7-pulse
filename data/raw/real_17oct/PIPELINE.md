# The refresh pipeline (`pipeline.py`, 19 Oct 2026)

One command runs the whole real-data chain for Facebook and Instagram, and keeps going when a scraper breaks.
The user asked for it ("make the pipeline robust") after Versions 29 to 31 closed the Instagram and Facebook gaps by hand.

## How a run goes

1. **Searches** (Apify), one job a route, one run a keyword:

   | Job | Main scraper | Standbys (same output format) | Modes |
   |---|---|---|---|
   | `fb_posts_one` | scraper_one | fetch_cat | sweep, daily |
   | `fb_posts_sf` | silentflow | scrapeforge, topapi | sweep, daily |
   | `fb_posts_ap` | Apify's search | none | sweep, weekly |
   | `fb_posts_forge` | scrapeforge | topapi | sweep, weekly |
   | `fb_posts_cat` | fetch_cat | scraper_one | sweep, weekly |
   | `fb_reels_google` | Google's short videos (Facebook) | none | sweep, daily |
   | `fb_reels_alien` | alien_force (reels only) | Apify's reel search | sweep, weekly |
   | `fb_videos` | headply video search | Apify's video search | sweep, weekly |
   | `fb_groups` | lofomachines (public groups) | none | sweep, weekly |
   | `fb_google_web` | Google's site search of facebook.com | none | sweep, daily |
   | `ig_tagged` | posts tagging @v7egypt and @vsupersoda | none | sweep, daily |
   | `ig_kw` | apidojo | seemuapps | sweep, daily |
   | `ig_reels` | dami_studio (Reels search) | none | sweep, weekly |
   | `ig_reels_google` | Google's short videos (Instagram) | none | sweep, weekly |
   | `ig_google_web` | Google's site search of instagram.com | none | sweep, weekly |
   | `ig_hashtags` | Apify's hashtag scraper | none | sweep, weekly |

   In daily and weekly runs Facebook's own search (scraper_one, fetch_cat) is sorted by latest: limited to a day or two, it then lists
   those days' posts, which found posts no search over the whole window had (the 20 Oct date-slice test, `DATESLICE_TEST.md`).
   Sweeps over the whole window keep its top results.
2. **Links fetched by link:** reels, videos and posts that Google and the reel searches return as bare links, when the collection
   doesn't have them yet: Facebook with danek (standby: Apify's posts scraper), Instagram with Apify's post scraper.
3. **The chain:** `normalize.py`, `label.py` (Claude), the gap fillers in `collect.py` (`fbfill`, `fbfill2`, `fbviews`, `fbnames`,
   `igspeech`, `igprofiles`, `igcomments`, `igcomments2`, `igvisfetch`), the pictures (`vis_media.py`, `vis_read.py`), `normalize.py`
   and `label.py` again, `build_real.py --inject`, `fetch_media.py`, `build_media.py --inject`, and the quick tests
   (`test_v25`, `test_v29`, `test_v30`, `test_v31`).
4. **Report and alert:** `pipeline_runs/<time>.json` and `.md`, and a Telegram message to the bot's admin.

Publishing stays manual: `deploy/build_sites.py dashboard`, then a push, which needs the user's OK each time.

## What makes it robust

- **Health check on every run:** it must end `SUCCEEDED`, and at least half its rows must carry the fields its reader needs
  (`VALID` in `pipeline.py`). A run that fails, can't start, or comes back in a changed format goes to the job's next scraper.
  Standbys write in the same format, so `normalize.py` reads them unchanged (files are named by format: `fbp_sf_*`, `fbp_one_*`,
  `fbp_ap_*`, `fbp_hp_*`, `fbp_lofo_*`, `igp_post_*`, `igp_apidojo_*`, `igp_seemu_*`, `igp_dami_*`; link-only finds `fbl_*`, `igl_*`).
- **Empty when it shouldn't be:** a job whose every keyword comes back empty, though it found posts in an earlier run (the ledger),
  is tried once on its standby.
- **Apify's API errors:** reads are retried on 5xx (`collect.api`), up to four times. A scraper that refuses a cap under its own
  minimum (TikTok, Google and calm_builder take USD 0.50 at least) is asked again with that minimum, if it fits under the line.
- **Budget guard:** a run starts only if its cap fits under this run's line (`--max-usd`, default 10, and never past the account's
  usage limit). Runs that don't fit are skipped and reported, in the searches and in the gap fillers, which obey the same line.
  Until the fix of 19 Oct, the gap fillers' parallel runner started a skipped run again with a USD 0.50 cap.
- **No paying twice for nothing:** a video the speech or play scraper returned nothing for is asked for at most twice, and a page or
  Instagram account the follower scrapers couldn't read only once (`collect.attempts`).
- **Every picture:** `fetch_media.py` downloads an image for every post that has one, and `build_media.py` links them all (no budget
  since 21 Oct, DECISIONS #170; until then they were embedded under 6,000 KB for the claude.ai page limit).
- **One run at a time:** `pipeline.lock` (a stale lock from a run that died is taken over).
- **Ledger:** `pipeline_ledger.json`, every Apify run with its scraper, status, rows, usable rows and whether it stood in for another.
  The ledger, the lock and the reports stay on the machine that runs the pipeline (git-ignored).
- **Alerts:** a Telegram message to the admin(s) in `bot/state/subscribers.json`: cost, new links, standbys used, problems, failed
  steps. The token stays in `.env.telegram`; the tests check it never reaches a file or the output.
- **Tests:** `tests/test_pipeline.py` (19 checks) runs the pipeline against stand-ins for Apify and Telegram: healthy runs, a failed
  run, rows in a changed format, 502s, the budget guard, an empty job that found posts before, the lock, the window guard, a plan,
  and the gap fillers' runs that don't start (over the line, refused by Apify, or refused for a cap under the scraper's minimum).
  No token, no cost.
- **The public repo:** `SCRAPERS.md` counts the links and accounts a run was given instead of printing them: the links to private
  people's posts carry their handle on Facebook, X and TikTok.

## Commands

```
python3 pipeline.py plan --mode sweep          # what would run, and its worst cost; spends nothing
python3 pipeline.py run --mode fill            # no searches: fill the gaps of what's collected, rebuild, test
python3 pipeline.py run --mode sweep --max-usd 25
python3 pipeline.py status                     # the last runs, and any that needed a standby
```

The first real run (fill mode, 19 Oct, `--max-usd 1`): 23 steps, none failed, USD 0.62, the quick tests passed. Two gap-filler runs
didn't fit under the USD 1 line (speech for 35 videos, Apify's Instagram comments); the report didn't list them then and does now.

Worst cost of the searches (19 Oct prices; Facebook pads results, so most runs return their full count):
sweep about USD 24.50, daily about USD 2.30, weekly about USD 6.40, plus fetching new links and filling gaps (cents a day).

## Before a schedule

`daily` and `weekly` search the last 2 and 8 days. The dashboard's window ends on 16 Oct (`END` in `V7_Pulse_Dashboard.html`), so
posts after it would be collected but not shown; `pipeline.py` refuses those dates unless `--beyond-window` is passed. A schedule
needs, first:

1. the dashboard's window rolling forward: `END` and the dates in its copy taken from the data block, and the tests that pin
   16 Oct reading it from there;
2. V7's own posts and the comments on them refreshed too (`collect.py own` and `comments` over the new days);
3. the user's OK for the spending (anything that spends on a schedule needs it) and a monthly budget line.

The schedule files are ready in `deploy/` (`v7pulse-pipeline.service`, `v7pulse-pipeline.timer`, `v7pulse-pipeline-weekly.timer`)
and are not installed.

## Comments must belong to their post (24 Oct, DECISIONS #178)

thedoor's comment scraper returns a shared post's comments under the share's link. So shares go only to Apify's own comment scraper,
every set of comments is checked by `comment_check.py` before `normalize.py` keeps it (rejects in `comment_rejects.json`), `fbfill2`
asks Apify's scraper for the rejected posts once, and the run report names them. `tests/test_pipeline.py` covers it.

