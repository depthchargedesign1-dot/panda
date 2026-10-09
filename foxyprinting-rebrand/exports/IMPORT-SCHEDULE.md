# Shopify CSV import schedule

**Files 0–10 DONE (9 Oct 2026, 12:22 UTC).** New: Google fields files 11–15 below (from the 9 Oct full audit, `catalogue-audit/2026-10-09/README.md`).
 (owner: one file each morning and one at bedtime)

Files no longer need a slot each: import the next one as soon as Shopify's "import complete" email arrives. Always tick "Overwrite products with matching handles". Wait for Shopify's "import complete" email before the next file.
Before each reminder, Claude checks the previous file landed on the live store (spot-check handles) and ticks it off here.

| # | When (UK) | File | Status |
|---|---|---|---|
| 0 | 6 Oct | seo/2026-10-06-remaining/01-seo.csv | DONE (checked 15:08 UK; created 21 duplicate trerrace flag drafts) |
| 1 | Tue 6 Oct bedtime | seo/2026-10-06-remaining/02-seo-CLEAN.csv | DONE (finished 19:58 UTC, 6 Oct) |
| 2 | Wed 7 Oct morning | google-fields/2026-10-06-age-group-remaining/01-age-group-gender-SAFE.csv (NOT the older 01-age-group-gender.csv) | DONE (finished ~01:50 UTC 7 Oct, checked 07:55 UK) |
| 3 | Wed 7 Oct bedtime | google-fields/2026-10-06-age-group-remaining/02-age-group-gender-SAFE.csv (NOT 02-…-CLEAN) | DONE (finished 11:50 UTC 8 Oct) |
| 4 | as soon as #3 finishes | import-queue-2026-10-08/1-TEST-3-masks.csv (2 KB: check the 3 masks show Ready Cut/DIY x Elastic/Stick at £2.99/£3.49/£1.50/£2.00) | DONE 13:12 UTC 8 Oct (all 3 checked live: options + prices correct) |
| 5 | straight after the test looks right | import-queue-2026-10-08/2-ALL-single-masks.csv (all 6,729 single masks, 4.6 MB; replaces old masks 01–04) | DONE (last rows updated 17:38 UTC 8 Oct) |
| 6 | next | import-queue-2026-10-08/3-TEST-6-mugs-3-prints.csv (check 6 mugs + 3 prints) | DONE 21:36 UTC 8 Oct (checked live: 3 poster titles clean, Cerrone curly quotes fixed, mugs updated) |
| 7 | next | import-queue-2026-10-08/4-mugs-and-prints-part1.csv (14.5 MB; now also rewrites 1,435 poster descriptions) | DONE (last rows updated 23:21 UTC 8 Oct; checked 06:55 UTC 9 Oct: Jonny May 2, Joost Luiten 2, Jordan Ibe 1 posters and a Worlds Best mug match the file) |
| 8 | next | import-queue-2026-10-08/5-mugs-and-prints-part2.csv (13.9 MB; now also rewrites 5,133 poster descriptions) | DONE (last rows updated 09:00 UTC 9 Oct; checked 09:15 UTC: Ian Wright 2, Ian Snodin 2, Pedro 2 match the file; Miguel Almirón accents fixed) |
| 9 | next | import-queue-2026-10-08/6-mugs-and-prints-part3.csv (6.7 MB; now also rewrites 3,069 poster descriptions) | DONE (last rows updated 10:53 UTC 9 Oct; checked 10:58 UTC: Beau Brinkley, Beau Allen 2, Stuart Pearce titles match the file) |
| 10 | next | import-queue-2026-10-08/7-mugs-and-prints-part4.csv (8.5 MB; now also rewrites 3,736 poster descriptions) | DONE (last rows updated 12:21:57 UTC 9 Oct; checked 12:25 UTC: Ben Garland 1, The Weeknd 2026, Zara Larsson, Mervyn King match the file; 0 poster titles left with "Reproduction Print") |
| 11 | next | google-fields/2026-10-09-full/00-TEST-3-products.csv (3 products: check a signed print, a GameCube poster and a magnet show the new Google fields and nothing else changed) | to do |
| 12 | after the test | google-fields/2026-10-09-full/01-google-fields.csv (14,000 products; Handle + 7 Google metafields only) | to do |
| 13 | next | google-fields/2026-10-09-full/02-google-fields.csv | to do |
| 14 | next | google-fields/2026-10-09-full/03-google-fields.csv | to do |
| 15 | next | google-fields/2026-10-09-full/04-google-fields.csv (12,381 products) | to do |

Merged on 8 Oct (owner: "merge any we can to save time"): 13 queued files -> 7. Parts 4–7 hold all 6,458 mug descriptions (incl. 194 rude) and 13,250 signed prints; every product's rows are in one file; rows checked 46,810 = 46,810. Old per-job files are kept for reference only — don't import them. Masks and mugs/prints have different columns, so they are never mixed in one file (a blank cell would wipe that field).

Rebuilt on 8 Oct, evening (owner: "the css and descriptions for the poster prints does not display correct"): files 3–7 now carry a new clean description for all 13,376 "Printed Signature" posters (one h2, h3 sections, real size/frame list, Premium Display frames line, reproduction print stated at the top, signed-print + sports/celebrity/music disclaimer at the end; no inline styles, spans, h1, tables or "limited edition / authentic / memorabilia" wording). Mug rows unchanged. Titles and statuses refreshed from live just before the rebuild (1 status: trent-alexander-arnold-limited-edition-… is now draft live, so draft here). "Reproduction Print" removed from every title (owner: "i dont want reproduction Print in the title"; 9,587 live titles still have it until these files are imported; no SEO titles have it). 31 garbled poster titles repaired (e.g. Cã©Sar → César). Rows per handle unchanged (46,840 rows; each product in one file). Generator: `tools/poster_descriptions.py`; samples: `exports/poster-descriptions/2026-10-08/samples.html`.

If one slot is missed, the next reminder simply repeats the next undone file (the order matters, the dates don't).
After #0 finishes: delete the duplicate "trerrace" draft flags it created (owner to confirm).
