"""Do a scraper's comments belong to the post they were asked for? (24 Oct 2026, DECISIONS #178)

What went wrong: given a Facebook share (someone sharing another post), thedoor's comment scraper returns the comments of the post
that was shared and labels them with the share's link. On 19 Oct a share with 2 comments got 99, 73 of them older than the share itself,
and the dashboard showed them under it; their links opened the share, where those comments aren't. Apify's own comment scraper reads a
share's own comments.

So, at the source:
- shares never go to thedoor (collect.py stage_fbfill), only to Apify's own scraper (stage_fbfill2);
- every set of comments a scraper returns for a post is checked here: normalize.py keeps only the sets that pass (the rest are listed
  in comment_rejects.json), stage_fbfill2 asks Apify's scraper for the rejected posts, and pipeline.py reports them.
"""
import datetime, re

EARLY = datetime.timedelta(hours=1)   # a comment can't be older than its post; an hour of slack for clocks and rounded times


def key(url):
    """A post link as normalize.py matches it: without the query, except for permalink.php links, whose id is in the query."""
    u = url or ''
    return u if 'story_fbid' in u else u.split('?')[0].rstrip('/')


def when(t):
    """Epoch seconds or milliseconds, or an ISO time, as a UTC datetime (None if it can't be read)."""
    if t is None or t == '':
        return None
    try:
        if isinstance(t, (int, float)) or re.fullmatch(r'\d{10,13}', str(t)):
            v = float(t)
            return datetime.datetime.fromtimestamp(v / 1000 if v > 1e11 else v, datetime.timezone.utc)
        d = datetime.datetime.fromisoformat(str(t).replace('Z', '+00:00'))
        return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)
    except (ValueError, OverflowError):
        return None


def reason(post, dates, scraper):
    """Why these comments (their dates) can't be this post's, or None when they can.
    post: a post from items.json (date, comments, is_share); scraper: 'thedoor' or 'apify'."""
    if scraper == 'thedoor' and post.get('is_share'):
        return 'a share: thedoor returns the shared post’s comments'
    posted = when(post.get('date'))
    if posted:
        early = sum(1 for d in dates if when(d) and when(d) < posted - EARLY)
        if early:
            return '%d of %d comments are older than the post' % (early, len(dates))
    shown = post.get('comments')
    if shown is not None and len(dates) > 2 * shown + 20:   # the post's own count can lag the scrape a little, not by this much
        return '%d comments for a post that shows %d' % (len(dates), shown)
    return None
