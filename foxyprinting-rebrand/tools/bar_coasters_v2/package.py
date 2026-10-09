"""Build the v2 coaster print files named by SKU and zip them with the fonts.
usage: python3 package.py SRC_DIR OUT_DIR UPDATES_JSON"""
import json, os, sys, zipfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
import coaster_copy as C
from spec import FONTS

src, out, upd = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
sku = {r["key"]: r["sku"] for r in upd}
title = {p["key"]: p["title"] for p in C.P}
os.makedirs(out, exist_ok=True)
man = {}
for p in C.P:
    k = p["key"]
    d = os.path.join(out, sku[k])
    os.makedirs(d, exist_ok=True)
    name = f"{sku[k]} - 90x90mm coaster - PRINT"
    art.build(k, src, d, sku=name, title=p["title"])
    man[k] = dict(sku=sku[k], title=p["title"], handle=p["handle"], files=[name + ".pdf", name + ".svg"],
                  fonts=sorted({FONTS[l["font"]] for l in art.DESIGNS[k]["lines"]}), fields=p["fields"])
json.dump(man, open(os.path.join(out, "manifest.json"), "w"), ensure_ascii=False, indent=1)
fd = os.path.join(art.FONT_DIR)
ofl = open(os.path.join(fd, "OFL.txt")).read()
OFL_HEAD = ("Fonts used in the v2 bar coaster files (all SIL Open Font License 1.1, from Google Fonts):\n"
            "Cinzel (Copyright 2020 The Cinzel Project Authors), Great Vibes (Copyright 2010 The Great Vibes Pro Project Authors),\n"
            "Allura (Copyright 2010 The Allura Project Authors), Playfair Display (Copyright 2017 The Playfair Display Project Authors,\n"
            "Reserved Font Name \"Playfair Display\"), Montserrat (Copyright 2011 The Montserrat Project Authors),\n"
            "Zilla Slab (Copyright 2017, The Mozilla Foundation).\n\n")
z = os.path.join(out, "bar-coasters-v2-artwork.zip")
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for k, m in man.items():
        for f in m["files"]:
            zf.write(os.path.join(out, m["sku"], f), f"{m['sku']}/{f}")
    for f in sorted(set(FONTS.values())):
        zf.write(os.path.join(fd, f), f"Fonts/{f}")
    zf.writestr("Fonts/OFL.txt", OFL_HEAD + ofl)
print(z, os.path.getsize(z))
