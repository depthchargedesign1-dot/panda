# Foxy Printing (foxyprinting.co.uk): working rules

**Start every session by reading `foxyprinting-rebrand/STATUS.md`** (open questions, running work, known blocks) and keep it updated.

The Foxy Printing work lives in `foxyprinting-rebrand/`. The rest of this repository is an unrelated pandas checkout, so don't touch it.

## Creating products: ALWAYS follow these rules

1. **Products the owner asks for go live straight away** (owner's rule, 6 Oct 2026: "launch all new products I request as active all the time"). Create them `status: ACTIVE` and publish them to the Online Store (`gid://shopify/Publication/95329800`) and Shop (`gid://shopify/Publication/121694519547`), and also to Google & YouTube (`gid://shopify/Publication/10722541604`, feeds Merchant Center), Facebook & Instagram (`gid://shopify/Publication/68348608699`) and TikTok (`gid://shopify/Publication/78820802811`) unless the product is rude/profane, or shows a **football club badge/crest or any logo that could infringe** (owner, 6 Oct 2026, clarified: "I dont want any football club badges or any logos that can cause infringement going online"; e.g. club crests, brand/company logos, console or game publisher logos, retro gaming box art), which stay on the website only. **Celebrity faces and names are fine on every channel** (celebrity masks, the Request a Facemask listing, signed prints and posters of people), as long as no logo or badge is in the design (found 6 Oct 2026: new products had been left off these three channels), but only once every other rule below is met (copy, SEO, Google fields, images, SKUs) and the product has been re-read to check it. Anything you make on your own initiative (bulk imports, suggested pairing products the owner hasn't approved, test items) stays a **DRAFT** until the owner says so.
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
   - **Product images: real photos only** (owner's rule, 8 Oct 2026: "Please dont use cad images always use real images with print on"). Every product image must be a real photo of the actual product (our own photos, the store's existing real product photos, the owner's Dropbox photos, or the supplier's real packshots of the blank) with the design printed on it: the artwork placed onto the photo with the right perspective, curve, wrap, lighting and texture so it looks really printed. Never use flat, drawn, vector or "CAD" style mockups (plain shapes, flat rectangles standing in for a glass, mug or sign) as product images. If no real photo of the blank exists, ask the owner for one rather than drawing it. Owner, 8 Oct 2026, repeated after the bar pint glasses went live with cartoon-style images: "do not ever use this style of main image or mockup again". So never publish, attach or leave live a drawn/vector/cartoon product image, even as a stand-in, and never paste one product onto another product's scene (e.g. a drawn pint glass dropped onto the bar mat photo). A free-licence real stock photo of the plain blank (Pexels/Unsplash/Pixabay, commercial use allowed) is acceptable as the base for the print composite. Live-preview base images (`foxy.preview_base`) should also be real photos where possible.
