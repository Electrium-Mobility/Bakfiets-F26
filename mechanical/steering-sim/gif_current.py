"""GIFs of the steering as modelled in f26bakfiets_main_asm (11 Nov): handlebar arm,
bent rod with a ball joint on both ends, fork arm. The fork turns as far as the two
bumpers on the welded stopper bracket allow (about 38 deg each way).

The rod is free to spin about the line joining its two balls. Here it hangs with its
bend straight down, which is also how the model was saved.
Usage: gif_current.py [close_up side top front_right] [video]"""
import sys
import numpy as np
import pyvista as pv
import render as R
from linkage import rotate, unit
from current_design import CURRENT as L, SAVED_BAR, SAVED_FORK

FORK_STOP = 38.0
children = list(R.C.asm.children)
rod_shape = R.P["f26bakfiets_steering_rod_Default<As_Machined>"]
joints = sorted((c for c in children if c.label == "f26bakfiets_ball_joint"), key=lambda c: c.center().X)
bumpers = [c for c in children if c.label.startswith("9546K431")]

rod0 = R.mesh(rod_shape, 0.3)
bar_joint0, fork_joint0 = R.mesh(joints[0], 0.3), R.mesh(joints[1], 0.3)
fixed = {"stopper bracket": R.base["fork arm"], "bumper 1": R.mesh(bumpers[0], 0.3), "bumper 2": R.mesh(bumpers[1], 0.3)}
FIXED_COLOUR = {"stopper bracket": "#2a6fb0"}
bike = {k: v for k, v in R.base.items() if k != "fork arm"}

# Ball centres and rod centre of mass in the saved position.
B1 = rotate(L.bar_joint0, L.bar_point, L.bar_dir, SAVED_BAR)
B2 = rotate(L.fork_joint0, L.fork_point, L.fork_dir, SAVED_FORK)
c = rod_shape.center()
COM = np.array([c.X, c.Y, c.Z])

rows = L.sweep((-60, 60), 0.25)
bars_list = np.array(list(rows))
forks_list = np.array(list(rows.values()))
BAR_RIGHT = float(np.interp(FORK_STOP, forks_list, bars_list))
BAR_LEFT = float(np.interp(-FORK_STOP, forks_list, bars_list))


def fork_angle(bar):
    return float(np.interp(bar, bars_list, forks_list))


def frame_of(p1, p2, toward):
    """Right-handed axes: x along the rod's ball line, z as near to 'toward' as possible."""
    x = unit(p2 - p1)
    z = unit(toward - x * np.dot(toward, x))
    return np.column_stack([x, np.cross(z, x), z])


def rod_transform(bar, fork):
    """4x4 matrix that carries the rod from its saved position to this steering angle,
    with its centre of mass hanging straight below the ball line."""
    p1 = rotate(L.bar_joint0, L.bar_point, L.bar_dir, bar)
    p2 = rotate(L.fork_joint0, L.fork_point, L.fork_dir, fork)
    old = frame_of(B1, B2, COM - B1)
    new = frame_of(p1, p2, np.array([0.0, 0.0, -1.0]))
    rot = new @ old.T
    m = np.eye(4)
    m[:3, :3] = rot
    m[:3, 3] = p1 - rot @ B1
    return m


def frame(p, bar):
    fork = fork_angle(bar)
    for name, m in bike.items():
        m = m.copy()
        if name == "bars":
            m.rotate_vector(L.bar_dir, bar - SAVED_BAR, point=L.bar_point, inplace=True)
        if name in ("wheel", "fork"):
            m.rotate_vector(L.fork_dir, fork - SAVED_FORK, point=L.fork_point, inplace=True)
        p.add_mesh(m, smooth_shading=True, **R.STYLE[name])
    for name, m in fixed.items():
        p.add_mesh(m, smooth_shading=True, color=FIXED_COLOUR.get(name, "#222222"))
    p.add_mesh(rod0.copy().transform(rod_transform(bar, fork), inplace=True), smooth_shading=True, color="#d62728")
    p.add_mesh(bar_joint0.copy().rotate_vector(L.bar_dir, bar - SAVED_BAR, point=L.bar_point, inplace=True),
               smooth_shading=True, color="#ffd23f")
    p.add_mesh(fork_joint0.copy().rotate_vector(L.fork_dir, fork - SAVED_FORK, point=L.fork_point, inplace=True),
               smooth_shading=True, color="#ffd23f")

    def side(a):
        return "straight" if abs(a) < 0.05 else f"{abs(a):.0f} deg {'right' if a > 0 else 'left'}"
    p.add_text(f"handlebars {side(bar)}\nwheel {side(fork)}", position="upper_left", font_size=13, color="black")


def fork_to_bar(fork):
    return float(np.interp(fork, forks_list, bars_list))


def sweep_angles(step, fork_stop=FORK_STOP):
    """Handlebar angles: straight, to the right stop, to the left stop, back to straight."""
    right, left = fork_to_bar(fork_stop), fork_to_bar(-fork_stop)

    def run(a, b):
        n = max(2, int(round(abs(b - a) / step)) + 1)
        return list(np.linspace(a, b, n))
    return run(0, right) + run(right, left)[1:] + run(left, 0)[1:]


CAMS = {"close_up": [(1150, -1100, -150), (520, -100, 120), (0, 0, 1)],
        "side": [(400, -2400, 250), (400, 0, 200), (0, 0, 1)],
        "top": [(400, 0, 2600), (400, 0, 220), (1, 0, 0)],
        "front_right": [(1500, -1500, 1000), (340, 0, 220), (0, 0, 1)]}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "video"]
    video = "video" in sys.argv[1:]
    print(f"handlebars {BAR_LEFT:.1f} to {BAR_RIGHT:.1f} deg for fork -{FORK_STOP:.0f} to +{FORK_STOP:.0f}", flush=True)
    for g in args or list(CAMS):
        if video:
            p = pv.Plotter(off_screen=True, window_size=(1280, 800))
            p.open_movie(f"videos/current-{g.replace('_', '-')}.mp4", framerate=30, quality=7)
            angles = sweep_angles(1.0)
        else:
            p = pv.Plotter(off_screen=True, window_size=(900, 600))
            p.open_gif(f"views/current_{g}.gif", fps=12)
            angles = sweep_angles(2.5)
        for a in angles:
            p.clear()
            p.set_background("white")
            frame(p, float(a))
            p.camera_position = CAMS[g]
            p.write_frame()
        p.close()
        print("saved", g, len(angles), "frames", flush=True)
