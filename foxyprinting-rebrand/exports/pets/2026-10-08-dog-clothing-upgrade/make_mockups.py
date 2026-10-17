"""Example personalisation mockups (name, optional number) on each dog garment's main packshot.
Usage: python3 make_mockups.py <dir with packshots> <BebasNeue.ttf> <out dir>
Positions are fractions of the 1200 x 1440 supplier packshot, picked by eye for each garment's back panel."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

JOBS = [  # code, packshot, name, number, cx, top, name_h, colour, rotate
    ('PP001', 'pp001_ls21_2026.jpg', 'BELLA', '3', 0.58, 0.40, 0.075, (255, 255, 255), -3),
    ('PP002', 'pp002_ls21_2026.jpg', 'TEDDY', '5', 0.62, 0.44, 0.07, (255, 255, 255), -2),
    ('PP003', 'pp003_ls21_20262.jpg', 'LUNA', None, 0.52, 0.43, 0.09, (255, 255, 255), -2),
    ('PP004', 'pp004_ls21_2026.jpg', 'BEAR', None, 0.60, 0.43, 0.06, (255, 255, 255), -3),
    ('PP006', 'pp006_ls21_2026.jpg', 'MAX', None, 0.66, 0.47, 0.07, (255, 255, 255), -2),
    ('PP008', 'pp008_ls20_2026.jpg', 'OLLIE', '10', 0.60, 0.36, 0.07, (20, 30, 70), -6),
]


def render(src, font_path, out, name, number, cx_f, top_f, name_h, colour, rot):
    im = Image.open(src).convert('RGB')
    W, H = im.size
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    def centred(text, size, cx, top):
        f = ImageFont.truetype(font_path, size)
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        d.text((cx - (r - l) / 2 - l, top - t), text, font=f, fill=colour + (240,))
        return top + (b - t)

    cx, y = int(W * cx_f), int(H * top_f)
    y = centred(name, int(H * name_h), cx, y)
    if number:
        centred(number, int(H * name_h * 2), cx, y + int(H * 0.018))
    layer = layer.rotate(rot, resample=Image.BICUBIC, center=(cx, int(H * (top_f + 0.08))))
    im = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
    side = 2000
    s = side * 0.92 / max(W, H)
    im = im.resize((int(W * s), int(H * s)), Image.LANCZOS)
    canvas = Image.new('RGB', (side, side), 'white')
    canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    canvas.save(out, quality=85)


if __name__ == '__main__':
    src_dir, font, out_dir = map(Path, sys.argv[1:4])
    for code, f, name, num, cx, top, nh, col, rot in JOBS:
        o = out_dir / f'{code}-mockup.jpg'
        render(src_dir / f, str(font), o, name, num, cx, top, nh, col, rot)
        print(o)
