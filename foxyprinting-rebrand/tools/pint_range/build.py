"""Build print files + checks for the 8 new pint glasses.

usage: python3 tools/pint_range/build.py OUT_DIR
  OUT_DIR/<SKU prefix>/<SKU> - 90x130mm pint transfer [- options] - PRINT.svg/.pdf  (CUT trim layer, live text)
  OUT_DIR/raster/<SKU>.png (transparent, 40 px/mm) for the photo composites
  OUT_DIR/check.json  copy/SEO length checks
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import designs as D  # noqa: E402
import products as PR  # noqa: E402

A = D.A


def check(p):
    words = len(re.sub(r"<[^>]+>", " ", p["html"]).split())
    return dict(title_len=len(p["title"]), seo_title_len=len(p["seo_title"]), seo_desc_len=len(p["seo_desc"]), words=words,
                h2=p["html"].count("<h2>"), ok=(len(p["title"]) <= 150 and len(p["seo_title"]) <= 60 and 140 <= len(p["seo_desc"]) <= 160
                                                 and 180 <= words <= 350 and p["html"].count("<h2>") == 1))


def main():
    out = Path(sys.argv[1])
    (out / "raster").mkdir(parents=True, exist_ok=True)
    report = {}
    for p in PR.P:
        vs = PR.variants(p)
        pre = vs[0][1].rsplit("-", 1)[0]
        d = out / pre
        d.mkdir(exist_ok=True)
        small = 99
        for vals, sku in vs:
            els = p["design"](vals)
            small = min(small, min(e["size"] / 25.4 * 72 for e in els if e["k"] == "text"))
            nm = (f"{sku} - 90x130mm pint transfer" + "".join(f" - {v}" for v in vals) + " - PRINT").replace("&", "and")
            A.write_svg(els, D.W, D.H, str(d / f"{nm}.svg"), cut=2.5)
            A.write_pdf(els, D.W, D.H, str(d / f"{nm}.pdf"), p["title"], cut=2.5)
            A.raster(els, D.W, D.H, pxmm=40, transparent=True).save(out / "raster" / f"{sku}.png")
        report[p["key"]] = dict(check(p), prefix=pre, variants=len(vs), smallest_text_pt=round(small, 1))
        print(p["key"], report[p["key"]])
    json.dump(report, open(out / "check.json", "w"), indent=1)


if __name__ == "__main__":
    main()
