"""usage: check_job.py <batch e.g. a01> [result file]  -- compare a completed move job result with phase3/b250/<batch>.json.
Saves the result as phase3/results/<batch>.json. Prints counts and every failure / mismatch."""
import json, sys, glob, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = sys.argv[1]
src = sys.argv[2] if len(sys.argv) > 2 else max(glob.glob("/root/.claude/projects/-home-user-panda/*/tool-results/mcp-Dropbox-check_job_status-*.txt"), key=os.path.getmtime)
res = json.load(open(src))
os.makedirs(f"{D}/phase3/results", exist_ok=True)
json.dump(res, open(f"{D}/phase3/results/{b}.json", "w"))
batch = json.load(open(f"{D}/phase3/b250/{b}.json"))
ents = res["move_result"]["entries"]
print("result entries", len(ents), "batch", len(batch))
ok = bad = 0
for i, (r, x) in enumerate(zip(ents, batch)):
    if r["entry_status"] == "success":
        o = r["object"]
        if o["file_id"] == x["id"] and o["name"] == x["destination_path"].rsplit("/", 1)[1]: ok += 1
        else: bad += 1; print("MISMATCH", i, x, o.get("file_id"), o.get("name"))
    else:
        bad += 1; print("FAIL", i, x, r["failure"])
print(b, "ok", ok, "not ok", bad)
