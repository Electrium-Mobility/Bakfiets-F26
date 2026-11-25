"""U-joint steering (from a sketch): fixed geometry, joint sizes and layout cases.

Chain, handlebars to fork (x forward, y left, z up, mm; straight ahead):
  handlebar post -> UJ1 under the post -> S1, long and level, forward under the main tube
  -> UJ2 -> S2, short -> UJ3 -> S3, long, up beside the frame's front (down) tube
  -> UJ4 above the head tube -> S4, short -> UJ5 on the fork steerer top.
The handlebar arm at the post bottom is cut off (as the sketch says).

Bought joints assumed: DIN 808 size 42, 20 mm bore (e.g. DIN808-42-B20-82-EG):
42 mm across, 82 mm long, so each yoke reaches 41 mm from the cross centre. A double
joint of the same size is taken as 124 mm long (two crosses 42 mm apart): an assumption.
Shafts 20 mm round bar. Ratings used: single 35 deg, double 70 deg (Borgeson steering
joint listings).
"""
import math
import numpy as np
from linkage import unit
from current_design import CURRENT as L

BAR_POINT, BAR_DIR = L.bar_point, L.bar_dir          # both axis directions point down
FORK_POINT, FORK_DIR = L.fork_point, L.fork_dir
UJ_R, YOKE = 21.0, 41.0         # joint body radius, cross centre to yoke end
SHAFT_R = 10.0
DOUBLE_GAP = 42.0               # cross to cross in a double joint
SINGLE_LIMIT, DOUBLE_LIMIT = 35.0, 70.0
POST_END_Z = -61.2              # bottom of the handlebar post once the arm is cut off
STEERER_TOP = 105.0             # CAD steerer top, mm up the fork axis from FORK_POINT
STUB = 20.0                     # adapter stub from the steerer top to the yoke end


def post_point(z):
    t = (z - BAR_POINT[2]) / BAR_DIR[2]
    return BAR_POINT + BAR_DIR * t


def fork_up(s):
    return FORK_POINT - FORK_DIR * s


A = post_point(POST_END_Z - YOKE)                     # UJ1 centre for a single joint


def bend(u, v):
    return math.degrees(math.acos(np.clip(np.dot(unit(u), unit(v)), -1, 1)))


REACH = {"single": YOKE, "double": YOKE + DOUBLE_GAP / 2, "gearbox": 35.0}
LIMIT = {"single": SINGLE_LIMIT, "double": DOUBLE_LIMIT, "gearbox": 90.0}
CASES = {
    # the simpler drawing: two joints at the corner, two at the top
    "sketch": dict(kinds=["single"] * 5, a_z=A[2]),
    # the first drawing: three joints at the top (short level rod, then a rod down to the fork)
    "sketch3": dict(kinds=["single"] * 6, a_z=A[2]),
    # gearbox under the post, S1 under the (moved) kickstand cross piece, doubles at the top
    "fixed2": dict(kinds=["gearbox", "single", "single", "double", "double"], a_z=-122.0),
    "fixed3": dict(kinds=["gearbox", "single", "single", "double", "double", "double"], a_z=-122.0),
}


def unpack(x, case):
    """Joint centres from search variables x: B (x, y) level with A, then (x, y, z) each."""
    pts = [post_point(case["a_z"]), np.array([x[0], x[1], case["a_z"]])]
    rest = x[2:]
    for i in range(0, len(rest), 3):
        pts.append(np.array(rest[i:i + 3]))
    pts.append(fork_up(STEERER_TOP + STUB + REACH[case["kinds"][-1]]))
    return pts


def flows_n(pts):
    """Flow direction of every shaft: post (down), S1, S2, ..., steerer (down)."""
    return [BAR_DIR] + [unit(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)] + [FORK_DIR]
