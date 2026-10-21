"""Build the published copies of the dashboard and the cost calculator.

- dashboard: V7_Pulse_Dashboard.html is already a complete page (since 21 Oct 2026 there's no claude.ai copy, DECISIONS #170), so
  this copies it to docs/index.html with the post images it links to, copied into docs/media/. GitHub Pages serves docs/, so
  committing and pushing this repo updates the public site. docs/ is the whole site: it needs nothing else from this repo or this
  machine (see "Hosting" in CLAUDE.md). MEDIA_BASE changes where the page looks for the images, for example a CDN:
  MEDIA_BASE=https://cdn.example.com/v7/ python3 deploy/build_sites.py dashboard (the default is media/, next to the page).
- costs: writes deploy/v7-pulse-costs/index.html, a separate clone of mohanadabouserie/v7-pulse-costs. Its source has no page
  skeleton (the claude.ai artifact viewer adds one), so this adds it.

  python3 deploy/build_sites.py              # both
  python3 deploy/build_sites.py dashboard    # one
"""
import json, os, re, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = 'data/raw/media_13oct/img/'   # where the dashboard's MEDIA block points (build_media.py), relative to the repo root
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n')


def dashboard():
    s = open(os.path.join(ROOT, 'V7_Pulse_Dashboard.html'), encoding='utf-8').read()
    site = os.path.join(ROOT, 'docs')
    m = re.search(r'/\*MEDIA\*/var MEDIA=(.*?);/\*END_MEDIA\*/', s, re.S)
    assert m, 'MEDIA block not found'
    files = sorted(set(re.findall(r'"s":"' + re.escape(IMG) + r'([^"/]+)"', m.group(1))))
    base = os.environ.get('MEDIA_BASE', 'media/')
    s = s[:m.start(1)] + m.group(1).replace('"s":"' + IMG, '"s":"' + base) + s[m.end(1):]
    assert IMG not in s, 'the page still points at ' + IMG
    mdir = os.path.join(site, 'media')
    os.makedirs(mdir, exist_ok=True)
    for f in os.listdir(mdir):
        if f not in files: os.remove(os.path.join(mdir, f))
    for f in files:
        shutil.copyfile(os.path.join(ROOT, IMG, f), os.path.join(mdir, f))
    with open(os.path.join(site, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(s)
    open(os.path.join(site, '.nojekyll'), 'a').close()   # serve the files as they are
    print('wrote docs/index.html and', len(files), 'images in docs/media/' + ('' if base == 'media/' else ' (the page reads them from ' + base + ')'))


def costs():
    s = open(os.path.join(ROOT, 'V7_Pulse_Costs.html'), encoding='utf-8').read()
    assert '<!doctype' not in s.lower(), 'V7_Pulse_Costs.html already has a skeleton'
    path = os.path.join(ROOT, 'deploy', 'v7-pulse-costs', 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(HEAD + s.rstrip('\n') + '\n</html>\n')
    open(os.path.join(os.path.dirname(path), '.nojekyll'), 'a').close()
    print('wrote deploy/v7-pulse-costs/index.html')


SITES = {'dashboard': dashboard, 'costs': costs}
for name in sys.argv[1:] or SITES:
    SITES[name]()
