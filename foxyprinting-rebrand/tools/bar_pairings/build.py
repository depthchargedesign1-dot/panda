"""Build artwork, zips, mockups and productCreate inputs for the bar-mat pairing products (8 Oct 2026).

usage: python3 tools/bar_pairings/build.py OUT_DIR
Writes OUT_DIR/<key>/... and OUT_DIR/manifest.json; productCreate inputs go to
exports/bar-pairings/2026-10-08/products.json.
"""
import json
import os
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools" / "artwork"))
import bar_pairings as A  # noqa: E402
import data as D  # noqa: E402
from PIL import Image  # noqa: E402

OUT = Path(sys.argv[1])
CDN = "https://cdn.shopify.com/s/files/1/1774/9115/files/bar-mat-{}-1-main.jpg"
MAT_CODE = {
    "personalised-bar-mat-runner-walnut-gold": "x3-26", "personalised-bar-mat-runner-crown-copper": "x3-23",
    "personalised-bar-mat-runner-rustic-established": "x3-28", "bar-mat-runner-my-cave-my-rules-navy": "ot-1",
    "bar-mat-runner-man-cave-welcome": "ot-3", "bar-mat-runner-man-cave-slate": "ot-9",
    "personalised-bar-mat-runner-best-bar-in-town": "br-best-bar", "personalised-bar-mat-runner-distressed-union-jack": "br-union-jack",
    "personalised-bar-mat-runner-vintage-black-established": "br-vintage-black",
    "personalised-bar-mat-runner-vintage-wood-established": "br-vintage-wood", "personalised-bar-mat-runner-name-man-cave": "br-man-cave",
    "bar-mat-runner-beer-oclock-bottles": "an-4", "bar-mat-runner-its-beer-oclock": "an-12",
    "personalised-bar-mat-runner-best-bar-cream": "an-8",
    "personalised-club-bar-mat-red-and-white": "gb-red-white", "personalised-club-bar-mat-red-and-white-stripes": "gb-red-white-stripes",
    "personalised-club-bar-mat-claret-and-blue": "gb-claret-blue",
}
SHAPES = {"coaster": [("coaster", A.COASTER, "90x90mm", None)],
          "pint": [("pint", A.PINT, "v2 90x130mm transfer", 2.5)],
          "tumbler": [("tumbler", A.TUMBLER, "v2 50x50mm transfer", 2.5)],
          "sign": [("wide", A.SIGN_WIDE, "12x5in", None), ("tall", A.SIGN_TALL, "8x10in", None)]}
FONT_FILES = [A.BEBAS, A.PACIFICO, A.BARLOW, A.BARLOWB]


def mat_image(handle, cache):
    code = MAT_CODE[handle]
    f = cache / f"{code}.jpg"
    if not f.exists():
        urllib.request.urlretrieve(CDN.format(code), f)
    return Image.open(f)


def design(p, shape, w, h, vals, cw=None, sample=False):
    if p["theme"] == "club":
        return A.club(shape, w, h, vals, cw, sample=sample)
    return A.themed(p["theme"], shape, w, h, vals, sample=sample)


def mock(p, shape, w, h, vals, cw=None):
    els = design(p, shape, w, h, vals, cw, sample=True)
    glass = shape in ("pint", "tumbler")
    tex = A.raster(els, w, h, pxmm=14 if shape != "wide" else 8, transparent=glass)
    if shape == "coaster":
        return A.mock_coaster(tex), tex
    if glass:
        return A.mock_glass(tex, shape), tex
    return A.mock_sign(tex, shape == "wide"), tex


