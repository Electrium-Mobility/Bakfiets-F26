import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notebook import *
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np

fig, ax = page(150, 84, (15, 8.4))
note(ax, 8, 80, 'Your onboarding, start to finish', size=24, weight='bold')
note(ax, 8, 75.2, 'Everyone does steps 1 to 4. Then you follow your subteam\'s line, and it ends at the term projects.',
     size=11.5, color=PENCIL)

MID = 42
def stop(x, y, label, head, body, col=INK, r=2.4):
    ax.add_patch(Circle((x, y), r, fc=PAPER, ec=col, lw=2.2, zorder=3))
    note(ax, x, y, label, size=11 if len(label) < 2 else 9, color=col, ha='center', weight='bold', zorder=4)
    note(ax, x, y - 4, head, size=11, weight='bold', ha='center', va='top', color=col)
    if body: note(ax, x, y - 7.4, body, size=9.2, ha='center', va='top', color=PENCIL, linespacing=1.15)
def s_curve(x0, y0, x1, y1, col, lw=3):
    t = np.linspace(0, 1, 50); s = (1 - np.cos(np.pi * t)) / 2
    ax.plot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * s, color=col, lw=lw, zorder=1)

# shared start
ax.plot([12, 66], [MID, MID], color=INK, lw=3, zorder=1)
stop(12, MID, '1', 'accounts', 'GitHub account,\njoin Discord, post\nyour username')
stop(28, MID, '2', 'get the files', 'clone with GitHub\nDesktop. new to Git?\nwatch the video first')
stop(44, MID, '3', 'install', 'SolidWorks, KiCad\nor Arduino IDE')
stop(60, MID, '4', 'WHMIS', 'about an hour on\nLEARN. needed for\nbay work, not Stage 1', RED)

lanes = [(GREEN, 64, 'mechanical', 'open the bike in\nSolidWorks, post\na screenshot', 'e.g. #2, #3, #5, #6'),
         (GOLD, MID, 'electrical', 'read the anti-spark\nschematic, notes\non #8', 'e.g. #7, #9, #10, #11'),
         (BLUE, 20, 'firmware', 'run the desk demo,\nphoto on #12', 'e.g. #13, #14, #15')]
for col, y, name, s1, s2 in lanes:
    s_curve(66, MID, 76, y, col)
    ax.plot([76, 118], [y, y], color=col, lw=3, zorder=1)
    s_curve(118, y, 128, MID, col)
    note(ax, 77, y + 3.4, name, size=12, color=col, weight='bold')
    stop(86, y, 'S1', 'Stage 1', s1, col)
    stop(108, y, 'S2', 'Stage 2', 'one starter task,\n' + s2, col)

ax.add_patch(FancyBboxPatch((128, 31), 19, 22, boxstyle='round,pad=0,rounding_size=1.5', fc='#f3efe4', ec=INK, lw=2, zorder=3))
note(ax, 137.5, 50.5, 'term\nprojects', size=13.5, weight='bold', ha='center', va='top', linespacing=1.0, zorder=4)
note(ax, 137.5, 42, "issues labelled\n'term project'.\nonboarding is\ndone here", size=9.2, ha='center', va='top', color=PENCIL, linespacing=1.15, zorder=4)
point(ax, (58, 60), (67.5, MID + 1.6), 'pick your\nsubteam here', rad=-0.3)

note(ax, 8, 4, 'Claim any task by commenting "I\'ll take this" on its issue. Stuck? Ask in your subteam channel.', size=10.5, color=PENCIL)
save(fig, os.path.join(HERE, 'onboarding-path.png'))
