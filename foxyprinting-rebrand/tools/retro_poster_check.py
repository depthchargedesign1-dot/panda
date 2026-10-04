import collections, csv, glob, json, os, re, sys
OUT = sys.argv[1]
rows = json.load(open(os.path.join(OUT, "_rows.json")))
src = {}
for line in open(sys.argv[2]):
    o = json.loads(line)
    if "__parentId" not in o:
        src[o["handle"]] = o
problems = collections.defaultdict(list)
wc = []
BANNED = re.compile(r"\b(official|licensed|authentic|genuine|approved|endorsed|merchandise|memorabilia|signed|autographed)\b", re.I)
for r in rows:
    b = r["Body (HTML)"]
    text = re.sub(r"<[^>]+>", " ", b.replace("&amp;", "&"))
    n = len(text.split()); wc.append(n)
    if not 150 <= n <= 220: problems["word count"].append((r["Handle"], n))
    if re.search(r"\w+-\w+-\w+", text): problems["hyphen-joined words"].append(r["Handle"])
    if re.search(r"(?<!\w)-(?!\w)|\s-\w|\w-\s", text): problems["stray hyphen"].append(r["Handle"])
    if b.count("<h2>") != 1: problems["h2 count"].append(r["Handle"])
    if re.search(r"\b[A-Z]{6,}\b", text.replace("FOXY", "")): problems["ALL CAPS word"].append((r["Handle"], re.findall(r"\b[A-Z]{6,}\b", text)))
    main = b.split('<h3>Please note</h3>')[0]
    if BANNED.search(re.sub(r"<[^>]+>", " ", main)): problems["banned word"].append(r["Handle"])
    disc = b.split('<p class="disclaimer">')[-1]
    if '<p class="disclaimer">' not in b or not b.rstrip().endswith("</p>") or "unofficial, fan-made print" not in disc:
        problems["disclaimer"].append(r["Handle"])
    if re.search(r"\b(merchandise|authentic|genuine|approved)\b", disc, re.I): problems["banned in disclaimer"].append(r["Handle"])
    if "[" in b or "{" in b: problems["placeholder"].append(r["Handle"])
    if "style=" in b or "<img" in b or "<span" in b: problems["inline style/img/span"].append(r["Handle"])
    g = r["_game"]
    if g:
        kw = f"{g} retro gaming poster".lower()
        opening = re.sub(r"<[^>]+>", "", b.split("</p>")[0])
        first = opening.split(". ")[0]
        if kw not in first.lower(): problems["keyword not in opening"].append(r["Handle"])
    if not len(r["SEO Title"]) <= 60: problems["seo title len"].append(r["Handle"])
    if not 140 <= len(r["SEO Description"]) <= 155: problems["meta len"].append((r["Handle"], len(r["SEO Description"])))
    tags = [t.strip() for t in r["Tags"].split(",")]
    s = src[r["Handle"]]
    if "third-party-name" not in tags: problems["tag"].append(r["Handle"])
    if set(s["tags"]) - set(tags): problems["lost tag"].append(r["Handle"])
    if r["Title"] != s["title"]: problems["title changed"].append(r["Handle"])
    if r["_old_price"] != "2.99" or r["Variant Price"] != "4.99": problems["price"].append(r["Handle"])
# csv files
files = sorted(glob.glob(os.path.join(OUT, "0*.csv")))
total = 0
for f in files:
    with open(f, newline="", encoding="utf-8") as fh:
        rs = list(csv.DictReader(fh))
    size = os.path.getsize(f)
    if not f.endswith("TEST-3-products.csv"):
        total += len(rs)
    print(os.path.basename(f), len(rs), "rows", f"{size/1024:.0f} KB", "OK" if size < 15e6 else "TOO BIG",
          "prices:", dict(collections.Counter(x["Variant Price"] for x in rs)))
print("rows in import files", total, "of", len(rows))
print("word count min/max/avg", min(wc), max(wc), sum(wc) / len(wc))
for k, v in problems.items():
    print("PROBLEM", k, len(v), v[:5])
print("no problems" if not problems else "")
