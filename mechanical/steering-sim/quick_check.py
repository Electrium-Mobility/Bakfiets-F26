"""Quick check of the parts near the fork crown and the stop, at the angles that matter."""
import jackshaft as J
import jackshaft_check as C
import offshelf as O
d = C.d
rows = {round(b): (s, f) for b, s, f, w in J.simulate(d, step=1.0, limit=J.STOP_DEG)}
for bar in (-35, -33, -30, 0, 30, 33, 35):
    s, f = rows[bar]
    p = O.build(d, bar, s, f)
    new, turned = C.parts_at(bar, s, f)
    out = [f"bars {bar:+3d}: stop pin to A {p['stop pin'].distance_to(p['stop A']):4.1f} B {p['stop pin'].distance_to(p['stop B']):4.1f}"]
    for a in ("upper u-bolts", "upper plate", "upper bearing"):
        out.append(f"{a}/fork {p[a].distance_to(turned['fork']):5.1f}")
    for a in ("upper rod", "upper arm", "ball 3"):
        out.append(f"{a}/upper parts {min(new[a].distance_to(p[k]) for k in ('upper plate','upper bearing','upper u-bolts')):5.1f}")
    print("  ".join(out), flush=True)
p = O.build(d, 0, *rows[0])
for a in ("stop A", "stop B", "lower plate", "lower bearing", "upper plate", "upper bearing", "upper u-bolts"):
    print(f"{a} to box {p[a].distance_to(C.box):.1f}, to frame {p[a].distance_to(C.frame):.1f}", flush=True)
