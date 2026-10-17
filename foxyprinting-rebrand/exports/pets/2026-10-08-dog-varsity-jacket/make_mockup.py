"""Example personalisation mockup for the dog varsity jacket (PP005).
Draws an example name + number ("BUSTER" / "7") in white Bebas Neue (OFL) on the jacket's back panel
of the supplier packshot, then pads it to a 2000 x 2000 white square (artwork-specs.md).
Usage: python3 make_mockup.py <packshot.jpg> <BebasNeue.ttf> <out.jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

src, font_path, out = sys.argv[1:4]
im = Image.open(src).convert('RGB')
W, H = im.size  # 1200 x 1440 supplier packshot
layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

def centred(text, size, cx, top):
    f = ImageFont.truetype(font_path, size)
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    d.text((cx - (r - l) / 2 - l, top - t), text, font=f, fill=(255, 255, 255, 240))
    return top + (b - t)

cx = int(W * 0.56)
y = centred('BUSTER', int(H * 0.085), cx, int(H * 0.40))
centred('7', int(H * 0.17), cx, y + int(H * 0.02))
# tilt slightly to follow the jacket's back line
layer = layer.rotate(-4, resample=Image.BICUBIC, center=(cx, int(H * 0.5)))
im = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')

side = 2000
scale = side * 0.92 / max(W, H)
im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
canvas = Image.new('RGB', (side, side), 'white')
canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
canvas.save(out, quality=85)
print(out, canvas.size)
