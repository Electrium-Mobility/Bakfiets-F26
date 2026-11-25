"""Cable steering for the Bakfiets, laid out like the Trek Fetch+ 4 and Decathlon F900E:
a two-groove disc on the handlebar post, another on top of the fork's steerer, and two
steel cables in bike brake housing. Turning the bars winds one cable onto the bar disc,
which pulls the fork disc round by the same angle (equal discs, so steering is 1:1).

Coordinates are from the CAD: x forward, y to the left, z up, mm. Positions here are for
riding straight; bar_deg and fork_deg turn the discs (positive = right turn).
"""
import numpy as np
from build123d import Cylinder, Plane, Location, Box, Spline, Circle, sweep, Compound, Vector, Align, Axis
from linkage import rotate, unit

# Sizes (mm)
DISC_R = 60              # outer radius of the disc plates
GROOVE_R = 55            # cable centre runs at this radius, resting on the core plates
CORE_R = GROOVE_R - 1.6 / 2   # core plates: the groove bottom, under the cable
PLATE_T, CORE_T = 3, 4   # plates and the core plates that make the two grooves
FORK_PLATES = (PLATE_T, CORE_T, PLATE_T, CORE_T, PLATE_T)   # 17 mm
# The bar disc has 2 mm outer plates (15 mm in all) to fit between the handlebar arm
# (underside z -61.2) and a kickstand cross member under it (top z -80.3).
BAR_PLATES = (2, CORE_T, PLATE_T, CORE_T, 2)
DISC_T = sum(FORK_PLATES)
BAR_DISC_T = sum(BAR_PLATES)
CABLE_D, HOUSING_D = 1.6, 5.0
BAR_SPAN = 70            # free cable from the bar disc to its housing stop (clears the disc)
FORK_SPAN = 50           # free cable from the fork disc to its housing stop
PLATE = 5                # thickness of the stop plates on both brackets
FERRULE_L = 25           # barrel adjuster and ferrule at a housing stop
STEERER_D = 43.8         # fork steerer as drawn in the CAD; measure the real one
BEND_R = 60             # bend radius of the housings

# Pivot axes, straight ahead
BAR_POINT, BAR_DIR = np.array([-4.0, 0.0, 332.0]), unit(np.array([0.012, 0.0, -1.0]))
FORK_POINT, FORK_DIR = np.array([693.5, 0.0, 444.5]), unit(np.array([0.468, 0.0, -0.884]))

# Disc centres: under the handlebar arm, and on the steerer above the head tube
BAR_DISC = BAR_POINT + BAR_DIR * ((BAR_POINT[2] - (-70.75)) / -BAR_DIR[2])
FORK_DISC = FORK_POINT + FORK_DIR * -100.0
Y = np.array([0.0, 1.0, 0.0])
X = np.array([1.0, 0.0, 0.0])


def in_plane(v, n):
    v = np.asarray(v, float)
    return unit(v - n * np.dot(v, n))


def groove_offset(n, which):
    """Groove centre along the disc axis: lower groove for the right cable, upper for the left."""
    # groove centres sit half a core plus half the middle plate from the disc's middle
    return n * ((PLATE_T + CORE_T) / 2 * (1 if which == "left" else -1))


def ends():
    """Tangent points (where a cable leaves its disc), stop points and the cable's
    direction there, for both cables at both discs. These stay fixed as the discs turn:
    a cable winds on or off the disc but always leaves it at the same place."""
    up_b = -BAR_DIR                      # bar disc axis, pointing up
    up_f = -FORK_DIR                     # fork disc axis, pointing up
    fwd_b = in_plane(X, up_b)
    side_b = in_plane(Y, up_b)
    side_f = in_plane(Y, up_f)
    back_f = in_plane(-X, up_f)
    out = {}
    for which, s in (("left", 1), ("right", -1)):
        # bar disc: cable leaves the left or right edge heading forward
        tb = BAR_DISC + side_b * GROOVE_R * s + groove_offset(up_b, which)
        # fork disc: cable leaves the front edge heading out sideways
        tf = FORK_DISC - back_f * GROOVE_R + groove_offset(up_f, which)
        out[which] = {"bar_tangent": tb, "bar_dir": fwd_b, "bar_stop": tb + fwd_b * BAR_SPAN,
                      "fork_tangent": tf, "fork_dir": side_f * s, "fork_stop": tf + side_f * s * FORK_SPAN}
    return out


