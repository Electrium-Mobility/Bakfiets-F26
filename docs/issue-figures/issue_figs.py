# Figures for the Bakfiets F26 GitHub issues. Hand-drawn look, one idea per picture.
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Wedge
plt.rcParams['font.family'] = 'Ink Free'
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
BG = '#f7f5f0'; INK = '#222'; RED = '#d23a2a'; BLU = '#2f62c9'; BLK = '#222'; ORG = '#d97a2b'; GRN = '#2f7d4f'; PUR = '#7b3fb0'; GRY = '#9a968c'
DARK = '#1d1d1d'; SLATE = '#3d4957'; TAN = '#e8d3a8'; YEL = '#f0b429'


def page(w, h, title):
    fig, ax = plt.subplots(figsize=(w / 10, h / 10), facecolor=BG)
    ax.set_facecolor(BG); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off')
    ax.text(3, h - 4, title, fontsize=25, color=INK, ha='left', va='center')
    return fig, ax


def t(ax, x, y, s, c=INK, fs=15, ha='center', **k):
    ax.text(x, y, s, color=c, fontsize=fs, ha=ha, va='center', zorder=9, **k)


def w(ax, xs, ys, c=BLK, lw=3.5, ls='-'):
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle='round', solid_joinstyle='round', zorder=2)


def box(ax, x, y, bw, bh, s='', fc=DARK, tc='white', fs=16, ec='#000', ls='-'):
    ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle='round,pad=0.2,rounding_size=1.2', fc=fc, ec=ec, lw=2, ls=ls, zorder=4))
    if s:
        t(ax, x + bw / 2, y + bh / 2, s, c=tc, fs=fs)


def arrow(ax, a, b, c=INK, lw=3):
    ax.annotate('', xy=b, xytext=a, zorder=3, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, mutation_scale=20, shrinkA=0, shrinkB=0))


def pin(ax, x, y, s, side, c=YEL, tc='white'):
    ax.add_patch(Circle((x, y), 0.8, fc=c, ec='#000', zorder=7))
    t(ax, x + (-2 if side == 'l' else 2), y, s, c=tc, ha='right' if side == 'l' else 'left', fs=14)


def res(ax, x, y, bw=7, bh=3.6, vertical=False):
    if vertical:
        ax.add_patch(FancyBboxPatch((x - bh / 2, y), bh, bw, boxstyle='round,pad=0.1', fc=TAN, ec=INK, lw=2, zorder=5))
    else:
        ax.add_patch(FancyBboxPatch((x, y - bh / 2), bw, bh, boxstyle='round,pad=0.1', fc=TAN, ec=INK, lw=2, zorder=5))


def done(fig, name):
    fig.savefig(os.path.join(OUT, name + '.png'), dpi=130, bbox_inches='tight', facecolor=BG)
    plt.close(fig)


# 1. what the CAN link does
fig, ax = page(140, 42, 'What this task builds')
box(ax, 4, 12, 26, 15, 'motor\ncontroller', fs=17)
box(ax, 50, 14, 17, 11, 'CAN Pal', fc=GRN, fs=16)
box(ax, 84, 12, 20, 15, 'ESP32', fs=18)
box(ax, 118, 12, 19, 15, '24 km/h\n46 V  70%', fc='#10243f', fs=15)
w(ax, [30, 50], [21, 21], PUR); w(ax, [30, 50], [18, 18], GRN)
t(ax, 40, 26, 'CAN wires', fs=14); t(ax, 40, 13.5, 'speed + battery', fs=13, c=GRY)
arrow(ax, (67, 19.5), (84, 19.5)); t(ax, 75.5, 24, 'TX, RX', fs=14)
arrow(ax, (104, 19.5), (118, 19.5)); t(ax, 127.5, 8.5, 'screen', fs=14)
t(ax, 70, 4, 'the data only travels one way in this task: controller to screen', c=GRY, fs=14)
done(fig, 'can-what-it-does')

