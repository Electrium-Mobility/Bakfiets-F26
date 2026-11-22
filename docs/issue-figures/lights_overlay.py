# Labels the 21 Nov light strip photos for #79 and #80. Same look as overlay.py.
import sys, os
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
FONT = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 24)
SMALL = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 22)
BLUE, ORANGE, RED, GREEN = (40, 90, 220), (235, 120, 20), (214, 40, 30), (30, 130, 70)
INK = (30, 30, 30)


def label(d, xy, s, color=INK, font=FONT):
    x, y = xy
    l, t, r, b = d.textbbox((x, y), s, font=font)
    d.rounded_rectangle((l - 8, t - 5, r + 8, b + 5), 7, fill=(255, 255, 255), outline=color, width=2)
    d.text((x, y), s, fill=color, font=font)


def point(d, p, lab, s, c, font=SMALL):
    d.line([p, (lab[0] + 40, lab[1] + 20)], fill=c, width=3)
    d.ellipse((p[0] - 11, p[1] - 11, p[0] + 11, p[1] + 11), fill=c, outline='white', width=3)
    label(d, lab, s, c, font)


def open_photo(name, size):
    return Image.open(os.path.join(src, name)).convert('RGB').resize(size)


# 37: the first test on the bench
im = open_photo('01-first-60-leds-lit.jpg', (1000, 750)); d = ImageDraw.Draw(im)
point(d, (150, 222), (20, 290), 'DIN end, wires from the ESP32', GREEN)
point(d, (110, 60), (230, 40), 'ESP32-S3 boards', BLUE)
label(d, (330, 430), 'first 60 LEDs lit', ORANGE, SMALL)
label(d, (20, 690), 'NUM_LEDS was 60 on the first upload', INK, SMALL)
im.save(os.path.join(out, '37-strip-first-test.jpg'), quality=88)

# 38: the board on the breadboard
im = open_photo('03-board-on-breadboard.jpg', (750, 1000)); d = ImageDraw.Draw(im)
point(d, (276, 205), (20, 120), 'USB port, plug in here', GREEN)
point(d, (330, 205), (420, 120), 'UART port, needs a driver', RED)
point(d, (290, 258), (20, 300), 'RESET', INK)
point(d, (328, 258), (420, 300), 'BOOT', INK)
point(d, (372, 410), (420, 470), 'wires to the strip', BLUE)
im.save(os.path.join(out, '38-board-on-breadboard.jpg'), quality=88)

# 39: Jack's two soldered strips
im = open_photo('04-two-soldered-pieces.jpg', (750, 1000)); d = ImageDraw.Draw(im)
point(d, (230, 450), (20, 380), "Jack's two strips", ORANGE)
point(d, (590, 860), (380, 930), 'plugs', BLUE)
im.save(os.path.join(out, '39-two-soldered-strips.jpg'), quality=88)

# 40: one cut strip
im = open_photo('07-cut-36-led-piece.jpg', (1000, 750)); d = ImageDraw.Draw(im)
label(d, (330, 520), 'one strip, 36 LEDs, 25 cm', ORANGE)
point(d, (918, 412), (640, 300), 'cut on the copper pads', RED, SMALL)
im.save(os.path.join(out, '40-cut-strip.jpg'), quality=88)

# 41: the extension cable
im = open_photo('09-extension-cable-length.jpg', (750, 1000)); d = ImageDraw.Draw(im)
point(d, (355, 560), (400, 640), 'extension cable', BLUE)
im.save(os.path.join(out, '41-extension-cable.jpg'), quality=88)
print('ok')