# Housing route: straight runs joined by bends of radius BEND_R, the way a taut housing
# lies. Corners from route_opt.py (shortest route keeping 12 mm from the frame, box,
# kickstand and brackets and 15 mm from the wheel, fork and bars through +/-35 deg):
# a bottom corner beside the main tube bend, a top corner beside the head tube, and a
# corner straight out from the fork stop. y is given for the right side; the left mirrors it.
ROUTE = {
    "right": {"bottom": (454.5, 48.4, -24.1), "top": (691.9, 129.8, 462.7), "fork_out": 75.0},
    "left": {"bottom": (454.5, 48.4, -24.1), "top": (691.9, 129.8, 462.7), "fork_out": 75.0},
}
BAR_OUT = 60             # straight run out of the bar stop before the first bend


def housing_points(which):
    """Corners of one housing, from the end of the bar stop's ferrule to the end of the
    fork stop's ferrule. The first and last runs line up with their stops."""
    e = ends()[which]
    s = 1 if which == "left" else -1
    r = ROUTE[which]
    start = e["bar_stop"] + e["bar_dir"] * FERRULE_L
    end = e["fork_stop"] + e["fork_dir"] * FERRULE_L
    bx, by, bz = r["bottom"]
    tx, ty, tz = r["top"]
    return [start, start + e["bar_dir"] * BAR_OUT, np.array([bx, s * by, bz]), np.array([tx, s * ty, tz]),
            end + e["fork_dir"] * r["fork_out"], end]


def fillet_pieces(pts, r=BEND_R):
    """Straight runs and arcs of radius r for a polyline with rounded corners:
    ("line", p, q) and ("arc", p, middle, q). Raises if a run is too short for its bends."""
    pts = [np.asarray(p, float) for p in pts]
    n = len(pts)
    tl = [0.0] * n                       # how far each bend reaches back along its runs
    for i in range(1, n - 1):
        a, b = unit(pts[i - 1] - pts[i]), unit(pts[i + 1] - pts[i])
        inside = np.arccos(np.clip(np.dot(a, b), -1, 1))
        tl[i] = r / np.tan(inside / 2) if np.pi - inside > 1e-4 else 0.0
    for i in range(n - 1):
        if tl[i] + tl[i + 1] > np.linalg.norm(pts[i + 1] - pts[i]) + 1e-6:
            raise ValueError(f"run {i} too short for its bends")
    pieces, here = [], pts[0]
    for i in range(1, n):
        d = unit(pts[i] - pts[i - 1])
        stop = pts[i] - d * tl[i] if i < n - 1 else pts[i]
        pieces.append(("line", here, stop))
        here = stop
        if i < n - 1 and tl[i] > 0:
            d2 = unit(pts[i + 1] - pts[i])
            out = pts[i] + d2 * tl[i]
            turn = np.arccos(np.clip(np.dot(d, d2), -1, 1))        # how far the housing turns
            centre = pts[i] + unit(d2 - d) * (r / np.cos(turn / 2))
            mid = centre + unit(pts[i] - centre) * r
            pieces.append(("arc", here, mid, out))
            here = out
    return pieces


def housing_path(which):
    from build123d import Line, ThreePointArc, Wire
    edges = []
    for p in fillet_pieces(housing_points(which)):
        if p[0] == "line":
            if np.linalg.norm(p[2] - p[1]) > 1e-6:
                edges.append(Line(tuple(p[1]), tuple(p[2])))
        else:
            edges.append(ThreePointArc(tuple(p[1]), tuple(p[2]), tuple(p[3])))
    return Wire(edges)


