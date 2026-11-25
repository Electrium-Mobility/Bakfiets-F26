"""Finds a taut housing route: straight runs joined by bends of radius R, from the bar
stop to the fork stop, as short as possible while keeping clear of the bike.

Distances are measured to triangle meshes of the parts (pyvista find_closest_cell),
so they are close but not exact; cable_check.py does the exact check afterwards."""
import sys
import time
import numpy as np
import pyvista as pv
from scipy.optimize import minimize
import jackshaft_check as C
import cable as K
from render import mesh
from current_design import SAVED_BAR, SAVED_FORK

R = 60.0                     # bend radius of the housing
STATIC_GAP, MOVING_GAP = 12.0, 15.0
HOUSING_R = K.HOUSING_D / 2


def fillet_path(pts, r=R, step=3.0):
    """Points along a polyline whose corners are rounded to radius r. Returns the points
    and how far short the straight runs fall of what the bends need (0 when it fits)."""
    pts = [np.asarray(p, float) for p in pts]
    n = len(pts)
    tl = [0.0] * n                                   # tangent length taken by each corner's bend
    for i in range(1, n - 1):
        a, b = unit(pts[i - 1] - pts[i]), unit(pts[i + 1] - pts[i])
        theta = np.arccos(np.clip(np.dot(a, b), -1, 1))   # inside angle
        tl[i] = r / np.tan(theta / 2) if theta > 1e-6 else 0.0
    short = 0.0
    for i in range(n - 1):
        need = tl[i] + tl[i + 1]
        short += max(0.0, need - np.linalg.norm(pts[i + 1] - pts[i]))
    out = [pts[0]]
    for i in range(1, n):
        p0, p1 = out[-1], pts[i]
        d = unit(pts[i] - pts[i - 1])
        end = p1 - d * tl[i] if i < n - 1 else p1
        L = np.linalg.norm(end - p0)
        k = max(1, int(L / step))
        out += [p0 + (end - p0) * t for t in np.linspace(0, 1, k + 1)[1:]]
        if i < n - 1 and tl[i] > 0:
            d2 = unit(pts[i + 1] - pts[i])
            start2 = p1 + d2 * tl[i]
            # arc from end to start2 round the corner
            bis = unit(d2 - d)
            theta = np.arccos(np.clip(np.dot(-d, d2), -1, 1))
            centre = p1 + bis * (r / np.sin(theta / 2))
            u, v = end - centre, start2 - centre
            ang = np.arccos(np.clip(np.dot(unit(u), unit(v)), -1, 1))
            axis = unit(np.cross(u, v))
            m = max(2, int(r * ang / step))
            for t in np.linspace(0, 1, m + 1)[1:]:
                out.append(K.rotate(end, centre, axis, np.degrees(ang * t)))
    return np.array(out), short


def unit(v):
    return v / np.linalg.norm(v)


def to_mesh(shape, tol):
    return mesh(shape, tol).triangulate()


print("meshing", flush=True)
t0 = time.time()
labels = {c.label: c for c in C.asm.children}
static = {"frame": to_mesh(C.frame, 1.0), "box": to_mesh(C.box, 1.0), "kickstand": to_mesh(C.kickstand, 1.0),
}
parts0 = K.build_all(0, 0, mark=False)
near_end = {"bar bracket": "bar", "fork bracket": "fork", "bar disc": "bar", "fork disc": "fork"}
for n in near_end:
    static[n] = to_mesh(parts0[n], 0.3)
ANGLES = list(range(-35, 36, 5))
bar_axis, fork_axis = (K.BAR_POINT, K.BAR_DIR), (K.FORK_POINT, K.FORK_DIR)
wheel0, fork0, bars0 = to_mesh(C.wheel0, 1.0), to_mesh(C.fork0, 1.0), to_mesh(C.bars0, 1.0)
moving = []
for a in ANGLES:
    moving.append(("wheel", a, wheel0.copy().rotate_vector(K.FORK_DIR, a - SAVED_FORK, point=K.FORK_POINT)))
    moving.append(("fork", a, fork0.copy().rotate_vector(K.FORK_DIR, a - SAVED_FORK, point=K.FORK_POINT)))
    moving.append(("bars", a, bars0.copy().rotate_vector(K.BAR_DIR, a - SAVED_BAR, point=K.BAR_POINT)))
print(f"meshed in {time.time()-t0:.0f} s", flush=True)


def gaps(path, end_skip=35.0):
    """Smallest gap from the housing surface to every part. Stretches within end_skip of
    each end are not checked against the bracket and disc at that end."""
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    near_bar, near_fork = s < end_skip, s > s[-1] - end_skip
    out = {}
    for name, m in static.items():
        pts = path
        if near_end.get(name) == "bar":
            pts = path[~near_bar]
        elif near_end.get(name) == "fork":
            pts = path[~near_fork]
        _, cp = m.find_closest_cell(pts, return_closest_point=True)
        out[name] = (np.linalg.norm(pts - cp, axis=1).min() - HOUSING_R, None)
    for name, a, m in moving:
        _, cp = m.find_closest_cell(path, return_closest_point=True)
        g = np.linalg.norm(path - cp, axis=1).min() - HOUSING_R
        if name not in out or g < out[name][0]:
            out[name] = (g, a)
    return out


def corners(x, which):
    s = 1 if which == "left" else -1
    e = K.ends()[which]
    S0 = e["bar_stop"] + e["bar_dir"] * K.FERRULE_L
    F0 = e["fork_stop"] + e["fork_dir"] * K.FERRULE_L
    bx, by, bz, tx, ty, tz, l1 = x
    return [S0, S0 + e["bar_dir"] * 60, np.array([bx, s * by, bz]), np.array([tx, s * ty, tz]),
            F0 + e["fork_dir"] * l1, F0]


def cost(x, which, verbose=False):
    path, short = fillet_path(corners(x, which))
    L = np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1))
    g = gaps(path)
    pen = 0.0
    for name, (d, a) in g.items():
        need = MOVING_GAP if name in ("wheel", "fork", "bars") else STATIC_GAP
        pen += max(0.0, need - d) ** 2
    c = L + 50 * pen + 200 * short
    if verbose:
        print(f"length {L:.0f} mm, short {short:.1f}, gaps " + ", ".join(f"{k} {d:.1f}" + (f"@{a:+d}" if a is not None else "") for k, (d, a) in sorted(g.items(), key=lambda kv: kv[1][0])))
    return c


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "right"
    # start: bottom corner beside the main tube bend, top corner beside the head tube
    x0 = np.array([500.0, 45.0, -25.0, 655.0, 130.0, 470.0, 75.0])
    cost(x0, which, True)
    best = minimize(cost, x0, args=(which,), method="Nelder-Mead",
                    options={"maxiter": 600, "xatol": 0.5, "fatol": 0.5, "initial_simplex": None})
    print("result", np.round(best.x, 1), round(best.fun, 1), flush=True)
    cost(best.x, which, True)
    np.save(f"route_{which}.npy", best.x)
