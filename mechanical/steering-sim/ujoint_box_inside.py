"""Marks which 5 mm grid points lie inside the cargo box solid (the point clouds only see
its surface), saved to ujoint_box_inside.npz for the layout search."""
import numpy as np
import pyvista as pv
from build123d import import_step
from render import mesh
asm = import_step("step/f26bakfiets_main_asm.step")
box = [c for c in asm.children if c.label == "f26bakfiets_cargo_box_low_detail"][0]
m = mesh(box, 1.0).triangulate().clean()
print("closed:", m.n_open_edges == 0, "open edges", m.n_open_edges)
xs, ys, zs = np.arange(0, 620, 5.0), np.arange(-230, 231, 5.0), np.arange(30, 425, 5.0)
g = np.stack(np.meshgrid(xs, ys, zs, indexing="ij"), -1).reshape(-1, 3)
sel = pv.PolyData(g).select_enclosed_points(m, check_surface=False)
inside = sel["SelectedPoints"].astype(bool).reshape(len(xs), len(ys), len(zs))
np.savez_compressed("ujoint_box_inside.npz", inside=inside, x0=xs[0], y0=ys[0], z0=zs[0], step=5.0)
print("inside fraction", inside.mean())
for z in (100, 200, 300):
    k = int((z - zs[0]) / 5)
    j = int((-100 - ys[0]) / 5)
    row = inside[:, j, k]
    print(f"z {z}, y -100: inside x from {xs[row].min() if row.any() else None} to {xs[row].max() if row.any() else None}")
