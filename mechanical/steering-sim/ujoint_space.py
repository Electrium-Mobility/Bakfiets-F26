"""Point clouds of the bike parts (straight ahead, plus the wheel and fork swept from
-35 to +35 deg) saved to ujoint_space.npz, for fast clearance estimates with a KD tree."""
import numpy as np
from build123d import import_step
import pyvista as pv
from current_design import CURRENT as L, SAVED_BAR, SAVED_FORK
from render import mesh

asm = import_step("step/f26bakfiets_main_asm.step")
P = {c.label: c for c in asm.children}
names = {"frame": "f26bakfiets_frame_Default<As_Machined>", "box": "f26bakfiets_cargo_box_low_detail",
         "kickstand": "f26bakfiets_kickstand_Default<As_Machined>", "bars": "f26bakfiets_steering_handlebars",
         "wheel": "f26bakfiets_front_wheel", "fork": "f26bakfiets_front_suspension"}


def dense(m, step=2.0):
    """Mesh vertices plus points spread over big triangles, so no gap is over ~step."""
    m = m.triangulate()
    pts = [m.points]
    faces = m.faces.reshape(-1, 4)[:, 1:]
    tri = m.points[faces]
    for k in range(len(tri)):
        a, b, c = tri[k]
        n = int(max(np.linalg.norm(b - a), np.linalg.norm(c - a), np.linalg.norm(c - b)) / step)
        if n > 1:
            u, v = np.meshgrid(np.linspace(0, 1, n + 1), np.linspace(0, 1, n + 1))
            keep = u + v <= 1
            pts.append(a + np.outer(u[keep], b - a) + np.outer(v[keep], c - a))
    return np.vstack(pts)

out = {}
for k in ("frame", "box", "kickstand"):
    out[k] = dense(mesh(P[names[k]], 1.0))
bars0 = mesh(P[names["bars"]], 1.0)
bars0.rotate_vector(L.bar_dir, -SAVED_BAR, point=L.bar_point, inplace=True)
out["bars0"] = dense(bars0)
for k in ("wheel", "fork"):
    m0 = mesh(P[names[k]], 1.5)
    m0.rotate_vector(L.fork_dir, -SAVED_FORK, point=L.fork_point, inplace=True)
    out[k + "0"] = dense(m0)
np.savez_compressed("ujoint_space.npz", **out)
print({k: len(v) for k, v in out.items()})
