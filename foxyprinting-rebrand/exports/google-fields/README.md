# Google Shopping fields fix (all 7 fields)

Built on 2 October 2026 from a full export of all 58,741 products. **This replaces the old `google-age-gender` files.** Those were never imported, so don't use them.

## What the check found

| Field | Wrong or missing | Fix |
|---|---:|---|
| Age group | 56,477 | `kids` or `adult` from `tools/age_group.py`. 32k said `kids` on adult items such as posters; others said `Unisex`, `newborn`, `Adults` or were blank. |
| Google product category | 25,371 | Mapped from each product's (fixed) Shopify category using Shopify's official Shopify→Google mapping. It replaced blanks, bare number codes ("5194.0") and invalid paths. Baby grows go to *Baby One-Pieces*. |
| MPN | 58,107 | Set to the product's own SKU. Most still had old supplier codes. |
| Colour | 29,830 | Blanks and "Multi", "multicolour" and similar became `Multicolor`. Real colours are capitalised. |
| Custom product | 17,801 | `true` on everything: it's all made to order, with no barcode. |
| Condition | 11,036 | `new`. Some were blank or "New". |
| Gender | 10,803 | `unisex`. Some were blank or "Unisex". |

Of all products, 58,310 need at least one change. The other 62 have no category at all, such as gift sets and hidden option products, and are listed in `no-google-category.csv`.

## How to import (Shopify admin)

1. **Test first.** Go to Products → **Import**, choose `00-TEST-3-products.csv`, tick **"Overwrite products with matching handles"** and import. The test file has a baby grow, a printed signature print and a face mask.
2. Open those 3 products. Check that the title, price, variants, images and description are **unchanged**, and that the Google fields show the new values.
3. If that looks right, import `01` to `04` the same way, one at a time.

The files only hold Handle and the 7 Google fields. There's no Title column, so titles fixed since the export (e.g. the signed prints) can't be overwritten.
