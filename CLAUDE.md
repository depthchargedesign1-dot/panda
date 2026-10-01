# Foxy Printing (foxyprinting.co.uk): working rules

The Foxy Printing work lives in `foxyprinting-rebrand/`. The rest of this repository is an unrelated pandas checkout, so don't touch it.

## Creating products: ALWAYS follow these rules

1. **Every new product is created as a DRAFT** (`status: DRAFT`). Never set a product to Active or publish it to a sales channel unless the owner explicitly says so for that specific product or batch. This applies to every route: `productSet`, `productCreate`, `create-product` and CSV imports.
2. **Every new product gets a detailed, human-sounding, SEO description** written from its keywords and tags (see "Product copy" below). Never leave the description empty, and never paste the same text across products.
3. Set the **SEO title and meta description** (`seo { title description }`) on every product.
4. Set the **Google Shopping fields** (see below) so the product is ready for Google Ads / Merchant Center.
5. Set **Product type**, **vendor "Foxy Printing"**, sensible **tags**, and a unique **SKU** on every variant (`FOXY-<machine>-<initials>-NN`, see `foxyprinting-rebrand/tools/build_plan.py`).
6. Personalised products: use template suffix `personalised` (cards: `card`). Set metafields `foxy.mockup` and `foxy.personalise_fields` so the live preview works.
7. Image alt text should describe the product in plain words and include the main keyword once.
8. Before creating, search the store for an existing product with the same handle or title to avoid duplicates.

## Product copy (description) guidelines

Write like a friendly UK shop owner who makes the product in-house, not like an AI or a keyword list. Use **UK English** (personalised, colour, Mum, favourite).

**Keywords**
- Pick one **primary keyword**, the phrase a shopper would type into Google, e.g. "personalised 5th birthday card for girls".
- Pick 3–6 **secondary keywords** from the product's tags and range, e.g. "birthday card with name", "age card", "card for granddaughter", "unicorn birthday card".
- Use the primary keyword in the **first sentence**, in the **H2**, and once more naturally lower down.
- Use each secondary keyword about once.
- No keyword stuffing, no ALL CAPS, no lists of keywords, and no "best/cheapest" claims you can't back up.

**Structure** (HTML for `descriptionHtml`, 180–350 words):
```html
<p>Opening 2–3 sentences: who it's for, the occasion, the emotional hook, primary keyword in sentence one.</p>
<h2>[Primary keyword phrased naturally]</h2>
<p>What they get and how personalisation works: name, age, message, photo. Mention the live preview.</p>
<h3>Why you'll love it</h3>
<ul>
  <li>Concrete benefit + real spec (size, material, print method)</li>
  <li>… 4–6 bullets, each different</li>
</ul>
<h3>Size &amp; details</h3>
<ul><li>Factual specs only</li></ul>
<h3>Delivery</h3>
<p>Dispatch and postage facts.</p>
<p>Short closing line with a secondary keyword or a gifting idea (e.g. pair it with a mug).</p>
```
- One `<h2>`, then `<h3>`s. No inline styles, no font-size spans, no images in the description.
- Answer the questions buyers ask: size, material, can I add a message inside, how fast, does it come with an envelope, is it dishwasher-safe or washable.
- Never claim a product is official, licensed or endorsed. For new original ranges, avoid naming licensed characters or brands. For celebrity face masks, follow the `celebrity-face-mask-listing` skill.

**Every product family is different. Use its own fact sheet.**
- Materials, sizes, care, packaging, delivery and buyer questions come from **`foxyprinting-rebrand/plan/product-facts.md`**, using the sheet for that product family only. A face mask (350gsm card, eye holes, elastic) has nothing in common with a Christmas Eve box or a mug, so never copy specs across families.
- The "Why you'll love it" bullets, the "Size & details" list and the buyer questions answered must all be specific to that product type.
- If the family has no sheet, or a needed fact is marked **ASK**, ask the owner once, write the answer into the sheet, and commit it. Never invent specs, sizes, reviews or delivery promises.

**SEO title** (≤ 60 characters): `Primary Keyword | Foxy Printing`, e.g. `Personalised 5th Birthday Card with Name | Foxy Printing`.

**Meta description** (140–155 characters): a benefit plus the personalisation plus a reason to buy now, in natural sentences. Example: "Make their day with a personalised 5th birthday card – add their name, age and your message. Printed on thick card and posted 1st Class."

**Product title** (Google Shopping friendly, ≤ 150 characters, most important words first): `Personalised [Product] – [Occasion/Recipient] – [Key feature]`, e.g. `Personalised 5th Birthday Card for Girls – Unicorn Design with Name & Age`.

## Google Shopping metafields (set on every new product)

The store uses the Shopify Google & YouTube channel namespace `mm-google-shopping`:

| key | type | value |
|---|---|---|
| `custom_product` | boolean | `true` (personalised, no GTIN) |
| `condition` | single_line_text_field | `new` |
| `google_product_category` | single_line_text_field | full Google taxonomy path, e.g. cards: `Arts & Entertainment > Party & Celebration > Gift Giving > Greeting & Note Cards`; mugs: `Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs` |
| `gender` | single_line_text_field | `unisex` / `female` / `male` |
| `age_group` | single_line_text_field | `adult`, `kids`, `toddler`, `infant` or `newborn` (**not** "Unisex", which older products wrongly use) |
| `color` | single_line_text_field | main colour, or `Multicolor` |
| `mpn` | single_line_text_field | the variant SKU |

## Other house rules
- Never change the live theme ("NEW WAREHOUSE 2020"). Theme work goes to the unpublished **Foxy Pop** theme (`gid://shopify/OnlineStoreTheme/189320528253`). After `themeFilesUpsert`, re-read the files to confirm they saved.
- Artwork sizes: `foxyprinting-rebrand/plan/artwork-specs.md`.
- The owner prefers that routine commands for this project are run without asking.
