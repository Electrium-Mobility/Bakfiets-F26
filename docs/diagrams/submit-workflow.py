import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notebook import *
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np

fig, ax = page(150, 92, (15, 9.2))
note(ax, 8, 88, 'Getting your work into the repo', size=24, weight='bold')
note(ax, 8, 83.2, 'The top line is main, the copy everyone shares. You branch off it, work on your branch, and a pull request brings it back.',
     size=11.5, color=PENCIL)

MAIN_Y, BR_Y = 66, 40
# main line
ax.plot([10, 145], [MAIN_Y, MAIN_Y], color=INK, lw=4, solid_capstyle='round', zorder=2)
note(ax, 146, MAIN_Y, 'main', size=14, weight='bold', ha='left')
for x in (14, 22, 30, 128, 138):
    ax.add_patch(Circle((x, MAIN_Y), 1.3, fc=PAPER, ec=INK, lw=2, zorder=3))
note(ax, 11, MAIN_Y + 4.5, "other people's work", size=9.5, color=PENCIL)

# branch curve out and back
def curve(x0, y0, x1, y1, col):
    t = np.linspace(0, 1, 60); s = (1 - np.cos(np.pi * t)) / 2
    ax.plot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * s, color=col, lw=4, solid_capstyle='round', zorder=2)
curve(38, MAIN_Y, 50, BR_Y, GREEN)
ax.plot([50, 104], [BR_Y, BR_Y], color=GREEN, lw=4, solid_capstyle='round', zorder=2)
curve(104, BR_Y, 118, MAIN_Y, GREEN)
ax.add_patch(Circle((38, MAIN_Y), 1.6, fc=GREEN, ec=INK, lw=1.5, zorder=4))
ax.add_patch(Circle((118, MAIN_Y), 2.0, fc=GREEN, ec=INK, lw=1.8, zorder=4))
for x in (60, 72, 84):
    ax.add_patch(Circle((x, BR_Y), 1.5, fc=GREEN, ec=INK, lw=1.5, zorder=4))
note(ax, 58, BR_Y + 3.4, 'your branch: battery-mount-sketch', size=10, color=GREEN)

def step(x, y, n, head, button, extra=None, color=INK):
    note(ax, x, y, f'{n}. {head}', size=12.5, color=color, weight='bold', va='top')
    mono(ax, x, y - 4.3, button, size=8.8, color=INK, va='top', linespacing=1.3)
    if extra: note(ax, x, y - 4.3 - 3.3 * (button.count('\n') + 1), extra, size=10, color=PENCIL, va='top', linespacing=1.25)

# 0: once
ax.add_patch(FancyBboxPatch((8, 4), 30, 17, boxstyle='round,pad=0,rounding_size=1', fc='#f1ece0', ec=PENCIL, lw=1, ls=(0, (4, 3))))
step(10, 19.5, 0, 'first time only', '[File > Clone repository]', 'copies the whole repo\nonto your laptop', color=PENCIL)

step(10, 60, 1, 'get the latest', '[Fetch origin]\n[Pull origin]', 'do this before every\nnew task')
point(ax, (26, 56.5), (36.5, MAIN_Y - 1.4), '', rad=0.2)

step(24, 35, 2, 'make a branch', '[Current branch >\n New branch]', 'name it after the task')
point(ax, (38.5, 33.5), (45, BR_Y + 6), '', rad=-0.25)

step(56, 35, 3, 'work, then commit', '[Summary box, then\n Commit to <branch>]', 'each dot is one commit.\ncommit whenever something works.\nstill only on your laptop')

step(86, 35, 4, 'push', '[Publish branch]\nlater: [Push origin]', "now it's on GitHub")

step(112, 35, 5, 'pull request', '[Create Pull Request]', 'say what you did.\nadd "Closes #5" so the\nissue closes with it.')
point(ax, (110, 26), (108.5, BR_Y + 3.5), '', rad=0.3)

step(66, 81, 6, 'review', 'your subteam lead reads it', None, color=GOLD)
note(ax, 66, 73, 'asked for changes? fix them, commit, push.\nthe pull request updates on its own.', size=10, color=GOLD, va='top', linespacing=1.25)
point(ax, (100, 71), (93, BR_Y + 1.8), '', color=GOLD, rad=-0.3)

note(ax, 121, 58, '7. merged', size=12.5, color=GREEN, weight='bold', va='top')
note(ax, 121, 54, 'the lead merges it.\nyour work is on main now.', size=10, color=PENCIL, va='top', linespacing=1.25)
point(ax, (122.5, 58.5), (119.5, MAIN_Y - 1.8), '', color=GREEN, rad=-0.3)

note(ax, 44, 11, 'Steps 1 to 4 happen on your laptop in GitHub Desktop.', size=10.5, color=PENCIL)
note(ax, 44, 7.5, 'Steps 5 to 7 happen on github.com.', size=10.5, color=PENCIL)
note(ax, 98, 10, 'No permission to push? GitHub Desktop offers\nto fork. Click [Fork this repository], then\n[To contribute to the parent project].',
     size=10, color=PENCIL, linespacing=1.3)
save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submit-workflow.png'))
