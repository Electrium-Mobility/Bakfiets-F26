"""Solids and kinematics for the U-joint steering cases in ujoint_layout.CASES
(joint centres found by ujoint_opt.py, saved in ujoint_<case>.npy).

Every joint is "single", "double" or "gearbox" (1:1 right-angle bevel box). Shaft
positions never move when steering; only the shafts spin. So the clash check uses
each joint's swept envelope (42 mm across), and the pictures turn the yokes."""
import math
import numpy as np
from scipy.optimize import minimize
from build123d import Cylinder, Box, Plane, Location, Vector
import ujoint_layout as U
from linkage import rotate, unit

GEARBOX = 60.0            # assumed cube size of the right-angle gearbox; check the bought part
KICK_SHIFT = 30.0         # fixed cases: kickstand front cross piece moved this far forward


def layout(case):
    c = U.CASES[case]
    x = np.load(f"ujoint_{case}.npy")
    return U.unpack(x, c), list(c["kinds"])


def bend_table(case):
    pts, kinds = layout(case)
    f = U.flows_n(pts)
    return [(f"UJ{i + 1}" if k != "gearbox" else "gearbox", k, U.bend(f[i], f[i + 1]), U.LIMIT[k])
            for i, k in enumerate(kinds)]


# ---------------------------------------------------------------- kinematics
def chain(case):
    """Axes (flow directions) and cross centres; a double joint becomes two crosses with a
    centre piece along the bisector. A gearbox drives S1 1:1, so the chain then starts at S1.
    free[i] is True for shafts whose yoke twist is a free choice (the real shafts)."""
    pts, kinds = layout(case)
    f = U.flows_n(pts)
    gear = kinds[0] == "gearbox"
    axes, crosses, free = ([f[1]] if gear else [f[0]]), [], [False]
    for i, k in enumerate(kinds):
        if i == 0 and gear:
            continue
        if k == "single":
            crosses.append(pts[i])
            axes.append(f[i + 1])
            free.append(True)
        else:
            crosses += [pts[i] - f[i] * U.DOUBLE_GAP / 2, pts[i] + f[i + 1] * U.DOUBLE_GAP / 2]
            axes += [unit(f[i] + f[i + 1]), f[i + 1]]
            free += [False, True]
    free[-1] = False
    return axes, crosses, free


def ref_pins(axes, phases, start_angle):
    """Pin direction of each shaft's input and output yoke at straight ahead."""
    n = len(axes)
    base = unit(np.cross(axes[0], axes[1]))
    start = rotate(base, np.zeros(3), axes[0], start_angle)
    ref_in, ref_out = [None], [start]
    for i in range(1, n):
        pin_in = unit(np.cross(axes[i], ref_out[-1]))
        ref_in.append(pin_in)
        ref_out.append(rotate(pin_in, np.zeros(3), axes[i], phases[i] if i < n - 1 else 0.0))
    return ref_in, ref_out


def sweep_all(axes, phases, start_angle, top=35.0, step=0.25):
    """Angle of every shaft for handlebar angles -top..top (walked out from 0 both ways so
    every pin keeps its sign). Returns {bar rounded to 0.01: [angles]}."""
    ref_in, ref_out = ref_pins(axes, phases, start_angle)
    n = len(axes)
    out = {0.0: [0.0] * n}
    for sgn in (1, -1):
        pins = list(ref_in)
        for t in np.arange(step, top + 1e-9, step) * sgn:
            angs = [float(t)]
            pin = rotate(ref_out[0], np.zeros(3), axes[0], t)
            for i in range(1, n):
                cand = unit(np.cross(axes[i], pin))
                if np.dot(cand, pins[i]) < 0:
                    cand = -cand
                pins[i] = cand
                a = math.degrees(math.atan2(np.dot(np.cross(ref_in[i], cand), axes[i]), np.dot(ref_in[i], cand)))
                angs.append(a)
                pin = rotate(ref_out[i], np.zeros(3), axes[i], a)
            out[round(float(t), 2)] = angs
    return out


