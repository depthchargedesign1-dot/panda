# Word Art Prints: the other 166 products (8 Oct 2026)

The owner approved this on 8 Oct 2026 ("yes do the same for the word art prints"). These are the Word Art Prints collection (`gid://shopify/Collection/279839473851`, 219 products) **minus** the 53 "Personalised Name Word Art" letter prints in `../2026-10-06-sizes/list.json`, which were not touched. That leaves 166 products: 31 pop-figure designs, 25 dog, 20 hobby, 15 style, 14 kids, 14 number, 12 animal, 11 cat, 10 love, 7 pet, 4 family and 3 travel.

## What changed on each product
- **Variants:** the single "Default Title" option became **Size**, with 8 values:
  - "A4 Print Only": the old variant renamed, so its id, price, stock and order history stay;
  - A3 Print Only £9.99, A2 £12.99, A1 £19.99;
  - A4 Print + Black/Silver Frame £19.99;
  - A3 Print + Black/Silver Frame £29.99.
  
  New variants copy the A4's settings: taxable, DENY, tracked, ships, GB, HS 491191, same stock. Compare-at is cleared. Weights are 800 g for prints, 740 g for A4 framed and 1300 g for A3 framed. SKUs are the old SKU plus `-A4`, `-A3`, `-A2`, `-A1`, `-A4-BLK`, `-A4-SLV`, `-A3-BLK` or `-A3-SLV`. All 1,328 are unique.
- **Personalisation:**
  - template suffix `personalised`;
  - `foxy.personalise_fields` has two boxes: "Name / Dog’s name / Cat’s name / Pet’s name / Family name (shown largest)" and "Your words message (20–30 words, separated by commas)";
  - `foxy.mockup` set to `photo`;
  - tag `io-word-art` added and tag `Poster Options` removed.
- **Description:** each one is new and unique, written by `tools/word_art_other.py`. They are 296–348 words of UK English, with one h2 then h3 sections. There are no inline styles, h4s, hashtags or empty tags, and no mention of cards or white/gold frames. They use only facts from the existing copy: sizes, paper, Premium Display frames, how the words work, and delivery.
- **SEO:** title ≤ 60 characters, `Personalised <subject> Word Art Print | Foxy Printing`. Meta description 140–155 characters. Pop-figure SEO uses generic subjects such as "Potions Master Pop" and keeps character names out.
- **Google:** `custom_product` true, `mpn` = A4 SKU, `color` set by eye from the black-frame photo. Gender (unisex), condition (new), age_group (adult, per `tools/age_group.py` for Posters) and category were already correct, so they weren't changed.
- **Third-party names (31 pop-figure designs):** a disclaimer goes last under "Please note" (`<p class="disclaimer">`) and the tag `third-party-name` is added.
- **Images (163 products):** there are no print-only photos for any of these designs, so the print-only variants have no image.
  - The black-frame photo is first and the silver-frame photo second. Framed variants are linked to the matching photo.
  - Plain alt text with the keyword once, e.g. "Personalised beagle word art print in a black frame".
  - 231 images detached with `fileUpdate referencesToRemove`; the files are still in Shopify Files: 163 white frame, 54 gold frame and 14 white frame on a pink wall.

## Deviations / left for the owner
- **Images not touched (no images at all):**
  - Copy of Copy of Personalised Rachel (7164594323643);
  - Copy of Personalised Mulan (7164585312443);
  - Personalised Pug 3 duplicate (7161690357947).
- **Gold-frame and pink-wall photos detached as well as white-frame ones:** only black and silver frames are sold.
- **Title typos left as they were (not asked to retitle):**
  - Voldermort, Pheobe, Mcgonagol, Dumbledor and Moaning Martel;
  - "Staue of Liberty" and "FGerman Shepard";
  - "Ihasa Apso", Racoon, Shiatsu and "Cat 2  " (double space);
  - "Copy of …" titles;
  - many handles and SKUs are off by one from the title (old copy-and-paste naming).
- **Duplicates:** Rachel ×3, Mulan ×2, Pug 3 ×2, Dress 1 B ×2, German Shepherd ×2, Statue of Liberty ×2.
- **Pop-figure designs:**
  - All 31 are still published on Google & YouTube, Facebook & Instagram and TikTok, as well as the Online Store; 29 are also on Shop.
  - The artwork is in the style of collectable pop vinyl figures. Some designs show names like DISNEY or FRIENDS, and the source files are labelled "BENMAW".
  - Nothing was unpublished. **Owner to decide** whether these should be website + Shop only under the logo/infringement rule.

## Process
1. Tested on 2 products, the Dachshund (`copy-of-personalised-crown-3-word-art-poster-print`) and Snape (`copy-of-personalised-sirius-word-art-poster-print-inspired-by-pop-figures`), then re-read them.
2. Phase A ran in 28 batches (`a_00`–`a_27`): option rename, A4 SKU, `productVariantsBulkCreate`, description/template/SEO, tags and metafields.
3. Phase B ran in 23 batches (`b_00`–`b_22`): new SKUs, variant images, `fileUpdate` alts and detach, `productReorderMedia`.
4. Fixes made along the way:
   - an en-dash typo in `personalise_fields` on 6 a_01 products, fixed;
   - number designs' "Design:" line now reads "a black number 50";
   - "a 18th" changed to "an 18th".
5. Final re-read of all 166 (`after.json`, checked by `tools/word_art_other_verify.py`) found **0 problems**: options, prices, compare-at, weights, SKUs, template, tags, description equals plan, HTML rules, SEO, all foxy and Google metafields, media order, alts and variant images.

Files:
- before: `collection_all_before.json`;
- plan: `plan.json`, `list.json`;
- batches: `a_*.graphql`/`.vars.json`, `b_*.graphql`;
- after: `after.json`.
