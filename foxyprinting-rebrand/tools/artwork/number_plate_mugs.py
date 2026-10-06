"""Funny "number plate" mugs (Foxy Printing, Oct 2026).

Builds, for 10 original designs x 5 country bands:
  * print-ready 11oz sublimation wrap artwork (SVG with live text, PDF, mirrored PDF, 300 dpi PNG)
  * a zip per design (with the fonts + OFL licence) for Shopify Files / Dropbox
  * products.json with the house copy, SEO, tags, SKUs and Google fields

Run:  python3 tools/artwork/number_plate_mugs.py            (artwork + products.json)
      python3 tools/artwork/number_plate_mugs.py ebay URLS.json   (eBay upload CSV)

Wrap size: 200 x 85 mm (standard 11oz sublimation print area) + 3 mm bleed = 206 x 91 mm,
3 mm safe area. Font: Barlow Condensed (SIL OFL 1.1, Google Fonts) - an open-licence
condensed font in the spirit of UK plates; the commercial Charles Wright font is NOT used.
Wales flag: flag-icons (MIT). Other flags are drawn here. The NI band is lettering only.
"""
import csv
import html
import json
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))           # foxyprinting-rebrand/
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(ROOT, "exports", "number-plate-mugs")

TRIM_W, TRIM_H, BLEED, SAFE = 200.0, 85.0, 3.0, 3.0
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
PLATE_W, PLATE_H = 92.0, 22.0
PLATE_CX = (51.0, 149.0)          # trim coords: left = white front plate, right = yellow rear plate
YELLOW, WHITE, BLUE, INK = "#FFD100", "#FFFFFF", "#003DA5", "#111111"
PRICE = "7.99"

COUNTRIES = [  # option value, code on band, flag, file label
    ("GB", "GB", "union", "GB"),
    ("Scotland", "SCO", "saltire", "Scotland"),
    ("Wales", "CYM", "wales", "Wales"),
    ("Northern Ireland", "NI", None, "Northern Ireland"),
    ("Ireland", "IRL", "ireland", "Ireland"),
]

FACTS = dict(  # MUGS fact sheet only (plan/product-facts.md)
    details=[
        "White ceramic mug, 11oz (approx. 325ml)",
        "C-shaped handle and a high-gloss finish",
        "Sublimation printed in-house in North Yorkshire",
        "Dishwasher and microwave safe – avoid abrasive scourers",
        "Novelty plate design – not a real or road-legal registration",
    ],
    delivery="Every mug is printed to order in our North Yorkshire workshop and sent out in protective packaging for UK delivery.",
)

COMMON_BULLETS = [
    "Two plates on one mug: a white front plate on one side and a yellow rear plate on the other, so the joke faces out whichever hand they drink with",
    "Pick the band that suits them – GB with the Union flag, Scotland with the saltire and SCO, Wales with the dragon and CYM, Northern Ireland with NI lettering, or Ireland with the tricolour and IRL",
    "Sublimation printed onto an 11oz white ceramic mug, dishwasher and microwave safe for everyday brews",
]

