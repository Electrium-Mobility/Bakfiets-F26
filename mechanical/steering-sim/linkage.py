"""Kinematics of the Bakfiets steering: handlebar arm -> rod -> fork arm.

The handlebar and fork turn about two different axes. A rod with a ball joint at
each end links an arm on each. For a handlebar angle, the fork angle is the one
that keeps the rod at its fixed length. All lengths in mm, angles in degrees.
"""
import math
import numpy as np

def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)

def rotate(p, axis_point, axis_dir, deg):
    """Rotates point p about the axis (Rodrigues' formula)."""
    k = unit(axis_dir)
    v = np.asarray(p, float) - axis_point
    t = math.radians(deg)
    v_rot = v * math.cos(t) + np.cross(k, v) * math.sin(t) + k * np.dot(k, v) * (1 - math.cos(t))
    return axis_point + v_rot

class Linkage:
    def __init__(self, bar_point, bar_dir, bar_joint, fork_point, fork_dir, fork_joint):
        self.bar_point, self.bar_dir = np.asarray(bar_point, float), unit(bar_dir)
        self.fork_point, self.fork_dir = np.asarray(fork_point, float), unit(fork_dir)
        self.bar_joint0 = np.asarray(bar_joint, float)
        self.fork_joint0 = np.asarray(fork_joint, float)
        self.rod_length = np.linalg.norm(self.fork_joint0 - self.bar_joint0)

    def arm_length(self, joint, point, direction):
        v = joint - point
        return np.linalg.norm(v - direction * np.dot(v, direction))

    def fork_angles(self, bar_deg):
        """Both fork angles that fit the rod length, or [] if none (past dead centre).

        The joint on the fork moves on a circle: c + a cos(t) + b sin(t).
        The rod length condition gives A cos(t) + B sin(t) = C."""
        p1 = rotate(self.bar_joint0, self.bar_point, self.bar_dir, bar_deg)
        k = self.fork_dir
        v = self.fork_joint0 - self.fork_point
        axial = k * np.dot(k, v)
        a = v - axial
        b = np.cross(k, a)
        c = self.fork_point + axial
        d = c - p1
        # |d + a cos t + b sin t|^2 = L^2, with a.b = 0 and |a| = |b| = r
        r2 = np.dot(a, a)
        A, B = 2 * np.dot(d, a), 2 * np.dot(d, b)
        C = self.rod_length ** 2 - np.dot(d, d) - r2
        R = math.hypot(A, B)
        if R == 0 or abs(C) > R:
            return []
        base = math.atan2(B, A)
        spread = math.acos(C / R)
        return [math.degrees(base + spread), math.degrees(base - spread)]

    def transmission_angle(self, bar_deg, fork_deg):
        """Angle between the rod and the direction the fork joint moves.
        0 means the rod pushes straight along the arm's path (best);
        90 means it pushes along the arm and the linkage is at dead centre."""
        p1 = rotate(self.bar_joint0, self.bar_point, self.bar_dir, bar_deg)
        p2 = rotate(self.fork_joint0, self.fork_point, self.fork_dir, fork_deg)
        motion = np.cross(self.fork_dir, p2 - self.fork_point)
        rod = p2 - p1
        cosang = abs(np.dot(unit(motion), unit(rod)))
        return math.degrees(math.acos(min(1.0, cosang)))

    def sweep(self, bar_range=(-90, 90), step=1.0):
        """Follows the fork angle continuously from straight ahead in both directions."""
        rows = {0.0: 0.0}
        for direction in (1, -1):
            prev = 0.0
            deg = 0.0
            while True:
                deg += direction * step
                if abs(deg) > max(abs(bar_range[0]), abs(bar_range[1])):
                    break
                sols = self.fork_angles(deg)
                if not sols:
                    break
                fork = min(sols, key=lambda s: abs(((s - prev + 180) % 360) - 180))
                fork = prev + ((fork - prev + 180) % 360) - 180
                rows[deg] = fork
                prev = fork
        return dict(sorted(rows.items()))
