"""Pictures of the cable steering on the bike. The old welded stopper bracket and its
bumpers at the head tube are left out, since the bike has neither."""
import sys
import numpy as np
import pyvista as pv
import render as R
import cable as K
from current_design import SAVED_BAR, SAVED_FORK

pv.OFF_SCREEN = True
P = R.P
bike = {k: v for k, v in R.base.items() if k != "fork arm"}
STYLE = dict(R.STYLE)
STYLE["stopper bracket"] = dict(color="#7a7a7a")
STYLE["bumpers"] = dict(color="#333333")


def colour(name):
    if "disc" in name:
        return "#ff9f1c"
    if "housing" in name:
        return "#1f77b4"
    if "cable" in name:
        return "#111111"
    if "bracket" in name:
        return "#d62728"
    if "stop" in name:
        return "#c0c0c0"
    return "#8c8c8c"


def scene(p, a):
    for name, m in bike.items():
        m = m.copy()
        if name == "bars":
            m.rotate_vector(K.BAR_DIR, a - SAVED_BAR, point=K.BAR_POINT, inplace=True)
        if name in ("wheel", "fork"):
            m.rotate_vector(K.FORK_DIR, a - SAVED_FORK, point=K.FORK_POINT, inplace=True)
        p.add_mesh(m, smooth_shading=True, **STYLE[name])
    for name, shape in K.build_all(a, a).items():
        if "housing" in name:
            # Drawn as a tube along the same path: the swept solid meshes with small
            # bulges at its face seams, which are not in the housing itself.
            path = K.housing_path(name.split()[0])
            pts = np.array([[q.X, q.Y, q.Z] for q in (path.position_at(i / 400) for i in range(401))])
            p.add_mesh(pv.lines_from_points(pts).tube(radius=K.HOUSING_D / 2, n_sides=24), smooth_shading=True, color=colour(name))
            continue
        p.add_mesh(R.mesh(shape, 0.3), smooth_shading=True, color=colour(name))
    p.add_text(f"handlebars and wheel {a:+.0f} deg", position="upper_left", font_size=13, color="black")


CAMS = {
    "whole_front_right": [(1500, -1500, 1000), (340, 0, 220), (0, 0, 1)],
    "whole_rear_left": [(-900, 1300, 900), (340, 0, 220), (0, 0, 1)],
    "whole_side": [(340, -2400, 250), (340, 0, 220), (0, 0, 1)],
    "bar_end": [(380, -380, 80), (20, 0, -60), (0, 0, 1)],
    "fork_end": [(1000, -420, 760), (670, 0, 520), (0, 0, 1)],
}

if __name__ == "__main__":
    for n in sys.argv[1:] or list(CAMS):
        p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
        p.set_background("white")
        scene(p, 0.0)
        p.camera_position = CAMS[n]
        p.screenshot(f"views/cable_{n}.png")
        p.close()
        print("saved", n, flush=True)
