"""Pictures and a video of the off-the-shelf jackshaft. Annie's welded stopper bracket
is left off, because the stops are on the turning shaft in this version."""
import sys
import numpy as np
import pyvista as pv
import render as R
import jackshaft as J
import jackshaft_check as C
import offshelf as O
from current_design import SAVED_BAR, SAVED_FORK

pv.OFF_SCREEN = True
d = C.d
rows = {round(b, 1): (s, f) for b, s, f, w in J.simulate(d, step=0.5, limit=J.STOP_DEG)}
bike = {k: v for k, v in R.base.items() if k != "fork arm"}


def scene(p, bar, labels=None):
    s, f = rows[round(bar, 1)]
    for name, m in bike.items():
        m = m.copy()
        if name == "bars":
            m.rotate_vector(R.BAR_DIR, bar - SAVED_BAR, point=R.BAR_POINT, inplace=True)
        if name in ("wheel", "fork"):
            m.rotate_vector(R.FORK_DIR, f - SAVED_FORK, point=R.FORK_POINT, inplace=True)
        p.add_mesh(m, smooth_shading=True, **R.STYLE[name])
    parts = O.build(d, bar, s, f)
    for name, shape in parts.items():
        p.add_mesh(R.mesh(shape, 0.5), smooth_shading=True, color=O.colour(name))
    if labels:
        pts, txt = zip(*labels)
        p.add_point_labels(np.array(pts), list(txt), font_size=17, point_size=1, shape_opacity=0.9,
                           shape_color="white", text_color="black", always_visible=True)
    p.add_text(f"handlebars {bar:+.0f} deg   wheel {f:+.0f} deg", position="upper_left", font_size=13, color="black")
    return parts


def labels_now():
    t = d.shaft_dir
    return [
        ((J.BAR_JOINT + d.lower_joint()) / 2, "lower rod: M10 threaded rod + 2 rod ends"),
        (d.shaft_point(150), "12 mm steel shaft"),
        (d.shaft_point(52), "pillow block bearing on a plate, U-bolted to the frame"),
        (d.shaft_point(333), "pillow block bearing on a plate, U-bolted to the frame"),
        (d.lower_joint(), "bottom arm on a clamping hub"),
        (d.upper_joint(), "top arm on a clamping hub"),
        ((d.upper_joint() + d.fork_joint()) / 2, "upper rod: M10 threaded rod + 2 rod ends"),
        (d.shaft_point(88) + np.array([0, -60, 0]), "stop: collar with a bolt, 2 sleeved bolts in the plate"),
    ]


def still(name, bar, cam, size=(1600, 1000), labels=True):
    p = pv.Plotter(off_screen=True, window_size=size)
    p.set_background("white")
    scene(p, bar, labels_now() if labels else None)
    p.camera_position = cam
    p.screenshot(f"views/os_{name}.png")
    p.close()
    print("saved", name, flush=True)


CAMS = {
    "close_up": [(1150, -1100, -150), (520, -100, 120), (0, 0, 1)],
    "side": [(500, -2600, 300), (430, -60, 150), (0, 0, 1)],
    "front_right": [(1900, -1300, 900), (450, -60, 180), (0, 0, 1)],
    "rear_right_high": [(-900, -1500, 1300), (420, -60, 150), (0, 0, 1)],
    "underneath": [(450, -700, -1900), (420, -80, 0), (0, 0, 1)],
    "top_joint": [(1000, -650, 650), (650, -100, 340), (0, 0, 1)],
    "bottom_joint": [(800, -600, -300), (480, -110, -10), (0, 0, 1)],
    "lower_bearing": [(850, -650, 0), (540, -60, 110), (0, 0, 1)],
    "handlebar_joint": [(260, -420, -170), (20, -100, -62), (0, 0, 1)],
    "fork_joint": [(980, -380, 520), (760, -80, 380), (0, 0, 1)],
    "stop": [(800, -650, 150), (540, -60, 70), (0, 0, 1)],
    "upper_bearing": [(1000, -650, 600), (680, -60, 400), (0, 0, 1)],
}

if __name__ == "__main__":
    which = sys.argv[1:] or list(CAMS)
    for n in which:
        if n in CAMS:
            still(n, 0.0, CAMS[n], labels=n not in ("stop",))
    if "turns" in which or not sys.argv[1:]:
        still("full_left", -J.STOP_DEG, CAMS["stop"], labels=False)
        still("full_right", J.STOP_DEG, CAMS["stop"], labels=False)
    if "video" in which or not sys.argv[1:]:
        angles = list(np.arange(0, J.STOP_DEG + 0.01, 1.0)) + list(np.arange(J.STOP_DEG, -J.STOP_DEG - 0.01, -1.0)) + list(np.arange(-J.STOP_DEG, 0.01, 1.0))
        for vname, cam in (("close-up", CAMS["close_up"]), ("stop", CAMS["stop"])):
            p = pv.Plotter(off_screen=True, window_size=(1280, 800))
            p.open_movie(f"videos/offshelf-{vname}.mp4", framerate=30, quality=7)
            for a in angles:
                p.clear()
                p.set_background("white")
                scene(p, float(a))
                p.camera_position = cam
                p.write_frame()
            p.close()
            print("saved video", vname, flush=True)
    # GIFs for the docs page: the whole steering, then one for every mechanism.
    # Smaller and coarser than the videos so the page loads quickly.
    GIFS = {
        "steering": CAMS["close_up"],
        "gif_handlebar_end": CAMS["handlebar_joint"],
        "gif_bottom_arm": [(300, -520, 60), (470, -120, -35), (0, 0, 1)],
        "gif_top_arm": [(560, -520, 520), (650, -120, 365), (0, 0, 1)],
        "gif_fork_end": CAMS["fork_joint"],
        "gif_stop": [(700, -380, 160), (545, -60, 75), (0, 0, 1)],
        # whole-bike views
        "gif_side": CAMS["side"],
        "gif_top": [(430, -60, 2600), (430, -60, 150), (1, 0, 0)],
        "gif_front_right": CAMS["front_right"],
        "gif_rear_right_high": CAMS["rear_right_high"],
        "gif_underneath": CAMS["underneath"],
    }
    wanted = [g for g in GIFS if g in which or (g == "steering" and "gif" in which) or "gifs" in which or not sys.argv[1:]]
    if "whole_gifs" in which:
        wanted = ["gif_side", "gif_top", "gif_front_right", "gif_rear_right_high", "gif_underneath"]
    angles = list(np.arange(0, J.STOP_DEG + 0.01, 2.5)) + list(np.arange(J.STOP_DEG, -J.STOP_DEG - 0.01, -2.5)) + list(np.arange(-J.STOP_DEG, 0.01, 2.5))
    for g in wanted:
        p = pv.Plotter(off_screen=True, window_size=(900, 600))
        p.open_gif(f"views/os_{g}.gif", fps=12)
        for a in angles:
            p.clear()
            p.set_background("white")
            scene(p, float(a))
            p.camera_position = GIFS[g]
            p.write_frame()
        p.close()
        print("saved", g, flush=True)
