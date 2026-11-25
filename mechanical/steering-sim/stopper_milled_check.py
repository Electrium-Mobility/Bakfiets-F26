"""Checks the milled stopper with fine meshes: where the fork first touches a bumper,
and the smallest gap from every stopper part to every bike part from stop to stop.
Gaps are measured from the vertices of one mesh to the surface of the other, both
ways, so they read slightly high (by under the mesh tolerance, 0.2 mm)."""
import time
import numpy as np
import pyvista as pv
import render as R
import gif_current as G
import stopper_milled as M
from current_design import SAVED_FORK

t0 = time.time()
C = R.C
made, bump = M.parts(C.asm)
TOL = 0.2


def fine(shape):
    return R.mesh(shape, TOL).triangulate().clean()


made_m = {k: fine(v) for k, v in made.items()}
bump_m = [fine(b) for b in bump]
joint = max((c for c in C.asm.children if c.label == "f26bakfiets_ball_joint"), key=lambda c: c.center().X)
fork_m, joint_m = fine(C.fork0), fine(joint)
still = {"frame": fine(C.frame), "box": R.base["box"].triangulate(), "kickstand": R.base["kickstand"].triangulate()}
print(f"meshed in {time.time() - t0:.0f} s", flush=True)


def gap(a, b):
    """Smallest distance between two meshes, vertices to surface both ways, unsigned
    (several meshes here are not closed). Returns -1 if any triangles of the two cross."""
    d1 = np.abs(a.compute_implicit_distance(b)["implicit_distance"]).min()
    d2 = np.abs(b.compute_implicit_distance(a)["implicit_distance"]).min()
    g = float(min(d1, d2))
    if g < 3.0:
        # Overlap test: points of a inside b, by ray parity, for closed-enough b.
        sel = a.select_interior_points(b, check_surface=False)
        if np.asarray(sel["selected_points"] if "selected_points" in sel.point_data else sel["SelectedPoints"]).any():
            return -1.0
    return g


def turned(m, fork):
    return m.copy().rotate_vector(G.L.fork_dir, fork - SAVED_FORK, point=G.L.fork_point)


def rod_at(fork):
    bar = G.fork_to_bar(fork)
    return G.rod0.copy().transform(G.rod_transform(bar, fork), inplace=True).triangulate()


# Fixed parts against each other and the frame, box and kickstand.
for k, m in made_m.items():
    print(f"{k}: " + ", ".join(f"{n} {gap(m, s):.1f}" for n, s in still.items()), flush=True)
for i, b in enumerate(bump_m):
    print(f"bumper {i}: to its bar {min(gap(b, m) for k, m in made_m.items() if 'bar' in k):.2f}, "
          + ", ".join(f"{n} {gap(b, s):.1f}" for n, s in still.items()), flush=True)

# Stop angles: first fork angle where the fork or ball joint reaches a bumper.
def contact_gap(fork, bumps=None):
    """Unsigned gap between the fork or ball joint and the bumpers, measured both ways."""
    out = 1e9
    for mm in (fork_m, joint_m):
        t = turned(mm, fork)
        for b in bumps or bump_m:
            out = min(out, float(np.abs(t.compute_implicit_distance(b)["implicit_distance"]).min()),
                      float(np.abs(b.compute_implicit_distance(t)["implicit_distance"]).min()))
    return out


for sign, name in ((-1, "left"), (1, "right")):
    # Step the fork towards the bumper; contact is where the gap first drops under the mesh tolerance.
    a = 30.0
    while contact_gap(sign * a) > TOL and a < 45:
        a += 0.1
    print(f"stops turning {name} at fork {a:.1f} deg, handlebars {G.fork_to_bar(sign * a):+.1f}", flush=True)

# Moving parts against the stopper through the whole sweep.
worst = {}
for fork in np.arange(-M.STOP_DEG, M.STOP_DEG + 0.01, 2.5):
    moving = {"fork": turned(fork_m, fork), "ball joint": turned(joint_m, fork),
              "wheel": turned(R.base["wheel"].triangulate(), fork), "rod": rod_at(fork)}
    row = []
    for mn, mm in moving.items():
        for k, m in made_m.items():
            g = gap(mm, m)
            if g < 3:
                print(f"    {mn} to {k}: {g:.1f}", flush=True)
            if g < worst.get((mn, k), (1e9,))[0]:
                worst[(mn, k)] = (g, fork)
            row.append(g)
        for i, b in enumerate(bump_m):
            if mn in ("rod", "wheel"):
                g = gap(mm, b)
                if g < worst.get((mn, f"bumper {i}"), (1e9,))[0]:
                    worst[(mn, f"bumper {i}")] = (g, fork)
    print(f"  fork {fork:+5.1f}: closest {min(row):.1f}", flush=True)
print("closest gap per pair over the sweep:")
for (mn, k), (g, fork) in sorted(worst.items(), key=lambda kv: kv[1][0]):
    print(f"  {mn:10s} to {k:15s} {g:6.1f} mm at fork {fork:+.1f}")
print(f"DONE in {time.time() - t0:.0f} s")
