"""Build the GitHub Pages copies of the dashboard and the cost calculator.

The artifact viewer adds the page skeleton (doctype, charset, viewport) at publish time,
so the source files have none. A standalone host needs it, or phones render the pages
at desktop width. Run after every change to a source file:
- dashboard: writes docs/index.html in this repo (mohanadabouserie/v7-pulse). GitHub Pages
  serves docs/, so committing and pushing this repo updates the public site.
- costs: writes deploy/v7-pulse-costs/index.html, a separate clone of mohanadabouserie/v7-pulse-costs.

  python3 deploy/build_sites.py              # both
  python3 deploy/build_sites.py dashboard    # one
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n')
# name: (source, output, [(text that only makes sense inside claude.ai, public wording)])
SITES = {
    'costs': ('V7_Pulse_Costs.html', 'deploy/v7-pulse-costs/index.html', []),
    'dashboard': ('V7_Pulse_Dashboard.html', 'docs/index.html', [
        ("'Short built-in answers. Open the dashboard in claude.ai and allow Claude for full answers.'",
         "'Short built-in answers. Full answers from Claude aren’t available in this copy.'"),
    ]),
}

def build(name):
    src, out, swaps = SITES[name]
    s = open(os.path.join(ROOT, src), encoding='utf-8').read()
    assert '<!doctype' not in s.lower(), src + ' already has a skeleton'
    for old, new in swaps:
        assert s.count(old) == 1, 'text to swap not found once in ' + src + ': ' + old[:60]
        s = s.replace(old, new)
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(HEAD + s.rstrip('\n') + '\n</html>\n')
    open(os.path.join(os.path.dirname(path), '.nojekyll'), 'a').close()   # serve the files as they are
    print('wrote', out)

for name in sys.argv[1:] or SITES:
    build(name)
