"""Phase 1 (read-only) move plan for the celebrity face mask folders in Dropbox.

Inputs : inventory.csv (built from raw/root-pNN.json, a recursive list_folder of the
         "2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES" namespace),
         ../face-masks/dropbox-masks-master-list.csv (person + category identified on 2 Oct 2026),
         tools/overrides.py (manual decisions for names the master list misses or gets wrong).
Outputs: plan.csv, summary.md (proposed-folders.md is written by hand).

Owner's rules applied here:
- nothing is deleted or overwritten; duplicates are left where they are and flagged;
- a number in the name ("Name 2", "Name2") is ALWAYS a different image: kept and moved;
- duplicates only when the base name AND the number match; "(2)", "- Copy" and years such as
  "2021" are not version numbers, so those matches are listed as "check";
- when two files share name + number but differ in size, the larger is the main file and
  the smaller is flagged.
"""
import csv, collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from norm import parse, master_key_candidates, strip_accents, IMG
from overrides import OVERRIDE, KEY_CAT, SENSITIVE

ROOT_DISPLAY = "/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES"
TS = "!!!!!!! TO SORT 2026 JAMIE MIXED UPLOADED TO FOXY SORT INTO FOLDERS"

# ---------------------------------------------------------------- destinations
TV = "2026 TV SHOWS AND STARS"
SPORTS = "2026 SPORTS STARS"
NEW = set()  # folders the plan proposes to create

DEST = {
    "tv": TV, "reality": TV, "film": "2026 MOVIE STARS", "music": "2026 MUSIC",
    "football": "2026 FOOTBALLERS", "comedy": "2026 COMEDIANS 2019",
    "politics": "2026 ROYALS AND POLITICIANS", "royal": "2026 ROYALS AND POLITICIANS",
    "models": "WAG MODEL", "bollywood": "2026 BOLLYWOOD ACTORS",
    "kids": "2026 CELEBRITY KIDS CARTOON", "pack": "!!MASK PACK MOCKUP IMAGES",
    "business": "2026 BUSINESS AND PUBLIC FIGURES", "online": "2026 YOUTUBERS AND INFLUENCERS",
    "novelty": "2026 NOVELTY, ANIMALS AND EMOJIS",
}
SPORT_DEST = {
    "darts": "2026 DARTS", "cricket": "2026 CRICKET", "boxing": "2026 BOXERS", "f1": "2026 F1 DRIVER",
    "athletics": "2026 ATHLETES", "olympic": SPORTS + "/Olympic Athletes", "golf": SPORTS + "/Golf",
    "tennis": SPORTS + "/Tennis", "rugby": SPORTS + "/RUGBY 2019", "cycling": SPORTS + "/Cycling",
    "basketball": SPORTS + "/Basketball", "mma": SPORTS + "/MMA", "snooker": SPORTS + "/Snooker",
    "wrestling": SPORTS + "/Wrestling", "motorbike": SPORTS + "/Motorbike Racing",
    "other": SPORTS + "/Misc Sports", "nfl": SPORTS + "/Misc Sports", "": SPORTS + "/Misc Sports",
}
SHOW_SUB = {  # show (as in the master list) -> existing subfolder of 2026 TV SHOWS AND STARS
    "coronation street": "2026 CORONATION STREET", "eastenders": "2026 Eastenders", "emmerdale": "2026 Emmerdale",
    "benidorm": "2026 BENIDORM", "hollyoaks": "Hollyoaks", "friends": "Friends", "gavin & stacey": "GAVIN STACEY",
    "gavin and stacey": "GAVIN STACEY", "geordie shore": "GEORDIE SHORE", "love island": "LOVE ISLAND",
    "the only way is essex": "TOWIE", "strictly come dancing": "Strictly Come Dancing",
    "stranger things": "STRANGER THINGS", "the chase": "The Chase", "the voice": "The Voice", "the voice uk": "The Voice",
    "rupaul's drag race": "Ru Pauls Drag Race", "still game": "still game", "squid game": "Squid Game",
    "money heist": "Money Heist", "the boys": "The Boys Tv", "gangs of london": "Gangs of London",
    "the office (us)": "The office- American", "i'm a celebrity... get me out of here!": "IM A CELEB",
    "i'm a celebrity": "IM A CELEB", "ink master": "Ink Master",
}
FILM_SUB = {"harry potter": "Harry Potter", "mamma mia!": "Mamma Mia", "mamma mia": "Mamma Mia", "saw": "Saw",
            "spider-man": "Spider man", "the a-team": "A TEAM"}

