"""STL files for the printed cable steering parts, straight ahead, placed on the build
plate. Discs lie flat; the handlebar bracket splits through its clamp into two pieces."""
import os
import sys
import numpy as np
import pyvista as pv
from build123d import Plane, Box, Location, export_stl
import cable as K

out_dir = sys.argv[1] if len(sys.argv) > 1 else "step/print"
os.makedirs(out_dir, exist_ok=True)
p = K.build_all(0, 0, mark=False)


def on_plate(shape):
    """Moves a shape so it sits on z = 0, centred on x and y."""
    bb = shape.bounding_box()
    return shape.moved(Location((-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z)))


parts = {}
# Discs: their own axis becomes z. The fork disc prints hub down, so the disc above
# the hub needs supports under its rim; the stop tab ends up on top.
bar_pl = Plane(origin=tuple(K.BAR_DISC), z_dir=tuple(-K.BAR_DIR))
parts["handlebar disc"] = on_plate(bar_pl.to_local_coords(p["bar disc"]))
fork_pl = Plane(origin=tuple(K.FORK_DISC), x_dir=tuple(K.in_plane(K.X, -K.FORK_DIR)), z_dir=tuple(-K.FORK_DIR))
parts["fork disc"] = on_plate(fork_pl.to_local_coords(p["fork disc"]))
# Handlebar bracket: split through the main tube clamp at z = 0
bb = p["bar bracket"]
big = 400
lower = bb.cut(Box(big, big, big, align=None).moved(Location((-big / 2, -big / 2, 0))))
upper = bb.cut(Box(big, big, big, align=None).moved(Location((-big / 2, -big / 2, -big))))
parts["handlebar bracket, lower"] = on_plate(lower)
parts["handlebar bracket, clamp cap"] = on_plate(upper)
# Fork bracket in its own frame: base plate flat on the build plate
fb_pl = Plane(origin=tuple(K.FORK_POINT), x_dir=tuple(K.in_plane(K.X, -K.FORK_DIR)), z_dir=tuple(-K.FORK_DIR))
parts["fork bracket"] = on_plate(fb_pl.to_local_coords(p["fork bracket"]))

for name, shape in parts.items():
    path = os.path.join(out_dir, name + ".stl")
    export_stl(shape, path, tolerance=0.02, angular_tolerance=0.1)
    m = pv.read(path).clean(tolerance=1e-4)            # merge seam vertices so the mesh is closed
    m.save(path, binary=True)
    assert m.n_open_edges == 0 and m.is_manifold, name
    bb = shape.bounding_box()
    print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, {shape.volume / 1000:.1f} cm3, valid {shape.is_valid}")
