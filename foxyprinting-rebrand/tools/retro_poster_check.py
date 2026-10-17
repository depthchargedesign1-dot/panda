"""Checks the retro gaming poster import files. Usage: python3 check.py OUT_DIR export.jsonl"""
import collections, csv, glob, json, os, re, sys

OUT = sys.argv[1]
src, srcv = {}, collections.defaultdict(list)
ids = {}
for line in open(sys.argv[2]):
    o = json.loads(line)
    if "__parentId" in o:
        srcv[o["__parentId"]].append(o)
    else:
        src[o["handle"]] = o
BANNED = re.compile(r"\b(official|licensed|authentic|genuine|approved|endorsed|merchandise|memorabilia|signed|autographed)\b", re.I)
SINGLE_COLS = ["Handle", "Title", "Body (HTML)", "Tags", "SEO Title", "SEO Description", "Option1 Name", "Option1 Value", "Variant SKU", "Variant Price"]
MV_COLS = ["Handle", "Body (HTML)", "Tags", "SEO Title", "SEO Description"]


def check_rows(rows, mv):
    problems = collections.defaultdict(list)
    wc = []
    for r in rows:
        s = src[r["Handle"]]
        vs = srcv[s["id"]]
        b = r["Body (HTML)"]
        text = re.sub(r"<[^>]+>", " ", b.replace("&amp;", "&"))
        n = len(text.split()); wc.append(n)
        if not 150 <= n <= 220: problems["word count"].append((r["Handle"], n))
        if re.search(r"\w+-\w+-\w+", text): problems["hyphen-joined words"].append(r["Handle"])
        if re.search(r"(?<!\w)-(?!\w)|\s-\w|\w-\s", text): problems["stray hyphen"].append(r["Handle"])
        if b.count("<h2>") != 1: problems["h2 count"].append(r["Handle"])
        if re.search(r"\b[A-Z]{6,}\b", text): problems["ALL CAPS word"].append(r["Handle"])
        main = b.split("<h3>Please note</h3>")[0]
        if BANNED.search(re.sub(r"<[^>]+>", " ", main)): problems["banned word"].append(r["Handle"])
        disc = b.split('<p class="disclaimer">')[-1]
        if '<p class="disclaimer">' not in b or "unofficial, fan-made print" not in disc or not b.endswith("</p>"):
            problems["disclaimer"].append(r["Handle"])
        if re.search(r"\b(merchandise|authentic|genuine|approved)\b", disc, re.I): problems["banned in disclaimer"].append(r["Handle"])
        if "[" in b or "{" in b: problems["placeholder"].append(r["Handle"])
        if "style=" in b or "<img" in b or "<span" in b: problems["inline style/img/span"].append(r["Handle"])
        if BANNED.search(r["SEO Title"] + " " + r["SEO Description"]): problems["banned word in SEO"].append(r["Handle"])
        if not len(r["SEO Title"]) <= 60: problems["seo title len"].append(r["Handle"])
        if not 140 <= len(r["SEO Description"]) <= 155: problems["meta len"].append((r["Handle"], len(r["SEO Description"])))
        tags = [t.strip() for t in r["Tags"].split(",")]
        if "third-party-name" not in tags: problems["tag"].append(r["Handle"])
        if set(s["tags"]) - set(tags): problems["lost tag"].append(r["Handle"])
        if mv:
            # size list must match the real variants
            sizes = re.search(r"<h3>Size &amp; details</h3><ul>(.*?)</ul>", b).group(1)
            for v in vs:
                m = re.match(r"(A[0-4]) Print(?: Only| \+ (\w+) Frame)$", v["title"])
                if not m:
                    problems["unexpected variant"].append((r["Handle"], v["title"])); continue
                if m.group(2):
                    framed = re.search(r"Framed[^<]*", sizes)
                    if not framed or m.group(1) not in framed.group(0) or m.group(2).lower() not in framed.group(0):
                        problems["framed variant not in sizes"].append((r["Handle"], v["title"]))
                else:
                    pr = re.search(r"Print only:[^<]*", sizes)
                    if not pr or m.group(1) not in pr.group(0):
                        problems["print variant not in sizes"].append((r["Handle"], v["title"]))
        else:
            if r["Title"] != s["title"]: problems["title changed"].append(r["Handle"])
            if len(vs) != 1 or vs[0]["price"] != "2.99" or r["Variant Price"] != "4.99": problems["price"].append(r["Handle"])
            if r["Variant SKU"] != vs[0]["sku"]: problems["sku changed"].append(r["Handle"])
    return problems, wc


def report(label, pattern, cols, mv):
    files = sorted(f for p in pattern for f in glob.glob(os.path.join(OUT, p)))
    rows, handles = [], collections.Counter()
    print(f"\n== {label}")
    for f in files:
        with open(f, newline="", encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            if rd.fieldnames != cols: print("  WRONG COLUMNS", f, rd.fieldnames)
            rs = list(rd)
        size = os.path.getsize(f)
        print(f"  {os.path.basename(f)}: {len(rs)} rows, {size/1024:.0f} KB {'OK' if size < 15e6 else 'TOO BIG'}",
              "" if mv else dict(collections.Counter(x["Variant Price"] for x in rs)))
        rows += rs
        if "TEST" not in f:
            handles.update(x["Handle"] for x in rs)
    dup = [h for h, n in handles.items() if n > 1]
    print("  rows in main files:", sum(handles.values()), "duplicate handles:", len(dup))
    problems, wc = check_rows(rows, mv)
    print(f"  words min/max/avg {min(wc)}/{max(wc)}/{sum(wc)/len(wc):.0f}")
    for k, v in problems.items():
        print("  PROBLEM", k, len(v), v[:5])
    if not problems:
        print("  all checks passed")
    return handles


a = report("single-variant (price 2.99 -> 4.99)", ["00-TEST-3-products.csv", "01-*.csv"], SINGLE_COLS, False)
b = report("multi-variant (copy only)", ["00-TEST-3-multivariant.csv", "02-*.csv"], MV_COLS, True)
print("\noverlap between single and multi files:", len(set(a) & set(b)))
