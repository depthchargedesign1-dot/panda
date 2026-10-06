"""Owner asked for as few move calls as possible (each needs a click): pack into 1,000-entry batches.
Pass 1 (phase3/b1000/p1-NN): every remaining normal rename + case-only step 1 (-> "<stem> TMPCASE<ext>"); independent.
Pass 2 (phase3/b1000/p2-NN): TMPCASE -> final name (only after pass 1 is confirmed).
Excludes the 2 test renames and a01 lines 1-125 (sent 08:2x). Path-based (mistyped source fails safe)."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{D}/phase3/b250"
sent = json.load(open(f"{D}/phase3/sent/a01-250.json"))[:125]
done = {x["id"] for x in sent}
import glob as _g
for f in _g.glob(f"{D}/phase3/sent/p1-*.json"): done |= {x["id"] for x in json.load(open(f))}
A, T, F = [], [], []
for n in range(1, 16): A += json.load(open(f"{B}/a{n:02d}.json"))
for n in range(1, 8): T += json.load(open(f"{B}/t{n:02d}.json")); F += json.load(open(f"{B}/f{n:02d}.json"))
M = "ns:1384231538//2026 MOVIE STARS/"
FIX = [  # names sent in the first 1000 that were wrong; corrected in pass 2 (ids from phase3/sent/p1-01.json)
    {"source_path": M + "Gus Bad.jpg", "destination_path": M + "Gus (Breaking Bad) 2.jpg"},
    {"source_path": M + "Gease (Sandy2).jpg", "destination_path": M + "Sandy (Grease) 2.jpg"},
    {"source_path": M + "Adrian Brody JB.jpg", "destination_path": M + "Adrien Brody JB.jpg"}]
_s1 = {x["destination_path"]: x["id"] for x in json.load(open(f"{D}/phase3/sent/p1-01.json"))}
C = "ns:1384231538//2026 CARTOON, GAME AND FILM CHARACTERS/"
FIX2 = [  # LOTR names already sent (a01 first 125 / sent p1-01); corrected in pass 2 after the 6 Oct review
    {"source_path": C + "Aragorn Lotr.jpg", "destination_path": C + "Aragorn (Lord of the Rings).jpg", "id": "id:nVgixzQZKNAAAAAAAABb_g"},
    {"source_path": C + "Lotr (Gollum).jpg", "destination_path": C + "Gollum (Lord of the Rings).jpg", "id": "id:nVgixzQZKNAAAAAAAAAadg"}]
for x in FIX: x["id"] = _s1[x["source_path"]]
FIX = FIX + FIX2
F = F + FIX
P1 = [x for x in A if x["id"] not in done] + T
os.makedirs(f"{D}/phase3/b1000", exist_ok=True)
def write(tag, L):
    for i in range(0, len(L), 1000):
        part = L[i:i + 1000]; name = f"{tag}-{i // 1000 + 1:02d}"
        json.dump(part, open(f"{D}/phase3/b1000/{name}.json", "w"), ensure_ascii=False)
        open(f"{D}/phase3/b1000/{name}.txt", "w").write("\n".join(json.dumps({"source_path": x["source_path"], "destination_path": x["destination_path"]}, ensure_ascii=False) for x in part) + "\n")
for _f in _g.glob(f"{D}/phase3/b1000/p[12]-*.json"):  # clear stale batches left from earlier, longer runs
    open(_f, "w").write("[]"); open(_f[:-5] + ".txt", "w").write("")
write("p1", P1); write("p2", F)
# NOTE: after p1-01 was sent, batches are renumbered from the remaining entries (sent ones excluded).
print(len(P1), len(F))
