# Amazon UK test upload (6 Oct 2026)

This is a test with 3 products. If it works, the same script builds the Amazon files for every new product.

| Amazon parent SKU | Product | Variations (child SKUs) | Price | Personalisation (Amazon Custom) |
|---|---|---|---|---|
| `FOXY-SUB-FNPMBUBU` | Funny Number Plate Mug, BR3W UP (Brew Up) | 5 country bands: GB, Scotland, Wales, Northern Ireland, Ireland (`-01`…`-05`) | £7.99 | None. It's a fixed design, so don't switch on Amazon Custom. |
| `FOXY-DTF-PBH` | Personalised bobble hat with your logo | 8 colours (`FOXY-DTF-PBH-01`…`-08`) | £8.50 | Badge/logo upload (required) and a message for us (optional) |
| `FOXY-FLAG-CFLAG02` | Personalised England terrace flag (St George cross) | 3 sizes: 3ft x 2ft £19.99, 5ft x 3ft £34.99, 8ft x 5ft £59.99 | as listed | Text on the flag (required), second line, logo upload and a message for us (all optional) |

On Shopify the 8 hat colours are 8 separate products. On Amazon they are grouped as **one parent with 8 colour children**, which is how Amazon wants colours shown.

## Files

| File | What it is |
|---|---|
| `amazon-test-upload.xlsx` | **Use this one.** The *Listings* sheet has 19 rows (3 parents and 16 children) under Amazon's flat-file column names. The other sheets are *Customisation* (the Amazon Custom spec), *Column guide* (how each of our columns maps to the label in Amazon's new template) and *ASK* (what you still need to fill in). Cells still marked **ASK** are yellow. |
| `amazon-test-upload.csv` | The Listings sheet as a CSV, for reading or copying. Amazon does **not** accept CSV uploads (see below). |
| `amazon-customisation-spec.csv` | Every Amazon Custom field per product: type, label, hint, max characters, required yes/no, surcharge £0. |
| `build-report.txt` | The script's checks: title rules, bullet lengths, and every value still marked ASK. |
| `shopify-source.json` | The Shopify data this was built from (titles, descriptions, prices, SKUs, options, images, weights, `foxy.personalise_fields`), read from the store on 6 Oct 2026. |
| `amazon-config.json` | Test settings: product groups, Amazon product types, the hat's group title and colour names, extra search words. |

### What's in each row
- **SKU**: `item_sku` is the Shopify SKU. A parent's SKU is the child SKU without the final `-NN`. I didn't add an `AMZ-` prefix. If Amazon says a SKU is already in use on your account, re-run the script with `--sku-prefix AMZ-`.
- **Title** starts with the brand and contains no promo words ("best", "sale", "free delivery", "fast turnaround" and so on) and none of the banned symbols `! $ ? _ { } ^ ¬ ¦`. No word appears more than twice. Titles are 200 characters or fewer, and the hats are kept under 125 because some apparel categories have that lower limit. The flag title uses only the country, so no club or other third-party names appear anywhere.
- **5 bullet points**, each under 250 characters, and a plain-text **description** of 2,000 characters or fewer. Both are written from the Shopify copy, with the website-only parts taken out: live preview, basket/checkout, multi-buy offers, phone numbers, "contact us", delivery promises and cross-selling lines. Amazon doesn't allow these, and they wouldn't make sense there. The personalisation sentence is rewritten for Amazon's **Customise now** button. Each hat colour keeps its own description from its own Shopify page.
- **Search terms** (`generic_keywords`) come from the Shopify tags plus a few extra words. They stay under Amazon's 249-byte limit, skip words already in the title, and include the US spelling "personalized".
- **Images**: main and other image URLs come straight from cdn.shopify.com. Each mug country has its own band photo as its main image. Each hat colour has its own photo, which is also its swatch.
- **Price** is from Shopify. **Quantity** is 20 per child, a working figure because everything is made to order. **Condition** is New. **Weight**: hats 85 g (from the fact sheet). Mugs and flags are ASK because Shopify has 0 g for them.
- **Variations**: the mug's countries use Amazon's **Style** theme, because Amazon has no "Country" theme. The hats use **Color** and the flag uses **Size**.

## Steps for you

