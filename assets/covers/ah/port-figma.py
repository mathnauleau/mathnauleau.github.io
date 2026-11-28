"""Put the Figma export of the AH Compact cover on the site, with the story's classes.

    python3 assets/covers/ah/port-figma.py [path/to/export.svg]

Default input: assets/covers/ah/ah-compact-figma.svg. The export is copied there first
when another path is given. Then:
  - every ID, url(#…) reference and keyframe is prefixed ah- (no clashes on the page);
  - the story's classes are added, on wrapper groups so CSS transforms don't replace
    Figma's own positioning (see STORY below; the motion itself is in ah.css);
  - every direct child group of the groceries frame becomes a .bob (lifts on hover);
  - the point of light follows the cycle line itself (SMIL, 7s per half); Figma's own
    dot keyframes are dropped (they trail older versions of the line);
  - the cover replaces <svg class="ah"> in index.html (CRLF kept).
Afterwards run assets/covers/export.py to refresh the exports.
If Figma renames a layer, update the IDs below.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(ROOT, 'assets/covers/ah/ah-compact-figma.svg')
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
DOT_ID = 'Frame_2'
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

# The point of light follows the cycle line itself (Figma's own dot keyframes trail an
# older version of the line): out over the top, back along the bottom, 7s each half.
CYCLE_FRAME, CYCLE_TOP, CYCLE_BOTTOM = 'Frame', 'Vector_2', 'Vector_3'


def offset_of(eid):
    st, en = span(eid)
    m = re.search(r'translate\(([-\d.]+) ([-\d.]+)\)', body[st:body.index('>', st)])
    return (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)


def absolute(d, ox, oy):
    """Absolute M/L/H/V/C path, offset by (ox, oy); returns (path, length)."""
    toks = re.findall(r'[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?', d)
    out, i, cmd, x, y, length = [], 0, None, 0.0, 0.0, 0.0
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]; i += 1
        if cmd in 'Zz':
            continue
        n = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6}[cmd]
        v = [float(t) for t in toks[i:i + n]]; i += n
        if cmd == 'M':
            x, y = v; out.append(f'M{x + ox:g} {y + oy:g}'); cmd = 'L'; continue
        if cmd in 'LHV':
            nx, ny = (v[0], v[1]) if cmd == 'L' else ((v[0], y) if cmd == 'H' else (x, v[0]))
            length += ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
            x, y = nx, ny; out.append(f'L{x + ox:g} {y + oy:g}')
        else:
            pts = [(x, y), (v[0], v[1]), (v[2], v[3]), (v[4], v[5])]
            prev = pts[0]
            for k in range(1, 41):
                s = k / 40
                q = [sum(c * p_[j] for c, p_ in zip(((1 - s) ** 3, 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s * s, s ** 3), pts)) for j in (0, 1)]
                length += ((q[0] - prev[0]) ** 2 + (q[1] - prev[1]) ** 2) ** 0.5; prev = q
            x, y = v[4], v[5]
            out.append('C' + ' '.join(f'{a + (ox if k % 2 == 0 else oy):g}' for k, a in enumerate(v)))
    return ''.join(out), length, (x + ox, y + oy)


fx, fy = offset_of(CYCLE_FRAME)
paths = []
for eid in (CYCLE_TOP, CYCLE_BOTTOM):
    st, en = span(eid)
    tag = body[st:en]
    ox, oy = (re.search(r'translate\(([-\d.]+) ([-\d.]+)\)', tag) or [None]) and offset_of(eid)
    d = re.search(r'\bd="([^"]+)"', tag).group(1)
    paths.append(absolute(d, fx + ox, fy + oy))
(top, l1, end1), (bottom, l2, _) = paths
start2 = re.match(r'M([-\d.]+) ([-\d.]+)', bottom).groups()
gap = ((float(start2[0]) - end1[0]) ** 2 + (float(start2[1]) - end1[1]) ** 2) ** 0.5
loop = top + 'L' + bottom[1:]
total = l1 + gap + l2
k1, k2 = l1 / total, (l1 + gap) / total
st, en = span(DOT_ID)
dot = body[st:en]
dot = dot[:dot.rindex('</g>')] + (
    f'<animateMotion dur="14s" repeatCount="indefinite" calcMode="spline" '
    f'keyPoints="0;{k1:.4f};{k2:.4f};1" keyTimes="0;0.5;0.5;1" '
    f'keySplines="0.45 0 0.55 1;0 0 1 1;0.45 0 0.55 1" path="{loop}" />'
    f'<animate attributeName="opacity" values="0;1;1;0;0;1;1;0" '
    f'keyTimes="0;0.075;0.425;0.5;0.5;0.575;0.925;1" dur="14s" repeatCount="indefinite" /></g>')
body = body[:st] + dot + body[en:]

svg = '<svg class="ah" viewBox="0 0 800 500" fill="none" role="img" aria-label="AH Compact">' + body.rstrip() + '\n</svg>'
svg = '\n'.join(('                ' + l) if l.strip() else l for l in svg.split('\n')).lstrip()
page = open(PAGE, newline='').read().replace('\r\n', '\n')
page, n = re.subn(r'<svg class="ah".*?</svg>', lambda m: svg, page, count=1, flags=re.S)
assert n == 1
open(PAGE, 'w', newline='').write(page.replace('\n', '\r\n'))

css = open(CSS).read()
css = re.sub(r'\n*' + re.escape(MARK_A) + r'.*?' + re.escape(MARK_B) + r'\n?', '\n', css, flags=re.S).rstrip() + '\n'
open(CSS, 'w').write(css)
print(f'ok: {len(kids)} grocery items, {len(svg) // 1024} KB inline')
