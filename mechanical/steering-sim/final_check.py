"""Final gap check on the off-the-shelf parts exactly as drawn, including each rod
against its own arm (the rod end's eye, ball and bolt sit on the arm on purpose, so
only the shank and the threaded rod are tested there)."""
import time
import jackshaft as J
import jackshaft_check as C
import offshelf as O

t0 = time.time()
d = C.d
rows = {round(b): (s, f) for b, s, f, w in J.simulate(d, step=1.0, limit=J.STOP_DEG)}
fixed_parts = ["lower plate", "lower bearing", "lower u-bolts", "upper plate", "upper bearing", "upper u-bolts", "stop A", "stop B"]
moving = ["shaft", "lower hub", "lower arm", "upper hub", "upper arm", "lower rod", "upper rod", "stop collar", "stop pin",
          "bar spacer", "fork bracket", "lower washer", "upper washer", "bar washer", "fork washer", "lower bolts", "upper bolts"]
skip = {("bar spacer", "kickstand"), ("fork bracket", "fork"), ("fork washer", "fork"), ("upper bolts", "fork")}
worst = {}


def note(k, g, bar):
    if g < worst.get(k, (1e9,))[0]:
        worst[k] = (g, bar)


p0 = O.build(d, 0, *rows[0])
for n in fixed_parts:
    note((n, "box"), p0[n].distance_to(C.box), 0)
for bar in range(-35, 36, 5):
    s, f = rows[bar]
    p = O.build(d, bar, s, f)
    _, turned = C.parts_at(bar, s, f)
    obstacles = {"frame": C.frame, "box": C.box, "kickstand": C.kickstand, "wheel": turned["wheel"], "fork": turned["fork"]}
    for n in moving:
        for on, o in obstacles.items():
            if (n, on) in skip or (n.startswith("bar") and on == "frame"):
                continue
            note((n, on), p[n].distance_to(o), bar)
    for n in fixed_parts:
        for on in ("wheel", "fork"):
            note((n, on), p[n].distance_to(obstacles[on]), bar)
    for n in ("lower arm", "upper arm", "lower hub", "upper hub", "lower rod", "upper rod", "stop pin", "fork bracket"):
        for m in fixed_parts:
            if n == "stop pin" and m.startswith("stop"):
                continue
            note((n, m), p[n].distance_to(p[m]), bar)
    # each rod against its own arm, hub and bracket: children are
    # [eye, ball, shank] for the first end, the same for the second, then the rod
    for rod, mounts in (("lower rod", ("lower arm", "lower hub")), ("upper rod", ("upper arm", "upper hub", "fork bracket"))):
        kids = p[rod].children
        for pname, piece in (("shank 1", kids[2]), ("shank 2", kids[5]), ("threaded rod", kids[6])):
            for m in mounts:
                note((f"{rod} {pname}", m), piece.distance_to(p[m]), bar)
    print(f"checked {bar:+d} [{time.time()-t0:.0f} s]", flush=True)
for (a, b), (g, bar) in sorted(worst.items(), key=lambda kv: kv[1][0])[:16]:
    print(f"  {a} / {b}: {g:.1f} mm at {bar:+d}")
