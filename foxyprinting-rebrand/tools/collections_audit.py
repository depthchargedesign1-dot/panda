"""Empty-collection audit (8 Oct 2026).

Reads exports/collections-audit/2026-10-08/raw/all.json (every collection with total productsCount and
`visible` = ACTIVE + published to the Online Store, from productsCount(query:"collection_id:N status:active
published_status:published")) and status.json (active/draft split for the empty ones), classifies every
collection with 0-2 visible products and writes empty-collections.csv.
Usage: python3 tools/collections_audit.py
"""
import csv, json
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "exports/collections-audit/2026-10-08"
nodes = json.load(open(D / "raw/all.json"))

OUTDATED = {  # (a) seasonal-past / dated
    "king-charles-coronation", "king-charles-coronation-pins", "king-charles-iii-coeronation-clothing",
    "king-charles-iii-coronation-bags", "king-charles-iii-coronation-bear", "king-charles-iii-coronation-bunting",
    "king-charles-iii-coronation-clothing", "king-charles-iii-coronation-coasters",
    "king-charles-iii-coronation-kids-t-shirts", "king-charles-iii-coronation-medals",
    "king-charles-iii-coronation-metal-bottle", "king-charles-iii-coronation-snoods",
    "king-charles-iii-coronation-tea-towels", "king-charles-coronation-mug", "printed-clothing-new-2023",
    "social-distancing-stickers-printing",
}
REDIRECT = {
    "social-distancing-stickers-printing": "/collections/new-stickers-labels",
    "printed-clothing-new-2023": "/collections/new-custom-clothing",
}
DUPLICATE = {  # (e) legacy duplicates of a live collection
    "this-guy-is": "/collections/this-girl-this-guy-mugs (334 live)",
    "this-is-my-birthday-mugs": "/collections/this-is-my-birthday-mug (449 live)",
}
DRAFT_NOTE = {  # (b)
    "atari-posters": "293 Atari posters set to DRAFT on 7 Oct 2026 (not by this audit). Retro game box art / console logos are off-limits online (owner rule 6 Oct), so keep them draft and hide this collection from the Online Store. Do NOT reactivate.",
    "atari-7800-posters": "34 Atari 7800 posters DRAFT since 7 Oct; same as ALL ATARI POSTERS: keep draft, hide collection.",
    "atari-jaguar": "32 Atari Jaguar replacement cases DRAFT (6 Oct); console/publisher artwork risk: keep draft, hide collection.",
    "errea-bags": "4 Errea trolley bags are UNLISTED (old RRP stock, Errea brand). Hide the collection, or relist only if you still have the stock.",
    "design-your-own-leavers-hoodies-2026": "3 leavers designer products in DRAFT (created 8 Oct, waiting for the owner). Goes live when you approve them; nothing to make.",
    "plaques-occasion-gifts": "Its 4 ACTIVE products (club-name bottle-opener plaques: Chelsea, Arsenal, Aston Villa, Bournemouth) are not on the Online Store (left alone on 6 Oct). FIXED 8 Oct: added 5 live plaques/photo tiles/award trophy. Owner: check the club plaques for crests before putting them on the website.",
}
RULE_FIXED = {  # (c) fixed 8 Oct 2026 (old rule kept in `rule` column)
    "unicorn-santa-sacks": "FIXED: rule now TITLE CONTAINS Unicorn AND TAG = Santa Sacks (10 Personalised Unicorn Santa Sacks). Old tag UNICORN SANTA SACKS was on no product.",
    "ru-pauls-drag-race": "FIXED: rule now TAG = RU PAULS DRAG RACE OR TAG = Ru Paul Drag Race (RuPaul + Michelle Visage masks; tag spelling differed). Near-empty: add more Drag Race masks.",
    "stag-hen-ideas": "FIXED: now a hub of stag & hen masks + stag/hen T-shirts (TAG STAG & HEN PARTY FACE MASKS / STAG DOO T-SHIRTS / Stag T-Shirts / Hen T-Shirts / stag-do / hen-party).",
    "personalised-flask": "FIXED: rule now also TAG = hip flask (Personalised Hip Flask). Near-empty (1).",
    "i-love-celebrity-mugs": "FIXED: rule now also TITLE CONTAINS 'I Love Celebrity' (about 495 mugs).",
    "the-voice": "FIXED: tag THE VOICE added to 12 coach/presenter masks (will.i.am, Tom Jones, Danny Jones, Anne-Marie, Emma Willis, Rita Ora, Boy George, Holly Willoughby).",
}
GENUINE = {  # (d) new product made 8 Oct 2026, ACTIVE on all 5 channels
    "trust-me-im-a-mugs": "personalised-trust-me-im-a-mug",
    "i-like-mugs": "personalised-i-like-and-maybe-3-people-mug",
    "i-used-to-drive-mugs": "personalised-i-used-to-drive-retirement-mug",
    "ive-got-mugs": "personalised-ive-got-this-mug",
    "cheeky-mugs": "personalised-cheeky-little-brew-mug",
    "art-poster": "personalised-mid-century-abstract-family-name-print",
}
AFTER = {  # visible products re-counted after the 8 Oct fixes / new products
    "unicorn-santa-sacks": 10, "ru-pauls-drag-race": 4, "stag-hen-ideas": 575, "personalised-flask": 1,
    "i-love-celebrity-mugs": 118, "the-voice": 12, "plaques-occasion-gifts": 5,
    "trust-me-im-a-mugs": 1, "i-like-mugs": 1, "i-used-to-drive-mugs": 1, "ive-got-mugs": 1, "cheeky-mugs": 1,
    "art-poster": 1, "personalised-mug": 6, "personalised-poster": 2,
}
QUEUE = {
    "a6-movie-and-film-poster-card-packs": "Needs film-poster artwork for a 6-card A6 pack (studio/poster art is a trademark risk). Queue: owner to say which films/actors (celebrity faces are fine, no logos).",
    "a6-autographed-f1-poster-card-packs": "Needs 6 F1 driver printed-signature prints for an A6 pack (no team logos). Queue: build from the existing F1 printed-signature posters once the owner OKs it.",
}

