# Shopify CSV import schedule (owner: one file each morning and one at bedtime)

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
| 6 | next | import-queue-2026-10-08/3-TEST-6-mugs-3-prints.csv (check 6 mugs + 3 prints) | READY (rebuilt 8 Oct: 3 posters with new descriptions, no "Reproduction Print" in titles, garbled title fixed; 6 mug rows unchanged). Sent to owner ~17:05 UTC. Import after the masks file finishes. Files 4–7 rebuilt too (see below) |
| 7 | next | import-queue-2026-10-08/4-mugs-and-prints-part1.csv (14.5 MB; now also rewrites 1,435 poster descriptions) | SENT 8 Oct ~21:15 UTC for overnight import (owner asked for a big file). SAFEGUARD checked: no live Status/Title changes since 16:50 UTC on its handles. File 3 still not imported; it's independent, so it can follow |
| 8 | next | import-queue-2026-10-08/5-mugs-and-prints-part2.csv (13.9 MB; now also rewrites 5,133 poster descriptions) | to do |
| 9 | next | import-queue-2026-10-08/6-mugs-and-prints-part3.csv (6.7 MB; now also rewrites 3,069 poster descriptions) | to do |
| 10 | next | import-queue-2026-10-08/7-mugs-and-prints-part4.csv (8.5 MB; now also rewrites 3,736 poster descriptions) | to do |

Merged on 8 Oct (owner: "merge any we can to save time"): 13 queued files -> 7. Parts 4–7 hold all 6,458 mug descriptions (incl. 194 rude) and 13,250 signed prints; every product's rows are in one file; rows checked 46,810 = 46,810. Old per-job files are kept for reference only — don't import them. Masks and mugs/prints have different columns, so they are never mixed in one file (a blank cell would wipe that field).

Rebuilt on 8 Oct, evening (owner: "the css and descriptions for the poster prints does not display correct"): files 3–7 now carry a new clean description for all 13,376 "Printed Signature" posters (one h2, h3 sections, real size/frame list, Premium Display frames line, reproduction print stated at the top, signed-print + sports/celebrity/music disclaimer at the end; no inline styles, spans, h1, tables or "limited edition / authentic / memorabilia" wording). Mug rows unchanged. Titles and statuses refreshed from live just before the rebuild (1 status: trent-alexander-arnold-limited-edition-… is now draft live, so draft here). "Reproduction Print" removed from every title (owner: "i dont want reproduction Print in the title"; 9,587 live titles still have it until these files are imported; no SEO titles have it). 31 garbled poster titles repaired (e.g. Cã©Sar → César). Rows per handle unchanged (46,840 rows; each product in one file). Generator: `tools/poster_descriptions.py`; samples: `exports/poster-descriptions/2026-10-08/samples.html`.

If one slot is missed, the next reminder simply repeats the next undone file (the order matters, the dates don't).
After #0 finishes: delete the duplicate "trerrace" draft flags it created (owner to confirm).
