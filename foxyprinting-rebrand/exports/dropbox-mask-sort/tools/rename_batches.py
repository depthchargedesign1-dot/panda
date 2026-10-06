"""Split phase3/rename-entries.json into move batches (<=500) using folder file ids for short destinations.
Writes phase3/batches/bNN.json. Only plain moves inside the same folder (renames); autorename stays false."""
import json, glob, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ents = []
for f in sorted(glob.glob(f"{D}/phase3/list/all-p*.json")): ents += json.load(open(f))["entries"]
fid = {e["path"].split("//", 1)[1].lower(): e["file_id"] for e in ents if e["object_type"] == "folder"}
R = json.load(open(f"{D}/phase3/rename-entries.json"))
os.makedirs(f"{D}/phase3/batches", exist_ok=True)
out = []
for r in R:
    folder, new = os.path.split(r["new"])
    out.append({"source_path": r["source_path"], "destination_path": fid[folder.lower()] + "/" + new})
for i in range(0, len(out), 500):
    json.dump(out[i:i + 500], open(f"{D}/phase3/batches/b{i // 500 + 1:02d}.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "entries in", (len(out) + 499) // 500, "batches")
