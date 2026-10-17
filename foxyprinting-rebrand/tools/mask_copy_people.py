"""Rebuild face mask copy using the person identification (exports/face-masks/dropbox-masks-master-list.csv).

Listings matched to an identified person get that person's own intro, category and show; the rest fall back
to the title-based copy. Writes import CSVs plus category tags. Sensitive and low-confidence matches are skipped.
Usage: python3 tools/mask_copy_people.py <shopify_masks.jsonl> <who_dir> <out_dir>
"""
import csv
import glob
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import mask_copy as M  # noqa: E402

TAG = {"football": "mask-footballers", "sport": "mask-sport", "tv": "mask-tv-stars", "film": "mask-film-stars",
       "music": "mask-music", "comedy": "mask-comedians", "reality": "mask-reality-tv", "royal": "mask-politicians-royals",
       "politics": "mask-politicians-royals", "characters": "mask-characters", "models": "mask-tv-stars", "other": "mask-tv-stars"}


def main(src, who_dir, out):
    who = {}
    for f in glob.glob(f"{who_dir}/out*.jsonl"):
        for line in open(f):
            try:
                o = json.loads(line)
                who[o["key"]] = o
            except Exception:
                pass
    master = list(csv.DictReader(open(f"{out}/dropbox-masks-master-list.csv", encoding="utf-8")))
    by_handle = {}
    rank = {"high": 0, "medium": 1, "low": 2}
    for r in master:
        if r["sensitive"] == "True" or r["confidence"] == "low" or not r["foxy_handles"]:
            continue
        for h in r["foxy_handles"].split():
            cur = by_handle.get(h)
            if cur is None or rank[r["confidence"]] < rank[cur["confidence"]]:
                by_handle[h] = r
    P = {}
    for line in open(src):
        o = json.loads(line)
        if "__parentId" not in o:
            P[o["id"]] = o
    rows, tags, matched = [], {}, 0
    for p in P.values():
        if p["status"] != "ACTIVE" or re.search(r"face covering", p["title"], re.I):
            continue
        r = by_handle.get(p["handle"])
        ident = None
        if r:
            o = who.get(r["key"], {})
            name = r["name"]
            if r["character"] and r["character"].lower() in p["title"].lower():
                name = r["character"]
            ident = dict(name=name, show=r["show"] or None, category=r["category"], sport=r["sport"] or None, blurb=o.get("blurb") or r["blurb"])
            matched += 1
            t = ["celebrity-face-mask", TAG.get(r["category"], "mask-tv-stars")]
            if r["category"] == "sport" and r["sport"] in M.SPORT_CAT:
                t.append("mask-" + r["sport"])
            tags[p["id"]] = t
        b = M.build(p, ident)
        if b:
            rows.append((p, b, bool(ident)))
    single = [x for x in rows if x[0].get("totalVariants", 1) == 1]
    cols = ["Handle", "Body (HTML)", "SEO Title", "SEO Description"]
    for n, i in enumerate(range(0, len(single), 3500)):
        with open(f"{out}/masks-{n + 1:02d}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(cols)
            for p, b, _ in single[i:i + 3500]:
                w.writerow([p["handle"], b["body"], b["seo_title"], b["meta"]])
    with open(f"{out}/masks-00-TEST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cols)
        for p, b, _ in [x for x in single if x[2]][:3]:
            w.writerow([p["handle"], b["body"], b["seo_title"], b["meta"]])
    json.dump(tags, open(f"{out}/masks-category-tags.json", "w"))
    print(f"listings written {len(rows)} (person-specific {sum(1 for x in rows if x[2])}), csv rows {len(single)}, tag updates {len(tags)}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
