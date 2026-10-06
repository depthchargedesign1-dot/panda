"""usage: check_sent.py <sent-name e.g. p1-02> <result file> -- compare job result with phase3/sent/<name>.json, save phase3/results/sent-<name>.json"""
import json, sys, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/phase3"
n, src = sys.argv[1], sys.argv[2]
res = json.load(open(src)); json.dump(res, open(f"{D}/results/sent-{n}.json", "w"))
b = json.load(open(f"{D}/sent/{n}.json")); e = res["move_result"]["entries"]
print(res["status"], "result", len(e), "batch", len(b))
ok = 0
for i, (r, x) in enumerate(zip(e, b)):
    if r["entry_status"] == "success" and r["object"]["file_id"] == x["id"] and r["object"]["name"] == x["destination_path"].rsplit("/", 1)[1]: ok += 1
    else: print("PROBLEM", i, r.get("failure") or (r["object"].get("file_id"), r["object"].get("name")), x)
print(n, "ok", ok)
