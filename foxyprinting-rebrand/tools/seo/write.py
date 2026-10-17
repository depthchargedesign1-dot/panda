"""Write the SEO import CSVs, review sample and run the checks."""
import collections
import csv
import glob
import json
import os
import random
import re

import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = build.OUT
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "*.csv")):
    os.remove(f)

rows = json.load(open(os.path.join(HERE, "rows.json")))
rows.sort(key=lambda r: r["handle"])
COLS = ["Handle", "SEO Title", "SEO Description"]


def out_row(r):
    return {"Handle": r["handle"], "SEO Title": r["t"], "SEO Description": r["d"]}


def pick(fam, rx):
    for r in rows:
        if r["fam"] == fam and r["wrote_t"] and r["wrote_d"] and re.search(rx, r["old_title"], re.I):
            return r


byh = {r["handle"]: r for r in rows}
test = [byh["personalised-blue-bike-birthday-card"], byh["worlds-best-public-librarian"], byh["roxy-mitchell-2015-celebrity-face-mask"]]
test_handles = {r["handle"] for r in test}


def write(name, rs):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rs:
            w.writerow(out_row(r))
    return p


files = [(write("00-TEST-3-products.csv", test), len(test))]
main_rows = [r for r in rows if r["handle"] not in test_handles]
for i in range(0, len(main_rows), 10000):
    chunk = main_rows[i:i + 10000]
    files.append((write(f"{i // 10000 + 1:02d}-seo.csv", chunk), len(chunk)))

# review sample
random.seed(20261004)
sample = random.sample(rows, 200)
with open(os.path.join(OUT, "review-sample.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Handle", "Family", "Product title (unchanged)", "Old SEO title", "New SEO title", "Old SEO description",
                "New SEO description", "Title written?", "Description written?"])
    for r in sample:
        w.writerow([r["handle"], r["fam"], r["old_title"], r["old_seo_t"], r["t"], r["old_seo_d"], r["d"],
                    "yes" if r["wrote_t"] else "kept", "yes" if r["wrote_d"] else "kept"])

# ---------------- checks (re-read the files)
problems = collections.defaultdict(list)
seen_handles = collections.Counter()
fam_of = {r["handle"]: r["fam"] for r in rows}
by_fam_title = collections.defaultdict(list)
for p, n in files:
    with open(p, newline="", encoding="utf-8") as fh:
        rs = list(csv.DictReader(fh))
    assert list(rs[0].keys()) == COLS, p
    if os.path.getsize(p) >= 15e6:
        problems["file too big"].append(p)
    if len(rs) > 10000:
        problems["too many rows"].append(p)
    for r in rs:
        if not p.endswith("00-TEST-3-products.csv"):
            seen_handles[r["Handle"]] += 1
        t, d = r["SEO Title"], r["SEO Description"]
        if not t or len(t) > 60:
            problems["title length"].append((r["Handle"], t))
        if not d or not 140 <= len(d) <= 155:
            problems["meta length"].append((r["Handle"], len(d or "")))
        for s, kind in ((t, "title"), (d, "meta")):
            for pr in build.problems(s or ""):
                problems[f"{kind}: {pr.split(':')[0]}"].append((r["Handle"], s))
            if " - -" in (s or ""):
                problems[f"{kind}: ' - -'"].append(r["Handle"])
        if build.PROFANE.search(d or ""):
            problems["meta swearing"].append(r["Handle"])
        if not p.endswith("00-TEST-3-products.csv"):
            by_fam_title[(fam_of[r["Handle"]], t.lower())].append(r["Handle"])
dups = {k: v for k, v in by_fam_title.items() if len(v) > 1}
if dups:
    problems["duplicate SEO title within family"] = list(dups.items())[:20]
if any(v > 1 for v in seen_handles.values()):
    problems["handle in two files"].append([h for h, v in seen_handles.items() if v > 1][:5])
missing = len(rows) - len(test) - sum(seen_handles.values())
if missing:
    problems["rows missing from files"].append(missing)

json.dump({"files": [(os.path.basename(p), n, os.path.getsize(p)) for p, n in files],
           "test": [out_row(r) for r in test],
           "problems": {k: v[:10] if isinstance(v, list) else v for k, v in problems.items()},
           "fam_counts": collections.Counter(r["fam"] for r in rows),
           "wrote_t": sum(r["wrote_t"] for r in rows), "wrote_d": sum(r["wrote_d"] for r in rows),
           "both": sum(r["wrote_t"] and r["wrote_d"] for r in rows),
           "only_t": sum(r["wrote_t"] and not r["wrote_d"] for r in rows),
           "only_d": sum(r["wrote_d"] and not r["wrote_t"] for r in rows)},
          open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=str)
for p, n in files:
    print(os.path.basename(p), n, "rows", f"{os.path.getsize(p) / 1e6:.2f} MB")
print("PROBLEMS:", {k: len(v) for k, v in problems.items()} or "none")
for k, v in problems.items():
    print(k, v[:5])
