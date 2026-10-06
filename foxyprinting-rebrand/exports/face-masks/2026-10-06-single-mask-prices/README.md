# Single face masks: new options and prices (owner, 6 Oct 2026)

Every **single** mask (one mask: celebrity, character or YouTuber) gets the same two options and four prices. Packs, pairs, couples and multi-mask sets are left exactly as they are.

| Style | Fitting | Price | SKU ending |
|---|---|---|---|
| Ready Cut | Elastic | £2.99 | `-RC-E` |
| Ready Cut | Stick | £3.49 | `-RC-S` |
| DIY | Elastic | £1.50 | `-DIY-E` |
| DIY | Stick | £2.00 | `-DIY-S` |

- **Ready Cut:** cut to the face shape, with the eye holes cut.
- **DIY:** printed only. The customer cuts it out.
- **Elastic:** elastic and sticky tabs are supplied for the customer to attach.
- **Stick:** a stick and stickers are supplied for the customer to attach.

The SKU is the old SKU plus the ending, e.g. `FOXYFM3679` becomes `FOXYFM3679-RC-E`, and so on. All 26,940 new SKUs are unique and none clashes with an SKU already in the store. The facts are also in `plan/product-facts.md` (face mask sheet).

## What's changing

| | Products |
|---|---:|
| Single masks changed (4 variants each) | **6,735** |
| ...of which Active | 6,678 |
| ...of which Archived (they stay archived) | 57 |
| ...of which already had "Ready to Wear / DIY" (converted to the new four) | 7 |
| Borderline: **left unchanged**, see `borderline.csv` | 7 |
| Excluded: packs, couples, sets, multipacks, personalised photo packs, Style + Quantity, fabric face coverings, bulk/trade, KING CHARLES III + Crown | 326 |

Old prices on the changed masks: £2.49 (4,266), £2.50 (1,342), £3.00 (681), £2.95 (189), £1.99 (185), £4.99 (49 YouTuber/creator masks), £2.48 (16), and £2.99/£1.50 (7).

`classification.csv` lists all 7,068 mask products with the old price, the decision and the reason.

## Files

| File | Products | Rows |
|---|---:|---:|
| `import/00-TEST-3-masks.csv` | 3 | 12 |
| `import/01-single-masks.csv` | 2,000 | 8,000 |
| `import/02-single-masks.csv` | 2,000 | 8,000 |
| `import/03-single-masks.csv` | 2,000 | 8,000 |
| `import/04-single-masks.csv` | 732 | 2,928 |

Each file is well under Shopify's 15 MB limit (the largest is 1.5 MB). There are four rows per mask, one per variant. The first row carries the Title and the current Status. The file has no Body, SEO, tags or image columns, so descriptions, SEO, tags and photos are kept.

Weight: the old variant's weight is copied (100 g on most). 746 masks had no weight or 0 g, so their weight cell is blank and they'll show 0 g, as before.

Inventory: tracking is turned off (blank tracker) and the policy is "continue selling", so the masks never show as sold out.

## Order: import these LAST

Import these files **after** the SEO files (`exports/seo/2026-10-06-remaining/`) and the age-group files (`exports/google-fields/2026-10-06-age-group-remaining/`) have finished.

Those files still list 544 (SEO) and 1,093 (age group) of these masks with the old single "Title / Default Title" variant. If one of them is imported *after* this one, it could put the old variant back. For the same reason, don't re-import any older mask CSV with option or SKU columns once this is done.

## How to import (Shopify admin)

1. Go to **Products → Import**, choose `00-TEST-3-masks.csv` and tick **"Overwrite products with matching handles"**. Import it.
2. Check the 3 test masks on the **live product page** and in the admin:
   - Aaron Chalmers Face Mask (was £2.49)
   - Jake Paul Face Mask, the Boxer one (was £4.99)
   - Jack Joseph Face Mask (was Ready to Wear £2.99 / DIY £1.50)

   For each one, check:
   - there are **exactly 4 variants**: Style = Ready Cut / DIY, Fitting = Elastic / Stick;
   - the prices are **£2.99, £3.49, £1.50 and £2.00**, and the page shows "from £1.50" or £2.99 as the first choice;
   - there's **no leftover "Default Title" variant** at the old price (or an old "Ready to Wear" one on Jack Joseph);
   - the title, description, SEO, tags, images and status are unchanged;
   - you can add each variant to the cart.
3. **If a leftover "Default Title" (or "Ready to Wear") variant appears**, stop and tell Claude before importing the rest. Claude will remove the leftovers through the API.
4. If the test is right, import `01`, `02`, `03` and `04` one at a time, with the same box ticked. Wait for Shopify's "import complete" email before starting the next one.

### Will the old "Default Title" variant be removed?
Very probably, yes. With "Overwrite products with matching handles" ticked, the variants in the file become the product's variants, and old variants whose options aren't in the file are dropped. Shopify's help pages and community threads describe imports that change option values replacing (deleting) the existing variants. Shopify doesn't spell this out for every case, though, so the test import is how we confirm it.

## Things to know after the import

- **Google Merchant Center:** the old variant is replaced, so every mask gets new variant IDs, and four Google items in place of one (about 26,900 in place of 6,735). Expect a re-review and a few days of "pending" items. The product-level `mm-google-shopping.mpn` still holds the old SKU, so all four variants share it. Claude can set it to the `-RC-E` SKU through the API if you want.
- **Descriptions** (not changed now, counts only):
  - **6,735 of 6,735** single-mask descriptions don't mention the Stick option, so all would need a line about it.
  - 6,716 mention elastic, and 6,311 use the exact phrase "elastic and sticky tabs included".
  - **420** say or suggest the elastic or tabs are already on ("tabs are on the back", "tabs are fitted", "elastic attached" and similar). That goes against the rule that they're supplied for the customer to attach.
  - Only 17 mention DIY. Almost all describe a ready-cut mask with pre-cut eye holes, which isn't true for the DIY variant.
- New masks made with the `celebrity-face-mask-listing` skill should use the same Style/Fitting options and prices from now on.

## Rebuild
`MASK_DATA=<folder> python3 build.py`, then `python3 validate.py`. The folder must hold:
- `m.jsonl`: the bulk export of mask products and variants;
- `weights*.jsonl`: a bulk export of every store variant's id, SKU and weight.

`classify.py` holds the single/pack rules.
