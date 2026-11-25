"""Bolt-on steering stopper for the bent-rod steering (f26bakfiets_main_asm, 11 Nov).

It replaces the welded strip (Part1). A two-piece clamp grips the bare top of the head
tube; a half shell hangs from it down the right side of the head tube and carries the
same two M6 stud bumpers (McMaster 9546K431) the welded strip carried. The fork arm
meets a bumper at 35 deg of fork turn either way (the welded strip stops it at 39).

Local coordinates used below: x forward (square to the steering axis), y to the left,
z up the steering axis, origin at FORK_POINT. Angles are measured from forward,
positive to the left, so the fork arm (on the right) sits near -78 deg.
"""
import numpy as np
from build123d import Axis, Box, Cylinder, Location, Plane, GeomType
from linkage import unit

FORK_POINT = np.array([693.5, 0.0, 444.5])
FORK_DIR = unit([0.468, 0.0, -0.884])      # points down the steering axis
STOP_DEG = 35.0                            # fork angle at which the arm meets a bumper
OLD_LEFT, OLD_RIGHT = -39.02, 39.08        # where the welded strip's bumpers stop the fork (contact.py)

HEAD_TUBE_R = 23.05      # head tube, 46.1 mm across, bare all round from about 35 to 78 mm up the axis
RING_T = 8               # clamp ring wall
RING_LO, RING_HI = 42, 70
SHELL_R, SHELL_T = 78, 6   # shell inner radius (the fork crown sweeps out to 72.6) and wall
SHELL_FROM, SHELL_TO = -150, -8   # shell angles
SHELL_BOTTOM = -84       # the fork arm passes below this, 95 to 98.5 mm down the axis
PLATE_T = 8              # the two flat sectors joining ring and shell
LUG_T = 18               # bumper lug thickness along the bumper's axis
LUG_BOTTOM, LUG_TOP = -111, -55
BOLT_D = 6.4             # M6 clearance, clamp bolts and bumper studs
EAR_X = 37               # clamp bolts sit this far ahead of and behind the axis


def plane():
    up = -FORK_DIR
    fwd = unit(np.array([1.0, 0, 0]) - up * up[0])
    return Plane(origin=tuple(FORK_POINT), x_dir=tuple(fwd), z_dir=tuple(up))


def sector(r_in, r_out, deg_from, deg_to, z_lo, z_hi):
    """Part of a ring between two angles, in local coordinates."""
    s = Cylinder(r_out, z_hi - z_lo, arc_size=deg_to - deg_from, align=None)
    s = s.cut(Cylinder(r_in, z_hi - z_lo + 2, align=None).moved(Location((0, 0, -1))))
    return s.rotate(Axis.Z, deg_from).moved(Location((0, 0, z_lo)))


def box(lo, hi):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    return Box(*(hi - lo), align=None).moved(Location(tuple(lo)))


def cyl(p, q, d):
    p, q = np.asarray(p, float), np.asarray(q, float)
    pl = Plane(origin=tuple(p), z_dir=tuple(q - p))
    return pl * Cylinder(d / 2, float(np.linalg.norm(q - p)), align=None)


def old_bumpers(asm):
    return sorted((c for c in asm.children if c.label.startswith("9546K431")), key=lambda c: -c.center().X)


def bumpers(asm):
    """The two CAD bumpers, each turned about the steering axis so the fork meets it at STOP_DEG.
    Returns [front (stops left turns), rear (stops right turns)] in bike coordinates."""
    ax = Axis(tuple(FORK_POINT), tuple(FORK_DIR))
    front, rear = old_bumpers(asm)
    return [front.rotate(ax, -STOP_DEG - OLD_LEFT), rear.rotate(ax, STOP_DEG - OLD_RIGHT)]


def mount(bumper):
    """Centre of the bumper's flat mounting face and the direction away from the bumper, local."""
    pl = plane()
    f = max((f for f in bumper.faces() if f.geom_type == GeomType.PLANE), key=lambda f: f.area)
    to_local = lambda v: np.array(tuple(pl.to_local_coords(v)))
    m, c = to_local(f.center()), to_local(bumper.center())
    n = to_local(f.center() + f.normal_at()) - m
    if n @ (m - c) < 0:
        n = -n
    n[2] = 0
    return m, unit(n)


def stopper(asm):
    """Returns (body, cap, bumpers) in bike coordinates."""
    pl = plane()
    bump = bumpers(asm)
    ring_r = HEAD_TUBE_R + RING_T
    body = Cylinder(ring_r, RING_HI - RING_LO, align=None).moved(Location((0, 0, RING_LO)))
    for s in (1, -1):                                              # clamp ears, ahead and behind
        body = body.fuse(box((min(s * 27, s * 47), -9, RING_LO), (max(s * 27, s * 47), 9, RING_HI)))
    for z in (RING_LO, RING_HI - PLATE_T):                         # two flat sectors out to the shell
        body = body.fuse(sector(ring_r - 2, SHELL_R + SHELL_T, SHELL_FROM, SHELL_TO, z, z + PLATE_T))
    body = body.fuse(sector(SHELL_R, SHELL_R + SHELL_T, SHELL_FROM, SHELL_TO, SHELL_BOTTOM, RING_HI))
    holes = []
    for b in bump:                                                 # one lug behind each bumper
        m, n = mount(b)
        w = np.cross([0, 0, 1], n)
        if w @ unit([m[0], m[1], 0]) < 0:
            w = -w                                                 # w points away from the axis
        lug_pl = Plane(origin=(m[0], m[1], 0), x_dir=tuple(n), z_dir=(0, 0, 1))
        y_lo, y_hi = (-12, 16) if np.cross(n, w)[2] > 0 else (-16, 12)
        body = body.fuse(lug_pl * box((0, y_lo, LUG_BOTTOM), (LUG_T, y_hi, LUG_TOP)))
        holes.append(cyl(m - n, m + n * (LUG_T + 1), BOLT_D))                         # stud
        holes.append(cyl(m + n * 8, m + n * (LUG_T + 1), 14))                         # nut pocket from the back
    body = body.cut(Cylinder(HEAD_TUBE_R, 60, align=None).moved(Location((0, 0, RING_LO - 10))))
    for h in holes:
        body = body.cut(h)
    for s in (1, -1):                                              # M6 clamp bolts across the split
        body = body.cut(cyl((s * EAR_X, -12, (RING_LO + RING_HI) / 2), (s * EAR_X, 12, (RING_LO + RING_HI) / 2), BOLT_D))
    body = body.cut(box((-50, -1, RING_LO - 1), (50, 1, RING_HI + 1)))                # split: cap on the left
    solids = sorted(body.solids(), key=lambda s: s.volume)
    assert len(solids) == 2, f"expected body and cap, got {len(solids)} pieces"
    cap, main = solids
    return pl * main, pl * cap, bump


if __name__ == "__main__":
    from build123d import import_step, export_step, export_stl
    asm = import_step("step/f26bakfiets_main_asm.step")
    main, cap, bump = stopper(asm)
    print(f"body {main.volume / 1000:.0f} cm3, cap {cap.volume / 1000:.0f} cm3")
    for name, part in (("stopper_body", main), ("stopper_cap", cap)):
        export_step(part, f"step/{name}.step")
        export_stl(part, f"step/print/{name}.stl", tolerance=0.05)
        print("saved", name)
