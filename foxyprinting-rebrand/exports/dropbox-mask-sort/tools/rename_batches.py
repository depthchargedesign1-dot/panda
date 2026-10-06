"""Paths (not ids) are used so a mistyped source fails as not_found instead of touching another file.
Split phase3/rename-entries.json into move batches (<=500), folder-id destinations, autorename false.
Dropbox rejects a case-only rename (to/conflict), so those go in two passes through a temporary name:
  phase3/b250/aNN.json  normal renames
  phase3/b250/tNN.json  case-only step 1: -> "<new stem> TMPCASE<ext>"
  phase3/b250/fNN.json  case-only step 2: TMPCASE -> final name
DONE ids (already renamed in the 08:05 test) are left out."""
import json, glob, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONE = {"id:Ac8E0IpXMi8AAAAAAAAUng", "id:Ac8E0IpXMi8AAAAAAAAbBQ"}
ents = []
for f in sorted(glob.glob(f"{D}/phase3/list/all-p*.json")): ents += json.load(open(f))["entries"]
fid = {e["path"].split("//", 1)[1].lower(): e["file_id"] for e in ents if e["object_type"] == "folder"}
names = {e["name"].lower() for e in ents}
R = json.load(open(f"{D}/phase3/rename-entries.json"))
os.makedirs(f"{D}/phase3/b250", exist_ok=True)
A, T, F = [], [], []
for r in R:
    if r["source_path"] in DONE: continue
    folder, new = os.path.split(r["new"])
    NS = "ns:1384231538//"
    dest = NS + folder + "/"
    srcp = NS + r["old"]
    if os.path.basename(r["old"]).lower() == new.lower():
        stem, ext = os.path.splitext(new); tmp = f"{stem} TMPCASE{ext}"
        assert tmp.lower() not in names
        T.append({"source_path": srcp, "destination_path": dest + tmp, "id": r["source_path"]})
        F.append({"source_path": dest + tmp, "destination_path": dest + new, "id": r["source_path"]})
    else:
        A.append({"source_path": srcp, "destination_path": dest + new, "id": r["source_path"]})
for tag, L in (("a", A), ("t", T), ("f", F)):
    for i in range(0, len(L), 250):
        json.dump(L[i:i + 250], open(f"{D}/phase3/b250/{tag}{i // 250 + 1:02d}.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(A), len(T), len(F))