# 2. CAN wiring
fig, ax = page(144, 66, 'Wiring the ESP32 to the motor controller')
box(ax, 4, 12, 30, 42); t(ax, 15, 48, 'ESP32', c='white', fs=19)
box(ax, 60, 12, 26, 42, fc=GRN); t(ax, 73, 48, 'CAN Pal', c='white', fs=19)
box(ax, 112, 12, 28, 42); t(ax, 126, 48, 'motor\ncontroller', c='white', fs=16)
t(ax, 126, 40.5, '4-pin CAN plug', c='white', fs=13)
for y, a, b, c in [(44, '3.3 V', 'Vcc', RED), (37, 'GND', 'GND', BLK), (30, 'GPIO 17', 'TX', BLU), (23, 'GPIO 18', 'RX', ORG)]:
    w(ax, [34, 60], [y, y], c); pin(ax, 34, y, a, 'l'); pin(ax, 60, y, b, 'r')
for y, a, b, c in [(38, 'H', 'CAN-H (pin 3)', PUR), (31, 'L', 'CAN-L (pin 2)', GRN), (24, 'GND', 'GND (pin 1)', BLK)]:
    w(ax, [86, 112], [y, y], c); pin(ax, 86, y, a, 'l'); pin(ax, 112, y, b, 'r')
pin(ax, 112, 17, '5 V (pin 4): leave empty', 'r', c='#bbb', tc='#ccc')
t(ax, 73, 16, 'termination\nswitch: ON', c='white', fs=13)
t(ax, 47, 56, 'labels match: TX to TX, RX to RX', c=BLU, fs=14)
t(ax, 99, 44, 'green terminal', fs=13)
t(ax, 72, 5, 'pack off at the antispark before plugging anything in. check the labels printed on the controller first', c=RED, fs=15)
done(fig, 'can-wiring')

# 3. speed maths
fig, ax = page(146, 40, 'Turning the controller\'s number into km/h')
xs = [3, 39, 75, 111]
items = [('ERPM\nfrom the controller', '5000', SLATE), ('divide by\npole pairs', '5000 / 23 = 217\nwheel turns a minute', SLATE), ('multiply by wheel\ncircumference', '217 x 1.9 m = 413\nmetres a minute', SLATE), ('multiply by 60,\ndivide by 1000', '413 x 60 / 1000\n= 24.8 km/h', GRN)]
for x, (a, b, c) in zip(xs, items):
    box(ax, x, 16, 29, 13, a, fc=c, fs=15); t(ax, x + 14.5, 9, b, fs=15)
for x in xs[:-1]:
    arrow(ax, (x + 29.5, 22.5), (x + 35.5, 22.5))
t(ax, 73, 3, 'made-up example. 23 pole pairs and 1.9 m are placeholders until we measure ours', c=RED, fs=15)
done(fig, 'speed-math')

# 4. voltage divider
fig, ax = page(116, 76, 'The voltage divider')
w(ax, [24, 24], [66, 8]); box(ax, 8, 62, 32, 7, 'battery +  (up to 50.4 V)', fc=RED, fs=14)
res(ax, 24, 44, bw=12, vertical=True); t(ax, 28, 50, '200 kΩ', ha='left', fs=17)
res(ax, 24, 19, bw=12, vertical=True); t(ax, 28, 25, '10 kΩ', ha='left', fs=17)
w(ax, [24, 66], [36, 36], BLU); ax.add_patch(Circle((24, 36), 0.9, fc=BLU, ec=BLU, zorder=6))
t(ax, 27, 32.5, 'about 2.4 V here', ha='left', c=BLU, fs=15)
res(ax, 42, 36, bw=9); t(ax, 46.5, 41, '1 kΩ', fs=16)
w(ax, [60, 60], [36, 22], BLU); ax.add_patch(Circle((60, 36), 0.9, fc=BLU, ec=BLU, zorder=6))
ax.plot([55, 65], [22, 22], color=INK, lw=4, zorder=5); ax.plot([55, 65], [19.5, 19.5], color=INK, lw=4, zorder=5)
t(ax, 67, 21, '100 nF capacitor', ha='left', fs=15)
w(ax, [60, 60], [19.5, 8]); w(ax, [24, 100], [8, 8])
box(ax, 72, 29, 34, 15, 'ESP32\npin: GPIO 1, 2, 4, 6, 7 or 8', fs=14)
w(ax, [100, 100], [8, 29]); w(ax, [66, 72], [36, 36], BLU)
t(ax, 89, 25, 'GND', fs=14, ha='left')
t(ax, 62, 3, 'measure the blue point with a multimeter before connecting it to the ESP32', c=RED, fs=15)
done(fig, 'voltage-divider')

