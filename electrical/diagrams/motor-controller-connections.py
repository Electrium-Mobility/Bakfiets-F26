import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'docs', 'diagrams'))
from notebook import *
from matplotlib.patches import Rectangle, Circle

fig, ax = page(150, 94, (15, 9.4))
note(ax, 8, 90, 'What plugs into the motor controller', size=24, weight='bold')
note(ax, 8, 85.2, 'The FSESC 6.7 (a VESC) sits in the middle of everything. Thick lines carry battery power. Thin lines are signals.',
     size=11.5, color=PENCIL)

def block(x, y, w, h, title, sub, col):
    ax.add_patch(Rectangle((x, y), w, h, fc='#f3efe4', ec=col, lw=2, zorder=2))
    note(ax, x + w / 2, y + h - 3, title, size=12.5, weight='bold', ha='center', zorder=3)
    if sub: note(ax, x + w / 2, y + h / 2 - 2, sub, size=9.5, color=PENCIL, ha='center', linespacing=1.15, zorder=3)
def thick(xs, ys, c=RED, lw=5): ax.plot(xs, ys, color=c, lw=lw, solid_capstyle='round', zorder=1)
def thin(xs, ys, c, ls='-'): ax.plot(xs, ys, color=c, lw=2, ls=ls, solid_capstyle='round', zorder=1)

Y = 64
block(8, 56, 20, 16, 'battery', 'Pack 4, 12S2P\n36 to 50.4V', RED)
block(8, 39, 20, 11, 'BMS', 'inside the pack,\nP- out', RED)
thick([18, 18], [56, 50], INK, lw=4)
thick([28, 42, 42, 92], [44.5, 44.5, 54, 54], INK, lw=4)
note(ax, 44, 55.8, 'negative (P-) to the controller', size=9, color=INK)
block(60, 58, 15, 12, 'antispark', 'soft on\nswitch', RED)
block(92, 44, 28, 30, 'FSESC 6.7', 'motor controller\n(VESC)', INK)
block(130, 56, 16, 16, 'hub motor', '2000W, set\nto 500W', INK)
thick([28, 60], [Y, Y]); thick([75, 92], [Y, Y])
note(ax, 30, Y + 1.8, 'B+', size=10, color=RED, weight='bold')
for dy in (-2.2, 0, 2.2):
    thick([120, 130], [Y + dy, Y + dy], INK, lw=3)
note(ax, 125, Y - 5.4, '3 phase\nwires', size=8.5, color=INK, ha='center', linespacing=1)
thin([138, 138, 120], [56, 52, 52], PENCIL, ls=(0, (3, 2)))
note(ax, 139, 53, 'hall cable, if the\nmotor has one', size=8.5, color=PENCIL, linespacing=1.05)
point(ax, (58, 47), (67, 57.6), 'connect battery last,\nthrough the antispark', color=PENCIL, rad=0.2)

# laptop
ax.add_patch(Rectangle((98, 76.4), 18, 6, fc='#e4ebf5', ec=BLUE, lw=1.5, zorder=2))
note(ax, 107, 79.4, 'laptop: VESC Tool', size=10.5, ha='center', color=BLUE)
thin([107, 107], [76.4, 74], BLUE, ls=(0, (3, 2)))
note(ax, 108.5, 75.2, 'USB, for setup', size=8.5, color=BLUE)

# COMM port on the controller, pins in the order Flipsky prints them
names = ['ADC3', 'ADC2', 'TX', 'RX', 'ADC1', 'GND', '3.3V', '5V']
px = [94.7 + i * 3.3 for i in range(8)]
pos = dict(zip(names, px))
used = {'ADC2', 'ADC1', 'GND', '3.3V'}
ax.add_patch(Rectangle((92.8, 44.6), 26.4, 5.6, fc='#e9e6df', ec=INK, lw=1.2, zorder=3))
for x, n in zip(px, names):
    ax.add_patch(Circle((x, 46.2), 0.9, fc=INK if n in used else PAPER, ec=INK, lw=1, zorder=4))
    mono(ax, x, 48.8, n, size=6.4, ha='center', zorder=4, color=INK if n in used else '#8a857a')
note(ax, 106, 52.6, 'COMM plug', size=9, color=PENCIL, ha='center', zorder=4)

# throttle: signal to ADC1, power and ground from the SWD plug
block(36, 29, 24, 12, 'thumb throttle', '', GOLD)
note(ax, 48, 32, '3.3V and GND go to\nthe SWD plug', size=9, color=PENCIL, ha='center', linespacing=1.05, zorder=3)
thin([60, pos['ADC1'], pos['ADC1']], [33, 33, 45.3], GOLD)
note(ax, 63, 34.8, 'signal to ADC1', size=9.5, color=GOLD)

# rear brake lever: signal to ADC2, power and ground from COMM
block(14, 10, 24, 15, 'rear brake lever', 'with cut-off wire', BLUE)
thin([32, 32, pos['ADC2'], pos['ADC2']], [25, 42.5, 42.5, 45.3], BLUE)
thin([38, pos['GND'], pos['GND']], [20, 20, 45.3], INK)
thin([38, pos['3.3V'], pos['3.3V']], [16, 16, 45.3], RED)
note(ax, 64, 44, 'signal to ADC2', size=9.5, color=BLUE)
note(ax, 64, 21.8, 'ground', size=9.5, color=INK)
note(ax, 64, 12.8, '3.3V', size=9.5, color=RED)

# ESP32 reaches the controller over CAN, through an add-on board
block(124, 32, 22, 10, 'CAN board', 'transceiver', GREEN)
thin([120, 122, 122, 124], [49, 49, 39, 39], '#7b3fb0')
thin([120, 121, 121, 124], [47, 47, 36, 36], GREEN)
note(ax, 124.5, 45, 'CAN-H, CAN-L,\nGND', size=9, color=PENCIL, linespacing=1.05)
block(124, 6, 22, 20, 'ESP32-S3', '5V from the\npower board', BLUE)
thin([132, 132], [32, 26], BLUE); thin([138, 138], [32, 26], BLUE)
note(ax, 133, 29, 'TX', size=9, color=BLUE, ha='left'); note(ax, 139, 29, 'RX', size=9, color=BLUE, ha='left')

mono(ax, 149, -1.5, 'wiring from issues #18 (throttle), #40 (brake) and #22 (CAN). pin order from Flipsky. GPIO choice is a suggestion.', size=7, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'motor-controller-connections.png'))
