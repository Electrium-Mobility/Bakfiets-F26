"""Shaded, labelled pictures of the jackshaft steering, and an animation of it turning.

The cargo box and wheel are drawn see-through so the rods behind them show.
Output goes to views/: shaded_*.png and steering.gif.
"""
import numpy as np
import pyvista as pv
from build123d import Axis
import jackshaft_check as C
from jackshaft import simulate, STOP_DEG, BAR_POINT, BAR_DIR, FORK_POINT, FORK_DIR
from current_design import SAVED_BAR, SAVED_FORK

pv.OFF_SCREEN = True
TOL = 1.0

def mesh(shape, tol=TOL):
    """Triangulates face by face, skipping the odd face OpenCascade can't mesh."""
    pts, faces, skipped = [], [], 0
    for face in shape.faces():
        try:
            verts, tris = face.tessellate(tol, 0.3)
        except AttributeError:
            skipped += 1
            continue
        offset = len(pts)
        pts.extend([v.X, v.Y, v.Z] for v in verts)
        faces.extend([3, a + offset, b + offset, c + offset] for a, b, c in tris)
    if skipped:
        print(f"  skipped {skipped} face(s) that would not mesh", flush=True)
    return pv.PolyData(np.array(pts), np.hstack(faces))

P = {c.label: c for c in C.asm.children}
base = {   # meshes in the saved (turned) position, rotated per frame below
    "frame": mesh(C.frame, 2.0), "box": mesh(C.box, 2.0), "kickstand": mesh(C.kickstand, 2.0),
    "bars": mesh(C.bars0, 1.5), "wheel": mesh(C.wheel0, 3.0), "fork": mesh(C.fork0, 1.5),
    "fork arm": mesh(P["Part1^f26bakfiets_main_asm"], 1.0),
}
STYLE = {
    "frame": dict(color="#7a7a7a"), "kickstand": dict(color="#9a9a9a"),
    "box": dict(color="#d8cfb8", opacity=0.18), "bars": dict(color="#555555"),
    "wheel": dict(color="#444444", opacity=0.25), "fork": dict(color="#666666"),
    "fork arm": dict(color="#2a6fb0"),
    "lower rod": dict(color="#d62728"), "upper rod": dict(color="#d62728"),
    "shaft": dict(color="#1f77b4"), "lower collar": dict(color="#1f77b4"), "upper collar": dict(color="#1f77b4"),
    "bar spacer": dict(color="#8c8c8c"), "fork spacer": dict(color="#8c8c8c"), "lower arm": dict(color="#ff9f1c"), "upper arm": dict(color="#ff9f1c"),
}
rows = {round(b, 1): (s, f) for b, s, f, w in simulate(C.d, step=0.5, limit=STOP_DEG)}


def scene(p, bar, labels=True):
    s, f = rows[round(bar, 1)]
    turn_bar, turn_fork = bar - SAVED_BAR, f - SAVED_FORK
    for name, m in base.items():
        m = m.copy()
        if name == "bars":
            m.rotate_vector(BAR_DIR, turn_bar, point=BAR_POINT, inplace=True)
        if name in ("wheel", "fork", "fork arm"):
            m.rotate_vector(FORK_DIR, turn_fork, point=FORK_POINT, inplace=True)
        p.add_mesh(m, smooth_shading=True, **STYLE[name])
    new, _ = C.parts_at(bar, s, f, draw=True)
    for name, shape in new.items():
        style = STYLE.get(name, dict(color="#ffd23f"))   # balls in yellow
        p.add_mesh(mesh(shape, 0.5), smooth_shading=True, **style)
    if labels:
        lo, hi = C.d.shaft_point(C.d.z_lo), C.d.shaft_point(C.d.z_hi)
        lower_mid = (C.J.BAR_JOINT + C.d.lower_joint()) / 2
        upper_mid = (C.d.upper_joint() + C.d.fork_joint()) / 2
        pts = np.array([lower_mid, (lo + hi) / 2, upper_mid, C.d.lower_joint(), C.d.upper_joint(),
                        C.J.BAR_JOINT, C.d.fork_joint()])
        text = ["lower rod (480 mm)", "jackshaft", "upper rod (103 mm)", "lower arm (89 mm)",
                "upper arm (74.5 mm)", "handlebar arm + 25 mm spacer", "fork arm + 40 mm spacer"]
        p.add_point_labels(pts, text, font_size=16, point_size=1, shape_opacity=0.85,
                           shape_color="white", text_color="black", always_visible=True)
    p.add_text(f"handlebars {bar:+.0f} deg   fork {f:+.1f} deg", position="upper_left", font_size=14, color="black")


def still(name, bar, position, focal, up=(0, 0, 1), size=(1600, 1100)):
    p = pv.Plotter(off_screen=True, window_size=size)
    p.set_background("white")
    scene(p, bar)
    p.camera_position = [position, focal, up]
    p.screenshot(f"views/shaded_{name}.png")
    p.close()
    print("saved", name, flush=True)


if __name__ == "__main__":
    still("right_side", 0, (500, -2600, 300), (430, -60, 150))
    still("close_up", 0, (1150, -1100, -150), (520, -100, 120))
    still("top", 0, (420, -90, 2600), (420, -90, 100), up=(1, 0, 0))
    still("full_right_turn", 35, (1150, -1100, -150), (520, -100, 120))
    still("full_left_turn", -35, (1150, -1100, -150), (520, -100, 120))

    # Animation: straight, full right, full left, back to straight.
    angles = list(np.arange(0, 35.01, 2.5)) + list(np.arange(35, -35.01, -2.5)) + list(np.arange(-35, 0.01, 2.5))
    p = pv.Plotter(off_screen=True, window_size=(1100, 760))
    p.open_gif("views/steering.gif", fps=12)
    for a in angles:
        p.clear()
        p.set_background("white")
        scene(p, float(a), labels=False)
        p.camera_position = [(1150, -1100, -150), (520, -100, 120), (0, 0, 1)]
        p.write_frame()
    p.close()
    print("saved steering.gif", flush=True)
