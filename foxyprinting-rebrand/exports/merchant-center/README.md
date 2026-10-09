# Merchant Center tidy-up report (6 Oct 2026): read only, nothing changed

Source: two Shopify bulk exports taken 6 Oct 2026 (all 58,760 products; featured image of the 55,989 ACTIVE ones).
Rebuild with `build_duplicates.py` (see its docstring). No status, title, handle or description was changed.

## `2026-10-06-duplicates.csv` (2,505 rows, ACTIVE products only)
Columns: id, title, handle, status, likely_original_id, recommendation, reason, main_image_vs_original, priority,
in_58_conflicted_copies, product_type. "Original" = the copy without "copy" in its handle/title, else the oldest.

| priority | rows | what | recommendation |
|---|---|---|---|
| HIGH | 284 | same title + identical description as another ACTIVE product, and the same main image file (or no image) | set to DRAFT + URL redirect to the original (17 have no image on one side: check first) |
| MEDIUM | 58 | the 58 identical `-copy` signed prints from the 5 Oct "conflicted copy" fix | owner kept them ACTIVE on 5 Oct; DRAFT + redirect if Merchant Center flags them |
| MEDIUM | 593 | same title + identical description, but a different main image | make unique: next free number in the title, new description |
| LOW | 44 | "copy" in handle, twin exists, but the text or image differs | tidy handle (with redirect), rewrite text if needed |
| LOW | 1,514 | "copy" in handle/title only (old Shopify "Duplicate" leftovers), no twin | keep; optional handle tidy |
| LOW | 12 | option/upgrade helper products (OPTIONS_HIDDEN_PRODUCT, "Your Poster is UPGRADED…") | keep ACTIVE; exclude from the Google feed |

HIGH rows by type: Celebrity Mugs 155 (mostly "This girl loves her <dog> Mug"), Football Posters 88, others 41.

## `2026-10-06-shared-descriptions.csv`
407 groups of ACTIVE products (8,376 listings) share word-for-word description text with different titles,
e.g. 1,030 football signed prints, 1,000 Santa sacks, 760 name mugs, 549 SNES cases. Merchant Center does not
usually reject these, but unique copy helps ranking. Also 2,093 ACTIVE products have an empty description.
Note: the football print template says "a limited edition signed print", which breaks the house rule on
reproduction prints ("Printed Signature" / "Reproduction Print"): flagged for the owner, not changed.

## `2026-10-06-retro-gaming-boxart-risk.csv`
13,044 ACTIVE retro gaming products named after specific games (likely publisher box art): magnets 4,298,
posters 3,314, replacement cases/covers 2,832, keyrings 2,600. Risk number only; nothing changed.
Excludes the personalised "put yourself on the cover" cases and the new blank cases.
