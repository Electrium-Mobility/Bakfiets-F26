# Plain pen sketch: where the Y-cable sits in the power path.
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams['font.family'] = 'Ink Free'
plt.rcParams['path.sketch'] = (0.5, 60, 1.2)
OUT = sys.argv[1]
INK, GRAY, RED = '#1a1a1a', '#8a8a8a', '#c0392b'

fig, ax = plt.subplots(figsize=(12, 5.4), facecolor='white')
ax.set_xlim(0, 120); ax.set_ylim(0, 54); ax.axis('off')


def t(x, y, s, fs=15, c=INK, ha='center'):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va='center')


def box(x, y, w, h, name, fs=16):
    ax.add_patch(Rectangle((x, y - h / 2), w, h, fill=False, ec=INK, lw=1.8))
    t(x + w / 2, y, name, fs=fs)


def cable(xs, ys):
    # a red and a black wire side by side
    ax.plot(xs, [v + 0.6 for v in ys], color=RED, lw=2.2)
    ax.plot(xs, [v - 0.6 for v in ys], color=INK, lw=2.2)


def plug(x, y, name, big=True):
    w, h = (2.4, 4) if big else (1.8, 3)
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fill=False, ec=INK, lw=1.6, hatch='///'))
    t(x, y - h / 2 - 2.2, name, fs=11, c=GRAY)


Y0 = 30
box(1, Y0, 16, 12, 'Pack 4\nbattery')
cable([17, 24], [Y0, Y0]); plug(25, Y0, 'XT60')
cable([26.2, 30], [Y0, Y0])
box(30, Y0, 18, 12, 'antispark\nand power button', fs=13)
cable([48, 53], [Y0, Y0]); plug(54, Y0, 'XT60')

# the Y-cable itself
cable([55.2, 64], [Y0, Y0])
ax.add_patch(Rectangle((51, 7), 36, 41, fill=False, ec=GRAY, lw=1.2, ls='--'))
t(68.5, 51, 'the Y-cable (this task)', fs=14, c=GRAY)
t(60, Y0 + 4, 'thick', fs=11, c=GRAY)
cable([64, 70, 82], [Y0, 42, 42]); plug(83, 42, 'XT60')
cable([64, 70, 82], [Y0, 16, 16]); plug(83, 16, 'small plug', big=False)
t(75, 45.5, 'thick', fs=11, c=GRAY)
t(75, 19.5, 'thin is fine', fs=11, c=GRAY)

cable([84.2, 92], [42, 42])
box(92, 42, 25, 10, 'motor controller', fs=15)
t(104.5, 34.5, 'all the motor power', fs=11, c=GRAY)
cable([83.9, 92], [16, 16])
box(92, 16, 25, 10, 'power board', fs=15)
t(104.5, 8.5, '5 V for the lights and electronics', fs=11, c=GRAY)

ax.plot([2, 7], [4, 4], color=RED, lw=2.4); t(8.5, 4, '+', fs=14, c=RED, ha='left')
ax.plot([12, 17], [4, 4], color=INK, lw=2.4); t(18.5, 4, '-', fs=14, ha='left')
fig.savefig(OUT, dpi=140, bbox_inches='tight', facecolor='white')