8. Before creating, search the store for an existing product with the same handle or title to avoid duplicates.
9. To change an existing product, use `productUpdate`, `metafieldsSet` or `productVariantsBulk*`. Don't use `productSet`: on 2 Oct 2026, a `productSet` that sent only one metafield wiped the cufflinks' other `foxy.*` and `mm-google-shopping` metafields. If you must use `productSet`, send every metafield, then re-read the product to check.
10. **Glass products are always printed UV DTF** (owner's rule, 9 Oct 2026: "we will always print UVDTF onto glasses so remember when you are asked to make new glass products thats the style of print that applies always"). Every new glass product (pints, tumblers, flutes, gin glasses, glass cans, any glassware) states UV DTF as the print method in its copy, specs and print files, and its product images must show a UV DTF print: crisp opaque full-colour transfer with a white underbase, sharp edges, a slight raised gloss, no film edge and no background box. Never sublimation, vinyl, engraving or etching on glass. Photos used for glass products must be **clean and crisp** (owner, same day): full-resolution, sharp, no blur, no visible JPEG noise.
11. Live preview style (`foxy.mockup`): use a drawn style (`card`, `drinkware`, `apparel`, `bauble`, `box`, `flat`) only when the product really is that shape, e.g. a greeting card, a mug or glass, a T-shirt or baby grow, a bauble, a gift box or a plaque. For anything else, use `photo`. It shows the product's own photo with a card of the customer's details.

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
Never call a printed reproduction "signed", "autographed", "hand-signed", "authentic", "limited edition" or "memorabilia". Use **"Printed Signature"** in the title (see `foxyprinting-rebrand/tools/signed_titles.py`). Owner's decision (6 Oct 2026): **"Reproduction Print" goes in the description, not the title** (the owner was worried it hurts sales), stated clearly near the top, and the signed-print disclaimer goes at the end: *"This is a printed reproduction. The signature is printed as part of the design – it is not hand-signed and is not an original autograph…"*
- **Frames** (owner, 6 Oct 2026): where a print is sold framed, highlight that these are **Premium Display frames: thick, chunky and very professional, not cheap thin frames**. Frame material and depth are still **ASK**; don't invent measurements.

## Other house rules
- **Live theme: "Foxy Pop 2026 – plate squeeze"** (`gid://shopify/OnlineStoreTheme/189519069565`, published by the owner on 9 Oct 2026; = "poster tidy" `189518610813` + number plate mug squeeze/plate font/dealer line in `assets/personaliser.js`, the Word Art Designer (`snippets/word-art-designer.liquid`, `assets/word-art-designer.*`, render line in `sections/main-product.liquid`) and leavers colour photos). "Poster tidy" is now the first rollback. Everything below about "poster tidy" still applies, because it is included. **Live theme: "Foxy Pop 2026 – poster tidy"** (`gid://shopify/OnlineStoreTheme/189518610813`, published by the owner on 8 Oct 2026; = "swatches & posters" `189514809725` + even-grid size buttons for long option names + tidier old descriptions in `sections/main-product.liquid`; "swatches & posters" is now the first rollback). It contains everything from "field fix" (page header banners, Celebrity Masks hero/grid/mega menu promo, cart quick-pay, the theme's own "Buy it now" button (this store pays through PayPal, not Shopify Payments), per-product live preview (`foxy.live_preview`, `foxy.preview_base`, `foxy.preview_zone`), the `&#39;` placeholder fix, Judge.me reviews, app embeds) PLUS: the leavers designer (`product.leavers-designer` template, `assets/leavers-*`, Print Studio page), the "(optional)" personalisation fix, Ralawise-style round colour swatches on product pages (`snippets/colour-hex.liquid`), longer school-name (80) / class-names (3000) boxes, "Shop by type" sub-collection tiles + compact banners on collection pages (`foxy.subcollections`, `foxy.compact_header`), and the Celebrity Posters mega-menu promo (`sections/header-group.json`). Collection headers come from `collection.metafields.foxy.header_image`, else the auto `foxy-header-<group>` banners. Mirror of its changed files: `foxyprinting-rebrand/theme-working-copy-leavers-designer/` (leavers-* asset sources live on branch `claude/zealous-wozniak-qzr6bg`, folder `leavers-designer/`).
- **Rollback:** "Foxy Pop 2026 – field fix" (`189420994941`). On 8 Oct 2026 the owner deleted the other Foxy Pop copies (live preview, page banners, mug tiles, optional fields, leavers designer, leavers logo upload) to stay under the 20-theme limit. Don't change old themes, and never delete a theme yourself.
- **Current shared working copy (9 Oct 2026):** "Foxy Pop 2026 – word art fix" (`189546004861`), duplicated from the live "plate squeeze" by the Word Art Designer session (it owns `assets/word-art-designer.js`/`.css` there). Put new theme changes here.
- **One shared working copy at a time:** the owner's son's Claude and other sessions also change the theme. Before any theme change, check whether an unpublished working copy duplicated from the CURRENT live theme already exists and use that one (agree file ownership with the other session); only `themeDuplicate` the live theme if there is none. Tell the other sessions the copy's id.
- Never edit the live theme directly. For any theme change, `themeDuplicate` the live theme into a new unpublished copy, `themeFilesUpsert` to the copy, re-read the files to confirm they saved, then ask the owner to preview and publish it. Mirror the copy's files in `foxyprinting-rebrand/theme-working-copy/` and, once published, in `foxyprinting-rebrand/theme/`.
- Personalisation labels (`foxy.personalise_fields`): write apostrophes as ’ (curly), e.g. "Child’s name".
- Artwork sizes: `foxyprinting-rebrand/plan/artwork-specs.md`.
- **Production artwork** (print files, Intec ColorCut cut/crease files, editable PDFs): follow the `foxy-production-artwork` skill. Owner's rule (5 Oct 2026): each product's editable artwork goes in its own folder in Dropbox, `/AI DESIGNS 2026/<Product title> - <SKU>/`.
- The owner prefers that routine commands for this project are run without asking.
- **CSV imports: only the owner runs them** (owner, 8 Oct 2026). His son also works on the store with his own Claude account; that Claude must never run or schedule Shopify CSV imports or the import reminders. Import files and the schedule live in `foxyprinting-rebrand/exports/IMPORT-SCHEDULE.md`; the owner's Claude hands them over.
- **Print-ready artwork for every new product** (owner's rule, 6 Oct 2026): every product we create must come with print-ready production artwork. That means the right print size from `foxyprinting-rebrand/plan/artwork-specs.md`, **3 mm bleed** on every trimmed or cut edge (or the wrap bleed the spec gives, e.g. mugs), a safe area of at least 3 mm inside the trim, CMYK-safe colours, 300 dpi for any images, live/editable text where the customer personalises, and cut lines on a CUT layer where it's machine-cut. **Include the fonts** used (owner's rule): put the font files (open-licence fonts only, e.g. Google Fonts/OFL) and their licence text in a `Fonts` subfolder, or a `FONTS - DOWNLOAD LINK.txt` (font name, source URL and a Shopify Files link to the .ttf/.otf) when the file can't be uploaded directly. Save it in Dropbox `/AI DESIGNS 2026/<Product title> - <SKU>/` as the `foxy-production-artwork` skill describes, before the product goes live.
- **Mask packs and pairs: main image** (owner's rule, 6 Oct 2026): for any product with 2 or more masks, the first/main product image shows the masks side by side on a clean background with **no text** on it.
- **Always suggest pairings** (owner's rule, 6 Oct 2026): whenever a new product or product idea comes up, suggest other products that pair with it (e.g. a mask pack, a matching mug or card, party props, a bundle) and offer to make them.
- **Racial caricature products** (yellowface, blackface and similar, e.g. Little Britain's Ting Tong): don't make them. Offer the other characters or the actors as themselves instead.
- **Push changes straight to the store** (owner's standing rule, 5 Oct 2026): whenever it's a benefit, apply changes directly through the API (`productUpdate`, `metafieldsSet`, `productVariantsBulkUpdate`, in aliased batches) instead of handing the owner a CSV. Keep CSV import files only for sets too large to push sensibly (tens of thousands of rows or many MB of text), and say why.
- **Tags and metafields** (owner's standing rule, 3 Oct 2026): when a product's tags or metafields (Google Shopping, `foxy.*`, SEO) are wrong, fix them straight away with `tagsAdd`/`tagsRemove`, `metafieldsSet` or `productUpdate`. There's no need to ask first. For thousands of products, where a CSV import is the only practical route, prepare the import files.

## Before launch: Google Merchant Center & Google Ads review (owner's request, 2 Oct 2026)
When the owner says the new site is nearly ready (before publishing Foxy Pop or setting the new products Active), work through `foxyprinting-rebrand/plan/launch-checklist.md` with them. It covers what needs checking or updating in Google Merchant Center and Google Ads. Remind the owner of this when launch comes up.
- **Dropbox: never delete** (owner's rule, 4 Oct 2026). Never delete, trash or overwrite anything in Dropbox (`mcp__Dropbox__delete` or any other route) without the owner's explicit permission for that specific file or folder, given at the time. This is also blocked in `.claude/settings.json`.
