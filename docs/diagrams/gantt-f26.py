import sys, os
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notebook import *
from matplotlib.patches import Rectangle, FancyBboxPatch

# Rough plan for Fall 2026. Solid bars are planned, hatched bars are a guess
# that the squad leads will firm up. Edit the rows below and rerun.
START, END = date(2026, 10, 5), date(2026, 12, 5)
X0, X1 = 44, 146                       # plot area on the page
def x(d): return X0 + (d - START).days / (END - START).days * (X1 - X0)
D = lambda m, d: date(2026, m, d)

rows = [
    ('Mechanical', GREEN, [
        ('#31 hub motor fit, torque arms', [(D(10, 7), D(10, 9), 1)]),
        ('#32 brakes: pick, then fit',     [(D(10, 7), D(10, 9), 1), (D(10, 21), D(11, 4), 0)]),
        ('#2 record what is welded',       [(D(10, 7), D(10, 14), 1)]),
        ('#4 measure the frame',           [(D(10, 9), D(10, 21), 1)]),
        ('#5 battery mount',               [(D(10, 7), D(10, 21), 1)]),
        ('#25 steering: study, CAD, build', [(D(10, 7), D(10, 21), 1), (D(10, 21), D(11, 11), 0), (D(11, 11), D(12, 2), 0)]),
        ('#6 frame FEA',                   [(D(10, 21), D(11, 18), 0)]),
        ('#26 mount everything',           [(D(11, 4), D(12, 2), 0)]),
    ]),
    ('Electrical', GOLD, [
        ('#19 check BMS and charger',      [(D(10, 7), D(10, 9), 1)]),
        ('#21 Pack 4 check and rest test', [(D(10, 9), D(10, 21), 1)]),
        ('#18 bench test: supply, then pack', [(D(10, 7), D(10, 21), 1), (D(10, 21), D(11, 11), 0)]),
        ('#20 wiring harness',             [(D(11, 11), D(12, 2), 0)]),
    ]),
    ('Firmware', BLUE, [
        ('#12 board test',                 [(D(10, 7), D(10, 8), 1)]),
        ('#23 pick a screen',              [(D(10, 7), D(10, 9), 1)]),
        ('#22 read the VESC, then test',   [(D(10, 7), D(10, 21), 1), (D(10, 21), D(11, 11), 0)]),
        ('#13, #14 LEDs and PA button',    [(D(10, 7), D(10, 21), 1)]),
        ('#24 2026 display',               [(D(11, 4), D(12, 2), 0)]),
    ]),
]
n_rows = sum(len(r[2]) + 1 for r in rows)
H = int(round(28 + n_rows * 4.6))
fig, ax = page(150, H, (15, H / 10))
note(ax, 8, H - 5, 'Bakfiets F26: the plan for the term', size=24, weight='bold')

top = H - 16
bottom = 10
# reading week
ax.add_patch(Rectangle((x(D(10, 10)), bottom), x(D(10, 19)) - x(D(10, 10)), top - bottom + 4, fc='#ece6d6', ec='none', zorder=0))
note(ax, (x(D(10, 10)) + x(D(10, 19))) / 2, top + 5.6, 'reading week', size=10, color=PENCIL, ha='center')
# Wednesday meetings
for m, d in [(10, 7), (10, 21), (10, 28), (11, 4), (11, 11), (11, 18), (11, 25), (12, 2)]:
    xx = x(D(m, d))
    ax.plot([xx, xx], [bottom, top + 2], color='#d6cfbd', lw=1, zorder=0)
    mono(ax, xx, top + 2.4, f'{d} {"Oct" if m == 10 else "Nov" if m == 11 else "Dec"}', size=8.5, color=PENCIL, ha='center')
mono(ax, X0 - 1, top + 2.4, 'Wed:', size=8.5, color=PENCIL, ha='right')

# milestones
y = top - 2
for d, label, dy in [(D(10, 7), 'Stage 1 due', 0), (D(10, 9), 'buy list due', 2.4), (D(10, 10), 'order 1 in', -2.4),
                     (D(10, 21), 'Stage 2 due', 0), (D(10, 28), 'order 2: steering', 0)]:
    xx = x(d)
    ax.plot([xx], [y], marker='D', ms=7, color=RED, zorder=4)
    if label == 'Stage 1 due':
        note(ax, xx - 1.2, y - 0.4, label, size=8.8, color=RED, ha='right')
    else:
        note(ax, xx + 0.8, y + 1.2 + dy, label, size=8.8, color=RED)
note(ax, 8, y - 0.6, 'Milestones', size=11, weight='bold', color=RED)
y -= 6

for team, col, items in rows:
    note(ax, 8, y - 0.6, team, size=12, weight='bold', color=col)
    y -= 4.6
    for label, segs in items:
        note(ax, 9, y - 0.6, label, size=9.4, color=INK)
        for s, e, firm in segs:
            w = max(x(e) - x(s), 0.9)
            ax.add_patch(FancyBboxPatch((x(s), y - 1.3), w, 2.6, boxstyle='round,pad=0,rounding_size=0.6',
                                        fc=col if firm else 'none', ec=col, lw=1.4, hatch=None if firm else '////',
                                        alpha=0.9, zorder=3))
        y -= 4.6
    y -= 0.4

save(fig, os.path.join(HERE, 'gantt-f26.png'))