def min_bend_radius(which, samples=400):
    """Smallest bend radius along a housing, from its curvature."""
    path = housing_path(which)
    pts = np.array([[p.X, p.Y, p.Z] for p in (path.position_at(i / samples) for i in range(samples + 1))])
    r_min, where = 1e9, None
    for i in range(1, samples):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        ab, bc, ca = np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)
        area2 = np.linalg.norm(np.cross(b - a, c - a))
        if area2 > 1e-9:
            r = ab * bc * ca / (2 * area2)
            if r < r_min:
                r_min, where = r, b
    return r_min, where, path.length


# Cable anchors. One end of each cable keeps its factory barrel nipple; the other end
# gets a screw-on (solderless) nipple after the cable is cut to length. Both sit in a
# hole drilled through the whole disc, reached from the groove by a slot in the core plate.
ANCHOR_DEG = 60          # groove from where the cable leaves the disc back to the anchor, straight ahead
ANCHOR_R = 46            # anchor hole centre, from the disc axis (hole edge 2.2 mm inside the groove bottom)
ANCHOR_LEAD = 15         # hole this many degrees further round than where the cable leaves the groove
ANCHOR_HOLE_D = 12       # a 7 x 8 mm nipple lying flat needs about 10.6; measure the bought part
ANCHOR_SLOT_W = 2.0      # slot for the 1.6 mm cable, cut into the core plate before stacking
NIPPLE_D, NIPPLE_L = 7.0, 8.0


def anchors(end):
    """Where each cable is fixed to the bar or fork disc, straight ahead: the point P where
    it leaves the groove and the anchor hole centre H, both at the groove's height. The
    anchor sits ANCHOR_DEG round the groove from the exit point, on the side the cable
    wraps from, so the cable never fully unwinds: at full lock it still has 25 deg wrapped."""
    centre, k = (BAR_DISC, BAR_DIR) if end == "bar" else (FORK_DISC, FORK_DIR)
    out = {}
    for which, w in ends().items():
        t, d = w[f"{end}_tangent"], w[f"{end}_dir"]
        # A small positive turn about k moves T along k x r; the wrapped cable lies behind T.
        s = np.sign(np.dot(np.cross(k, t - centre), d))
        p = rotate(t, centre, k, -s * ANCHOR_DEG)
        h_dir = rotate(t, centre, k, -s * (ANCHOR_DEG + ANCHOR_LEAD)) - centre
        off = np.dot(t - centre, k) * k                     # groove height along the axis
        h_dir = unit(h_dir - off)
        out[which] = {"P": p, "H": centre + off + h_dir * ANCHOR_R, "wrap_sign": -s}
    return out


def disc(centre, axis, deg, turn_axis_point, turn_axis, hole_r, plates=FORK_PLATES, mark=True, anchor_pts=()):
    """Two-groove disc: three plates of radius DISC_R with two smaller core plates between."""
    up = unit(axis)
    thick = sum(plates)
    pl = Plane(origin=tuple(centre - up * thick / 2), z_dir=tuple(up))
    parts = []
    z = 0.0
    for i, (r, t) in enumerate(zip((DISC_R, CORE_R, DISC_R, CORE_R, DISC_R), plates)):
        parts.append(pl * Cylinder(r, t, align=None).moved(Location((0, 0, z))))
        z += t
    body = parts[0]
    for p in parts[1:]:
        body = body.fuse(p)
    body = body.cut(pl * Cylinder(hole_r, thick + 2, align=None).moved(Location((0, 0, -1))))
    for a in anchor_pts:
        hole_base = a["H"] - up * np.dot(a["H"] - centre, up) - up * (thick / 2 + 1)
        body = body.cut(Plane(origin=tuple(hole_base), z_dir=tuple(up)) * Cylinder(ANCHOR_HOLE_D / 2, thick + 2, align=None))
        v = a["H"] - a["P"]
        slot_pl = Plane(origin=tuple(a["P"] - unit(v) * 3), x_dir=tuple(unit(v)), z_dir=tuple(up))
        body = body.cut(slot_pl * Box(np.linalg.norm(v) + 3, ANCHOR_SLOT_W, CORE_T + 0.2, align=(Align.MIN, Align.CENTER, Align.CENTER)))
    # a mark so the turning shows: a bolt head near the edge
    if not mark:
        return body.rotate(__import__("build123d").Axis(tuple(turn_axis_point), tuple(turn_axis)), deg)
    mark = rotate(centre + in_plane(X, up) * 40 + up * (thick / 2), turn_axis_point, turn_axis, deg)
    body = body.rotate(__import__("build123d").Axis(tuple(turn_axis_point), tuple(turn_axis)), deg)
    bolt = Plane(origin=tuple(mark), z_dir=tuple(rotate(up, np.zeros(3), turn_axis, deg))) * Cylinder(5, 4, align=None)
    return body.fuse(bolt)


