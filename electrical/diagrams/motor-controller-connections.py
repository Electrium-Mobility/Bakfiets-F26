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
block(8, 56, 20, 16, 'battery', '12S3P\n36 to 50.4V', RED)
block(8, 39, 20, 11, 'BMS', 'pack B- in,\nP- out', RED)
thick([18, 18], [56, 50], INK, lw=4)
thick([28, 42, 42, 92], [44.5, 44.5, 54, 54], INK, lw=4)
note(ax, 44, 55.8, 'negative (P-) to the controller', size=9, color=INK)
block(40, 60, 9, 8, 'fuse', '', RED)
block(60, 58, 15, 12, 'antispark', 'soft on\nswitch', RED)
block(92, 44, 28, 30, 'FSESC 6.7', 'motor controller\n(VESC)', INK)
block(130, 56, 16, 16, 'hub motor', '500W', INK)
thick([28, 40], [Y, Y]); thick([49, 60], [Y, Y]); thick([75, 92], [Y, Y])
note(ax, 30, Y + 1.8, 'B+', size=10, color=RED, weight='bold')
for dy in (-2.2, 0, 2.2):
    thick([120, 130], [Y + dy, Y + dy], INK, lw=3)
note(ax, 125, Y - 5.4, '3 phase\nwires', size=8.5, color=INK, ha='center', linespacing=1)
thin([138, 138, 120], [56, 52, 52], PENCIL, ls=(0, (3, 2)))
note(ax, 139, 53, 'hall cable, if the\nmotor has one', size=8.5, color=PENCIL, linespacing=1.05)
point(ax, (34, 78), (44.5, 68.5), 'fuse on the positive side, DC-rated for 60V\nor more. car blade fuses (32V) are not safe', color=RED, rad=-0.25)
point(ax, (58, 47), (67, 57.6), 'connect battery last,\nthrough the antispark', color=PENCIL, rad=0.2)

# laptop
ax.add_patch(Rectangle((98, 76.4), 18, 6, fc='#e4ebf5', ec=BLUE, lw=1.5, zorder=2))
note(ax, 107, 79.4, 'laptop: VESC Tool', size=10.5, ha='center', color=BLUE)
thin([107, 107], [76.4, 74], BLUE, ls=(0, (3, 2)))
note(ax, 108.5, 75.2, 'USB, for setup', size=8.5, color=BLUE)

# COMM port on the controller
px = [95, 99.5, 104, 108.5, 113, 117.5]
names = ['3.3V', 'ADC1', 'GND', 'TX', 'RX', '5V']
ax.add_patch(Rectangle((93.2, 44.6), 25.6, 5.6, fc='#e9e6df', ec=INK, lw=1.2, zorder=3))
for x, n in zip(px, names):
    ax.add_patch(Circle((x, 46.2), 0.9, fc=INK if n != '5V' else PAPER, ec=INK, lw=1, zorder=4))
    mono(ax, x, 48.8, n, size=7.6, ha='center', zorder=4, color=INK if n != '5V' else '#6f6a60')
note(ax, 122, 44, 'COMM port. the pin order here\nis only for the drawing: check\nthe Flipsky manual', size=9, color=PENCIL, linespacing=1.1)

# throttle, wires drop straight down then left, no crossings
block(22, 10, 24, 15, 'thumb throttle', 'hall sensor inside', GOLD)
for n, y in [('3.3V', 20.5), ('ADC1', 17.5), ('GND', 14.5)]:
    x = px[names.index(n)]
    thin([46, x, x], [y, y, 45.3], GOLD if n != 'GND' else INK)
    mono(ax, 45, y, n, size=7.6, color=GOLD if n != 'GND' else INK, ha='right', zorder=3)
point(ax, (6, 33.5), (26, 24.6), 'power it from 3.3V, not 5V.\nthe ADC input only takes 3.3V', color=RED, rad=-0.2)

# ESP32, to the right; RX->TX and TX->RX, GND shared
block(124, 4, 22, 24, 'ESP32-S3', '', BLUE)
thin([113, 113, 124], [45.3, 20.5, 20.5], BLUE)     # VESC RX <- ESP TX
thin([108.5, 108.5, 124], [45.3, 17.5, 17.5], BLUE) # VESC TX -> ESP RX
thin([104, 104, 124], [14.5, 11.5, 11.5], INK)      # shared ground
for n, y in [('TX  GPIO17', 20.5), ('RX  GPIO18', 17.5), ('GND', 11.5)]:
    mono(ax, 125, y, n, size=7.6, color=BLUE if n != 'GND' else INK, zorder=3)
point(ax, (58, 38), (108, 30), "TX to RX, RX to TX.\nthe two data wires swap", color=BLUE, rad=-0.2)
point(ax, (128, 36), (117.8, 45), "leave the controller's 5V\npin off the ESP32", color=RED, rad=-0.2, ha='left')
ax.annotate('', xy=(135, 25.2), xytext=(135, 31), arrowprops=dict(arrowstyle='->', color=GOLD, lw=2))
note(ax, 136.5, 29.5, '5V from the power board', size=9, color=GOLD)

mono(ax, 149, -1.5, 'wiring from issues #18 (throttle), #20 (fuse) and #22 (UART). GPIO choice is a suggestion.', size=7, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'motor-controller-connections.png'))
