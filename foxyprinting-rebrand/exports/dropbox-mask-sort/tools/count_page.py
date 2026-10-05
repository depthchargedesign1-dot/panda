"""Append the newest list_folder tool result to missed/<label>.jsonl (compact: path,size) and print totals + cursor."""
import json, glob, os, sys
label = sys.argv[1]
d = "/home/user/panda/foxyprinting-rebrand/exports/dropbox-mask-sort/missed-raw"; os.makedirs(d, exist_ok=True)
f = max(glob.glob("/root/.claude/projects/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/tool-results/mcp-Dropbox-list_folder-*.txt"), key=os.path.getmtime)
data = json.load(open(f))
with open(f"{d}/{label}.jsonl", "a") as out:
    for e in data["entries"]:
        out.write(json.dumps({"t": e["object_type"][0], "p": e.get("path_display") or e["path"], "s": e.get("file", {}).get("size")}) + "\n")
rows = [json.loads(l) for l in open(f"{d}/{label}.jsonl")]
print(label, "files:", sum(r["t"] == "f" for r in rows), "folders:", sum(r["t"] == "f" and 0 or r["t"] != "f" for r in rows), "more:", data["has_more"])
if data["has_more"]: print(data["cursor"])
