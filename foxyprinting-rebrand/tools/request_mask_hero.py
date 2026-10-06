"""Main image for "Request Any Celebrity Face Mask": 6 celebrity mask faces in a 3x2 grid with "REQUEST A FACEMASK".

Owner's request (6 Oct 2026): "the request a mask needs a main image of 5 or 6 celebrity faces and REQUEST A FACEMASK
text on it". The faces are the owner's own mask artwork from Dropbox
(/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/...). This product stays website/Shop only (celebrity faces).

Usage: python3 tools/request_mask_hero.py OUT.jpg face1 face2 ... face6
Mask images are faces on white (or transparent PNGs); white around the face is knocked out so each face sits as a
die-cut card mask with a soft shadow.
"""
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W = H = 2048
ORANGE = (255, 106, 19)    # brand colour_primary
INK = (29, 18, 64)         # brand colour_ink
CREAM = (255, 244, 234)    # brand colour_tint
HEAD_FONT = "/root/.fonts/BarlowCondensed-SemiBold.ttf"
SUB_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def cutout(path):
    im = Image.open(path)
    im = im.convert("RGBA")
    if im.getextrema()[3][0] == 255:  # no transparency: knock out near-white background
        rgb = im.convert("RGB")
        white = Image.new("RGB", rgb.size, (255, 255, 255))
        diff = ImageChops.difference(rgb, white).convert("L")
        alpha = diff.point(lambda v: 255 if v > 18 else 0).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
        im.putalpha(alpha)
    box = im.getchannel("A").getbbox()
    return im.crop(box) if box else im


def place(canvas, face, cx, cy, max_w, max_h, angle):
    s = min(max_w / face.width, max_h / face.height)
    f = face.resize((max(1, int(face.width * s)), max(1, int(face.height * s))), Image.LANCZOS)
    f = f.rotate(angle, resample=Image.BICUBIC, expand=True)
    shadow = Image.new("RGBA", f.size, (0, 0, 0, 0))
    shadow.putalpha(f.getchannel("A").point(lambda v: int(v * 0.35)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(shadow, (int(cx - f.width / 2 + 12), int(cy - f.height / 2 + 18)))
    canvas.alpha_composite(f, (int(cx - f.width / 2), int(cy - f.height / 2)))


def fit_font(draw, text, path, max_w, start):
    size = start
    while size > 20:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
        size -= 4
    return ImageFont.truetype(path, size)


def main(out, faces):
    canvas = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(canvas)
    # headline band
    d.rectangle([0, 0, W, 360], fill=ORANGE)
    head = "REQUEST A FACEMASK"
    font = fit_font(d, head, HEAD_FONT, W - 160, 300)
    tw = d.textlength(head, font=font)
    d.text(((W - tw) / 2, 180), head, font=font, fill=(255, 255, 255), anchor="lm")
    # faces 3 x 2
    cells = [(W * (i % 3 * 2 + 1) / 6, 360 + 400 + (i // 3) * 760) for i in range(6)]
    angles = [-5, 3, -3, 4, -4, 5]
    for (cx, cy), path, a in zip(cells, faces, angles):
        place(canvas, cutout(path), cx, cy, 600, 700, a)
    # footer band
    d.rectangle([0, H - 170, W, H], fill=INK)
    sub = "ANY CELEBRITY  •  ANY FACE  •  JUST TELL US WHO"
    sf = fit_font(d, sub, SUB_FONT, W - 200, 76)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, H - 85), sub, font=sf, fill=(255, 255, 255), anchor="lm")
    canvas.convert("RGB").save(out, quality=92)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:8])
