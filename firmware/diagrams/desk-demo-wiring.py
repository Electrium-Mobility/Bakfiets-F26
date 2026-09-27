import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'docs', 'diagrams'))
from notebook import *
from matplotlib.patches import Rectangle, Circle

fig, ax = page(120, 92, (12, 9.2))
note(ax, 8, 88, 'Wiring the desk demo', size=24, weight='bold')
note(ax, 8, 83.2, 'Four wires, screen to ESP32-S3. Hold the board with the USB ports at the bottom.\n'
                  'Everything goes on the left pin row, the one with 3V3 at the top.', size=11.5, color=PENCIL, linespacing=1.4)

# board
bx, by, bw, bh = 74, 6, 32, 70
ax.add_patch(Rectangle((bx, by), bw, bh, fc='#dfeee4', ec=GREEN, lw=2))
ax.add_patch(Rectangle((bx + 15, by + 46), 12, 15, fc='#e9e6df', ec=PENCIL, lw=1.2))
mono(ax, bx + 21, by + 53.5, 'ESP32-S3\nmodule', size=8, color=PENCIL, ha='center')
mono(ax, bx + 21, by + 33, 'DevKitC-1', size=10, color=GREEN, ha='center', weight='bold')
for i in range(2):
    ax.add_patch(Rectangle((bx + 10 + i * 11, by - 2.2), 6.5, 3.4, fc='#d9d4c7', ec=INK, lw=1.2))

left = ['3V3', '3V3', 'RST', '4', '5', '6', '7', '15', '16', '17', '18', '8', '3', '46', '9', '10', '11', '12', '13', '14', '5V', 'G']
top, step = by + bh - 4, 2.95
pin = {}
used = {0: 'VCC', 14: 'SCL', 15: 'SDA', 21: 'GND'}
for i, lab in enumerate(left):
    y = top - i * step
    hit = i in used
    ax.add_patch(Circle((bx + 2, y), 0.85, fc=INK if hit else PAPER, ec=INK, lw=1, zorder=3))
    name = lab if lab in ('3V3', 'RST', '5V', 'G') else 'GPIO' + lab
    mono(ax, bx + 3.8, y, name, size=8.4 if hit else 7.6, color=INK if hit else '#6f6a60', weight='bold' if hit else 'normal')
    pin[i] = (bx + 2, y)
    ax.add_patch(Circle((bx + bw - 2, y), 0.85, fc=PAPER, ec='#8c877c', lw=0.9))

# screen, on its side so the wires don't cross
sx, sy, sw, sh = 16, 38, 24, 30
ax.add_patch(Rectangle((sx, sy), sw, sh, fc='#dde6f3', ec=BLUE, lw=2))
ax.add_patch(Rectangle((sx + 3, sy + 3), sw - 11, sh - 6, fc='#1b1f27', ec=INK, lw=1))
note(ax, sx + 3 + (sw - 11) / 2, sy + sh / 2, '36 km/h', size=10, color='#8fd694', ha='center', rotation=270)
mono(ax, sx + sw / 2, sy + sh + 1.1, 'SSD1306 OLED, 0.96"', size=8.5, ha='center', va='bottom')
colors = {'GND': INK, 'VCC': RED, 'SCL': GOLD, 'SDA': BLUE}
sp = {}
for i, n in enumerate(['GND', 'VCC', 'SCL', 'SDA']):
    x, y = sx + sw - 2.8, sy + sh - 5 - i * 6.5
    ax.add_patch(Circle((x, y), 0.95, fc=INK, ec=INK, zorder=3))
    mono(ax, x - 2, y, n, size=8.5, ha='right', weight='bold')
    sp[n] = (x, y)

def wire(xs, ys, c): ax.plot(xs, ys, color=c, lw=3, solid_capstyle='round', zorder=2)
for n, i, lx in [('VCC', 0, 52), ('SCL', 14, 57), ('SDA', 15, 62)]:
    (x0, y0), (px, py) = sp[n], pin[i]
    wire([x0, lx, lx, px], [y0, y0, py, py], colors[n])
x0, y0 = sp['GND']; px, py = pin[21]
wire([x0, x0 + 4, x0 + 4, 9, 9, px], [y0, y0, sy + sh + 4, sy + sh + 4, py, py], colors['GND'])

# margin notes
point(ax, (48, 76.5), (bx + 1, pin[0][1] + 0.4), '3V3, not 5V', color=RED, rad=-0.25)
point(ax, (44, 17), (bx + 1, pin[15][1] - 0.8), 'SCL to 9, SDA to 10.\nswap them and the screen\nstays blank', rad=0.3)
point(ax, (11, 32.5), (sx + 3, sy + 0.3), 'check the labels on your own screen.\nsome have GND and VCC swapped', color=RED, rad=0.25)
point(ax, (108, 3), (bx + 18.8, by - 1.2), 'two USB-C ports.\nuse the one printed\nUSB, not UART', rad=0.3, ha='left')
note(ax, bx + bw + 1.2, top - 30, 'right row:\nnot used', size=9.5, color='#6f6a60')

rows = [('VCC', '3V3'), ('GND', 'G'), ('SCL', 'GPIO9'), ('SDA', 'GPIO10')]
note(ax, 12, 25.5, 'cheat sheet', size=12, weight='bold')
for k, (a, b) in enumerate(rows):
    y = 22 - k * 3.1
    ax.plot([12, 15.5], [y, y], color=colors[a], lw=4)
    mono(ax, 17, y, f'{a:<4} -> {b}', size=9.5)
note(ax, 12, 1.5, 'Unplug USB before you move any wires.', size=10.5, color=PENCIL)
mono(ax, 119, -1.8, 'pins: firmware/desk-demo/desk-demo.ino + Espressif DevKitC-1 v1.1 user guide', size=6.8, color='#6f6a60', ha='right')
save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'desk-demo-wiring.png'))
