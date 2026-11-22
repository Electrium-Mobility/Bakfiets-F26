"""Saves the new parts, riding straight, as one STEP file to open in SolidWorks."""
from build123d import Compound, export_step
import jackshaft as J
import jackshaft_check as C
import offshelf as O

rows = {round(b): (s, f) for b, s, f, w in J.simulate(C.d, step=1.0, limit=J.STOP_DEG)}
parts = O.build(C.d, 0, *rows[0])
for name, shape in parts.items():
    shape.label = name
export_step(Compound(children=list(parts.values())), "step/offshelf_parts.step")
print("saved", len(parts), "parts:", ", ".join(parts))
