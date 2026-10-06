"""Pack the last calls (owner wants as few move calls as possible).
q1 = remaining pass-1 entries (b1000/p1-03) + pass-2 entries whose step 1 was in an EARLIER call (or fixes), up to 1000.
q2 = pass-2 entries whose step 1 is in q1 (must run after q1 completes) + any overflow.
Writes phase3/b1000/q1.json/.txt and q2.json/.txt."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/phase3/b1000"
last = json.load(open(f"{D}/p1-03.json"))
p2 = json.load(open(f"{D}/p2-01.json")) + json.load(open(f"{D}/p2-02.json"))
later = {x["destination_path"] for x in last}          # TMPCASE names created by q1 itself
early = [x for x in p2 if x["source_path"] not in later]
dep = [x for x in p2 if x["source_path"] in later]
room = 1000 - len(last)
q1 = last + early[:room]; q2 = early[room:] + dep
assert len(q1) <= 1000 and len(q2) <= 1000 and len(q1) + len(q2) == len(last) + len(p2)
for n, L in (("q1", q1), ("q2", q2)):
    json.dump(L, open(f"{D}/{n}.json", "w"), ensure_ascii=False)
    open(f"{D}/{n}.txt", "w").write("\n".join(json.dumps({"source_path": x["source_path"], "destination_path": x["destination_path"]}, ensure_ascii=False) for x in L) + "\n")
print("q1", len(q1), "(pass1", len(last), "+ pass2", len(q1) - len(last), ")  q2", len(q2), "(dependent on q1:", len(dep), ")")