D = [
    dict(reg=("BR3W", "UP"), meaning="Brew Up", gift="Tea Lover Gift", primary="funny tea mug",
         seo_title="Funny Tea Mug – BR3W UP Number Plate | Foxy Printing",
         meta="A funny tea mug styled like a UK number plate that reads BR3W UP. Choose a GB, Scotland, Wales, NI or Ireland band – a cheerful gift for tea lovers.",
         opening="This funny tea mug is for the person who meets every crisis with “I’ll put the kettle on”. Styled like a proper British number plate, it reads BR3W UP – the call to arms in every Yorkshire kitchen when a cuppa is overdue.",
         h2="A funny tea mug with a number plate twist",
         para="BR3W UP is printed on both sides of the mug, as a white front plate and a yellow rear plate, just like a car. Choose the band on the left of the plate to suit the tea drinker in your life: GB, Scotland, Wales, Northern Ireland or Ireland. It’s a novelty number plate mug rather than a real registration, so nobody will be clamping the kitchen.",
         bullets=["Gives the household tea maker a mug that finally gives them the credit", "A tea lover gift for birthdays, Secret Santa or a new-job welcome"],
         closing="Pair it with a box of their favourite tea bags for an easy tea lover gift.",
         tags=["tea mug", "tea lover gift"]),
    dict(reg=("B15", "CU1T"), meaning="Biscuit", gift="Biscuit Lover Gift", primary="biscuit lover mug",
         seo_title="Biscuit Lover Mug – B15 CU1T Number Plate | Foxy Printing",
         meta="A biscuit lover mug made like a UK number plate reading B15 CU1T. Choose a GB, Scotland, Wales, NI or Ireland band – a fun gift for any tea break.",
         opening="This biscuit lover mug is for the person in every office who knows exactly where the good biscuits are hidden. It gives them a number plate of their own, B15 CU1T, so everyone knows what goes with their brew.",
         h2="Biscuit lover mug with a cheeky registration",
         para="We print the B15 CU1T plate twice – once as a white front plate and once as a yellow rear plate – so the joke is on show whichever way the mug is put down. Pick a GB, Scotland, Wales, Northern Ireland or Ireland band to match where they’re from. It’s a novelty number plate mug and not a real registration, although it does make dunking feel like serious business.",
         bullets=["A fun desk mug that gets people talking at tea break", "An easy add-on gift with a packet of their favourite biscuits"],
         closing="Tuck a packet of chocolate digestives in with it and you’ve got a ready-made tea break gift.",
         tags=["biscuit mug", "tea lover gift"]),
    dict(reg=("2", "SUG4RS"), meaning="Two Sugars", gift="Builder’s Tea Gift", primary="two sugars mug",
         seo_title="Two Sugars Mug – 2 SUG4RS Number Plate | Foxy Printing",
         meta="Never forget their order again: a two sugars mug styled like a UK number plate reading 2 SUG4RS, with a GB, Scotland, Wales, NI or Ireland band.",
         opening="This two sugars mug settles the tea round for good, with a UK number plate design that reads 2 SUG4RS. No more shouting “how many sugars?” across the office.",
         h2="The two sugars mug that remembers their order",
         para="Whoever’s on the tea round only needs one glance: 2 SUG4RS sits on a white front plate on one side and a yellow rear plate on the other. You choose the country band – GB, Scotland, Wales, Northern Ireland or Ireland. The plate is a novelty design, not a real registration, so it’s a number plate mug that never needs taxing.",
         bullets=["Ends the daily tea round guessing game once and for all", "Great for builders, tradespeople and anyone who likes their tea sweet"],
         closing="A builder’s tea gift for the van, the site cabin or the staffroom.",
         tags=["builders tea mug", "tea lover gift"]),
    dict(reg=("D3C4F", "N0"), meaning="No Decaf", gift="Coffee Lover Gift", primary="funny coffee mug",
         seo_title="Funny Coffee Mug – D3C4F N0 Number Plate | Foxy Printing",
         meta="A funny coffee mug for anyone who won’t touch decaf. The UK number plate style design reads D3C4F N0, with a GB, Scotland, Wales, NI or Ireland band.",
         opening="For the friend who treats decaf as a personal insult, this funny coffee mug says it before they’ve had their first sip. The number plate reads D3C4F N0 – short, sharp and as strong as their morning espresso.",
         h2="A funny coffee mug for proper coffee drinkers",
         para="The D3C4F N0 plate appears twice, a white front plate on one side and a yellow rear plate on the other, with the country band of your choice: GB, Scotland, Wales, Northern Ireland or Ireland. It’s a novelty number plate mug – the registration isn’t real, but their feelings about decaf definitely are.",
         bullets=["Lets the coffee lover in your life make their feelings clear", "Holds 11oz, plenty for that first strong coffee of the day"],
         closing="Pair it with a bag of freshly ground beans for a coffee lover gift they’ll use every morning.",
         tags=["coffee mug", "coffee lover gift"]),
    dict(reg=("BO55", "MUG"), meaning="Boss Mug", gift="Gift for the Boss", primary="boss mug",
         seo_title="Funny Boss Mug – BO55 MUG Number Plate | Foxy Printing",
         meta="A funny boss mug made like a UK number plate reading BO55 MUG. Pick a GB, Scotland, Wales, NI or Ireland band – a great gift for the boss or a promotion.",
         opening="Whether they run the office, the house or the five-a-side team, this boss mug lets them claim the title in style. The plate reads BO55 MUG and even follows the real two letters, two numbers, three letters layout.",
         h2="A boss mug with a proper plate layout",
         para="BO55 MUG is printed as a white front plate on one side of the mug and a yellow rear plate on the other, with a GB, Scotland, Wales, Northern Ireland or Ireland band – your choice. It’s a novelty number plate mug and not a real registration, so the only thing it gives them is bragging rights.",
         bullets=["A funny gift for a manager’s birthday, a promotion or a leaving do", "Looks the part on a desk next to the car keys"],
         closing="A great Secret Santa gift for the boss – or a cheeky one for whoever really runs your house.",
         tags=["boss gift", "office mug"]),
    dict(reg=("WFH", "4EVA"), meaning="WFH Forever", gift="Home Office Gift", primary="work from home mug",
         seo_title="Work From Home Mug – WFH 4EVA Plate | Foxy Printing",
         meta="A work from home mug styled like a UK number plate reading WFH 4EVA. Choose a GB, Scotland, Wales, NI or Ireland band – a fun home office gift.",
         opening="This work from home mug is for the home-office hero whose daily commute runs from the kettle to the laptop. The number plate says it proudly: WFH 4EVA.",
         h2="The work from home mug for remote workers",
         para="We print WFH 4EVA as a white front plate on one side and a yellow rear plate on the other, so it reads right on camera whichever hand they hold it in. Choose a GB, Scotland, Wales, Northern Ireland or Ireland band. It’s a novelty number plate mug, not a real registration – the only thing parked is them, at the kitchen table.",
         bullets=["Brightens up video calls when it’s sat in the background", "A fun gift for a colleague going hybrid or fully remote"],
         closing="Add a coaster and a desk plant and you’ve got a complete home office gift.",
         tags=["office mug", "home office gift"]),
    dict(reg=("NAP", "T1ME"), meaning="Nap Time", gift="Retirement Gift", primary="funny retirement mug",
         seo_title="Funny Retirement Mug – NAP T1ME Plate | Foxy Printing",
         meta="A funny retirement mug made like a UK number plate that reads NAP T1ME. Choose a GB, Scotland, Wales, NI or Ireland band – a fun gift for the leaving do.",
         opening="This funny retirement mug is for anyone retired, semi-retired or just very good at sofa time. It puts their new priorities on a UK number plate: NAP T1ME.",
         h2="A funny retirement mug for well-earned rest",
         para="NAP T1ME is printed on both sides – a white front plate and a yellow rear plate – with the band of your choice: GB, Scotland, Wales, Northern Ireland or Ireland. It’s a novelty number plate mug rather than a real registration, though the afternoon snooze it describes is very real indeed.",
         bullets=["A light-hearted retirement gift that gets a laugh at the leaving do", "Also suits new parents, students and anyone who loves a Sunday snooze"],
         closing="Pop it in a gift bag with a good book and some biscuits for a cosy retirement gift.",
         tags=["retirement gift", "gift for grandad"]),
    dict(reg=("D4D", "T4X1"), meaning="Dad Taxi", gift="Gift for Dad", primary="dad taxi mug",
         seo_title="Dad Taxi Mug – D4D T4X1 Number Plate | Foxy Printing",
         meta="A dad taxi mug for the dad who does all the lifts, styled like a UK number plate reading D4D T4X1 with a GB, Scotland, Wales, NI or Ireland band.",
         opening="Football at nine, a party at two, a lift home at midnight – if Dad’s car is the family bus, this dad taxi mug is the one. The number plate reads D4D T4X1, so there’s no doubt who’s driving.",
         h2="The dad taxi mug for the family chauffeur",
         para="D4D T4X1 goes on as a white front plate on one side and a yellow rear plate on the other, and you choose the band: GB, Scotland, Wales, Northern Ireland or Ireland. It’s a novelty number plate mug, not a real registration – sadly it doesn’t come with fares.",
         bullets=["A funny Father’s Day or birthday gift for dads who do all the driving", "A car lover gift with a proper plate layout and country band"],
         closing="Matching keyrings make a lovely add-on for the dad taxi driver.",
         tags=["gift for dad", "fathers day gift"]),
    dict(reg=("F1X3D", "1T"), meaning="Fixed It", gift="Mechanic & DIY Gift", primary="funny mechanic mug",
         seo_title="Funny Mechanic Mug – F1X3D 1T Plate | Foxy Printing",
         meta="A funny mechanic mug made like a UK number plate that reads F1X3D 1T. Choose a GB, Scotland, Wales, NI or Ireland band – a fun gift for the garage or shed.",
         opening="For the mechanic, the DIY dad or the friend who swears they can fix anything with cable ties, this funny mechanic mug says it with confidence: F1X3D 1T.",
         h2="A funny mechanic mug for the garage",
         para="The F1X3D 1T plate is printed twice, as a white front plate and a yellow rear plate, with a GB, Scotland, Wales, Northern Ireland or Ireland band – pick the one that suits them. It’s a novelty number plate mug and not a real registration, so there’s no MOT needed.",
         bullets=["Made for the garage, the workshop or the shed", "A car lover gift for enthusiasts, DIYers and anyone handy with a spanner"],
         closing="Give it with a pair of work gloves for a DIY gift that gets a laugh.",
         tags=["mechanic gift", "diy gift"]),
    dict(reg=("SN00", "ZED"), meaning="Snoozed", gift="Monday Morning Mug", primary="Monday morning mug",
         seo_title="Funny Monday Morning Mug – SN00 ZED | Foxy Printing",
         meta="A funny Monday morning mug for serial snoozers, made like a UK number plate that reads SN00 ZED. Choose a GB, Scotland, Wales, NI or Ireland band.",
         opening="This Monday morning mug is for every serial snoozer who hits the button three times and still makes it in. The number plate design reads SN00 ZED.",
         h2="A Monday morning mug for serial snoozers",
         para="SN00 ZED appears as a white front plate on one side and a yellow rear plate on the other, with a GB, Scotland, Wales, Northern Ireland or Ireland band of your choice. It’s a novelty number plate mug and not a real registration – the alarm clock is the only thing that’s been clamped.",
         bullets=["Makes the first brew of the week a bit more bearable", "A cheeky gift for the colleague who is always just on time"],
         closing="A fun office mug for the serial snoozer – pair it with a big jar of instant coffee.",
         tags=["office mug", "funny work mug"]),
]

