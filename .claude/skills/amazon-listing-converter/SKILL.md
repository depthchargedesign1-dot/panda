---
name: amazon-listing-converter
description: Convert Foxy Printing (Shopify) products into a safe Amazon UK upload pack - variations (parent/child), personalisation as Amazon Custom text boxes (name, number, age...), GTIN/EAN handling, policy-safe titles and descriptions, IP/celebrity hold-back, a review workbook, Amazon's own category template filled in, and a JSON_LISTINGS_FEED for the SP-API / Amazon Selling Partner connector. Use for "put these on Amazon", "Amazon upload file", "list Shopify products on Amazon".
---

# Shopify (foxyprinting.co.uk) -> Amazon UK

Script: `scripts/shopify_to_amazon.py`, settings: `scripts/amazon_config.json`, test:
`python3 tests/test_converter.py`. **Nothing is ever sent to Amazon by the script.**

## 1. Get the products out of Shopify
- Shaun can export: Shopify Admin > Products > Export (CSV) -> pass the CSV.
- Or you fetch them with the Shopify connector (GraphQL workflow: schema -> validate -> query), 50 per page,
  and save every page's `nodes` into one JSON file:
  ```graphql
  query($q:String!,$after:String){ products(first:50, query:$q, after:$after){ pageInfo{hasNextPage endCursor}
    nodes{ id handle title status vendor productType tags descriptionHtml options{name values}
      media(first:9){nodes{... on MediaImage{image{url altText}}}}
      variants(first:100){nodes{sku price barcode selectedOptions{name value}
        media(first:1){nodes{... on MediaImage{image{url}}}}}} } } }
  ```
  Filter with `$q`, e.g. `product_type:Mugs status:active`, `tag:foxy-new-2026`, `title:*personalised*`.

## 2. Convert
`python3 scripts/shopify_to_amazon.py products.json --out "Amazon upload <date>"`
(add `--template <Amazon category template .xlsm>` once Shaun has downloaded it; `--only-personalised` to
do just the name products). Show Shaun the summary: rows, parents, personalised SKUs, held back, checks.

What it does:
- **Variations**: products with options become a PARENT (`<SKU stem>-PARENT`, no price) + CHILD per variant.
  Option names map to themes in `variation_themes` (Colour/Colourway -> COLOR, Size -> SIZE,
  Country/Style/Design -> STYLE). Child SKUs = Shopify SKUs, so stock/price tools can link them.
- **Personalisation**: detected from Shopify tags (`AgeNameMessage`, `Add Any Name`, `Any Name`,
  `Add Any Number`, `Add Name On Back`, `Add Month & Year`, `Add Song`, ...), titles ("Personalised",
  "name & number") and old description wording ("please supply us with your name"). Each personalised SKU
  gets a template (e.g. `FOXY - Name + Number`) with field labels, character limits and customer
  instructions (sheet "Custom templates"), the bullets/description tell buyers to use "Customise now",
  fulfilment is merchant (Amazon Custom can't use FBA) and handling time is 3 days.
- **Safety**: held back (sheet "Held back") = drafts, missing/duplicate SKUs, no price, no image, no
  product-type mapping, and anything matching trademark/celebrity terms or tags (`ip_hold_terms`,
  `*Fan` tags, Celebrity tags). Emails, phone numbers, URLs and "contact us / many more in our store" lines
  are stripped (Amazon bans them). Titles lose banned characters and are capped at 200; keywords <= 249 bytes,
  internal tags never leak. Valid EANs are used; otherwise GTIN exemption is declared (Shaun needs an
  approved GTIN exemption for brand "Foxy Printing", or Brand Registry).

## 3. Upload safely (in this order)
1. Shaun reviews the workbook (Listings / Held back / Checks).
2. **Amazon's own template (recommended without API)**: Seller Central > Catalogue > Add products via
   upload > choose product type (confirm `DRINKING_CUP` for mugs, `SHIRT` for tees) > download, re-run with
   `--template`, upload the FILLED file, read Amazon's processing report.
3. **With the Amazon Selling Partner connector** (claude.ai connector "Amazon Selling Partner") or SP-API:
   for each message in the JSON feed call the Listings Items API with `mode=VALIDATION_PREVIEW`, fix all
   issues, then submit for real; or send the whole feed (`JSON_LISTINGS_FEED`) through the Feeds API.
   Put the seller ID in `seller_id`. Never submit without a validation pass and Shaun's go-ahead.
4. **Amazon Custom** (the name box) after the ASINs exist: enrol in Amazon Custom (Professional account),
   build each template once on one SKU (Edit > Customisation information > Text input per field, fixed font
   and colour, limits from the sheet), then apply it to the rest with Amazon's bulk customisation tool using
   `Amazon Custom mapping - <date>.txt`. The listing file/API cannot create the customisation template itself.
5. Test-buy one personalised listing; the buyer's text arrives in the order customisation file
   (Orders API `BuyerCustomizedInfo`), which is what production prints (mugkit `--set Name=...`).

## Connecting to Amazon directly (SP-API) - `scripts/spapi.py`
One-time setup (Shaun):
1. Finish the developer profile (security answers from the Dropbox "Amazon-SP-API-Security-Pack").
   Ask for a **private developer** (own account only) with roles Product Listing, Pricing, Inventory and
   Order Tracking, Amazon Fulfilment (add Buyer Communication later if needed).
2. When approved: Seller Central > Apps and Services > Develop apps > Add new app client (SP-API) >
   then "Authorise" it (self-authorisation) to get the refresh token. Note the LWA client id + secret.
3. Put them in the cloud environment settings as environment variables, never in chat or files:
   `SPAPI_CLIENT_ID`, `SPAPI_CLIENT_SECRET`, `SPAPI_REFRESH_TOKEN`, `SPAPI_SELLER_ID`.
4. Network access: allow `api.amazon.com`, `sellingpartnerapi-eu.amazon.com` and the feed-document host
   `tortuga-prod-eu.s3-eu-west-1.amazonaws.com` (or use the Higgsfield sandbox, which has internet).
Use (always in this order):
- `python3 scripts/spapi.py check` - proves the connection; must show amazon.co.uk `uk_ready: true`.
- `python3 scripts/spapi.py search-types mug` and `product-type DRINKING_CUP` - confirm the product type,
  required attributes and allowed variation themes; fix `amazon_config.json` if they differ.
- `python3 scripts/spapi.py validate "<JSON_LISTINGS_FEED>.json"` - Amazon checks every SKU, nothing changes.
- Only after Shaun says go: `submit "<feed>.json" --confirm` (refuses if validation is missing, has errors,
  is over 24h old or the feed changed), then `feed-status <feedId>` for the processing report.
Tests: `python3 tests/test_spapi.py` (mock Amazon, no network).

## Settings worth checking with Shaun (amazon_config.json)
`price_rule` (same / plus:1.00 / markup:15 - Amazon fees are higher than Shopify), `quantity`
(made-to-order stock), `handling_days`, `product_types` (add posters, masks, flags... only after checking
the Amazon product type), `ip_allow_skus` (only for licensed items).
