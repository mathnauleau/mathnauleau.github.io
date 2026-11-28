"""Put the Figma export of the Home energy app cover on the site, with its animations.

    python3 design/covers/nrg/port-figma.py [path/to/export.svg]

Default input: design/covers/nrg/home-energy-figma.svg (another path is copied there
first). Then:
  - IDs and url(#…) references are prefixed nrg- (no clashes on the page); Figma's
    own <style> (keyframes for the dot, drawn on an older line) is dropped;
  - the phone's story gets its classes back (notification, usage line and area,
    today's dot and halo, tooltip, stat bars); the motion is in nrg.css;
  - the point of light follows the redelivery line (SMIL, 7s, house to grid);
  - the wind turbines' blades turn around their hubs (SMIL rotate);
  - the pill labels, outlined by Figma without the gap before the amount, become live
    text again (label, gap, bold amount), with pills sized to fit;
  - the cover replaces <svg class="nrg"> in index.html (CRLF kept).
Afterwards run design/covers/export.py. If Figma renames a layer, update the IDs below.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = os.path.join(ROOT, 'design/covers/nrg/home-energy-figma.svg')
PAGE = os.path.join(ROOT, 'index.html')
F = "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

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

# Point of light along the redelivery line
st, en = find(REDELIVERY)
line = body[st:en]
d = re.search(r'\bd="([^"]+)"', line).group(1)
tx, ty = re.search(r'translate\(([-\d.]+) ([-\d.]+)\)', line).groups()
st, en = find(DOT)
dot = body[st:en]
dot = re.sub(r'\s*opacity="0"', '', dot, count=1)
dot = dot[:dot.rindex('</g>')] + (
    f'<animateMotion dur="7s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1" keyTimes="0;1" '
    f'keySplines="0.45 0 0.55 1" path="{d}" /></g>')
body = body[:st] + (f'<g class="pk" transform="translate({tx} {ty})" opacity="0">'
                    f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.85;1" dur="7s" repeatCount="indefinite" />'
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
