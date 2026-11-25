# Labels the 21 Nov light strip photos, in the same look as the 17 Nov bay photos:
# big white boxes, black Ink Free text and black arrows.
# Run: python lights_overlay.py ../lights/photos .
import math, os, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont
SRC_DIR, OUT = sys.argv[1], sys.argv[2]
FONT = r'C:\Windows\Fonts\Inkfree.ttf'
SS = 2  # draw at double size so the lines come out smooth


def arrow(d, a, b):
    """Slim line from a to the tip b, with a small solid head."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L, W_ = 34 * SS, 13 * SS
    neck = (b[0] - L * math.cos(ang), b[1] - L * math.sin(ang))
    head = [b, (neck[0] - W_ * math.sin(ang), neck[1] + W_ * math.cos(ang)), (neck[0] + W_ * math.sin(ang), neck[1] - W_ * math.cos(ang))]
    d.line([a, neck], fill='white', width=9 * SS)
    d.polygon(head, fill='white', outline='white', width=6 * SS)
    d.line([a, neck], fill='#111', width=4 * SS)
    d.polygon(head, fill='#111')


def box_edge(b, c, t):
    """Where the line from the box centre c to the target t leaves box b."""
    dx, dy = t[0] - c[0], t[1] - c[1]
    k = min((b[2] - c[0]) / dx if dx > 0 else (b[0] - c[0]) / dx if dx < 0 else 1e9,
            (b[3] - c[1]) / dy if dy > 0 else (b[1] - c[1]) / dy if dy < 0 else 1e9)
    return (c[0] + dx * k, c[1] + dy * k)


def make(src_name, name, labels, fs=74):
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC_DIR, src_name))).convert('RGB')
    r = 1400 / max(im.size)
    w, h = int(im.size[0] * r), int(im.size[1] * r)
    im = im.resize((w * SS, h * SS), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, fs * SS)
    p, m = 18 * SS, 12 * SS
    kw = dict(font=f, anchor='mm', align='center', spacing=10 * SS, stroke_width=SS)
    placed = []
    for target, (lx, ly), text in labels:
        lx, ly = lx * SS, ly * SS
        b = d.multiline_textbbox((lx, ly), text, **kw)
        lx += max(0, m + p - b[0]) - max(0, b[2] + p + m - w * SS)
        ly += max(0, m + p - b[1]) - max(0, b[3] + p + m - h * SS)
        b = d.multiline_textbbox((lx, ly), text, **kw)
        box = [b[0] - p, b[1] - p, b[2] + p, b[3] + p]
        placed.append((target, (lx, ly), text, box))
    for target, c, text, box in placed:
        if target:
            t = (target[0] * SS, target[1] * SS)
            arrow(d, box_edge(box, c, t), t)
    for target, c, text, box in placed:
        d.rounded_rectangle(box, radius=14 * SS, fill='white', outline='#222', width=3 * SS)
        d.multiline_text(c, text, fill='#000', stroke_fill='#000', **kw)
    im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, name + '.jpg'), quality=86)


make('01-first-60-leds-lit.jpg', '37-strip-first-test',
     [((150, 90), (620, 110), 'ESP32-S3 boards'),
      ((120, 290), (260, 640), 'wires from\nthe ESP32'),
      ((600, 515), (760, 820), 'first 60 LEDs lit')])
make('03-board-on-breadboard.jpg', '38-board-on-breadboard',
     [((386, 287), (190, 110), 'USB port\nplug in here'),
      ((462, 287), (850, 110), 'UART port\nneeds a driver'),
      ((406, 361), (150, 520), 'RESET'),
      ((459, 361), (880, 470), 'BOOT'),
      ((521, 574), (840, 820), 'wires to\nthe strip')])
make('07-cut-36-led-piece.jpg', '40-cut-strip',
     [((784, 640), (620, 880), 'one strip of 36 LEDs'),
      ((1285, 577), (1110, 430), 'cut on the\ncopper pads')])
make('09-extension-cable-length.jpg', '41-extension-cable',
     [((497, 784), (790, 1000), 'extension\ncable')])
print('done')
