"""8 new personalised pint glass designs (owner, 9 Oct 2026: "yes make all 8 and list on foxy").

Clear-glass UV DTF style (owner, 9 Oct 2026): only words, motifs and photos printed straight onto the clear
20oz nonic pint, centred in the middle of the glass, no background panel. Print area (owner, 8 Oct 2026):
90 x 130 mm max, 10 mm below the rim; these designs sit inside ~56 x 90 mm in the middle so they stay on the
clear front of the glass. Sample name "Ava"/"Smith" etc.; live text ids are the website field names.

Elements and writers come from tools/artwork/bar_pairings.py (SVG + layered ASCII PDF + raster).
usage: python3 tools/pint_range/designs.py OUT_DIR
"""
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools" / "artwork"))
import bar_pairings as A  # noqa: E402
from bar_pairings import BARLOW, BARLOWB, BEBAS, T, arc, circ, line, poly, rect  # noqa: E402

F = A.FONTS
GREATV = os.path.join(F, "GreatVibes-Regular.ttf")
ALLURA = os.path.join(F, "Allura-Regular.ttf")
CINZEL = os.path.join(F, "Cinzel-Bold.ttf")
CINZELR = os.path.join(F, "Cinzel-Regular.ttf")
MONTB = os.path.join(F, "Montserrat-Bold.ttf")
POPB = os.path.join(F, "Poppins-Bold.ttf")
for path, nm, pdf in ((GREATV, "Great Vibes", "GreatVibes"), (ALLURA, "Allura", "Allura"), (CINZEL, "Cinzel Bold", "Cinzel-Bold"),
                      (CINZELR, "Cinzel", "Cinzel-Regular"), (MONTB, "Montserrat Bold", "Montserrat-Bold"), (POPB, "Poppins Bold", "Poppins-Bold")):
    A.FONT_NAME[path] = nm
    A.PDF_NAME[path] = pdf

W, H = A.PINT          # 90 x 130 mm print area
CX = W / 2
INK = "#1A1A1A"
GOLD = "#B8892B"
NAVY = "#1F2D5C"


def fit(s, font, size, maxw, sp=0.0):
    w = A.text_w(font, size, s, sp)
    return size * min(1.0, maxw / w) if w else size


def photo_slot(cx, cy, rw, rh, label, live, stroke=INK):
    """Customer photo goes here (background removed, cut out with a thick outline). Print file placeholder."""
    els = [dict(k="ellipse", x=cx, y=cy, rx=rw, ry=rh, stroke="#9A9A9A", sw=0.4, dash=(1.6, 1.0))]
    els.append(T(label, cx, cy - 1.0, BARLOW, 4.0, "#9A9A9A", sp=0.4, live=live))
    els.append(T("HERE", cx, cy + 4.2, BARLOW, 4.0, "#9A9A9A", sp=0.4))
    return els


# ------------------------------------------------------------------ 1. Face photo "Hands Off!" pint
def face_pint(name="AVA’S", line2="HANDS OFF!"):
    els = photo_slot(CX, 52, 21, 26, "YOUR PHOTO", "Face_photo_upload")
    s = fit(name, POPB, 13.0, 56, 0.3)
    els.append(T(name, CX, 92, POPB, s, INK, sp=0.3, live="Name"))
    els.append(T("PINT", CX, 92 + s * 0.98, POPB, s, INK, sp=0.3))
    els.append(T(line2, CX, 92 + s * 0.98 + 7.5, POPB, 5.2, INK, sp=0.4, live="Bottom_line"))
    return els


# ------------------------------------------------------------------ 2. Big word + gold script name (owner's DAD reference)
def word_name_pint(word="DAD", name="Ava"):
    els = []
    s = fit(word, BEBAS, 44.0, 58, 0.5)
    els.append(T(word, CX, 70, BEBAS, s, INK, sp=0.5, live="Big_word"))
    n = fit(name, GREATV, 24.0, 60)
    els.append(T(name, CX + 2, 70 + n * 0.25, GREATV, n, GOLD, live="Name"))
    return els


