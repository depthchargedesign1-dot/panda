"""Print-ready artwork + local mockups for the bar-mat pairing products (owner, 8 Oct 2026).

Products: club-colours coaster / pint glass / metal bar sign (17 team colourways, customer uploads
their own badge), themed personalised pint glasses, whisky tumblers and metal home bar signs that
match the bar mats made on 8 Oct 2026 (see exports/bar-mats/2026-10-08/).

Every design is a list of simple elements in millimetres on the TRIM area (origin top-left).
From one list we write:
  * <SKU> - <size> - PRINT.svg  layers "Artwork" (live text with ids named after the customer
    fields, font-family named), "CUT" (red trim path, UV DTF transfers only) and "Guides" (hidden)
  * <SKU> - <size> - PRINT.pdf  pure-ASCII PDF (A85, subset-embedded OFL fonts), layers Artwork/CUT
  * a PIL raster of the trim area for the product mockups.

Sizes (plan/artwork-specs.md + plan/product-facts.md):
  * coaster: 90 x 90 mm trim (square cork-backed MDF coaster, from the live coaster listings) + 3 mm bleed
  * metal sign: 12 x 5in = 304.8 x 127 mm and 8 x 10in = 203.2 x 254 mm (1.15mm gloss white aluminium,
    the live "Personalised Metal Pub Sign" sizes) + 3 mm bleed
  * UV DTF glass transfer: pint 70 x 90 mm, whisky tumbler 70 x 60 mm. ASK: the owner has not confirmed
    the maximum print area for the 20oz nonic pint or the whisky tumbler; change PINT / TUMBLER and re-run.
Sample name "Ava" is used in the print files (the owner's Illustrator script swaps it).

usage: python3 tools/artwork/bar_pairings.py OUT_DIR [mockup-name]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "assets", "fonts")
BEBAS = os.path.join(FONTS, "BebasNeue-Regular.ttf")
PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")
BARLOW = os.path.join(FONTS, "BarlowCondensed-SemiBold.ttf")
BARLOWB = os.path.join(FONTS, "BarlowCondensed-Bold.ttf")
FONT_NAME = {BEBAS: "Bebas Neue", PACIFICO: "Pacifico", BARLOW: "Barlow Condensed SemiBold",
             BARLOWB: "Barlow Condensed Bold"}
PDF_NAME = {BEBAS: "BebasNeue", PACIFICO: "Pacifico", BARLOW: "BarlowCondensed-SemiBold",
            BARLOWB: "BarlowCondensed-Bold"}
BLEED = 3.0
SAFE = 3.0
CUT_RED = "#FF0000"

COASTER = (90.0, 90.0)
SIGN_WIDE = (304.8, 127.0)
SIGN_TALL = (203.2, 254.0)
PINT = (70.0, 90.0)       # ASK
TUMBLER = (70.0, 60.0)    # ASK

# ------------------------------------------------------------------ club colourways (match the 17 club bar mats)
# key, label, main, accent, text-on-main, stripes ("v" vertical / "h" hoops / None), google colour
CLUB = [
    ("red_white", "Red & White", "#C8102E", "#FFFFFF", "#FFFFFF", None, "Red/White"),
    ("red_white_stripes", "Red & White Stripes", "#C8102E", "#FFFFFF", "#FFFFFF", "v", "Red/White"),
    ("blue_white", "Blue & White", "#1D4FA0", "#FFFFFF", "#FFFFFF", None, "Blue/White"),
    ("blue_white_stripes", "Blue & White Stripes", "#1D4FA0", "#FFFFFF", "#FFFFFF", "v", "Blue/White"),
    ("black_white_stripes", "Black & White Stripes", "#1A1A1A", "#FFFFFF", "#FFFFFF", "v", "Black/White"),
    ("green_white", "Green & White", "#2E8B3A", "#FFFFFF", "#FFFFFF", None, "Green/White"),
    ("green_white_hoops", "Green & White Hoops", "#2E8B3A", "#FFFFFF", "#FFFFFF", "h", "Green/White"),
    ("sky_blue_white", "Sky Blue & White", "#5DA9DD", "#FFFFFF", "#FFFFFF", None, "Blue/White"),
    ("navy_white", "Navy & White", "#1B2A4A", "#FFFFFF", "#FFFFFF", None, "Navy/White"),
    ("black_orange", "Black & Orange", "#EE7623", "#1A1A1A", "#1A1A1A", None, "Orange/Black"),
    ("black_yellow", "Black & Yellow", "#1A1A1A", "#F6C700", "#F6C700", None, "Black/Yellow"),
    ("yellow_black", "Yellow & Black", "#F6C700", "#1A1A1A", "#1A1A1A", None, "Yellow/Black"),
    ("blue_yellow", "Blue & Yellow", "#1D4FA0", "#F6C700", "#F6C700", None, "Blue/Yellow"),
    ("blue_red", "Blue & Red", "#1D4FA0", "#C8102E", "#FFFFFF", "v", "Blue/Red"),
    ("green_yellow", "Green & Yellow", "#F6C700", "#2E8B3A", "#2E8B3A", None, "Green/Yellow"),
    ("yellow_red", "Yellow & Red", "#F6C700", "#C8102E", "#C8102E", None, "Yellow/Red"),
    ("claret_blue", "Claret & Blue", "#7A263A", "#8EC5E8", "#FFFFFF", None, "Claret/Blue"),
]


# ------------------------------------------------------------------ element helpers
def rect(x, y, w, h, fill=None, stroke=None, sw=0.5, r=0):
    return dict(k="rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, r=r)


def circ(x, y, r, fill=None, stroke=None, sw=0.5, dash=None):
    return dict(k="circle", x=x, y=y, r=r, fill=fill, stroke=stroke, sw=sw, dash=dash)


def line(x1, y1, x2, y2, stroke, sw=0.5):
    return dict(k="line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, sw=sw)


def poly(pts, fill):
    return dict(k="poly", pts=pts, fill=fill)


def arc(x, y, r, a0, a1, stroke, sw=0.5):
    """arc centred x,y radius r from angle a0 to a1 (degrees, 0 = right, clockwise in y-down space)"""
    return dict(k="arc", x=x, y=y, r=r, a0=a0, a1=a1, stroke=stroke, sw=sw)


def clip(x, y, w, h, els, r=0):
    return dict(k="clip", x=x, y=y, w=w, h=h, r=r, els=els)


def text_w(font, size, s, sp=0.0):
    f = ImageFont.truetype(font, 400)
    return f.getlength(s) / 400 * size + sp * max(0, len(s) - 1)


def T(s, x, y, font, size, fill, sp=0.0, maxw=None, live=None):
    """centred text, baseline at y. Shrinks (and its spacing) to fit maxw."""
    if maxw:
        w = text_w(font, size, s, sp)
        if w > maxw:
            f = maxw / w
            size, sp = size * f, sp * f
    return dict(k="text", text=s, x=x, y=y, font=font, size=size, fill=fill, sp=sp, live=live)


def diamond(x, y, r, fill):
    return poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill)


def rule_with_diamond(cx, y, half, col, sw=0.5, d=1.6):
    return [line(cx - half, y, cx - d * 2, y, col, sw), line(cx + d * 2, y, cx + half, y, col, sw), diamond(cx, y, d, col)]


def bg(w, h, fill):
    return rect(-BLEED, -BLEED, w + 2 * BLEED, h + 2 * BLEED, fill=fill)


def grain(w, h, col, step):
    """subtle plank lines for the wood-look designs"""
    out = []
    y = -BLEED + step / 2
    i = 0
    while y < h + BLEED:
        out.append(line(-BLEED, y, w + BLEED, y + (0.6 if i % 2 else -0.6), col, 0.35))
        y += step
        i += 1
    return out


# ------------------------------------------------------------------ layout
def stack(w, h, lines, box=None, gap=0.28, fill_h=0.62, fill_w=0.76):
    """lines: list of (text, font, rel_size, colour, rel_spacing, live) or ('RULE', colour) / ('GAP', rel).
    Lays them out centred in box (x, y, bw, bh) scaled to fit."""
    bx, by, bw, bh = box or (0, 0, w, h)
    base = 10.0
    items = []
    for ln in lines:
        if ln[0] == "RULE":
            items.append(("RULE", ln[1], 0.5))
        elif ln[0] == "GAP":
            items.append(("GAP", None, ln[1]))
        else:
            items.append(ln)
    # total height at base scale
    def hh(scale):
        tot = 0
        for it in items:
            if it[0] == "RULE":
                tot += 3.2 * scale / base * base * 0.6
            elif it[0] == "GAP":
                tot += it[2] * base * scale
            else:
                tot += it[2] * base * scale * (1 + gap)
        return tot
    scale = bh * fill_h / hh(1.0)
    # width constraint
    for it in items:
        if it[0] in ("RULE", "GAP"):
            continue
        tw = text_w(it[1], it[2] * base * scale, it[0], it[4] * base * scale)
        if tw > bw * fill_w:
            scale *= bw * fill_w / tw
    els = []
    y = by + (bh - hh(scale)) / 2
    cx = bx + bw / 2
    for it in items:
        if it[0] == "RULE":
            y += 3.2 * scale * 0.3
            els += rule_with_diamond(cx, y, bw * 0.28, it[1], sw=max(0.3, 0.12 * scale), d=max(0.8, 0.4 * scale))
            y += 3.2 * scale * 0.3
        elif it[0] == "GAP":
            y += it[2] * base * scale
        else:
            s, font, rel, col, rsp, live = it
            size = rel * base * scale
            y += size * (1 + gap) * 0.86
            els.append(T(s, cx, y, font, size, col, rsp * base * scale, maxw=bw * fill_w, live=live))
            y += size * (1 + gap) * 0.14
    return els


# ------------------------------------------------------------------ union flag (drawn, CMYK-safe)
def union_flag(x, y, w, h):
    NAVY, RED, WHITE = "#1F3A6E", "#C8102E", "#FFFFFF"
    t = min(w, h)
    els = [rect(x, y, w, h, fill=NAVY)]
    for (x1, y1, x2, y2) in ((x, y, x + w, y + h), (x, y + h, x + w, y)):
        els.append(line(x1, y1, x2, y2, WHITE, t * 0.2))
        els.append(line(x1, y1, x2, y2, RED, t * 0.067))
    els.append(rect(x + w / 2 - t * 0.1666, y, t * 0.333, h, fill=WHITE))
    els.append(rect(x, y + h / 2 - t * 0.1666, w, t * 0.333, fill=WHITE))
    els.append(rect(x + w / 2 - t * 0.1, y, t * 0.2, h, fill=RED))
    els.append(rect(x, y + h / 2 - t * 0.1, w, t * 0.2, fill=RED))
    return [clip(x, y, w, h, els)]


# ------------------------------------------------------------------ badge placeholder / sample shield
def badge(cx, cy, r, ring, main, sample=False):
    els = [circ(cx, cy, r, fill="#FFFFFF", stroke=ring, sw=r * 0.12)]
    if sample:  # a generic made-up shield for the website mockup only (no real club)
        s = r * 0.62
        pts = [(cx - s, cy - s * 0.9), (cx + s, cy - s * 0.9), (cx + s, cy + s * 0.15), (cx, cy + s * 1.1), (cx - s, cy + s * 0.15)]
        els.append(poly(pts, main))
        els.append(poly([(cx - s * 0.62, cy - s * 0.55), (cx + s * 0.62, cy - s * 0.55), (cx + s * 0.62, cy + s * 0.05),
                         (cx, cy + s * 0.68), (cx - s * 0.62, cy + s * 0.05)], "#FFFFFF"))
        # five-point star
        star = []
        for i in range(10):
            a = math.radians(-90 + i * 36)
            rr = s * (0.42 if i % 2 == 0 else 0.17)
            star.append((cx + rr * math.cos(a), cy - s * 0.02 + rr * math.sin(a)))
        els.append(poly(star, main))
    else:
        els.append(circ(cx, cy, r * 0.8, stroke="#9A9A9A", sw=max(0.25, r * 0.02), dash=(1.5, 1.0)))
        els.append(T("YOUR BADGE", cx, cy - r * 0.02, BARLOW, r * 0.26, "#9A9A9A", maxw=r * 1.4, live="Club_badge_upload"))
        els.append(T("HERE", cx, cy + r * 0.3, BARLOW, r * 0.26, "#9A9A9A"))
    return els


# ------------------------------------------------------------------ themes
# p = dict(name=..., est=..., welcome=...), shape in coaster / pint / tumbler / wide / tall
def club(shape, w, h, p, cw, sample=False):
    key, label, main, acc, txt, stripes, _ = cw
    ring = acc if acc != "#FFFFFF" or main not in ("#FFFFFF",) else main
    els = []
    glass = shape in ("pint", "tumbler")
    R = 2.5 if glass else 0
    inner = []
    inner.append(rect(0, 0, w, h, fill=main, r=R) if glass else bg(w, h, main))
    if stripes == "v":
        n = 2
        bwid = min(w, h) * 0.035
        for i in range(n):
            for xx in (min(w, h) * 0.07 + i * bwid * 2.0, w - min(w, h) * 0.07 - i * bwid * 2.0 - bwid):
                inner.append(rect(xx, -BLEED, bwid, h + 2 * BLEED, fill=acc))
    elif stripes == "h":
        n = 2
        bh_ = min(w, h) * 0.035
        for i in range(n):
            for yy in (min(w, h) * 0.07 + i * bh_ * 2.0, h - min(w, h) * 0.07 - i * bh_ * 2.0 - bh_):
                inner.append(rect(-BLEED, yy, w + 2 * BLEED, bh_, fill=acc))
    m = min(w, h)
    inset = m * 0.05
    inner.append(rect(inset, inset, w - 2 * inset, h - 2 * inset, stroke=acc, sw=m * 0.012, r=R))
    welcome = p.get("welcome", "WELCOME TO")
    if shape == "wide":
        r = h * 0.27
        inner += badge(h * 0.46, h / 2, r, acc, main, sample) + badge(w - h * 0.46, h / 2, r, acc, main, sample)
        inner += stack(w, h, [(welcome, BARLOW, 0.32, txt, 0.12, "Welcome_line"), (p["name"], BEBAS, 1.25, txt, 0.04, "Club_or_team_name"),
                              (p["est"], BARLOW, 0.32, txt, 0.12, "Est_year")], box=(h * 0.78, 0, w - h * 1.56, h), fill_h=0.7, fill_w=0.92)
    else:
        if shape == "tall":
            r, cy, box = w * 0.26, h * 0.32, (0, h * 0.55, w, h * 0.38)
        elif shape == "coaster":
            r, cy, box = w * 0.2, h * 0.34, (0, h * 0.56, w, h * 0.36)
        elif shape == "pint":
            r, cy, box = w * 0.26, h * 0.3, (0, h * 0.54, w, h * 0.4)
        else:  # tumbler
            r, cy, box = h * 0.24, h * 0.3, (0, h * 0.54, w, h * 0.4)
        inner += badge(w / 2, cy, r, acc, main, sample)
        inner += stack(w, h, [(welcome, BARLOW, 0.3, txt, 0.12, "Welcome_line"), (p["name"], BEBAS, 1.1, txt, 0.04, "Club_or_team_name"),
                              (p["est"], BARLOW, 0.3, txt, 0.12, "Est_year")], box=box, fill_h=0.8,
                        fill_w=0.62 if stripes == "v" else 0.76)
    if glass:
        els.append(clip(0, 0, w, h, inner, r=R))
    else:
        els += inner
    return els


def themed(theme, shape, w, h, p, sample=False):
    glass = shape in ("pint", "tumbler")
    R = 2.5 if glass else 0
    m = min(w, h)
    els = []
    name, est, welcome = p["name"], p["est"], p.get("welcome", "WELCOME TO")

    def base(fill):
        return rect(0, 0, w, h, fill=fill, r=R) if glass else bg(w, h, fill)

    if theme == "rustic":
        BR, GOLD, CREAM, DARK = "#4A2E1A", "#C9A24A", "#F1E6CF", "#3B2414"
        els += [base(BR)] + grain(w, h, DARK, m * 0.11)
        els += [rect(m * 0.04, m * 0.04, w - m * 0.08, h - m * 0.08, stroke=GOLD, sw=m * 0.01, r=R),
                rect(m * 0.065, m * 0.065, w - m * 0.13, h - m * 0.13, stroke=GOLD, sw=m * 0.004, r=R)]
        for (x, y) in ((m * 0.065, m * 0.065), (w - m * 0.065, m * 0.065), (m * 0.065, h - m * 0.065), (w - m * 0.065, h - m * 0.065)):
            els.append(diamond(x, y, m * 0.02, GOLD))
        els += stack(w, h, [(welcome, BARLOW, 0.3, GOLD, 0.16, "Welcome_line"), ("RULE", GOLD), (name, BARLOW, 1.0, CREAM, 0.1, "Bar_name"),
                            ("RULE", GOLD), ("ESTABLISHED " + est, BARLOW, 0.3, GOLD, 0.16, "Est_year")], fill_h=0.66 if shape != "wide" else 0.7)
    elif theme == "vintage_black":
        BK, WH = "#141414", "#F2F2F2"
        els.append(base(BK))
        els.append(rect(m * 0.05, m * 0.05, w - m * 0.1, h - m * 0.1, stroke=WH, sw=m * 0.005, r=R))
        rr = m * 0.09
        for (x, y, a0) in ((m * 0.05, m * 0.05, 0), (w - m * 0.05, m * 0.05, 90), (w - m * 0.05, h - m * 0.05, 180), (m * 0.05, h - m * 0.05, 270)):
            els.append(arc(x, y, rr, a0, a0 + 90, WH, m * 0.006))
            els.append(arc(x, y, rr * 0.6, a0, a0 + 90, WH, m * 0.004))
        els += stack(w, h, [(welcome, BARLOW, 0.3, WH, 0.12, "Welcome_line"), (name, BARLOW, 1.0, WH, 0.03, "Bar_name"),
                            ("Established " + est, BARLOW, 0.32, WH, 0.04, "Est_year")], fill_h=0.6)
    elif theme == "walnut":
        WN, GOLD, DARK = "#2E1C11", "#D4AF5A", "#24150C"
        els += [base(WN)] + grain(w, h, DARK, m * 0.08)
        els.append(rect(m * 0.05, m * 0.05, w - m * 0.1, h - m * 0.1, stroke=GOLD, sw=m * 0.006, r=R))
        # chevron points top and bottom
        cw_ = min(w * 0.18, m * 0.4)
        els.append(poly([(w / 2 - cw_, m * 0.05), (w / 2 + cw_, m * 0.05), (w / 2, m * 0.13)], GOLD))
        els.append(poly([(w / 2 - cw_, h - m * 0.05), (w / 2 + cw_, h - m * 0.05), (w / 2, h - m * 0.13)], GOLD))
        for (x, y) in ((m * 0.1, m * 0.1), (w - m * 0.1, m * 0.1), (m * 0.1, h - m * 0.1), (w - m * 0.1, h - m * 0.1)):
            els.append(circ(x, y, m * 0.018, fill=GOLD))
        els += stack(w, h, [(welcome, BARLOW, 0.28, GOLD, 0.2, "Welcome_line"), (name, BARLOW, 1.0, GOLD, 0.22, "Bar_name"),
                            ("EST. " + est, BARLOW, 0.3, GOLD, 0.2, "Est_year")], fill_h=0.55)
    elif theme in ("my_rules", "my_cave_rules"):
        NV, YL, WH = "#262A78", "#F2C230", "#FFFFFF"
        els.append(base(NV))
        for y in (m * 0.12, h - m * 0.12):
            els.append(line(m * 0.06, y, w - m * 0.06, y, YL, m * 0.012))
            for x in (w * 0.2, w / 2, w * 0.8):
                els.append(diamond(x, y, m * 0.03, YL))
        word = "CAVE" if theme == "my_cave_rules" else "BAR"
        els += stack(w, h, [(name, BARLOW, 0.42, WH, 0.1, "Name"), ("MY " + word, BEBAS, 1.0, WH, 0.04, None),
                            ("MY RULES", BEBAS, 1.0, YL, 0.04, None), ("EST. " + est, BARLOW, 0.3, YL, 0.16, "Est_year")],
                        fill_h=0.62, gap=0.18)
    elif theme == "man_cave":
        CH, GOLD, CREAM = "#2D2D2F", "#E0A526", "#F3E9D2"
        els.append(base(CH))
        sw_ = m * 0.05
        for y in (m * 0.07, h - m * 0.07 - sw_):
            for i in range(4):
                for x0 in (m * 0.07 + i * sw_ * 0.9, w - m * 0.07 - (i + 1) * sw_ * 0.9):
                    els.append(poly([(x0 + sw_ * 0.35, y), (x0 + sw_ * 0.7, y), (x0 + sw_ * 0.35, y + sw_), (x0, y + sw_)], GOLD))
        els += stack(w, h, [("WELCOME", BARLOW, 0.3, CREAM, 0.3, None), (name, BARLOW, 0.5, GOLD, 0.12, "Name"),
                            ("MAN CAVE", BARLOW, 1.0, CREAM, 0.32, None), ("EST. " + est, BARLOW, 0.3, CREAM, 0.3, "Est_year")],
                        fill_h=0.58)
    elif theme == "beer":
        OR, CR, LO = "#C8641E", "#FBF1DC", "#D9823F"
        els.append(base(OR))
        # bubbles
        import random
        rnd = random.Random(7)
        for _ in range(int(w * h / 90)):
            els.append(circ(rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0.006, 0.02) * m, fill=LO))
        els.append(rect(m * 0.06, m * 0.06, w - m * 0.12, h - m * 0.12, stroke=CR, sw=m * 0.012, r=R))
        els += stack(w, h, [("IT’S", BEBAS, 0.36, CR, 0.1, None), ("Beer", PACIFICO, 1.0, CR, 0.0, None),
                            ("O’CLOCK", BEBAS, 0.62, CR, 0.12, None), ("GAP", 0.12), ("AT " + name, BARLOW, 0.34, CR, 0.1, "Bar_name")],
                        fill_h=0.7, gap=0.12)
    elif theme == "union":
        WH, BK = "#FFFFFF", "#1A1A1A"
        if glass:
            els.append(clip(0, 0, w, h, union_flag(-1, -1, w + 2, h + 2), r=R))
        else:
            els += union_flag(-BLEED, -BLEED, w + 2 * BLEED, h + 2 * BLEED)
        if shape == "wide":
            pw, ph = w * 0.5, h * 0.5
        elif shape == "tall":
            pw, ph = w * 0.78, h * 0.4
        else:
            pw, ph = w * 0.8, h * 0.52 if shape != "pint" else h * 0.44
        px, py = (w - pw) / 2, (h - ph) / 2
        els.append(rect(px, py, pw, ph, fill=WH, stroke=BK, sw=m * 0.012))
        els.append(rect(px + m * 0.02, py + m * 0.02, pw - m * 0.04, ph - m * 0.04, stroke=BK, sw=m * 0.004))
        els += stack(w, h, [(welcome, BARLOW, 0.3, BK, 0.14, "Welcome_line"), (name, BEBAS, 1.0, BK, 0.04, "Bar_name"),
                            ("EST. " + est, BARLOW, 0.3, BK, 0.14, "Est_year")], box=(px, py, pw, ph), fill_h=0.72)
    elif theme == "best_bar":
        CRM, BRN, LBR = "#F3ECDF", "#5A3A22", "#A57C55"
        els.append(base(CRM))
        els.append(rect(m * 0.05, m * 0.05, w - m * 0.1, h - m * 0.1, stroke=LBR, sw=m * 0.006, r=R))
        lines_ = [("Welcome to the", PACIFICO, 0.45, BRN, 0.0, "Welcome_line"), ("BEST BAR", BARLOW, 0.9, BRN, 0.16, None),
                  ("IN TOWN", BARLOW, 0.5, BRN, 0.3, None), ("GAP", 0.5)]
        st = stack(w, h, lines_, box=(0, 0, w, h * 0.78), fill_h=0.72)
        els += st
        bh_ = h * (0.16 if shape != "wide" else 0.18)
        by_ = h * 0.66 if shape != "wide" else h * 0.64
        bw_ = w * 0.7
        els.append(rect((w - bw_) / 2, by_, bw_, bh_, fill=BRN, r=R * 0.5))
        els += stack(w, h, [(name + "  |  EST. " + est, BARLOW, 1.0, CRM, 0.14, "Bar_name")], box=((w - bw_) / 2, by_, bw_, bh_), fill_h=0.5)
    else:
        raise KeyError(theme)
    if glass:
        return [clip(0, 0, w, h, els, r=R)]
    return els


# ------------------------------------------------------------------ SVG / PDF / raster writers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg_el(e, o, out, defs, cid):
    k = e["k"]
    if k == "clip":
        cid[0] += 1
        i = f"c{cid[0]}"
        defs.append(f'<clipPath id="{i}"><rect x="{e["x"] + o:.2f}" y="{e["y"] + o:.2f}" width="{e["w"]:.2f}" height="{e["h"]:.2f}" rx="{e["r"]:.2f}"/></clipPath>')
        out.append(f'<g clip-path="url(#{i})">')
        for s in e["els"]:
            _svg_el(s, o, out, defs, cid)
        out.append('</g>')
        return
    st = lambda: (f' fill="{e["fill"]}"' if e.get("fill") else ' fill="none"') + (
        f' stroke="{e["stroke"]}" stroke-width="{e["sw"]:.2f}"' if e.get("stroke") else "")
    if k == "rect":
        out.append(f'<rect x="{e["x"] + o:.2f}" y="{e["y"] + o:.2f}" width="{e["w"]:.2f}" height="{e["h"]:.2f}" rx="{e["r"]:.2f}"{st()}/>')
    elif k == "circle":
        d = f' stroke-dasharray="{e["dash"][0]} {e["dash"][1]}"' if e.get("dash") else ""
        out.append(f'<circle cx="{e["x"] + o:.2f}" cy="{e["y"] + o:.2f}" r="{e["r"]:.2f}"{st()}{d}/>')
    elif k == "line":
        out.append(f'<line x1="{e["x1"] + o:.2f}" y1="{e["y1"] + o:.2f}" x2="{e["x2"] + o:.2f}" y2="{e["y2"] + o:.2f}" stroke="{e["stroke"]}" stroke-width="{e["sw"]:.2f}"/>')
    elif k == "poly":
        pts = " ".join(f"{x + o:.2f},{y + o:.2f}" for x, y in e["pts"])
        out.append(f'<polygon points="{pts}" fill="{e["fill"]}"/>')
    elif k == "arc":
        a0, a1 = math.radians(e["a0"]), math.radians(e["a1"])
        x0, y0 = e["x"] + o + e["r"] * math.cos(a0), e["y"] + o + e["r"] * math.sin(a0)
        x1, y1 = e["x"] + o + e["r"] * math.cos(a1), e["y"] + o + e["r"] * math.sin(a1)
        out.append(f'<path d="M {x0:.2f} {y0:.2f} A {e["r"]:.2f} {e["r"]:.2f} 0 0 1 {x1:.2f} {y1:.2f}" fill="none" stroke="{e["stroke"]}" stroke-width="{e["sw"]:.2f}"/>')
    elif k == "text":
        idt = f' id="{e["live"]}"' if e.get("live") else ""
        sp = f' letter-spacing="{e["sp"]:.2f}"' if e["sp"] else ""
        out.append(f'<text{idt} x="{e["x"] + o:.2f}" y="{e["y"] + o:.2f}" font-family="{FONT_NAME[e["font"]]}" font-size="{e["size"]:.2f}" '
                   f'text-anchor="middle"{sp} fill="{e["fill"]}">{esc(e["text"])}</text>')


def write_svg(els, w, h, path, cut=None):
    o = BLEED
    W, H = w + 2 * o, h + 2 * o
    out, defs, cid = [], [], [0]
    for e in els:
        _svg_el(e, o, out, defs, cid)
    a = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">']
    if defs:
        a.append("<defs>" + "".join(defs) + "</defs>")
    a.append('<g id="Artwork">')
    a += out
    a.append("</g>")
    if cut:
        a.append(f'<g id="CUT"><rect x="{o:.2f}" y="{o:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{cut:.2f}" fill="none" stroke="{CUT_RED}" stroke-width="0.25"/></g>')
    a.append('<g id="Guides" style="display:none">')
    a.append(f'<rect x="{o}" y="{o}" width="{w}" height="{h}" fill="none" stroke="#00AEEF" stroke-width="0.2"/>')
    a.append(f'<rect x="{o + SAFE}" y="{o + SAFE}" width="{w - 2 * SAFE}" height="{h - 2 * SAFE}" fill="none" stroke="#EC008C" stroke-width="0.2" stroke-dasharray="1 1"/>')
    a.append("</g></svg>")
    open(path, "w").write("\n".join(a))


def write_pdf(els, w, h, path, title, cut=None):
    from reportlab import rl_config
    rl_config.useA85 = 1
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    for f, n in PDF_NAME.items():
        try:
            pdfmetrics.getFont(n)
        except KeyError:
            pdfmetrics.registerFont(TTFont(n, f))
    o = BLEED
    W, H = w + 2 * o, h + 2 * o
    c = canvas.Canvas(path, pagesize=(W * mm, H * mm), pageCompression=0)
    c.setTitle(title)
    c.setAuthor("Foxy Printing")
    X = lambda v: (v + o) * mm
    Y = lambda v: (H - (v + o)) * mm

    def draw(e):
        k = e["k"]
        if k == "clip":
            c.saveState()
            p = c.beginPath()
            if e["r"]:
                p.roundRect(X(e["x"]), Y(e["y"] + e["h"]), e["w"] * mm, e["h"] * mm, e["r"] * mm)
            else:
                p.rect(X(e["x"]), Y(e["y"] + e["h"]), e["w"] * mm, e["h"] * mm)
            c.clipPath(p, stroke=0, fill=0)
            for s in e["els"]:
                draw(s)
            c.restoreState()
            return
        if e.get("fill"):
            c.setFillColor(HexColor(e["fill"]))
        if e.get("stroke"):
            c.setStrokeColor(HexColor(e["stroke"]))
            c.setLineWidth(e["sw"] * mm)
        f, s = (1 if e.get("fill") else 0), (1 if e.get("stroke") else 0)
        if k == "rect":
            if e["r"]:
                c.roundRect(X(e["x"]), Y(e["y"] + e["h"]), e["w"] * mm, e["h"] * mm, e["r"] * mm, stroke=s, fill=f)
            else:
                c.rect(X(e["x"]), Y(e["y"] + e["h"]), e["w"] * mm, e["h"] * mm, stroke=s, fill=f)
        elif k == "circle":
            if e.get("dash"):
                c.setDash(e["dash"][0] * mm, e["dash"][1] * mm)
            c.circle(X(e["x"]), Y(e["y"]), e["r"] * mm, stroke=s, fill=f)
            c.setDash()
        elif k == "line":
            c.line(X(e["x1"]), Y(e["y1"]), X(e["x2"]), Y(e["y2"]))
        elif k == "poly":
            p = c.beginPath()
            p.moveTo(X(e["pts"][0][0]), Y(e["pts"][0][1]))
            for x, y in e["pts"][1:]:
                p.lineTo(X(x), Y(y))
            p.close()
            c.drawPath(p, stroke=0, fill=1)
        elif k == "arc":
            r = e["r"]
            # reportlab angles are counter-clockwise in y-up space = clockwise in our y-down space, negate
            c.arc(X(e["x"] - r), Y(e["y"] + r), X(e["x"] + r), Y(e["y"] - r), -e["a0"], -(e["a1"] - e["a0"]))
        elif k == "text":
            fn = PDF_NAME[e["font"]]
            size = e["size"] * mm
            sp = e["sp"] * mm
            tw = pdfmetrics.stringWidth(e["text"], fn, size) + sp * (len(e["text"]) - 1)
            t = c.beginText(X(e["x"]) - tw / 2, Y(e["y"]))
            t.setFont(fn, size)
            t.setCharSpace(sp)
            t.textOut(e["text"])
            c.drawText(t)

    for e in els:
        draw(e)
    if cut:
        c.setStrokeColor(HexColor(CUT_RED))
        c.setLineWidth(0.25 * mm)
        c.roundRect(X(0), Y(h), w * mm, h * mm, cut * mm, stroke=1, fill=0)
    c.showPage()
    c.save()
    layer_pdf(path, bool(cut))
    ascii_pdf(path)


def layer_pdf(path, has_cut):
    """Split the page content into optional-content layers Artwork / CUT (the cut path is the last
    roundRect drawn, after the final 'RG' colour set)."""
    import pikepdf
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    page = pdf.pages[0]
    data = page.Contents.read_bytes() if not isinstance(page.Contents, pikepdf.Array) else b"".join(s.read_bytes() for s in page.Contents)
    ocg_art = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=pikepdf.String("Artwork")))
    ocgs = [ocg_art]
    props = pikepdf.Dictionary(Art=ocg_art)
    if has_cut:
        ocg_cut = pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=pikepdf.String("CUT")))
        ocgs.append(ocg_cut)
        props.Cut = ocg_cut
        i = data.rfind(b"1 0 0 RG")
        art, cut = data[:i], data[i:]
        new = b"/OC /Art BDC\n" + art + b"\nEMC\n/OC /Cut BDC\n" + cut + b"\nEMC\n"
    else:
        new = b"/OC /Art BDC\n" + data + b"\nEMC\n"
    page.Contents = pdf.make_stream(new)
    res = page.Resources
    res.Properties = props
    pdf.Root.OCProperties = pikepdf.Dictionary(OCGs=pikepdf.Array(ocgs), D=pikepdf.Dictionary(Order=pikepdf.Array(ocgs), ON=pikepdf.Array(ocgs)))
    pdf.save(path)


def ascii_pdf(path):
    import base64
    import pikepdf
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream):
            raw = obj.read_raw_bytes()
            if any(x >= 128 or (x < 32 and x not in (9, 10, 13)) for x in raw):
                filt = obj.get("/Filter")
                filters = [] if filt is None else (list(filt) if isinstance(filt, pikepdf.Array) else [filt])
                obj.write(base64.a85encode(raw, wrapcol=76) + b"~>", filter=[pikepdf.Name.ASCII85Decode] + filters)
    pdf.save(path, compress_streams=False, object_stream_mode=pikepdf.ObjectStreamMode.disable,
             stream_decode_level=pikepdf.StreamDecodeLevel.none)
    b = bytearray(open(path, "rb").read())
    for i in range(min(80, len(b))):
        if b[i] >= 128:
            b[i] = ord("~")
    assert all(x < 128 for x in b), "PDF not pure ASCII"
    open(path, "wb").write(bytes(b))


# ---- raster
_fc = {}


def _font(path, px):
    key = (path, int(px))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(path, max(1, int(px)))
    return _fc[key]


def raster(els, w, h, pxmm=12, bleed=False, transparent=False):
    o = BLEED if bleed else 0
    W, H = round((w + 2 * o) * pxmm), round((h + 2 * o) * pxmm)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0) if transparent else (255, 255, 255, 255))
    _draw_list(img, els, o, pxmm)
    return img


def _rgba(hexc):
    hexc = hexc.lstrip("#")
    return tuple(int(hexc[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def _draw_list(img, els, o, k):
    d = ImageDraw.Draw(img)
    P = lambda v: (v + o) * k
    for e in els:
        t = e["k"]
        if t == "clip":
            layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            _draw_list(layer, e["els"], o, k)
            mask = Image.new("L", img.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle([P(e["x"]), P(e["y"]), P(e["x"] + e["w"]), P(e["y"] + e["h"])], radius=e["r"] * k, fill=255)
            a = layer.split()[3]
            from PIL import ImageChops
            layer.putalpha(ImageChops.multiply(a, mask))
            img.alpha_composite(layer)
            d = ImageDraw.Draw(img)
            continue
        fill = _rgba(e["fill"]) if e.get("fill") else None
        stroke = _rgba(e["stroke"]) if e.get("stroke") else None
        swp = max(1, round(e.get("sw", 0) * k)) if stroke else 0
        if t == "rect":
            box = [P(e["x"]), P(e["y"]), P(e["x"] + e["w"]), P(e["y"] + e["h"])]
            if fill:
                d.rounded_rectangle(box, radius=e["r"] * k, fill=fill)
            if stroke:
                hw = swp / 2
                d.rounded_rectangle([box[0] - hw, box[1] - hw, box[2] + hw, box[3] + hw], radius=e["r"] * k, outline=stroke, width=swp)
        elif t == "circle":
            box = [P(e["x"] - e["r"]), P(e["y"] - e["r"]), P(e["x"] + e["r"]), P(e["y"] + e["r"])]
            if fill:
                d.ellipse(box, fill=fill)
            if stroke:
                if e.get("dash"):
                    n = int(2 * math.pi * e["r"] / sum(e["dash"]))
                    for i in range(n):
                        a0 = 360 * i / n
                        d.arc(box, a0, a0 + 360 / n * e["dash"][0] / sum(e["dash"]), fill=stroke, width=swp)
                else:
                    hw = swp / 2
                    d.ellipse([box[0] - hw, box[1] - hw, box[2] + hw, box[3] + hw], outline=stroke, width=swp)
        elif t == "line":
            d.line([P(e["x1"]), P(e["y1"]), P(e["x2"]), P(e["y2"])], fill=stroke, width=swp)
        elif t == "poly":
            d.polygon([(P(x), P(y)) for x, y in e["pts"]], fill=fill)
        elif t == "arc":
            r = e["r"]
            d.arc([P(e["x"] - r), P(e["y"] - r), P(e["x"] + r), P(e["y"] + r)], e["a0"], e["a1"], fill=stroke, width=swp)
        elif t == "text":
            f = _font(e["font"], e["size"] * k)
            col = _rgba(e["fill"])
            sp = e["sp"] * k
            tw = f.getlength(e["text"]) + sp * (len(e["text"]) - 1)
            x = P(e["x"]) - tw / 2
            y = P(e["y"])
            if sp:
                for ch in e["text"]:
                    d.text((x, y), ch, font=f, fill=col, anchor="ls")
                    x += f.getlength(ch) + sp
            else:
                d.text((x, y), e["text"], font=f, fill=col, anchor="ls")


# ------------------------------------------------------------------ mockups (2000 x 2000)
N = 2000


def _shadow(size, box, radius, blur=30, offset=(14, 26), alpha=90):
    sh = Image.new("L", size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1]], radius=radius, fill=alpha)
    return sh.filter(ImageFilter.GaussianBlur(blur))


def round_corners(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=r, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m)
    return im


def mock_coaster(tex):
    """tex: RGBA trim-area raster (square). Coaster on a cork base, like the live coaster photos."""
    img = Image.new("RGBA", (N, N), (255, 255, 255, 255))
    s = 1300
    x, y = 260, 240
    # cork base offset down-right
    import random
    rnd = random.Random(3)
    cork = Image.new("RGBA", (s, s), (205, 168, 120, 255))
    cd = ImageDraw.Draw(cork)
    for _ in range(9000):
        px, py = rnd.randrange(s), rnd.randrange(s)
        c = rnd.choice([(178, 140, 95), (222, 190, 148), (160, 122, 80)])
        cd.ellipse([px, py, px + rnd.randint(2, 6), py + rnd.randint(2, 6)], fill=c + (255,))
    cork = round_corners(cork, 70)
    img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (N, N), (0, 0, 0)).split(), _shadow((N, N), (x + 170, y + 190, x + 170 + s, y + 190 + s), 70))))
    img.alpha_composite(cork, (x + 170, y + 190))
    face = round_corners(tex.resize((s, s), Image.LANCZOS), 70)
    img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (N, N), (0, 0, 0)).split(), _shadow((N, N), (x, y, x + s, y + s), 70, blur=18, offset=(6, 10), alpha=110))))
    img.alpha_composite(face, (x, y))
    # thin edge + gloss
    ImageDraw.Draw(img).rounded_rectangle([x, y, x + s, y + s], radius=70, outline=(120, 120, 120, 255), width=4)
    gl = Image.new("L", (s, s), 0)
    gd = ImageDraw.Draw(gl)
    gd.polygon([(0, 0), (s * 0.55, 0), (0, s * 0.55)], fill=38)
    gl = gl.filter(ImageFilter.GaussianBlur(60))
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=70, fill=255)
    from PIL import ImageChops
    white = Image.new("RGBA", (s, s), (255, 255, 255, 255))
    white.putalpha(ImageChops.multiply(gl, m))
    img.alpha_composite(white, (x, y))
    return img.convert("RGB")


def mock_sign(tex, wide):
    img = Image.new("RGBA", (N, N), (255, 255, 255, 255))
    if wide:
        sw_ = 1760
        sh_ = round(sw_ * tex.height / tex.width)
    else:
        sh_ = 1700
        sw_ = round(sh_ * tex.width / tex.height)
    x, y = (N - sw_) // 2, (N - sh_) // 2 - 20
    r = 26
    img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (N, N), (0, 0, 0)).split(), _shadow((N, N), (x, y, x + sw_, y + sh_), r, blur=26, offset=(10, 22), alpha=95))))
    face = round_corners(tex.resize((sw_, sh_), Image.LANCZOS), r)
    img.alpha_composite(face, (x, y))
    # metallic sheen
    from PIL import ImageChops
    gl = Image.new("L", (sw_, sh_), 0)
    ImageDraw.Draw(gl).polygon([(sw_ * 0.15, 0), (sw_ * 0.32, 0), (sw_ * 0.17, sh_), (0, sh_)], fill=30)
    gl = gl.filter(ImageFilter.GaussianBlur(40))
    m = Image.new("L", (sw_, sh_), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, sw_ - 1, sh_ - 1], radius=r, fill=255)
    wl = Image.new("RGBA", (sw_, sh_), (255, 255, 255, 255))
    wl.putalpha(ImageChops.multiply(gl, m))
    img.alpha_composite(wl, (x, y))
    ImageDraw.Draw(img).rounded_rectangle([x, y, x + sw_, y + sh_], radius=r, outline=(170, 170, 170, 255), width=3)
    return img.convert("RGB")


def _cyl_warp(tex, out_w):
    """squash the transfer horizontally as if wrapped round a cylinder (front view)."""
    import numpy as np
    a = np.asarray(tex.convert("RGBA")).astype(np.float32)
    h, w = a.shape[:2]
    # transfer covers +-60 degrees of the glass
    th = np.linspace(-1, 1, out_w)
    ang = np.radians(62)
    src = (np.arcsin(np.clip(th, -1, 1) * math.sin(ang)) / ang + 1) / 2 * (w - 1)
    xi = np.clip(src.astype(int), 0, w - 1)
    out = a[:, xi, :]
    shade = 0.82 + 0.18 * np.cos(th * ang)
    out[:, :, :3] *= shade[None, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"), "RGBA")


def mock_glass(tex, kind):
    """kind pint (20oz nonic with beer) or tumbler (rocks glass with whisky). tex = transparent RGBA transfer."""
    img = Image.new("RGBA", (N, N), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    if kind == "pint":
        top, bot, cx = 300, 1780, N // 2
        wt, wb, bulge_y, bulge = 640, 500, 470, 34
        def half(y):
            if y < bulge_y:
                return wt / 2 + (y - top) / (bulge_y - top) * bulge * 0.5
            if y < bulge_y + 120:
                return wt / 2 + bulge * 0.5 - (y - bulge_y) / 120 * bulge * 0.6
            t = (y - bulge_y - 120) / (bot - bulge_y - 120)
            return (wt / 2 + bulge * 0.5 - bulge * 0.6) * (1 - t) + wb / 2 * t
        liquid_top, foam = 470, (225, 214, 190)
        drink = [(219, 150, 40), (180, 105, 20)]
        tw_mm, tex_px = 70.0, 600
        ty = 1010
    else:
        top, bot, cx = 700, 1700, N // 2
        wt, wb = 860, 800
        def half(y):
            t = (y - top) / (bot - top)
            return wt / 2 * (1 - t) + wb / 2 * t
        liquid_top, foam = 1260, None
        drink = [(196, 120, 40), (150, 80, 22)]
        tw_mm, tex_px = 70.0, 640
        ty = 1150
    # shadow
    sh = Image.new("L", (N, N), 0)
    ImageDraw.Draw(sh).ellipse([cx - wb / 2 - 40, bot - 30, cx + wb / 2 + 60, bot + 50], fill=110)
    img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (N, N), (0, 0, 0)).split(), sh.filter(ImageFilter.GaussianBlur(28)))))
    pts_l = [(cx - half(y), y) for y in range(top, bot + 1, 10)]
    pts_r = [(cx + half(y), y) for y in range(bot, top - 1, -10)]
    body = Image.new("L", (N, N), 0)
    ImageDraw.Draw(body).polygon(pts_l + pts_r, fill=255)
    # glass tint
    glass = Image.new("RGBA", (N, N), (232, 238, 240, 255))
    glass.putalpha(body.point(lambda v: v * 0.55))
    img.alpha_composite(glass)
    # liquid
    base_h = 70 if kind == "pint" else 120
    liq = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ld = ImageDraw.Draw(liq)
    for y in range(liquid_top, bot - base_h):
        t = (y - liquid_top) / (bot - base_h - liquid_top)
        c = tuple(int(drink[0][i] * (1 - t) + drink[1][i] * t) for i in range(3))
        hw = half(y) - 14
        ld.line([(cx - hw, y), (cx + hw, y)], fill=c + (235,))
    if foam:
        for y in range(top + 14, liquid_top):
            hw = half(y) - 12
            ld.line([(cx - hw, y), (cx + hw, y)], fill=foam + (255,))
        ld.ellipse([cx - half(top) + 12, top - 10, cx + half(top) - 12, top + 40], fill=(240, 233, 214, 255))
    img.alpha_composite(liq)
    if kind == "tumbler":
        # ice cubes
        for (x0, y0, s_) in ((cx - 250, liquid_top - 90, 230), (cx + 20, liquid_top - 60, 210)):
            ice = Image.new("RGBA", (N, N), (0, 0, 0, 0))
            ImageDraw.Draw(ice).rounded_rectangle([x0, y0, x0 + s_, y0 + s_], radius=30, fill=(235, 240, 242, 150), outline=(255, 255, 255, 200), width=5)
            img.alpha_composite(ice)
        # thick base
        bd = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        ImageDraw.Draw(bd).rectangle([cx - half(bot - 60) + 6, bot - base_h, cx + half(bot - 60) - 6, bot], fill=(214, 224, 228, 200))
        img.alpha_composite(bd)
    # transfer
    w_px = tex_px
    tw = _cyl_warp(tex, w_px)
    th_px = round(tex.height * (w_px / tex.width) * 1.0)
    tw = tw.resize((w_px, th_px), Image.LANCZOS)
    img.alpha_composite(tw, (cx - w_px // 2, ty - th_px // 2))
    # rim + outline + highlights
    hl = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.line(pts_l, fill=(150, 160, 165, 255), width=6)
    hd.line(pts_r, fill=(150, 160, 165, 255), width=6)
    hd.ellipse([cx - half(top), top - 18, cx + half(top), top + 18], outline=(160, 168, 172, 255), width=5)
    hd.line([(cx - half(bot), bot), (cx + half(bot), bot)], fill=(150, 160, 165, 255), width=8)
    for y in range(top + 40, bot - 40, 4):
        hd.line([(cx - half(y) + 40, y), (cx - half(y) + 70, y)], fill=(255, 255, 255, 70))
        hd.line([(cx + half(y) - 60, y), (cx + half(y) - 48, y)], fill=(255, 255, 255, 60))
    img.alpha_composite(hl)
    return img.convert("RGB")


def pair_image(product_img, mat_img, product_scale=0.62):
    """product mockup with the matching bar mat laid in front, on white (no text)."""
    img = Image.new("RGB", (N, N), (255, 255, 255))
    m = mat_img.convert("RGB")
    # trim white
    from PIL import ImageChops
    bgc = Image.new("RGB", m.size, (255, 255, 255))
    bb = ImageChops.difference(m, bgc).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if bb:
        m = m.crop(bb)
    m.thumbnail((1850, 760), Image.LANCZOS)
    p = product_img.copy()
    p = p.resize((round(N * product_scale), round(N * product_scale)), Image.LANCZOS)
    img.paste(p, ((N - p.width) // 2, 40))
    img.paste(m, ((N - m.width) // 2, N - m.height - 70))
    return img


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    p = dict(name="AVA’S BAR", est="2021")
    for th in ("rustic", "vintage_black", "walnut", "my_rules", "my_cave_rules", "man_cave", "beer", "union", "best_bar"):
        for shape, (w, h) in (("coaster", COASTER), ("pint", PINT), ("tumbler", TUMBLER), ("wide", SIGN_WIDE), ("tall", SIGN_TALL)):
            els = themed(th, shape, w, h, p)
            raster(els, w, h, pxmm=6, transparent=shape in ("pint", "tumbler")).save(f"{out}/{th}-{shape}.png")
    for shape, (w, h) in (("coaster", COASTER), ("pint", PINT), ("tumbler", TUMBLER), ("wide", SIGN_WIDE), ("tall", SIGN_TALL)):
        els = club(shape, w, h, dict(name="AVA’S FC", est="EST. 1987"), CLUB[1], sample=True)
        raster(els, w, h, pxmm=6, transparent=shape in ("pint", "tumbler")).save(f"{out}/club-{shape}.png")
