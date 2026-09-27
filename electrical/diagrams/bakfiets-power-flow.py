import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'docs', 'diagrams'))
from notebook import *
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

fig, ax = page(150, 96, (15, 9.6))
note(ax, 8, 92, 'How power flows through the bakfiets', size=24, weight='bold')
note(ax, 8, 87.2, 'Follow the numbers; they match the list under this drawing. Top row: full battery voltage. Bottom rows: 5V and signals.',
     size=11.5, color=PENCIL)

def block(x, y, w, h, title, sub, col, n=None, fc='#f3efe4'):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=col, lw=2, zorder=2))
    note(ax, x + w / 2, y + h - 3, title, size=12, weight='bold', ha='center', zorder=3)
    if sub: note(ax, x + w / 2, y + h / 2 - 2, sub, size=9.2, color=PENCIL, ha='center', linespacing=1.15, zorder=3)
    if n:
        ax.add_patch(Circle((x + 0.2, y + h - 0.2), 1.9, fc=col, ec=col, zorder=4))
        note(ax, x + 0.2, y + h - 0.3, str(n), size=10.5, color='white', weight='bold', ha='center', zorder=5)
def thick(xs, ys, c=RED, lw=5): ax.plot(xs, ys, color=c, lw=lw, solid_capstyle='round', zorder=1)
def arrow(p, q, c, ls='-', lw=2, rad=0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=14, color=c, lw=lw, ls=ls,
                                 connectionstyle=f'arc3,rad={rad}', zorder=1))

# band labels

# row 1: battery side
Y = 66
block(9, 60, 15, 12, 'charger', '12S, 50.4V', RED, 1)
block(30, 60, 15, 12, 'BMS', 'guards\nthe cells', RED, 2)
block(51, 58, 18, 16, 'battery pack', '12S3P\n18650 cells', RED, 3)
block(75, 62, 7, 8, 'fuse', '', RED)
block(88, 60, 15, 12, 'antispark', 'soft power-on', RED, 4)
block(110, 57, 20, 18, 'motor\ncontroller', '', RED, 5)
note(ax, 120, 60, 'FSESC 6.7 (VESC)', size=9.2, color=PENCIL, ha='center', zorder=3)
block(135, 59, 13, 14, 'hub\nmotor', '', INK)
note(ax, 141.5, 61.5, '500W', size=9.2, color=PENCIL, ha='center', zorder=3)
thick([24, 30], [Y, Y]); thick([45, 51], [Y, Y]); thick([69, 75], [Y, Y]); thick([82, 88], [Y, Y]); thick([103, 110], [Y, Y])
for dy in (-2, 0, 2): thick([130, 135], [Y + dy, Y + dy], INK, lw=2.6)
note(ax, 132.5, 76.5, '3 phase\nwires', size=8.5, color=INK, ha='center', linespacing=1)
note(ax, 71.5, 76, 'fuse on the + side,\nDC-rated 60V or more', size=9.5, color=RED, ha='center', linespacing=1.1)
point(ax, (12, 80), (27, 66.8), 'the charger plugs into a charging port\non the frame, wired to the BMS (#19)', color=RED, rad=-0.2)

# row 2: power board
block(88, 34, 22, 14, 'power board', 'steps battery power\ndown to 5V', GOLD, 6)
thick([107, 107], [Y, 48], RED, lw=4)
note(ax, 108.5, 51, 'battery'+chr(10)+'power', size=9, color=RED, linespacing=1)
block(128, 36, 18, 12, 'throttle', 'thumb lever', BLUE)
arrow((137, 48), (125, 57), BLUE, ls=(0, (4, 3)))
note(ax, 138, 51.5, 'speed request\n(ADC, 3.3V)', size=8.8, color=BLUE, linespacing=1.05)

# row 3: electronics
block(34, 10, 24, 14, 'ESP32-S3', "the bike's small\ncomputer", BLUE, 7)
block(9, 12, 17, 10, 'screen', '128x64 OLED', BLUE)
block(84, 12, 22, 10, 'lights', 'LED strip, brake', GOLD)
block(34, 1, 24, 6, 'buttons', '', BLUE)
block(84, 1, 22, 6, 'brake lever', '', BLUE)
arrow((92, 34), (52, 24.2), GOLD, lw=2.4, rad=-0.1)
arrow((97, 34), (97, 22.2), GOLD, lw=2.4)
note(ax, 70, 29, '5V', size=10.5, color=GOLD, weight='bold')
note(ax, 98.5, 28, '5V', size=10.5, color=GOLD, weight='bold')
arrow((34, 17), (26.2, 17), BLUE, ls=(0, (4, 3)))
note(ax, 28.5, 19.4, 'I2C', size=9.5, color=BLUE)
arrow((58, 17), (83.8, 17), BLUE, ls=(0, (4, 3)))
note(ax, 64, 19.4, 'LED data', size=9.5, color=BLUE)
arrow((46, 7), (46, 9.8), BLUE, ls=(0, (4, 3)))
arrow((95, 7), (95, 11.8), BLUE, ls=(0, (4, 3)))
note(ax, 107, 4, 'brake lever turns on\nthe brake lights', size=9, color=PENCIL, linespacing=1.1)
ax.plot([40, 40, 114, 114], [24, 54, 54, 56.8], color=BLUE, lw=1.8, ls=(0, (2, 3)), zorder=1)
note(ax, 42, 56.5, 'UART (#22): the controller sends speed and battery data to the ESP32', size=9.5, color=BLUE)

# legend
lx, ly = 116, 23
note(ax, lx, ly, 'key', size=12, weight='bold')
ax.plot([lx, lx + 5], [ly - 3.5, ly - 3.5], color=RED, lw=5); note(ax, lx + 6.5, ly - 3.5, 'battery voltage, 36 to 50.4V', size=9.5)
ax.plot([lx, lx + 5], [ly - 7, ly - 7], color=GOLD, lw=2.4); note(ax, lx + 6.5, ly - 7, '5V for small electronics', size=9.5)
ax.plot([lx, lx + 5], [ly - 10.5, ly - 10.5], color=BLUE, lw=2, ls=(0, (4, 3))); note(ax, lx + 6.5, ly - 10.5, 'signals only', size=9.5)
mono(ax, 149, -1.8, 'redrawn from the 2024 block diagram (high-level-circuit-diagram-2024.png); fuse and UART added from issues #20 and #22', size=6.8, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'bakfiets-power-flow.png'))