# 5. battery percent
fig, ax = plt.subplots(figsize=(8.6, 4.6), facecolor=BG); ax.set_facecolor(BG)
ax.plot([37, 50.4], [0, 100], color=BLU, lw=2.4, solid_capstyle='round')
ax.scatter([37, 43.7, 50.4], [0, 50, 100], s=70, color=BLU, edgecolor=BG, linewidth=2, zorder=5)
for x, y, s, ha in [(38.6, 1, '37 V is 0%', 'left'), (44.8, 42, '43.7 V is 50%', 'left'), (49.6, 103, '50.4 V is 100%', 'right')]:
    ax.text(x, y, s, fontsize=15, color=INK, ha=ha)
ax.set_xlim(36, 51.5); ax.set_ylim(-5, 110); ax.set_xlabel('battery voltage (V)', fontsize=15, color=INK); ax.set_ylabel('battery %', fontsize=15, color=INK)
ax.set_title('Turning volts into a battery %', fontsize=22, color=INK, loc='left')
ax.grid(axis='y', color='#e2ddd1', lw=0.8); ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
for s in ['left', 'bottom']:
    ax.spines[s].set_color('#b9b4a8')
ax.tick_params(colors='#6b675f', labelsize=12, length=0)
fig.savefig(os.path.join(OUT, 'battery-percent.png'), dpi=130, bbox_inches='tight', facecolor=BG); plt.close(fig)

# 6. voltage cutoffs
fig, ax = page(130, 36, 'What the two battery cutoffs do')
x0, x1 = 12, 118
def vx(v): return x0 + (v - 36) / (51 - 36) * (x1 - x0)
ax.add_patch(Rectangle((vx(40.8), 15), vx(50.4) - vx(40.8), 6, fc=GRN, ec='none', zorder=3))
ax.add_patch(Rectangle((vx(37.2), 15), vx(40.8) - vx(37.2), 6, fc=YEL, ec='none', zorder=3))
ax.add_patch(Rectangle((vx(36), 15), vx(37.2) - vx(36), 6, fc=RED, ec='none', zorder=3))
for v, s in [(50.4, '50.4 V\nfull'), (40.8, '40.8 V\ncutoff start'), (37.2, '37.2 V\ncutoff end')]:
    w(ax, [vx(v), vx(v)], [13, 23], INK, lw=2.5); t(ax, vx(v), 8, s, fs=15)
t(ax, vx(45.6), 26, 'full power', fs=15); t(ax, vx(39), 26, 'power fades', fs=15); t(ax, vx(36.3), 26, 'stop', fs=15, c=RED)
done(fig, 'voltage-cutoffs')

# 7. lights current
fig, ax = plt.subplots(figsize=(8.6, 4.2), facecolor=BG); ax.set_facecolor(BG)
ax.barh([1, 0], [7.5, 1.5], color=BLU, height=0.34)
ax.axvline(4, color=RED, lw=2.2, ls=(0, (4, 3)))
ax.text(4.1, 1.47, 'the 5 V converter can give 4 A', fontsize=15, color=INK, va='center')
ax.text(7.35, 1, '125 x 60 mA = 7.5 A', fontsize=15, color='white', va='center', ha='right')
ax.text(1.65, 0, '7.5 A x 20% = 1.5 A', fontsize=15, color=INK, va='center')
ax.set_yticks([1, 0]); ax.set_yticklabels(['full white', 'setBrightness(50)'], fontsize=15, color=INK)
ax.set_xlim(0, 8.2); ax.set_ylim(-0.5, 1.75); ax.set_xlabel('current (A)', fontsize=15, color=INK)
ax.set_title('Example: the 2024 strip on its own', fontsize=22, color=INK, loc='left')
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#b9b4a8'); ax.tick_params(colors='#6b675f', labelsize=12, length=0); ax.tick_params(axis='y', labelcolor=INK)
fig.savefig(os.path.join(OUT, 'lights-current.png'), dpi=130, bbox_inches='tight', facecolor=BG); plt.close(fig)

