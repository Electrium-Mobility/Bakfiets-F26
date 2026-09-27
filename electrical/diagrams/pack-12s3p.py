import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'diagrams'))
from notebook import *
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch

fig, ax = page(150, 94, (15, 9.4))
note(ax, 8, 90, 'What "12S3P" means', size=24, weight='bold')
note(ax, 8, 85.2, 'Looking down on the pack from above. 36 cells, wired as 12 groups of 3.', size=12, color=PENCIL)

r = 2.6
gx0, pitch = 16, 10.4
ys = [66, 59.6, 53.2]
NICKEL = '#b8b2a4'
xs = [gx0 + g * pitch for g in range(12)]

# nickel strips on top: join each group's cells, and link pairs 1-2, 3-4 ...
for g in range(0, 12, 2):
    ax.add_patch(Rectangle((xs[g] - 1.2, ys[2] - 1), xs[g + 1] - xs[g] + 2.4, ys[0] - ys[2] + 2, fc=NICKEL, ec=PENCIL, lw=1, alpha=0.55, zorder=1))
ax.add_patch(Rectangle((xs[0] - 1.2, ys[2] - 1), 2.4, ys[0] - ys[2] + 2, fc=NICKEL, ec=PENCIL, lw=1, alpha=0.0))
for g in range(12):
    up = (g % 2 == 0)
    for y in ys:
        ax.add_patch(Circle((xs[g], y), r, fc='#f3efe4', ec=INK, lw=1.4, zorder=2))
        if up:
            ax.add_patch(Circle((xs[g], y), 1.05, fc='#d9d2c0', ec=INK, lw=1, zorder=3))
            mono(ax, xs[g], y, '+', size=10, color=RED, ha='center', weight='bold', zorder=4)
        else:
            mono(ax, xs[g], y, '-', size=12, color=INK, ha='center', weight='bold', zorder=4)
    mono(ax, xs[g], 47.6, f'{g + 1}', size=9, color=PENCIL, ha='center')
    mono(ax, xs[g], 44.6, f'{3.7 * (g + 1):.1f}V', size=8.4, color=INK, ha='center', weight='bold')

# underside strips (dashed): link 2-3, 4-5 ...
for g in range(1, 11, 2):
    ax.add_patch(Rectangle((xs[g] - 1.2, ys[2] - 4.6), xs[g + 1] - xs[g] + 2.4, 1.6, fc='none', ec=PENCIL, lw=1.1, ls=(0, (3, 2))))
note(ax, xs[-1] + 2, ys[2] - 14, 'dashed boxes:\nstrips on the\nunderside', size=9, color=PENCIL, ha='left', linespacing=1.1)
# ends
note(ax, xs[0] - 4.2, ys[1], 'B-', size=15, color=INK, ha='right', weight='bold')
note(ax, xs[0] - 4.2, ys[1] - 4, 'underside of\ngroup 1', size=8.5, color=PENCIL, ha='right', linespacing=1)
note(ax, xs[-1] + 4.2, ys[1], 'B+', size=15, color=RED, ha='left', weight='bold')
note(ax, xs[-1] + 4.2, ys[1] - 4, 'underside of\ngroup 12.\n50.4V when full', size=9.5, color=RED, ha='left', linespacing=1.1)

# bracket around group 1
ax.add_patch(FancyBboxPatch((xs[0] - 3.8, ys[2] - 3.6), 7.6, ys[0] - ys[2] + 7.2, boxstyle='round,pad=0,rounding_size=1.6', fc='none', ec=GOLD, lw=2))
point(ax, (8, 77.5), (xs[0] - 2, ys[0] + 3.5), 'one group = 3 cells side by side (the "3P").\nsame voltage as a single cell, 3x the capacity',
      color=GOLD, rad=0.2)

# running total arrow
ax.annotate('', xy=(xs[-1] + 2, 41.6), xytext=(xs[0] - 2, 41.6), arrowprops=dict(arrowstyle='->', color=INK, lw=1.4))
note(ax, (xs[0] + xs[-1]) / 2, 39.2, 'voltage adds up group by group (the "12S"): 12 x 3.7V = about 44V', size=10.5, ha='center')

# balance wires
cy = 76
ax.add_patch(Rectangle((xs[4] - 2, cy - 1.4), xs[11] - xs[4] + 4, 3.2, fc='#e4ebf5', ec=BLUE, lw=1.6))
mono(ax, (xs[4] + xs[11]) / 2, cy + 0.2, 'balance plug -> BMS', size=9, color=BLUE, ha='center', weight='bold')
taps = [xs[0] - r - 0.4] + [(xs[g] + xs[g + 1]) / 2 for g in range(11)] + [xs[-1] + r + 0.4]
for k, x in enumerate(taps):
    tx = xs[4] - 1 + k * (xs[11] - xs[4] + 2) / 12
    ax.plot([x, x, tx], [ys[0] + r + 0.4 if 0 < k < 12 else ys[1], 71, cy - 1.4], color=BLUE, lw=0.9)
    if k in (0, 3, 4, 12):
        mono(ax, x + (0.6 if k else -2.2), 70.4 if 0 < k < 12 else ys[1] + 6.5, f'B{k}', size=7.6, color=BLUE, ha='left' if k else 'right', va='top')
point(ax, (120, 86.5), (xs[11] - 4, cy + 1.8), '13 thin wires, one per join.\nthe BMS watches every group\nthrough these', color=BLUE, rad=-0.25, ha='left')

# notes at the bottom
note(ax, 8, 30, 'the numbers', size=13, weight='bold')
mono(ax, 8, 25.6, 'full    12 x 4.2V = 50.4V', size=10)
mono(ax, 8, 22.4, 'normal  12 x 3.7V = ~44V   ("48V" is just the class name)', size=10)
mono(ax, 8, 19.2, 'empty   12 x 3.0V = ~36V', size=10)
note(ax, 8, 14.2, 'If the cells are about 3Ah each, 3 in parallel gives about 9Ah.', size=10.5, color=PENCIL)

note(ax, 88, 30, 'checking a group', size=13, weight='bold')
note(ax, 88, 23.4, 'Meter between B3 and B4 = group 4 on its own.\nA healthy group reads 3.0 to 4.2V.\nPlug the balance wires in the order the\nBMS manual shows, or you can kill the BMS.', size=10.5, linespacing=1.35)
note(ax, 88, 12.6, 'Never work on a pack alone.', size=11, color=RED)

mono(ax, 149, 2, "sketch only. we haven't opened the 2024 pack, so its real layout may differ.", size=7.2, color='#6f6a60', ha='right')
save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pack-12s3p.png'))