def cyl_between(p, q, d):
    v = np.asarray(q, float) - np.asarray(p, float)
    return Plane(origin=tuple(p), z_dir=tuple(v / np.linalg.norm(v))) * Cylinder(d / 2, np.linalg.norm(v), align=None)


def build(bar_deg, fork_deg, mark=True):
    ab, af = anchors("bar"), anchors("fork")
    bar_disc = disc(BAR_DISC, -BAR_DIR, bar_deg, BAR_POINT, BAR_DIR, 17.5, BAR_PLATES, mark, ab.values())
    for c in bar_bolt_centres():                       # M5 bolts up through the handlebar arm
        c = rotate(c, BAR_POINT, BAR_DIR, bar_deg)
        bar_disc = bar_disc.cut(cyl_between(c + BAR_DIR * 20, c - BAR_DIR * 20, 5.5))
    fork_disc = disc(FORK_DISC, -FORK_DIR, fork_deg, FORK_POINT, FORK_DIR, STEERER_D / 2 + 0.5, FORK_PLATES, mark, af.values())
    fork_disc = fork_disc.fuse(fork_disc_extras().rotate(Axis(tuple(FORK_POINT), tuple(FORK_DIR)), fork_deg))
    out = {"bar disc": bar_disc, "fork disc": fork_disc}
    e = ends()
    for which in ("left", "right"):
        w = e[which]
        for end, a, deg, k in (("bar", ab[which], bar_deg, BAR_DIR), ("fork", af[which], fork_deg, FORK_DIR)):
            pt = BAR_POINT if end == "bar" else FORK_POINT
            p, h = rotate(a["P"], pt, k, deg), rotate(a["H"], pt, k, deg)
            u = unit(h - p)
            # The cable pulls the nipple against the hole wall on the slot side; its end-face
            # rim touches the wall where a^2 + (d/2)^2 = (hole/2)^2.
            a_back = np.sqrt((ANCHOR_HOLE_D / 2) ** 2 - (NIPPLE_D / 2) ** 2)
            n0 = h - u * a_back
            out[f"{which} anchor cable, {end}"] = cyl_between(p, n0, CABLE_D)
            out[f"{which} nipple, {end}"] = cyl_between(n0 + u * 0.2, n0 + u * NIPPLE_L, NIPPLE_D)
        out[f"{which} cable, bar"] = cyl_between(w["bar_tangent"], w["bar_stop"], CABLE_D)
        out[f"{which} cable, fork"] = cyl_between(w["fork_tangent"], w["fork_stop"], CABLE_D)
        out[f"{which} stop, bar"] = cyl_between(w["bar_stop"], w["bar_stop"] + w["bar_dir"] * FERRULE_L, 8)
        out[f"{which} stop, fork"] = cyl_between(w["fork_stop"], w["fork_stop"] + w["fork_dir"] * FERRULE_L, 8)
        path = housing_path(which)
        start = path.position_at(0)
        out[f"{which} housing"] = sweep(Plane(origin=start, z_dir=path.tangent_at(0)) * Circle(HOUSING_D / 2), path)
    return out


