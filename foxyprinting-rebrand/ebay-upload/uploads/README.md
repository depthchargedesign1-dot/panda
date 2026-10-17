# eBay upload files

Upload each file in Seller Hub > Reports > Uploads > **Upload template**. Wait for the results file, and download it to see any rows eBay rejected.

**Do `../shop/SHOP-SETUP.md` first.** The files point at the business policies `FOXY Royal Mail 24`, `FOXY 30 Day Returns` and `FOXY Payment` by name.

| Order | File | What | Listings / rows |
|---|---|---|---|
| 1 | `M-A-01-personalised-photo-masks.csv` | 7 personalised photo masks (stag, hen, birthday, wedding, leaving do, office party, your own face). Personalise box on, 3 styles x 15 pack sizes, £3.99 for 1 mask up to the website's pack prices | 7 / 322 |
| 2 | `M-TEST-50-celebrity-masks.csv` | The 50-mask test: the best-selling celebrity masks of the last 12 months (real people only, no Disney, Muppets or Star Wars characters). Ready Cut / DIY x Elastic / Stick at £2.99 / £3.49 / £1.50 / £2.00, or one price for packs | 50 / 226 |

Every file has:
- Category `116724` (Costume Masks & Eye Masks).
  - I read this number off eBay UK's own category page addresses but couldn't open eBay from here, so check it.
  - If the upload report says the category is wrong: Seller Hub > Create listing > type "celebrity face mask" > note the category number > tell me, and I rebuild in a minute.
- Quantity 3 on every variation, fixed price, Good 'Til Cancelled, condition New.
- Item specifics: Brand Foxy Printing, Type Face Mask, Material Card, Size One Size, Department Adults, Made in United Kingdom.
- Up to 12 pictures from Shopify, and the branded description template.

`*.sku-map.csv`: eBay's Custom label (SKU) is limited to 50 characters, so 76 of the long celebrity mask SKUs were shortened. This file pairs each eBay SKU with its Shopify SKU, so you can still find the right product when an order comes in.

`*.report.txt`: every title that was changed for eBay (80-character limit, shop codes like "LF1" removed).

**Watching the test (2–3 weeks):** look out for eBay messages saying a listing was removed (VeRO / intellectual property, or the faces/names policy).
- None removed: I'll build the rest of the celebrity masks in files of 500, best sellers first.
- One or two removed: drop those names and carry on.
- Several removed, or an account warning: stop. Celebrity masks stay on Shopify only.

Rebuild a file (e.g. after a price or category change):

    python3 -I tools/ebay_csv.py source/masks-first-81.jsonl lists/1b-masks-test-batch-top50.csv uploads/M-TEST-50-celebrity-masks.csv --config config/masks-celebrity.json
    python3 -I tools/ebay_csv.py source/masks-first-81.jsonl lists/1-masks.csv uploads/M-A-01-personalised-photo-masks.csv --config config/masks-personalised.json --tier A