rows = []
for n in nodes:
    v, t, h = n["visible"], n["productsCount"]["count"], n["handle"]
    if v > 2:
        continue
    os_ = n["os"]
    rule = n["rule"] or "MANUAL"
    if v > 0:
        cls, rec = "near-empty", "1-2 visible products: add more products when making new lines."
        if h in RULE_FIXED: cls, rec = "c-rule-fixed", RULE_FIXED[h]
        if not os_: cls, rec = "hidden", "Not on the Online Store: no Google impact."
        if h in ("ve-day-bunting", "wales-2021-football-face-masks"): cls, rec = "a-outdated", "Dated (VE Day 80 / Euro 2021). Hide from the Online Store; draft the products."
        if h == "personalised-poster": rec = "Now 2 (new family name print added 8 Oct)."
        if h == "personalised-mug": rec = "Now 6 (the 5 new personalised mugs carry its tag, 8 Oct)."
    elif h in RULE_FIXED: cls, rec = "c-rule-fixed", RULE_FIXED[h]
    elif not os_: cls, rec = "hidden", "Not on the Online Store, so Google can't see it. Leave hidden (or tidy up later)."
    elif h.startswith("ve-day") or h in OUTDATED:
        cls = "a-outdated"
        rec = ("Past event (VE Day 80th, May 2025 / Coronation, May 2023 / Covid era). Products already DRAFT: keep them draft. "
               "Hide this collection from the Online Store (Products > Collections > tick > Exclude from sales channels > Online Store) "
               "and add a 301 redirect to " + REDIRECT.get(h, "/collections/politicians-and-royals" if "king-charles" in h else "/ (homepage)") + ".")
    elif h in DUPLICATE: cls, rec = "e-duplicate", "Duplicate of a live collection. Hide it and 301 redirect to " + DUPLICATE[h] + "."
    elif h in DRAFT_NOTE: cls, rec = "b-draft-or-archived", DRAFT_NOTE[h]
    elif h in GENUINE: cls, rec = "d-genuine", f"FILLED 8 Oct: new product https://foxyprinting.co.uk/products/{GENUINE[h]} (ACTIVE, all 5 channels)."
    elif h in QUEUE: cls, rec = "d-queue", QUEUE[h]
    else: cls, rec = "?", "check"
    rows.append(dict(title=n["title"], handle=h, url=f"https://foxyprinting.co.uk/collections/{h}",
                     type="smart" if n["rule"] else "manual", rule=rule, on_online_store=os_, total=t, visible=v,
                     visible_after_8oct_fixes=AFTER.get(h, v),
                     **{"class": cls}, recommendation=rec))

rows.sort(key=lambda r: (r["visible"], r["class"], r["title"]))
with open(D / "empty-collections.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(nodes), "collections;", Counter((r["visible"] == 0, r["class"]) for r in rows))
print([r["handle"] for r in rows if r["class"] == "?"])
