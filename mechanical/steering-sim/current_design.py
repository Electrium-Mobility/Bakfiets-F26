"""Sweeps the steering as modelled in f26bakfiets_main_asm (11 Nov), from true straight ahead.
Annie saved the model turned left: handlebars -34.2 deg, fork -40.9 deg."""
from linkage import Linkage, rotate
import numpy as np

SAVED_BAR, SAVED_FORK = -34.2, -40.9
L = Linkage(
    bar_point=(-4.0, 0.0, 332.0), bar_dir=(0.012, 0.0, -1.0), bar_joint=(61.8, -90.1, -37.3),
    fork_point=(693.5, 0.0, 444.5), fork_dir=(0.468, 0.0, -0.884), fork_joint=(814.2, -55.0, 374.7),
)
# Move both joints to the straight-ahead position.
L.bar_joint0 = rotate(L.bar_joint0, L.bar_point, L.bar_dir, -SAVED_BAR)
L.fork_joint0 = rotate(L.fork_joint0, L.fork_point, L.fork_dir, -SAVED_FORK)
CURRENT = L

if __name__ == "__main__":
    gap = np.linalg.norm(L.fork_joint0 - L.bar_joint0) - 858.5
    print(f"rod length check at straight ahead: off by {gap:.1f} mm")
    print("straight-ahead joints:", np.round(L.bar_joint0, 1), np.round(L.fork_joint0, 1))
    rows = L.sweep((-120, 120), 1.0)
    print(f"handlebars reach {min(rows):.0f} to {max(rows):.0f} deg before the linkage locks (sweep stops at 120)")
    print(" bar   fork   transmission")
    for bar, fork in rows.items():
        if bar % 10 == 0 or bar in (min(rows), max(rows)):
            print(f"{bar:5.0f} {fork:6.1f} {L.transmission_angle(bar, fork):8.1f}")
