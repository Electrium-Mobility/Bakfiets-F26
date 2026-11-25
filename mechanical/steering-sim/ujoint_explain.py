"""Explainer GIFs for the U-joint steering (fixed3): every shaft carries a white stripe that
turns with it, and the gearbox is see-through with its two bevel gears drawn, so the
spin can be followed from the handlebar post to the fork.

Output: views/ujoint_explain_whole.gif, views/ujoint_explain_gearbox.gif
"""
import sys
sys.argv = [sys.argv[0], "fixed3"]
import numpy as np
import pyvista as pv
import ujoint_render as UR
import ujoint_layout as U
from linkage import rotate, unit

pv.OFF_SCREEN = True
axes, crosses = UR.axes, UR.crosses
ref_out = UR.ref_out
GC = np.array(tuple(UR.env["gearbox"].bounding_box().center()))
UP = -unit(U.BAR_DIR)                    # up the handlebar post
SHAFT_R = 10.0
STRIPE = "#ffffff"
STATIC = [(m, c) for (m, c), n in zip(UR.STATIC, [n for n in UR.env if n.startswith("S") or "stub" in n or n == "gearbox"])
          if n != "gearbox"]
GEARBOX = UR.R.mesh(UR.env["gearbox"], 0.5)
UR.STATIC[:] = STATIC                  # draw the gearbox see-through, not solid


def ends(k):
    """Ends of shaft k: shaft 0 runs from the gearbox to the first joint; the last one
    from the last joint into the steerer."""
    a = GC if k == 0 else crosses[k - 1]
    b = crosses[k] if k < len(crosses) else crosses[-1] + axes[k] * 60
    return np.asarray(a, float), np.asarray(b, float)


def stripes(k, ang):
    """Four stripes round shaft k, white and yellow by turns, so its spin shows from any side."""
    return [(stripe(k, ang + q * 90), "#ffffff" if q % 2 == 0 else "#ffd23f") for q in range(4)]


def stripe(k, ang):
    a, b = ends(k)
    ax = axes[k]
    trim = 30 if k else 38
    if np.linalg.norm(b - a) < 2 * trim + 6:
        trim = 3                                     # short centre pieces of double joints
    p0, p1 = a + ax * trim, b - ax * 25
    d = rotate(ref_out[k], np.zeros(3), ax, ang)
    w = np.cross(ax, d)
    c = (p0 + p1) / 2 + d * (SHAFT_R + 0.5)
    box = pv.Box(bounds=(-np.linalg.norm(p1 - p0) / 2, np.linalg.norm(p1 - p0) / 2, -1.5, 1.5, -3.5, 3.5))
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = ax, d, w, c
    return box.transform(m, inplace=False)


def bevel(axis, ang, tick_ref):
    """Bevel gear as a cone whose point faces the gearbox centre, with a white tick on it."""
    centre = GC + axis * 16
    cone = pv.Cone(center=centre, direction=-axis, height=14, radius=17, resolution=40)
    d = rotate(tick_ref, np.zeros(3), axis, ang)
    tick = pv.Line(centre + axis * 7 + d * 4, centre + axis * 7 + d * 17).tube(radius=2.2)
    return cone, tick


def scene(p, bar, labels):
    UR.scene(p, bar, show_bike=False)                # stubs, arrows, yokes, crosses, static shafts
    ang = UR.SPIN[round(round(bar * 4) / 4, 2)]
    for k in range(len(axes)):
        for m, col in stripes(k, ang[k]):
            p.add_mesh(m, color=col)
    p.add_mesh(GEARBOX, color="#555555", opacity=0.18)
    tick_in = unit(np.cross(UP, axes[0]))
    for axis, a, ref in ((UP, bar, tick_in), (axes[0], ang[0], UP)):
        cone, tick = bevel(axis, a, ref)
        p.add_mesh(cone, color="#e0a526", smooth_shading=True)
        p.add_mesh(tick, color=STRIPE)
    if labels:
        pts, txt = zip(*labels)
        p.add_point_labels(np.array(pts), list(txt), font_size=15, point_size=1, shape_opacity=0.85,
                           shape_color="white", text_color="black", always_visible=True)


LABELS_WHOLE = [
    (U.post_point(60), "1  handlebars turn the post"),
    (GC + np.array([-40, 0, -70]), "2  gears turn the spin 90°"),
    (crosses[0] + np.array([0, 0, -60]), "3  U-joints carry the spin round bends"),
    ((crosses[1] + crosses[2]) / 2 + np.array([50, 0, 0]), "4  shafts spin"),
    (U.fork_up(80) + np.array([60, 0, 0]), "5  fork turns"),
]
LABELS_GEAR = [
    (U.post_point(60), "handlebar post"),
    (GC + UP * 30 + np.array([-40, 0, 0]), "gear on the post"),
    (GC + axes[0] * 30 + np.array([0, 0, -40]), "gear on the shaft"),
]
VIEWS = {
    "whole": ([(750, -2100, 650), (360, -80, 260), (0, 0, 1)], LABELS_WHOLE),
    "gearbox": ([(260, -420, 40), (60, -20, -100), (0, 0, 1)], LABELS_GEAR),
}

if __name__ == "__main__":
    for name in sys.argv[2:] or list(VIEWS):
        cam, labels = VIEWS[name]
        p = pv.Plotter(off_screen=True, window_size=(900, 600))
        p.open_gif(f"views/ujoint_explain_{name}.gif", fps=12)
        frames = UR.sweep(1.0)                        # 1 deg steps: about 12 s for the full sweep
        for a in frames:
            p.clear()
            p.set_background("white")
            scene(p, float(a), labels)
            p.camera_position = cam
            p.write_frame()
        p.close()
        print("saved", name, len(frames), "frames", flush=True)
