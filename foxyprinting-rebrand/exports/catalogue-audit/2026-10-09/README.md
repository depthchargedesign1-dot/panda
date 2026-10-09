# Full catalogue audit, 9 Oct 2026

Source: a full Shopify export at 13:00 UTC on 9 Oct, after all 7 queued CSV imports had finished. It covered 59,055 products (56,079 active) and 158,241 variants.
Checker: `tools/catalogue_audit.py` (read only). Every product with an issue is listed in `issues.csv.gz`; the counts are in `summary.md`.

## Already fine (no action)
- **SKUs.** Every variant has a SKU. 23 active products share a SKU with another product (mostly new Apparel); see the list.
- **Barcodes (GTIN).** None are needed. Everything is made to order, so Google gets `custom_product = true` ("no identifier exists") instead of a barcode, once the Google fields import below is done.
- **Vendor, product type and tags** are set on almost everything: 851, 1,914 and 36 active gaps respectively.
- **Gender and age group** are right on all but about 200 products, which the import below fixes.

## Fix 1: Google Shopping fields (biggest win). Owner to import
The Google fields files built on 2 Oct (`../../google-fields/01-04`) were never imported, so many products still carry old values:

| field | products to fix | what was wrong |
|---|---:|---|
| MPN | 46,721 | old supplier codes or junk such as "FSP-22135-A4 9893521928" instead of the SKU |
| Colour | 28,168 | blank or "Multi" |
| Google product category | 24,704 | blank, or a bare number such as "5194.0" |
| Custom product | 16,747 | blank or false; this tells Google there is no barcode |
| Condition | 11,057 | blank or "New" |
| Age group / gender | 202 / 115 | |

Files are in `../../google-fields/2026-10-09-full/`:
- `00-TEST-3-products.csv`: a signed print, a GameCube poster and a magnet. Import this first.
- `01` to `04-google-fields.csv`: 54,381 products in total.

They hold the Handle plus the 7 Google metafields only. There's no Title, Status or description column, so nothing else can be overwritten.
`no-google-category.csv` lists 123 products with no category to map from (e.g. gift tins, hidden option products).

## Fixed straight away (API)
- Removed a false "THESE MASKS ARE OFFICIALLY LICENSED TO FOXYPRINTING" line from 2 royal family 8-pack masks.

## Fix 2: description clean-up (copy project, by product family)
| issue (active) | count | worst families |
|---|---:|---|
| Old HTML (inline styles, spans, font sizes) | 23,407 | Baby Vest 2,004, Kids Cards 1,185, Gaming Cards 1,060, Movie Cards 876 |
| No H2 heading (old layout) | 27,330 | Baby Vest, Kids Cards, Holiday Stockings |
| Short (<60 words) | 14,858 | NES posters, magnets and keyrings |
| Word-for-word duplicates | 4,466 | Holiday Stockings 1,056, Coasters 622, SNES cases 548 |
| Empty | 49 | |
| "Limited Edition" on reproduction prints | 135 | "Football Posters" range ("A Limited Edition Print of your favourite footballer…") |
| "memorabilia" wording | 209 | signed athletics, darts and horror posters |
| Celebrity/sports disclaimer missing | 78 | Celebrity Facemask 69 |
| `[brackets]` left in text | 80 | |

Note: "hand-signed" (13,359) and "official merchandise" (278) are **not** problems. They appear in the disclaimers ("not hand-signed", "not official merchandise").
Mystery boxes say they contain "official licensed items". That is true for bought-in items, so it's left as is.

## Fix 3: SEO
3,521 active products have no SEO title and 3,458 no meta description. Almost all are retro gaming posters (NES 693, SNES 604, Sega 594, Saturn 244…).

## Needs the owner's decision
- **716 active products have no image.** Google rejects these, and shoppers can't see the product. Most are PS1 magnets (271), 3DO magnets (100), Mega CD posters (97) and Movie Cards (91). Set them to draft until there are images?
- **38,303 main images have no alt text.** This helps SEO and accessibility but not Merchant Center. It can be filled from the product title, but only per image through the API, which is slow. Do it range by range?
- 2,505 duplicate and near-duplicate listings from the 6 Oct Merchant Center report (`../../merchant-center/README.md`) are still open.
