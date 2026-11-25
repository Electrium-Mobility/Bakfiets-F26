"""Shop drawings of the milled stopper: views/stopper_drawings.pdf, plus one PNG per
sheet (views/stopper_drawing_<n>.png) for checking by eye.

Sheet 1: clamp block, top view with every point measured from the bore centre.
Sheet 2: the two stop bars.
Sheet 3: assembly, hardware and torques.
Block coordinates: X towards the front of the bike, Y to the bike's left, looking down
the steering axis from above. All sizes in mm.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, Polygon as MPoly
from build123d import Axis
import render as R
import stopper_milled as M
import stopper as S

made, bump = M.parts(R.C.asm, local=True)
mounts = [S.mount(b) for b in bump]
block = made["stopper block"]
T = M.BLOCK_HI - M.BLOCK_LO
HT_TOP = 68.3                   # head tube top, mm up the steering axis in the model
INK, DIM, HID = "#111111", "#1f4e9a", "#777777"
A3 = (16.54, 11.69)


def edge_points(edge, n=40):
    if edge.geom_type.name == "LINE":
        return np.array([[v.X, v.Y] for v in (edge.start_point(), edge.end_point())])
    return np.array([[p.X, p.Y] for p in (edge.position_at(i / n) for i in range(n + 1))])


def outline_corners(face):
    """Corners of the block outline in order round the edge, from its straight edges,
    leaving out the bore, the slit and the bolt holes."""
    segs = []
    for e in face.outer_wire().edges():
        if e.geom_type.name != "LINE":
            continue
        a, b = e.start_point(), e.end_point()
        if abs(a.X) < 1 and abs(b.X) < 1:
            continue                                   # slit walls
        segs.append(((round(a.X, 2), round(a.Y, 2)), (round(b.X, 2), round(b.Y, 2))))
    # Walk the outline from one side of the slit round to the other, following shared ends.
    nxt = {}
    for a, b in segs:
        nxt.setdefault(a, []).append(b)
        nxt.setdefault(b, []).append(a)
    start = max((p for p in nxt if abs(p[0]) < 1 and len(nxt[p]) == 1), key=lambda p: p[0])
    order, prev, cur = [start], None, start
    while True:
        cands = [q for q in nxt.get(cur, []) if q != prev and q not in order]
        if not cands:
            break
        prev, cur = cur, cands[0]
        order.append(cur)
    # Drop points that sit in the middle of a straight run.
    out = []
    for i, p in enumerate(order):
        a, b = np.array(order[i - 1]), np.array(order[(i + 1) % len(order)])
        v1, v2 = np.array(p) - a, b - np.array(p)
        if abs(v1[0] * v2[1] - v1[1] * v2[0]) > 1e-3 * np.linalg.norm(v1) * np.linalg.norm(v2) and abs(p[0]) > 1:
            out.append(p)
    return out


def title(fig, text, sub):
    fig.text(0.02, 0.965, text, fontsize=18, weight="bold", color=INK)
    fig.text(0.02, 0.94, sub, fontsize=10, color=INK)
    fig.text(0.98, 0.015, "Bakfiets F26 steering stopper, for the bent-rod steering. All sizes in mm. "
             "Material 6061-T6 aluminium. Break all sharp edges.", fontsize=8, ha="right", color=INK)


def table(ax, rows, cols, x0, y0, title_text, col_w=None):
    ax.axis("off")
    ax.text(x0, y0, title_text, fontsize=10, weight="bold", va="top", transform=ax.transAxes)
    t = ax.table(cellText=rows, colLabels=cols, loc="upper left", bbox=None, cellLoc="center",
                 colWidths=col_w)
    t.auto_set_font_size(False)
    t.set_fontsize(8)
    t.scale(1, 1.15)
    return t


def sheet_block(pdf):
    fig = plt.figure(figsize=A3)
    title(fig, "Sheet 1 of 3: clamp block (1 off)",
          f"From {T:.0f} mm plate. Datum: bore centre, X towards the front of the bike, Y to the left, "
          "viewed from above (looking down the steering axis).")
    ax = fig.add_axes([0.03, 0.08, 0.55, 0.83])
    ax.set_aspect("equal")
    top = block.faces().sort_by(Axis.Z)[-1]
    for e in top.edges():
        p = edge_points(e)
        ax.plot(p[:, 0], p[:, 1], color=INK, lw=1.4)
    # Pockets (underside) and holes.
    labels = []
    for i, (m, n) in enumerate(mounts):
        c = np.array(M.bar_corners(m, n))[[0, 1, 3, 2], :2]
        ax.add_patch(MPoly(c, closed=True, fill=False, ls="--", ec=HID, lw=1.2))
        tag = "P1" if i == 0 else "P2"
        cc = c.mean(axis=0)
        ax.text(cc[0], cc[1], tag, ha="center", va="center", fontsize=9, color=HID)
        for j, h in enumerate(M.bar_bolts(m, n)):
            ax.add_patch(Circle(h[:2], 3.2, fill=False, ec=INK, lw=1.2))
            labels.append((f"H{len(labels) + 1}", h[:2], "6.4 thru (M6 clearance)"))
    for k, (tag, p, _) in enumerate(labels):
        off = np.array([12, 6]) if p[0] > 0 else np.array([-4, 14])
        ax.annotate(tag, p, xytext=tuple(p + off), fontsize=9, color=DIM,
                    arrowprops=dict(arrowstyle="-", color=DIM, lw=0.8))
    ax.plot([0], [0], "+", color=DIM, ms=14, mew=1.2)
    ax.text(3, -4, "bore centre (0, 0)", fontsize=9, color=DIM, va="top")
    ax.annotate(f"bore {2 * S.HEAD_TUBE_R:.1f} as modelled.\nBore to the measured head tube\n+0.05 to +0.15, then slit", (-S.HEAD_TUBE_R * 0.7, S.HEAD_TUBE_R * 0.7),
                xytext=(-95, 45), fontsize=9, color=DIM, arrowprops=dict(arrowstyle="->", color=DIM, lw=0.8))
    ax.annotate(f"slit 1.5 wide, through,\nbore to lug end", (0, M.LUG_TO - 3), xytext=(25, M.LUG_TO + 12),
                fontsize=9, color=DIM, arrowprops=dict(arrowstyle="->", color=DIM, lw=0.8))
    ax.annotate("arm end edge parallel to\npocket P1 sides (square off it)", (115, -15), xytext=(60, 40),
                fontsize=9, color=DIM, arrowprops=dict(arrowstyle="->", color=DIM, lw=0.8))
    ax.set_xlabel("X (mm), front of bike to the right")
    ax.set_ylabel("Y (mm), bike's left up")
    ax.grid(True, color="#e6e6e6", lw=0.6)
    ax.set_xlim(-110, 140)
    ax.set_ylim(-110, 80)

    # Tables: outline corners in order round the edge, holes, pockets.
    verts = outline_corners(top)
    for i, (x, y) in enumerate(verts):
        ax.text(x, y, f" C{i + 1}", fontsize=7.5, color="#a33", ha="left", va="bottom")
    ta = fig.add_axes([0.61, 0.40, 0.15, 0.48])
    table(ta, [[f"C{i + 1}", f"{x:.1f}", f"{y:.1f}"] for i, (x, y) in enumerate(verts)], ["corner", "X", "Y"], 0, 1.06,
          "Outline corners,\nstraight edges between")
    tb = fig.add_axes([0.79, 0.70, 0.19, 0.18])
    table(tb, [[t_, f"{p[0]:.1f}", f"{p[1]:.1f}", d] for t_, p, d in labels] +
          [[f"H{len(labels) + 1 + k}", "side", f"{y:.0f}", "M6 pinch, see section"] for k, y in enumerate(M.PINCH_Y)],
          ["hole", "X", "Y", "size"], 0, 1.12, "Holes", col_w=[0.13, 0.17, 0.17, 0.53])
    rows = []
    for i, (m, n) in enumerate(mounts):
        c = np.array(M.bar_corners(m, n))[[0, 1, 3, 2], :2]
        ang = np.degrees(np.arctan2(n[1], n[0]))
        for k, p in enumerate(c):
            rows.append([f"P{i + 1}" if k == 0 else "", f"{p[0]:.1f}", f"{p[1]:.1f}", f"{ang:.1f}" if k == 0 else ""])
    tc = fig.add_axes([0.79, 0.38, 0.19, 0.24])
    table(tc, rows, ["pocket", "X", "Y", "side angle"], 0, 1.16,
          f"Pockets {M.BAR + 0.1:.1f} square, {M.POCKET} deep,\nfrom the underside (corners; angle from X)",
          col_w=[0.2, 0.25, 0.25, 0.3])

    # Section through the pinch lug.
    sx = fig.add_axes([0.62, 0.08, 0.36, 0.25])
    sx.set_aspect("equal")
    sx.add_patch(Rectangle((-M.LUG_W / 2, 0), M.LUG_W, T, fill=False, ec=INK, lw=1.4))
    sx.plot([0, 0], [0, T], color=INK, lw=1.0)
    sx.plot([-0.75, -0.75], [0, T], color=INK, lw=0.6)
    sx.plot([0.75, 0.75], [0, T], color=INK, lw=0.6)
    zc = T / 2
    sx.add_patch(Rectangle((-M.LUG_W / 2, zc - 3.2), M.LUG_W / 2, 6.4, fill=False, ec=HID, ls="--"))
    sx.add_patch(Rectangle((0, zc - 2.5), M.LUG_W / 2, 5.0, fill=False, ec=HID, ls="--"))
    sx.text(-M.LUG_W / 4, T + 3, "6.4 clearance", ha="center", fontsize=8, color=DIM)
    sx.text(M.LUG_W / 4, T + 3, "M6 tapped", ha="center", fontsize=8, color=DIM)
    sx.annotate("", (-M.LUG_W / 2 - 4, 0), (-M.LUG_W / 2 - 4, T), arrowprops=dict(arrowstyle="<->", color=DIM))
    sx.text(-M.LUG_W / 2 - 6, T / 2, f"{T:.0f}", ha="right", va="center", fontsize=9, color=DIM)
    sx.annotate("", (-M.LUG_W / 2, -4), (M.LUG_W / 2, -4), arrowprops=dict(arrowstyle="<->", color=DIM))
    sx.text(0, -7, f"lug {M.LUG_W:.0f} wide (X {-M.LUG_W / 2:.0f} to {M.LUG_W / 2:.0f})", ha="center", va="top", fontsize=9, color=DIM)
    sx.set_title(f"Pinch lug seen from the left of the bike. Two M6 bolts along X at Y = "
                 f"{M.PINCH_Y[0]} and {M.PINCH_Y[1]}, centred in the {T:.0f} mm thickness.\n"
                 f"Clearance on the rear half (X < 0), tapped on the front half. Drill and tap before cutting the slit.",
                 fontsize=8.5)
    sx.set_xlim(-30, 30)
    sx.set_ylim(-14, 28)
    sx.axis("off")
    pdf.savefig(fig)
    fig.savefig("views/stopper_drawing_1.png", dpi=110)
    plt.close(fig)


def sheet_bars(pdf):
    fig = plt.figure(figsize=A3)
    title(fig, "Sheet 2 of 3: stop bars (2 off, A and B)",
          "From 1 in (25.4) square bar. Saw to length, face both ends square. Stamp the letter on face F.")
    B = M.BAR
    rows = []
    for i, (m, n) in enumerate(mounts):
        top = M.BLOCK_LO + M.POCKET
        L = top - (m[2] - M.BAR_BELOW)
        hole = top - m[2]
        rows.append(("A, front (stops left turns)" if i == 0 else "B, rear (stops right turns)", L, hole))
    for i, (name, L, hole) in enumerate(rows):
        ox = 0.05 + i * 0.47
        ax = fig.add_axes([ox, 0.1, 0.42, 0.78])
        ax.set_aspect("equal")
        # Face F view (bumper face): bar shown upright, top end up.
        ax.add_patch(Rectangle((0, 0), B, L, fill=False, ec=INK, lw=1.4))
        ax.add_patch(Circle((B / 2, L - hole), 3.0, fill=False, ec=INK, lw=1.2))
        ax.add_patch(Circle((B / 2, L - hole), 2.5, fill=False, ec=INK, lw=0.6))
        ax.text(B / 2, -8, "face F (bumper face)", ha="center", fontsize=9)
        ax.annotate("", (-8, 0), (-8, L), arrowprops=dict(arrowstyle="<->", color=DIM))
        ax.text(-10, L / 2, f"{L:.1f}", rotation=90, ha="right", va="center", fontsize=11, color=DIM)
        ax.annotate("", (B + 8, L), (B + 8, L - hole), arrowprops=dict(arrowstyle="<->", color=DIM))
        ax.text(B + 10, L - hole / 2, f"{hole:.1f}", rotation=90, ha="left", va="center", fontsize=11, color=DIM)
        ax.annotate("M6 x 12 deep, centred\n(bumper stud)", (B / 2 + 3, L - hole), xytext=(B + 22, L - hole - 25),
                    fontsize=9, color=DIM, arrowprops=dict(arrowstyle="->", color=DIM))
        # Top end view, drawn above.
        y0 = L + 25
        ax.add_patch(Rectangle((0, y0), B, B, fill=False, ec=INK, lw=1.4))
        d_near = B / 2 - M.BOLT_SPREAD
        for d in (d_near, B / 2 + M.BOLT_SPREAD):
            ax.add_patch(Circle((B / 2, y0 + d), 3.0, fill=False, ec=INK, lw=1.2))
            ax.add_patch(Circle((B / 2, y0 + d), 2.5, fill=False, ec=INK, lw=0.6))
        ax.plot([0, B], [y0, y0], color=INK, lw=3)
        ax.text(B / 2, y0 - 4, "face F", ha="center", va="top", fontsize=8)
        ax.annotate("", (B + 6, y0), (B + 6, y0 + d_near), arrowprops=dict(arrowstyle="<->", color=DIM))
        ax.text(B + 8, y0 + d_near / 2, f"{d_near:.1f}", va="center", fontsize=9, color=DIM)
        ax.annotate("", (B + 18, y0), (B + 18, y0 + B / 2 + M.BOLT_SPREAD), arrowprops=dict(arrowstyle="<->", color=DIM))
        ax.text(B + 20, y0 + (B / 2 + M.BOLT_SPREAD) / 2, f"{B / 2 + M.BOLT_SPREAD:.1f}", va="center", fontsize=9, color=DIM)
        ax.text(B / 2, y0 + B + 6, "top end: 2 x M6 x 12 deep\n(tap drill 5.0 x 15), centred across F",
                ha="center", fontsize=9, color=DIM)
        ax.set_title(f"Bar {name}", fontsize=12, pad=12)
        ax.set_xlim(-45, 95)
        ax.set_ylim(-20, y0 + B + 30)
        ax.axis("off")
    pdf.savefig(fig)
    fig.savefig("views/stopper_drawing_2.png", dpi=110)
    plt.close(fig)


def sheet_assembly(pdf):
    fig = plt.figure(figsize=A3)
    title(fig, "Sheet 3 of 3: assembly, hardware, torques", "")
    img = plt.imread("views/stopper_right_front_straight.png")
    ax = fig.add_axes([0.02, 0.32, 0.5, 0.58])
    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Fitted, straight ahead (block dark green, bars light green)", fontsize=10)
    img = plt.imread("views/stopper_below_left.png")
    ax = fig.add_axes([0.5, 0.32, 0.48, 0.58])
    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Full left: fork arm on bumper A (fork 35 deg)", fontsize=10)
    tx = fig.add_axes([0.03, 0.03, 0.94, 0.27])
    tx.axis("off")
    lines = [
        "Hardware: 4 x M6 x 25 socket cap (block to bars), 2 x M6 x 30 socket cap (pinch), 2 x McMaster 9546K431 rubber bumpers (buy new).",
        "Bolt grade 8.8 or better, with washers under the heads. Medium threadlocker on the four bar bolts.",
        "Torque: bar bolts 8 N m. Pinch bolts 6 N m each, tightened in turns, checking the gap across the slit stays even.",
        f"Fit: block top face {HT_TOP - M.BLOCK_HI:.1f} below the top of the head tube, square to the head tube, "
        "slit on the bike's left. Its underside must clear the down tube weld.",
        "Bars: fit face F (the bumper face) towards the fork arm. The bolt holes also line up turned 180 deg, so check the bumpers face each other.",
        "Stops: fork 35 deg each way (handlebars about 34 right, 30 left).",
        "The welded strip in the CAD is not on the bike. Check the space beside the head tube is clear before fitting.",
    ]
    for i, s in enumerate(lines):
        tx.text(0, 1 - i * 0.14, s, fontsize=10, va="top")
    pdf.savefig(fig)
    fig.savefig("views/stopper_drawing_3.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    with PdfPages("views/stopper_drawings.pdf") as pdf:
        sheet_block(pdf)
        sheet_bars(pdf)
        sheet_assembly(pdf)
    print("saved views/stopper_drawings.pdf")
