"""Put the Figma export of the Home energy app cover on the site, with its animations.

    python3 assets/covers/nrg/port-figma.py [path/to/export.svg]

Default input: assets/covers/nrg/home-energy-figma.svg (another path is copied there
first). Then:
  - IDs and url(#…) references are prefixed nrg- (no clashes on the page); Figma's
    own <style> (keyframes for the dot, drawn on an older line) is dropped;
  - the phone's story gets its classes back (notification, usage line and area,
    today's dot and halo, tooltip, stat bars); the motion is in nrg.css;
  - one point of light runs along the supply line (grid to house, over the top) and
    then the redelivery line (house back to the grid, along the bottom), 7s each;
  - the wind turbines' blades turn around their hubs (SMIL rotate);
  - the pill labels, outlined by Figma without the gap before the amount, become live
    text again (label, gap, bold amount), with pills sized to fit;
  - the cover replaces <svg class="nrg"> in index.html (CRLF kept).
Afterwards run assets/covers/export.py. If Figma renames a layer, update the IDs below.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(ROOT, 'assets/covers/nrg/home-energy-figma.svg')
PAGE = os.path.join(ROOT, 'index.html')
F = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

SUPPLY = 'Vector_3'              # the line from the grid over the top into the house
REDELIVERY = 'Vector_4'          # the line from the house back to the grid
DOT = 'Frame'                    # the point of light
TURBINES = [  # (blade IDs, hub x, hub y in the turbine group's own space, seconds per turn)
    (('Vector_27', 'Vector_28', 'Vector_29'), 27.53, 32.69, 10.5),
    (('Vector_22', 'Vector_23', 'Vector_24'), 14.37, 16.55, 8),
]
CLASS_ON = {'Vector_56': 'area'}
LINE = 'Vector_57'
WRAP = [('Vector_58', 'halo'), ('Vector_59', 'dot'), ('Frame_19', 'tip'),
        ('Vector_65', 'prog'), ('Vector_67', 'prog'), ('Frame_23', 'notif')]
# pill frame ID, background path ID, text group ID, text x, label, amount, x, right-aligned
PILLS = [
    ('Frame_2', 'Vector_7', 'Electricity___54_mo', 26, 'Electricity', '€54/mo', 72, False),
    ('Frame_4', 'Vector_9', 'Gas___38_mo', 26, 'Gas', '€38/mo', 72, False),
    ('Frame_6', 'Vector_11', 'Yearly_bill___1_104', 30, 'Yearly bill', '€1,104', 744, True),
    ('Frame_8', 'Vector_13', 'To_the_grid____210_yr', 30, 'To the grid', '+€210/yr', 744, True),
]
TEXT_W = {'Electricity': 117.7, 'Gas': 80.8, 'Yearly bill': 106.4, 'To the grid': 131.7}  # measured in Chrome

if len(sys.argv) > 1 and os.path.abspath(sys.argv[1]) != SRC:
    shutil.copy(sys.argv[1], SRC)
fig = open(SRC).read()
body = fig[fig.index('>', fig.index('<svg')) + 1:fig.rindex('</svg>')]
body = re.sub(r'<style>.*?</style>', '', body, flags=re.S)
for i in sorted(set(re.findall(r'\bid="([^"]+)"', body)), key=len, reverse=True):
    body = re.sub(rf'\bid="{re.escape(i)}"', f'id="nrg-{i}"', body)
    body = body.replace(f'url(#{i})', f'url(#nrg-{i})').replace(f'href="#{i}"', f'href="#nrg-{i}"')


def find(eid):
    m = re.search(rf'<(g|path|rect)\b[^>]*\bid="nrg-{re.escape(eid)}"', body)
    if not m:
        sys.exit(f'Figma ID not found: {eid}')
    st = m.start()
    if m.group(1) != 'g':
        end = body.index('>', st) + 1
        if not body[st:end].endswith('/>'):
            end = body.index(f'</{m.group(1)}>', end) + len(m.group(1)) + 3
        return st, end
    d = 0
    for mm in re.finditer(r'<g\b[^>]*?(/?)>|</g>', body[st:]):
        t = mm.group(0)
        d += -1 if t == '</g>' else (0 if t.endswith('/>') else 1)
        if d == 0:
            return st, st + mm.end()


def wrap(eid, open_tag):
    global body
    st, en = find(eid)
    body = body[:st] + open_tag + body[st:en] + '</g>' + body[en:]


# Phone story classes
for eid, cls in CLASS_ON.items():
    body = re.sub(rf'(<path\b)([^>]*\bid="nrg-{eid}")', rf'\1 class="{cls}"\2', body, count=1)
body = re.sub(rf'(<path\b)([^>]*\bid="nrg-{LINE}")', r'\1 class="line" pathLength="1"\2', body, count=1)
for eid, cls in WRAP:
    wrap(eid, f'<g class="{cls}">')

# Point of light: along the supply line (grid to house, over the top), then the
# redelivery line (house back to the grid, along the bottom); 7s each, one dot.
def absolute(d, ox, oy):
    """Absolute M/L/H/V/C path offset by (ox, oy) -> (path, length, end point)."""
    toks = re.findall(r'[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?', d)
    out, i, cmd, x, y, length = [], 0, None, 0.0, 0.0, 0.0
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]; i += 1
        if cmd in 'Zz':
            continue
        n = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6}[cmd]
        v = [float(q) for q in toks[i:i + n]]; i += n
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
                w = ((1 - s) ** 3, 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s * s, s ** 3)
                q = [sum(c * p_[j] for c, p_ in zip(w, pts)) for j in (0, 1)]
                length += ((q[0] - prev[0]) ** 2 + (q[1] - prev[1]) ** 2) ** 0.5; prev = q
            x, y = v[4], v[5]
            out.append('C' + ' '.join(f'{a + (ox if k % 2 == 0 else oy):g}' for k, a in enumerate(v)))
    return ''.join(out), length, (x + ox, y + oy)


def line_of(eid):
    st, en = find(eid)
    tag = body[st:en]
    m = re.search(r'translate\(([-\d.]+) ([-\d.]+)\)', tag)
    ox, oy = (float(m.group(1)), float(m.group(2))) if m else (0.0, 0.0)
    return absolute(re.search(r'\bd="([^"]+)"', tag).group(1), ox, oy)


(top, l1, end1), (bottom, l2, _) = line_of(SUPPLY), line_of(REDELIVERY)
sx, sy = (float(v) for v in re.match(r'M([-\d.]+) ([-\d.]+)', bottom).groups())
gap = ((sx - end1[0]) ** 2 + (sy - end1[1]) ** 2) ** 0.5
total = l1 + gap + l2
k1, k2 = l1 / total, (l1 + gap) / total
st, en = find(DOT)
dot = body[st:en]
dot = re.sub(r'\s*opacity="0"', '', dot, count=1)
dot = dot[:dot.rindex('</g>')] + (
    f'<animateMotion dur="14s" repeatCount="indefinite" calcMode="spline" '
    f'keyPoints="0;{k1:.4f};{k2:.4f};1" keyTimes="0;0.5;0.5;1" '
    f'keySplines="0.45 0 0.55 1;0 0 1 1;0.45 0 0.55 1" path="{top}L{bottom[1:]}" /></g>')
body = body[:st] + ('<g class="pk" opacity="0">'
                    '<animate attributeName="opacity" values="0;1;1;0;0;1;1;0" '
                    'keyTimes="0;0.075;0.425;0.5;0.5;0.575;0.925;1" dur="14s" repeatCount="indefinite" />'
                    + dot + '</g>') + body[en:]

# Turning blades
for ids, hx, hy, dur in TURBINES:
    spans = sorted(find(i) for i in ids)
    st, en = spans[0][0], spans[-1][1]
    body = body[:st] + (f'<g class="blades"><animateTransform attributeName="transform" type="rotate" '
                        f'from="0 {hx} {hy}" to="360 {hx} {hy}" dur="{dur}s" repeatCount="indefinite" />'
                        + body[st:en] + '</g>') + body[en:]

# Pills: live text, sized to fit
for frame, bg, txt, tx_, label, amount, x, right in PILLS:
    w = round(tx_ + TEXT_W[label] + 14)
    st, en = find(frame)
    grp = body[st:en]
    grp = re.sub(r'translate\([-\d.]+ ([-\d.]+)\)', lambda m: f'translate({x - w if right else x} {m.group(1)})', grp, count=1)
    grp = re.sub(rf'<path id="nrg-{bg}" d="[^"]+"', f'<rect id="nrg-{bg}" width="{w}" height="28" rx="14"', grp, count=1)
    ts, te = re.search(rf'<g id="nrg-{txt}".*?</g>', grp, re.S).span()
    grp = grp[:ts] + (f'<text x="{tx_}" y="18.5" font-family="{F}" font-size="13" fill="#FFFFFF">{label}'
                      f'<tspan dx="6" font-weight="700">{amount}</tspan></text>') + grp[te:]
    body = body[:st] + grp + body[en:]

svg = ('<svg class="nrg" viewBox="0 0 800 500" fill="none" role="img" aria-label="Home energy app">'
       + body.rstrip() + '\n</svg>')
svg = '\n'.join(('                ' + l) if l.strip() else l for l in svg.split('\n')).lstrip()
page = open(PAGE, newline='').read().replace('\r\n', '\n')
page, n = re.subn(r'<svg class="nrg".*?</svg>', lambda m: svg, page, count=1, flags=re.S)
assert n == 1
open(PAGE, 'w', newline='').write(page.replace('\n', '\r\n'))
print(f'ok: {len(svg) // 1024} KB inline')
