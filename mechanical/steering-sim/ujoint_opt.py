"""Searches for U-joint layouts: joint centres with the smallest bends (as a share of
each joint's rating) that keep clear of the bike. Distances come from point clouds of
the parts (ujoint_space.npz, built by ujoint_space.py), so they are estimates;
ujoint_check.py measures the chosen layout on the real solids.

Usage: ujoint_opt.py <case>   (cases in CASES below; results to ujoint_<case>.npy)"""
import os
import sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import differential_evolution, minimize
import ujoint_layout as U

STATIC_GAP, MOVING_GAP = 8.0, 10.0
ANGLES = range(-35, 36, 5)


def voxel(p, s):
    return np.unique(np.round(p / s), axis=0) * s


def box_keep(p, lo, hi):
    return p[np.all((p >= lo) & (p <= hi), axis=1)]


LO, HI = np.array([-150, -260, -330]), np.array([1000, 150, 750])
if not os.path.exists("ujoint_space_small.npz"):
    z = np.load("ujoint_space.npz")
    small = {k: voxel(box_keep(z[k], LO, HI), 2.0) for k in ("frame", "box", "kickstand")}
    small["moving0"] = voxel(box_keep(np.vstack([z["wheel0"], z["fork0"]]), LO, HI), 3.0)
    np.savez_compressed("ujoint_space_small.npz", **small)
z = np.load("ujoint_space_small.npz")
static = {k: cKDTree(z[k]) for k in ("frame", "box", "kickstand")}


def rot_cloud(p, point, axis, deg):
    k = axis / np.linalg.norm(axis)
    v = p - point
    t = np.radians(deg)
    return point + v * np.cos(t) + np.cross(k, v) * np.sin(t) + np.outer(v @ k, k) * (1 - np.cos(t))


moving = cKDTree(np.vstack([rot_cloud(z["moving0"], U.FORK_POINT, U.FORK_DIR, a) for a in ANGLES]))
bi = np.load("ujoint_box_inside.npz")
INSIDE, B0, BSTEP = bi["inside"], np.array([bi["x0"], bi["y0"], bi["z0"]]), float(bi["step"])


def in_box(P):
    idx = np.round((P - B0) / BSTEP).astype(int)
    ok = np.all((idx >= 0) & (idx < np.array(INSIDE.shape)), axis=1)
    out = np.zeros(len(P), bool)
    out[ok] = INSIDE[idx[ok, 0], idx[ok, 1], idx[ok, 2]]
    return out


REACH, LIMIT = U.REACH, U.LIMIT


def samples(pts, kinds, a_top):
    """Points along the joint bodies and shafts, with the radius at each point.
    a_top: where the post (or the coupling to the gearbox) starts, on the post axis."""
    P, R = [], []

    def seg(p, q, r):
        L = np.linalg.norm(q - p)
        for t in np.linspace(0, 1, max(2, int(L / 5))):
            P.append(p + (q - p) * t), R.append(r)
    f = U.flows_n(pts)
    # post coupling / UJ1 yoke up to the post end
    seg(a_top, pts[0], U.SHAFT_R if kinds[0] == "gearbox" else U.UJ_R)
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]
        ra, rb = REACH[kinds[i]], REACH[kinds[i + 1]]
        d = f[i + 1]
        seg(p, p + d * ra, U.UJ_R if kinds[i] != "gearbox" else 30.0)
        seg(p + d * ra, q - d * rb, U.SHAFT_R)
        seg(q - d * rb, q, U.UJ_R)
    seg(pts[-1], U.fork_up(U.STEERER_TOP), U.SHAFT_R)
    for c in pts:
        P.append(c), R.append(U.UJ_R if kinds[0] != "gearbox" or c is not pts[0] else 30.0)
    return np.array(P), np.array(R)


def gaps(pts, kinds, a_top, skip_kick_post=True):
    P, R = samples(pts, kinds, a_top)
    res = {}
    for k, t in static.items():
        g = t.query(P)[0] - R
        if k == "kickstand" and skip_kick_post:   # boxed in under the post: reported, not searched
            g = np.where(P[:, 0] < 60, 99, g)
        res[k] = g
    res["box"] = np.where(in_box(P), -50.0, res["box"])
    res["wheel/fork"] = moving.query(P)[0] - R
    return res


def bends(pts):
    f = U.flows_n(pts)
    return np.array([U.bend(f[i], f[i + 1]) for i in range(len(pts))])


CASES = {k: dict(v, skip_kick=True) for k, v in U.CASES.items()}
BOUNDS_B = [(300, 620), (-150, 20)]
BOUNDS_P = [(480, 760), (-200, 20), (-160, 700)]
unpack = U.unpack


def cost(x, case, report=False):
    kinds = case["kinds"]
    pts = unpack(x, case)
    b = bends(pts)
    lim = np.array([LIMIT[k] for k in kinds])
    share = b / lim
    if kinds[0] == "gearbox":
        share[0] = 0.0       # the box makes the right angle
    pen = 0.0
    for i in range(len(pts) - 1):
        need = REACH[kinds[i]] + REACH[kinds[i + 1]] + 10
        pen += max(0.0, need - np.linalg.norm(pts[i + 1] - pts[i])) ** 2
    a_top = U.post_point(U.POST_END_Z)
    g = gaps(pts, kinds, a_top, case["skip_kick"])
    for k, v in g.items():
        need = MOVING_GAP if k == "wheel/fork" else STATIC_GAP
        pen += np.sum(np.clip(need - v, 0, None) ** 2) / 10
    if report:
        return pts, b, {k: float(v.min()) for k, v in g.items()}
    return share.max() + 0.1 * share.mean() + pen / 100


if __name__ == "__main__":
    name = sys.argv[1]
    case = CASES[name]
    nmid = len(case["kinds"]) - 3          # free points after B, before the steerer joint
    bounds = BOUNDS_B + BOUNDS_P * nmid
    r = differential_evolution(cost, bounds, args=(case,), maxiter=100, popsize=12, tol=1e-7,
                               seed=1, polish=False, updating="deferred", workers=1)
    r2 = minimize(cost, r.x, args=(case,), method="Nelder-Mead", options=dict(maxiter=6000, xatol=0.1, fatol=1e-5))
    x = r2.x if r2.fun < r.fun else r.x
    pts, b, g = cost(x, case, report=True)
    np.save(f"ujoint_{name}.npy", x)
    print(name, "cost", round(min(r.fun, r2.fun), 4))
    for i, (p, k) in enumerate(zip(pts, case["kinds"])):
        print(f"  UJ{i + 1} {k:8s} at {np.round(p, 1)}  bend {b[i]:.1f} (limit {LIMIT[k]:.0f})")
    print("  smallest gaps (mm, point-cloud estimate):", {k: round(v, 1) for k, v in g.items()})
