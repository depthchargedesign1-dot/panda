"""v2 glass transfer artwork at the owner's real print areas (8 Oct 2026):
pint glass 90 x 130 mm (w x h), whisky tumbler 50 x 50 mm, + 3 mm bleed, 3 mm safe, red 0.25 mm CUT trim path
(2.5 mm corners), live text, OFL fonts. UV DTF transfer kept 10 mm below the rim.

usage: python3 tools/bar_pairings/glass_v2.py OUT_DIR [OLD_ZIP]
Writes OUT_DIR/<SKU prefix>/<SKU> - v2 <size> transfer [- colour] - PRINT.svg/.pdf, check PNGs, and, with OLD_ZIP,
OUT_DIR/bar-pairings-artwork-v2.zip = the coaster + sign files from the v1 zip + the v2 glass files + Fonts.
"""
import os
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools" / "artwork"))
import bar_pairings as A  # noqa: E402
import data as D  # noqa: E402

LABEL = {"pint": "v2 90x130mm transfer", "tumbler": "v2 50x50mm transfer"}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    made = {}
    for p in D.P:
        if p["kind"] not in ("pint", "tumbler"):
            continue
        shape = p["kind"]
        w, h = A.PINT if shape == "pint" else A.TUMBLER
        pre = f"FOXY-{p['machine']}-{p['code']}"
        d = out / pre
        d.mkdir(exist_ok=True)
        colours = A.CLUB if p["theme"] == "club" else [None]
        files = []
        for n, cw in enumerate(colours, 1):
            sku = f"{pre}-{n:02d}"
            els = A.club(shape, w, h, p["art"], cw) if cw else A.themed(p["theme"], shape, w, h, p["art"])
            nm = (f"{sku} - {LABEL[shape]}" + (f" - {cw[1]}" if cw else "") + " - PRINT").replace("&", "and")
            A.write_svg(els, w, h, str(d / f"{nm}.svg"), cut=2.5)
            A.write_pdf(els, w, h, str(d / f"{nm}.pdf"), p["title"] + " (v2)", cut=2.5)
            files.append(nm)
            if n == 1:
                subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", str(d / f"{nm}.pdf"), str(out / f"check-{pre}")], check=True)
        made[p["key"]] = dict(prefix=pre, files=files, size=f"{w:g} x {h:g} mm")
        print(p["key"], pre, len(files), "files", f"{w:g}x{h:g}")
    if len(sys.argv) > 2:
        old = zipfile.ZipFile(sys.argv[2])
        z = out / "bar-pairings-artwork-v2.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for i in old.infolist():
                top = i.filename.split("/")[0]
                if top.startswith("FOXY-UVDTF-") or i.is_dir():
                    continue  # old 70x90 / 70x60 glass placeholders left out of v2
                zf.writestr(i, old.read(i))
            for pre_dir in sorted(x for x in out.iterdir() if x.is_dir()):
                for f in sorted(pre_dir.iterdir()):
                    zf.write(f, f"{pre_dir.name}/{f.name}")
            zf.writestr("READ ME - v2 sizes.txt", README)
        print("zip", z, z.stat().st_size)
    return made


README = """bar-pairings-artwork-v2.zip (8 Oct 2026)

Same as bar-pairings-artwork.zip, except the 10 glass products now use the owner's real UV DTF print areas:
  * pint glasses (20oz nonic): 90 x 130 mm (w x h) trim, page 96 x 136 mm with 3 mm bleed
  * whisky tumblers: 50 x 50 mm trim, page 56 x 56 mm with 3 mm bleed
3 mm safe area inside the trim, red (RGB 255,0,0) 0.25 mm CUT trim path with 2.5 mm corners on its own layer,
live editable text (sample name "Ava"), OFL fonts in Fonts/. Apply the transfer 10 mm below the rim.
The old 70 x 90 mm / 70 x 60 mm placeholder glass files are not in this zip (they are still in v1 and in Dropbox).
Coaster (90 x 90 mm) and metal sign files are unchanged from v1.
"""

if __name__ == "__main__":
    main()
