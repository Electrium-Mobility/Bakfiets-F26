"""Where the fork disc's stop tab meets the fork bracket, and its gaps on the way there."""
import cable as K
from build123d import Axis
fb = K.fork_bracket()
p0 = K.build_all(0, 0, mark=False)
others = {n: p0[n] for n in ("left stop, fork", "right stop, fork", "left cable, fork", "right cable, fork", "left housing", "right housing")}
ax = Axis(tuple(K.FORK_POINT), tuple(K.FORK_DIR))
extras0 = K.fork_disc_extras()
for sign in (1, -1):
    contact = None
    for a in range(0, 46):
        e = extras0.rotate(ax, sign * a)
        g = e.distance_to(fb)
        if a in (0, 30, 35) or (contact is None and g < 0.05):
            og = min(e.distance_to(o) for o in others.values())
            print(f"{'right' if sign > 0 else 'left'} {a:2d} deg: hub and tab to fork bracket {g:5.1f} mm, to stops/cables/housings {og:5.1f} mm")
        if g < 0.05 and contact is None:
            contact = a
            break
    print("  stop meets the bracket at", contact, "deg")
