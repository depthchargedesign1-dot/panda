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
