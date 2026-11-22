"""Extra pictures for docs/steering: the current bent rod, the new parts on their own,
a top view and a numbered close-up. Output goes to views/doc_*.png."""
import numpy as np
import pyvista as pv
import render as R
import jackshaft_check as C
from current_design import SAVED_BAR, SAVED_FORK

pv.OFF_SCREEN = True
P = R.P


def label(p, points, texts, size=18):
    p.add_point_labels(np.array(points), texts, font_size=size, point_size=1, shape_opacity=0.9,
                       shape_color="white", text_color="black", always_visible=True)


def save(p, name, position, focal, up=(0, 0, 1)):
    p.camera_position = [position, focal, up]
    p.screenshot(f"views/doc_{name}.png")
    p.close()
    print("saved", name, flush=True)


def plotter(size=(1600, 1000)):
    p = pv.Plotter(off_screen=True, window_size=size)
    p.set_background("white")
    return p


# 1. The current steering as Annie saved it, with the bent rod in red and the
#    straight line between its two balls in yellow.
p = plotter()
for name, m in R.base.items():
    p.add_mesh(m, smooth_shading=True, **R.STYLE[name])
rod = P["f26bakfiets_steering_rod_Default<As_Machined>"]
p.add_mesh(R.mesh(rod, 0.5), color="#d62728", smooth_shading=True)
b1, b2 = np.array([61.8, -90.1, -37.3]), np.array([814.2, -55.0, 374.7])
p.add_mesh(pv.Line(b1, b2), color="#e6b800", line_width=6)
p.add_mesh(pv.Sphere(radius=9, center=b1), color="#ffd23f")
p.add_mesh(pv.Sphere(radius=9, center=b2), color="#ffd23f")
bend = np.array([575.0, -60.0, -5.0])
label(p, [(b1 + b2) / 2, bend, b1, b2],
      ["the rod can spin around this line", "the bend is 220 mm off the line", "handlebar end", "fork end"])
save(p, "current_rod", (500, -2600, 200), (430, -60, 170))

# 2. The new parts on their own, with sizes.
s, f = R.rows[0.0]
new, _ = C.parts_at(0, s, f, draw=True)
p = plotter()
for name, shape in new.items():
    p.add_mesh(R.mesh(shape, 0.5), smooth_shading=True, **R.STYLE.get(name, dict(color="#ffd23f")))
d = C.d
lo, hi = d.shaft_point(d.z_lo), d.shaft_point(d.z_hi)
label(p, [(C.J.BAR_JOINT + d.lower_joint()) / 2, (lo + hi) / 2, (d.upper_joint() + d.fork_joint()) / 2,
          d.lower_joint(), d.upper_joint(), C.J.BAR_JOINT, d.fork_joint()],
      ["lower rod, 480 mm", "turning shaft, about 520 mm", "upper rod, 103 mm", "bottom arm, 89 mm",
       "top arm, 74.5 mm", "to the handlebar arm", "to the fork arm"])
save(p, "new_parts", (700, -2200, 300), (420, -110, 170))

# 3. Top view of the whole bike, new parts in colour.
p = plotter((1200, 1500))
R.scene(p, 0.0, labels=False)
label(p, [(C.J.BAR_JOINT + d.lower_joint()) / 2, (lo + hi) / 2, d.fork_joint()],
      ["lower rod", "turning shaft", "upper rod and fork arm"])
save(p, "top", (420, -60, 2800), (420, -60, 100), up=(1, 0, 0))

# 4. Close-up with numbers that follow a turn from the handlebars to the wheel.
p = plotter()
R.scene(p, 0.0, labels=False)
label(p, [C.J.BAR_JOINT, (C.J.BAR_JOINT + d.lower_joint()) / 2, (lo + hi) / 2, d.upper_joint(), d.fork_joint()],
      ["1  handlebar arm", "2  lower rod", "3  turning shaft", "4  top arm and upper rod", "5  fork arm"], size=20)
save(p, "numbered", (1150, -1100, -150), (520, -100, 120))

# 5. More angles, all riding straight, with the new parts labelled.
lab_pts = [C.J.BAR_JOINT, (C.J.BAR_JOINT + d.lower_joint()) / 2, (lo + hi) / 2, d.upper_joint(), d.fork_joint()]
lab_txt = ["handlebar arm", "lower rod", "turning shaft", "top arm", "fork arm"]
views = {
    "front_right": ((1900, -1300, 900), (450, -60, 180)),
    "rear_right_high": ((-900, -1500, 1300), (420, -60, 150)),
    "front": ((2600, -150, 300), (500, -60, 200)),
    "underneath": ((450, -700, -1900), (420, -80, 0)),
    "top_joint": ((1000, -650, 650), (690, -100, 360)),
    "bottom_joint": ((700, -650, -350), (420, -110, -50)),
}
for name, (pos, focal) in views.items():
    p = plotter()
    R.scene(p, 0.0, labels=False)
    label(p, lab_pts, lab_txt)
    save(p, name, pos, focal)