def flat_on_white(tex, pad=200):
    img = Image.new("RGBA", (A.N, A.N), (255, 255, 255, 255))
    t = tex.copy()
    t.thumbnail((A.N - 2 * pad, A.N - 2 * pad), Image.LANCZOS)
    t = A.round_corners(t, 24)
    img.alpha_composite(t, ((A.N - t.width) // 2, (A.N - t.height) // 2))
    return img.convert("RGB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = OUT / "_mats"
    cache.mkdir(exist_ok=True)
    manifest, inputs = {}, []
    ofl = (ROOT / "tools/artwork/assets/fonts/OFL.txt").read_text()
    ofl_all = ("Fonts used: Bebas Neue (Copyright 2010 Dharma Type), Pacifico (Copyright 2018 The Pacifico Project Authors),\n"
               "Barlow Condensed (Copyright 2017 The Barlow Project Authors). All under the SIL Open Font License 1.1:\n\n" + ofl)
    for p in D.P:
        k = p["key"]
        d = OUT / k
        (d / "print").mkdir(parents=True, exist_ok=True)
        (d / "img").mkdir(parents=True, exist_ok=True)
        pre = f"FOXY-{p['machine']}-{p['code']}"
        colours = A.CLUB if p["theme"] == "club" else [None]
        shapes = SHAPES[p["kind"]]
        # ---- variants
        variants = []
        n = 0
        for cw in colours:
            for (shape, (w, h), label, cut) in shapes:
                n += 1
                v = dict(sku=f"{pre}-{n:02d}", shape=shape, colour=cw[1] if cw else None, colour_key=cw[0] if cw else None,
                         gcolour=cw[6] if cw else None)
                if p["kind"] == "sign":
                    v["size"] = dict(wide="12 x 5in panoramic", tall="8 x 10in")[shape]
                    v["price"] = dict(wide="19.99", tall="24.99")[shape]
                else:
                    v["price"] = dict(coaster=D.COASTER_PRICE, pint=D.PINT_PRICE, tumbler=D.TUMBLER_PRICE)[p["kind"]]
                variants.append(v)
        # ---- print files
        files = []
        for v in variants:
            shape = v["shape"]
            (_, (w, h), label, cut) = [s for s in shapes if s[0] == shape][0]
            cw = [c for c in A.CLUB if c[0] == v["colour_key"]][0] if v["colour_key"] else None
            els = design(p, shape, w, h, p["art"], cw)
            nm = f"{v['sku']} - {label}" + (f" - {cw[1]}" if cw else "") + " - PRINT"
            nm = nm.replace("&", "and")
            A.write_svg(els, w, h, str(d / "print" / f"{nm}.svg"), cut=cut)
            A.write_pdf(els, w, h, str(d / "print" / f"{nm}.pdf"), p["title"], cut=cut)
            files.append(nm)
            v["print"] = nm
        # check render of the first file
        # ---- zip (PDF + SVG + fonts)
        z = d / f"{pre}-artwork.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted((d / "print").iterdir()):
                zf.write(f, f"print/{f.name}")
            for f in FONT_FILES:
                zf.write(f, f"Fonts/{os.path.basename(f)}")
            zf.writestr("Fonts/OFL.txt", ofl_all)
        # ---- mockups
        imgs = []
        if p["theme"] == "club":
            for i, cw in enumerate(A.CLUB):
                shape, (w, h) = shapes[0][0], shapes[0][1]
                im, tex = mock(p, shape, w, h, p["sample"], cw)
                f = d / "img" / f"{k}-{cw[0]}.jpg"
                im.save(f, quality=86)
                kind_word = dict(coaster="coaster", pint="pint glass", sign="bar sign")[p["kind"]]
                imgs.append(dict(file=str(f), colour=cw[1],
                                 alt=f"Personalised club colours {kind_word} in {cw[1].lower()} with a badge circle and your club name"))
                if i == 0:
                    first_tex = tex
            # move red & white first
            if p["kind"] == "sign":
                im, tex = mock(p, "tall", *A.SIGN_TALL, p["sample"], A.CLUB[0])
                f = d / "img" / f"{k}-tall.jpg"
                im.save(f, quality=86)
                imgs.insert(1, dict(file=str(f), colour=None, alt="Personalised club colours bar sign in the 8 x 10in size with your club badge at the top"))
            mainimg = Image.open(imgs[0]["file"])
        else:
            shape, (w, h) = shapes[0][0], shapes[0][1]
            im, tex = mock(p, shape, w, h, p["sample"])
            f = d / "img" / f"{k}-1-main.jpg"
            im.save(f, quality=86)
            pk = p["seo_title"].split(" | ")[0].split(" – ")[0]
            imgs.append(dict(file=str(f), colour=None, alt=f"{pk} showing the name {p['sample']['name'].title()} – {p['title'].split(' – ')[1].lower()}"))
            mainimg = im
            if p["kind"] == "sign":
                im2, _ = mock(p, "tall", *A.SIGN_TALL, p["sample"])
                f = d / "img" / f"{k}-2-tall.jpg"
                im2.save(f, quality=86)
                imgs.append(dict(file=str(f), colour=None, alt=f"{pk} in the 8 x 10in size"))
            else:
                f = d / "img" / f"{k}-2-design.jpg"
                flat_on_white(tex).save(f, quality=86)
                imgs.append(dict(file=str(f), colour=None, alt=f"Close-up of the printed design on the {pk.lower()}"))
        # pairing image with the matching bar mat
        f = d / "img" / f"{k}-pair.jpg"
        A.pair_image(mainimg, mat_image("personalised-club-bar-mat-red-and-white" if p["theme"] == "club" else p["matches"][0], cache)).save(f, quality=86)
        pk = p["seo_title"].split(" | ")[0].split(" – ")[0]
        imgs.append(dict(file=str(f), colour=None, alt=f"{pk} with the matching bar mat runner"))
        manifest[k] = dict(prefix=pre, zip=str(z), files=files, images=imgs, variants=variants)
        # ---- productCreate input
        mf = [dict(namespace="mm-google-shopping", key="custom_product", type="boolean", value="true"),
              dict(namespace="mm-google-shopping", key="condition", type="single_line_text_field", value="new"),
              dict(namespace="mm-google-shopping", key="google_product_category", type="single_line_text_field", value=p["cat"]),
              dict(namespace="mm-google-shopping", key="gender", type="single_line_text_field", value="unisex"),
              dict(namespace="mm-google-shopping", key="age_group", type="single_line_text_field", value="adult"),
              dict(namespace="mm-google-shopping", key="color", type="single_line_text_field", value=p["color"]),
              dict(namespace="mm-google-shopping", key="mpn", type="single_line_text_field", value=variants[0]["sku"]),
              dict(namespace="foxy", key="mockup", type="single_line_text_field", value=p["mockup"]),
              dict(namespace="foxy", key="personalise_fields", type="list.single_line_text_field",
                   value=json.dumps(p["fields"], ensure_ascii=False))]
        opts = []
        if p["theme"] == "club":
            opts.append(dict(name="Team colours", values=[dict(name=c[1]) for c in A.CLUB]))
        if p["kind"] == "sign":
            opts.append(dict(name="Size", values=[dict(name="12 x 5in panoramic"), dict(name="8 x 10in")]))
        prod = dict(title=p["title"], handle=p["handle"], vendor="Foxy Printing", productType=p["productType"], status="ACTIVE",
                    tags=sorted(set(p["tags"])), seo=dict(title=p["seo_title"], description=p["seo_desc"]),
                    descriptionHtml=p["descriptionHtml"], templateSuffix="personalised", metafields=mf)
        if opts:
            prod["productOptions"] = opts
        inputs.append(dict(key=k, product=prod, variants=variants, kind=p["kind"]))
        print(k, len(variants), "variants", len(files), "print files", len(imgs), "images")
    json.dump(manifest, open(OUT / "manifest.json", "w"), ensure_ascii=False, indent=1)
    exp = ROOT / "exports/bar-pairings/2026-10-08"
    exp.mkdir(parents=True, exist_ok=True)
    json.dump(inputs, open(exp / "products.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
