"""Gap check for the cable steering: every new part against every bike part and every
other new part, from 35 deg left to 35 deg right. Steering is 1:1, so the fork turns
as far as the bars. Prints DONE at the end; a log without it was cut off."""
import time
import itertools
import jackshaft_check as C
import cable as K
from build123d import Axis
from current_design import SAVED_BAR, SAVED_FORK

t0 = time.time()
bar_axis = Axis(tuple(K.BAR_POINT), tuple(K.BAR_DIR))
fork_axis = Axis(tuple(K.FORK_POINT), tuple(K.FORK_DIR))
moving_labels = {"f26bakfiets_steering_handlebars": ("bars", bar_axis, SAVED_BAR),
                 "f26bakfiets_front_wheel": ("wheel", fork_axis, SAVED_FORK),
                 "f26bakfiets_front_suspension": ("fork", fork_axis, SAVED_FORK)}
static = {}
OLD_STEERING = ("steering_rod", "ball_joint",   # the linkage the cables replace
                "Part1", "9546K431")           # old stopper bracket and bumpers, removed
for c in C.asm.children:
    if c.label not in moving_labels and not any(o in c.label for o in OLD_STEERING):
        static[c.label.replace("f26bakfiets_", "").split("_Default")[0]] = c
print("bike parts held still:", sorted(static), flush=True)

# Pairs touching on purpose.
MOUNTED = {("bar disc", "bars"), ("bar spacers", "bars"), ("fork disc", "fork"),
           ("bar bracket", "frame"), ("fork bracket", "frame")}


def touching_on_purpose(a, b):
    pair = {a, b}
    if pair == {"bar spacers", "bar disc"}:
        return True
    for side in ("left", "right"):
        for end in ("bar", "fork"):
            cable, stop = f"{side} cable, {end}", f"{side} stop, {end}"
            if pair in ({cable, f"{end} disc"}, {cable, stop}, {stop, f"{end} bracket"}, {stop, f"{side} housing"}):
                return True
    return False


STATIC_NEW = {"bar bracket", "fork bracket"} | {f"{s} stop, {e}" for s in ("left", "right") for e in ("bar", "fork")} \
    | {f"{s} cable, {e}" for s in ("left", "right") for e in ("bar", "fork")} | {"left housing", "right housing"} \
    | {"bar disc"}   # round outside (only holes cut in it), so the same at every angle; the fork disc has the stop tab
worst = {}


def note(k, g, a):
    if g < worst.get(k, (1e9,))[0]:
        worst[k] = (g, a)


for a in range(-35, 36, 5):
    p = K.build_all(a, a, mark=False)
    bike = dict(static)
    for label, (name, axis, saved) in moving_labels.items():
        part = next(c for c in C.asm.children if c.label == label)
        bike[name] = part.rotate(axis, a - saved)
    for name, part in p.items():
        for bn, b in bike.items():
            if (name, bn) in MOUNTED:
                continue
            if name in STATIC_NEW and bn in static and a != 0:
                continue                      # both still: checking once is enough
            note((name, bn), part.distance_to(b), a)
    for n1, n2 in itertools.combinations(p, 2):
        if touching_on_purpose(n1, n2) or (n1 in STATIC_NEW and n2 in STATIC_NEW and a != 0):
            continue
        note((n1, n2), p[n1].distance_to(p[n2]), a)
    print(f"checked {a:+d} [{time.time()-t0:.0f} s]", flush=True)
print("smallest gaps (mm, at steering angle):")
for (x, y), (g, a) in sorted(worst.items(), key=lambda kv: kv[1][0])[:80]:
    print(f"  {x} / {y}: {g:.1f} at {a:+d}")
print("DONE")
