"""Assign every face mask one clean category tag (mask-<category>) plus a sport sub-tag where it applies.

The tidy mask collections are smart collections built on these tags, so the old, inconsistent tags
(TV STARS, FOOTBALLERS, MOVIE ...) no longer decide where a mask appears.
Usage: python3 tools/mask_categories.py <shopify_masks.jsonl> <out.json>
"""
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from mask_copy import category  # title first, then product type, then tags

SPORT_SUBS = {"football", "darts", "golf", "f1", "tennis", "boxing", "cricket", "rugby", "snooker"}
TOP = {  # mask_copy category -> top-level collection tag
    "football": "mask-footballers", "darts": "mask-sport", "golf": "mask-sport", "f1": "mask-sport", "tennis": "mask-sport",
    "boxing": "mask-sport", "cricket": "mask-sport", "rugby": "mask-sport", "snooker": "mask-sport", "sport": "mask-sport",
    "royal": "mask-politicians-royals", "music": "mask-music", "comedy": "mask-comedians", "reality": "mask-reality-tv",
    "film": "mask-film-stars", "tv": "mask-tv-stars", "celeb": "mask-tv-stars",
}


def tags_for(p):
    t = p["title"]
    tags = ["celebrity-face-mask"]
    if re.search(r"personalised|custom photo|your own|request a", t, re.I):
        return ["personalised-face-mask"]
    if re.search(r"\b\d+\s*(x|pack)\b|\bpack\b|couple", t, re.I):
        tags.append("mask-packs-couples")
    if re.search(r"\b(minions?|santa|miss piggy|muppet|elf|grinch|pyro\w*|kids?)\b", t, re.I):
        tags.append("mask-characters")
    if re.search(r"stag|hen\b", " ".join(p.get("tags", [])), re.I):
        tags.append("mask-stag-hen")
    key = category(p)[0]
    tags.append(TOP[key] if key in TOP else "mask-tv-stars")
    if key in SPORT_SUBS and key != "football":
        tags.append(f"mask-{key}")
    return tags


def main(src, out):
    res, counts = {}, {}
    for line in open(src):
        p = json.loads(line)
        if "__parentId" in p or re.search(r"face covering", p["title"], re.I):
            continue
        tg = tags_for(p)
        res[p["id"]] = tg
        for t in tg:
            counts[t] = counts.get(t, 0) + 1
    json.dump(res, open(out, "w"))
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{v:6d}  {k}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
