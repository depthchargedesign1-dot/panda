"""Final product images: wrap a transfer onto the full-size licensed photo and export a square 2048 px JPEG.

usage: python3 -I render.py BLANK PHOTO TRANSFER.png OUT.jpg
The photo is first scaled to WORK px tall (keeps it sharp but fast), wrapped (wrap.py), then cropped to a square
around the glass and resized to 2048 x 2048 with a light unsharp mask, white background kept.
"""
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wrap  # noqa: E402

WORK = {"pint": 3000, "tumbler": 2600}
# square crop (fractions of the working image): centre x, centre y, side as fraction of height
CROP = {"pint": (0.5, 0.52, 0.86), "tumbler": (0.5, 0.52, 0.96)}


def main(blank, photo, art, out):
    tmp_in = Path(out).with_suffix(".work.png")
    im = Image.open(photo).convert("RGB")
    h = WORK[blank]
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    im.save(tmp_in)
    tmp_out = Path(out).with_suffix(".wrapped.png")
    info = wrap.wrap(blank, str(tmp_in), art, str(tmp_out), ss=2)
    w = Image.open(tmp_out).convert("RGB")
    cx, cy, side = CROP[blank]
    s = round(side * w.height)
    x0, y0 = round(cx * w.width - s / 2), round(cy * w.height - s / 2)
    canvas = Image.new("RGB", (s, s), (255, 255, 255))
    canvas.paste(w.crop((max(0, x0), max(0, y0), min(w.width, x0 + s), min(w.height, y0 + s))), (max(0, -x0), max(0, -y0)))
    canvas = canvas.resize((2048, 2048), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    canvas.save(out, quality=92, subsampling=0, optimize=True)
    tmp_in.unlink()
    tmp_out.unlink()
    return info


if __name__ == "__main__":
    print(main(*sys.argv[1:5]))
