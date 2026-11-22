"""The jackshaft built from off-the-shelf parts, for pictures and a parts list.

Bought parts are drawn at typical catalogue sizes, rounded. Check them against the
parts actually ordered.

- 12 mm steel shaft in two KP001 pillow block bearings
- the pillow blocks bolt onto two flat plates that lie against the side of the
  frame's front tube, held on by two U-bolts each (the plates are the only made parts)
- the arms are flat bar bolted to 12 mm clamping hubs
- the rods are M10 threaded rod with a rod end screwed onto each end
- the stop is a shaft collar with a long bolt sticking out, which hits one of two
  long bolts with rubber sleeves screwed into the upper plate
"""
import numpy as np
from build123d import Box, Cylinder, Sphere, Plane, Location, Vector, Compound
import jackshaft as J
import jackshaft_check as C
from linkage import rotate, unit
from current_design import CURRENT

SHAFT_D = 12
TUBE_R = 22.25
PLATE_T, PLATE_W = 6, 76
KP_L, KP_W, KP_HOUSING_D = 76, 20, 32            # KP001 pillow block: length, width along shaft, housing
HUB_D, HUB_H, HUB_FLANGE_D, HUB_FLANGE_T = 30, 20, 40, 5
ARM_W, ARM_T = 25, 6
EYE_D, EYE_T, BALL_D, SHANK_D, SHANK_LEN = 28, 12, 16, 15, 30   # M10 rod end (e.g. SI10T/K), rounded
ROD_D = 10
UBOLT_D = 8
COLLAR_D, COLLAR_W = 25, 12
STOP_BOLT_D, STOP_LEN = 12, 42                   # M8 x 45 bolt with a rubber sleeve, sleeve drawn
PIN_LEN = 28                                     # M6 bolt in the stop collar
LOWER = (20, 120, 52)        # lower plate: bottom, top and bearing height (mm up the frame)
UPPER = (305, 362, 333)      # upper plate: above the box wall, below the top arm
Z_STOP = 75                  # stop collar height, on the lower plate
BAR_ARM_FACE = 20           # old ball centre down to the top of the handlebar arm, measured in the CAD
FORK_ARM_FACE = 23          # old ball centre up to the top of the fork arm, measured in the CAD
PIN_FORWARD = 15             # stop pin angle forward of straight out, when riding straight


def cyl_between(p1, p2, d):
    v = Vector(*(np.asarray(p2, float) - np.asarray(p1, float)))
    return Plane(origin=tuple(p1), z_dir=v.normalized()) * Cylinder(d / 2, v.length, align=None)


def tube_axis_point(z):
    return np.array([515 + z * 0.365 / 0.931, 0.0, z])


class Frame:
    """Local directions at a height: t along the shaft, n from the tube to the shaft, s sideways."""
    def __init__(self, d, z):
        self.t = d.shaft_dir
        tube = tube_axis_point(z)
        v = d.shaft_point(z) - tube
        v -= self.t * np.dot(v, self.t)
        self.gap = np.linalg.norm(v)                 # tube centre to shaft centre
        self.n = v / self.gap
        self.s = np.cross(self.n, self.t)   # matches the y axis of a plane with x = t, z = n
        self.tube = tube
        self.shaft = d.shaft_point(z)

    def at(self, along, side, out):
        """Point 'out' mm from the tube's centre line towards the shaft."""
        return self.tube + self.t * along + self.s * side + self.n * out

    def box(self, along, side, out, size_t, size_s, size_n):
        """Box with its low corner at (along, side, out) in this frame."""
        pl = Plane(origin=tuple(self.at(along, side, out)), x_dir=tuple(self.t), z_dir=tuple(self.n))
        return pl * Box(size_t, size_s, size_n, align=None)


def plate_with_bearing(d, z_bottom, z_top, z_bearing):
    f = Frame(d, z_bearing)
    a, b = z_bottom - z_bearing, z_top - z_bearing        # along the shaft, roughly heights
    length = b - a
    out = {}
    out["plate"] = f.box(a, -PLATE_W / 2, TUBE_R, length, PLATE_W, PLATE_T)
    base_top = f.gap - 4
    out["bearing"] = f.box(-KP_W / 2, -KP_L / 2, TUBE_R + PLATE_T, KP_W, KP_L, base_top - TUBE_R - PLATE_T).fuse(
        cyl_between(f.shaft - f.t * KP_W / 2, f.shaft + f.t * KP_W / 2, KP_HOUSING_D))
    # U-bolts: two straight legs up through the plate, joined by a half circle round
    # the far side of the tube.
    bolts = []
    r = TUBE_R + UBOLT_D / 2
    for along in (a + 12, b - 12):
        for side in (-1, 1):
            bolts.append(cyl_between(f.at(along, side * r, 0), f.at(along, side * r, TUBE_R + PLATE_T + 8), UBOLT_D))
        arc = [f.at(along, r * np.cos(th), -r * np.sin(th)) for th in np.linspace(0, np.pi, 13)]
        for p, q in zip(arc[:-1], arc[1:]):
            bolts.append(cyl_between(p, q, UBOLT_D))
            bolts.append(Sphere(UBOLT_D / 2).moved(Location(tuple(q))))
    out["u-bolts"] = Compound(children=bolts)
    return out, f


