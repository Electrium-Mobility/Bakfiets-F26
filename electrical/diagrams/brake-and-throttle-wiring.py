# Plain pen sketch: the brake lever and the thumb throttle wired to the motor controller together.
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc
plt.rcParams['font.family'] = 'Ink Free'
plt.rcParams['path.sketch'] = (0.5, 60, 1.2)
OUT = sys.argv[1]
INK, GRAY = '#1a1a1a', '#8a8a8a'
WIRE = {'power': '#c0392b', 'signal': '#2c5fb3', 'ground': INK}
PITCH = 4.5
COMM = ['ADC3', 'ADC2', 'TX', 'RX', 'ADC1', 'GND', '3.3V', '5V']
SWD = ['3.3V', 'SWCLK', 'GND', 'SWDIO', 'NRST']
SX = 71  # x of the socket pins

fig, ax = plt.subplots(figsize=(11, 10), facecolor='white')
ax.set_xlim(0, 100); ax.set_ylim(0, 92); ax.axis('off')


def t(x, y, s, fs=15, c=INK, ha='center'):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va='center')


def part(name, y0):
    ax.add_patch(Rectangle((1, y0 - 6), 22, 12, fill=False, ec=INK, lw=1.8))
    t(12, y0, name, fs=16)
    ax.plot([23, 29], [y0, y0], color=INK, lw=2.4)
    ax.add_patch(Rectangle((29, y0 - 5), 4, 10, fill=False, ec=INK, lw=1.8))
    ax.add_patch(Rectangle((33, y0 - 5), 4, 10, fill=False, ec=INK, lw=1.8, hatch='///'))
    t(31, y0 - 8, 'its plug', fs=11, c=GRAY)
    t(35, y0 + 8, 'pigtail', fs=11, c=GRAY)


def socket(ytop, title, pins, used):
    t(SX - 1, ytop + 3.5, title, fs=14, ha='left')
    ax.add_patch(Rectangle((SX - 1.6, ytop - len(pins) * PITCH + 1), 3.2, len(pins) * PITCH, fill=False, ec=INK, lw=1.6))
    pos = {}
    for i, name in enumerate(pins):
        y = ytop - 1.2 - i * PITCH
        ax.add_patch(Circle((SX, y), 0.8, fc=INK if name in used else 'white', ec=INK, lw=1.3))
        t(SX + 3, y, f'pin {i + 1}  {name}', fs=11.5, c=INK if name in used else GRAY, ha='left')
        pos[name] = y
    return pos


def wire(y_from, x_turn, y_to, kind, hop_at=None):
    c = WIRE[kind]
    ax.plot([37, x_turn], [y_from, y_from], color=c, lw=2.4)
    if hop_at is None:
        ax.plot([x_turn, x_turn], [y_from, y_to], color=c, lw=2.4)
    else:  # small hop where this wire jumps over another one
        lo, hi = sorted((y_from, y_to))
        ax.plot([x_turn, x_turn], [lo, hop_at - 1.4], color=c, lw=2.4)
        ax.plot([x_turn, x_turn], [hop_at + 1.4, hi], color=c, lw=2.4)
        ax.add_patch(Arc((x_turn, hop_at), 2.8, 2.8, theta1=-90, theta2=90, color=c, lw=2.4))
    ax.plot([x_turn, SX - 0.8], [y_to, y_to], color=c, lw=2.4)


ax.add_patch(Rectangle((64, 2), 35, 88, fill=False, ec=INK, lw=2.2))
t(81.5, 87, 'motor controller', fs=16)
swd = socket(80, 'SWD plug', SWD, {'3.3V', 'GND'})
comm = socket(52, 'COMM plug', COMM, {'ADC2', 'ADC1', 'GND', '3.3V'})

part('thumb throttle', 62)
wire(65, 44, swd['3.3V'], 'power')
wire(62, 48, swd['GND'], 'ground')
wire(59, 52, comm['ADC1'], 'signal')

part('brake lever', 22)
wire(25, 56, comm['ADC2'], 'signal', hop_at=comm['ADC1'])
wire(22, 59, comm['GND'], 'ground')
wire(19, 61.5, comm['3.3V'], 'power')

for i, kind in enumerate(['power', 'signal', 'ground']):
    y = 10 - i * 3.5
    ax.plot([2, 7], [y, y], color=WIRE[kind], lw=2.6)
    t(8.5, y, kind, fs=13, c=WIRE[kind], ha='left')
t(36, 6, 'check the labels printed on our controller first', fs=12, c=GRAY)
fig.savefig(OUT, dpi=140, bbox_inches='tight', facecolor='white')
