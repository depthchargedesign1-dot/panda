#!/usr/bin/env python3
"""Framed product photos for new word art prints (9 Oct 2026).

Puts each artwork into the store's own real frame photos (the 1500x1500 brick-wall template, Black =
Robbie_Williams-Black.jpg, Silver = COLUMBO_PETER-Silver.jpg), replacing the old print inside the frame
with the new artwork on white paper, like a real print with a margin.

Usage: python3 -I framed_images.py <frames_dir> <art_dir> <out_dir> name1.jpg name2.jpg ...
Writes <name>-black.jpg, <name>-silver.jpg (1500x1500) and <name>-flat.jpg (2000px long side).
"""
import os, sys
from PIL import Image, ImageFilter

FRAMES = {'black': ('Robbie_Williams-Black.jpg', (240, 399, 1268, 1117)),
          'silver': ('COLUMBO_PETER-Silver.jpg', (234, 393, 1270, 1120))}


def trim_white(im):
    g = im.convert('L').point(lambda v: 255 if v < 245 else 0)
    box = g.getbbox()
    return im.crop(box) if box else im


def paper(art, w, h, margin=0.07):
    """Artwork centred on white paper of w x h, keeping a margin like a real print."""
    p = Image.new('RGB', (w, h), 'white')
    a = art.copy()
    a.thumbnail((int(w * (1 - 2 * margin)), int(h * (1 - 2 * margin))), Image.LANCZOS)
    p.paste(a, ((w - a.width) // 2, (h - a.height) // 2))
    return p


def framed(art, frames_dir, kind):
    name, (l, t, r, b) = FRAMES[kind]
    ph = Image.open(os.path.join(frames_dir, name)).convert('RGB')
    w, h = r - l, b - t
    p = paper(art, w + 4, h + 4)
    # a soft inner shadow from the frame moulding, so the paper sits behind the frame
    sh = Image.new('L', p.size, 0)
    sh.paste(255, (0, 0, p.width, 10)); sh.paste(255, (0, 0, 10, p.height))
    sh = sh.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.25))
    p = Image.composite(Image.new('RGB', p.size, (90, 90, 90)), p, sh)
    ph.paste(p, (l - 2, t - 2))
    return ph


def main(frames_dir, art_dir, out_dir, *names):
    os.makedirs(out_dir, exist_ok=True)
    for n in names:
        art = trim_white(Image.open(os.path.join(art_dir, n)).convert('RGB'))
        stem = os.path.splitext(n)[0]
        for kind in FRAMES:
            framed(art, frames_dir, kind).save(os.path.join(out_dir, f'{stem}-{kind}.jpg'), quality=90)
        flat = paper(art, 2000, int(2000 / 1.414), margin=0.05)
        flat.save(os.path.join(out_dir, f'{stem}-flat.jpg'), quality=90)
        print(stem)


if __name__ == '__main__':
    main(*sys.argv[1:])