### (a) Download Amazon's official templates
1. Go to Seller Central > **Catalogue > Add Products via Upload** (in some accounts: Catalogue > Add products > *Spreadsheet* tab) > **Download spreadsheet / Generate template**.
2. Search for and add the product types for **mugs**, **hats** and **flags**. My guesses at Amazon's names are `DRINKING_CUP`, `HAT` and `FLAG`, but **check them**: type "mug", "beanie hat" and "flag" into the product-type search and use what Amazon offers. If a name differs, change `feed_product_type` in the config and re-run the script. You can put up to 20 product types in one template.
3. Choose **Marketplace: Amazon.co.uk**, **language English (UK)** and the **Custom** or **Advanced** template, not *Lite*, so the variation, handling-time and image columns are all there. Download the .xlsm.

### (b) Copy our rows into it
Amazon only accepts its own template (.xlsm/.xlsx) or a tab-delimited .txt. It doesn't accept a CSV or a sheet it didn't generate. The new templates also hide internal header rows, so **our file can't be uploaded as it stands**. Copy each column across instead:
1. Open our `amazon-test-upload.xlsx` and the template side by side.
2. Use the *Column guide* sheet to match our column names (for example `item_name`, `parent_child`, `bullet_point1`) to the template's labels (for example *Item Name*, *Parentage Level*, *Bullet Point*). Paste values only (Paste Special > Values), starting on the template's first data row.
3. Fill every yellow **ASK** cell (see the list below). For drop-down columns (Variation Theme, Colour Map, Target Gender, Condition, Product Type), pick the matching value from the template's own drop-down so the spelling is exactly what Amazon expects.
4. Leave *External Product ID* and its type **blank**. That only works once the GTIN exemption is approved (see below).
5. Upload: **Catalogue > Add Products via Upload > Upload your spreadsheet**, choose the file, and tick *Check my file* first if it's offered. Wait for the processing report and download it.

### (c) Set up Amazon Custom (personalisation) for each listing
This **can't be done from the listings file**. See "What Amazon Custom can and can't do in bulk" below. Once the hat and flag listings are live (they each have an ASIN):
1. Register for **Amazon Custom** if you haven't yet. It needs a Professional selling account.
2. Go to **Inventory > Manage All Inventory > Custom products** tab (it may be labelled *Manage Custom Products*), then click **Enable customisation** next to the first hat child ASIN.
3. Add one **surface** using the hat photo, then add the fields in the order shown in `amazon-customisation-spec.csv`:
   - Hat: **Image** "Badge or logo upload" (required; draw the placement box on the cuff); **Text** "Message for us", hint "e.g. how many hats, team order details", 160 characters, optional.
   - Flag: **Text** "Text on the flag", hint "name, group or town", 24 characters, required; **Text** "Second line", 24, optional; **Image** "Logo upload", optional; **Text** "Message for us", 160, optional.
   - Set the price surcharge to £0 on every field. The variations (colour, size, country) are **not** Amazon Custom fields: customers pick them on the product page, and each has its own price.
4. Save it, then copy it to the other 7 hat colours and the other 2 flag sizes. Either use the copy option on that page, or use the **bulk customisation tool**: build the first ASIN, generate Amazon's Excel template from it, list the other ASINs, and upload.
5. The character limits match the website (24 for a line of text, 160 for a message). Amazon applies one overall limit per text box, not a per-line limit.

### (d) What to check after the test upload
- The processing report shows **0 errors** for all 19 rows. Common errors are a missing required attribute for that product type, an invalid drop-down value, a missing GTIN or exemption, or a brand not approved.
- In **Manage All Inventory**, each parent shows its children: 5 mug countries, 8 hat colours and 3 flag sizes, all grouped under one listing, with the right price on each child.
- Open each product page on amazon.co.uk: the title, the 5 bullets and the description read properly and there's no website-only wording left. The main image shows on a white background, and each colour or country shows its own photo.
- The main image must be on a **pure white background with no text**. I checked the mug photos: they are white, 2048 x 2048. **I couldn't check the hat and flag photos** because Shopify's CDN is blocked from here. If any of them has a coloured background or text, Amazon may suppress the listing. Swap in a white-background shot.
- On a hat and on a flag, **Customise now** appears, the logo upload works, the text boxes stop at the right length, and the preview looks right. Place a test order (then cancel it) and check that the customer's text and uploaded image appear in the order's customisation details.
- Check the delivery promise on the page matches your real dispatch time, because Amazon now measures this (see below).

