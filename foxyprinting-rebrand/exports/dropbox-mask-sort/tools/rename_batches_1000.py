"""Owner asked for as few move calls as possible (each needs a click): pack into 1,000-entry batches.
Pass 1 (phase3/b1000/p1-NN): every remaining normal rename + case-only step 1 (-> "<stem> TMPCASE<ext>"); independent.
Pass 2 (phase3/b1000/p2-NN): TMPCASE -> final name (only after pass 1 is confirmed).
Excludes the 2 test renames and a01 lines 1-125 (sent 08:2x). Path-based (mistyped source fails safe)."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{D}/phase3/b250"
sent = json.load(open(f"{B}/a01.json"))[:125]
done = {x["id"] for x in sent}
A, T, F = [], [], []
for n in range(1, 16): A += json.load(open(f"{B}/a{n:02d}.json"))
for n in range(1, 8): T += json.load(open(f"{B}/t{n:02d}.json")); F += json.load(open(f"{B}/f{n:02d}.json"))
P1 = [x for x in A if x["id"] not in done] + T
os.makedirs(f"{D}/phase3/b1000", exist_ok=True)
def write(tag, L):
    for i in range(0, len(L), 1000):
        part = L[i:i + 1000]; name = f"{tag}-{i // 1000 + 1:02d}"
        json.dump(part, open(f"{D}/phase3/b1000/{name}.json", "w"), ensure_ascii=False)
        open(f"{D}/phase3/b1000/{name}.txt", "w").write("\n".join(json.dumps({"source_path": x["source_path"], "destination_path": x["destination_path"]}, ensure_ascii=False) for x in part) + "\n")
write("p1", P1); write("p2", F)
print(len(P1), len(F))
