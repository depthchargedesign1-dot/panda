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

## Third-party names: a disclaimer is REQUIRED

If a product's title, description, tags, design or image uses **any** name or mark that belongs to someone else, it must carry a disclaimer. That includes:
- a football or sports club, league or player;
- a TV show, film, book, cartoon or game character;
- a celebrity or public figure;
- a band;
- a console or game publisher (Nintendo, Sega, PlayStation, Xbox, Atari);
- a brand or logo.

Foxy Printing is not endorsed by, sponsored by or connected to any of them.

**Rules**
1. Add the disclaimer as the **last block** of the description, under `<h3>Please note</h3>`, in a `<p class="disclaimer">`. Fill in the real name(s). Never leave `[brackets]` in it.
2. Pick the template that matches the type of name (below). If a product uses two kinds (e.g. a club and a player), combine them into one paragraph.
3. Never use the words **official, licensed, authentic, genuine, approved, endorsed or merchandise** (meaning official merch) about the product. Don't use club crests, team logos, studio logos or console logos unless the owner confirms a licence.
4. Use names only to **describe** the design or what it fits (e.g. "for Liverpool fans", "replacement case for SNES games"). Never write them as if the product comes from that brand.
5. Keep the trademark out of the **SEO title** and **meta description** where you can, and lead with the generic description, e.g. "Personalised Football Fan Birthday Card – Red Team Colours". Google Ads and Merchant Center can disapprove listings that put trademarks in ad text, or that look like counterfeits.
6. Set the tag `third-party-name` on the product so these items can be found and reviewed later.
7. If you're unsure whether a name is protected, assume it is and add the disclaimer.

**Templates** (UK English; replace the bracketed parts):

- **Football / sports clubs, leagues, players**
  > This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with [Club name], [League, e.g. the Premier League], or any club, league or player. Club and player names are used only to describe the design and who it's for. All trademarks belong to their respective owners.

- **TV, film, book, cartoon or game characters ("theme inspired")**
  > This is an unofficial design inspired by [Show/Film/Character]. It is not official merchandise and is not endorsed by, sponsored by, or connected with [Show/Character] or [rights holder, e.g. the studio], or any of their licensees. All names, characters and trademarks belong to their respective owners.

- **Celebrities and public figures (e.g. face masks)**
  > This is an unofficial novelty product made for fun and fancy dress. [Name] has not endorsed, sponsored or approved this product, and Foxy Printing has no connection with [him/her/them]. The name is used only to describe the design.

- **Video games and consoles (replacement cases, covers, posters, magnets, keyrings)**
  > This is an unofficial, fan-made [replacement case / cover / print] produced by Foxy Printing. It is not made, endorsed or licensed by [Nintendo / Sega / Sony / Microsoft / Atari / the game's publisher]. [For cases: No game, cartridge or disc is included.] All trademarks and game titles belong to their respective owners and are used only to identify compatibility or theme.

- **Bands and musicians**
  > This is an unofficial fan design. It is not endorsed by, or connected with, [Band/Artist], their management or record label. All names and trademarks belong to their respective owners.

- **Brands, products and logos (e.g. drink brands, PerfectDraft)**
  > This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by [Brand]. [Brand] is a trademark of its owner and is used only to describe compatibility or the design theme.

> **Note for the owner:** a disclaimer makes clear you're not the official brand, and it helps with customers and marketplaces. But it does **not** give permission to use someone else's trademark or artwork. Rights holders can still send takedown notices. For your biggest-selling licensed-style lines, get advice from an IP solicitor or a licence.

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
| `gender` | single_line_text_field | **always `unisex`** (owner's rule) |
| `age_group` | single_line_text_field | `kids` or `adult`, decided by `foxyprinting-rebrand/tools/age_group.py`: baby grows, kids' cards, kids' invites, school items and santa sacks are `kids`; adult/rude cards are `adult`; celebrity masks are `adult` unless the mask is a children's character; otherwise use common sense from the title (**never** "Unisex") |
| `color` | single_line_text_field | main colour, or `Multicolor` |
| `mpn` | single_line_text_field | the variant SKU |

## Other house rules
- Never change the live theme ("NEW WAREHOUSE 2020"). Theme work goes to the unpublished **Foxy Pop** theme (`gid://shopify/OnlineStoreTheme/189320528253`). After `themeFilesUpsert`, re-read the files to confirm they saved.
- Artwork sizes: `foxyprinting-rebrand/plan/artwork-specs.md`.
- The owner prefers that routine commands for this project are run without asking.