## Still to fill in (ASK)
| What | Where | Notes |
|---|---|---|
| **Brand name registered?** | `brand_name` (currently "Foxy Printing") | Is "Foxy Printing" in Amazon **Brand Registry** (it needs a registered UK trademark)? If it isn't, it can still be used as a brand once the GTIN exemption for that brand is approved. Whatever you use, it must match the exemption application exactly. |
| **GTIN exemption** | `external_product_id` left blank | We have no barcodes. Apply in Seller Central (search help for "GTIN exemption") for brand "Foxy Printing", in the mug, hat and flag categories, with photos showing the product and its branding. Do this **before** uploading. |
| **Amazon category (browse node)** | `recommended_browse_nodes` | Take the node IDs from the template's browse data or the product-type picker for each product. |
| **Handling time** | `fulfillment_latency` | Days from order to dispatch, for each child. See the 2026 handling-time note below. |
| **Shipping template name** | `merchant_shipping_group_name` | The exact name of your shipping template (Settings > Shipping settings). Leave blank to use the default. |
| Product weights | `item_weight` | Mug and each flag size. Shopify has 0 g for these. |
| Country of origin | `country_of_origin` | Where the blank is made (mug, hat, flag fabric). |
| Product type names | `feed_product_type` | Confirm `DRINKING_CUP` / `HAT` / `FLAG` in the template generator (see step a). |

## What Amazon Custom can and can't do in bulk
- **The listings file doesn't carry personalisation fields.** Category templates create the product, its variations, price and stock, but not text boxes or upload fields. I found no "customisation" columns in any template documentation. Personalisation is switched on for each ASIN in Seller Central, after the listing exists.
- **Amazon Custom fields** can be: **text** (you set the label, the character limit and which characters are allowed, such as letters, numbers, capitals and emoji; there is one overall limit per box, not per line), **image upload** (the customer uploads their own picture and you set where it goes on the product), and **options** (drop-downs or swatches). Each field can be required or optional and can carry a surcharge. You get up to 5 surfaces per product, with up to 10 text or image fields and up to 100 option fields per surface.
- **Bulk is possible, but only from inside Amazon Custom.** Amazon's **bulk customisation tool** works like this: you build the customisation on one *base* ASIN, Amazon generates an Excel template from it, you list the other ASINs (and edits) in that template, and you upload it. It covers text, image and option fields and all surfaces. So the hats can be done once and applied to all 8 colours. Our `amazon-customisation-spec.csv` is the plan for that base ASIN, but it is **not** Amazon's bulk-customisation file, because that file is generated by Amazon from your base ASIN.
- Customer entries arrive with each order as **customisation details**, including the uploaded image file.

## Handling time and made-to-order (Amazon UK, 2026)
- From **15 July 2026**, the account-wide default handling time in the UK can only be 0 or 1 day. **Set a longer handling time on each SKU** in the `fulfillment_latency` column.
- From **1 September 2026**, if a SKU's handling time is a day or more longer than how fast you actually dispatch, for more than 30 days, Amazon turns on **Automated Handling Time** and shortens it for you. Made-to-order, custom and handmade items can ask for a **Handling Time Exception**.

