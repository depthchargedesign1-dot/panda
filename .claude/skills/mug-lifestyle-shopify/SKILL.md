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
**Owner's rule (8 Oct 2026): "Please dont use cad images always use real images with print on".** Every product
image must be a REAL PHOTO of the actual product (our own photos, the store's real product photos, Shaun's Dropbox
photos/PSD mockups such as `/RANDOM IMAGES LEFT ON/MUG BLANK.jpg`, or the supplier's real packshot of the blank) with
the artwork placed on it realistically (perspective, curve/wrap, lighting, texture). Never use flat/drawn/vector
"CAD" mockups (mugkit's drawn mug, flat plates, plain shapes) as product images; they are for proofs only. If there
is no real photo of the blank, ask Shaun for one instead of drawing it. Live-preview bases should be real photos too
where possible.
Proof mockups come from mugkit (exact print, never AI) - use them to check the print, not as listing images. Upload them with `mcp__Higgsfield__media_upload` from the
same sandbox command that built them (see mug-print-artwork), `media_confirm`, use the cloudfront URLs.

## 2. Lifestyle photos (Higgsfield)
- Note `mcp__Higgsfield__balance` before and after.
- **Fallback - ChatGPT (Shaun's rule):** if Higgsfield is out of credits, disconnected or failing, use ChatGPT /
  OpenAI image generation instead (same prompt, mockup as the reference image, same print check). That needs an
  OpenAI connector or `OPENAI_API_KEY` in the environment settings with `api.openai.com` allowed in the network
  settings. If neither is set up, tell Shaun, upload the exact mockups, and mark the lifestyle shot as still to do.
  Never ship a lifestyle photo whose print doesn't match the artwork.
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
