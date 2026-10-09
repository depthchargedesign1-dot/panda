#!/usr/bin/env python3
"""Fill renames-log.csv from a fresh recursive listing (phase3/list/<label>-pNN.json), matched by file id.
usage: rename_log.py <label>"""
import csv, glob, json, sys, collections
B = "/home/user/panda/foxyprinting-rebrand/exports/dropbox-mask-sort/"
NS = "ns:1384231538//"
label = sys.argv[1]
cur = {}
tmp = []
for f in sorted(glob.glob(B + f"phase3/list/{label}-p*.json")):
    for e in json.load(open(f))["entries"]:
        if e.get("object_type") != "file": continue
        p = e["path"][len(NS):] if e["path"].startswith(NS) else e["path"]
        cur[e["file_id"]] = p
        if "TMPCASE" in p: tmp.append(p)
rows = list(csv.DictReader(open(B + "rename-plan.csv")))
out, cnt = [], collections.Counter()
for r in rows:
    old = f"{r['folder']}/{r['old']}"; new = f"{r['folder']}/{r['new']}"
    now = cur.get(r["file_id"])
    if now is None: st = "missing from listing"
    elif now == new: st = "renamed"
    elif now == old: st = "not renamed"
    else: st = "other: " + now
    cnt[st.split(":")[0]] += 1
    out.append({"old": old, "new": new, "status": st, "file_id": r["file_id"]})
with open(B + "renames-log.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["old", "new", "status", "file_id"]); w.writeheader(); w.writerows(out)
print(dict(cnt), "files listed:", len(cur), "TMPCASE left:", len(tmp))
for p in tmp[:20]: print("  TMPCASE", p)
for o in out:
    if o["status"] != "renamed": print(" ", o["status"], "|", o["old"], "->", o["new"])
