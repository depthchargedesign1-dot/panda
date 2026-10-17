"""MH/JB rule (owner): any image with MH or JB is a separate image and must be kept.
Finds plan rows (duplicate_exact / duplicate_smaller / check) that are only "duplicates" because an
MH/JB-marked file was compared with an unmarked one (or JB vs MH), and plans moving them as variants.
Uses the post-phase-2 recursive listing (phase2/post) for current folder contents.
Writes mhjb-plan.csv and phase2/mhjb-entries.json."""
import csv, glob, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__)); import norm
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = "/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/"
RENAMED = {"2026 COMEDIANS 2019": "2026 COMEDIANS", "2026 CELEBRITY KIDS CARTOON": "2026 CARTOON, GAME AND FILM CHARACTERS",
           "WAG MODEL": "2026 WAGS AND MODELS", "2026 SPORTS STARS/RUGBY 2019": "2026 SPORTS STARS/Rugby"}
NEW = ("2026 BUSINESS AND PUBLIC FIGURES", "2026 YOUTUBERS", "2026 NOVELTY", "2026 SPORTS STARS/Snooker",
       "2026 SPORTS STARS/Wrestling", "2026 SPORTS STARS/Motorbike Racing")
TOK = re.compile(r"(?<![A-Za-z])(MH|JB)(?![A-Za-z])", re.I)
import ast
_bp = ast.parse(open(os.path.join(os.path.dirname(__file__), "build_plan.py")).read())
_names = {"TV": "2026 TV SHOWS AND STARS", "SPORTS": "2026 SPORTS STARS"}
CAT = {}
for n in _bp.body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in ("DEST", "SPORT_DEST"):
        for k, v in zip(n.value.keys, n.value.values):
            CAT[k.value] = v.value if isinstance(v, ast.Constant) else (_names[v.id] if isinstance(v, ast.Name) else _names[v.left.id] + v.right.value)
def marks(name): return frozenset(m.upper() for m in TOK.findall(os.path.splitext(name)[0]))
def rel(p): return p[len(TOP):] if p.lower().startswith(TOP.lower()) else p
def fix(folder):
    for o, n in RENAMED.items():
        if folder == o or folder.startswith(o + "/"): return n + folder[len(o):]
    return folder
ents = []
for f in sorted(glob.glob(f"{D}/phase2/post/p*.json")): ents += json.load(open(f))["entries"]
files = [e for e in ents if e["object_type"] == "file"]
folders = {e["path"].split("//", 1)[1].lower(): e for e in ents if e["object_type"] == "folder"}
cur = {e["path"].split("//", 1)[1].lower(): e for e in files}
byfolder = collections.defaultdict(list)
for e in files:
    t = e["path"].split("//", 1)[1]; byfolder[os.path.dirname(t).lower()].append(e)
rows, out = [], []
for r in csv.DictReader(open(f"{D}/plan.csv")):
    if r["action"] not in ("duplicate_exact", "duplicate_smaller", "check"): continue
    src = rel(r["source_path"]); e = cur.get(src.lower())
    if not e: continue                                   # no longer where the plan saw it
    other = os.path.basename(r["match_path"]) if r["match_path"] else ""
    ms, mo = marks(r["file_name"]), marks(other)
    if ms == mo: continue                                # not an MH/JB difference
    folder = fix(os.path.dirname(rel(r["match_path"] or r["destination_path"])))
    if folder == "" or folder.startswith("!!!!!!! TO SORT"):     # match is unsorted too: use the plan's category folder
        folder = fix(os.path.dirname(rel(r["destination_path"]))) if r["destination_path"] else fix(CAT.get(r["category"].split(" | ")[0].split("/")[-1], ""))
    p = norm.parse(r["file_name"])
    row = dict(source=src, size=r["size"], plan_action=r["action"], match=rel(r["match_path"]), source_marks=" ".join(sorted(ms)),
               match_marks=" ".join(sorted(mo)), folder=folder, destination="", decision="", note="")
    if folder.startswith(NEW) or folder.lower() not in folders:
        row.update(decision="not moved", note="folder not created (owner's choice) / not found"); rows.append(row); continue
    same = [x for x in byfolder[folder.lower()] if (lambda q: q["base_key"] == p["base_key"] and q["version"] == p["version"])(norm.parse(x["name"])) and marks(x["name"]) == ms]
    if same:
        row.update(decision="not moved", note="folder already has same name+number+marker: " + same[0]["name"]); rows.append(row); continue
    if any(x["name"].lower() == r["file_name"].lower() for x in byfolder[folder.lower()]):
        row.update(decision="not moved", note="name already used in folder"); rows.append(row); continue
    row.update(decision="move as variant", destination=folder + "/" + r["file_name"])
    rows.append(row); out.append(dict(source_path=e["file_id"], fid=folders[folder.lower()]["file_id"], name=r["file_name"], row=row))
# two unsorted files heading to the same folder with same name+number+marker: leave both (check)
g = collections.Counter((o["row"]["folder"].lower(), norm.parse(o["name"])["base_key"], norm.parse(o["name"])["version"], marks(o["name"])) for o in out)
keep = []
for o in out:
    k = (o["row"]["folder"].lower(), norm.parse(o["name"])["base_key"], norm.parse(o["name"])["version"], marks(o["name"]))
    if g[k] > 1: o["row"].update(decision="not moved", destination="", note="another unsorted file has the same name+number+marker (check)")
    else: keep.append(o)
with open(f"{D}/mhjb-plan.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump([dict(source_path=o["source_path"], destination_path=f'{o["fid"]}/{o["name"]}', src_display=TOP + o["row"]["source"],
                dest_display=TOP + o["row"]["destination"]) for o in keep], open(f"{D}/phase2/mhjb-entries.json", "w"), indent=0)
print(collections.Counter(r["decision"] for r in rows), collections.Counter(r["note"].split(":")[0] for r in rows if r["note"]))
