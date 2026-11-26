"""
Bakfiets F26 rear light - 4 printed parts, all PETG, no TPU.
  body     rectangular channel for one 36-LED WS2813B 144/m piece, with the tube saddle
           built into its back
  lid      clear diffuser, slides in from the open end
  end-cap  flush cap, press-fit prongs, cable notch (seal with silicone)
  clamp    closes on the seat tube with 4 x M3 x 10 + 4 x M3 nuts
Exports STL already oriented for printing.
"""
import math
from pathlib import Path
import cadquery as cq

LEDS, PITCH = 36, 1000 / 144
STRIP_W, STRIP_H, STANDOFF = 12.0, 2.0, 7.0
SIDE_CLR, END_CLR, END_SPACE = 0.5, 1.0, 6.0
WALL, FLOOR, EDGE_R = 2.4, 2.4, 1.0
LID_T, GROOVE_DEPTH, GROOVE_CLR, LID_CLR, LIP = 1.2, 1.0, 0.35, 0.2, 1.0
CAP_T, PRONG_L, PRONG_T, FIT, RIB_H = 3.0, 6.0, 1.2, 0.15, 0.3
CABLE_W, CABLE_H = 4.5, 4.0
TUBE_D, TILT, BORE_CLR, SPLIT_GAP = 28.6, 17.0, 0.2, 1.0
CLAMP_WALL, TOP_T = 5.0, 6.0
# M3 x 10 socket head: 3.5 cap + 1.0 gap + 2.5 saddle + 2.4 nut = 9.4, so a 10 mm screw goes fully through the nut
M3_CLR, M3_HEAD_D, M3_NUT_AF, M3_NUT_T, CAP_BOSS, NUT_DEPTH = 3.4, 6.2, 5.6, 2.6, 3.5, 2.5
SCREW_Y = 4.5          # 2 screws each side of the tube, at +/- this along the tube

strip_len = LEDS * PITCH
in_w = STRIP_W + 2 * SIDE_CLR
cav_h = STRIP_H + STANDOFF
out_w = in_w + 2 * WALL
out_h = FLOOR + cav_h + LID_T + GROOVE_CLR + LIP
in_len = strip_len + 2 * END_CLR + END_SPACE
out_len = WALL + in_len
x_mid = out_len / 2
t = math.radians(TILT)
bore_r = TUBE_D / 2 + BORE_CLR
bolt_x = bore_r + 1.5 + M3_CLR / 2 + 0.8
half_w = bolt_x + M3_HEAD_D / 2 + 1.5
blk_h = bore_r + CLAMP_WALL
z_tube = -(TOP_T + bore_r / math.cos(t) + (out_w / 2) * math.tan(t))


def box(x, y, z, at=(0, 0, 0), c=(False, True, False)):
    return cq.Workplane("XY").box(x, y, z, centered=c).translate(at)


def tilt(s):
    return s.rotate((0, 0, 0), (1, 0, 0), TILT).translate((x_mid, 0, z_tube))


def body():
    b = box(out_len, out_w, out_h).edges("|X").fillet(EDGE_R)
    b = b.cut(box(in_len + 1, in_w, out_h, at=(WALL, 0, FLOOR)))
    b = b.cut(box(in_len + 1, in_w + 2 * GROOVE_DEPTH, LID_T + GROOVE_CLR, at=(WALL, 0, FLOOR + cav_h)))
    # saddle on the back, same width as the body
    s = box(2 * half_w, out_w, 80, at=(x_mid, 0, -80 + 0.01), c=(True, True, False)).edges("|Y").fillet(3.0)
    s = s.intersect(tilt(box(2 * half_w + 20, 200, 200, at=(0, 0, SPLIT_GAP / 2), c=(True, True, False))))
    s = s.cut(tilt(cq.Workplane("XZ").circle(bore_r).extrude(100, both=True)))
    for sx in (1, -1):
        for sy in (1, -1):
            nz = SPLIT_GAP / 2 + NUT_DEPTH
            x, y = sx * bolt_x, sy * SCREW_Y
            cut = (cq.Workplane("XY").circle(M3_CLR / 2).extrude(12).translate((x, y, 0))
                   .union(cq.Workplane("XY").polygon(6, M3_NUT_AF / math.cos(math.pi / 6)).extrude(M3_NUT_T)
                          .translate((x, y, nz)))
                   .union(box(half_w, M3_NUT_AF, M3_NUT_T, at=(x if sx > 0 else x - half_w, y, nz))))
            s = s.cut(tilt(cut))
    return b.union(s)


def lid():
    return box(in_len - 0.3, in_w + 2 * GROOVE_DEPTH - 2 * LID_CLR, LID_T)


def end_cap():
    c = box(CAP_T, out_w, out_h).edges("|X").fillet(EDGE_R)
    ph = cav_h - FIT
    for sy in (1, -1):
        y = sy * (in_w / 2 - FIT - PRONG_T / 2)
        p = box(PRONG_L, PRONG_T, ph, at=(-PRONG_L, y, FLOOR))
        for i in range(2):
            p = p.union(box(1.0, RIB_H, ph, at=(-PRONG_L + 1.5 + i * 2.5, y + sy * (PRONG_T + RIB_H) / 2, FLOOR)))
        c = c.union(p)
    # cable notch, open at the bottom so a cable with its plug on drops in; seal with silicone
    return c.cut(box(CAP_T + PRONG_L + 2, CABLE_W, FLOOR + CABLE_H, at=(-PRONG_L - 1, 0, -0.01)))


def clamp():
    top = blk_h - SPLIT_GAP / 2
    c = box(2 * half_w, out_w, top, c=(True, True, False)).edges("|Y and <Z").fillet(4.0)
    c = c.cut(cq.Workplane("XZ").circle(bore_r).extrude(out_w, both=True).translate((0, 0, top + SPLIT_GAP / 2)))
    for sx in (1, -1):
        for sy in (1, -1):
            x, y = sx * bolt_x, sy * SCREW_Y
            c = c.cut(cq.Workplane("XY").circle(M3_CLR / 2).extrude(top + 1).translate((x, y, -0.5)))
            c = c.cut(cq.Workplane("XY").circle(M3_HEAD_D / 2).extrude(top - CAP_BOSS).translate((x, y, -0.01)))
    return c


def on_bed(s):
    bb = s.val().BoundingBox()
    return s.translate((-bb.xmin, -(bb.ymin + bb.ymax) / 2, -bb.zmin))


if __name__ == "__main__":
    out = Path(__file__).parent / "print"
    out.mkdir(exist_ok=True)
    parts = {
        # body upside down: lid opening on the bed, saddle pointing up (no supports)
        "body": on_bed(body().rotate((0, 0, 0), (1, 0, 0), 180)),
        "lid": on_bed(lid()),
        # cap face down, prongs up
        "end-cap": on_bed(end_cap().rotate((0, 0, 0), (0, 1, 0), 90)),
        "clamp": on_bed(clamp()),
    }
    for n, p in parts.items():
        cq.exporters.export(p, str(out / f"rear-light-{n}.stl"), tolerance=0.02, angularTolerance=0.1)
    first = WALL + END_CLR + PITCH / 2
    last = first + (LEDS - 1) * PITCH
    print(f"strip {strip_len:.2f} | body {out_len:.1f} x {out_w:.1f} x {out_h:.1f} | "
          f"end margins {first - WALL:.2f} / {out_len - PRONG_L - last:.2f}")