BASE_TAGS = ["number-plate-mugs", "funny-mugs", "car-lover-gifts", "novelty mug", "11oz mug", "foxy-new-2026",
             "machine-sublimation", "range-number-plate-mugs", "country-gb", "country-scotland", "country-wales",
             "country-northern-ireland", "country-ireland"]


def slug(s):  # same as tools/build_plan.py
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def reg_text(d):
    return " ".join(d["reg"])


def title(d):
    return f"Funny Number Plate Mug – {reg_text(d)} ({d['meaning']}) – {d['gift']} – 11oz Ceramic"


_TAKEN = set()


def sku_base(d):  # build_plan.sku convention: FOXY-<machine>-<title initials, 8 max>
    if "_sku" not in d:
        base = "FOXY-SUB-" + "".join(w[0] for w in slug(title(d)).split("-"))[:8].upper()
        cand, n = base, 2
        while cand in _TAKEN:
            cand, n = f"{base}{n}", n + 1
        _TAKEN.add(cand)
        d["_sku"] = cand
    return d["_sku"]


def description(d):
    li = lambda xs: "".join(f"<li>{html.escape(x, quote=False)}</li>" for x in xs)
    e = lambda s: html.escape(s, quote=False)
    return (f"<p>{e(d['opening'])}</p>"
            f"<h2>{e(d['h2'][0].upper() + d['h2'][1:])}</h2>"
            f"<p>{e(d['para'])}</p>"
            f"<h3>Why you’ll love it</h3><ul>{li(d['bullets'] + COMMON_BULLETS)}</ul>"
            f"<h3>Size &amp; details</h3><ul>{li(FACTS['details'])}</ul>"
            f"<h3>Delivery</h3><p>{e(FACTS['delivery'])}</p>"
            f"<p>{e(d['closing'])}</p>")