# 8. 5 V map
fig, ax = page(132, 56, 'Everything that shares the 5 V supply')
box(ax, 4, 20, 20, 13, 'battery\n50.4 V', fc=RED, fs=15)
box(ax, 36, 19, 24, 15, '5 V converter\nup to 4 A', fc=SLATE, fs=15)
arrow(ax, (24.5, 26.5), (36, 26.5), RED)
loads = ['ESP32 and screen', 'headlight', 'rear light', 'turn signals (4)', 'side LED strip']
for i, s in enumerate(loads):
    y = 42 - i * 8.2
    box(ax, 88, y, 40, 6.2, s, fc='#fff7e3', tc=INK, fs=15)
    w(ax, [76, 88], [y + 3.1, y + 3.1], ORG)
w(ax, [60, 76], [26.5, 26.5], ORG); w(ax, [76, 76], [45.1, 12.3], ORG)
t(ax, 68, 30.5, '5 V', c=ORG, fs=17)
t(ax, 66, 4, 'add up the current of every box on the right. the total has to fit under 4 A', c=RED, fs=16)
done(fig, 'five-volt-map')

# 9. level shifter
fig, ax = page(132, 32, 'What a level shifter does')
box(ax, 4, 9, 22, 12, 'ESP32', fs=18); box(ax, 54, 9, 24, 12, 'level\nshifter', fc=GRN, fs=16); box(ax, 106, 9, 22, 12, 'LED strip', fc=SLATE, fs=17)
arrow(ax, (26.5, 15), (54, 15), BLU); arrow(ax, (78.5, 15), (106, 15), BLU)
t(ax, 40, 19.5, '3.3 V signal', c=BLU, fs=15); t(ax, 92, 19.5, '5 V signal', c=BLU, fs=15)
t(ax, 66, 4, 'the strip wants at least about 3.5 V, so 3.3 V straight from the ESP32 may be too low', c=GRY, fs=14)
done(fig, 'level-shifter')

# 10. post vs IS
fig, ax = page(120, 58, 'Post mount or IS mount?')
for x0_, name, vertical in [(8, 'post mount', False), (68, 'IS mount', True)]:
    ax.add_patch(Polygon([(x0_, 44), (x0_ + 44, 40), (x0_ + 44, 34), (x0_, 38)], closed=True, fc='#6fb58c', ec=INK, lw=2, zorder=3))
    t(ax, x0_ + 22, 45.5, 'frame tube', fs=14)
    box(ax, x0_ + 8, 16, 28, 12, 'caliper', fc=SLATE, fs=15)
    t(ax, x0_ + 22, 5, name, fs=19)
    for bx in (x0_ + 15, x0_ + 29):
        if not vertical:
            w(ax, [bx, bx], [18, 39], '#555', lw=7)
            ax.add_patch(Rectangle((bx - 2.2, 14), 4.4, 3, fc='#888', ec=INK, zorder=6))
        else:
            ax.add_patch(Circle((bx, 22), 2.4, fc='#888', ec=INK, lw=2, zorder=6))
            ax.add_patch(Circle((bx, 22), 0.9, fc=INK, ec=INK, zorder=7))
t(ax, 30, 10.5, 'bolts run along the line of the wheel', fs=14, c=BLU)
t(ax, 90, 10.5, 'bolts point straight at you, across the bike', fs=14, c=BLU)
done(fig, 'post-vs-is-mount')

