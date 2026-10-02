# Honest titles for reproduction "signed" prints (refreshed 2 Oct 2026)

**13,434 poster and print listings** describe a printed signature as "Signed" or "Autographed". The owner approved fixing all of them on 2 Oct 2026. New titles come from `tools/signed_titles.py`, which:
- removes the product type pasted at the start ("Signed Footballer Posters …");
- changes "Signed / Autographed / Hand-Signed" to **"Printed Signature"**, keeping only the first one;
- removes "Limited Edition", "Official", "Authentic", "Genuine", "Collectible" and "Merchandise", and changes "Memorabilia" or "Merch" to "Wall Art";
- removes repeated segments;
- adds **"– Reproduction Print"**.

Example: `ROCKY MARCIANO Limited Edition Boxer Signed Print - Boxing` becomes `ROCKY MARCIANO Boxer Printed Signature Print – Boxing – Reproduction Print`.

Left alone: Sport Cards (44) and Lego display cases (19), which aren't prints. Handles (URLs) don't change, so links and Google history are kept. `before-after-review.csv` lists every old and new title.

## Already done through the API
- 3 test products.
- The 134 products whose SEO title or meta description also said "signed".
- The 20 collection names (e.g. "Signed Footballer Posters" is now "Footballer Printed Signature Posters"). Collection handles are unchanged.

The bulk API route is blocked by the Shopify connector's safety policy, so the remaining titles go through a CSV import.

## Import (owner, about 5 minutes)
1. Shopify admin → Products → Import → `00-TEST-3-products.csv`, with **"Overwrite products with matching handles"** ticked.
2. Open those 3 products and check that only the title changed.
3. Import `01-signed-titles.csv` (6,714 products), then `02-signed-titles.csv` (6,714 products).

The Foxy Pop theme also shows a "printed reproduction, not hand-signed" notice on every one of these product pages automatically.
