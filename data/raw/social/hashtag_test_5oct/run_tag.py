import sys,json,time
sys.path.insert(0,'.')
from apify_run import run, usage
TAG='اشرب_اي'
u0=usage()
ig=run('apify~instagram-hashtag-scraper',{"hashtags":[TAG],"resultsLimit":5,"resultsType":"posts"},'hashtag/ig.json',5,0.05,240)
tt=run('clockworks~tiktok-scraper',{"hashtags":[TAG],"resultsPerPage":5,"shouldDownloadVideos":False,"shouldDownloadCovers":False,"shouldDownloadSubtitles":False,"shouldDownloadSlideshowImages":False},'hashtag/tt.json',5,0.5,240)
time.sleep(5); u1=usage()
print(f'IG items {len(ig or [])} | TikTok items {len(tt or [])} | usage ${u0:.4f} -> ${u1:.4f} (+${u1-u0:.4f})')
