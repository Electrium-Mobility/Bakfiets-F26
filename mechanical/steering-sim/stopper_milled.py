"""Milled steering stopper for the bent-rod steering (f26bakfiets_main_asm, 11 Nov).
It replaces the welded strip (Part1) with three plain aluminium parts:

- Clamp block: 20 mm plate, square to the steering axis on the bare top of the head
  tube. Two straight arms from the bore, one to each bar. Bored to the head tube, slit
  on the left, closed by two M6 pinch bolts. A square pocket under each arm end takes a bar.
- Two stop bars: 1 in square bar, sawn to length. Two M6 tapped holes in the top end
  (bolts come down through the block), one M6 tapped hole in the side for a bumper.
- The same two M6 stud bumpers (McMaster 9546K431).

The fork arm meets a bumper at 35 deg of fork turn either way.
Coordinates as in stopper.py: local x forward, y left, z up the steering axis.
"""
import numpy as np
from build123d import Cylinder, Polygon, extrude, Location
from scipy.spatial import ConvexHull
import stopper as S
from stopper import box, cyl, plane, bumpers, mount, HEAD_TUBE_R, STOP_DEG

BLOCK_LO, BLOCK_HI = 35, 55     # block faces, up the axis. The head tube top is 68.3 up; the
                                # down tube weld reaches 33 (block overlaps it below 34). Top face
                                # 13.3 below the head tube top, clear of the upper headset cup
BORE_WALL = 9                   # block material round the bore
BAR = 25.4                      # 1 in square bar
POCKET = 10                     # bars sit this deep in the block
MARGIN = 8                      # block material round the pockets
BAR_BELOW = 9                   # bar ends this far below the bumper's centre: covers its 14.6 mm
                                # mounting face; any longer and the rod hits the rear bar turning left
BUMP_HOLE = 12                  # depth of the M6 bumper hole
BOLT_SPREAD = 6.5               # bar bolts this far each side of the bar's centre
LUG_W, LUG_TO = 28, 58          # pinch lug width and how far left it reaches
PINCH_Y = (36, 50)              # two M6 pinch bolts side by side, left of the axis


def bar_frame(m, n):
    """Bar axes in the plane square to the steering axis: n out of the bumper's
    face into the bar, w across it."""
    w = np.array([-n[1], n[0], 0.0])
    return n, w


def bar_corners(m, n, grow=0.0):
    n, w = bar_frame(m, n)
    c = np.array([m[0], m[1], 0.0])
    return [c + n * a + w * b for a in (-grow, BAR + grow) for b in (-BAR / 2 - grow, BAR / 2 + grow)]


def bar_solid(m, n, z_lo, z_hi, grow=0.0):
    corners = bar_corners(m, n, grow)
    order = [corners[0], corners[1], corners[3], corners[2]]
    return prism([(p[0], p[1]) for p in order], z_lo, z_hi)


def prism(outline, z_lo, z_hi):
    """Straight prism from a 2D outline, always extruded up (+z) whichever way the outline runs."""
    face = Polygon(*outline, align=None).moved(Location((0, 0, z_lo)))
    return extrude(face, z_hi - z_lo, dir=(0, 0, 1))


def boss_outline():
    corner_r = (HEAD_TUBE_R + BORE_WALL) / np.cos(np.radians(22.5))     # octagon round the bore
    return [(np.cos(a) * corner_r, np.sin(a) * corner_r) for a in np.radians(np.arange(22.5, 360, 45))]


def arm_outline(m, n):
    """Straight-edged arm: convex hull of the boss octagon and one pocket with its margin.
    Its far end runs parallel to the pocket sides, so the pocket squares off that edge."""
    pts = np.array(boss_outline() + [(p[0], p[1]) for p in bar_corners(m, n, MARGIN)])
    return [tuple(p) for p in pts[ConvexHull(pts).vertices]]


def parts(asm, local=False):
    """Returns dict of name -> solid, plus the turned bumpers. Solids are in bike
    coordinates, or in the local frame (bore centre, axis up) if local is True."""
    pl = plane()
    bump = bumpers(asm)
    mounts = [mount(b) for b in bump]

    # Block: two arms from the bore boss, one to each pocket, plus the pinch lug.
    block = prism(arm_outline(*mounts[0]), BLOCK_LO, BLOCK_HI)
    block = block.fuse(prism(arm_outline(*mounts[1]), BLOCK_LO, BLOCK_HI))
    block = block.fuse(box((-LUG_W / 2, 0, BLOCK_LO), (LUG_W / 2, LUG_TO, BLOCK_HI)))       # pinch lug, left
    block = block.cut(Cylinder(HEAD_TUBE_R, 60, align=None).moved(Location((0, 0, BLOCK_LO - 10))))
    block = block.cut(box((-0.75, 0, BLOCK_LO - 1), (0.75, LUG_TO + 1, BLOCK_HI + 1)))     # slit
    zc = (BLOCK_LO + BLOCK_HI) / 2
    for y in PINCH_Y:                                       # M6 pinch bolts: clearance behind the slit, tapped ahead
        block = block.cut(cyl((-LUG_W, y, zc), (0, y, zc), 6.4))
        block = block.cut(cyl((0, y, zc), (LUG_W, y, zc), 5.0))

    out = {"stopper block": None}
    for i, (m, n) in enumerate(mounts):
        nn, w = bar_frame(m, n)
        z_lo = m[2] - BAR_BELOW
        bar = bar_solid(m, n, z_lo, BLOCK_LO + POCKET)
        bar = bar.cut(cyl(m - nn, m + nn * BUMP_HOLE, 5.0))                                 # M6 tap drill
        block = block.cut(bar_solid(m, n, BLOCK_LO - 1, BLOCK_LO + POCKET, grow=0.05))      # pocket
        for c in bar_bolts(m, n):
            block = block.cut(cyl((c[0], c[1], BLOCK_LO), (c[0], c[1], BLOCK_HI + 1), 6.4))   # M6 clearance
            bar = bar.cut(cyl((c[0], c[1], BLOCK_LO + POCKET - 15), (c[0], c[1], BLOCK_LO + POCKET + 1), 5.0))
        out[f"stop bar {'front' if i == 0 else 'rear'}"] = bar if local else pl * bar
    out["stopper block"] = block if local else pl * block
    return out, bump


def bar_bolts(m, n):
    """Two bolts down through the block into the bar's top end, spread along the
    bumper's push so they resist the bar tipping."""
    nn, w = bar_frame(m, n)
    centre = np.array([m[0], m[1], 0]) + nn * BAR / 2
    return [centre + nn * s * BOLT_SPREAD for s in (1, -1)]


if __name__ == "__main__":
    from build123d import import_step, export_step, export_stl
    asm = import_step("step/f26bakfiets_main_asm.step")
    made, bump = parts(asm)
    for name, part in made.items():
        bb = part.bounding_box()
        print(f"{name}: {part.volume / 1000:.0f} cm3, {len(part.solids())} solid(s), valid {part.is_valid}")
        export_step(part, f"step/{name.replace(' ', '_')}.step")
    # Test-print copies, flat on the bed (local frame), to check the fit on the bike first.
    for name, part in parts(asm, local=True)[0].items():
        export_stl(part, f"step/print/{name.replace(' ', '_')}.stl", tolerance=0.05)
    pl = plane()
    for i, (m, n) in enumerate(mount(b) for b in bump):
        print(f"bar {i}: length {BLOCK_LO + POCKET - (m[2] - BAR_BELOW):.1f} mm, bumper hole "
              f"{BLOCK_LO + POCKET - m[2]:.1f} mm from the top end")