# Brackets. Both clamp to the frame, so they stay put while the discs turn.
MAIN_TUBE_R = 22.2       # main tube, 44.4 mm across, centred on y = 0, z = 0
HEAD_TUBE_R = 23.05      # head tube, 46.1 mm across, bare from 30 to 65 mm up the fork axis
CLAMP_T = 5.8            # wall of the clamp rings
ARM_BOTTOM_Z = -61.2     # underside of the handlebar arm


def box_between(lo, hi, plane=Plane.XY):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    return plane * Box(*(hi - lo), align=None).moved(Location(tuple(lo)))


def bar_bracket():
    """Stop plate across the bike just ahead of the bar disc, hung from a two-piece clamp
    on the main tube by a post up the middle. Right of centre the plate stays below the
    handlebar arm, which sweeps that side; the left stop gets a taller boss."""
    e = ends()
    x1 = min(e["left"]["bar_stop"][0], e["right"]["bar_stop"][0])
    x0 = x1 - PLATE
    zl, zr = e["left"]["bar_stop"][2], e["right"]["bar_stop"][2]
    body = box_between((x0, -63, zr - 8), (x1, 63, ARM_BOTTOM_Z - 2.8))        # cross plate
    body = body.fuse(box_between((x0, 45, zl - 4), (x1, 63, zl + 8)))           # left boss
    body = body.fuse(box_between((x0, -12, ARM_BOTTOM_Z - 3), (x1, 12, -MAIN_TUBE_R - 3)))  # post
    ring_pl = Plane(origin=(x0 - 2.5, 0, 0), z_dir=(1, 0, 0))
    ring = ring_pl * Cylinder(MAIN_TUBE_R + CLAMP_T, 10, align=None)
    body = body.fuse(ring)
    for s in (1, -1):                                                            # clamp bolt lugs
        body = body.fuse(box_between((x0 - 2.5, min(s * 26, s * 36), -4), (x0 + 7.5, max(s * 26, s * 36), 4)))
    body = body.cut(ring_pl * Cylinder(MAIN_TUBE_R, 12, align=None).moved(Location((0, 0, -1))))
    for s in (1, -1):                                                            # M6 clamp bolts, vertical
        body = body.cut(cyl_between(np.array([x0 + 2.5, s * 31, -10]), np.array([x0 + 2.5, s * 31, 10]), CLAMP_BOLT_D))
    for which in ("left", "right"):                                              # cable holes
        p = e[which]["bar_stop"]
        body = body.cut(cyl_between(p - X * (PLATE + 1), p + X, 3))
    return body


def fork_bracket():
    """Clamp ring on the bare top of the head tube, a plate forward from it, and two
    uprights beside the fork disc that hold the stops 50 mm out to each side."""
    up = -FORK_DIR
    fwd = in_plane(X, up)
    pl = Plane(origin=tuple(FORK_POINT), x_dir=tuple(fwd), z_dir=tuple(up))   # local (forward, y, up the axis)
    body = pl * Cylinder(HEAD_TUBE_R + CLAMP_T, 18, align=None).moved(Location((0, 0, 42)))
    body = body.fuse(box_between((20, -50, 52), (68, 50, 58), pl))              # base plate
    for s in (1, -1):
        body = body.fuse(box_between((46, min(s * 45, s * 50), 52), (68, max(s * 45, s * 50), 116), pl))
    body = body.fuse(box_between((-38, -10, 42), (-26, 10, 60), pl))             # clamp bolt lug
    body = body.cut(pl * Cylinder(HEAD_TUBE_R, 40, align=None).moved(Location((0, 0, 30))))
    body = body.cut(box_between((-40, -1, 40), (-HEAD_TUBE_R + 1, 1, 62), pl))       # pinch slit at the back
    a, b = pl.from_local_coords((-32, -15, 51)), pl.from_local_coords((-32, 15, 51))
    body = body.cut(cyl_between(np.array([a.X, a.Y, a.Z]), np.array([b.X, b.Y, b.Z]), CLAMP_BOLT_D))   # M6 pinch bolt
    e = ends()
    for which in ("left", "right"):
        p, d = e[which]["fork_stop"], e[which]["fork_dir"]
        body = body.cut(cyl_between(p - d * (PLATE + 1), p + d, 3))
    return body


