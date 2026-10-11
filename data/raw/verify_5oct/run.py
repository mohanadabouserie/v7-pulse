import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK=os.environ['APIFY_API_TOKEN']; OUT=sys.argv[1]; batch=sys.argv[2]
NODL={"shouldDownloadVideos":False,"shouldDownloadCovers":False,"shouldDownloadSlideshowImages":False,"shouldDownloadAvatars":False,"shouldDownloadMusicCovers":False}
tests={
 'reddit':     ('trudax~reddit-scraper-lite', {"startUrls":[{"url":"https://www.reddit.com/r/RateIT_T/comments/1vk12pd/"},{"url":"https://www.reddit.com/r/EGYescapism/comments/1vub9t5/"}],"skipComments":False,"maxComments":3,"skipCommunity":True,"skipUserPosts":True,"maxItems":8,"maxPostCount":2}, 8),
 'ig_comments':('apify~instagram-comment-scraper', {"directUrls":["https://www.instagram.com/p/DdG_sWYEi_T/"],"resultsLimit":5}, 5),
 'tt_comments':('clockworks~tiktok-scraper', dict(NODL, postURLs=["https://www.tiktok.com/@engysaed/video/7682168436096601364"], commentsPerPost=5), 8),
 'yt_comments':('streamers~youtube-comments-scraper', {"startUrls":[{"url":"https://www.youtube.com/shorts/n3Cr1WFLDc8"}],"maxComments":5}, 6),
 'yt_channel': ('streamers~youtube-channel-scraper', {"startUrls":[{"url":"https://www.youtube.com/@V7Egypt"}],"maxResults":1,"maxResultsShorts":0,"maxResultStreams":0}, 2),
 'ig_pages':   ('apify~instagram-profile-scraper', {"usernames":["v7tunisia","v7uzbekistan","thehalaldrinksco"]}, 3),
 'talabat':    ('thirdwatch~talabat-scraper', {"queries":["koshary","shawarma","burger","pizza","grills","sandwiches"],"country":"eg","maxResults":3,"scrapeMenu":True}, 18),
 'fb_group_posts':('apify~facebook-groups-scraper', {"startUrls":[{"url":"https://www.facebook.com/groups/2828301800643081/"}],"resultsLimit":2}, 2),
 'fb_group_profile':('maximedupre~facebook-group-profile-scraper', {"findGroupsBy":"url","groupUrls":[{"url":"https://www.facebook.com/groups/2828301800643081/"}]}, 1),
}
B={'1':['reddit','ig_comments','tt_comments','yt_comments','yt_channel'],'2':['ig_pages','talabat','fb_group_posts','fb_group_profile']}[batch]
def run(name):
    actor, body, cap = tests[name]
    url=f'https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items?timeout=280&maxTotalChargeUsd=1&maxItems={cap}'
    req=urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={'Authorization':f'Bearer {TOK}','Content-Type':'application/json'})
    t=time.time()
    try: items=json.load(urllib.request.urlopen(req, timeout=320))
    except urllib.error.HTTPError as e: return name, f'HTTP {e.code}: {e.read()[:240]!r}', time.time()-t
    except Exception as e: return name, f'ERR {e}', time.time()-t
    json.dump({'input':body,'items':items}, open(f'{OUT}/{name}.json','w'), ensure_ascii=False, indent=1)
    return name, f'{len(items)} items', time.time()-t
with ThreadPoolExecutor(5) as ex:
    for n,r,dt in ex.map(run, B): print(f'{n:17s} {r} ({dt:.0f}s)', flush=True)
