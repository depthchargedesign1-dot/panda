---
name: mug-lifestyle-shopify
description: Turn finished Foxy Printing mug artwork into a Shopify product on foxyprinting.co.uk - accurate mockups, AI lifestyle photos (Higgsfield) checked for correct print, image upload, product copy, SEO, tags and Google Shopping metafields. Use after mug-print-artwork, or whenever mug images/listings need making or refreshing.
---

# Mug lifestyle images + Foxy Printing (Shopify) listing

Store: Foxy Printing - foxyprinting.co.uk (Shopify connector, GBP). Admin handle `naughty-but-nice-mugs`.

## 1. Images (order matters - first is the featured image)
1. `mockup 0 both sides` - both faces on pure white (Amazon/eBay main image too)
2. `mockup 1 left side`, `mockup 2 right side`
3. Lifestyle 1 - kitchen / morning brew
4. Lifestyle 2 - matches the theme (office desk, football on the telly + scarf, gift wrap and card, Christmas)
5. Lifestyle 3 - in hand / gift box opening (optional)
6. `mockup 3 flat wrap`
Mockups come from mugkit (exact print, never AI). Upload them with `mcp__Higgsfield__media_upload` from the
same sandbox command that built them (see mug-print-artwork), `media_confirm`, use the cloudfront URLs.

## 2. Lifestyle photos (Higgsfield)
- Note `mcp__Higgsfield__balance` before and after.
- `generate_image_batch`, model `gpt_image_2_5`, 1:1, high quality, `use_unlim:false`, reference media =
  the matching mockup (role per `models_explore`). Prompt pattern:
  "Photorealistic product photo of the exact white 11oz ceramic mug from the reference, same printed design,
  same colours, same lettering, handle on the <left/right>, <scene>, soft natural light, shallow depth of
  field, no extra text, no logos, no people's faces." Personalised mugs: use the sample name only.
- Wait with `jobs_wait`, then CHECK every result: download it into the sandbox and look at it with
  `image_paths`. Reject any where the name/number/wording is misspelt, warped or invented, or where the
  shirt/art changed. Regenerate a rejected one once; if it fails again, drop it (mockups are enough).
- Only for marketing/ads do you use `marketing_studio_image`.

## 3. Shopify product (DRAFT unless Shaun says publish)
- `create-product`: title, descriptionHtml, vendor `Foxy Printing`, productType `Mugs`, status DRAFT,
  images in the order above with alt text, variants with SKU + price.
- Prices: match the current range (new 2026 mugs are GBP 7.99); personalised mugs 8.99 unless told otherwise.
  Say which price you used.
- Description structure (copy the number-plate mug house style): opening line with the joke/benefit ->
  `<h2>` feature line -> paragraph -> `<h3>Why you'll love it</h3>` 5 bullets -> `<h3>Size &amp; details</h3>`
  (white ceramic 11oz approx 325ml, C-handle, high gloss, sublimation printed in-house in North Yorkshire,
  dishwasher and microwave safe) -> `<h3>Personalisation</h3>` (what to type, printed exactly as typed) for
  personalised -> `<h3>Delivery</h3>` (printed to order in our North Yorkshire workshop).
- Tags: `11oz mug`, `foxy-new-2026`, `machine-sublimation`, `novelty mug`, range tag (`range-<slug>`),
  plus topic tags (`football-mugs`, `personalised-mugs`, `funny-mugs`, `gift for dad`, ...).
- SEO: `global.title_tag` "<Short name> | Foxy Printing" (<= 60 chars), `global.description_tag` <= 155.
- Google Shopping metafields (namespace `mm-google-shopping`, single_line_text_field unless noted):
  `custom_product` (boolean) true, `condition` new, `google_product_category`
  "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs", `gender` unisex, `age_group` adult,
  `color` White, `mpn` = first SKU.
- Category: look up the Shopify taxonomy id for Mugs once with GraphQL (`taxonomy` search "Mugs"), then
  `productUpdate(product:{id, category})`. Follow the GraphQL workflow (schema -> validate -> run).
- Personalised products: tag `personalised`, and make sure the theme's personalisation field (line item
  property) is enabled for the product. If you cannot see how the store collects names, ask Shaun once.

## 4. Report
Shopify admin link, price used, images (and which lifestyle shots were dropped), Higgsfield credits used.
