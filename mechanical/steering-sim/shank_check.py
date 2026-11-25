"""Rod end shanks and threaded rods against the tabs and brackets they bolt to."""
import jackshaft as J
import jackshaft_check as C
import offshelf as O
d = C.d
worst = {}
for b, s, f, w in J.simulate(d, step=2.5, limit=J.STOP_DEG):
    p = O.build(d, b, s, f)
    lk, uk = p["lower rod"].children, p["upper rod"].children
    pairs = {"lower shank / bottom arm": (lk[5], p["lower arm"]), "lower rod / bottom arm": (lk[6], p["lower arm"]),
             "upper shank / top arm": (uk[2], p["upper arm"]), "upper rod / top arm": (uk[6], p["upper arm"]),
             "upper shank / fork bracket": (uk[5], p["fork bracket"]), "upper rod / fork bracket": (uk[6], p["fork bracket"]),
             "upper rod / top hub": (uk[6], p["upper hub"])}
    for k, (a, o) in pairs.items():
        g = a.distance_to(o)
        if g < worst.get(k, (1e9,))[0]:
            worst[k] = (g, b)
for k, (g, b) in sorted(worst.items(), key=lambda kv: kv[1][0]):
    print(f"  {k}: {g:.1f} mm at {b:+.1f}")
# top arm against the upper bearing parts
w = 1e9
for b, s, f, _ in J.simulate(d, step=5.0, limit=J.STOP_DEG):
    p = O.build(d, b, s, f)
    w = min(w, min(p["upper arm"].distance_to(p[k]) for k in ("upper plate", "upper bearing", "upper u-bolts")))
print(f"  top arm / upper bearing parts: {w:.1f} mm")