# 11. rear brake plan
fig, ax = page(120, 72, 'The rear brake plan')
ax.add_patch(Circle((48, 34), 26, fc='none', ec=BLK, lw=9, zorder=2))
ax.add_patch(Circle((48, 34), 13, fc=DARK, ec='#000', lw=2, zorder=3))
ax.add_patch(Circle((48, 34), 9.5, fc='#c9c5ba', ec='#555', lw=2, zorder=4))
ax.add_patch(Circle((48, 34), 6, fc=DARK, ec='#000', lw=1.5, zorder=5))
ax.add_patch(Circle((48, 34), 1.8, fc='#aaa', ec='#000', zorder=6))
w(ax, [48, 27], [34, 60], '#37a56a', lw=9)
ax.add_patch(FancyBboxPatch((33, 43.5), 8, 5, boxstyle='round,pad=0.2', fc=RED, ec='#000', lw=2, zorder=7))
for label, xy, target in [('rotor: the metal disc,\nbolted to the motor\'s side cover', (92, 36), (57.5, 34)), ('caliper: squeezes the disc,\nmounted on the seat stay', (92, 58), (41, 46)), ('hub motor', (92, 16), (48, 25)), ('seat stay', (11, 50), (31, 54))]:
    ax.annotate(label, xy=target, xytext=xy, fontsize=15, color=INK, ha='center', va='center', zorder=9, arrowprops=dict(arrowstyle='->', color=RED, lw=2, shrinkA=4, shrinkB=2))
t(ax, 60, 3.5, 'caliper and rotor come from the green mountain bike in the bay', c=GRY, fs=15)
done(fig, 'rear-brake-plan')

# 12. AWG sizes
fig, ax = page(120, 40, 'AWG: a smaller number means a thicker wire')
for x, d, name, use in [(22, 2.053, '12 AWG', 'battery and motor'), (60, 1.024, '18 AWG', '5 V power'), (98, 0.644, '22 AWG', 'small signals')]:
    ax.add_patch(Circle((x, 22), d * 3.4, fc='#c77a3a', ec=INK, lw=1.5, zorder=4))
    t(ax, x, 11, name, fs=18); t(ax, x, 6, use, fs=15, c=GRY)
t(ax, 60, 30.5, 'circles show the metal core, drawn to the same scale', c=GRY, fs=14)
done(fig, 'awg-sizes')

# 13. antispark ground
fig, ax = page(146, 62, 'If the antispark switches the negative wire')
for x, good, head in [(4, True, 'do this: negative from the switched side'), (76, False, 'avoid this: negative from the battery side')]:
    t(ax, x + 32, 53, head, c=GRN if good else RED, fs=16)
    box(ax, x, 36, 14, 9, 'battery', fc=SLATE, fs=14); box(ax, x + 22, 36, 16, 9, 'antispark', fc=YEL, tc=INK, fs=14); box(ax, x + 48, 36, 16, 9, 'motor\ncontroller', fs=13)
    box(ax, x + 22, 12, 18, 10, '5 V converter\nand ESP32', fc=SLATE, fs=13)
    w(ax, [x + 14, x + 22], [40.5, 40.5]); w(ax, [x + 38, x + 48], [40.5, 40.5])
    w(ax, [x + 56, x + 56, x + 40], [36, 17, 17], BLU); t(ax, x + 50, 13.5, 'ground in\nthe CAN wire', c=BLU, fs=12)
    if good:
        w(ax, [x + 43, x + 43, x + 34, x + 34], [40.5, 29, 29, 22]); ax.add_patch(Circle((x + 43, 40.5), 0.9, fc=BLK, zorder=6))
    else:
        w(ax, [x + 18, x + 18, x + 28, x + 28], [40.5, 29, 29, 22], RED, lw=5); ax.add_patch(Circle((x + 18, 40.5), 0.9, fc=RED, ec=RED, zorder=6))
t(ax, 108, 5, 'this path goes around the switch\nand can damage the controller', c=RED, fs=15)
t(ax, 36, 5, 'the switch can do its job', c=GRN, fs=15)
done(fig, 'antispark-ground')

