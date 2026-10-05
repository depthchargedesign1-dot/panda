# 2026-10-05 – Dropbox "conflicted copy" titles + "Harry Stlyes" typo

## What was found
- **63 ACTIVE** signed-print products with `Fujistsu-Pc's CoNFLicted 2019-04-08` in the title,
  `-fujistsu-pcs-conflicted-copy-2019-04-08` in the handle and `(Fujistsu-PC's Conflicted Copy 2019-04-08)`
  in the description. Searches for `conflicted`, `*onflicted*`, `*Fujistsu*`, `*Fujitsu*`, `*2019-04-08*` and
  `handle:*conflicted*` all return the same 63. SEO title/meta were empty and image alt text was `0`, so no junk there.
- **3 ACTIVE** "Harry Stlyes 2/3/4" products.

## What was changed (productUpdate only, redirectNewHandle: true)
| id | old handle | new title / handle |
|---|---|---|
| gid://shopify/Product/14903390404989 | harry-stlyes-3-signed-autographed-music-star-print | Harry Styles 3 – … / harry-styles-3-signed-autographed-music-star-print |
| gid://shopify/Product/14903390732669 | harry-stlyes-4-signed-autographed-music-star-print | Harry Styles 4 – … / harry-styles-4-signed-autographed-music-star-print |

Typo also fixed in the description. Tags, status, SEO, media, metafields untouched. Redirects from the old
URLs were created (UrlRedirect 1753960415613 and 1753960448381) and checked.

## What was NOT changed: duplicates (`duplicates.csv`, 64 rows)
Every one of the 63 conflicted-copy products, plus "Harry Stlyes 2", already has a clean twin: an ACTIVE product
with exactly the clean handle and the clean title. For 63 of the 64 pairs the description is identical once the junk
is removed. These are leftover copies. Owner to decide: usually set the junk copy to Draft/Archived (or delete it)
and add a URL redirect from its handle to the clean twin. Nothing was archived or deleted.

## Notes for the owner (`notes.csv`)
Sports people labelled "Music Star Print" (Martin Offiah, Nat Lofthouse), odd titles (Nwa Fully Printed Signature 1/2,
Printed Signature By Blur, Selina Gomez 2, Manic Street 2), and range-wide tag/alt/description issues.

## Files
- `before.json` – all 66 affected products (id, title, handle, status, tags, type, vendor, seo, descriptionHtml, media alt) before any change.
- `after.json` – the 2 changed products re-read after the update.
- `duplicates.csv`, `notes.csv`.

## Rollback
For each product in `after.json`, `productUpdate` with the `title`, `handle` and `descriptionHtml` from `before.json`
(redirectNewHandle: false), then delete the two UrlRedirects listed above.

## Update 2026-10-05 (owner's decision: fix, keep every version ACTIVE)
Rule: a number after a name means a different image of the same person, and every version is kept.
I compared each conflicted copy's main image with its twin's (filename, width/height, file size, then an ImageMagick
pixel compare plus a visual check).
- `renumbered.csv`: 6 with a different photo get the next free number: Harry Stlyes 2 -> **Harry Styles 5**,
  Miley Cyrus 1 -> **Miley Cyrus 5**, Miley Cyrus 2 -> **Miley Cyrus 6**, Oasis 1 -> **Oasis 7**,
  Paul Weller 2 -> **Paul Weller 5**, Slash 1 -> **Slash 5**.
- `identical.csv`: 58 with the same artwork get the clean title and the handle `<clean handle>-copy`. For 5 of them
  (The Clash 1 and 2, The Doors 2, The National 1 and 2) only the mockup background differs, and the photo is the same.
- "Selina Gomez 2" could not become "Selena Gomez 2": that product already exists with a different photo. So it
  became **Selena Gomez 3** (`before-extra.json`), and its conflicted copy becomes "Selena Gomez 3", handle `...-copy`.
- Junk is removed from descriptionHtml. Nothing else changes (status, price, tags, media).

**Status: partly applied.** 10 products are done and verified (`after-fix.json`). The other 55 are in
`pending-updates.json`, ready to send. They are not applied because the session's permission check stopped further
bulk store edits.
