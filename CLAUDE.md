# Foxy Printing (foxyprinting.co.uk): working rules

The Foxy Printing work lives in `foxyprinting-rebrand/`. The rest of this repository is an unrelated pandas checkout, so don't touch it.

## Creating products: ALWAYS follow these rules

1. **Every new product is created as a DRAFT** (`status: DRAFT`). Never set a product to Active or publish it to a sales channel unless the owner explicitly says so for that specific product or batch. This applies to every route: `productSet`, `productCreate`, `create-product` and CSV imports.
2. **Every new product gets a detailed, human-sounding, SEO description** written from its keywords and tags (see "Product copy" below). Never leave the description empty, and never paste the same text across products.
3. Set the **SEO title and meta description** (`seo { title description }`) on every product.
4. Set the **Google Shopping fields** (see below) so the product is ready for Google Ads / Merchant Center.
5. Set **Product type**, **vendor "Foxy Printing"**, sensible **tags**, and a unique **SKU** on every variant (`FOXY-<machine>-<initials>-NN`, see `foxyprinting-rebrand/tools/build_plan.py`).
   - **Longforte blanks** (owner's rule, 2 Oct 2026): the SKU is Longforte's own product code, then `-FOXY-NN`. For example, the hi-vis kids backpack is `BACKPACK-NEON-ORA-FOXY-01` (Neon Orange & Pink) and `BACKPACK-NEON-GRN-FOXY-02` (Neon Green & Blue). Look up the code on longforte.com (via web search) and never guess it.
6. Personalised products: use template suffix `personalised` (cards: `card`). Set metafields `foxy.mockup` and `foxy.personalise_fields` so the live preview works.
   - Give every personalised product a **full set of personalisation options** that suits it (owner's request), not just one name box. For example:
     - team items: Team name, Club badge upload, Player name, Number, Initials, Team colours;
     - photo gifts: Photo upload, Name, Message;
     - kids' items: Child's name, Age.
   - How the theme reads the labels:
     - "upload", "photo", "logo", "badge" or "crest" becomes an image upload;
     - "message" becomes a longer text box;
     - the words "number" and "age" are limited to 3 characters (phone numbers excluded), "initials" to 4.
   - Tag the product `io-<range>` (e.g. `io-football`) so the owner can attach a matching Infinite Options set in the app if wanted.
7. Image alt text should describe the product in plain words and include the main keyword once.
8. Before creating, search the store for an existing product with the same handle or title to avoid duplicates.
9. To change an existing product, use `productUpdate`, `metafieldsSet` or `productVariantsBulk*`. Don't use `productSet`: on 2 Oct 2026, a `productSet` that sent only one metafield wiped the cufflinks' other `foxy.*` and `mm-google-shopping` metafields. If you must use `productSet`, send every metafield, then re-read the product to check.
10. Live preview style (`foxy.mockup`): use a drawn style (`card`, `drinkware`, `apparel`, `bauble`, `box`, `flat`) only when the product really is that shape, e.g. a greeting card, a mug or glass, a T-shirt or baby grow, a bauble, a gift box or a plaque. For anything else, use `photo`. It shows the product's own photo with a card of the customer's details.

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

## Reproduction "signed" prints
Never call a printed reproduction "signed", "autographed", "hand-signed", "authentic" or "memorabilia". Use **"Printed Signature"** and **"Reproduction Print"** in the title (see `foxyprinting-rebrand/tools/signed_titles.py`), and add the signed-print disclaimer: *"This is a printed reproduction. The signature is printed as part of the design – it is not hand-signed and is not an original autograph…"*

## Other house rules
- **"Foxy Pop 2026 – page banners" is now the live theme** (`gid://shopify/OnlineStoreTheme/189397139837`, published by the owner on 5 Oct 2026). On top of "related fix" it adds:
  - page header banners from the page metafield `foxy.header_image`;
  - the Celebrity Masks homepage hero, the 12-tile "Shop celebrity masks by category" grid and the Celebrity Masks mega menu promo;
  - quick-pay buttons on the cart page and on product pages without personalisation.

  Earlier themes ("Foxy Pop 2026 – related fix" `189396713853`, "Foxy Pop 2026 – menu fix" `189341303165`, Foxy Pop `189320528253` and "NEW WAREHOUSE 2020") are in the library; don't change them.
- Never edit the live theme directly. Make theme fixes on an unpublished copy: `themeDuplicate` the live theme, `themeFilesUpsert` to the copy, and re-read the files to confirm they saved. Then ask the owner to preview and publish the copy. The current working copy is "Foxy Pop 2026 – live preview" (`gid://shopify/OnlineStoreTheme/189408444797`, made 5 Oct 2026): per-product live preview (`foxy.live_preview` = true), a clean preview photo (`foxy.preview_base`) and text drawn in `foxy.preview_zone` (one zone or a list with a `role` each). Keep the repo's `foxyprinting-rebrand/theme/` in step with whatever is live; pending working-copy files are in `foxyprinting-rebrand/theme-working-copy/`.
- Artwork sizes: `foxyprinting-rebrand/plan/artwork-specs.md`.
- The owner prefers that routine commands for this project are run without asking.
- **Tags and metafields** (owner's standing rule, 3 Oct 2026): when a product's tags or metafields (Google Shopping, `foxy.*`, SEO) are wrong, fix them straight away with `tagsAdd`/`tagsRemove`, `metafieldsSet` or `productUpdate`. There's no need to ask first. For thousands of products, where a CSV import is the only practical route, prepare the import files.

## Before launch: Google Merchant Center & Google Ads review (owner's request, 2 Oct 2026)
When the owner says the new site is nearly ready (before publishing Foxy Pop or setting the new products Active), work through `foxyprinting-rebrand/plan/launch-checklist.md` with them. It covers what needs checking or updating in Google Merchant Center and Google Ads. Remind the owner of this when launch comes up.
- **Dropbox: never delete** (owner's rule, 4 Oct 2026). Never delete, trash or overwrite anything in Dropbox (`mcp__Dropbox__delete` or any other route) without the owner's explicit permission for that specific file or folder, given at the time. This is also blocked in `.claude/settings.json`.
