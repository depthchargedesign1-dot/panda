"""Text files for the 20 coaster Dropbox folders. usage: python3 dropbox_texts.py MANIFEST OUT_JSON"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coaster_copy as C
ZIP = "https://cdn.shopify.com/s/files/1/1774/9115/files/bar-coasters-v2-artwork.zip"
MD5 = "b984a0fbcb9a5f42fd24a41af846a2c8"
SRC = {**{f"x{n}": f"/Bar Runners Bar Mats/bar mats 3x10/{n}. 100x100.pdf" for n in range(21, 31)},
       **{f"o{n:02d}": f"/Bar Runners Bar Mats/others mats x10/{n}. 100x100 others.pdf" for n in range(1, 11)}}
GF = {"Cinzel-Regular.ttf": ("Cinzel", "https://fonts.google.com/specimen/Cinzel"),
      "Cinzel-SemiBold.ttf": ("Cinzel SemiBold", "https://fonts.google.com/specimen/Cinzel"),
      "Cinzel-Bold.ttf": ("Cinzel Bold", "https://fonts.google.com/specimen/Cinzel"),
      "GreatVibes-Regular.ttf": ("Great Vibes", "https://fonts.google.com/specimen/Great+Vibes"),
      "Allura-Regular.ttf": ("Allura", "https://fonts.google.com/specimen/Allura"),
      "PlayfairDisplay-Regular.ttf": ("Playfair Display", "https://fonts.google.com/specimen/Playfair+Display"),
      "Montserrat-Medium.ttf": ("Montserrat Medium", "https://fonts.google.com/specimen/Montserrat"),
      "Montserrat-Bold.ttf": ("Montserrat Bold", "https://fonts.google.com/specimen/Montserrat"),
      "ZillaSlab-Bold.ttf": ("Zilla Slab Bold", "https://fonts.google.com/specimen/Zilla+Slab")}
man = json.load(open(sys.argv[1]))
out = {}
for p in C.P:
    k = p["key"]; m = man[k]
    folder = f"/AI DESIGNS 2026/{p['title']} - {m['sku']}"
    f = m["files"][0][:-4]
    notes = "o03: the original 2021 file has its text as outlines; the two lines are covered with the flat navy (#23256E) and re-set as live text in Zilla Slab Bold." if k == "o03" else \
        "x29: one letter per pool ball (3 top, 4 bottom); centre each letter in its ball if you change them." if k == "x29" else \
        "o01: MAN/CAVE has a gold shadow copy 1.1 mm to the right of the white text; change both." if k == "o01" else ""
    fn = ", ".join(dict.fromkeys(GF[x][0].replace(" SemiBold", "").replace(" Bold", "").replace(" Medium", "") for x in m["fonts"]))
    readme = f"""{p['title']}
SKU {m['sku']} | https://foxyprinting.co.uk/products/{p['handle']}

v2 print file (8 Oct 2026): "{f}" .pdf + .svg, in bar-coasters-v2-artwork.zip, folder {m['sku']}/:
{ZIP}  (md5 {MD5})

- 90 x 90 mm sublimation coaster: trim 90 x 90 + 3 mm bleed = 96 x 96 mm page. Pre-cut blank, so no CUT layer.
- Safe area 3 mm inside the trim; keep detail off the rounded corners.
- PDF layers Artwork + Text; SVG groups Artwork / Text / Guides (hidden). Live, editable text with the sample name "Ava".
- Website boxes: {', '.join(p['fields'])}. Leave optional lines as designed if a box is blank.
- Fonts (OFL, Google Fonts): {fn}. See Fonts/.
{(notes + chr(10)) if notes else ''}
Made from the owner's 2021 file {SRC[k]} (100 x 100 mm, left unchanged); its demo/commercial fonts were replaced.
Generator: foxyprinting-rebrand/tools/bar_coasters_v2/art.py
"""
    fonts = "Fonts for this coaster (SIL Open Font License 1.1):\n" + "".join(
        f"- {GF[x][0]}: {GF[x][1]}\n" for x in m["fonts"]) + f".ttf files: bar-coasters-v2-artwork.zip, folder Fonts/ (with OFL.txt):\n{ZIP}\n"
    out[k] = dict(folder=folder, readme=readme, fonts=fonts)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(out))
