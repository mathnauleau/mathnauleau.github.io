"""Export the home-page covers from index.html into design/covers/.

    python3 design/covers/export.py            animated exports only
    python3 design/covers/export.py --stills   also the stills (needs Google Chrome)

Animated: each inline <svg class="<prefix>"> with assets/css/covers/base.css and its own
stylesheet embedded, so it animates when opened in a browser.

Stills: for covers whose story has distinct stages, headless Chrome seeks every
animation to a moment of the loop, writes the resulting values inline and stops the
animations, so each file shows one stage (useful for Figma, slides, thumbnails).
"""
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'design', 'covers')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# prefix -> (folder/file, title)
COVERS = {
    'ops': ('ops/designops.svg', 'DesignOps'),
    'xl': ('xl/data-tool.svg', 'Data tool'),
    'pds': ('pds/pantry.svg', 'Pantry Design System'),
    'nrg': ('nrg/home-energy.svg', 'Home energy app'),
    'wl': ('wl/white-label.svg', 'White label eCommerce App'),
    'ah': ('ah/ah-compact.svg', 'AH Compact'),
    'cbk': ('cbk/cookbook.svg', 'Cookbook.md'),
    'isl': ('isl/island.svg', 'Island Slide Puzzle'),
}

# prefix -> [(file suffix, time in ms, label)]
STILLS = {
    'xl': [('1-spreadsheet', 1500, 'the old Excel workflow'),
           ('2-dashboard', 8000, 'the new tool')],
    'wl': [('1-blue', 1500, 'brand 1: Hamburg Serial, blue'),
           ('2-pink', 5500, 'brand 2: Ivar Display, pink'),
           ('3-orange', 9500, 'brand 3: Proxima Nova, orange')],
}

PROPS = ['opacity', 'transform', 'translate', 'fill', 'stroke', 'stroke-opacity',
         'fill-opacity', 'stroke-dashoffset', 'rx']

page = open(os.path.join(ROOT, 'index.html'), newline='').read().replace('\r\n', '\n')
base = open(os.path.join(ROOT, 'assets/css/covers/base.css')).read()


def svg_of(prefix):
    m = re.search(rf'<svg class="{prefix}".*?</svg>', page, re.S)
    return m.group(0)


def css_of(prefix):
    return base + '\n' + open(os.path.join(ROOT, f'assets/css/covers/{prefix}.css')).read()


def standalone(prefix, svg, css, note):
    svg = svg.replace(f'<svg class="{prefix}"',
                      f'<svg xmlns="http://www.w3.org/2000/svg" class="{prefix}" width="800" height="500"', 1)
    i = svg.index('>') + 1
    svg = svg[:i] + '\n  <style><![CDATA[\n' + css + ']]></style>' + svg[i:]
    return f'<!-- {note} -->\n' + svg + '\n'


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text)
    return full


for prefix, (path, title) in COVERS.items():
    note = (f'{title} cover, exported from index.html by design/covers/export.py.\n'
            f'     Open it in a browser to see it animate; the styles are assets/css/covers/base.css\n'
            f'     and assets/css/covers/{prefix}.css. Edit the page, then re-run the script.')
    print('animated', write(path, standalone(prefix, svg_of(prefix), css_of(prefix), note)))

if '--stills' not in sys.argv:
    sys.exit()

FREEZE = '''
<script>
addEventListener('load', function () {
  var t = %d, svg = document.querySelector('svg');
  if (svg.pauseAnimations) { svg.pauseAnimations(); svg.setCurrentTime(t / 1000); }
  var anims = document.getAnimations();
  anims.forEach(function (a) { a.pause(); a.currentTime = t; });
  var props = %s, seen = new Set();
  anims.forEach(function (a) {
    var el = a.effect && a.effect.target;
    if (!el || seen.has(el)) return;
    seen.add(el);
    var cs = getComputedStyle(el);
    props.forEach(function (p) { el.style.setProperty(p, cs.getPropertyValue(p)); });
  });
  anims.forEach(function (a) { a.cancel(); });
  svg.querySelectorAll('animate, animateMotion, set').forEach(function (n) { n.remove(); });
  document.getElementById('out').textContent = new XMLSerializer().serializeToString(svg);
});
</script>'''

for prefix, stills in STILLS.items():
    path, title = COVERS[prefix]
    folder, name = os.path.split(path)
    css = css_of(prefix)
    for suffix, t, label in stills:
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write('<!doctype html><meta charset="utf-8"><style>' + css + '</style>' + svg_of(prefix)
                    + '<textarea id="out"></textarea>' + FREEZE % (t, PROPS))
        dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=1000',
                              '--dump-dom', 'file://' + f.name], capture_output=True, text=True).stdout
        os.unlink(f.name)
        frozen = html.unescape(re.search(r'<textarea id="out">(.*?)</textarea>', dom, re.S).group(1))
        frozen = re.sub(r'^<svg xmlns="http://www.w3.org/2000/svg" ', '<svg ', frozen)
        still_css = css + '\n/* Still: animations off, values frozen inline */\n* { animation: none !important; transition: none !important; }\n'
        note = (f'{title} cover, still: {label} (t = {t / 1000:g}s of the loop).\n'
                f'     Exported from index.html by design/covers/export.py (stills option).')
        out = os.path.join(folder, name.replace('.svg', f'-{suffix}.svg'))
        print('still   ', write(out, standalone(prefix, frozen, still_css, note)))
