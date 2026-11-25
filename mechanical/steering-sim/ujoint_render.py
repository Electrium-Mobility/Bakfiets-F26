"""Pictures and GIFs of the U-joint steering. The yokes turn with their shafts, so the
uneven turning of the joints shows. Run ujoint_check.py <case> first (it saves the
yoke twists and the handlebar-to-fork table).

Usage: ujoint_render.py <case> [stills] [gifs]"""
import sys
import numpy as np
import pyvista as pv
import render as R
import ujoint_layout as U
import ujoint_parts as J
from linkage import rotate, unit
from current_design import SAVED_BAR, SAVED_FORK

pv.OFF_SCREEN = True
CASE = sys.argv[1]
pts, kinds = J.layout(CASE)
axes, crosses, _ = J.chain(CASE)
saved = np.load(f"ujoint_{CASE}_phases.npz")
PHASES, START, TABLE = list(saved["phases"]), float(saved["start"]), saved["table"]
ref_in, ref_out = J.ref_pins(axes, PHASES, START)
SPIN = J.sweep_all(axes, PHASES, START, step=0.25)
GEAR = kinds[0] == "gearbox"

bike = {k: v for k, v in R.base.items() if k != "fork arm"}
# The handlebar arm under the post is cut off in this design: drop its triangles.
bars = bike["bars"].copy()
bars.rotate_vector(U.BAR_DIR, -SAVED_BAR, point=U.BAR_POINT, inplace=True)
cc = bars.cell_centers().points
bike["bars"] = bars.extract_cells(np.where(cc[:, 2] > -56.5)[0]).extract_surface()   # at straight ahead
if GEAR:
    bike["kickstand"] = R.mesh(J.kickstand_fixed(R.C.kickstand), 2.0)
SHAFT, YOKE_C, CROSS_C, BOX_C = "#d62728", "#1f77b4", "#ffd23f", "#555555"
env = J.envelopes(CASE)
STATIC = [(R.mesh(s, 0.3), BOX_C if n == "gearbox" else SHAFT)
          for n, s in env.items() if n.startswith("S") or "stub" in n or n == "gearbox"]


def oriented_box(centre, a, p, la, lp, lq):
    q = np.cross(a, p)
    b = pv.Box(bounds=(-la / 2, la / 2, -lp / 2, lp / 2, -lq / 2, lq / 2))
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = a, p, q, centre
    return b.transform(m, inplace=False)


def yoke(c, a, p):
    """Yoke at cross c on a shaft leaving along a, its pin along p: hub, two ears, pin."""
    return [pv.Cylinder(center=c + a * 31, direction=a, radius=17, height=20, resolution=32),
            oriented_box(c + a * 10 + p * 15, a, p, 34, 7, 22),
            oriented_box(c + a * 10 - p * 15, a, p, 34, 7, 22),
            pv.Cylinder(center=c, direction=p, radius=5, height=36, resolution=16)]


def fork_of(bar):
    return float(np.interp(bar, TABLE[:, 0], TABLE[:, 1]))


