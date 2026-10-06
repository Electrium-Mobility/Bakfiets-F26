import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notebook import *
from matplotlib.patches import FancyBboxPatch

fig, ax = page(150, 96, (15, 9.6))
note(ax, 8, 92, 'How the Bakfiets team is run', size=24, weight='bold')
note(ax, 8, 87.2, 'Roles, not names. Who holds each role is in ONBOARDING.md.', size=11.5, color=PENCIL)

def role(x, y, w, h, title, body, col, dashed=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h), w, h, boxstyle='round,pad=0,rounding_size=1.2', fc='#f3efe4',
                                ec=col, lw=2, ls=(0, (4, 3)) if dashed else '-', zorder=3))
    note(ax, x, y - 2.6, title, size=13, weight='bold', ha='center', color=col, zorder=4)
    note(ax, x, y - 6, body, size=9.6, ha='center', va='top', color=INK, linespacing=1.2, zorder=4)
def link(x0, y0, x1, y1, col=INK):
    ym = (y0 + y1) / 2
    ax.plot([x0, x0, x1, x1], [y0, ym, ym, y1], color=col, lw=2, zorder=1)

# club level
role(52, 82, 40, 14, 'Electrium team leads', 'two of them. they set our\nterm goals', PENCIL)
role(108, 82, 36, 14, 'Electrium safety captain', 'inspects our bay in the first\nweek of each month', RED, dashed=True)

# project lead
role(52, 61, 44, 17, 'Bakfiets project lead', 'turns term goals into issues, runs the\nWednesday meeting, makes calls that affect\nmore than one subteam, orders parts,\nlets members into the bay', INK)
link(52, 68, 52, 61)

# subteam leads
subs = [(25, 'mechanical lead', 'can approve any pull request', GREEN),
        (75, 'electrical lead', 'must be there for any\nbattery work', GOLD),
        (125, 'firmware lead', 'can approve any pull request', BLUE)]
for x, t, b, c in subs:
    link(52, 44, x, 38, c)
    role(x, 38, 40, 16, t, 'runs the subteam channel and\nkeeps its issues up to date.\n' + b, c)
    link(x, 22, x, 17, c)
    ax.add_patch(FancyBboxPatch((x - 18, 5), 36, 12, boxstyle='round,pad=0,rounding_size=1.2', fc=PAPER, ec=c, lw=1.4, zorder=3))
    note(ax, x, 14.4, 'members', size=12, weight='bold', ha='center', color=c, zorder=4)
    note(ax, x, 11.4, 'claim an issue with a comment,\npost a weekly update on it,\nask in the channel', size=9.2, ha='center', va='top', color=PENCIL, linespacing=1.15, zorder=4)
note(ax, 100, 46.5, 'also called squad leads. any squad lead,\nor the project lead, approves pull requests', size=10, color=RED, linespacing=1.15)

# rhythm
note(ax, 100, 63, 'every week', size=12, weight='bold')
note(ax, 100, 59.9, 'whole team: Wednesdays 6:30 to 7:30pm,\nthe Electrium bay\nsubteam leads: a short check-in with\nthe project lead about blockers',
     size=9.6, va='top', color=INK, linespacing=1.2)
mono(ax, 149, -1.5, 'roles from ONBOARDING.md, "Who Leads What"', size=7, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'team-structure.png'))