## GTIN exemption, Brand Registry and "custom product" flags
- Handmade, made-to-order and custom products are among the cases that qualify for a GTIN exemption. You apply with the brand name exactly as it will appear on the listings, the category, and photos of the product (renders aren't accepted, and the branding should be visible).
- Brand Registry needs a registered trademark. Without it you can still list under your brand once the exemption is approved. Some categories also allow "Generic" as the brand. Amazon support error code 5665 is the route if the brand isn't eligible for Brand Registry.
- The **personalised** flag on Amazon comes from enabling **Amazon Custom** on the ASIN, not from a column in the listings file. Amazon Custom needs a Professional account; Brand Registry isn't listed as a requirement.
- **Amazon Handmade** is a separate programme with its own application. It isn't used here, because printed blanks are unlikely to qualify.

## Pairing ideas for Amazon (offer to list next)
- The other 9 number-plate mugs (same file layout) and a tea-lover bundle.
- A personalised football scarf or B10 cap to go with the hats (same Amazon Custom logo upload).
- The rest of the country terrace flags (Scotland, Wales, Union Jack and so on, still with no club names), plus car flags and bunting.

## Re-running or exporting new products
```bash
cd foxyprinting-rebrand
python3 tools/amazon_export.py --print-query            # GraphQL to run through the Shopify MCP with {"ids": [...]}
# save the raw response as exports/amazon/<date>/shopify-source.json, then:
python3 tools/amazon_export.py --source exports/amazon/<date>/shopify-source.json \
    --config exports/amazon/<date>/amazon-config.json --out exports/amazon/<date> --name amazon-upload
```
Without `--config`, each Shopify product becomes its own Amazon parent and its Shopify options become the variations. Use a config to group separate Shopify products (like the hat colours) or to set Amazon-only values. `--fetch ID ...` pulls the data directly when `SHOPIFY_SHOP` and `SHOPIFY_ADMIN_TOKEN` are set. Third-party-name products keep their Shopify disclaimer at the end of the Amazon description, and the script flags any that don't have one.

## Shopify issues found while building this (not changed)
- The hats' shipping weight on Shopify is **0.2 g** (it should be about 85 g). The mug and flag weights are **0 g**. This also affects Shopify's own postage rates.
- The live hats have only **2** personalisation fields (badge/logo upload, message), but `exports/bobble-hats/payload.json` planned 4 (it also had "Club or business name (optional)" and "Text to print under the design (optional)"). If you want those 2 extra boxes, add them to `foxy.personalise_fields` and re-run. They'll become two optional Amazon Custom text fields.

## Sources (researched 6 Oct 2026; Seller Central, sell.amazon.co.uk and Amazon's developer docs are blocked from this machine, so these come from search results and seller-forum summaries)
- Variations, parent/child, relationship type and variation theme, plus themes being retired in late 2025: [My Amazon Guy](https://myamazonguy.com/parentage/how-to-add-products-into-an-existing-parentage-via-template-on-amazon-seller-central/), [Seller Central help 581](https://sellercentral-europe.amazon.com/gp/help/external/581), [Jungle Scout](https://www.junglescout.com/blog/amazon-product-listing-variations/)
- Templates (Lite, Advanced, Custom; up to 20 product types; .xlsm or .txt only): [Inventory file templates, Seller Central help G1641](https://sellercentral-europe.amazon.com/gp/help/external/G1641), [SellerEngine: Lite templates](https://sellerengine.com/lite-templates-go-live/), [Channable: required attributes](https://helpcenter.channable.com/hc/en-us/articles/360014280220)
- Flat-file column names (item_sku, feed_product_type, bullet_point1–5, generic_keywords 250 bytes): [amalyze flat-file guide](https://amalyze.com/resources/guides/listing/amazon-listing-flat-file-upload), [StoreAutomator](https://support.storeautomator.com/hc/en-us/articles/4411195600146-Flat-File-Templates-for-Amazon)
- Title rules from 21 Jan 2025 (200 characters, banned symbols, no word more than twice, no promo phrases): [Seller forum announcement](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/3781c84d-4778-40fe-9dde-30039a0948f6), [Search Engine Land](https://searchengineland.com/?p=450485), [SPS Commerce](https://www.spscommerce.com/community/articles/new-amazon-product-title-requirements-2025)
- Amazon Custom (text, image and option fields; required flag; 5 surfaces / 10 / 100; enabling per ASIN): [Seller forum: Amazon Custom guide](https://sellercentral.amazon.com/seller-forums/discussions/t/cbfc0ba4-dbfe-427b-9a34-eb3c98bea254), [Ecomclips](https://ecomclips.com/blog/how-to-do-an-image-customization-on-amazon-using-clipping-mask-sell-personalize-product-on-amazon/), [amalytix](https://www.amalytix.com/en/glossary/amazon-custom/); one overall character limit per text box: [Seller forum (CA)](https://sellercentral.amazon.ca/seller-forums/discussions/t/128c9dbe-6161-465f-bdcd-414b056b3e13)
- Amazon Custom bulk customisation tool (base ASIN, then a generated Excel template, then upload): [Seller forum: Amazon Custom new bulk listing tool](https://sellercentral.amazon.com/seller-forums/discussions/t/9995c0100b477446c929fd5091dec19d), [EU forum version](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/1a2ab4827818741100e2a74aa4a50849), [Amazon Handmade bulk customisation](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/786134dcf9ecc29118a6f707a16659c2)
- Amazon Custom eligibility (Professional account): [sell.amazon.co.uk: Amazon Custom](https://sell.amazon.co.uk/programmes/custom-products)
- GTIN exemption and Brand Registry: [Seller forum: GTIN exemption for items I make](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/aa6f17fb7b4bd15cd8855dc644a1f75a), [amalyze GTIN exemption](https://amalyze.com/resources/guides/listing/amazon-listing-gtin-exemption), [Jungle Scout](https://www.junglescout.com/resources/articles/gtin-exemption-amazon/), [Streamoid](https://streamoid.com/resources/guide/amazon-gtin-exemption-guide)
- UK handling time changes in 2026: [ChannelX, Jul 2026](https://channelx.world/2026/07/3-updates-to-amazon-uk-fbm-requirements/), [ChannelX, Jun 2026](https://channelx.world/2026/06/amazon-uk-update-fbm-requirements/), [Seller forum (UK)](https://sellercentral.amazon.co.uk/seller-forums/discussions/t/20198e40-521c-4a27-b682-3f088fa0a7dc)
