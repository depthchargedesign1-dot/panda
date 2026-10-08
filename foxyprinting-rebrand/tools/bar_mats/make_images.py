"""Make the product images for every new bar mat. Usage: make_images.py SCRATCH OUTDIR"""
import json, os, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from images import white_composite, clean_mockup, wood_mockup, trim, save

S, OUT = Path(sys.argv[1]), Path(sys.argv[2])
ROOT = Path(__file__).resolve().parents[2]
prods = json.load(open(ROOT / "exports/bar-mats/2026-10-08/products.json"))
WOOD = S / "wood.jpg"
RUN = (150, 150, 2648, 862); MAT = (776, 1144, 2024, 1852)
manifest = {}
for o in prods:
    k, g, pk, design = o["key"], o["group"], o["primary"], o["design"]
    d = OUT / k; d.mkdir(parents=True, exist_ok=True)
    files = []
    if g == "GB":
        c = k[3:]
        L = trim(Image.open(S / f"gbflat/{c}_L.jpg").convert("RGB")); Sm = trim(Image.open(S / f"gbflat/{c}_S.jpg").convert("RGB"))
        save(Image.open(S / f"dl1/gb_{c}.jpg").convert("RGB"), d / "1-main.jpg")
        save(white_composite(L, Sm), d / "2-both-sizes.jpg")
        files = [("1-main.jpg", f"{pk[0].upper()+pk[1:]} – large runner and small mat on a home bar"),
                 ("2-both-sizes.jpg", f"{design} bar runner and small bar mat with blank badge circles for your club logo")]
    elif g in ("X3", "OT"):
        n = o["img"][1]; src = S / (f"dl1/x3_{n}.jpg" if g == "X3" and n <= 28 else (f"dl2/x3_{n}.jpg" if g == "X3" else f"dl2/ot_{n:02d}.jpg"))
        im = Image.open(src).convert("RGB")
        save(white_composite(im.crop(RUN), im.crop(MAT)), d / "1-main.jpg")
        save(clean_mockup(src), d / "2-on-the-bar.jpg")
        files = [("1-main.jpg", f"{pk[0].upper()+pk[1:]} – long runner and small mat, {design.lower()} design"),
                 ("2-on-the-bar.jpg", f"{design} bar runner and bar mat on a dark wooden bar top")]
    else:
        if g == "BR":
            key = o["img"][1]
            Sm = Image.open(S / f"dl2/br_{key}.jpg").convert("RGB")
            Lp = S / f"dl3/brL_{key}.jpg"
            L = Image.open(Lp).convert("RGB") if Lp.exists() else None
        else:
            n = o["img"][1]
            L = Image.open(S / f"anna/a{n:02d}.jpg").convert("RGB")
            sp = S / f"dl3/an440_{n:02d}.jpg"
            Sm = Image.open(sp).convert("RGB") if sp.exists() else None
        big = L if L is not None else Sm
        small = Sm if L is not None else None
        save(white_composite(big, small), d / "1-main.jpg")
        save(wood_mockup(big, small, WOOD), d / "2-on-the-bar.jpg")
        files = [("1-main.jpg", f"{pk[0].upper()+pk[1:]} – {design.lower()} design"),
                 ("2-on-the-bar.jpg", f"{design} bar mat runner laid on a wooden home bar")]
    manifest[k] = [{"file": str(d / f), "alt": a} for f, a in files]
json.dump(manifest, open(OUT / "images.json", "w"), ensure_ascii=False, indent=1)
print(len(manifest), "products,", sum(len(v) for v in manifest.values()), "images")
