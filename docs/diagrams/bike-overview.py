import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from notebook import *
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

fig, ax = page(150, 100, (15, 10))
note(ax, 8, 96, 'The bike, labelled', size=24, weight='bold')
note(ax, 8, 91.2, 'The 2024 CAD render. The hub motor, battery pack and wiring aren\'t modelled yet, so they\'re listed on the right.',
     size=11.5, color=PENCIL)

img = mpimg.imread(os.path.join(HERE, '..', 'images', 'render-2024.png'))
X0, X1, Y0, Y1 = 14, 94, 8, 72.5          # where the image sits
ax.add_patch(Rectangle((X0 - 0.8, Y0 - 0.8), X1 - X0 + 1.6, Y1 - Y0 + 1.6, fc='white', ec=PENCIL, lw=1, zorder=1))
ax.imshow(img, extent=(X0, X1, Y0, Y1), zorder=2, aspect='auto')
W, H = 983, 793
def P(px, py): return (X0 + (X1 - X0) * px / W, Y1 - (Y1 - Y0) * py / H)

labels = [
    ((8, 84), P(215, 70), 'seat', 0.2),
    ((40, 84), P(560, 125), 'handlebars. a rod under the frame\nlinks them to the front fork', -0.25),
    ((4.5, 24), P(90, 330), 'rear wheel', -0.3),
    ((20, 2.2), P(330, 285), 'frame: a normal back half plus a\nlong, low section that carries the box', 0.3),
    ((62, 2.2), P(640, 610), 'kickstand', 0.3),
    ((96, 20), P(850, 640), 'front wheel (drawn smaller in the CAD;\nthe website says 26"). check in #4', 0.25),
    ((96, 44), P(800, 400), 'front fork', 0.2),
    ((70, 80), P(560, 330), 'wooden cargo box', -0.3),
]
for txt, tgt, s, rad in labels:
    point(ax, txt, tgt, s, size=10.5, color=INK, rad=rad)

# right column: what's still to come
cx = 108
note(ax, cx, 84, 'not in the model yet', size=14, weight='bold', color=RED)
items = [
    ('motor', '500W hub motor in one wheel.\nwhich wheel: check the bike, #1'),
    ('battery', '12S3P pack. where it mounts\nis #5, then #26'),
    ('motor controller', 'FSESC 6.7 (VESC). #18'),
    ('BMS + charge port', 'picked in #19'),
    ('screen + ESP32-S3', 'near the handlebars. #22, #24'),
    ('wiring', 'every wire and fuse. #20'),
]
y = 78
for head, body in items:
    note(ax, cx, y, head, size=12, weight='bold')
    note(ax, cx, y - 3.2, body, size=10, color=PENCIL, va='top', linespacing=1.2)
    y -= 5.5 + 3.2 * (body.count('\n') + 1)
note(ax, cx, 10, 'the real frame is only partly\nwelded. #2 records what exists.', size=10, color=PENCIL, linespacing=1.2)
mono(ax, 149, -1.5, 'render: 2024 SolidWorks model (mechanical/cad-2024/Assem1.SLDASM)', size=7, color='#6f6a60', ha='right')
save(fig, os.path.join(HERE, 'bike-overview.png'))