# ------------------------------------------------------------------ 3. No.1 Grandad hexagon
def hexagon_pint(title="GRANDAD", name="AVA"):
    els = []
    hw, hh = 29.0, 36.0          # half width / half height of the hexagon
    top, bot = 66 - hh, 66 + hh
    # hexagon outline: flat top/bottom, vertical sides (8-point outline drawn as lines)
    pts = [(CX - hw, 66), (CX - hw * 0.55, top), (CX + hw * 0.55, top), (CX + hw, 66), (CX + hw * 0.55, bot), (CX - hw * 0.55, bot)]
    for i in range(6):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 6]
        els.append(line(x1, y1, x2, y2, INK, 0.7))
    els.append(poly([(CX - 11, top + 3), (CX + 11, top + 3), (CX, top + 10)], GOLD))
    els.append(poly([(CX - 11, bot - 3), (CX + 11, bot - 3), (CX, bot - 10)], GOLD))
    # "No" with a small raised underlined o, then a big 1 (laid out from the real glyph widths)
    wN, wo, w1 = A.text_w(CINZEL, 15.0, "N"), A.text_w(CINZEL, 8.0, "o"), A.text_w(CINZEL, 15.0, "1")
    x0 = CX - (wN + 0.6 + wo + 1.6 + w1) / 2
    els.append(T("N", x0 + wN / 2, 58, CINZEL, 15.0, INK))
    xo = x0 + wN + 0.6 + wo / 2
    els.append(T("o", xo, 52.5, CINZEL, 8.0, INK))
    els.append(line(xo - wo / 2, 55.0, xo + wo / 2, 55.0, INK, 0.8))
    els.append(T("1", x0 + wN + 0.6 + wo + 1.6 + w1 / 2, 58, CINZEL, 15.0, INK))
    s = fit(title, CINZEL, 9.0, 46, 0.6)
    els.append(T(title, CX, 70, CINZEL, s, INK, sp=0.6, live="Title"))
    # arrow
    y = 75.5
    els.append(line(CX - 18, y, CX + 17, y, GOLD, 0.6))
    els.append(poly([(CX + 19.5, y), (CX + 15.5, y - 2), (CX + 15.5, y + 2)], GOLD))
    for dx in (0, 2.0, 4.0):
        els.append(line(CX - 18 + dx, y, CX - 20.5 + dx, y - 2.2, GOLD, 0.5))
        els.append(line(CX - 18 + dx, y, CX - 20.5 + dx, y + 2.2, GOLD, 0.5))
    s = fit(name, CINZELR, 6.0, 40, 0.8)
    els.append(T(name, CX, 84, CINZELR, s, INK, sp=0.8, live="Name"))
    return els


# ------------------------------------------------------------------ 4/5. Tuxedo, braces and bow tie motifs (prom + wedding)
def bow_tie(cx, cy, w, col):
    h = w * 0.42
    els = [poly([(cx - w / 2, cy - h / 2), (cx - w * 0.08, cy - h * 0.12), (cx - w * 0.08, cy + h * 0.12), (cx - w / 2, cy + h / 2)], col),
           poly([(cx + w / 2, cy - h / 2), (cx + w * 0.08, cy - h * 0.12), (cx + w * 0.08, cy + h * 0.12), (cx + w / 2, cy + h / 2)], col),
           rect(cx - w * 0.1, cy - h * 0.2, w * 0.2, h * 0.4, fill=col, r=w * 0.03)]
    return els


def buttons(cx, y0, n, gap, r, col):
    return [circ(cx, y0 + i * gap, r, fill=col) for i in range(n)]


def outfit(style, col, top):
    """style: bowtie / braces / tuxedo, drawn from y=top downwards (about 62 mm tall)."""
    els = []
    if style == "tuxedo":
        # lapels: two long tapering shapes meeting in a V under the bow tie
        els.append(poly([(CX - 10.5, top + 2), (CX - 21, top + 1), (CX - 25, top + 58), (CX - 17, top + 58), (CX - 2.5, top + 32)], col))
        els.append(poly([(CX + 10.5, top + 2), (CX + 21, top + 1), (CX + 25, top + 58), (CX + 17, top + 58), (CX + 2.5, top + 32)], col))
        # peak notch on each lapel (clear cut)
        els += bow_tie(CX, top + 6, 15, col)
        els += buttons(CX, top + 38, 2, 8.0, 1.4, col)
    elif style == "braces":
        for x in (CX - 19, CX + 19):
            els.append(rect(x - 1.6, top + 2, 3.2, 58, fill=col))
            els.append(rect(x - 2.6, top + 20, 5.2, 3.0, stroke=col, sw=0.6, r=0.4))
        els += bow_tie(CX, top + 6, 17, col)
        els += buttons(CX, top + 20, 3, 11.0, 1.8, col)
    else:  # bowtie & buttons
        els += bow_tie(CX, top + 6, 19, col)
        els += buttons(CX, top + 20, 4, 10.0, 1.6, col)
    return els


PROM_COL = {"Black": INK, "Navy": NAVY, "Red": "#B3132B", "Pink": "#D9608A"}


def prom_pint(style="tuxedo", colour="Navy", name="Ava’s", year="2026"):
    col = PROM_COL[colour]
    els = []
    s = fit(name, ALLURA, 17.0, 60)
    els.append(T(name, CX, 18, ALLURA, s, col, live="Name"))
    els.append(T("Prom", CX, 18 + 12.5, ALLURA, 17.0, col))
    els.append(T(year, CX, 18 + 23, MONTB, 7.5, col, sp=0.6, live="Year"))
    els += outfit(style, col, 48)
    return els