def arm_on_hub(d, z, joint0, shaft_deg, hub_above=False):
    """Flat bar arm on a clamping hub. The rod end's eye sits against the arm with its
    ball centre at the joint, so the arm is shifted by half the eye plus half the arm:
    down for the bottom arm (rod end on top), up for the top arm (rod end underneath)."""
    t = d.shaft_dir
    j = rotate(joint0, d.shaft_point(0), t, shaft_deg)
    shift = (EYE_T / 2 + ARM_T / 2) * (1 if hub_above else -1)
    centre = d.shaft_point(z) + t * shift
    r = (j - centre) - t * np.dot(j - centre, t)
    length = np.linalg.norm(r)
    pl = Plane(origin=tuple(centre), x_dir=tuple(r / length), z_dir=tuple(t))
    arm = pl * Box(length + ARM_W / 2, ARM_W, ARM_T, align=None).moved(Location((0, -ARM_W / 2, -ARM_T / 2)))
    hub = (Cylinder(HUB_FLANGE_D / 2, HUB_FLANGE_T, align=None).moved(Location((0, 0, -ARM_T / 2 - HUB_FLANGE_T)))
           .fuse(Cylinder(HUB_D / 2, HUB_H, align=None).moved(Location((0, 0, -ARM_T / 2 - HUB_FLANGE_T - HUB_H)))))
    if hub_above:            # mirror the hub to the top side of the arm
        hub = Cylinder(HUB_FLANGE_D / 2, HUB_FLANGE_T, align=None).moved(Location((0, 0, ARM_T / 2))).fuse(
            Cylinder(HUB_D / 2, HUB_H, align=None).moved(Location((0, 0, ARM_T / 2 + HUB_FLANGE_T))))
    return pl * hub, arm, j


def rod_end(p, bolt_axis, toward):
    """An M10 rod end: a ring (eye) around a swivel ball, a threaded shank pointing at
    the other end of the rod, and the bolt through the ball."""
    a = unit(bolt_axis)
    u = unit(np.asarray(toward) - p)               # the shank always points along the rod
    e = unit(a - u * np.dot(a, u))                  # so the eye is square to the rod; the ball swivels to meet the bolt
    eye = cyl_between(p - e * EYE_T / 2, p + e * EYE_T / 2, EYE_D).cut(
        cyl_between(p - e * EYE_T, p + e * EYE_T, BALL_D))
    ball = Sphere(BALL_D / 2).moved(Location(tuple(p))).cut(cyl_between(p - a * 20, p + a * 20, 10))
    shank = cyl_between(p + u * (EYE_D / 2 - 2), p + u * (EYE_D / 2 + SHANK_LEN), SHANK_D)
    bolt = cyl_between(p - a * (EYE_T / 2 + ARM_T + 6), p + a * (EYE_T / 2 + 6), 10)
    return [eye, ball, shank, bolt]


def rod_with_ends(p1, a1, p2, a2):
    """Threaded rod between two rod ends whose ball centres are p1 and p2."""
    parts = rod_end(p1, a1, p2) + rod_end(p2, a2, p1)
    u = unit(np.asarray(p2) - np.asarray(p1))
    gap = EYE_D / 2 + SHANK_LEN - 8                      # rod screwed into both shanks
    parts.append(cyl_between(p1 + u * gap, p2 - u * gap, ROD_D))
    return parts


def shaft_at_stops(d):
    """Shaft angle at the left and right handlebar stops."""
    rows = {round(b): s for b, s, f, w in J.simulate(d, step=1.0, limit=J.STOP_DEG)}
    return rows[-J.STOP_DEG], rows[J.STOP_DEG]


