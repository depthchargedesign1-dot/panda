"""Rebuild moves-log.csv / move-conflicts.csv from phase2/entries.json and every phase2/job*.json + result0.json.
A file counts as moved when a successful move result carries its file id."""
import csv, glob, json, os, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ents = json.load(open(f"{D}/phase2/entries.json"))
moved = {}
fails = []
for f in sorted(glob.glob(f"{D}/phase2/job*.json")) + [f"{D}/phase2/result0.json"]:
    for r in json.load(open(f))["move_result"]["entries"]:
        if r["entry_status"] == "success":
            o = r["object"]
            if o.get("file_id"):
                moved[o["file_id"]] = o.get("path_display", "")
        else:
            fails.append((os.path.basename(f), r))
# result0 (test batch) had no ids recorded; its three sources are known
for sid, p in [("id:nVgixzQZKNAAAAAAAABX6g", "!!MASK PACK MOCKUP IMAGES/Tenacious D Mask Pack.jpg"),
               ("id:Ac8E0IpXMi8AAAAAAAAT-A", "2026 SPORTS STARS/Olympic Athletes/Yohan Blake (larger).JPG"),
               ("id:nVgixzQZKNAAAAAAAABcfA", "2026 BOLLYWOOD ACTORS/Anushka Sharma-Bollywood.jpg")]:
    moved.setdefault(sid, "/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/" + p)
log = []
for e in ents:
    p = moved.get(e["source_path"])
    log.append(dict(source=e["src_display"], destination=e["dest_display"], action=e["action"],
                    status="moved" if p else "pending", result=p or "", file_id=e["source_path"]))
f = ["source", "destination", "action", "status", "result", "file_id"]
with open(f"{D}/moves-log.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=f); w.writeheader(); w.writerows(log)
json.dump([{"job": a, **b} for a, b in fails], open(f"{D}/phase2/failures.json", "w"), indent=1)
print(collections.Counter(r["status"] for r in log), "failures:", len(fails), "ids moved not in entries:", len(set(moved) - {e['source_path'] for e in ents}))
