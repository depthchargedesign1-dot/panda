# Shopify CSV import schedule (owner: one file each morning and one at bedtime)

Files no longer need a slot each: import the next one as soon as Shopify's "import complete" email arrives. Always tick "Overwrite products with matching handles". Wait for Shopify's "import complete" email before the next file.
Before each reminder, Claude checks the previous file landed on the live store (spot-check handles) and ticks it off here.

| # | When (UK) | File | Status |
|---|---|---|---|
| 0 | 6 Oct | seo/2026-10-06-remaining/01-seo.csv | DONE (checked 15:08 UK; created 21 duplicate trerrace flag drafts) |
| 1 | Tue 6 Oct bedtime | seo/2026-10-06-remaining/02-seo-CLEAN.csv | DONE (finished 19:58 UTC, 6 Oct) |
| 2 | Wed 7 Oct morning | google-fields/2026-10-06-age-group-remaining/01-age-group-gender-SAFE.csv (NOT the older 01-age-group-gender.csv) | DONE (finished ~01:50 UTC 7 Oct, checked 07:55 UK) |
| 3 | Wed 7 Oct bedtime | google-fields/2026-10-06-age-group-remaining/02-age-group-gender-SAFE.csv (NOT 02-…-CLEAN) | DONE (finished 11:50 UTC 8 Oct) |
| 4 | as soon as #3 finishes | import-queue-2026-10-08/1-TEST-3-masks.csv (2 KB: check the 3 masks show Ready Cut/DIY x Elastic/Stick at £2.99/£3.49/£1.50/£2.00) | to do |
| 5 | straight after the test looks right | import-queue-2026-10-08/2-ALL-single-masks.csv (all 6,729 single masks, 4.6 MB; replaces old masks 01–04) | to do |
| 6 | next | import-queue-2026-10-08/3-TEST-6-mugs-3-prints.csv (check 6 mugs + 3 prints) | to do |
| 7 | next | import-queue-2026-10-08/4-mugs-and-prints-part1.csv (13.8 MB) | to do |
| 8 | next | import-queue-2026-10-08/5-mugs-and-prints-part2.csv (13.8 MB) | to do |
| 9 | next | import-queue-2026-10-08/6-mugs-and-prints-part3.csv (13.8 MB) | to do |
| 10 | next | import-queue-2026-10-08/7-mugs-and-prints-part4.csv (13.4 MB) | to do |

Merged on 8 Oct (owner: "merge any we can to save time"): 13 queued files -> 7. Parts 4–7 hold all 6,458 mug descriptions (incl. 194 rude) and 13,250 signed prints; every product's rows are in one file; rows checked 46,810 = 46,810. Old per-job files are kept for reference only — don't import them. Masks and mugs/prints have different columns, so they are never mixed in one file (a blank cell would wipe that field).

If one slot is missed, the next reminder simply repeats the next undone file (the order matters, the dates don't).
After #0 finishes: delete the duplicate "trerrace" draft flags it created (owner to confirm).
