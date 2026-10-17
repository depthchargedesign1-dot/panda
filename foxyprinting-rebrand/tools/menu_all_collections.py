"""Add every remaining collection to the mega menu as extra "More …" columns.

Reads a collection snapshot (handle, title, onStore, productsCount), skips collections that
are already linked, hidden/duplicate (plan/collection-tidy.md), off the store, empty or
system-only, and groups the rest by banner group (tools/collection_headers.py).
Writes plan/menu_extra.json, which plan/mega_menu.py merges into the menu.
Usage: python3 tools/menu_all_collections.py <collections.json>
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "plan")]
from collection_headers import header_for  # noqa: E402
import mega_menu  # noqa: E402

SYSTEM = {"newest-products", "new-collections", "frontpage", "facebook", "untitled-range-40564",
          "best-selling-products", "fathers-day-gifts"}

# banner group -> (department, column title)
PLACE = {
    "masks": ("Fan Shop & Retro", "More Face Masks"),
    "retro": ("Fan Shop & Retro", "More Retro Gaming"),
    "gaming": ("Fan Shop & Retro", "More Retro Gaming"),
    "skins": ("Fan Shop & Retro", "Skins & Wraps"),
    "sports": ("Fan Shop & Retro", "More Sports"),
    "mugs": ("Home & Drinkware", "More Mugs"),
    "prints": ("Home & Drinkware", "More Prints & Posters"),
    "bar": ("Home & Drinkware", "Bar, Coasters & Glassware"),
    "drinkware": ("Home & Drinkware", "Bar, Coasters & Glassware"),
    "commemorative": ("Occasions", "Royal & Commemorative"),
    "love": ("Occasions", "Love & Weddings"),
    "halloween": ("Occasions", "More Seasonal"),
    "easter": ("Occasions", "More Seasonal"),
    "gifts": ("Personalised Gifts", "More Gifts"),
    "stickers": ("Business Printing", "More Stickers & Labels"),
    "business": ("Business Printing", "More Business Printing"),
    "kids": ("Baby & Kids", "More Kids"),
    "baby": ("Baby & Kids", "More Kids"),
    "clothing": ("Clothing", "More Clothing"),
    "cards": ("Cards & Invitations", "More Cards"),
    "party": ("Cards & Invitations", "More Party Printing"),
    "christmas": ("Christmas", "More Christmas"),
    "pets": ("Pets", "More Pet Gifts"),
    "skip": ("Cards & Invitations", "More Cards"),
}

SMALL = {"and", "of", "the", "for", "a", "in", "on", "to", "with", "or", "by"}
KEEP_UPPER = {"TV", "PS1", "PS2", "PS3", "PS4", "PSP", "N64", "NES", "SNES", "UK", "DVD", "VHS", "CD", "F1",
              "A6", "A4", "A3", "LED", "NFL", "WWE", "UFC", "VE", "III", "II", "DJ", "3DO", "TOWIE", "PE"}


def nice(title):
    """Tidy SHOUTY titles for the menu ('PS1 GAME CASES' -> 'PS1 Game Cases')."""
    t = re.sub(r"\s+", " ", title).strip()
    if t.upper() != t:
        return t
    out = []
    for i, w in enumerate(t.split(" ")):
        bare = re.sub(r"[^A-Za-z0-9]", "", w)
        if bare in KEEP_UPPER:
            out.append(w)
        elif i and w.lower() in SMALL:
            out.append(w.lower())
        else:
            out.append(re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda m: m.group(0).capitalize(), w))
    return " ".join(out)


def linked_handles():
    urls = set()
    for _, u, cols in mega_menu.BASE_MENU:
        urls.add(u)
        for _, u2, kids in cols:
            urls.add(u2)
            urls.update(u3 for _, u3 in kids)
    return {u.rsplit("/", 1)[-1] for u in urls}


def hidden():
    """Handles and titles listed for hiding in plan/collection-tidy.md (sections A and B)."""
    tidy = (ROOT / "plan" / "collection-tidy.md").read_text().split("## C.")[0]
    handles = set(re.findall(r"`([a-z0-9-]+)`", tidy))
    titles = {re.sub(r"\s*\(`.*", "", m).strip().lower()
              for m in re.findall(r"^(?:\| |- )([^|\n]+?)(?: \||$)", tidy, re.M)}
    return handles, titles


def build(snapshot):
    hidden_h, hidden_t = hidden()
    skip = linked_handles() | hidden_h | SYSTEM
    extra = {}
    for c in sorted(snapshot, key=lambda c: nice(c["title"]).lower()):
        h = c["handle"]
        if h in skip or c["title"].strip().lower() in hidden_t or c["productsCount"]["count"] == 0:
            continue
        if not c.get("onStore") and not h.startswith("new-"):
            continue
        group = "prints" if re.search(r"signed|autograph", h) else header_for(h)
        dept, col = PLACE[group]
        extra.setdefault(dept, {}).setdefault(col, []).append([nice(c["title"]), f"/collections/{h}"])
    return extra


if __name__ == "__main__":
    extra = build(json.load(open(sys.argv[1])))
    (ROOT / "plan" / "menu_extra.json").write_text(json.dumps(extra, indent=1, ensure_ascii=False) + "\n")
    print({d: {c: len(v) for c, v in cols.items()} for d, cols in extra.items()})
