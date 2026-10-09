"""Write summary.md from plan.csv and inventory.csv (phase 1, read-only)."""
import csv, collections, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = "/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/"
rows = list(csv.DictReader(open(os.path.join(OUT, "plan.csv"), encoding="utf-8")))
inv = list(csv.DictReader(open(os.path.join(OUT, "inventory.csv"), encoding="utf-8")))
folders = {r["path"].lower() for r in inv if r["type"] == "folder"}


def dest_folder(x):
    return x["destination_path"][len(ROOT):].rsplit("/", 1)[0] if x["destination_path"] else ""


ts = [x for x in rows if x["origin"] == "TO SORT"]
lo = [x for x in rows if x["origin"] != "TO SORT"]
A = ["move", "variant", "check", "duplicate_larger", "duplicate_exact", "duplicate_smaller", "unsure", "leave"]

L = []
w = L.append
w("# Celebrity face mask folders: phase 1 move plan (read-only)")
w("")
w("Made on 5 Oct 2026 from a full read-only listing of `/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES` "
  "(13,054 entries: 12,875 files, 179 folders). **Nothing in Dropbox has been moved, copied, renamed, created or deleted.**")
w("")
w("Files: `plan.csv` (one row per source file), `proposed-folders.md`, `missed-candidates.md`, `inventory.csv` "
  "(every file and folder in the set, with size and dates), `raw-listings.tar.gz` (the raw Dropbox listings), `tools/` (the scripts).")
w("")
w("## Totals")
w("")
w("| | TO SORT folder | Loose images in the root | Total |")
w("|---|---:|---:|---:|")
w("| Files looked at | %d | %d | %d |" % (len(ts), len(lo), len(rows)))
for a in A:
    w("| `%s` | %d | %d | %d |" % (a, sum(x["action"] == a for x in ts), sum(x["action"] == a for x in lo), sum(x["action"] == a for x in rows)))
w("")
w("The TO SORT folder holds 951 files at the top level plus 20 in its `Rappers` subfolder (971 in all).")
w("")
w("### What the actions mean")
w("")
w("- **move**: a new person (or a new numbered version) for the clean set. Move to `destination_path`.")
w("- **variant**: the person is already in the 2026 folders, but this file has a different number (\"Name 2\", \"Name3\"). "
  "Owner's rule: a number always means a different image, so keep both and move it.")
w("- **check**: same name and number as a file already in the 2026 folders, but one of the two names carries a Dropbox/Windows copy "
  "marker such as `(2)`, `- Copy` or a year such as `2021`. Those are not version numbers, so this is **not** counted as a duplicate. "
  "The reason column gives both sizes (and says when they are byte-identical). Owner to look before anything moves.")
w("- **duplicate_larger**: same name and number as an existing file, and this file is **larger**. Plan: move it in beside the old one "
  "as `<name> (larger).jpg` (never overwrite), then the owner retires the smaller one.")
w("- **duplicate_exact**: same name and number and the same size in bytes as a file already in the set. Leave it where it is.")
w("- **duplicate_smaller**: same name and number, but the copy already in the set is larger. Leave this one where it is; flagged so nothing "
  "replaces the better file.")
w("- **unsure**: person or category not clear from the file name (bare first names, random camera/agency names) or a sensitive subject. Not moved.")
w("- **leave**: not a face image (PDF, InDesign, PSD, `.DS_Store`, product mockups, header graphics). Not moved.")
w("")
w("Duplicates are matched on the normalised name **and** number (e.g. `Mark Owen 2.jpg` = `mark owen 2 MH.jpg`; `Mark Owen.jpg` is a "
  "different image from `Mark Owen 2.jpg`). Suffixes MH, JB, CPDVD, MINT, Onbuy ver, Face, Mask, `_`, `-` and agency numbers are ignored; "
  "the part after ` - ` (club, show, sport) is ignored for matching. Sizes are compared in bytes from the Dropbox listing, not by pixels.")
w("")
w("## Where the files would go (move + variant + check + duplicate_larger)")
w("")
w("| Destination folder | From TO SORT | From the root | Total | Folder exists? |")
w("|---|---:|---:|---:|---|")
cnt = collections.Counter(); cts = collections.Counter(); clo = collections.Counter()
for x in rows:
    d = dest_folder(x)
    if d:
        cnt[d] += 1
        (cts if x["origin"] == "TO SORT" else clo)[d] += 1
for d, n in sorted(cnt.items(), key=lambda t: (-t[1], t[0])):
    w("| %s | %d | %d | %d | %s |" % (d, cts[d], clo[d], n, "yes" if d.lower() in folders else "**new**"))
w("")
w("## Duplicates")
w("")
for a in ["duplicate_exact", "duplicate_smaller", "duplicate_larger", "check"]:
    w("- `%s`: %d" % (a, sum(x["action"] == a for x in rows)))
w("")
w("Full detail (which file each one matches, both sizes) is in `plan.csv` (`match_path`, `match_size`, `reason`).")
w("")
w("## Unsure (%d) and best guesses" % sum(x["action"] == "unsure" for x in rows))
w("")
w("| File | Where | Best guess / why |")
w("|---|---|---|")
for x in sorted([x for x in rows if x["action"] == "unsure"], key=lambda x: x["file_name"].lower()):
    w("| %s | %s | %s |" % (x["file_name"].replace("|", "/"), x["origin"], (x["person"] + ": " if x["person"] else "") + x["reason"].replace("|", "/")))
w("")
w("## Not face images (left where they are): %d" % sum(x["action"] == "leave" for x in rows))
w("")
for x in sorted([x for x in rows if x["action"] == "leave"], key=lambda x: x["file_name"].lower()):
    w("- %s (%s): %s" % (x["file_name"], x["origin"], x["reason"]))
w("")
w("## How the people and categories were worked out")
w("")
w("1. Each file name is normalised (`tools/norm.py`) and matched to the person list built on 2 Oct 2026 "
  "(`../face-masks/dropbox-masks-master-list.csv`, 6,980 people with category, sport and show). 97% of the files matched.")
w("2. The rest, and the people that list had filed as \"other\", were decided by hand in `tools/overrides.py` "
  "(e.g. `Linda - Gimmie Gimmie` = Kathy Burke, TV; `S Roberta - Barca` = Sergi Roberto, footballer; YouTubers, business people, novelty masks).")
w("3. Category to folder: TV and reality to `2026 TV SHOWS AND STARS` (into the show's own subfolder where one already exists, e.g. "
  "Coronation Street, Emmerdale, Hollyoaks, TOWIE, Love Island); film to `2026 MOVIE STARS` (Harry Potter etc. into their subfolders); "
  "Indian film stars to `2026 BOLLYWOOD ACTORS`; sports by sport (see `proposed-folders.md`).")
w("4. Then `tools/build_plan.py` checks every file against everything already in the 2026 folders and `WAG MODEL`, and against the other "
  "source files, and makes sure no destination name is used twice.")
w("")
w("## Next steps (phase 2, needs the owner's go-ahead)")
w("")
w("1. Owner reviews `plan.csv`, especially `check`, `duplicate_larger`, `unsure` and the new folders.")
w("2. Create only the approved new folders, then move the approved `move`/`variant` rows in small batches with `mcp__Dropbox__move` "
  "(never `autorename` over an existing file, never delete), re-listing each destination after every batch.")
w("3. Duplicates stay where they are until the owner says what to do with them; nothing is trashed.")
open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("summary.md written", len(L), "lines")
