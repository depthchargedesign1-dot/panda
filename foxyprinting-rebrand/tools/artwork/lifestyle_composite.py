"""Composite a locally rendered product (transparent cut-out) onto an AI-generated empty background.
Backgrounds are text-prompt Higgsfield images with no people, logos or text (made 8 Oct 2026).
usage: python3 lifestyle_composite.py mug BG.png CUTOUT.png OUT.jpg [width_frac] [bottom_frac] [x_frac]
       python3 lifestyle_composite.py print BG.png PRINT_TEXTURE.png OUT.jpg [height_frac] [top_frac]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

N = 2000


def mug(bg, cut, out, wf=0.46, bf=0.80, xf=0.5):
    B = Image.open(bg).convert("RGB").resize((N, N), Image.LANCZOS)
    C = Image.open(cut).convert("RGBA")
    w = int(N * wf)
    C = C.resize((w, round(C.height * w / C.width)), Image.LANCZOS)
    # warm the white glaze slightly to sit in the warm scenes
    rgb = ImageEnhance.Color(C.convert("RGB")).enhance(1.0)
    arr = np.asarray(rgb).astype(np.float32)
    arr *= np.array([1.0, 0.985, 0.95])
    C2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    C2.putalpha(C.split()[3])
    x = int(N * xf - w / 2)
    y = int(N * bf - C.height)
    # soft contact shadow
    sh = Image.new("L", (N, N), 0)
    sw, shh = int(w * 0.62), int(w * 0.07)
    body_cx = x + int(w * 0.60)  # body sits right of the handle
    from PIL import ImageDraw
    ImageDraw.Draw(sh).ellipse([body_cx - sw // 2, y + C.height - shh // 2, body_cx + sw // 2, y + C.height + shh // 2], fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    a = np.asarray(sh).astype(np.float32) / 255 * 0.55
    barr = np.asarray(B).astype(np.float32) * (1 - a[..., None])
    B = Image.fromarray(barr.astype(np.uint8))
    B.paste(C2, (x, y), C2)
    B.save(out, quality=88)


def poster(bg, tex, out, hf=0.40, tf=0.14):
    B = Image.open(bg).convert("RGB").resize((N, N), Image.LANCZOS)
    T = Image.open(tex).convert("RGB")
    h = int(N * hf)
    T = T.resize((round(T.width * h / T.height), h), Image.LANCZOS)
    x, y = (N - T.width) // 2, int(N * tf)
    sh = Image.new("L", (N, N), 0)
    sh.paste(200, (x + 8, y + 16, x + 8 + T.width, y + 16 + T.height))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    a = np.asarray(sh).astype(np.float32) / 255 * 0.35
    barr = np.asarray(B).astype(np.float32) * (1 - a[..., None])
    B = Image.fromarray(barr.astype(np.uint8))
    # match the room light: very slight warm/dim
    tarr = np.asarray(T).astype(np.float32) * np.array([0.97, 0.955, 0.93])
    B.paste(Image.fromarray(np.clip(tarr, 0, 255).astype(np.uint8)), (x, y))
    B.save(out, quality=88)


if __name__ == "__main__":
    kind, a = sys.argv[1], sys.argv[2:]
    nums = [float(v) for v in a[3:]]
    (mug if kind == "mug" else poster)(a[0], a[1], a[2], *nums)
