# Draws the brake line routes and rough light positions on the photo of the frame.
import sys, os
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
FONT = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 24)
SMALL = ImageFont.truetype('C:/Windows/Fonts/Inkfree.ttf', 22)
base = Image.open(src).convert('RGB').resize((1000, 750))
BLUE, ORANGE, RED = (40, 90, 220), (235, 120, 20), (214, 40, 30)


def label(d, xy, s, color=(30, 30, 30), font=FONT):
    x, y = xy
    l, t, r, b = d.textbbox((x, y), s, font=font)
    d.rounded_rectangle((l - 8, t - 5, r + 8, b + 5), 7, fill=(255, 255, 255), outline=color, width=2)
    d.text((x, y), s, fill=color, font=font)


def route(d, pts, color):
    d.line(pts, fill=(255, 255, 255), width=11, joint='curve')
    d.line(pts, fill=color, width=6, joint='curve')
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill=color, outline='white', width=2)


im = base.copy(); d = ImageDraw.Draw(im)
route(d, [(530, 142), (445, 172), (452, 250), (490, 400), (520, 512), (640, 498), (760, 482), (806, 370), (848, 205), (925, 262), (946, 415)], BLUE)
route(d, [(305, 175), (438, 178), (446, 256), (482, 402), (470, 425), (275, 452), (172, 440), (145, 590)], ORANGE)
label(d, (560, 92), 'front line: along the box', BLUE)
label(d, (20, 96), 'rear line: along the frame', ORANGE)
label(d, (20, 680), 'rough routes. run your string along these with the bars turned both ways', (30, 30, 30), SMALL)
label(d, (830, 430), 'front brake', BLUE, SMALL)
label(d, (30, 610), 'rear brake', ORANGE, SMALL)
im.save(os.path.join(out, 'brake-line-routes.jpg'), quality=88)

im = base.copy(); d = ImageDraw.Draw(im)
spots = [((866, 170), (640, 60), 'headlight', RED), ((905, 228), (690, 120), 'front turn signals (a pair)', ORANGE), ((88, 505), (20, 440), 'rear light', RED), ((110, 590), (20, 610), 'rear turn signals (a pair)', ORANGE)]
d.line([(330, 533), (520, 512), (760, 482)], fill=(255, 255, 255), width=12)
d.line([(330, 533), (520, 512), (760, 482)], fill=BLUE, width=7)
for p, lab, s, c in spots:
    d.line([p, (lab[0] + 40, lab[1] + 20)], fill=c, width=3)
    d.ellipse((p[0] - 13, p[1] - 13, p[0] + 13, p[1] + 13), fill=c, outline='white', width=3)
    label(d, lab, s, c, SMALL)
label(d, (400, 570), 'side LED strip', BLUE, SMALL)
label(d, (180, 690), 'rough spots only. #53 works out the exact places', (30, 30, 30), SMALL)
im.save(os.path.join(out, 'lights-on-the-bike.jpg'), quality=88)
print('ok')