def build(d, bar, shaft, fork):
    t = d.shaft_dir
    out = {"shaft": cyl_between(d.shaft_point(d.z_lo - 45), d.shaft_point(UPPER[2] + 20), SHAFT_D)}

    # The front wall of the cargo box comes within about 35 mm of the frame tube between
    # roughly 100 and 305 mm up, so the bearings go below and above that band.
    lower, _ = plate_with_bearing(d, *LOWER)
    upper, fu = plate_with_bearing(d, *UPPER)
    for k, v in lower.items():
        out["lower " + k] = v
    for k, v in upper.items():
        out["upper " + k] = v

    hub, arm, j2 = arm_on_hub(d, d.z_lo, d.lower_joint(), shaft)
    out["lower hub"], out["lower arm"] = hub, arm
    hub, arm, j3 = arm_on_hub(d, d.z_hi, d.upper_joint(), shaft, hub_above=True)
    out["upper hub"], out["upper arm"] = hub, arm

    j1 = rotate(J.BAR_JOINT, C.BAR_POINT, C.BAR_DIR, bar)
    j4 = rotate(d.fork_joint(), C.FORK_POINT, C.FORK_DIR, fork)
    out["lower rod"] = Compound(children=rod_with_ends(j1, C.BAR_DIR, j2, t))
    out["upper rod"] = Compound(children=rod_with_ends(j3, t, j4, C.FORK_DIR))
    # The new rod ends bolt through the holes the old ball joints used, each standing
    # on a spacer on top of its arm. At the handlebar the ball is where the old one was,
    # 20 mm above the arm. At the fork the ball is lifted FORK_SPACER mm, and the arm's
    # top is 23 mm above the old ball.
    bar_down = unit(C.BAR_DIR)
    out["bar spacer"] = cyl_between(j1 + bar_down * BAR_ARM_FACE, j1 + bar_down * EYE_T / 2, 16)
    old_fork = rotate(CURRENT.fork_joint0, C.FORK_POINT, C.FORK_DIR, fork)
    fork_up = -unit(C.FORK_DIR)
    out["fork spacer"] = cyl_between(old_fork + fork_up * FORK_ARM_FACE, j4 - fork_up * EYE_T / 2, 16)

    # Stop: a shaft collar on the lower plate with a bolt sticking out. When riding
    # straight the bolt points 15 deg forward of straight out, so both stop bolts end
    # up at the front of the plate, away from the cargo box.
    fs = Frame(d, Z_STOP)
    out["stop collar"] = cyl_between(fs.shaft - t * COLLAR_W / 2, fs.shaft + t * COLLAR_W / 2, COLLAR_D)
    forward = -fs.s if fs.s[0] < 0 else fs.s
    pin0 = fs.shaft + (np.cos(np.radians(PIN_FORWARD)) * fs.n + np.sin(np.radians(PIN_FORWARD)) * forward) * PIN_LEN

    def tip(deg):
        return rotate(pin0, fs.shaft, t, deg)

    out["stop pin"] = cyl_between(fs.shaft, tip(shaft), 8)
    for name, lateral, height in stop_bolts(d):
        base = fs.at(0, lateral, TUBE_R + PLATE_T)
        out[name] = cyl_between(base, base + fs.n * height, STOP_BOLT_D)
    return out


_stop_cache = {}


def stop_bolts(d):
    """Where to put the two stop bolts so the pin first touches each one exactly at a
    handlebar stop. Worked out in the flat cross-section through the stop collar:
    the pin is a line from the shaft centre, a stop bolt is a line standing out from
    the plate, and they touch when the lines come within (sleeve radius + pin radius)."""
    key = id(d)
    if key in _stop_cache:
        return _stop_cache[key]
    fs = Frame(d, Z_STOP)
    t = d.shaft_dir
    forward = -fs.s if fs.s[0] < 0 else fs.s
    pin0 = fs.shaft + (np.cos(np.radians(PIN_FORWARD)) * fs.n + np.sin(np.radians(PIN_FORWARD)) * forward) * PIN_LEN

    def flat(p):            # (sideways, out from the tube's centre line)
        v = p - fs.tube
        return np.array([np.dot(v, fs.s), np.dot(v, fs.n)])

    centre = flat(fs.shaft)
    plate = TUBE_R + PLATE_T
    touch = STOP_BOLT_D / 2 + 4

    def seg_dist(a, b, c, e):
        def pt_seg(p, q, r):
            qr = r - q
            u = np.clip(np.dot(p - q, qr) / np.dot(qr, qr), 0, 1)
            return np.linalg.norm(p - (q + u * qr))
        return min(pt_seg(a, c, e), pt_seg(b, c, e), pt_seg(c, a, b), pt_seg(e, a, b))

    def first_contact(lateral, height, sign):
        bolt_a, bolt_b = np.array([lateral, plate]), np.array([lateral, plate + height])
        for deg in np.arange(0, 120, 0.25):
            tip = flat(rotate(pin0, fs.shaft, t, sign * deg))
            if seg_dist(centre, tip, bolt_a, bolt_b) <= touch:
                return deg
        return 999

    result = []
    height = 45.0
    for name, stop in zip(("stop A", "stop B"), shaft_at_stops(d)):
        sign = np.sign(stop)
        # Which way the tip moves sideways for this stop.
        side = np.sign(flat(rotate(pin0, fs.shaft, t, sign * 5))[0] - flat(pin0)[0])
        lo, hi = centre[0], centre[0] + side * 120          # bolt near the shaft .. far away
        for _ in range(40):
            mid = (lo + hi) / 2
            if first_contact(mid, height, sign) < abs(stop):
                lo = mid
            else:
                hi = mid
        result.append((name, hi, height))
    _stop_cache[key] = result
    return result


COLOURS = [("shaft", "#1f77b4"), ("bearing", "#2ca02c"), ("plate", "#9467bd"), ("u-bolt", "#bbbbbb"),
           ("hub", "#17becf"), ("arm", "#ff9f1c"), ("rod", "#d62728"), ("spacer", "#8c8c8c"),
           ("stop collar", "#17becf"), ("stop pin", "#555555"), ("stop", "#222222")]


def colour(name):
    for k, c in COLOURS:
        if k in name:
            return c
    return "#ffd23f"