EXISTING_SETS = ("2026 ", "WAG MODEL")          # folders that make up the "final" set
HOLDING = ("2026 ! DUPLICATES TO CHECK", "!!!!!!!!!!!MASKS NOT YET CUT 2026")


def top(path):
    return path.split("/", 1)[0] if "/" in path else ""


def in_final(path):
    t = top(path)
    return bool(t) and (t.startswith("2026 ") or t == "WAG MODEL" or t == "!!MASK PACK MOCKUP IMAGES") and t not in HOLDING


def load():
    inv = list(csv.DictReader(open(os.path.join(OUT, "inventory.csv"), encoding="utf-8")))
    M = list(csv.DictReader(open(os.path.join(OUT, "..", "face-masks", "dropbox-masks-master-list.csv"), encoding="utf-8")))
    return inv, M


def classify(name, master, byname):
    p = parse(name)
    key = p["base_key"]
    ov = OVERRIDE.get(key + p["qual_key"]) or OVERRIDE.get(key)
    if ov:
        return dict(person=ov[0], cat=ov[1], sport=ov[2] if len(ov) > 2 else "", show=ov[3] if len(ov) > 3 else "",
                     how="manual", known="")
    hit = next((k for k in master_key_candidates(name) if k in master), None)
    m = master.get(hit) if hit else byname.get(key)
    if not m:
        return None
    cat, sport, show = m["category"], m["sport"], m["show"]
    blurb = (m["known_as"] + " " + m["blurb"]).lower()
    if cat in ("film", "tv", "music") and ("bollywood" in blurb or re.search(r"\bindian (?:film |tv )?(actor|actress)", blurb)):
        cat = "bollywood"
    kc = KEY_CAT.get(hit) or KEY_CAT.get(key)
    if kc:
        cat = kc[0]; sport = kc[1] if len(kc) > 1 else sport
    if cat == "sport" and sport == "other":
        sport = KEY_CAT.get(("sport", hit), sport)
    return dict(person=m["name"], cat=cat, sport=sport, show=show, how="master-list", known=m["known_as"])


def destination(c):
    cat, sport, show = c["cat"], c["sport"], (c["show"] or "").strip().lower()
    if cat == "sport":
        d = SPORT_DEST.get(sport, SPORTS + "/Misc Sports")
    elif cat == "characters":
        d = DEST["kids"]
        if show in FILM_SUB:
            d = "2026 MOVIE STARS/" + FILM_SUB[show]
    elif cat in ("tv", "reality") and show in SHOW_SUB:
        d = TV + "/" + SHOW_SUB[show]
    elif cat == "tv" and show.startswith("the real housewives"):
        d = TV + "/Real Housewives"
    elif cat == "reality" and show.startswith("the real housewives"):
        d = TV + "/Real Housewives"
    elif cat == "film" and show in FILM_SUB:
        d = "2026 MOVIE STARS/" + FILM_SUB[show]
    elif cat in DEST:
        d = DEST[cat]
    else:
        d = None
    return d


