"""The 20 older matching bar / man cave coasters (8 Oct 2026, v2 modernisation).

Each design comes from the owner's 2021 Illustrator files in Dropbox
(/Bar Runners Bar Mats/bar mats 3x10/NN. 100x100.pdf and /others mats x10/N. 100x100 others.pdf).
Those files are 100 x 100 mm with the text in demo / commercial fonts (CreattionDemo, ROMANTICE, Butler,
Caslon Titling, Boostard Signature, Rehn, Nexa, Nooa). The v2 print files keep the vector background,
strip the old text and re-set it as live text in open-licence (OFL) Google Fonts.

Line spec (all in ORIGINAL 100 x 100 mm coordinates, y down; the generator scales x0.96 onto the 96 x 96 mm
bleed page so the 90 x 90 mm trim sits 3 mm in):
  dict(text=sample text, field=website field label or None (fixed text), font=key in FONTS,
       x0, x1 = horizontal extent of the original line (centre = middle, width = fit limit),
       y0, y1 = vertical extent of the original glyphs (caps: top of caps .. baseline),
       cap = cap height in mm (optional, else y1 - y0), colour, track = letter spacing in em,
       shadow = (dx, dy, colour) optional)
"""

FONTS = {
    "cinzel": "Cinzel-Regular.ttf",
    "cinzel_sb": "Cinzel-SemiBold.ttf",
    "cinzel_b": "Cinzel-Bold.ttf",
    "vibes": "GreatVibes-Regular.ttf",
    "allura": "Allura-Regular.ttf",
    "playfair": "PlayfairDisplay-Regular.ttf",
    "playfair_b": "PlayfairDisplay-Bold.ttf",
    "mont_m": "Montserrat-Medium.ttf",
    "mont_b": "Montserrat-Bold.ttf",
    "zilla_b": "ZillaSlab-Bold.ttf",
}
FONT_NAMES = {
    "cinzel": "Cinzel", "cinzel_sb": "Cinzel SemiBold", "cinzel_b": "Cinzel Bold", "vibes": "Great Vibes",
    "allura": "Allura", "playfair": "Playfair Display", "playfair_b": "Playfair Display Bold",
    "mont_m": "Montserrat Medium", "mont_b": "Montserrat Bold", "zilla_b": "Zilla Slab Bold",
}

WHOSE = "Whose cave? e.g. Dave’s (optional)"


def L(text, field, font, x0, x1, y0, y1, colour, track=0.0, cap=None, shadow=None, script=False):
    return dict(text=text, field=field, font=font, x0=x0, x1=x1, y0=y0, y1=y1, colour=colour, track=track,
                cap=cap, shadow=shadow, script=script)


def balls(letters, xs, y, field):
    return [L(ch, field, "cinzel_b", x - 5.0, x + 5.0, y - 3.1, y + 3.1, "#211D1E", cap=6.2) for ch, x in zip(letters, xs)]


