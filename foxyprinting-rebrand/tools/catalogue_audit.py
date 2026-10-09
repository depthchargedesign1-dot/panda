"""Full catalogue health check: every product against the CLAUDE.md house rules and Google Shopping needs.

Input: a bulk export JSONL from this query (one product line, then its variant lines with __parentId):
  products { id handle title status productType vendor tags templateSuffix descriptionHtml createdAt
    seo{title description} category{fullName}
    cp/cond/gpc/gen/age/col/mpn: metafield(namespace:"mm-google-shopping", key:...){value}
    mock/pf: metafield(namespace:"foxy", key:"mockup"/"personalise_fields"){value}
    featuredMedia{... on MediaImage{image{altText}}} mediaCount{count}
    variants{ id sku barcode price title } }
Usage: python3 -I catalogue_audit.py export.jsonl outdir
Writes outdir/issues.csv (one row per product with issues) and outdir/summary.md. Read only: changes nothing.
"""
import collections, csv, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_group import age_group

BANNED = re.compile(r"\b(official(ly)? licensed|licensed|authentic|genuine|memorabilia|limited edition|autographed|hand[- ]signed|"
                    r"official merchandise)\b", re.I)
BAD_HTML = re.compile(r"<h1|style=|<span|<font|<table|<img|<script", re.I)
GKEYS = {"cp": "custom_product", "cond": "condition", "gpc": "google_product_category", "gen": "gender",
         "age": "age_group", "col": "color", "mpn": "mpn"}


def words(h):
    return len(re.sub(r"<[^>]+>", " ", html.unescape(h or "")).split())


def load(path):
    prods = collections.OrderedDict()
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            prods[o["__parentId"]]["variants"].append(o)
        else:
            o["variants"] = []
            prods[o["id"]] = o
    return prods


def mf(p, k):
    return ((p.get(k) or {}).get("value") or "").strip()


def audit(p, dup_desc, dup_sku):
    iss = []
    d = p.get("descriptionHtml") or ""
    w = words(d)
    if w == 0:
        iss.append("desc-empty")
    elif w < 60:
        iss.append("desc-short")
    if d and BAD_HTML.search(d):
        iss.append("desc-messy-html")
    if d and "<h2" not in d.lower():
        iss.append("desc-no-h2")
    if re.search(r"\[[^\]]{2,40}\]", d):
        iss.append("desc-brackets")
    if BANNED.search(d) or BANNED.search(p["title"]):
        iss.append("banned-word")
    if dup_desc.get(d.strip(), 0) > 1 and w:
        iss.append("desc-duplicate")
    if "third-party-name" in p["tags"] and 'class="disclaimer"' not in d:
        iss.append("disclaimer-missing")
    seo = p.get("seo") or {}
    t, m = (seo.get("title") or "").strip(), (seo.get("description") or "").strip()
    if not t: iss.append("seo-title-missing")
    elif len(t) > 70: iss.append("seo-title-long")
    if not m: iss.append("meta-desc-missing")
    elif len(m) < 70: iss.append("meta-desc-short")
    elif len(m) > 160: iss.append("meta-desc-long")
    if len(p["title"]) > 150: iss.append("title-over-150")
    if (p.get("vendor") or "") != "Foxy Printing": iss.append("vendor")
    if not (p.get("productType") or "").strip(): iss.append("type-missing")
    if not p["tags"]: iss.append("tags-missing")
    if not (p.get("category") or {}).get("fullName"): iss.append("shopify-category-missing")
    for k, name in GKEYS.items():
        if not mf(p, k): iss.append(f"g-{name}-missing")
    if mf(p, "cp") and mf(p, "cp") != "true": iss.append("g-custom_product-not-true")
    if mf(p, "cond") and mf(p, "cond") != "new": iss.append("g-condition-not-new")
    if mf(p, "gen") and mf(p, "gen") != "unisex": iss.append("g-gender-not-unisex")
    want = age_group(p.get("productType"), p.get("title"), p.get("tags"))
    if mf(p, "age") and mf(p, "age") != want: iss.append("g-age_group-wrong")
    if mf(p, "gpc") and re.fullmatch(r"[\d.]+", mf(p, "gpc")): iss.append("g-category-is-number")
    skus = [v.get("sku") or "" for v in p["variants"]]
    if not p["variants"] or any(not s for s in skus): iss.append("sku-missing")
    if any(s and dup_sku[s] > 1 for s in skus): iss.append("sku-duplicate")
    if mf(p, "mpn") and skus and mf(p, "mpn") not in skus: iss.append("g-mpn-not-a-sku")
    if any(float(v.get("price") or 0) <= 0 for v in p["variants"]): iss.append("price-zero")
    if not (p.get("mediaCount") or {}).get("count"): iss.append("no-image")
    else:
        alt = (((p.get("featuredMedia") or {}).get("image") or {}).get("altText") or "").strip()
        if not alt: iss.append("main-image-alt-missing")
    if (p.get("templateSuffix") or "") in ("personalised", "card"):
        if not mf(p, "mock"): iss.append("foxy-mockup-missing")
        if not mf(p, "pf"): iss.append("foxy-personalise_fields-missing")
    return iss


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    prods = load(src)
    active = [p for p in prods.values() if p["status"] == "ACTIVE"]
    dup_desc = collections.Counter((p.get("descriptionHtml") or "").strip() for p in active)
    dup_sku = collections.Counter(v.get("sku") for p in prods.values() for v in p["variants"] if v.get("sku"))
    cnt, rows = collections.Counter(), []
    by_type = collections.defaultdict(collections.Counter)
    for p in prods.values():
        iss = audit(p, dup_desc, dup_sku)
        for i in iss:
            cnt[(i, p["status"])] += 1
            if p["status"] == "ACTIVE":
                by_type[i][p.get("productType") or "(none)"] += 1
        if iss:
            rows.append([p["id"].rsplit("/", 1)[1], p["handle"], p["status"], p["title"], p.get("productType"), "; ".join(iss)])
    with open(f"{out}/issues.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f); wr.writerow(["id", "Handle", "Status", "Title", "Type", "Issues"]); wr.writerows(rows)
    n = collections.Counter(p["status"] for p in prods.values())
    nv = sum(len(p["variants"]) for p in prods.values())
    keys = sorted({k for k, _ in cnt}, key=lambda k: -cnt[(k, "ACTIVE")])
    with open(f"{out}/summary.md", "w", encoding="utf-8") as f:
        f.write(f"Products: {dict(n)}; variants: {nv}; products with any issue: {len(rows)}\n\n")
        f.write("| issue | active | draft | archived | top active types |\n|---|---:|---:|---:|---|\n")
        for k in keys:
            top = ", ".join(f"{t} {c}" for t, c in by_type[k].most_common(4))
            f.write(f"| {k} | {cnt[(k,'ACTIVE')]} | {cnt[(k,'DRAFT')]} | {cnt[(k,'ARCHIVED')]} | {top} |\n")
    print(open(f"{out}/summary.md").read())