def scene(p, bar, show_bike=True):
    fork = fork_of(bar)
    if show_bike:
        for name, m in bike.items():
            m = m.copy()
            if name == "bars":
                m.rotate_vector(U.BAR_DIR, bar, point=U.BAR_POINT, inplace=True)
            if name in ("wheel", "fork"):
                m.rotate_vector(U.FORK_DIR, fork - SAVED_FORK, point=U.FORK_POINT, inplace=True)
            p.add_mesh(m, smooth_shading=True, **R.STYLE[name])
    else:
        # the handlebar post and the steerer as grey stubs, each with a pointer
        p.add_mesh(pv.Cylinder(center=U.post_point(0), direction=U.BAR_DIR, radius=17, height=120), color="#888888")
        p.add_mesh(pv.Cylinder(center=U.fork_up(75), direction=U.FORK_DIR, radius=22, height=60), color="#888888")
        for base, axis, ang in ((U.post_point(45), U.BAR_DIR, bar), (U.fork_up(95), U.FORK_DIR, fork)):
            fwd = np.array([1.0, 0, 0])
            fwd = unit(fwd - axis * np.dot(fwd, axis))
            tip = rotate(base + fwd * 100, base, axis, ang)
            p.add_mesh(pv.Arrow(start=base, direction=tip - base, scale=100, tip_length=0.3,
                                tip_radius=0.12, shaft_radius=0.05), color="#222222")
    for m, col in STATIC:
        p.add_mesh(m, smooth_shading=True, color=col)
    ang = SPIN[round(round(bar * 4) / 4, 2)]
    for k, c in enumerate(crosses):
        a_in, a_out = axes[k], axes[k + 1]
        p_in = rotate(ref_out[k], np.zeros(3), a_in, ang[k])
        p_out = rotate(ref_in[k + 1], np.zeros(3), a_out, ang[k + 1])
        for m in yoke(c, -a_in, p_in) + yoke(c, a_out, p_out):
            p.add_mesh(m, smooth_shading=True, color=YOKE_C)
        p.add_mesh(pv.Sphere(radius=7, center=c), color=CROSS_C)

    def side(a):
        return "straight" if abs(a) < 0.05 else f"{abs(a):.1f} deg {'right' if a > 0 else 'left'}"
    p.add_text(f"handlebars {side(bar)}\nwheel {side(fork)}", position="upper_left", font_size=13, color="black")


CAMS = {
    "whole_front_right": [(1500, -1500, 1000), (340, 0, 220), (0, 0, 1)],
    "whole_side": [(340, -2400, 250), (340, 0, 220), (0, 0, 1)],
    "under_right": [(450, -1300, -550), (340, 0, 100), (0, 0, 1)],
    "post_end": [(330, -420, -150), (40, 0, -100), (0, 0, 1)],
    "corner": [(950, -600, -120), (580, -60, 0), (0, 0, 1)],
    "head_end": [(1100, -700, 850), (640, -50, 520), (0, 0, 1)],
}
MECH_CAMS = {
    "mechanism": [(750, -2100, 650), (360, -80, 260), (0, 0, 1)],
    "mechanism_top_end": [(1150, -800, 950), (620, -90, 560), (0, 0, 1)],
}
GIFS = [("whole", CAMS["whole_front_right"], True), ("side", CAMS["whole_side"], True),
        ("post_end", CAMS["post_end"], True), ("head_end", CAMS["head_end"], True),
        ("mechanism", MECH_CAMS["mechanism"], False), ("mechanism_top_end", MECH_CAMS["mechanism_top_end"], False)]


def sweep(step):
    def run(a, b):
        n = max(2, int(round(abs(b - a) / step)) + 1)
        return list(np.linspace(a, b, n))
    return run(0, 35) + run(35, -35)[1:] + run(-35, 0)[1:]


if __name__ == "__main__":
    what = sys.argv[2:] or ["stills", "gifs"]
    tag = f"ujoint_{CASE}"
    if "stills" in what:
        for n, cam in {**CAMS, **MECH_CAMS}.items():
            p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
            p.set_background("white")
            scene(p, 0.0, show_bike=n not in MECH_CAMS)
            p.camera_position = cam
            p.screenshot(f"views/{tag}_{n}.png")
            p.close()
            print("saved", n, flush=True)
    if "gifs" in what:
        for n, cam, bike_on in GIFS:
            p = pv.Plotter(off_screen=True, window_size=(900, 600))
            p.open_gif(f"views/{tag}_{n}.gif", fps=12)
            for a in sweep(2.5):
                p.clear()
                p.set_background("white")
                scene(p, float(a), show_bike=bike_on)
                p.camera_position = cam
                p.write_frame()
            p.close()
            print("saved gif", n, flush=True)