DESIGNS = {
    # ---------------------------------------------------------------- others mats x10
    "o01": dict(lines=[
        L("WELCOME", None, "cinzel", 24.8, 75.0, 8.6, 12.6, "#C1B5AF", track=0.55),
        L("AVA’S", WHOSE, "cinzel_sb", 18.0, 82.0, 36.3, 48.2, "#FFFFFF", track=0.28, shadow=(1.1, 0, "#D99E46")),
        L("CAVE", None, "cinzel_sb", 17.7, 82.3, 53.1, 65.0, "#FFFFFF", track=0.55, shadow=(1.1, 0, "#D99E46")),
        L("EST. 2021", "Est. year (optional)", "cinzel", 24.8, 75.0, 88.0, 92.0, "#C1B5AF", track=0.45),
    ]),
    "o02": dict(lines=[
        L("WELL,", None, "cinzel_b", 22.0, 78.0, 33.0, 43.6, "#FFFFFF"),
        L("COME IN", None, "cinzel_b", 21.5, 80.2, 47.9, 58.5, "#FFFFFF"),
        L("AVA!", "Name to replace ‘Bud’ (optional)", "cinzel_b", 21.5, 80.2, 62.9, 73.5, "#FFFFFF"),
    ]),
    "o03": dict(cover=[(8.5, 36.8, 91.5, 63.2, "#23256E")], lines=[
        L("AVA’S CAVE", WHOSE, "zilla_b", 9.6, 90.4, 38.2, 47.9, "#FFFFFF"),
        L("MY RULES", None, "zilla_b", 9.6, 90.4, 52.1, 61.8, "#FEE866"),
    ]),
    "o04": dict(lines=[
        L("A", "Initial", "playfair", 30.0, 70.0, 40.0, 58.0, "#FFFFFF"),
    ]),
    "o05": dict(lines=[
        L("AVA’S", WHOSE, "playfair", 34.0, 66.0, 23.6, 30.4, "#FEC230", track=0.05),
        L("CAVE", None, "playfair", 37.0, 63.2, 33.0, 39.8, "#FEC230", track=0.05),
        L("TAKE A SIP", None, "playfair", 23.1, 76.7, 69.4, 75.0, "#FEC230", track=0.35),
        L("AND ENJOY", None, "playfair", 20.8, 79.1, 79.8, 85.4, "#FEC230", track=0.35),
    ]),
    "o06": dict(lines=[
        L("AVA’S", WHOSE, "cinzel", 33.0, 67.0, 6.8, 12.4, "#F7941D", track=0.05),
        L("CAVE", None, "cinzel", 37.5, 62.2, 14.5, 20.1, "#F7941D", track=0.05),
        L("MY", None, "cinzel", 42.9, 57.2, 79.6, 85.2, "#F7941D", track=0.05),
        L("RULES", None, "cinzel", 34.8, 65.3, 86.8, 92.4, "#F7941D", track=0.05),
    ]),
    "o07": dict(lines=[
        L("WELCOME", "Welcome line (optional)", "cinzel", 21.1, 79.1, 9.8, 15.6, "#FCDCE3", track=0.55),
        L("Ava", "Name", "allura", 28.0, 72.0, 36.0, 52.0, "#FCDCE3", script=True),
        L("WELCOME", "Welcome line (optional)", "cinzel", 21.0, 79.1, 83.8, 89.6, "#FCDCE3", track=0.55),
    ]),
    "o08": dict(lines=[
        L("ENJOY AVA’S", WHOSE, "mont_b", 22.0, 78.0, 38.0, 45.4, "#231F20", track=0.02),
        L("MAN CAVE", None, "cinzel", 16.6, 84.2, 50.6, 61.1, "#FFFFFF"),
    ]),
    "o09": dict(lines=[
        L("AVA’S", WHOSE, "playfair", 26.0, 74.0, 36.4, 47.4, "#FFFFFF", track=0.03),
        L("CAVE", None, "playfair", 30.0, 70.3, 50.7, 61.7, "#FFFFFF", track=0.03),
    ]),
    "o10": dict(lines=[
        L("AVA’S", "Line 1", "playfair", 33.0, 67.0, 30.9, 38.2, "#FFDD86", track=0.05),
        L("BAR", "Line 2", "playfair", 33.0, 67.0, 52.9, 60.2, "#FFDD86", track=0.05),
        L("EST. 2021", "Line 3 (optional)", "playfair", 33.0, 67.0, 63.9, 71.2, "#FFDD86", track=0.05),
    ]),
    # ---------------------------------------------------------------- bar mats 3x10
    "x21": dict(lines=[
        L("WELCOME", "Welcome line (optional)", "cinzel", 22.9, 77.1, 12.6, 18.4, "#E9E3E1", track=0.5),
        L("Ava", "Name", "vibes", 24.0, 76.0, 40.0, 56.0, "#FBE08F", script=True),
        L("WELCOME", "Welcome line (optional)", "cinzel", 22.9, 77.1, 84.6, 90.4, "#E9E3E1", track=0.5),
    ]),
    "x22": dict(lines=[
        L("Ava’s", "Your name", "vibes", 32.0, 68.0, 31.0, 40.0, "#FDBA51", script=True),
        L("Bar", None, "vibes", 29.0, 71.0, 45.5, 55.0, "#FDBA51", script=True),
        L("est. 2021", "Est. year (optional)", "vibes", 32.0, 68.0, 60.0, 68.0, "#FDBA51", script=True),
    ]),
    "x23": dict(lines=[
        L("AVA’S", "Bar name – line 1", "cinzel", 18.0, 82.0, 44.6, 55.8, "#D0A178", track=0.35),
        L("BAR", "Bar name – line 2 (optional)", "cinzel", 18.0, 82.0, 59.0, 70.2, "#D0A178", track=0.35),
    ]),
    "x24": dict(lines=[
        L("AVA’S", "Bar name – line 1", "cinzel", 24.0, 76.0, 40.4, 49.0, "#DCC4DF", track=0.45),
        L("BAR", "Bar name – line 2 (optional)", "cinzel", 24.0, 76.0, 52.7, 61.3, "#DCC4DF", track=0.45),
    ]),
    "x25": dict(lines=[
        L("WELCOME", "Welcome line (optional)", "cinzel", 24.9, 75.1, 27.1, 31.5, "#C1B5AF", track=0.55),
        L("AVA’S BAR", "Bar name", "cinzel", 10.0, 90.0, 47.7, 57.0, "#FFFFFF", track=0.25),
        L("WELCOME", "Welcome line (optional)", "cinzel", 24.9, 75.1, 71.0, 75.4, "#C1B5AF", track=0.55),
    ]),
    "x26": dict(strip=[(16.0, 33.0, 87.0, 62.0)], lines=[
        L("AVA’S", "Bar name – line 1", "cinzel", 18.0, 82.0, 37.3, 48.7, "#F2CA7B", track=0.4),
        L("BAR", "Bar name – line 2 (optional)", "cinzel", 18.0, 82.0, 52.6, 64.0, "#F2CA7B", track=0.4),
    ]),
    "x27": dict(lines=[
        L("WELCOME", "Welcome line (optional)", "mont_b", 30.2, 70.1, 22.6, 26.2, "#F7AC3D", track=0.45),
        L("AVA’S", "Bar name – line 1", "cinzel", 22.0, 78.0, 36.6, 52.6, "#F7AC3D"),
        L("BAR", "Bar name – line 2 (optional)", "cinzel", 18.9, 81.0, 54.6, 70.6, "#F7AC3D"),
        L("EST. 2021", "Est. year (optional)", "mont_b", 28.8, 71.1, 73.3, 76.9, "#F7AC3D", track=0.45),
    ]),
    "x28": dict(lines=[
        L("WELCOME", None, "mont_m", 28.9, 71.3, 15.2, 18.9, "#F2CA7B", track=0.6),
        L("TO", None, "mont_m", 44.0, 56.0, 21.0, 24.7, "#F2CA7B", track=0.6),
        L("AVA’S", "Bar name – line 1", "cinzel", 18.0, 82.0, 39.2, 50.2, "#F2CA7B", track=0.35),
        L("BAR", "Bar name – line 2 (optional)", "cinzel", 17.5, 82.5, 54.6, 65.6, "#F2CA7B", track=0.35),
        L("ESTABLISHED", None, "mont_m", 18.8, 81.3, 74.4, 78.1, "#F2CA7B", track=0.6),
        L("2021", "Est. year (optional)", "mont_m", 38.0, 62.0, 80.2, 83.9, "#F2CA7B", track=0.6),
    ]),
    "x29": dict(lines=[
        L("WELCOME", "Welcome line (optional)", "mont_b", 26.7, 73.6, 13.1, 16.8, "#F7AC3D", track=0.55),
        *balls("AVA", (31.83, 50.0, 68.18), 40.88, "Top row letters (up to 3)"),
        *balls("BAR!", (22.74, 40.91, 59.09, 77.26), 59.12, "Bottom row letters (up to 4)"),
        L("WELCOME", "Welcome line (optional)", "mont_b", 26.7, 73.6, 82.8, 86.5, "#F7AC3D", track=0.55),
    ]),
    "x30": dict(lines=[
        L("Ava’s Bar", "Bar name", "vibes", 14.0, 86.0, 47.0, 62.0, "#ED1C24", script=True),
        L("ENJOY", None, "cinzel", 32.7, 67.3, 75.6, 78.0, "#ED1C24", track=1.4),
        L("YOUR TIME", None, "cinzel", 20.4, 79.6, 81.5, 83.9, "#ED1C24", track=1.4),
    ]),
}