WED_ROLES = ["Groom", "Best Man", "Usher", "Groomsman", "Father of the Bride", "Father of the Groom"]


def wedding_pint(role="Best Man", name="AVA", date="12.06.2027", col=NAVY):
    els = []
    s = fit(role, ALLURA, 18.0, 62)
    els.append(T(role, CX, 18, ALLURA, s, col, live="Role"))
    s = fit(name, MONTB, 7.0, 54, 0.8)
    els.append(T(name, CX, 28, MONTB, s, col, sp=0.8, live="Name"))
    els.append(T(date, CX, 35.5, BARLOW, 4.6, col, sp=0.6, live="Wedding_date"))
    els += outfit("tuxedo", col, 44)
    return els


# ------------------------------------------------------------------ 6. Milestone birthday "Vintage" pint
def vintage_pint(name="Ava", year="1976", age="50"):
    els = []
    s = fit(name, GREATV, 15.0, 56)
    els.append(T(name, CX, 40, GREATV, s, GOLD, live="Name"))
    els.append(T("VINTAGE", CX, 52, BARLOWB, 9.0, INK, sp=1.6))
    els.append(T(year, CX, 74, BEBAS, 24.0, INK, sp=0.6, live="Year_born"))
    els += A.rule_with_diamond(CX, 79, 18, GOLD, sw=0.5, d=1.2)
    els.append(T("AGED TO PERFECTION", CX, 86.5, BARLOW, 4.8, INK, sp=0.6))
    els.append(T(age + " YEARS OF AWESOME", CX, 93, BARLOW, 4.0, GOLD, sp=0.5, live="Age"))
    return els


# ------------------------------------------------------------------ 7. Pet face pint
def paw(cx, cy, s, col):
    els = [dict(k="ellipse", x=cx, y=cy + s * 0.35, rx=s * 0.55, ry=s * 0.45, fill=col)]
    for dx, dy in ((-0.62, -0.25), (-0.22, -0.62), (0.22, -0.62), (0.62, -0.25)):
        els.append(dict(k="ellipse", x=cx + dx * s, y=cy + dy * s, rx=s * 0.2, ry=s * 0.26, fill=col))
    return els


def pet_pint(name="BISCUIT", line2="DAD’S DRINKING BUDDY"):
    els = photo_slot(CX, 50, 22, 24, "PET PHOTO", "Pet_photo_upload")
    s = fit(name, POPB, 11.0, 56, 0.4)
    els.append(T(name, CX, 88, POPB, s, INK, sp=0.4, live="Pet_name"))
    s2 = fit(line2, BARLOW, 5.0, 56, 0.4)
    els.append(T(line2, CX, 96, BARLOW, s2, INK, sp=0.4, live="Message"))
    els += paw(CX - 21, 23, 3.0, GOLD) + paw(CX, 20, 3.0, GOLD) + paw(CX + 21, 23, 3.0, GOLD)
    return els


# ------------------------------------------------------------------ 8. "The [Surname] Arms" pub sign pint
def pub_pint(surname="SMITH", est="1987", town="FREE HOUSE"):
    els = []
    # hanging sign bracket + swing sign outline
    els.append(line(CX - 20, 24, CX + 20, 24, INK, 0.9))
    els.append(line(CX - 20, 24, CX - 20, 30, INK, 0.6))
    for x in (CX - 13, CX + 13):
        els.append(line(x, 24, x, 30, INK, 0.5))
    els.append(rect(CX - 25, 30, 50, 62, stroke=INK, sw=0.8, r=2.0))
    els.append(rect(CX - 22.5, 32.5, 45, 57, stroke=GOLD, sw=0.4, r=1.4))
    els.append(T("THE", CX, 44, CINZEL, 6.5, INK, sp=1.2))
    s = fit(surname, CINZEL, 11.0, 40, 0.4)
    els.append(T(surname, CX, 58, CINZEL, s, INK, sp=0.4, live="Surname"))
    els.append(T("ARMS", CX, 70, CINZEL, 9.0, INK, sp=1.2))
    els += A.rule_with_diamond(CX, 75, 14, GOLD, sw=0.45, d=1.0)
    s = fit(town, CINZELR, 4.0, 38, 0.6)
    els.append(T(town, CX, 81.5, CINZELR, s, INK, sp=0.6, live="Second_line"))
    els.append(T("EST. " + est, CX, 87, CINZELR, 3.8, GOLD, sp=0.8, live="Est_year"))
    return els
