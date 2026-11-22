"""Jackshaft steering for the Bakfiets: handlebar arm -> lower rod -> jackshaft -> upper rod -> fork arm.

The jackshaft is a short shaft in two bearings, clamped beside the frame's front
upright tube, between the front of the cargo box and the back of the wheel. Both
rods are straight. The optimizer picks the shaft position and tilt, the arm
heights, lengths and angles, and the fork arm, so the fork follows the handlebars
closely and both rods push at a good angle.

Coordinates are from Annie's model: x forward, y to the left, z up, in mm.
Angles are positive for a right turn.
"""
import math
from dataclasses import dataclass
import numpy as np
from scipy.optimize import differential_evolution
from linkage import Linkage, rotate, unit
from current_design import CURRENT

BAR_POINT, BAR_DIR = CURRENT.bar_point, CURRENT.bar_dir
BAR_JOINT = CURRENT.bar_joint0                      # existing handlebar arm, straight ahead
FORK_POINT, FORK_DIR = CURRENT.fork_point, CURRENT.fork_dir
STOP_DEG = 35          # hard stops on the jackshaft limit the handlebars to this
CHECK_DEG = 40         # the linkage must behave a little past the stops

# Box front wall, from the model: x = 468 + 0.489 (z - 37) for z between 37 and 305.
def box_wall_x(z):
    return 468 + 0.489 * (min(max(z, 37), 305) - 37)

@dataclass
class Design:
    lean_deg: float    # jackshaft tilt forward from vertical
    x0: float          # jackshaft axis x at z = 0
    y_s: float         # jackshaft axis y (negative = right side of the bike)
    z_lo: float        # lower arm height
    z_hi: float        # upper arm height
    r_lo: float        # lower arm length
    r_hi: float        # upper arm length
    b_lo: float        # lower arm angle about the shaft, from pointing right (-y)
    b_hi: float        # upper arm angle about the shaft
    r_f: float         # fork arm length
    b_f: float         # fork arm angle about the fork axis, from pointing right
    z_f: float         # fork arm height

    @property
    def shaft_dir(self):
        a = math.radians(self.lean_deg)
        return unit((math.sin(a), 0.0, math.cos(a)))

    def shaft_point(self, z):
        return np.array([self.x0 + z * math.tan(math.radians(self.lean_deg)), self.y_s, z])

    def lower_joint(self):
        return rotate(self.shaft_point(self.z_lo) + np.array([0, -self.r_lo, 0]),
                      self.shaft_point(self.z_lo), self.shaft_dir, self.b_lo)

    def upper_joint(self):
        return rotate(self.shaft_point(self.z_hi) + np.array([0, -self.r_hi, 0]),
                      self.shaft_point(self.z_hi), self.shaft_dir, self.b_hi)

    def fork_axis_point(self):
        s = (self.z_f - FORK_POINT[2]) / FORK_DIR[2]
        return FORK_POINT + s * FORK_DIR

    def fork_joint(self):
        p = self.fork_axis_point()
        return rotate(p + np.array([0, -self.r_f, 0]), p, FORK_DIR, self.b_f)

    def links(self):
        lower = Linkage(BAR_POINT, BAR_DIR, BAR_JOINT, self.shaft_point(0), self.shaft_dir, self.lower_joint())
        upper = Linkage(self.shaft_point(0), self.shaft_dir, self.upper_joint(), FORK_POINT, FORK_DIR, self.fork_joint())
        return lower, upper


def follow(link, inputs, start_out=0.0):
    """Output angle for each input angle, following one branch continuously."""
    out, prev = {}, start_out
    for a in inputs:
        sols = link.fork_angles(a)
        if not sols:
            return None
        best = min(sols, key=lambda s: abs(((s - prev + 180) % 360) - 180))
        prev = prev + ((best - prev + 180) % 360) - 180
        out[a] = prev
    return out


def push_angle(axis_point, axis_dir, joint, other):
    """Angle between the rod and the way this joint moves. 0 is ideal, 90 is dead centre."""
    motion = np.cross(axis_dir, joint - axis_point)
    return math.degrees(math.acos(min(1.0, abs(np.dot(unit(motion), unit(other - joint))))))


