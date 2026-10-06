import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notebook import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = page(150, 100, (15, 10))
note(ax, 8, 96, 'Term projects: what comes first', size=24, weight='bold')
note(ax, 8, 91.2, 'Each box says what to finish first. Solid arrow: waits for it. Dashed arrow: only part of the work waits.',
     size=11.5, color=PENCIL)

N = {}
def node(key, x, y, title, after, col, w=24, h=10):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0,rounding_size=1', fc='#f3efe4', ec=col, lw=2, zorder=3))
    note(ax, x - w / 2 + 1.5, y + 2.4, key, size=12.5, weight='bold', color=col, zorder=4)
    note(ax, x - w / 2 + 8.2, y + 2.4, title, size=10.5, color=INK, zorder=4)
    note(ax, x - w / 2 + 1.5, y - 2.4, after, size=9, color=PENCIL, zorder=4)
    N[key] = (x, y, w, h)
def edge(a, b, col, dashed=False, rad=0.0, side=('r', 'l')):
    xa, ya, wa, ha = N[a]; xb, yb, wb, hb = N[b]
    anchor = {'r': lambda x, y, w, h: (x + w / 2, y), 'l': lambda x, y, w, h: (x - w / 2, y),
              'b': lambda x, y, w, h: (x, y - h / 2), 't': lambda x, y, w, h: (x, y + h / 2)}
    p = anchor[side[0]](xa, ya, wa, ha); q = anchor[side[1]](xb, yb, wb, hb)
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=15, color=col, lw=2,
                                 ls=(0, (4, 3)) if dashed else '-', connectionstyle=f'arc3,rad={rad}', zorder=2))

for y, name, col in [(84, 'electrical', GOLD), (54, 'firmware', BLUE), (29, 'mechanical', GREEN)]:
    note(ax, 8, y, name, size=14, weight='bold', color=col)
    ax.plot([8, 146], [y - 2.6, y - 2.6], color=col, lw=0.8, alpha=0.5, zorder=1)

node('#21', 30, 75, 'battery pack', 'after #7', GOLD)
node('#18', 31, 63, 'bench test', 'after #1, #7. pack: #19, #21', GOLD, w=28)
node('#19', 65, 75, 'BMS + charge port', 'after #7', GOLD, w=27)
node('#20', 100, 69, 'wiring harness', 'plan after #10', GOLD)

node('#23', 30, 42, 'screen or not?', 'after #12', BLUE)
node('#22', 100, 44, 'ESP32 to VESC', 'after #12', BLUE)
node('#24', 64, 42, '2026 display', 'after #12', BLUE)


node('#25', 30, 19, 'new steering', 'top priority', GREEN)
node('#27', 30, 7, 'fix cargo box', 'after onboarding', GREEN)
node('#26', 70, 19, 'mount everything', 'after #3', GREEN, w=27)
node('#28', 70, 7, 'missing parts', 'after #2 and #3', GREEN)
node('#6', 102, 7, 'frame FEA', 'after #4, with the lead', GREEN)
node('#30', 102, 19, 'frame welds', 'WIP, after #2, #4, #6', GREEN)
node('#29', 132, 13, 'repaint', 'after #30', GREEN, w=22)

edge('#18', '#20', GOLD, rad=0.08); edge('#19', '#20', GOLD, rad=-0.05)
edge('#23', '#24', BLUE)
edge('#22', '#24', BLUE, dashed=True, side=('l', 'r'))
edge('#25', '#26', GREEN, dashed=True)
edge('#6', '#30', GREEN, side=('t', 'b'))
edge('#30', '#29', GREEN, rad=-0.1)
edge('#18', '#22', GOLD, dashed=True, rad=-0.12)

point(ax, (114, 84), (104, 74.2), 'building waits for\n#18 and #19', color=PENCIL, rad=0.3, ha='left')
point(ax, (114, 56), (106, 49.2), 'testing needs the\n#18 bench setup', color=PENCIL, rad=0.3, ha='left')
point(ax, (86, 29), (79, 24.2), 'part sizes come from\n#19 (BMS) and #21 (battery)', color=PENCIL, rad=0.25, ha='left')
note(ax, 114, 36.5, '#23, #25 and #27 can start as soon\nas you finish onboarding', size=10.5, color=INK, linespacing=1.2)
mono(ax, 149, -2.5, 'from the "Start after" column in ONBOARDING.md and docs/term-projects.md', size=7, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'term-project-map.png'))
