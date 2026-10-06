# Google Shopping age group and gender: the remaining fixes

Built on 6 October 2026. **This replaces `../2026-10-05-age-group/`: don't import those files.** They are superseded, because part of the work was pushed by API afterwards and these files cover everything that is left.

## What it fixes

The API pushed batches 0 to 6 (the first 1,225 changes, all age group) of the 60,773 planned changes. These files cover the other 59,548 changes, which is **48,745 products**, one row each, with age group and gender combined.

| Group | Products |
|---|---:|
| Age group `adult` only (gender already `unisex`) | 31,796 |
| Age group `adult` and gender `unisex` (gender was blank, "Unisex", Male, Female or Kid) | 10,659 |
| Age group `kids` only (gender already `unisex`) | 6,146 |
| Age group `kids` and gender `unisex` | 144 |
| **Total** | **48,745** |

By value: 42,455 rows `adult,unisex` and 6,290 rows `kids,unisex`. The test file's 3 products come out of these totals.

There are no gender-only changes: every product that needs gender also needs age group. The age group in each row is the planned (correct) value, and for age-only products gender is already `unisex`, so a row never blanks a column.

## Files

| File | Rows |
|---|---:|
| `00-TEST-3-products.csv` | 3 |
| `01-age-group-gender.csv` | 25,000 |
| `02-age-group-gender.csv` | 23,742 |

The columns are the same as the 5 Oct files: `Handle`, `Google Shopping / Age Group (product.metafields.mm-google-shopping.age_group)`, `Google Shopping / Gender (product.metafields.mm-google-shopping.gender)`. There is no Title column, so titles, prices, variants, images and descriptions aren't touched.

## How to import (Shopify admin)

1. **Test first.** Products, then **Import**. Choose `00-TEST-3-products.csv`, tick **"Overwrite products with matching handles"** and import.
2. Open one of the 3 products and check its Google Shopping fields show the new age group and `unisex`, and that the title, price, images and description are unchanged.
3. If that looks right, import `01` then `02` the same way, one at a time, with the same box ticked.

Rebuild with `tools/build_age_group_remaining.py` (reads `phase2_items.json`, `phase2_before.json` and `phase2_done.log` from `../../rollback/2026-10-05-google-fixes/`, and a bulk product export for the id to handle lookup).