def bar_spacers(bar_deg):
    """Two spacers between the bar disc and the handlebar arm, on the arm's centreline
    25 and 45 mm from the post. At straight ahead the arm points right (-y)."""
    up = -BAR_DIR
    side = in_plane(Y, up)
    out = []
    for r in (25, 45):
        base = BAR_DISC + up * (BAR_DISC_T / 2) - side * r
        top = base + up * ((ARM_BOTTOM_Z - base[2]) / up[2])
        out.append(cyl_between(rotate(base, BAR_POINT, BAR_DIR, bar_deg), rotate(top, BAR_POINT, BAR_DIR, bar_deg), 10))
    return out[0].fuse(out[1])


# Printed-part features. The fork disc carries its own clamp hub (it grips the
# steerer below the disc) and the steering stop: a tab on its top face that meets
# the fork bracket's uprights a little past 35 deg either way.
HUB_OD, HUB_H = 64, 16          # clamp hub under the fork disc; its two M6 bolts sit side by side, 14 mm apart
CLAMP_BOLT_D = 6.4              # M6 clearance
STOP_TAB_W, STOP_TAB_T = 14, 6  # stop tab width and thickness
STOP_TAB_R = 65                 # how far the tab reaches from the steering axis: meets the bracket at 37.5 deg


def fork_plane():
    up = -FORK_DIR
    return Plane(origin=tuple(FORK_POINT), x_dir=tuple(in_plane(X, up)), z_dir=tuple(up))   # (forward, y, up the axis)


def fork_disc_extras():
    """Clamp hub and stop tab for the fork disc, straight ahead. The hub is split at the
    back and closed by two M6 bolts across a lug."""
    pl = fork_plane()
    s0 = 100 - DISC_T / 2                       # underside of the fork disc, up the axis
    hub = pl * Cylinder(HUB_OD / 2, HUB_H + 0.5, align=None).moved(Location((0, 0, s0 - HUB_H)))
    hub = hub.fuse(box_between((-55, -10, s0 - HUB_H), (-26, 10, s0 + 0.5), pl))
    hub = hub.cut(pl * Cylinder(STEERER_D / 2 + 0.3, 60, align=None).moved(Location((0, 0, s0 - HUB_H - 5))))
    hub = hub.cut(box_between((-57, -1, s0 - HUB_H - 1), (-STEERER_D / 2 + 1, 1, s0), pl))      # split
    for f in (-34, -48):
        a, b = pl.from_local_coords((f, -15, s0 - HUB_H / 2)), pl.from_local_coords((f, 15, s0 - HUB_H / 2))
        hub = hub.cut(cyl_between(np.array([a.X, a.Y, a.Z]), np.array([b.X, b.Y, b.Z]), CLAMP_BOLT_D))
    top = 100 + DISC_T / 2
    tab = box_between((40, -STOP_TAB_W / 2, top - 0.5), (STOP_TAB_R, STOP_TAB_W / 2, top + STOP_TAB_T), pl)
    return hub.fuse(tab)


def bar_bolt_centres():
    """Two M5 bolts join the handlebar disc to the handlebar arm, on the arm's centreline
    25 and 45 mm from the post (straight ahead)."""
    up = -BAR_DIR
    side = in_plane(Y, up)
    return [BAR_DISC - side * r for r in (25, 45)]


def build_all(bar_deg, fork_deg, mark=True):
    out = build(bar_deg, fork_deg, mark)
    out["bar bracket"] = bar_bracket()
    out["fork bracket"] = fork_bracket()
    out["bar spacers"] = bar_spacers(bar_deg)
    return out
