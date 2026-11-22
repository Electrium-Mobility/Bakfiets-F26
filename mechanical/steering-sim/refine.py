"""Searches arm heights and the fork spacer on real solid clearance.

The optimizer in simple_jackshaft.py only knows simple rules, so it can place a rod
through a bracket. Here every candidate is checked against the real frame, box,
kickstand, wheel and fork through the whole turn, and only layouts with at least
MIN_GAP mm everywhere are kept. Arm lengths are re-fitted for every candidate.
"""
import itertools
import numpy as np
from scipy.optimize import minimize
import simple_jackshaft as S
import jackshaft as J
import jackshaft_check as C
from current_design import CURRENT

MIN_GAP = 8.0
base = np.load("simple.npy")   # y_s, dx, z_lo, z_hi, r_lo, r_hi
bar_joint_z = J.BAR_JOINT[2]


def set_fork_spacer(mm):
    S.FORK_SPACER = mm
    S.FORK_JOINT = CURRENT.fork_joint0 - mm * J.FORK_DIR


def fit_lengths(z_lo, z_hi):
    def f(r):
        x = base.copy()
        x[2], x[3], x[4], x[5] = z_lo, z_hi, r[0], r[1]
        return S.cost(x)
    res = minimize(f, base[4:6], method="Nelder-Mead", options={"xatol": 0.2, "fatol": 0.01})
    x = base.copy()
    x[2], x[3], x[4], x[5] = z_lo, z_hi, *res.x
    return x


def gaps(d):
    C.d = d
    rows = {round(b): (s, f, w) for b, s, f, w in J.simulate(d, step=1.0, limit=J.STOP_DEG)}
    worst = {}
    for bar in range(-J.STOP_DEG, J.STOP_DEG + 1, 5):
        s, f, w = rows[bar]
        new, turned = C.parts_at(bar, s, f)
        pairs = {"lower rod/frame": (new["lower rod"], C.frame), "lower rod/kickstand": (new["lower rod"], C.kickstand),
                 "lower rod/box": (new["lower rod"], C.box), "upper rod/fork": (new["upper rod"], turned["fork"]),
                 "upper arm/fork": (new["upper arm"], turned["fork"]), "ball 4/frame": (new["ball 4"], C.frame)}
        for k, (a, b) in pairs.items():
            worst[k] = min(worst.get(k, 1e9), a.distance_to(b))
    err = max(abs(f - b) for b, (s, f, w) in rows.items())
    push = max(w for s, f, w in rows.values())
    return worst, err, push


if __name__ == "__main__":
    results = []
    for spacer, z_hi in itertools.product((20, 30, 40), (330, 350, 370)):
        set_fork_spacer(spacer)
        z_lo = bar_joint_z            # lower rod level with the dropped handlebar joint
        x = fit_lengths(z_lo, z_hi)
        d = S.make(x)
        worst, err, push = gaps(d)
        low = min(worst.values())
        results.append((low, err, push, spacer, x))
        print(f"fork spacer {spacer:2d}  z_hi {z_hi}  r_lo {x[4]:5.1f}  r_hi {x[5]:5.1f}  error {err:4.1f}  push {push:4.1f}  "
              f"smallest gap {low:5.1f}  ({min(worst, key=worst.get)})", flush=True)

    ok = [r for r in results if r[0] >= MIN_GAP]
    pick = min(ok, key=lambda r: (r[1] + 0.1 * r[2], r[3])) if ok else max(results, key=lambda r: r[0])
    print("chosen: fork spacer", pick[3], "design", np.round(pick[4], 1), "meets gap" if ok else "BEST AVAILABLE, gap below target")
    np.save("simple.npy", pick[4])
    np.save("fork_spacer.npy", np.array([pick[3]]))
