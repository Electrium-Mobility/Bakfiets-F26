"""GIFs of the cable steering turning from straight ahead to 35 deg each way and back.
New parts are meshed once; the discs and spacers are turned as meshes per frame."""
import sys
import numpy as np
import pyvista as pv
import render_cable as RC
import cable as K
from current_design import SAVED_BAR, SAVED_FORK

parts0 = K.build_all(0, 0)
meshes = {}
for name, shape in parts0.items():
    if "housing" in name:
        path = K.housing_path(name.split()[0])
        pts = np.array([[q.X, q.Y, q.Z] for q in (path.position_at(i / 400) for i in range(401))])
        meshes[name] = pv.lines_from_points(pts).tube(radius=K.HOUSING_D / 2, n_sides=24)
    else:
        meshes[name] = RC.R.mesh(shape, 0.3)
# A dark stripe on top of each disc (pictures only) so the turning shows.
def stripe(centre, up, thick):
    fwd = K.in_plane(K.X, up)
    c = centre + up * (thick / 2 + 0.3) + fwd * 38
    return pv.Cube(center=c, x_length=40, y_length=6, z_length=0.6).rotate_vector(
        np.cross([1, 0, 0], fwd) if np.linalg.norm(np.cross([1, 0, 0], fwd)) > 1e-6 else [0, 0, 1],
        np.degrees(np.arccos(np.clip(np.dot([1, 0, 0], fwd), -1, 1))), point=c)
meshes["bar stripe"] = stripe(K.BAR_DISC, -K.BAR_DIR, K.BAR_DISC_T)
meshes["fork stripe"] = stripe(K.FORK_DISC, -K.FORK_DIR, K.DISC_T)
TURNS_WITH_BARS = ("bar disc", "bar spacers", "bar stripe")


def frame(p, a):
    for name, m in RC.bike.items():
        m = m.copy()
        if name == "bars":
            m.rotate_vector(K.BAR_DIR, a - SAVED_BAR, point=K.BAR_POINT, inplace=True)
        if name in ("wheel", "fork"):
            m.rotate_vector(K.FORK_DIR, a - SAVED_FORK, point=K.FORK_POINT, inplace=True)
        p.add_mesh(m, smooth_shading=True, **RC.STYLE[name])
    for name, m in meshes.items():
        m = m.copy()
        if name in TURNS_WITH_BARS:
            m.rotate_vector(K.BAR_DIR, a, point=K.BAR_POINT, inplace=True)
        if name in ("fork disc", "fork stripe"):
            m.rotate_vector(K.FORK_DIR, a, point=K.FORK_POINT, inplace=True)
        p.add_mesh(m, smooth_shading=True, color="#222222" if "stripe" in name else RC.colour(name))
    side = "right" if a > 0 else "left" if a < 0 else "straight"
    p.add_text(f"handlebars and wheel {abs(a):.0f} deg {side}", position="upper_left", font_size=13, color="black")


GIFS = {"whole": RC.CAMS["whole_rear_left"], "bar_end": RC.CAMS["bar_end"],
        "fork_end": [(1250, -700, 1000), (720, 0, 380), (0, 0, 1)],
        "side": RC.CAMS["whole_side"], "front_right": RC.CAMS["whole_front_right"],
        "top": [(340, 0, 2600), (340, 0, 220), (1, 0, 0)]}
angles = list(np.arange(0, 35.01, 2.5)) + list(np.arange(35, -35.01, -2.5)) + list(np.arange(-35, 0.01, 2.5))
if sys.argv[1:2] == ["video"]:
    # Videos: 1 deg steps at 30 frames a second, larger than the GIFs.
    steps = list(np.arange(0, 35.01, 1.0)) + list(np.arange(35, -35.01, -1.0)) + list(np.arange(-35, 0.01, 1.0))
    for g in sys.argv[2:] or list(GIFS):
        p = pv.Plotter(off_screen=True, window_size=(1280, 800))
        p.open_movie(f"videos/cable-{g.replace('_', '-')}.mp4", framerate=30, quality=7)
        for a in steps:
            p.clear()
            p.set_background("white")
            frame(p, float(a))
            p.camera_position = GIFS[g]
            p.write_frame()
        p.close()
        print("saved video", g, flush=True)
    sys.exit()
for g in sys.argv[1:] or list(GIFS):
    p = pv.Plotter(off_screen=True, window_size=(900, 600))
    p.open_gif(f"views/cable_{g}.gif", fps=12)
    for a in angles:
        p.clear()
        p.set_background("white")
        frame(p, float(a))
        p.camera_position = GIFS[g]
        p.write_frame()
    p.close()
    print("saved", g, flush=True)
