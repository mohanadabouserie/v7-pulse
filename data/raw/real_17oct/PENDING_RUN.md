# Waiting for the next real run (since 29 Oct 2026)

Mahmoud's rule (29 Oct): keep making changes, then test them all **in one real refresh**, not one paid run per change. Every change
below has passed `tests/test_pipeline.py` against stand-ins (no money spent), but none has run on real data yet.

Keep this file current: add each new change that needs a real run, or a fix to data already collected, as it's made. When the run is
done, record what each check showed and move the finished items to the bottom ("Done").

Budget on 29 Oct:
- **Apify:** about USD 10.66 left of the USD 100 limit, until 16 Nov (Mohanad's account).
- **ElevenLabs:** 8,382 of 10,000 free credits, about 105 minutes of audio with the names, until about 28 Nov (Mahmoud's free account; it stops at the limit).

## A. Changes to check in the next real run

Run `python3 pipeline.py run --mode fill` (no searches), or a sweep if new search phrases are added. Check each item:

| # | Change | Decision | What to check on real data |
|---|---|---|---|
| A1 | ElevenLabs Scribe v2 is the speech to text for new posts: Facebook (fbfill, fbinner), Instagram (igspeech), TikTok and YouTube (new `ttytspeech`) | #197 | The `*_el_*.json` raw files have text; `normalize.py` attaches it (`speech attached to … TikTok and YouTube posts`, Facebook speech count); `label.py` labels the posts again (`sp`). TikTok's page download and YouTube by link work at scale. ElevenLabs spend per step under USD 2 |
| A2 | 64 product and competitor names given to ElevenLabs | #196, #197 | V7, V Cola, competitors spelled right in the new transcripts |
| A3 | The "maybe" label | #198 | `label.py` returns `maybe` on the first real batch (the schema changed); maybe posts get speech and frames (`vis_media.py --new`) and are labelled again; how many become about V7 |
| A4 | Long unclear videos read 3 minutes first | #201 | Facebook video files download (`fb_video_files`, fresh links on Apify at USD 0.0023 a post); `read` in the raw rows says which videos stopped after 3 minutes; YouTube lengths come from the page, and unclear YouTube videos up to 15 minutes are read whole |
| A5 | Replies under public posts, linked to their comment, labelled with it | #200 | **thedoor's reply rows:** their format wasn't seen yet; `normalize.py` guesses the parent fields (`parent_id`, `parent_comment_id`, …) and the thread link. Check that replies get `reply_to`. Also check that `comment_check.py` doesn't reject posts now that replies make the sets bigger, that `label.py` sees `answers`, and that the dashboard shows public replies under their comment |
| A6 | No comment limit on V7's own posts and pages abroad | #199 | Only when `collect.py comments` / `abroad` run again (not in the pipeline) |
| A8 | "Maybe" Facebook posts with videos inside a post link: inner videos read whole by link when 15 minutes or less | #202 | Lengths come through on real rows (`fbinner_*.json` has `seconds` for each video; the 26 Oct rows had them); videos over 15 minutes or without a length are left out ("unclear videos left out" in the log); USD 0.0047 a maybe post on Apify |
| A7 | New search phrases for posts that don't name V7 (شركة مصرية تنافس بيبسي, كريم صودا, Egyptian cream soda…) | #198 | Not in the keyword lists yet: priced test (full about USD 4.25, without Google's site search about USD 1.25) waits for Mahmoud's OK; add the phrases that find V7 posts |

**Before running:** `replies` is a fill step, so the next fill run will also start fetching the replies of the posts collected before (B3, about USD 7.60) unless it's held back. Decide B3 first, or pass a `--max-usd` that leaves room for it.

## B. Fixes to data already collected

Posts collected before 26 Oct (`vis_baseline.json`) keep their speech and labels unless Mahmoud asks; these are the fixes on the table:

| # | Fix | Size | Cost | Status |
|---|---|---|---|---|
| B1 | Speech again with ElevenLabs for the Facebook videos invideoiq read, then label again (clear `sp`) | 301 videos, 467 min; 203 about V7 (130 min; Kareem Elsayed's 11-minute video among them) | about USD 0.57 for the 203 (ElevenLabs; more than the free minutes left, so part now, part after the refill) | Recommended: the 203 about V7. Waiting for Mahmoud |
| B2 | Speech again with ElevenLabs for the Instagram reels apple_yang read | 229 reels about V7, about 180 min | about USD 0.79 (ElevenLabs) + USD 0.53 (Apify, fresh video links) | Not discussed yet |
| B3 | Replies under the public posts already collected (`collect.py replies`) | about 2,467 replies on 187 Facebook posts, 412 on 62 Instagram posts, 344 on 11 YouTube videos | about USD 2.94 + 3.27 + 1.35 = 7.60 (Apify; top-level comments come again) | Waiting for Mahmoud: priority against the budget |
| B4 | The comments abroad missing since the 17 Oct run was stopped by hand | about 1,009 comments on 72 posts | about USD 2.30 (Apify) | Waiting for Mahmoud. Needs a new run name: `stage_abroad` skips `abroad_comments.json` |
| B5 | "Maybe" check on older posts: label again those whose caption hints at V7 (Pepsi and Coca-Cola against an Egyptian drink, cream soda, boycotts…), then speech and frames | 168 candidate videos (63 Facebook, 93 Instagram, 7 YouTube, 5 TikTok) | labelling free; speech a few cents (ElevenLabs) | Waiting for Mahmoud |
| B6 | Speech for TikTok and YouTube videos about V7 (none was read before) | 96 TikTok, 21 YouTube | roughly USD 0.40–0.60 (ElevenLabs; lengths not known yet) | Not discussed yet |
| B7 | Replies on V7's own posts were labelled with 140 characters of the comment they answer; now 500 | all replies on V7's posts | free (Claude) | Optional |

## Gaps noted, not changes yet
- TikTok comments are not collected at all; X and Reddit replies aren't either.
- TikTok, YouTube, X and Reddit aren't in the refresh pipeline: they were searched once (17–20 Oct).
- Instagram reposts, TikTok duets and stitches aren't followed to the original (only Facebook shares are, `fbshareorigins`).

## Done
(nothing yet)
