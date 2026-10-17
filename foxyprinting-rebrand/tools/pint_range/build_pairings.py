"""Build print files + checks for the pint-range pairings (7 tumblers; the 3 sets reuse the pint/tumbler files).

usage: python3 tools/pint_range/build_pairings.py OUT_DIR
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as B  # noqa: E402
import pairings as PA  # noqa: E402

A = PA.D.A


def main():
    out = Path(sys.argv[1])
    (out / "raster").mkdir(parents=True, exist_ok=True)
    rep = {}
    for p in PA.P:
        vs = PA.variants(p)
        r = B.check(p)
        if p["kind"] == "tumbler":
            pre = vs[0][1].rsplit("-", 1)[0]
            d = out / pre
            d.mkdir(exist_ok=True)
            small = 99
            for vals, sku, _, _ in vs:
                els = p["design"](vals)
                small = min(small, min(e["size"] / 25.4 * 72 for e in els if e["k"] == "text"))
                nm = (f"{sku} - 50x50mm tumbler transfer" + "".join(f" - {v}" for v in vals) + " - PRINT").replace("&", "and")
                A.write_svg(els, A.TUMBLER[0], A.TUMBLER[1], str(d / f"{nm}.svg"), cut=2.5)
                A.write_pdf(els, A.TUMBLER[0], A.TUMBLER[1], str(d / f"{nm}.pdf"), p["title"], cut=2.5)
                A.raster(els, A.TUMBLER[0], A.TUMBLER[1], pxmm=40, transparent=True).save(out / "raster" / f"{sku}.png")
            r["smallest_text_pt"] = round(small, 1)
        r["variants"] = len(vs)
        rep[p["key"]] = r
        print(p["key"], r)
    json.dump(rep, open(out / "check.json", "w"), indent=1)


if __name__ == "__main__":
    main()
