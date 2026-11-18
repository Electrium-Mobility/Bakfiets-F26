# Plain pen sketch of the whole pigtail hookup: how one connection is built (top),
# and where the throttle and both brake levers go on the motor controller (bottom).
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arc
plt.rcParams['font.family'] = 'Ink Free'
plt.rcParams['path.sketch'] = (0.5, 60, 1.2)
OUT = sys.argv[1]
INK, GRAY = '#1a1a1a', '#8a8a8a'
WIRE = {'power': '#c0392b', 'signal': '#d4a017', 'ground': INK}

fig, ax = plt.subplots(figsize=(13, 15), facecolor='white')
ax.set_xlim(0, 130); ax.set_ylim(0, 150); ax.axis('off')


def t(x, y, s, fs=15, c=INK, ha='center', va='center'):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va)


def box(x, y, w, h, hatch=None, lw=1.8, ls='-'):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=INK, lw=lw, hatch=hatch, ls=ls))


# ======================= top: one connection, step by step =======================
t(65, 146, 'how one connection is built', fs=21)
Y = 122  # middle wire height

box(2, Y - 6, 16, 12); t(10, Y, 'throttle\nor brake\nlever', fs=13)
ax.plot([18, 23], [Y, Y], color=INK, lw=2.4)
box(23, Y - 5, 5, 10); t(25.5, Y + 8, 'its julet\nplug', fs=11, c=GRAY)
box(28.6, Y - 5, 5, 10, hatch='///'); t(31, Y - 9, 'pigtail\njulet', fs=11, c=GRAY)

# three pigtail wires, then the solder joints with heat shrink, then the new wire, then crimps
ys = {'power': Y + 3, 'signal': Y, 'ground': Y - 3}
for kind, y in ys.items():
    c = WIRE[kind]
    ax.plot([33.6, 52], [y, y], color=c, lw=2.4)                 # pigtail wire
    ax.add_patch(Circle((53, y), 0.7, fc=INK, ec=INK))           # solder joint
    ax.plot([54, 92], [y, y], color=c, lw=2.4)                   # 22 to 24 AWG wire
    ax.add_patch(Rectangle((92, y - 0.7), 4, 1.4, fc='white', ec=INK, lw=1.4))  # crimp
for y in ys.values():  # heat shrink over each joint
    ax.add_patch(FancyBboxPatch((49.5, y - 1.05), 7, 2.1, boxstyle='round,pad=0.1', fill=False, ec=GRAY, lw=1.3))

box(99, Y - 7, 6, 14, lw=2); t(102, Y + 10, 'VESC\nplug', fs=12, c=GRAY)
for y in ys.values():
    ax.plot([96, 99], [y, y], color=INK, lw=1.5)

# numbered steps under the drawing
steps = [
    (28, '1', 'push the two julet\nplugs together.\nif the pigtail won\'t go\nin, trim the outside of\nthe female connector'),
    (53, '2', 'solder 22 to 24 AWG\nwire onto all 3 pigtail\nwires. slide the heat\nshrink on first, then\nshrink it over the joint'),
    (94, '3', 'crimp the other end\nof all 3 wires, then\npush them into the\nVESC plug'),
]
for x, n, s in steps:
    ax.add_patch(Circle((x, Y - 16), 2.2, fill=False, ec=INK, lw=1.6)); t(x, Y - 16, n, fs=14)
    t(x, Y - 20, s, fs=12.5, va='top')
    ax.plot([x, x], [Y - 13.6, Y - 6], color=GRAY, lw=1, ls=':')
t(72, Y + 7, 'about 30 cm', fs=11, c=GRAY)
ax.annotate('', xy=(90, Y + 5.2), xytext=(56, Y + 5.2), arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1))

ax.plot([2, 128], [84, 84], color=GRAY, lw=1, ls='--')

# ======================= bottom: where everything plugs in =======================
t(65, 80, 'where everything plugs in', fs=21)
PITCH = 4.2
SX = 96
COMM = ['ADC3', 'ADC2', 'TX', 'RX', 'ADC1', 'GND', '3.3V', '5V']
SWD = ['3.3V', 'SWCLK', 'GND', 'SWDIO', 'NRST']


