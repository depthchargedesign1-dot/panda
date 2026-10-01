# Google Shopping age group and gender fix

These files set the Google Shopping **Age group** and **Gender** fields for every product that needs fixing. Built on 1 October 2026 from a full export of all 58,408 products.

- **Gender** is `unisex` on every product.
- **Age group** is `kids` or `adult`, set by `tools/age_group.py`:
  - **kids:** kids' cards, baby grows and baby clothing, kids' invites, christening items, school items, santa sacks and stockings, Christmas Eve boxes, and children's-character face masks (Bob the Builder, Peppa and so on).
  - **adult:** adult and rude cards, mugs, coasters, bar items, signed prints and posters, retro gaming cases, magnets and keyrings, celebrity and footballer masks.
  - Anything else is **kids** only if the title clearly says it's for a child ("kids", "boy", "girl", "baby", "5th birthday", "age 6"…). Otherwise it's **adult**.
- 1,861 products were already correct and aren't in the files. **56,547 products are updated** (50,196 adult, 6,351 kids).

| File | Products |
|---|---:|
| `00-TEST-3-products.csv` | 3 (one kids' card, one baby grow, one face mask) |
| `01-age-gender-update.csv` | 15,000 |
| `02-age-gender-update.csv` | 15,000 |
| `03-age-gender-update.csv` | 15,000 |
| `04-age-gender-update.csv` | 11,547 |

## How to import (Shopify admin)

1. **Test first.** Go to Products → **Import** and choose `00-TEST-3-products.csv`. Tick **"Overwrite products with matching handles"**, then import.
2. Open those 3 products and check that:
   - title, price, variants, images and description are all **unchanged**;
   - under **Metafields** (or the Google & YouTube section), Age group shows `kids` / `kids` / `adult` and Gender shows `unisex`.
3. If anything else changed, **stop** and tell Claude. If it all looks right, import `01` to `04` the same way, one at a time. Shopify emails you when each import finishes.

The files only hold **Handle, Title** (the current title, unchanged) and the two Google fields. Shopify's importer only updates the columns in the file, which is why the test with 3 products comes first.
