"""v3 clear-glass UV DTF designs for the 6 pint glasses and 4 whisky tumblers (owner, 9 Oct 2026).

Owner: "the pint glasses are wrong as youve full wrapped it, it just needs to be text and logos or images in
the middle of the glass" (with a reference photo: black and gold words printed straight onto a clear pint).
So no background panel, no frame: only the words and small motifs, in the theme's ink colours, centred in the
middle of the glass. Print area stays the owner's maximum (pint 90 x 130 mm, tumbler 50 x 50 mm) so the
transfer sits in the same place; the design itself is smaller and centred. UV DTF (white underbase under all ink).

usage: python3 tools/bar_pairings/glass_clear.py OUT_DIR
Writes OUT_DIR/<SKU prefix>/<SKU> - v3 clear <size> transfer [- colour] - PRINT.svg/.pdf (CUT trim on its own
layer, live text) and OUT_DIR/raster/<SKU>-01[-sample].png (transparent, 40 px/mm) for the photo composites.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools" / "artwork"))
import bar_pairings as A  # noqa: E402
import data as D  # noqa: E402

from bar_pairings import BARLOW, BARLOWB, BEBAS, PACIFICO, T, circ, diamond, line, poly, rect, stack, arc  # noqa: E402,F401

GOLD = "#B8892B"      # deeper gold so it reads on clear glass
INK = "#1A1A1A"
LABEL = {"pint": "v3 clear 90x130mm transfer", "tumbler": "v3 clear 50x50mm transfer"}


def box_for(shape, w, h):
    """design block centred in the print area (the middle of the glass)"""
    if shape == "pint":
        bw, bh = w * 0.58, h * 0.6  # ~52 x 78 mm: stays inside the clear front of the glass
    else:
        bw, bh = w * 0.92, h * 0.86
    return ((w - bw) / 2, (h - bh) / 2, bw, bh)


def dark(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b < 150


def club(shape, w, h, p, cw, sample):
    _, _, main, acc, _, _, _ = cw
    ink = main if dark(main) else (acc if dark(acc) else INK)
    second = acc if (acc != ink and acc != "#FFFFFF" and dark(acc)) else GOLD
    bx, by, bw, bh = box_for(shape, w, h)
    r = bw * 0.24
    cy = by + r + bh * 0.02
    els = A.badge(w / 2, cy, r, ink, main, sample)
    els[0] = circ(w / 2, cy, r, fill="#FFFFFF", stroke=ink, sw=r * 0.08)
    els += stack(w, h, [("WELCOME TO", BARLOW, 0.3, second, 0.14, "Welcome_line"), (p["name"], BEBAS, 1.15, ink, 0.04, "Club_or_team_name"),
                        ("RULE", second), (p["est"], BARLOW, 0.3, second, 0.14, "Est_year")],
                 box=(bx, cy + r * 1.15, bw, by + bh - (cy + r * 1.15)), fill_h=0.9, fill_w=0.9)
    return els


def themed(theme, shape, w, h, p, sample):
    name, est = p["name"], p["est"]
    bx, by, bw, bh = box = box_for(shape, w, h)
    m = min(bw, bh)
    els = []
    if theme == "rustic":
        BR = "#4A2E1A"
        els += stack(w, h, [("WELCOME TO", BARLOW, 0.3, GOLD, 0.16, "Welcome_line"), ("RULE", GOLD), (name, BARLOWB, 1.0, BR, 0.08, "Bar_name"),
                            ("RULE", GOLD), ("ESTABLISHED " + est, BARLOW, 0.3, GOLD, 0.16, "Est_year")], box=box, fill_h=0.62, fill_w=0.95)
    elif theme == "vintage_black":
        rr = m * 0.12
        for (x, y, a0) in ((bx, by, 0), (bx + bw, by, 90), (bx + bw, by + bh, 180), (bx, by + bh, 270)):
            els.append(arc(x, y, rr, a0, a0 + 90, INK, m * 0.012))
            els.append(arc(x, y, rr * 0.6, a0, a0 + 90, INK, m * 0.007))
        els += stack(w, h, [("WELCOME TO", BARLOW, 0.3, INK, 0.12, "Welcome_line"), (name, BARLOWB, 1.0, INK, 0.03, "Bar_name"),
                            ("Established " + est, BARLOW, 0.32, INK, 0.04, "Est_year")], box=box, fill_h=0.6, fill_w=0.86)
    elif theme == "walnut":
        WN = "#3A2414"
        cw_ = bw * 0.16
        els.append(poly([(w / 2 - cw_, by), (w / 2 + cw_, by), (w / 2, by + m * 0.09)], GOLD))
        els.append(poly([(w / 2 - cw_, by + bh), (w / 2 + cw_, by + bh), (w / 2, by + bh - m * 0.09)], GOLD))
        tq = 0.4 if shape == "tumbler" else 1.0
        els += stack(w, h, [("WELCOME TO", BARLOW, 0.28 / tq ** 0.35, GOLD, 0.2 * tq, "Welcome_line"), (name, BARLOWB, 1.0, WN, 0.12 * tq, "Bar_name"),
                            ("EST. " + est, BARLOW, 0.3 / tq ** 0.35, GOLD, 0.2 * tq, "Est_year")], box=box, fill_h=0.56, fill_w=0.9)
    elif theme in ("my_rules", "my_cave_rules"):
        NV = "#262A78"
        for y in (by + m * 0.04, by + bh - m * 0.04):
            els.append(line(bx + bw * 0.1, y, bx + bw * 0.9, y, GOLD, m * 0.014))
            for x in (bx + bw * 0.25, w / 2, bx + bw * 0.75):
                els.append(diamond(x, y, m * 0.035, GOLD))
        word = "CAVE" if theme == "my_cave_rules" else "BAR"
        els += stack(w, h, [(name, BARLOW, 0.42, NV, 0.1, "Name"), ("MY " + word, BEBAS, 1.0, NV, 0.04, None),
                            ("MY RULES", BEBAS, 1.0, GOLD, 0.04, None), ("EST. " + est, BARLOW, 0.3, NV, 0.16, "Est_year")],
                     box=box, fill_h=0.7, gap=0.16, fill_w=0.86)
    elif theme == "man_cave":
        CH = "#2D2D2F"
        sw_ = m * 0.07
        for y in (by, by + bh - sw_):
            for i in range(4):
                for x0 in (bx + i * sw_ * 0.9, bx + bw - (i + 1) * sw_ * 0.9):
                    els.append(poly([(x0 + sw_ * 0.35, y), (x0 + sw_ * 0.7, y), (x0 + sw_ * 0.35, y + sw_), (x0, y + sw_)], GOLD))
        tq = 0.35 if shape == "tumbler" else 1.0
        els += stack(w, h, [("WELCOME", BARLOW, 0.3 / tq ** 0.3, CH, 0.3 * tq, None), (name, BARLOWB, 0.5, GOLD, 0.12 * tq, "Name"),
                            ("MAN CAVE", BARLOWB, 1.0, CH, 0.24 * tq, None), ("EST. " + est, BARLOW, 0.3 / tq ** 0.3, CH, 0.3 * tq, "Est_year")],
                     box=(bx, by + sw_, bw, bh - 2 * sw_), fill_h=0.7, fill_w=0.9)
    elif theme == "beer":
        OR, DK, LO = "#C8641E", "#7A3A12", "#E2A15E"
        import random
        rnd = random.Random(7)
        for _ in range(14):  # a few bubbles rising above the words
            els.append(circ(rnd.uniform(bx + bw * 0.2, bx + bw * 0.8), rnd.uniform(by, by + bh * 0.16), rnd.uniform(0.012, 0.03) * m, stroke=LO, sw=m * 0.006))
        els += stack(w, h, [("IT’S", BEBAS, 0.36, DK, 0.1, None), ("Beer", PACIFICO, 1.0, OR, 0.0, None),
                            ("O’CLOCK", BEBAS, 0.62, DK, 0.12, None), ("GAP", 0.1), ("AT " + name, BARLOW, 0.34, OR, 0.1, "Bar_name")],
                     box=(bx, by + bh * 0.16, bw, bh * 0.84), fill_h=0.8, gap=0.12, fill_w=0.9)
    elif theme == "union":
        NV = "#1F3A6E"
        fw = bw * 0.62
        fh = fw * 0.5
        els += A.union_flag((w - fw) / 2, by, fw, fh)
        els += stack(w, h, [("WELCOME TO", BARLOW, 0.3, NV, 0.14, "Welcome_line"), (name, BEBAS, 1.0, NV, 0.04, "Bar_name"),
                            ("RULE", "#C8102E"), ("EST. " + est, BARLOW, 0.3, NV, 0.14, "Est_year")],
                     box=(bx, by + fh + m * 0.04, bw, bh - fh - m * 0.04), fill_h=0.84, fill_w=0.9)
    elif theme == "best_bar":
        BRN, LBR = "#5A3A22", "#A57C55"
        els += stack(w, h, [("Welcome to the", PACIFICO, 0.45, LBR, 0.0, "Welcome_line"), ("BEST BAR", BARLOWB, 0.9, BRN, 0.12, None),
                            ("IN TOWN", BARLOW, 0.5, BRN, 0.3, None), ("RULE", LBR), (name + "  |  EST. " + est, BARLOW, 0.28, BRN, 0.12, "Bar_name")],
                     box=box, fill_h=0.72, fill_w=0.95)
    else:
        raise KeyError(theme)
    return els


def design(p, cw=None, sample=False):
    shape = p["kind"]
    w, h = A.PINT if shape == "pint" else A.TUMBLER
    els = club(shape, w, h, p["art"], cw, sample) if p["theme"] == "club" else themed(p["theme"], shape, w, h, p["art"], sample)
    return els, w, h


def min_text_pt(els):
    return min((e["size"] / 25.4 * 72 for e in els if e["k"] == "text"), default=99)


def main():
    out = Path(sys.argv[1])
    (out / "raster").mkdir(parents=True, exist_ok=True)
    for p in D.P:
        if p["kind"] not in ("pint", "tumbler"):
            continue
        pre = f"FOXY-{p['machine']}-{p['code']}"
        d = out / pre
        d.mkdir(exist_ok=True)
        colours = A.CLUB if p["theme"] == "club" else [None]
        small = 99
        for n, cw in enumerate(colours, 1):
            sku = f"{pre}-{n:02d}"
            els, w, h = design(p, cw)
            small = min(small, min_text_pt(els))
            nm = (f"{sku} - {LABEL[p['kind']]}" + (f" - {cw[1]}" if cw else "") + " - PRINT").replace("&", "and")
            A.write_svg(els, w, h, str(d / f"{nm}.svg"), cut=2.5)
            A.write_pdf(els, w, h, str(d / f"{nm}.pdf"), p["title"] + " (v3 clear glass)", cut=2.5)
            if n == 1:
                A.raster(els, w, h, pxmm=40, transparent=True).save(out / "raster" / f"{sku}.png")
                if cw:  # made-up sample shield (no real club) for the website photo only
                    els_s, _, _ = design(p, cw, sample=True)
                    A.raster(els_s, w, h, pxmm=40, transparent=True).save(out / "raster" / f"{sku}-sample.png")
        print(p["key"], pre, len(colours), "files", f"smallest text {small:.1f}pt")


if __name__ == "__main__":
    main()
