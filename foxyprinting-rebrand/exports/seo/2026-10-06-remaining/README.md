# SEO titles + meta descriptions – the remaining 38,690 products (6 Oct 2026)

The first 8,160 products of the 46,850-product SEO update were pushed straight to the store by API.
These files hold the other **38,690** (the same checked text, with the 641 quality fixes from 5 Oct already applied).
Pushing them one by one would use the owner's Claude usage allowance many times over, so they're an import instead
(CLAUDE.md: CSV for very large sets).

## Import
1. Shopify admin → Products → Import → upload `00-TEST-3-products.csv`, tick **Overwrite products with matching handles**, import.
2. Open one of the 3 products → "Search engine listing" should show the new title and description.
3. Import `01-seo.csv`, then `02-seo.csv`.

Columns: Handle, SEO Title, SEO Description (same format as the 4 Oct files). Other product fields are left unchanged.
Supersedes the 4 Oct `0[1-6]-seo.csv` files for these products – don't import those.
