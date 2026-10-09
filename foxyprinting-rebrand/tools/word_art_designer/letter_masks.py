"""Masks for the Pink/Blue Letter A-Z word art products.

Their photos have an example name printed big across the letter, which spoils a mask traced from the photo,
so the letter is drawn from Russo One (SIL OFL, fonts/RussoOne-OFL.txt), a chunky chamfered block font like
the originals, and coloured with the letter's own colour taken from the traced mask (make_masks.py output).

Usage: python3 letter_masks.py products_all.json traced_masks_dir out_dir
"""
import json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 452, 640  # A portrait, same scale as the traced masks


def letter_of(title):
    m = re.search(r'Letter\s+([A-Z])\b', title)
    return m.group(1) if m else None


def body_colour(traced_png):
    a = np.asarray(Image.open(traced_png).convert('RGBA')).astype(np.float32)
    al = a[..., 3] > 128
    rgb = a[..., :3][al]
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722]) / 255
    keep = lum > np.percentile(lum, 35)  # the light letter body, not the dark example name
    return rgb[keep].mean(axis=0) if keep.any() else rgb.mean(axis=0)


def draw_letter(ch, colour):
    big = Image.new('L', (H * 7, H * 5), 0)
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'RussoOne.ttf'), H * 4)
    d = ImageDraw.Draw(big)
    d.text((H // 2, H // 4), ch, font=font, fill=255)
    big = big.crop(big.getbbox())
    bw, bh = big.size
    tw, th = W * 0.86, H * 0.86
    s = min(tw / bw, th / bh)
    sx = min(s * 1.3, tw / bw)  # widen narrow letters a little, like the originals' blocks
    sy = min(s * 1.3, th / bh)  # and stretch wide letters (M, W) taller
    nw, nh = max(1, round(bw * sx)), max(1, round(bh * sy))
    if ch in 'IJ1':
        nw = max(1, round(bw * s))
        nh = max(1, round(bh * s))
    letter = big.resize((nw, nh), Image.LANCZOS)
    alpha = Image.new('L', (W, H), 0)
    alpha.paste(letter, ((W - nw) // 2, (H - nh) // 2))
    out = Image.new('RGBA', (W, H), tuple(int(c) for c in colour) + (0,))
    out.putalpha(alpha)
    return out


def main():
    products = json.load(open(sys.argv[1]))
    traced, out = sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    report = []
    for p in products:
        if 'wa-names' not in p['tags']:
            continue
        ch = letter_of(p['title'])
        src = os.path.join(traced, p['handle'] + '.png')
        row = {'id': p['id'], 'handle': p['handle'], 'title': p['title']}
        if not ch or not os.path.exists(src):
            row['error'] = 'no letter in title' if not ch else 'no traced mask'
        else:
            col = body_colour(src)
            fn = os.path.join(out, p['handle'] + '.png')
            draw_letter(ch, col).save(fn, optimize=True)
            row.update({'file': fn, 'letter': ch, 'colour': [int(c) for c in col], 'size': [W, H]})
        report.append(row)
        print(row['title'][-20:], row.get('letter'), row.get('colour'), row.get('error', ''))
    json.dump(report, open(os.path.join(out, 'report.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