def main():
    inv, M = load()
    master = {r["key"]: r for r in M}
    byname = {}
    for r in M:
        byname.setdefault(re.sub("[^a-z0-9]", "", strip_accents(r["name"]).lower()), r)
    files = [r for r in inv if r["type"] == "file"]
    folders = {r["path"].lower() for r in inv if r["type"] == "folder"}

    # index of the final 2026 set by (base_key, version)
    final_idx = collections.defaultdict(list)
    other_idx = collections.defaultdict(list)     # JB / holding folders, for information
    occupied = collections.defaultdict(set)       # folder(lower) -> names(lower)
    for r in files:
        folder = r["path"].rsplit("/", 1)[0] if "/" in r["path"] else ""
        occupied[folder.lower()].add(r["name"].lower())
        if "/" not in r["path"] or r["path"].startswith(TS + "/"):
            continue
        p = parse(r["name"])
        if not p["base_key"]:
            continue
        (final_idx if in_final(r["path"]) else other_idx)[(p["base_key"], p["version"])].append((r, p))

    sources = [r for r in files if r["path"].startswith(TS + "/") or "/" not in r["path"]]
    rows = []
    # group sources by name+number so that copies inside the source set are handled together
    groups = collections.defaultdict(list)
    for r in sources:
        p = parse(r["name"])
        groups[(p["base_key"], p["version"])].append((r, p))

    for (key, ver), items in groups.items():
        # largest first: it becomes the main file within the source set
        items.sort(key=lambda t: -(int(t[0]["size"] or 0)))
        primary = None
        for r, p in items:
            size = int(r["size"] or 0)
            origin = "TO SORT" if r["path"].startswith(TS + "/") else "root (loose)"
            row = dict(source_path=ROOT_DISPLAY + "/" + r["path"], origin=origin, file_name=r["name"], size=size,
                       person="", category="", destination_path="", action="", reason="", match_path="", match_size="")
            ext = p["ext"]
            if ext not in IMG or not key:
                row.update(action="leave", reason="not a face image (%s); leave where it is" % (ext or "no extension"))
                rows.append(row); continue
            c = classify(r["name"], master, byname)
            if not c:
                row.update(action="unsure", reason="person not identified from the file name")
                rows.append(row); continue
            row["person"] = c["person"]
            if c["cat"] == "unsure":
                if c["person"] in SENSITIVE or key in SENSITIVE or c["how"] == "master-list" and c["known"] and any(
                        w in c["known"].lower() for w in ("criminal", "murderer", "gangster", "terror", "offender", "māori")):
                    why = "SENSITIVE (%s): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv" % (c["known"] or c["person"])
                elif c["how"] == "manual":
                    why = c.get("show") or "not identified"
                else:
                    why = "name too vague to identify (bare first name or unidentified: '%s'); may be a customer's personalised mask, open the image to check" % (c["known"] or c["person"])
                row.update(category="unsure", action="unsure", reason=why)
                rows.append(row); continue
            if c["cat"] == "leave":
                row.update(category="not a mask", action="leave", reason=c.get("show") or "not a face mask image")
                rows.append(row); continue
            dest = destination(c)
            if not dest:
                row.update(action="unsure", reason="no category for '%s'" % c["cat"])
                rows.append(row); continue
            row["category"] = c["cat"] + ("/" + c["sport"] if c["sport"] else "") + (" | " + c["show"] if c["show"] else "")
            if dest.split("/")[0].lower() not in folders and dest.lower() not in folders:
                NEW.add(dest.split("/")[0])
            if dest.lower() not in folders:
                NEW.add(dest)
            notes = []
            if c["person"] in SENSITIVE or key in SENSITIVE:
                notes.append("SENSITIVE: owner to decide if this mask is still wanted (see removed-sensitive-masks.csv)")
            if p["version"]:
                notes.append("version %s = a different image of %s (owner's rule: keep every version)" % (p["version"], c["person"]))

            # ---- duplicate checks
            action = "move"
            exact_name = lambda q: (q["copy_marker"] == "" and q["year"] == "")
            matches = final_idx.get((key, ver), [])
            if primary is not None:
                matches = matches + [primary]
            if matches:
                best = max(matches, key=lambda t: int(t[0]["size"] or 0))
                bsize = int(best[0]["size"] or 0)
                row["match_path"] = ROOT_DISPLAY + "/" + best[0]["path"]
                row["match_size"] = bsize
                markers = (p["copy_marker"] or p["year"]) or (best[1]["copy_marker"] or best[1]["year"])
                same_size = any(int(m[0]["size"] or 0) == size for m in matches)
                if markers:
                    action = "check"
                    notes.append("same name + number as %s, but one name carries a copy marker/year (%s); not counted as a duplicate"
                                 % (best[0]["name"], ",".join(x for x in [p["copy_marker"], p["year"], best[1]["copy_marker"], best[1]["year"]] if x)))
                    if same_size:
                        notes.append("sizes are identical (%d bytes), so it is very likely the same file" % size)
                    elif size > bsize:
                        notes.append("this file is LARGER (%d vs %d bytes)" % (size, bsize))
                    else:
                        notes.append("this file is smaller (%d vs %d bytes)" % (size, bsize))
                elif same_size:
                    action = "duplicate_exact"
                    twin = next(m for m in matches if int(m[0]["size"] or 0) == size)
                    row["match_path"] = ROOT_DISPLAY + "/" + twin[0]["path"]; row["match_size"] = size
                    notes.append("same name + number and same size (%d bytes) as %s; leave in place, do not move" % (size, twin[0]["path"]))
                elif size < bsize:
                    action = "duplicate_smaller"
                    notes.append("same name + number as %s, which is larger (%d vs %d bytes); keep that one as main, flag this one" % (best[0]["name"], bsize, size))
                else:
                    action = "duplicate_larger"
                    notes.append("same name + number as %s but THIS file is larger (%d vs %d bytes): move it in as the main file and flag the smaller one; never overwrite"
                                 % (best[0]["name"], size, bsize))
            else:
                # different number of the same person already in the final set?
                vers = sorted({k[1] or "main" for k in final_idx if k[0] == key})
                if vers:
                    action = "variant"
                    notes.append("same person already in the 2026 folders as version(s) %s; this is a different number, so keep both" % ", ".join(vers))
            info = other_idx.get((key, ver))
            if info:
                notes.append("also in %s" % "; ".join(sorted({x[0]["path"].rsplit("/", 1)[0] for x in info}))[:200])

            # ---- destination name collision check (case-insensitive, existing files + planned moves)
            dname = r["name"]
            if action in ("move", "variant", "duplicate_larger", "check"):
                taken = occupied[dest.lower()]
                if dname.lower() in taken:
                    stem, e = os.path.splitext(dname)
                    if action == "duplicate_larger":
                        dname = "%s (larger)%s" % (stem, e)
                        notes.append("the smaller file with this name stays put; this larger copy goes in beside it as '(larger)' so nothing is overwritten")
                    else:
                        n = 2
                        while ("%s (%d)%s" % (stem, n, e)).lower() in taken:
                            n += 1
                        dname = "%s (%d)%s" % (stem, n, e)
                        notes.append("name already used in the destination by a different file (different size); renamed to avoid overwriting")
                taken.add(dname.lower())
                row["destination_path"] = ROOT_DISPLAY + "/" + dest + "/" + dname
            else:
                row["destination_path"] = ""
            row["action"] = action
            row["reason"] = "; ".join([("identified via " + c["how"]) + (" (" + c["known"] + ")" if c["known"] else "")] + notes)
            rows.append(row)
            if primary is None:
                primary = (r, p)

    rows.sort(key=lambda x: (x["origin"], x["destination_path"] or "~", x["file_name"].lower()))
    cols = ["source_path", "origin", "file_name", "size", "person", "category", "destination_path", "action", "reason", "match_path", "match_size"]
    with open(os.path.join(OUT, "plan.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    return rows, folders


if __name__ == "__main__":
    rows, folders = main()
    c = collections.Counter(r["action"] for r in rows)
    print(len(rows), c)
    print("new folders:", sorted(NEW))
