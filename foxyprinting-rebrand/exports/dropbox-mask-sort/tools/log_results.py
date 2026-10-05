"""Rebuild moves-log.csv and move-conflicts.csv from phase2/batchN.json + phase2/resultN.json."""
import csv, glob, json, os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ents = {e["source_path"] + "|" + e["destination_path"]: e for e in json.load(open(f"{D}/phase2/entries.json"))}
log, conf = [], []
for bf in sorted(glob.glob(f"{D}/phase2/batch*.json"), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0])):
    n = re.findall(r"\d+", os.path.basename(bf))[0]
    rf = f"{D}/phase2/result{n}.json"
    batch = json.load(open(bf))
    res = json.load(open(rf))["move_result"]["entries"] if os.path.exists(rf) else []
    byi = {r["entry_index"]: r for r in res}
    for i, b in enumerate(batch):
        e = ents[b["source_path"] + "|" + b["destination_path"]]
        r = byi.get(i)
        if r is None:
            st, det = "not run", ""
        elif r["entry_status"] == "success":
            st, det = "moved", r["object"].get("path_display", "")
        else:
            st, det = "failed", json.dumps({k: v for k, v in r.items() if k not in ("entry_index",)})[:300]
        row = dict(batch=n, source=e["src_display"], destination=e["dest_display"], action=e["action"], status=st, result=det)
        log.append(row)
        if st == "failed":
            conf.append(row)
f = ["batch", "source", "destination", "action", "status", "result"]
for name, rows in (("moves-log.csv", log), ("move-conflicts.csv", conf)):
    with open(f"{D}/{name}", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=f); w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r["status"] for r in log))