# ---------------------------------------------------------------- artwork
def _font_metrics():
    from fontTools.ttLib import TTFont
    out = {}
    for w, f in (("600", "BarlowCondensed-SemiBold.ttf"), ("700", "BarlowCondensed-Bold.ttf")):
        t = TTFont(os.path.join(ASSETS, "fonts", f))
        cmap, hmtx, upm = t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm
        out[w] = dict(cap=t["OS/2"].sCapHeight / upm,
                      adv={c: hmtx[cmap[ord(c)]][0] / upm for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"})
    return out


FM = None
LS = 0.035  # letter spacing (em)


def text_w(s, size, weight="600"):
    return sum(FM[weight]["adv"][c] for c in s) * size + LS * size * (len(s) - 1)


def flag_svg(kind, x, y, w, uid):
    if kind == "union":
        h = w / 2
        return (f'<svg x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 60 30">'
                f'<clipPath id="{uid}s"><path d="M0,0 v30 h60 v-30 z"/></clipPath>'
                f'<clipPath id="{uid}t"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath>'
                f'<g clip-path="url(#{uid}s)"><path d="M0,0 v30 h60 v-30 z" fill="#012169"/>'
                f'<path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/>'
                f'<path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#{uid}t)" stroke="#C8102E" stroke-width="4"/>'
                f'<path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/>'
                f'<path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></g></svg>'), h
    if kind == "saltire":
        h = w * 3 / 5
        return (f'<svg x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 5 3">'
                f'<rect width="5" height="3" fill="#005EB8"/>'
                f'<path d="M0,0 L5,3 M5,0 L0,3" stroke="#fff" stroke-width="0.6"/></svg>'), h
    if kind == "ireland":
        h = w / 2
        return (f'<svg x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 3 1.5">'
                f'<rect width="1" height="1.5" fill="#169B62"/><rect x="1" width="1" height="1.5" fill="#FFFFFF"/>'
                f'<rect x="2" width="1" height="1.5" fill="#FF883E"/></svg>'), h
    if kind == "wales":
        h = w * 0.75
        src = open(os.path.join(ASSETS, "flag-wales.svg")).read()
        inner = re.sub(r"^.*?<svg[^>]*>", "", src, flags=re.S).rsplit("</svg>", 1)[0]
        return (f'<svg x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" viewBox="0 0 640 480">'
                f'{inner}</svg>'), h
    raise ValueError(kind)


def plate_svg(d, country, cx_trim, bg, uid):
    _, code, flag, _ = country
    cx, cy = cx_trim + BLEED, TRIM_H / 2 + BLEED
    L, T = cx - PLATE_W / 2, cy - PLATE_H / 2
    R, B = L + PLATE_W, T + PLATE_H
    bw = 12.0
    s = [f'<g id="{uid}" inkscape:groupmode="layer" inkscape:label="{"Front plate (white)" if bg == WHITE else "Rear plate (yellow)"}">',
         f'<clipPath id="{uid}c"><rect x="{L:.3f}" y="{T:.3f}" width="{PLATE_W}" height="{PLATE_H}" rx="2.6"/></clipPath>',
         f'<rect x="{L:.3f}" y="{T:.3f}" width="{PLATE_W}" height="{PLATE_H}" rx="2.6" fill="{bg}" stroke="#8A8A8A" stroke-width="0.25"/>',
         f'<g clip-path="url(#{uid}c)"><rect id="{uid}band" x="{L:.3f}" y="{T:.3f}" width="{bw}" height="{PLATE_H}" fill="{BLUE}"/></g>']
    bx = L + bw / 2
    if flag:
        fw = bw - 2.8
        fs, fh = flag_svg(flag, bx - fw / 2, T + 2.6, fw, uid + "f")
        s.append(fs)
        csize = 4.0 / FM["700"]["cap"]
        s.append(f'<text x="{bx:.3f}" y="{B - 2.9:.3f}" font-family="Barlow Condensed" font-weight="700" '
                 f'font-size="{csize:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    else:  # Northern Ireland: lettering only, no flag (owner's rule)
        csize = 6.5 / FM["700"]["cap"]
        s.append(f'<text x="{bx:.3f}" y="{cy + 3.25:.3f}" font-family="Barlow Condensed" font-weight="700" '
                 f'font-size="{csize:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    # registration (live, editable text; two words so the gap matches a real plate)
    x0, x1 = L + bw + 2.2, R - 2.6
    cap = PLATE_H * 0.60
    for _ in range(40):
        size = cap / FM["600"]["cap"]
        g1, g2 = d["reg"]
        gap = 0.55 * cap
        tw = text_w(g1, size) + gap + text_w(g2, size)
        if tw <= (x1 - x0) * 0.94:
            break
        cap *= 0.97
    sx = x0 + ((x1 - x0) - tw) / 2
    base = cy + cap / 2
    s.append(f'<g id="{uid}reg" font-family="Barlow Condensed" font-weight="600" font-size="{size:.3f}" '
             f'letter-spacing="{LS * size:.3f}" fill="{INK}">'
             f'<text x="{sx:.3f}" y="{base:.3f}">{g1}</text>'
             f'<text x="{sx + text_w(g1, size) + gap:.3f}" y="{base:.3f}">{g2}</text></g>')
    s.append(f'<rect x="{L + 1.1:.3f}" y="{T + 1.1:.3f}" width="{PLATE_W - 2.2:.3f}" height="{PLATE_H - 2.2:.3f}" '
             f'rx="1.7" fill="none" stroke="{INK}" stroke-width="0.45"/></g>')
    return "\n".join(s)


def wrap_svg(d, country, mirrored=False, guides=False):
    body = [f'<g id="Background" inkscape:groupmode="layer" inkscape:label="Background (bleed)">'
            f'<rect width="{PAGE_W}" height="{PAGE_H}" fill="#FFFFFF"/></g>',
            plate_svg(d, country, PLATE_CX[0], WHITE, "front"),
            plate_svg(d, country, PLATE_CX[1], YELLOW, "rear")]
    g = (f'<g id="Guides" inkscape:groupmode="layer" inkscape:label="Guides (do not print)" '
         f'style="display:{"inline" if guides else "none"}" fill="none" stroke-width="0.2">'
         f'<rect x="{BLEED}" y="{BLEED}" width="{TRIM_W}" height="{TRIM_H}" stroke="#00AEEF" stroke-dasharray="2,1"/>'
         f'<rect x="{BLEED + SAFE}" y="{BLEED + SAFE}" width="{TRIM_W - 2 * SAFE}" height="{TRIM_H - 2 * SAFE}" '
         f'stroke="#EC008C" stroke-dasharray="1,1"/></g>')
    content = "\n".join(body)
    if mirrored:
        content = f'<g transform="translate({PAGE_W},0) scale(-1,1)">{content}</g>'
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<!-- Foxy Printing | {title(d)} | {country[0]} | 11oz sublimation wrap: trim {TRIM_W:g} x {TRIM_H:g} mm, '
            f'bleed {BLEED:g} mm (page {PAGE_W:g} x {PAGE_H:g} mm), safe area {SAFE:g} mm. Font: Barlow Condensed (SIL OFL 1.1). -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'width="{PAGE_W:g}mm" height="{PAGE_H:g}mm" viewBox="0 0 {PAGE_W:g} {PAGE_H:g}">\n{content}\n{g}\n</svg>\n')


README = """Foxy Printing - {title}
SKU base {sku}  |  Plate: {reg}

Files (one set per country band: GB, Scotland, Wales, Northern Ireland, Ireland)
  ... .svg            editable master (live text, layers: Background / Front plate / Rear plate / Guides)
  ... .pdf            print file, 206 x 91 mm (200 x 85 mm wrap + 3 mm bleed each edge)
  ... - MIRRORED.pdf  same, flipped left-right - only if your print driver/RIP does NOT mirror for you
  ... - 300dpi.png    raster print file, 2433 x 1075 px at 300 dpi

Spec: 11oz white sublimation mug, wrap trim 200 x 85 mm, 3 mm bleed, 3 mm safe area
(no artwork near the edges - the plates sit well inside it). Plates are 92 x 22 mm, centred
51 mm and 149 mm from the left trim edge, so one plate sits each side of the handle.
Please check the 200 x 85 mm wrap against your mug blanks/press before the first run.

Font: Barlow Condensed SemiBold/Bold (SIL Open Font License 1.1) - in the Fonts folder.
Install it before editing the SVG so the live text renders correctly.
Wales flag artwork: flag-icons (MIT licence). The plate text is a novelty design, not a real registration.
"""


def build():
    global FM
    import cairosvg
    FM = _font_metrics()
    art_root, zip_root = os.path.join(OUT, "artwork"), os.path.join(OUT, "zips")
    for p in (art_root, zip_root):
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p)
    products, problems = [], []
    for i, d in enumerate(D, 1):
        sb = sku_base(d)
        folder = os.path.join(art_root, f"{sb} {reg_text(d)}")
        os.makedirs(folder)
        files = []
        for country in COUNTRIES:
            stem = f"{sb} {reg_text(d)} {country[3]} - 11oz mug wrap 206x91mm"
            svg = wrap_svg(d, country)
            open(os.path.join(folder, stem + ".svg"), "w").write(svg)
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(folder, stem + ".pdf"))
            cairosvg.svg2pdf(bytestring=wrap_svg(d, country, mirrored=True).encode(),
                             write_to=os.path.join(folder, stem + " - MIRRORED.pdf"))
            cairosvg.svg2png(bytestring=svg.encode(), dpi=300, write_to=os.path.join(folder, stem + " - 300dpi.png"))
            files.append(stem)
        open(os.path.join(folder, "README - how to print.txt"), "w").write(
            README.format(title=title(d), sku=sb, reg=reg_text(d)))
        zpath = os.path.join(zip_root, f"{sb}-number-plate-mug-artwork.zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            top = f"{title(d)} - {sb}-01"
            for f in sorted(os.listdir(folder)):
                z.write(os.path.join(folder, f), f"{top}/{f}")
            for f in sorted(os.listdir(os.path.join(ASSETS, "fonts"))):
                z.write(os.path.join(ASSETS, "fonts", f), f"{top}/Fonts/{f}")
            z.write(os.path.join(ASSETS, "flag-icons-LICENSE.txt"), f"{top}/Fonts/flag-icons (Wales flag) LICENSE.txt")
        desc = description(d)
        words = len(re.sub("<[^>]+>", " ", desc).split())
        t = title(d)
        checks = [(len(t) <= 150, f"title {len(t)}"), (len(d["seo_title"]) <= 60, f"seo title {len(d['seo_title'])}"),
                  (140 <= len(d["meta"]) <= 155, f"meta {len(d['meta'])}"), (180 <= words <= 350, f"words {words}"),
                  (desc.lower().count(d["primary"].lower()) >= 2, "primary kw count"),
                  (d["primary"].lower() in re.split(r"(?<=[.!?])\s", d["opening"])[0].lower(), "primary in 1st sentence"),
                  (d["primary"].lower() in d["h2"].lower(), "primary in h2")]
        for ok, msg in checks:
            if not ok:
                problems.append(f"{reg_text(d)}: {msg}")
        handle = slug(f"funny number plate mug {reg_text(d)} {d['meaning']}")
        products.append(dict(
            n=i, reg=reg_text(d), meaning=d["meaning"], title=t, handle=handle, sku_base=sb,
            skus={c[0]: f"{sb}-{k:02d}" for k, c in enumerate(COUNTRIES, 1)},
            productType="Mugs", vendor="Foxy Printing", price=PRICE,
            tags=sorted(set(BASE_TAGS + d["tags"] + [d["primary"].lower()])),
            seo=dict(title=d["seo_title"], description=d["meta"]), descriptionHtml=desc, words=words,
            primary=d["primary"], zip=os.path.relpath(zpath, ROOT), artwork_files=files,
            dropbox_folder=f"/AI DESIGNS 2026/{t} - {sb}-01",
            google=dict(custom_product="true", condition="new",
                        google_product_category="Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs",
                        gender="unisex", age_group="adult", color="White", mpn=f"{sb}-01"),
            alt={c[0]: f"Funny number plate mug reading {reg_text(d)} with a {c[0]} band, printed on a white 11oz ceramic mug"
                 for c in COUNTRIES}))
    json.dump(products, open(os.path.join(OUT, "products.json"), "w"), indent=1, ensure_ascii=False)
    # proof sheet with guides (for checking)
    proofs = []
    for d in D:
        for country in COUNTRIES:
            p = os.path.join("/tmp", f"proof-{sku_base(d)}-{country[1]}.png")
            cairosvg.svg2png(bytestring=wrap_svg(d, country, guides=True).encode(), dpi=60, write_to=p)
            proofs.append(p)
    os.system("convert " + " ".join(f"'{p}'" for p in proofs) + f" -bordercolor '#999' -border 1 miff:- | "
              f"montage - -tile 5x10 -geometry +2+2 '{OUT}/proof-sheet.png'")
    print("\n".join(problems) or "all copy checks passed")
    for p in products:
        print(p["sku_base"], p["reg"], "|", p["title"], "|", p["words"], "words |", len(p["seo"]["description"]))


EBAY_HTML = ('<div style="font-family:Arial,sans-serif;max-width:800px"><h2>{h}</h2>{body}</div>')


def ebay(urls_path):
    """urls.json: {sku_base: {"GB": url, ..., "extra": [url, ...]}} -> eBay File Exchange / Seller Hub CSV."""
    products = json.load(open(os.path.join(OUT, "products.json")))
    urls = json.load(open(urls_path))
    outdir = os.path.join(ROOT, "exports", "ebay", "number-plate-mugs")
    os.makedirs(outdir, exist_ok=True)
    head = ["*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)", "CustomLabel", "*Category", "*Title",
            "*ConditionID", "*C:Brand", "C:Type", "C:Material", "C:Capacity", "C:Colour", "C:Theme", "C:Features",
            "C:Care Instructions", "C:Country/Region of Manufacture", "Relationship", "RelationshipDetails",
            "PicURL", "*Description", "*Format", "*Duration", "*StartPrice", "*Quantity", "*Location",
            "ShippingProfileName", "ReturnProfileName", "PaymentProfileName"]
    rows = []
    for p in products:
        u = urls[p["sku_base"]]
        short = f"Funny Number Plate Mug {p['reg']} {p['meaning']} Gift 11oz Ceramic UK Seller"
        if len(short) > 80:
            short = f"Funny Number Plate Mug {p['reg']} {p['meaning']} Gift 11oz Ceramic"
        assert len(short) <= 80, short
        desc = re.sub(r"\s+", " ", p["descriptionHtml"]).replace('"', "'")
        rows.append({head[0]: "Add", "CustomLabel": p["sku_base"], "*Category": "177006",  # Home > Kitchen > Cups & Mugs (UK) - check in Seller Hub
                     "*Title": short, "*ConditionID": "1000", "*C:Brand": "Foxy Printing", "C:Type": "Mug",
                     "C:Material": "Ceramic", "C:Capacity": "11oz", "C:Colour": "White",
                     "C:Theme": "Novelty", "C:Features": "Dishwasher Safe|Microwave Safe",
                     "C:Care Instructions": "Dishwasher Safe", "C:Country/Region of Manufacture": "United Kingdom",
                     "RelationshipDetails": "Country=" + ";".join(c[0] for c in COUNTRIES),
                     "PicURL": "|".join([u["GB"]] + u.get("extra", [])[:10]),
                     "*Description": EBAY_HTML.format(h=html.escape(p["title"]), body=desc),
                     "*Format": "FixedPrice", "*Duration": "GTC", "*StartPrice": "", "*Quantity": "",
                     "*Location": "North Yorkshire, UK"})
        for c in COUNTRIES:
            rows.append({"Relationship": "Variation", "RelationshipDetails": f"Country={c[0]}",
                         "CustomLabel": p["skus"][c[0]], "*StartPrice": PRICE, "*Quantity": "10",
                         "PicURL": f"Country={c[0]}|{u[c[0]]}"})
    path = os.path.join(outdir, "ebay-number-plate-mugs-upload.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        w.writerows(rows)
    print("wrote", path, len(rows), "rows")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ebay":
        ebay(sys.argv[2])
    else:
        build()
