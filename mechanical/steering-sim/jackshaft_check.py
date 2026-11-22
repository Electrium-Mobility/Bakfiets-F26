"""Builds the jackshaft parts as solids, turns everything through the steering range,
and measures clearances to the frame, cargo box, wheel and fork. Also saves drawings.

Run after jackshaft.py, which saves the chosen design to design.npy.
"""
import numpy as np
from build123d import (import_step, Cylinder, Sphere, Box, Plane, Vector, Location, Axis,
                       Compound, ExportSVG, LineType, Unit, export_step)
from linkage import rotate
from current_design import SAVED_BAR, SAVED_FORK
from simple_jackshaft import make   # first: it sets the spacer-shifted handlebar joint
from current_design import CURRENT
import jackshaft as J
from jackshaft import simulate, BAR_POINT, BAR_DIR, FORK_POINT, FORK_DIR, STOP_DEG

ROD_DIA, BALL_DIA, SHAFT_DIA, ARM_W, ARM_T = 17.0, 24.0, 20.0, 25.0, 8.0

d = make(np.load("simple.npy"))
asm = import_step("step/f26bakfiets_main_asm.step")
P = {c.label: c for c in asm.children}
frame = P["f26bakfiets_frame_Default<As_Machined>"]
box = P["f26bakfiets_cargo_box_low_detail"]
kickstand = P["f26bakfiets_kickstand_Default<As_Machined>"]
wheel0, fork0 = P["f26bakfiets_front_wheel"], P["f26bakfiets_front_suspension"]
bars0 = P["f26bakfiets_steering_handlebars"]
fork_axis = Axis(tuple(FORK_POINT), tuple(FORK_DIR))
bar_axis = Axis(tuple(BAR_POINT), tuple(BAR_DIR))


def rod(p1, p2, dia=ROD_DIA, trim=0.0):
    v = Vector(*(p2 - p1))
    plane = Plane(origin=tuple(p1), z_dir=v.normalized())
    return plane * Cylinder(dia / 2, v.length - 2 * trim, align=None).moved(Location((0, 0, trim)))


def arm(centre, joint, axis_dir):
    """A flat bar from the shaft centre to the ball joint, square to the shaft."""
    v = joint - centre
    length = np.linalg.norm(v)
    plane = Plane(origin=tuple(centre), x_dir=tuple(v / length), z_dir=tuple(axis_dir))
    return plane * Box(length + ARM_W / 2, ARM_W, ARM_T, align=None).moved(Location((-ARM_W / 4, -ARM_W / 2, -ARM_T / 2)))


def parts_at(bar, shaft, fork, draw=False):
    j1 = rotate(J.BAR_JOINT, BAR_POINT, BAR_DIR, bar)
    s0, t = d.shaft_point(0), d.shaft_dir
    j2 = rotate(d.lower_joint(), s0, t, shaft)
    j3 = rotate(d.upper_joint(), s0, t, shaft)
    j4 = rotate(d.fork_joint(), FORK_POINT, FORK_DIR, fork)
    lo_c, hi_c = d.shaft_point(d.z_lo), d.shaft_point(d.z_hi)
    shaft_solid = rod(lo_c - 25 * t, hi_c + 25 * t, SHAFT_DIA)
    # For the gap check the rods stop short of their balls, so a rod touching its own
    # ball joint isn't counted. For pictures (draw=True) they run into the balls.
    trim = 0.0 if draw else BALL_DIA / 2 + 4
    new = {
        "lower rod": rod(j1, j2, trim=trim),
        "upper rod": rod(j3, j4, trim=trim),
        "shaft": shaft_solid,
        "lower arm": arm(lo_c, j2, t),
        "upper arm": arm(hi_c, j3, t),
    }
    for name, j in (("ball 1", j1), ("ball 2", j2), ("ball 3", j3), ("ball 4", j4)):
        new[name] = Sphere(BALL_DIA / 2).moved(Location(tuple(j)))
    if draw:
        # Collars where the arms clamp to the shaft, and the spacers that hold the two
        # existing ball joints off their arms.
        new["lower collar"] = rod(lo_c - 12 * t, lo_c + 12 * t, 34)
        new["upper collar"] = rod(hi_c - 12 * t, hi_c + 12 * t, 34)
        bar_arm_end = rotate(CURRENT.bar_joint0, BAR_POINT, BAR_DIR, bar)
        fork_arm_end = rotate(CURRENT.fork_joint0, FORK_POINT, FORK_DIR, fork)
        new["bar spacer"] = rod(bar_arm_end, j1, 14)
        new["fork spacer"] = rod(fork_arm_end, j4, 14)
    turned = {"wheel": wheel0.rotate(fork_axis, fork - SAVED_FORK),
              "fork": fork0.rotate(fork_axis, fork - SAVED_FORK)}
    return new, turned


if __name__ == "__main__":
    rows = {round(b): (s, f) for b, s, f, w in simulate(d, step=1.0, limit=STOP_DEG)}
    fixed = {"frame": frame, "box": box, "kickstand": kickstand}
    checks = [("lower rod", ["frame", "box", "kickstand", "wheel"]),
              ("upper rod", ["frame", "box", "wheel", "fork"]),
              ("shaft", ["frame", "box", "wheel"]),
              ("lower arm", ["frame", "box", "wheel"]),
              ("upper arm", ["frame", "box", "wheel", "fork"]),
              ("ball 2", ["frame", "wheel"]), ("ball 3", ["frame", "wheel", "fork"])]
    worst = {}
    for bar in range(-STOP_DEG, STOP_DEG + 1, 5):
        s, f = rows[bar]
        new, turned = parts_at(bar, s, f)
        others = {**fixed, **turned}
        for part, against in checks:
            for o in against:
                gap = new[part].distance_to(others[o])
                key = f"{part} to {o}"
                if key not in worst or gap < worst[key][0]:
                    worst[key] = (gap, bar)
    print("smallest gaps from -%d to +%d deg (mm, at handlebar angle):" % (STOP_DEG, STOP_DEG))
    for k, (gap, bar) in sorted(worst.items(), key=lambda kv: kv[1][0]):
        print(f"  {k:24s} {gap:6.1f}  at {bar:+d}")

    # Drawings at straight ahead, with the bike turned to straight ahead too.
    new, turned = parts_at(0, *rows[0])
    bars = bars0.rotate(bar_axis, -SAVED_BAR)
    bike = Compound(children=[frame, box, kickstand, bars, turned["wheel"], turned["fork"]])
    new_parts = Compound(children=list(new.values()))
    export_step(new_parts, "step/jackshaft_parts.step")
    # The bike in grey, the new parts in red drawn on top so they show through the box.
    for name, eye, up in (("side", (0, -5000, 0), (0, 0, 1)), ("top", (0, 0, 5000), (1, 0, 0)),
                          ("right_low", (1500, -4000, -400), (0, 0, 1))):
        bike_vis, _ = bike.project_to_viewport(eye, viewport_up=up)
        new_vis, _ = new_parts.project_to_viewport(eye, viewport_up=up)
        exp = ExportSVG(unit=Unit.MM, line_weight=0.2)
        exp.add_layer("bike", line_color=0x999999, line_weight=0.2)
        exp.add_layer("new", line_color=0xCC2222, line_weight=0.5)
        exp.add_shape(bike_vis, layer="bike")
        exp.add_shape(new_vis, layer="new")
        exp.write(f"views/jackshaft_{name}.svg")
    print("saved views and step/jackshaft_parts.step")
