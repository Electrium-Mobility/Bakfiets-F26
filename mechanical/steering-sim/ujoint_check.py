"""Checks a U-joint steering case on the real solids (BRep distances, not point clouds):
joint bends against their ratings, the handlebar-to-fork turning from -35 to +35 deg,
and the smallest gap from every new part to the frame, cargo box, kickstand,
handlebars, wheel and fork, with the moving parts turned in 5 deg steps.
A gap of 0 means the parts overlap; the overlap volume is then given.

Usage: ujoint_check.py <case>   (writes ujoint_check_<case>.log; also saves the
yoke twists to ujoint_<case>_phases.npz for the pictures)"""
import sys
import numpy as np
from build123d import import_step, Box, Location
import ujoint_layout as U
import ujoint_parts as J
from current_design import SAVED_BAR, SAVED_FORK
from build123d import Axis

case = sys.argv[1]
log = open(f"ujoint_check_{case}.log", "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    log.write(s + "\n")
    log.flush()


pts, kinds = J.layout(case)
say(f"case {case}: joints {kinds}")
for i, p in enumerate(pts):
    say(f"  joint {i + 1} centre {np.round(p, 1)}")
f = U.flows_n(pts)
for i in range(len(pts) - 1):
    say(f"  S{i + 1}: {np.linalg.norm(pts[i + 1] - pts[i]):.0f} mm centre to centre, direction {np.round(f[i + 1], 3)}")
say("bends (deg) against rating:")
for name, k, b, lim in J.bend_table(case):
    say(f"  {name:8s} {k:8s} {b:6.1f}  rating {lim:.0f}  {'OK' if b <= lim + 1e-6 else 'OVER by %.1f' % (b - lim)}")

plan = J.phase_plan(case)
np.savez(f"ujoint_{case}_phases.npz", phases=plan["phases"], start=plan["start"], table=plan["table"])
t = plan["table"]
say("turning, handlebars -> fork (best yoke twists found):")
for b in (-35, -30, -20, -10, -5, 0, 5, 10, 20, 30, 35):
    row = t[np.argmin(np.abs(t[:, 0] - b))]
    say(f"  {row[0]:+6.1f} -> {row[1]:+7.2f}   lag {row[1] - row[0]:+6.2f}")
d = np.gradient(t[:, 1], t[:, 0])
say(f"  worst lag {np.max(np.abs(t[:, 1] - t[:, 0])):.2f} deg; local ratio fork/bars {d.min():.3f} to {d.max():.3f}")
plan0 = J.phase_plan(case, search=False)
t0 = plan0["table"]
d0 = np.gradient(t0[:, 1], t0[:, 0])
say(f"  with all yokes lined up (no twist chosen): worst lag {np.max(np.abs(t0[:, 1] - t0[:, 0])):.2f} deg, ratio {d0.min():.3f} to {d0.max():.3f}")

# ------------------------------------------------------------- clashes
asm = import_step("step/f26bakfiets_main_asm.step")
P = {c.label: c for c in asm.children}
frame = P["f26bakfiets_frame_Default<As_Machined>"]
box = P["f26bakfiets_cargo_box_low_detail"]
kick = P["f26bakfiets_kickstand_Default<As_Machined>"]
if kinds[0] == "gearbox":
    kick = J.kickstand_fixed(kick)
    say(f"kickstand: front cross piece moved {J.KICK_SHIFT:.0f} mm forward")
bar_axis = Axis(tuple(U.BAR_POINT), tuple(U.BAR_DIR))
fork_axis = Axis(tuple(U.FORK_POINT), tuple(U.FORK_DIR))
bars0 = P["f26bakfiets_steering_handlebars"].rotate(bar_axis, -SAVED_BAR)
bars0 = bars0 - Box(400, 400, 20, align=None).moved(Location((-200, -200, -66.5)))   # arm cut off
wheel0 = P["f26bakfiets_front_wheel"].rotate(fork_axis, -SAVED_FORK)
fork0 = P["f26bakfiets_front_suspension"].rotate(fork_axis, -SAVED_FORK)

env = J.envelopes(case)
fixed = {"frame": frame, "box": box, "kickstand": kick}
worst = {}


def gap(a, b):
    d = a.distance_to(b)
    if d < 1e-6:
        inter = a & b
        v = inter.volume if inter else 0.0
        return 0.0, v
    return d, None


for n, s in env.items():
    for o, sh in fixed.items():
        worst[(n, o)] = (*gap(s, sh), None)
for bar in range(-35, 36, 5):
    fk = float(np.interp(bar, t[:, 0], t[:, 1]))
    moving = {"bars": bars0.rotate(bar_axis, bar), "wheel": wheel0.rotate(fork_axis, fk),
              "fork": fork0.rotate(fork_axis, fk)}
    for n, s in env.items():
        for o, sh in moving.items():
            if o == "bars" and (n in ("post stub", "gearbox") or n == "UJ1"):
                continue          # these bolt to the post
            if o == "fork" and n in ("steerer stub",):
                continue          # bolts to the steerer
            g, v = gap(s, sh)
            k = (n, o)
            if k not in worst or g < worst[k][0] or (g == 0 and (v or 0) > (worst[k][1] or 0)):
                worst[k] = (g, v, bar)
say("smallest gaps (mm), every new part to every bike part:")
for (n, o), (g, v, bar) in sorted(worst.items(), key=lambda kv: kv[1][0]):
    at = "" if bar is None else f" at handlebars {bar:+d}"
    extra = f"  OVERLAP {v:.0f} mm^3" if g == 0 else ""
    say(f"  {n:13s} to {o:9s} {g:6.1f}{at}{extra}")
# new parts against each other (not neighbours in the chain)
names = list(env)
n_j = len(kinds)


def joint_no(n):
    return 1 if n == "gearbox" else int(n[2:]) if n.startswith("UJ") else None


def adjacent(a, b):
    ja, jb = joint_no(a), joint_no(b)
    for s_, j in ((a, jb), (b, ja)):
        if j is None:
            continue
        if s_.startswith("S") and j in (int(s_[1:]), int(s_[1:]) + 1):
            return True
        if s_ == "post stub" and j == 1:
            return True
        if s_ == "steerer stub" and j == n_j:
            return True
    return False


say("new parts against each other (gaps under 15 mm; parts that join are skipped):")
for i, a in enumerate(names):
    for b in names[i + 1:]:
        if adjacent(a, b):
            continue
        g = env[a].distance_to(env[b])
        if g < 15:
            say(f"  {a} to {b}: {g:.1f}" + ("  OVERLAP" if g < 1e-6 else ""))
say("DONE")