def socket(ytop, title, pins, used, maybe=()):
    t(SX - 1, ytop + 3, title, fs=14, ha='left')
    ax.add_patch(Rectangle((SX - 1.6, ytop - len(pins) * PITCH + 1), 3.2, len(pins) * PITCH, fill=False, ec=INK, lw=1.6))
    pos = {}
    for i, name in enumerate(pins):
        y = ytop - 1.2 - i * PITCH
        on = name in used
        ax.add_patch(Circle((SX, y), 0.8, fc=INK if on else 'white', ec=INK, lw=1.3))
        t(SX + 3, y, f'pin {i + 1}  {name}', fs=11.5, c=INK if on or name in maybe else GRAY, ha='left')
        pos[name] = y
    return pos


ax.add_patch(Rectangle((89, 4), 39, 71, fill=False, ec=INK, lw=2.2))
t(108.5, 72, 'motor controller (VESC)', fs=15)
swd = socket(66, 'SWD plug', SWD, {'3.3V', 'GND'})
comm = socket(40, 'COMM plug', COMM, {'ADC2', 'ADC1', 'GND', '3.3V'}, maybe={'ADC3'})


def part(name, y0, ls='-'):
    box(2, y0 - 5, 19, 10, ls=ls); t(11.5, y0, name, fs=14)
    ax.plot([21, 25], [y0, y0], color=INK, lw=2.4, ls=ls)
    box(25, y0 - 4, 4, 8, ls=ls); box(29, y0 - 4, 4, 8, hatch='///', ls=ls)


def wire(y_from, x_turn, y_to, kind, hop=None, ls='-'):
    c = WIRE[kind]
    ax.plot([33, x_turn], [y_from, y_from], color=c, lw=2.4, ls=ls)
    lo, hi = sorted((y_from, y_to))
    hops = sorted([hop] if isinstance(hop, (int, float)) else (hop or []))
    y = lo
    for h in hops:  # small hop wherever this wire jumps over another one
        ax.plot([x_turn, x_turn], [y, h - 1.3], color=c, lw=2.4, ls=ls)
        ax.add_patch(Arc((x_turn, h), 2.6, 2.6, theta1=-90, theta2=90, color=c, lw=2.4))
        y = h + 1.3
    ax.plot([x_turn, x_turn], [y, hi], color=c, lw=2.4, ls=ls)
    ax.plot([x_turn, SX - 0.8], [y_to, y_to], color=c, lw=2.4, ls=ls)


part('thumb throttle', 60)
wire(62.5, 68, swd['3.3V'], 'power')
wire(60, 64, swd['GND'], 'ground')
wire(57.5, 60, comm['ADC1'], 'signal', hop=[36.5, 34, 31.5])
t(46, 66, '#68', fs=13, c=GRAY)

part('brake lever 1', 34)
wire(36.5, 76, comm['ADC2'], 'signal')
wire(34, 84, comm['3.3V'], 'power', hop=comm['ADC1'])
wire(31.5, 80, comm['GND'], 'ground', hop=comm['ADC1'])
t(46, 40, '#69', fs=13, c=GRAY)

part('brake lever 2', 14, ls='--')
ax.plot([33, 50], [14, 14], color=GRAY, lw=1.6, ls='--')
t(52, 14, 'how the second lever\nconnects is #70', fs=13, ha='left')
t(11.5, 7, 'also #69', fs=12, c=GRAY)

leg_y = 3
for i, (kind, label) in enumerate([('power', 'red = power'), ('signal', 'yellow = signal'), ('ground', 'black = ground')]):
    x = 2 + i * 27
    ax.plot([x, x + 5], [leg_y, leg_y], color=WIRE[kind], lw=2.6)
    t(x + 6.5, leg_y, label, fs=13, ha='left')

t(108.5, 1, 'check the labels printed on our controller first', fs=11, c=GRAY)
fig.savefig(OUT, dpi=130, bbox_inches='tight', facecolor='white')
