"""Build the "too rude to show" social adverts for the 10 rude number plate mugs.

Every mug is shown with the registration covered by a CENSORED bar (see rude_mugs_censored_mockups.py),
so no rude word appears anywhere (TikTok / Meta community guidelines).

usage: python3 rude_mugs_ad.py MUGS_DIR OUT_DIR
  MUGS_DIR: output of rude_mugs_censored_mockups.py
writes to OUT_DIR:
  rude-mugs-ad-9x16.mp4   1080x1920, 15 s, 30 fps, H.264 + silent AAC (TikTok, Reels, Stories)
  rude-mugs-ad-1x1.mp4    1080x1080, 15 s, 30 fps, H.264 + silent AAC (Facebook / Instagram feed)
  rude-mugs-carousel-1.jpg .. -3.jpg   1080x1350 carousel stills
  poster-9x16.jpg, poster-1x1.jpg      cover frames
"""
import math
import os
import subprocess
import sys
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "artwork", "assets", "fonts")
ANTON = "/root/.fonts/Anton-Regular.ttf"
POPPINS = os.path.join(FONTS, "Poppins-Bold.ttf")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

ORANGE = (255, 106, 19)
INK = (29, 18, 64)
PINK = (255, 45, 135)
WHITE = (255, 255, 255)
FPS = 30
DUR = 15.0
URL = "foxyprinting.co.uk"


# ------------------------------------------------------------------ text
def is_emoji(ch):
    return ord(ch) >= 0x1F000


@lru_cache(None)
def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 4), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    s = size / im.height
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


