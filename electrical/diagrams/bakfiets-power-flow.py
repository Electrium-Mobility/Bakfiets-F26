import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'docs', 'diagrams'))
from notebook import *
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

fig, ax = page(150, 98, (15, 9.8))
note(ax, 8, 94, 'How power flows through the bakfiets', size=24, weight='bold')
note(ax, 8, 89.2, 'Follow the numbers; they match the list under this drawing. Red is the positive side, black the negative side, both at battery voltage.',
     size=11.5, color=PENCIL)

def block(x, y, w, h, title, sub, col, n=None):
    ax.add_patch(Rectangle((x, y), w, h, fc='#f3efe4', ec=col, lw=2, zorder=2))
    note(ax, x + w / 2, y + h - 3, title, size=12, weight='bold', ha='center', zorder=3)
    if sub: note(ax, x + w / 2, y + h / 2 - 2, sub, size=9.2, color=PENCIL, ha='center', linespacing=1.15, zorder=3)
    if n:
        ax.add_patch(Circle((x + 0.2, y + h - 0.2), 1.9, fc=col, ec=col, zorder=4))
        note(ax, x + 0.2, y + h - 0.3, str(n), size=10.5, color='white', weight='bold', ha='center', zorder=5)
def line(xs, ys, c=RED, lw=5): ax.plot(xs, ys, color=c, lw=lw, solid_capstyle='round', zorder=1)
def arrow(p, q, c, ls='-', lw=2, rad=0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=14, color=c, lw=lw, ls=ls,
                                 connectionstyle=f'arc3,rad={rad}', zorder=1))

# positive side, top row
Y = 72
block(9, 66, 15, 12, 'charger', '12S, 50.4V', RED, 1)
block(34, 62, 18, 16, 'battery pack', '12S3P\n18650 cells', RED, 2)
block(58, 68, 7, 8, 'fuse', '', RED)
block(72, 66, 15, 12, 'antispark', 'soft power-on', RED, 4)
block(108, 60, 20, 20, 'motor\ncontroller', '', RED, 5)
note(ax, 118, 62.5, 'FSESC 6.7 (VESC)', size=9.2, color=PENCIL, ha='center', zorder=3)
block(134, 63, 14, 14, 'hub\nmotor', '', INK)
note(ax, 141, 65.5, '500W', size=9.2, color=PENCIL, ha='center', zorder=3)
line([24, 34], [Y, Y]); line([52, 58], [Y, Y]); line([65, 72], [Y, Y]); line([87, 108], [Y, Y])
for dy in (-2, 0, 2): line([128, 134], [Y + dy, Y + dy], INK, lw=2.6)
note(ax, 131, 80.5, '3 phase\nwires', size=8.5, color=INK, ha='center', linespacing=1)
note(ax, 26, 74.2, 'charging\nport', size=8.5, color=RED, linespacing=1)
note(ax, 61.5, 82, 'fuse on the + side,\nDC-rated 60V or more', size=9.5, color=RED, ha='center', linespacing=1.1)

# negative side through the BMS
block(34, 44, 18, 11, 'BMS', 'B- in, P- out', INK, 3)
line([43, 43], [62, 55], INK, lw=4)
note(ax, 44, 58.5, 'B-', size=10, color=INK, weight='bold')
line([52, 112, 112], [49.5, 49.5, 60], INK, lw=4)
note(ax, 58, 51.4, 'P-: charging and riding current both pass through the BMS', size=9.2, color=INK)
line([20, 20, 34], [66, 47, 47], INK, lw=2.6)
note(ax, 7.5, 57, 'charger\nnegative', size=8.5, color=INK, linespacing=1)
note(ax, 79.5, 64.2, 'the Electrium board likely\nswitches the - wire instead.\ncheck it in Stage 1', size=8.8, color=PENCIL, ha='center', va='top', linespacing=1.05)

# power board
block(88, 26, 22, 14, 'power board', 'steps battery power\ndown to 5V', GOLD, 6)
line([99, 99], [Y, 40], RED, lw=3.5)
line([104, 104], [49.5, 40], INK, lw=3.5)

# throttle and brakes into the controller
block(128, 40, 18, 11, 'throttle', 'thumb lever', BLUE)
arrow((134, 51), (124, 59.8), BLUE, ls=(0, (4, 3)))
note(ax, 136, 54.5, 'speed request\n(ADC, 3.3V)', size=8.8, color=BLUE, linespacing=1.05)

# electronics
block(34, 8, 24, 13, 'ESP32-S3', "the bike's small\ncomputer", BLUE, 7)
block(9, 9, 17, 10, 'screen', '128x64 OLED', BLUE)
block(84, 9, 22, 10, 'lights', 'LED strip, brake', GOLD)
block(34, 0.5, 24, 5.5, 'buttons', '', BLUE)
block(116, 9, 22, 10, 'brake levers', '', BLUE)
arrow((92, 26), (52, 21.2), GOLD, lw=2.4, rad=-0.1)
arrow((97, 26), (97, 19.2), GOLD, lw=2.4)
note(ax, 70, 25.6, '5V', size=10.5, color=GOLD, weight='bold')
note(ax, 98.5, 23, '5V', size=10.5, color=GOLD, weight='bold')
arrow((34, 14), (26.2, 14), BLUE, ls=(0, (4, 3)))
note(ax, 28.3, 16.4, 'I2C', size=9.5, color=BLUE)
arrow((58, 14), (83.8, 14), BLUE, ls=(0, (4, 3)))
note(ax, 63, 16.4, 'LED data', size=9.5, color=BLUE)
arrow((46, 6), (46, 7.8), BLUE, ls=(0, (4, 3)))
arrow((116, 14), (106.2, 14), BLUE, ls=(0, (4, 3)))
arrow((127, 19), (121, 59.8), BLUE, ls=(0, (4, 3)), rad=0.1)
note(ax, 131, 30, 'brake levers cut\nmotor power (#18)\nand light the\nbrake lights', size=8.8, color=BLUE, linespacing=1.05)
ax.plot([40, 40, 117, 117], [21, 43.5, 43.5, 60], color=BLUE, lw=1.8, ls=(0, (2, 3)), zorder=1)
note(ax, 56, 45.3, 'UART (#22): speed and battery data', size=9.3, color=BLUE)

# key
lx, ly = 9, 34
note(ax, lx, ly, 'key', size=12, weight='bold')
line([lx, lx + 4], [ly - 3.2, ly - 3.2], RED, 5); note(ax, lx + 5.5, ly - 3.2, 'battery +', size=9.5)
line([lx, lx + 4], [ly - 6.4, ly - 6.4], INK, 4); note(ax, lx + 5.5, ly - 6.4, 'battery -', size=9.5)
ax.plot([lx + 14, lx + 18], [ly - 3.2, ly - 3.2], color=GOLD, lw=2.4); note(ax, lx + 19.5, ly - 3.2, '5V', size=9.5)
ax.plot([lx + 14, lx + 18], [ly - 6.4, ly - 6.4], color=BLUE, lw=2, ls=(0, (4, 3))); note(ax, lx + 19.5, ly - 6.4, 'signals', size=9.5)
mono(ax, 149, -2, 'redrawn from the 2024 block diagram (high-level-circuit-diagram-2024.png); fuse, BMS side, brake cut-off and UART added from issues #18 to #22', size=6.6, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'bakfiets-power-flow.png'))