def simulate(d, limit=CHECK_DEG, step=1.0):
    """Rows of (bar, shaft, fork, worst push angle), or None if the linkage locks."""
    lower, upper = d.links()
    rows = []
    for sign in (1, -1):
        bars = [sign * step * i for i in range(int(limit / step) + 1)]
        shaft = follow(lower, bars)
        if shaft is None:
            return None
        fork = follow(upper, [shaft[b] for b in bars])
        if fork is None:
            return None
        for b in bars:
            s, f = shaft[b], fork[shaft[b]]
            j1 = rotate(BAR_JOINT, BAR_POINT, BAR_DIR, b)
            j2 = rotate(d.lower_joint(), d.shaft_point(0), d.shaft_dir, s)
            j3 = rotate(d.upper_joint(), d.shaft_point(0), d.shaft_dir, s)
            j4 = rotate(d.fork_joint(), FORK_POINT, FORK_DIR, f)
            worst = max(push_angle(BAR_POINT, BAR_DIR, j1, j2),
                        push_angle(d.shaft_point(0), d.shaft_dir, j2, j1),
                        push_angle(d.shaft_point(0), d.shaft_dir, j3, j4),
                        push_angle(FORK_POINT, FORK_DIR, j4, j3))
            rows.append((b, s, f, worst))
    return sorted(set(rows))


def penalties(d):
    p = 0.0
    lo, hi = d.lower_joint(), d.upper_joint()
    p += max(0, lo[2] - 10) * 2                 # lower rod stays under the box floor (z 37)
    p += max(0, -140 - lo[2]) * 2               # and keeps some ground clearance
    p += max(0, 45 - abs(d.y_s)) * 5            # shaft clear of the 44.5 mm frame tube
    for z in (d.z_lo, 37, 150, 305, d.z_hi):    # shaft in front of the box wall
        p += max(0, box_wall_x(z) + 25 - d.shaft_point(z)[0]) * 2
    p += max(0, d.shaft_point(d.z_lo)[0] - 575) * 2   # shaft bottom behind the wheel
    p += max(0, 60 - (d.z_hi - d.z_lo) / 4)     # bearings need some spread
    p += max(0, abs(hi[1]) - 170)               # upper joint not far out to the side
    return p


def cost(x):
    d = Design(*x)
    rows = simulate(d, step=2.0)
    if rows is None:
        return 1e4
    err = max(abs(f - b) for b, s, f, w in rows)
    push = max(w for b, s, f, w in rows if abs(b) <= STOP_DEG)
    return err + 0.5 * max(0, push - 25) + penalties(d)


BOUNDS = [
    (0, 26),        # lean_deg
    (470, 600),     # x0
    (-110, -45),    # y_s
    (-130, 10),     # z_lo
    (200, 420),     # z_hi
    (50, 140),      # r_lo
    (40, 140),      # r_hi
    (-60, 60),      # b_lo
    (-90, 90),      # b_hi
    (60, 130),      # r_f
    (-90, 90),      # b_f
    (300, 420),     # z_f
]

if __name__ == "__main__":
    best = differential_evolution(cost, BOUNDS, seed=1, maxiter=300, popsize=30, tol=1e-6, polish=True, workers=1)
    d = Design(*best.x)
    print("cost", round(best.fun, 2))
    for name, v in zip(Design.__dataclass_fields__, best.x):
        print(f"  {name:9s} {v:8.1f}")
    print("joints: bar", np.round(BAR_JOINT, 1), "lower", np.round(d.lower_joint(), 1),
          "upper", np.round(d.upper_joint(), 1), "fork", np.round(d.fork_joint(), 1))
    lower, upper = d.links()
    print(f"rods: lower {lower.rod_length:.1f} mm, upper {upper.rod_length:.1f} mm; penalties {penalties(d):.2f}")
    print(" bar  shaft  fork  worst push angle")
    for b, s, f, w in simulate(d, step=5.0, limit=45) or []:
        print(f"{b:4.0f} {s:6.1f} {f:6.1f} {w:6.1f}")
    np.save("design.npy", best.x)