# 14. harness overview
fig, ax = page(150, 92, 'The current wiring plan')
box(ax, 4, 56, 20, 13, 'Pack 4\n48 V', fc=SLATE, fs=16); box(ax, 36, 57, 18, 11, 'antispark', fc=YEL, tc=INK, fs=15); box(ax, 72, 54, 26, 17, 'motor\ncontroller', fs=18); box(ax, 122, 56, 24, 13, 'hub motor', fc=SLATE, fs=16)
w(ax, [24, 36], [62.5, 62.5], RED, lw=5); w(ax, [54, 72], [62.5, 62.5], RED, lw=5); t(ax, 30, 66, 'XT60', fs=13); t(ax, 63, 66, 'XT60', fs=13)
w(ax, [98, 122], [66, 66], ORG, lw=5); w(ax, [98, 122], [62.5, 62.5], YEL, lw=5); w(ax, [98, 122], [59, 59], GRN, lw=5); t(ax, 110, 70, '3 motor wires', fs=14)
w(ax, [98, 106, 106, 122], [56, 56, 52, 52, ], BLU, lw=2.5); w(ax, [122, 122], [52, 56], BLU, lw=2.5); t(ax, 113, 49.5, 'hall sensor plug', fs=13, c=BLU)
box(ax, 4, 74, 20, 6, 'XLR charge port', fc='#fff7e3', tc=INK, fs=13); w(ax, [14, 14], [69, 74], RED, lw=3)
w(ax, [63, 63], [62.5, 38], RED, lw=3.5); ax.add_patch(Circle((63, 62.5), 1, fc=RED, ec=RED, zorder=6))
box(ax, 52, 26, 22, 12, '5 V converter', fc=SLATE, fs=15)
w(ax, [52, 30], [32, 32], ORG, lw=3.5); box(ax, 8, 26, 22, 12, 'lights', fc='#fff7e3', tc=INK, fs=16)
w(ax, [63, 63], [26, 18], ORG, lw=3.5); box(ax, 52, 6, 22, 12, 'ESP32', fs=17); w(ax, [52, 30], [12, 12], ORG, lw=3.5, ls=(0, (2, 2))); box(ax, 8, 6, 22, 12, 'screen', fc='#10243f', fs=16)
w(ax, [74, 90, 90], [12, 12, 54], PUR, lw=3); t(ax, 88.5, 34, 'CAN', fs=15, c=PUR, ha='right')
box(ax, 106, 26, 24, 10, 'thumb throttle', fc='#7a4a1e', fs=14); box(ax, 106, 10, 24, 10, 'rear brake lever', fc=SLATE, fs=14)
w(ax, [106, 96, 96], [31, 31, 54], BLU, lw=2.5); w(ax, [106, 94, 94], [15, 15, 54], BLU, lw=2.5)
w(ax, [106, 100, 100, 74], [12, 12, 8, 8], BLU, lw=2, ls=(0, (2, 2)))
t(ax, 118, 6.5, 'dashed: brake light signal', fs=12, c=BLU)
done(fig, 'wiring-overview')

# 15. pigtail
fig, ax = page(126, 36, 'What a pigtail is')
box(ax, 4, 11, 22, 12, 'brake\nlever', fc=SLATE, fs=16); w(ax, [26, 46], [17, 17], BLK, lw=5)
ax.add_patch(Rectangle((46, 12.5), 9, 9, fc=YEL, ec='#000', lw=2, zorder=5)); ax.add_patch(Rectangle((56, 12.5), 9, 9, fc=DARK, ec='#000', lw=2, zorder=5))
w(ax, [65, 98], [20.5, 20.5], RED); w(ax, [65, 98], [17, 17], BLU); w(ax, [65, 98], [13.5, 13.5], BLK)
t(ax, 50.5, 26, 'the lever\'s plug', fs=14); t(ax, 60.5, 8, 'matching half', fs=14); t(ax, 112, 17, 'three bare wires\nwe can connect', fs=14)
t(ax, 82, 26, 'the pigtail: a short cable', fs=14, c=BLU)
done(fig, 'pigtail')
print(sorted(os.listdir(OUT)))