def phase_plan(case, search=True):
    """Yoke twists that make the fork follow the handlebars most evenly from -35 to +35.
    Returns dict with phases (per axis), start angle, table rows [bar, fork], axes, crosses."""
    axes, crosses, free = chain(case)
    idx = [i for i, fr in enumerate(free) if fr]

    def build(v):
        ph = [0.0] * len(axes)
        for j, i in enumerate(idx):
            ph[i] = v[j + 1]
        return ph, v[0]

    def table(v, step=0.25):
        ph, st = build(v)
        s = sweep_all(axes, ph, st, step=step)
        return np.array(sorted((b, a[-1]) for b, a in s.items()))

    def err(v):
        t = table(v, 1.0)
        return np.max(np.abs(t[:, 1] - t[:, 0]))

    best = (err(np.zeros(len(idx) + 1)), np.zeros(len(idx) + 1))
    if search:
        rng = np.random.default_rng(0)
        for trial in range(30):
            v0 = rng.choice([0.0, 45.0, 90.0, 135.0], size=len(idx) + 1)
            r = minimize(err, v0, method="Nelder-Mead", options=dict(maxiter=500, xatol=0.05, fatol=1e-4))
            if r.fun < best[0]:
                best = (r.fun, r.x)
    ph, st = build(best[1])
    return dict(phases=ph, start=st, table=table(best[1]), axes=axes, crosses=crosses)


# ---------------------------------------------------------------- solids
def cyl(p, q, r):
    v = Vector(*(np.asarray(q, float) - np.asarray(p, float)))
    return Plane(origin=tuple(np.asarray(p, float)), z_dir=v.normalized()) * Cylinder(r, v.length, align=None)


def envelopes(case):
    """Swept volumes for the clash check: name -> solid. Shafts stop where joints start."""
    pts, kinds = layout(case)
    f = U.flows_n(pts)
    out = {}
    for i, k in enumerate(kinds):
        c = pts[i]
        if k == "gearbox":
            x = unit(f[1] - f[0] * np.dot(f[1], f[0]))
            pl = Plane(origin=tuple(c), x_dir=tuple(x), z_dir=tuple(-f[0]))
            out["gearbox"] = pl * Box(GEARBOX, GEARBOX, GEARBOX)
        elif k == "single":
            out[f"UJ{i + 1}"] = cyl(c - f[i] * U.YOKE, c, U.UJ_R) + cyl(c, c + f[i + 1] * U.YOKE, U.UJ_R)
        else:
            c1, c2 = c - f[i] * U.DOUBLE_GAP / 2, c + f[i + 1] * U.DOUBLE_GAP / 2
            out[f"UJ{i + 1}"] = (cyl(c1 - f[i] * U.YOKE, c1, U.UJ_R) + cyl(c1, c2, U.UJ_R)
                                 + cyl(c2, c2 + f[i + 1] * U.YOKE, U.UJ_R))
    reach = [GEARBOX / 2 if k == "gearbox" else U.REACH[k] for k in kinds]
    for i in range(len(pts) - 1):
        p, q = pts[i] + f[i + 1] * reach[i], pts[i + 1] - f[i + 1] * reach[i + 1]
        out[f"S{i + 1}"] = cyl(p, q, U.SHAFT_R)
    post_end = U.post_point(U.POST_END_Z)
    top = pts[0] - f[0] * reach[0]
    if np.linalg.norm(top - post_end) > 1:
        out["post stub"] = cyl(post_end, top, U.SHAFT_R)
    # the stub plugs 10 mm into the steerer (CAD steerer top is 101.6 mm up the axis)
    out["steerer stub"] = cyl(pts[-1] + f[-1] * reach[-1], U.fork_up(U.STEERER_TOP - 10), U.SHAFT_R)
    return out


def kickstand_fixed(kick):
    """Fixed cases: the kickstand's front cross piece (two bars and the hangers carrying
    them, x 5 to 40, below z -31) cut off and welded back KICK_SHIFT further forward."""
    cut = Box(35, 420, 80, align=None).moved(Location((5, -210, -111)))
    piece = kick & cut
    return (kick - cut) + piece.moved(Location((KICK_SHIFT, 0, 0)))
