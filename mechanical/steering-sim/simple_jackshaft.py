"""The simplest jackshaft that works.

Rules that keep it easy to build:
- the shaft is parallel to the frame's front upright tube, so two identical clamps hold it
- both shaft arms are flat bars pointing straight sideways
- the existing handlebar arm and fork arm are kept as they are

Only five numbers are free: how far the shaft sits from the tube (sideways and
forward), the two arm heights, and the two arm lengths.
"""
import math
import numpy as np
from scipy.optimize import differential_evolution
import jackshaft as J
from current_design import CURRENT

TUBE_LEAN = math.degrees(math.atan2(0.365, 0.931))   # 21.4 deg forward of vertical
TUBE_X0 = 515.0                                       # tube centre x at z = 0

# Spacers on the ball joint bolts move the two existing joints along their axes:
# the handlebar joint down, so the lower rod passes under the box bracket at x 340,
# and the fork joint up, so the upper rod clears the fork crown.
BAR_SPACER = 0.0        # new rod end sits on top of the handlebar arm, where the old ball joint was
try:
    FORK_SPACER = float(np.load("fork_spacer.npy")[0])   # 50 mm: gives the upper rod room past the fork crown
except OSError:
    FORK_SPACER = 20.0
J.BAR_JOINT = CURRENT.bar_joint0 + BAR_SPACER * J.BAR_DIR      # BAR_DIR points down
FORK_JOINT = CURRENT.fork_joint0 - FORK_SPACER * J.FORK_DIR    # FORK_DIR points down


class SimpleDesign(J.Design):
    def fork_joint(self):
        return FORK_JOINT.copy()


def make(x):
    y_s, dx, z_lo, z_hi, r_lo, r_hi = x
    return SimpleDesign(lean_deg=TUBE_LEAN, x0=TUBE_X0 + dx, y_s=y_s, z_lo=z_lo, z_hi=z_hi,
                        r_lo=r_lo, r_hi=r_hi, b_lo=0.0, b_hi=0.0, r_f=0.0, b_f=0.0, z_f=0.0)


def cost(x):
    d = make(x)
    rows = J.simulate(d, step=2.0)
    if rows is None:
        return 1e4
    err = max(abs(f - b) for b, s, f, w in rows)
    push = max(w for b, s, f, w in rows if abs(b) <= J.STOP_DEG)
    return err + 0.5 * max(0, push - 25) + J.penalties(d)


BOUNDS = [(-110, -45), (-10, 30), (-130, 10), (200, 420), (50, 140), (40, 140)]

if __name__ == "__main__":
    start = None
    try:
        start = np.clip(np.load("simple.npy"), [b[0] for b in BOUNDS], [b[1] for b in BOUNDS])
    except OSError:
        pass
    best = differential_evolution(cost, BOUNDS, seed=1, maxiter=120, popsize=20, tol=1e-6, x0=start)
    d = make(best.x)
    print("cost", round(best.fun, 2))
    for name, v in zip(["y_s (sideways)", "dx (forward of tube)", "z_lo", "z_hi", "r_lo", "r_hi"], best.x):
        print(f"  {name:22s} {v:7.1f}")
    lower, upper = d.links()
    print("joints: lower", np.round(d.lower_joint(), 1), "upper", np.round(d.upper_joint(), 1))
    print(f"rods: lower {lower.rod_length:.1f} mm, upper {upper.rod_length:.1f} mm; penalties {J.penalties(d):.2f}")
    print(" bar  shaft  fork  error  worst push angle")
    for b, s, f, w in J.simulate(d, step=5.0, limit=45) or []:
        print(f"{b:4.0f} {s:6.1f} {f:6.1f} {f-b:5.1f} {w:6.1f}")
    np.save("design.npy", np.array([TUBE_LEAN, TUBE_X0 + best.x[1], best.x[0], best.x[2], best.x[3],
                                    best.x[4], best.x[5], 0, 0, 0, 0, 0]))
    np.save("simple.npy", best.x)
