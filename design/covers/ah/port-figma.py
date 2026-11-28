"""Put the Figma export of the AH Compact cover on the site, with the story's classes.

    python3 design/covers/ah/port-figma.py [path/to/export.svg]

Default input: design/covers/ah/ah-compact-figma.svg. The export is copied there first
when another path is given. Then:
  - every ID, url(#…) reference and keyframe is prefixed ah- (no clashes on the page);
  - the story's classes are added, on wrapper groups so CSS transforms don't replace
    Figma's own positioning (see STORY below; the motion itself is in ah.css);
  - every direct child group of the groceries frame becomes a .bob (lifts on hover);
  - Figma's point-of-light keyframes are written into ah.css (between the markers);
  - the cover replaces <svg class="ah"> in index.html (CRLF kept).
Afterwards run design/covers/export.py to refresh the exports.
If Figma renames a layer, update the IDs below.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(ROOT, 'design/covers/ah/ah-compact-figma.svg')
CSS = os.path.join(ROOT, 'assets/css/covers/ah.css')
PAGE = os.path.join(ROOT, 'index.html')

CLASS_ON = {  # Figma ID: class added on the element itself (opacity only)
    'Free_delivery_from_2_items': 'todo',
    'Free_delivery_unlocked': 'done',
    '_0_2': 'c0', '_1_2': 'c1', '_2_2': 'c2',
    'Frame_2': 'dot',
}
WRAP = [  # (Figma ID, wrapper class, extra attributes), inner first
    ('Frame_6', 'badge', ''),
    ('Frame_5', 'todo', ''),
    ('Frame_8', 'ok', ''),
    ('Vector_20', 'bar', ''),
    ('Frame_11', 'added', ' style="--t:2.6s"'),
    ('Frame_15', 'added', ' style="--t:4.75s"'),
]
GROCERIES = 'Frame_19'
MARK_A = '/* --- Figma point of light (written by port-figma.py) --- */'
MARK_B = '/* --- end Figma point of light --- */'

if len(sys.argv) > 1 and os.path.abspath(sys.argv[1]) != SRC:
    shutil.copy(sys.argv[1], SRC)
fig = open(SRC).read()
style = re.search(r'<style>(.*?)</style>', fig, re.S)
style = style.group(1) if style else ''
body = fig[fig.index('>', fig.index('<svg')) + 1:fig.rindex('</svg>')]
body = re.sub(r'<style>.*?</style>', '', body, flags=re.S)

for i in sorted(set(re.findall(r'\bid="([^"]+)"', body)), key=len, reverse=True):
    body = re.sub(rf'\bid="{re.escape(i)}"', f'id="ah-{i}"', body)
    body = body.replace(f'url(#{i})', f'url(#ah-{i})').replace(f'href="#{i}"', f'href="#ah-{i}"')


def span(eid):
    m = re.search(rf'<(g|path|rect)\b[^>]*\bid="ah-{re.escape(eid)}"', body)
    if not m:
        sys.exit(f'Figma ID not found: {eid}')
    st = m.start()
    if m.group(1) != 'g':
        return st, body.index('>', st) + 1
    d = 0
    for mm in re.finditer(r'<g\b[^>]*?(/?)>|</g>', body[st:]):
        t = mm.group(0)
        d += -1 if t == '</g>' else (0 if t.endswith('/>') else 1)
        if d == 0:
            return st, st + mm.end()


for eid, cls in CLASS_ON.items():
    body, n = re.subn(rf'(<(?:g|path)\b)([^>]*\bid="ah-{re.escape(eid)}")', rf'\1 class="{cls}"\2', body, count=1)
    if not n:
        sys.exit(f'Figma ID not found: {eid}')
for eid, cls, extra in WRAP:
    st, en = span(eid)
    body = body[:st] + f'<g class="{cls}"{extra}>' + body[st:en] + '</g>' + body[en:]

st, en = span(GROCERIES)
grp = body[st:en]
inner_start = grp.index('>') + 1
kids, depth, pos = [], 0, inner_start
for m in re.finditer(r'<g\b[^>]*?(/?)>|</g>', grp[inner_start:]):
    t = m.group(0)
    a = inner_start + m.start()
    if t == '</g>':
        depth -= 1
        if depth == 0:
            kids.append((kid_start, inner_start + m.end()))
        if depth < 0:
            break
    elif not t.endswith('/>'):
        if depth == 0:
            kid_start = a
        depth += 1
for a, b in reversed(kids):
    grp = grp[:a] + '<g class="bob">' + grp[a:b] + '</g>' + grp[b:]
body = body[:st] + grp + body[en:]

svg = '<svg class="ah" viewBox="0 0 800 500" fill="none" role="img" aria-label="AH Compact">' + body.rstrip() + '\n</svg>'
svg = '\n'.join(('                ' + l) if l.strip() else l for l in svg.split('\n')).lstrip()
page = open(PAGE, newline='').read().replace('\r\n', '\n')
page, n = re.subn(r'<svg class="ah".*?</svg>', lambda m: svg, page, count=1, flags=re.S)
assert n == 1
open(PAGE, 'w', newline='').write(page.replace('\n', '\r\n'))

style = style.replace('kf_', 'ah-kf_').replace('#Frame_2', '.dot').strip()
css = open(CSS).read()
css = re.sub(r'\n*  /\* The point of light going round the cycle.*?\n  \}\n', '\n', css, flags=re.S)
css = re.sub(r'\n*/\* Point of light: Order → over the top.*', '\n', css, flags=re.S)
css = re.sub(re.escape(MARK_A) + r'.*?' + re.escape(MARK_B) + r'\n?', '', css, flags=re.S).rstrip() + '\n'
css += f'\n{MARK_A}\n@scope (.ah) {{\n' + re.search(r'\.dot \{.*?\n\}', style, re.S).group(0) + '\n}\n'
css += style[:style.index('.dot {')].strip() + f'\n{MARK_B}\n'
open(CSS, 'w').write(css)
print(f'ok: {len(kids)} grocery items, {len(svg) // 1024} KB inline')
