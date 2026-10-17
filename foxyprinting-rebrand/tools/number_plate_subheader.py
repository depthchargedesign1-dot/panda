"""Compact 1800x600 header banner for the Funny Number Plate Mugs collection.
Composites our own BR3W UP both-ends mockup onto a Foxy-branded background,
leaving the left ~50% plain so the white collection title reads over it."""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

SRC = "exports/number-plate-mugs/mockups-local/FOXY-SUB-FNPMBUBU-6-both-ends.jpg"
OUT = sys.argv[1] if len(sys.argv) > 1 else "exports/mug-subheaders/foxy-subheader-funny-number-plate-mugs.jpg"
W, H = 1800, 600
INK, PURPLE, ORANGE = (29, 18, 64), (122, 43, 245), (255, 106, 19)

# background: ink -> purple horizontal gradient, with an orange glow behind the mugs
bg = Image.new("RGB", (W, H))
px = bg.load()
for x in range(W):
    t = (x / W) ** 1.4
    c = tuple(int(INK[i] + (PURPLE[i] - INK[i]) * t * 0.75) for i in range(3))
    for y in range(H):
        px[x, y] = c
glow = Image.new("L", (W, H), 0)
ImageDraw.Draw(glow).ellipse((1020, 40, 1780, 640), fill=150)
glow = glow.filter(ImageFilter.GaussianBlur(120))
bg = Image.composite(Image.new("RGB", (W, H), ORANGE), bg, glow)

# cut the mugs out of the white studio background (flood fill from the corners)
m = Image.open(SRC).convert("RGB")
mask = Image.new("L", m.size, 255)
probe = m.copy()
for corner in [(0, 0), (m.width - 1, 0), (0, m.height - 1), (m.width - 1, m.height - 1)]:
    ImageDraw.floodfill(probe, corner, (255, 0, 255), thresh=18)
r, g, b = probe.split()
bgpix = ImageChops.multiply(r.point(lambda v: 255 if v == 255 else 0), b.point(lambda v: 255 if v == 255 else 0))
bgpix = ImageChops.multiply(bgpix, g.point(lambda v: 255 if v == 0 else 0))
mask = ImageChops.invert(bgpix).filter(ImageFilter.GaussianBlur(1.2))
bbox = mask.getbbox()
m, mask = m.crop(bbox), mask.crop(bbox)
scale = 400 / m.height
size = (int(m.width * scale), int(m.height * scale))
m, mask = m.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)
x0 = W - size[0] - 70
y0 = (H - size[1]) // 2

# soft floor shadow
sh = Image.new("L", (W, H), 0)
ImageDraw.Draw(sh).ellipse((x0 + 40, y0 + size[1] - 30, x0 + size[0] - 40, y0 + size[1] + 30), fill=140)
sh = sh.filter(ImageFilter.GaussianBlur(22))
bg = Image.composite(Image.new("RGB", (W, H), (10, 6, 25)), bg, sh)
bg.paste(m, (x0, y0), mask)
bg.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
print(OUT, bg.size)