@lru_cache(None)
def line_img(text, font_path, size, fill, stroke=0, stroke_fill=INK, max_w=None, track=0.0):
    """One line of text (with colour emoji) as a tight RGBA image. Shrinks to max_w."""
    while True:
        f = ImageFont.truetype(font_path, size)
        asc, desc = f.getmetrics()
        parts, w = [], 0
        for ch in text:
            if is_emoji(ch):
                im = emoji_img(ch, int(size * .78))
                parts.append(("e", im, w))
                w += im.width + size * .05
            else:
                cw = f.getlength(ch) + size * track
                parts.append(("t", ch, w))
                w += cw
        if max_w is None or w + 2 * stroke <= max_w or size < 12:
            break
        size = int(size * max_w / (w + 2 * stroke)) - 1
    pad = stroke + 4
    H = asc + desc + 2 * pad
    im = Image.new("RGBA", (int(math.ceil(w)) + 2 * pad, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for kind, v, x in parts:
        if kind == "t":
            d.text((pad + x, pad), v, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    for kind, v, x in parts:
        if kind == "e":
            y = pad + (asc - v.height) // 2 + int(size * .08)
            im.alpha_composite(v, (int(pad + x), max(0, y)))
    bb = im.getbbox()
    return im.crop((0, bb[1], im.width, bb[3]))


def block(lines, gap=14):
    """lines: list of line_img results -> centred RGBA block"""
    w = max(l.width for l in lines)
    h = sum(l.height for l in lines) + gap * (len(lines) - 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for l in lines:
        im.alpha_composite(l, ((w - l.width) // 2, y))
        y += l.height + gap
    return im


def pill(text, font_path, size, fg, bg, padx=34, pady=20, max_w=None):
    t = line_img(text, font_path, size, fg, max_w=None if max_w is None else max_w - 2 * padx)
    im = Image.new("RGBA", (t.width + 2 * padx, t.height + 2 * pady), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], im.height // 2, fill=bg)
    im.alpha_composite(t, (padx, pady))
    return im


def wordmark(size):
    a = line_img("Foxy", POPPINS, size, WHITE)
    b = line_img("Printing", POPPINS, size, ORANGE)
    gap = int(size * .22)
    h = max(a.height, b.height)
    im = Image.new("RGBA", (a.width + gap + b.width, h), (0, 0, 0, 0))
    im.alpha_composite(a, (0, h - a.height))
    im.alpha_composite(b, (a.width + gap, h - b.height))
    return im


# ------------------------------------------------------------------ backgrounds
@lru_cache(None)
def background(w, h, base, glow, seed=0):
    """flat brand colour with a soft radial glow and faint diagonal stripes"""
    im = Image.new("RGB", (w, h), base)
    g = Image.new("L", (w, h), 0)
    ImageDraw.Draw(g).ellipse([w * .05, h * .18, w * .95, h * .82], fill=255)
    g = g.filter(ImageFilter.GaussianBlur(min(w, h) * .18))
    im = Image.composite(Image.new("RGB", (w, h), glow), im, g.point(lambda v: int(v * .55)))
    st = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(st)
    step = 90
    for x in range(-h, w + h, step):
        d.polygon([(x, 0), (x + 30, 0), (x + 30 - h, h), (x - h, h)], fill=14)
    return Image.composite(Image.new("RGB", (w, h), WHITE), im, st)


def lighten(c, k):
    return tuple(int(v + (255 - v) * k) for v in c)


def darken(c, k):
    return tuple(int(v * (1 - k)) for v in c)


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def back_out(t, s=1.9):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def paste_scaled(frame, im, cx, cy, scale=1.0, alpha=1.0, resample=Image.BILINEAR):
    if scale <= 0.01 or alpha <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), resample)
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    frame.alpha_composite(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))


# ------------------------------------------------------------------ assets
class Assets:
    def __init__(self, mugs_dir):
        self.front = [Image.open(os.path.join(mugs_dir, f"{n}-front.png")).convert("RGBA") for n in range(1, 11)]
        self.band = [Image.open(os.path.join(mugs_dir, f"{n}-band.png")).convert("RGBA") for n in range(1, 11)]
        self.pair = Image.open(os.path.join(mugs_dir, "pair.png")).convert("RGBA")
        self._c = {}

    def fit(self, key, im, w):
        k = (key, w)
        if k not in self._c:
            s = w / im.width
            self._c[k] = im.resize((w, round(im.height * s)), Image.LANCZOS)
        return self._c[k]


# ------------------------------------------------------------------ layout per format
class Layout:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.vertical = H > W
        if self.vertical:                       # TikTok UI: keep text out of right 120 / bottom 250
            self.tx, self.tw = (60 + (W - 120)) / 2, W - 60 - 120 - 20
            self.top, self.bottom = 150, H - 250
        else:
            self.tx, self.tw = W / 2, W - 130
            self.top, self.bottom = 60, H - 60


BG_CYCLE = [(ORANGE, lighten(ORANGE, .35)), (INK, (70, 40, 140)), (PINK, lighten(PINK, .35))]


def render_frame(t, A, L):
    W, H = L.W, L.H
    V = L.vertical
    S = H / 1920 if V else W / 1080          # text scale
    fr = None

    # ---------------- scene A: hook (0 - 3.0 s)
    if t < 3.0:
        fr = background(W, H, INK, (70, 40, 140)).convert("RGBA")
        k1, k2 = (118, 230) if V else (96, 180)
        l1 = line_img("NUMBER PLATES", ANTON, int(k1 * S), WHITE, max_w=L.tw)
        l2 = line_img("TOO RUDE", ANTON, int(k2 * S), PINK, stroke=int(6 * S), stroke_fill=WHITE, max_w=L.tw)
        l3 = line_img("TO SHOW YOU \U0001F648", ANTON, int(k1 * S), WHITE, max_w=L.tw)
        if V:
            y1, y2, y3 = L.top + 60, L.top + 250, L.top + 440
            mug_w, mug_cy = 900, 1270
        else:
            y1, y2, y3 = 85, 225, 370
            mug_w, mug_cy = 560, 770
        paste_scaled(fr, l1, L.tx, y1, back_out((t - .05) / .3), clamp(t / .1))
        paste_scaled(fr, l2, L.tx, y2, back_out((t - .35) / .35) * (1 + .03 * math.sin(t * 9) * (t > .7)),
                     clamp((t - .35) / .1))
        paste_scaled(fr, l3, L.tx, y3, back_out((t - .75) / .3), clamp((t - .75) / .1))
        mug = A.fit("f0", A.front[0], mug_w)
        k = ease_out((t - .2) / .7)
        paste_scaled(fr, mug, W / 2, mug_cy + (1 - k) * H * .45, 0.96 + .06 * clamp(t / 3), 1)
        # "18+" chip
        chip = pill("18+ HUMOUR", POPPINS, int(34 * S), WHITE, PINK, padx=int(22 * S), pady=int(12 * S))
        if V:
            paste_scaled(fr, chip, L.tx, L.bottom - 40, back_out((t - 1.3) / .3))
        else:
            paste_scaled(fr, chip, W - 60 - chip.width / 2, H - 50 - chip.height / 2, back_out((t - 1.3) / .3))

    # ---------------- scene B: 10 quick cuts (3.0 - 9.6 s)
    elif t < 9.6:
        i = min(9, int((t - 3.0) / 0.66))
        lt = t - 3.0 - i * 0.66
        base, glow = BG_CYCLE[i % 3]
        fr = background(W, H, base, glow).convert("RGBA")
        src = A.front[i] if i % 2 == 0 else A.band[i]
        if V:
            mug_w, mug_cy = 940, 1060
            head_y, sub_y = L.top + 70, L.bottom - 70
        else:
            mug_w, mug_cy = 620, 590
            head_y, sub_y = 105, H - 75
        mug = A.fit(("b", i), src, mug_w)
        punch = 1.10 - .10 * ease_out(lt / .14) + .035 * (lt / .66)
        slide = (1 - ease_out(lt / .16)) * (90 if i % 2 == 0 else -90)
        paste_scaled(fr, mug, W / 2 + slide, mug_cy, punch)
        head = line_img("10 CHEEKY DESIGNS", ANTON, int(130 * S), WHITE, stroke=int(5 * S), stroke_fill=INK,
                        max_w=L.tw)
        paste_scaled(fr, head, L.tx, head_y, back_out((t - 3.0) / .3) if t < 3.4 else 1)
        cnt = pill(f"{i + 1} / 10", POPPINS, int(44 * S), WHITE if base != INK else INK,
                   INK if base != INK else ORANGE, padx=int(26 * S), pady=int(12 * S))
        paste_scaled(fr, cnt, L.tx, head_y + int(125 * S), back_out(lt / .18))
        guess = line_img("CAN YOU GUESS IT? \U0001F914", ANTON, int(84 * S), WHITE, stroke=int(4 * S),
                         stroke_fill=INK, max_w=L.tw)
        if t >= 4.3:
            paste_scaled(fr, guess, L.tx, sub_y, back_out((t - 4.3) / .3) if t < 4.7 else 1)

    # ---------------- scene C: pair + price (9.6 - 12.2 s)
    elif t < 12.2:
        lt = t - 9.6
        fr = background(W, H, ORANGE, lighten(ORANGE, .35)).convert("RGBA")
        l1 = line_img("YOUR MATE WILL KNOW", ANTON, int(108 * S), WHITE, stroke=int(5 * S), stroke_fill=INK,
                      max_w=L.tw)
        l2 = line_img("EXACTLY WHAT IT SAYS \U0001F602", ANTON, int(108 * S), WHITE, stroke=int(5 * S),
                      stroke_fill=INK, max_w=L.tw)
        price = pill("£7.99 · PRINTED IN THE UK", POPPINS, int(50 * S), WHITE, INK,
                     padx=int(36 * S), pady=int(22 * S), max_w=L.tw)
        if V:
            y1, y2, mug_w, mug_cy, py = L.top + 70, L.top + 200, 1040, 960, L.bottom - 230
            sub = line_img("11oz ceramic · dishwasher safe", POPPINS, int(42 * S), INK, max_w=L.tw)
        else:
            y1, y2, mug_w, mug_cy, py = 95, 210, 760, 590, H - 95
            sub = None
        paste_scaled(fr, l1, L.tx, y1, back_out(lt / .3))
        paste_scaled(fr, l2, L.tx, y2, back_out((lt - .15) / .3))
        mug = A.fit("pair", A.pair, mug_w)
        k = ease_out(lt / .5)
        paste_scaled(fr, mug, W / 2 + (1 - k) * W * .6, mug_cy, 1.0 + .05 * clamp(lt / 2.6))
        paste_scaled(fr, price, L.tx, py, back_out((lt - .6) / .3))
        if sub is not None:
            paste_scaled(fr, sub, L.tx, py + int(110 * S), clamp((lt - .9) / .2))

    # ---------------- scene D: end card (12.2 - 15 s)
    else:
        lt = t - 12.2
        fr = background(W, H, INK, (70, 40, 140)).convert("RGBA")
        wm = wordmark(int(118 * S))
        if wm.width > L.tw:
            wm = wm.resize((int(L.tw), int(wm.height * L.tw / wm.width)), Image.LANCZOS)
        search = pill("Search: rude number plate mug", POPPINS, int(46 * S), WHITE, PINK,
                      padx=int(34 * S), pady=int(22 * S), max_w=L.tw)
        url = line_img(URL, POPPINS, int(80 * S), ORANGE, max_w=L.tw)
        price = line_img("£7.99 · printed in the UK", POPPINS, int(48 * S), WHITE, max_w=L.tw)
        small = line_img("10 cheeky designs · 18+ humour", POPPINS, int(34 * S), lighten(INK, .55), max_w=L.tw)
        if V:
            ywm, mug_w, mug_cy, yp, ys, yu, ysm = L.top + 90, 760, 760, 1150, 1290, 1420, 1540
        else:
            ywm, mug_w, mug_cy, yp, ys, yu, ysm = 90, 430, 390, 640, 750, 870, 975
        paste_scaled(fr, wm, L.tx, ywm, back_out(lt / .35))
        mug = A.fit("end", A.front[4], mug_w)
        paste_scaled(fr, mug, W / 2, mug_cy + (1 - ease_out(lt / .45)) * 200, 1.0 + .04 * clamp(lt / 2.8),
                     clamp(lt / .2))
        paste_scaled(fr, price, L.tx, yp, back_out((lt - .25) / .3))
        paste_scaled(fr, search, L.tx, ys, back_out((lt - .45) / .3) * (1 + .025 * math.sin(lt * 7) * (lt > .9)))
        paste_scaled(fr, url, L.tx, yu, back_out((lt - .65) / .3))
        paste_scaled(fr, small, L.tx, ysm, clamp((lt - .9) / .25))
    return fr.convert("RGB")


def video(A, W, H, out):
    L = Layout(W, H)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
           "-shortest", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for k in range(n):
        p.stdin.write(render_frame(k / FPS, A, L).tobytes())
    p.stdin.close()
    assert p.wait() == 0
    return L


# ------------------------------------------------------------------ carousel stills 1080x1350
def stills(A, out):
    W, H = 1080, 1350
    tw = W - 140
    # 1: hook
    fr = background(W, H, INK, (70, 40, 140)).convert("RGBA")
    paste_scaled(fr, line_img("NUMBER PLATES", ANTON, 110, WHITE, max_w=tw), W / 2, 120)
    paste_scaled(fr, line_img("TOO RUDE", ANTON, 220, PINK, stroke=6, stroke_fill=WHITE, max_w=tw), W / 2, 300)
    paste_scaled(fr, line_img("TO SHOW YOU \U0001F648", ANTON, 110, WHITE, max_w=tw), W / 2, 480)
    paste_scaled(fr, A.fit("s1", A.front[0], 820), W / 2, 900)
    paste_scaled(fr, line_img("Swipe to see all 10 \U0001F449", POPPINS, 40, lighten(INK, .6)), W / 2, 1270)
    fr.convert("RGB").save(os.path.join(out, "rude-mugs-carousel-1.jpg"), quality=92)

    # 2: all ten
    fr = background(W, H, ORANGE, lighten(ORANGE, .35)).convert("RGBA")
    paste_scaled(fr, line_img("10 CHEEKY DESIGNS", ANTON, 120, WHITE, stroke=5, stroke_fill=INK, max_w=tw),
                 W / 2, 110)
    paste_scaled(fr, line_img("Every plate censored. You know the rest.", POPPINS, 38, INK, max_w=tw), W / 2, 205)
    rows = [3, 4, 3]
    i = 0
    for r, k in enumerate(rows):
        for c in range(k):
            m = A.fit(("g", i), A.front[i] if i % 2 == 0 else A.band[i], 240)
            paste_scaled(fr, m, W / 2 + (c - (k - 1) / 2) * 252, 420 + r * 265)
            i += 1
    paste_scaled(fr, pill("Your mate will know exactly what it says \U0001F602", POPPINS, 36, WHITE, INK,
                          max_w=tw), W / 2, 1290)
    fr.convert("RGB").save(os.path.join(out, "rude-mugs-carousel-2.jpg"), quality=92)

    # 3: end card
    fr = background(W, H, INK, (70, 40, 140)).convert("RGBA")
    paste_scaled(fr, wordmark(110), W / 2, 120)
    paste_scaled(fr, A.fit("s3", A.pair, 980), W / 2, 520)
    paste_scaled(fr, line_img("£7.99 · 11oz ceramic · printed in the UK", POPPINS, 44, WHITE,
                              max_w=tw), W / 2, 870)
    paste_scaled(fr, pill("Search: rude number plate mug", POPPINS, 46, WHITE, PINK, max_w=tw), W / 2, 990)
    paste_scaled(fr, line_img(URL, POPPINS, 76, ORANGE, max_w=tw), W / 2, 1120)
    paste_scaled(fr, line_img("18+ humour · GB, Scotland, Wales, NI & Ireland bands", POPPINS, 32,
                              lighten(INK, .55), max_w=tw), W / 2, 1230)
    fr.convert("RGB").save(os.path.join(out, "rude-mugs-carousel-3.jpg"), quality=92)


def main(mugs_dir, out):
    os.makedirs(out, exist_ok=True)
    A = Assets(mugs_dir)
    stills(A, out)
    for W, H, name in [(1080, 1920, "9x16"), (1080, 1080, "1x1")]:
        L = video(A, W, H, os.path.join(out, f"rude-mugs-ad-{name}.mp4"))
        render_frame(1.6, A, L).save(os.path.join(out, f"poster-{name}.jpg"), quality=90)
        print(name, "done", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 3:            # preview: MUGS_DIR OUT_PNG W H t
        A = Assets(sys.argv[1])
        L = Layout(int(sys.argv[3]), int(sys.argv[4]))
        render_frame(float(sys.argv[5]), A, L).save(sys.argv[2])
    else:
        main(sys.argv[1], sys.argv[2])
