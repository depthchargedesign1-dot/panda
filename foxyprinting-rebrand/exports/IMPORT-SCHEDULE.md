# Shopify CSV import schedule (owner: one file each morning and one at bedtime)

Always tick "Overwrite products with matching handles". Wait for Shopify's "import complete" email before the next file.
Before each reminder, Claude checks the previous file landed on the live store (spot-check handles) and ticks it off here.

| # | When (UK) | File | Status |
|---|---|---|---|
| 0 | 6 Oct | seo/2026-10-06-remaining/01-seo.csv | DONE (checked 15:08 UK; created 21 duplicate trerrace flag drafts) |
| 1 | Tue 6 Oct bedtime | seo/2026-10-06-remaining/02-seo-CLEAN.csv | DONE (finished 19:58 UTC, 6 Oct) |
| 2 | Wed 7 Oct morning | google-fields/2026-10-06-age-group-remaining/01-age-group-gender-SAFE.csv (NOT the older 01-age-group-gender.csv) | uploading (started ~21:15 UTC 6 Oct; verify at morning reminder) |
| 3 | Wed 7 Oct bedtime | google-fields/2026-10-06-age-group-remaining/02-age-group-gender-SAFE.csv (NOT 02-…-CLEAN) | to do |
| 4 | Thu 8 Oct morning | face-masks/2026-10-06-single-mask-prices/import/00-TEST-3-masks.csv (check 3 masks), then 01-single-masks.csv | to do |
| 5 | Thu 8 Oct bedtime | face-masks/2026-10-06-single-mask-prices/import/02-single-masks.csv | to do |
| 6 | Fri 9 Oct morning | face-masks/.../03-single-masks.csv | to do |
| 7 | Fri 9 Oct bedtime | face-masks/.../04-single-masks.csv | to do |
| 7a | after #7 (next free slot) | mug-descriptions/2026-10-06/00-TEST-6-mugs.csv (check the 6 mugs: 3 normal, 3 rude), then 01-mug-descriptions.csv (6,081 mugs) | to do |
| 7b | next slot | mug-descriptions/2026-10-06/02-rude-mug-descriptions.csv (194 rude mugs) | to do |
| 8 | Sat 10 Oct morning | signed-prints/2026-10-06-title-copy/00-TEST-3-products.csv (check), then 01-signed-prints.csv | to do |
| 9 | Sat 10 Oct bedtime | signed-prints/.../02-signed-prints.csv | to do |
| 10 | Sun 11 Oct morning | signed-prints/.../03-signed-prints.csv | to do |
| 11 | Sun 11 Oct bedtime | signed-prints/.../04-signed-prints.csv | to do |

If one slot is missed, the next reminder simply repeats the next undone file (the order matters, the dates don't).
After #0 finishes: delete the duplicate "trerrace" draft flags it created (owner to confirm).
