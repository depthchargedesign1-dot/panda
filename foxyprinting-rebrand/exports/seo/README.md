# SEO titles and meta descriptions for every product (4 Oct 2026)

The owner approved this on 4 Oct 2026 ("Yes make the files for all of them").

These files fill in the **Google search title** and **meta description** (Shopify's "Search engine listing") on every product that was missing them or had text that broke the house rules. Nothing on the live store was changed. These are import files for you to run.

## What the files change

Each file has only three columns: **Handle, SEO Title, SEO Description**. With "Overwrite products with matching handles" ticked, Shopify updates only the columns in the file. Titles, descriptions, prices, variants, images and tags are not touched.

Where a product already had one good field (for example a good meta description but no title), the file repeats that existing text unchanged, so the import doesn't blank it.

## Files

| File | Rows | What it is |
|---|---:|---|
| `00-TEST-3-products.csv` | 3 | Test import: a card (`personalised-blue-bike-birthday-card`), a mug (`worlds-best-public-librarian`) and a face mask (`roxy-mitchell-2015-celebrity-face-mask`) |
| `01-seo.csv` | 10,000 | Handles a… onwards (alphabetical) |
| `02-seo.csv` | 10,000 | |
| `03-seo.csv` | 10,000 | |
| `04-seo.csv` | 10,000 | |
| `05-seo.csv` | 10,000 | |
| `06-seo.csv` | 3,766 | |
| `review-sample.csv` | 200 | Random rows showing the product title, the old SEO text and the new SEO text side by side |

The 3 test products are not repeated in `01`–`06`. Each file is under 3 MB, well inside Shopify's 15 MB limit.

## Import steps (owner, about 10 minutes)
1. Shopify admin → Products → Import → `00-TEST-3-products.csv`. Tick **"Overwrite products with matching handles"**.
2. Open those 3 products. Scroll to **Search engine listing** and check that the new title and description are there. Then check that nothing else changed: the product title, description, price, options and images.
3. Import `01-seo.csv` to `06-seo.csv`, one at a time.
4. **Face masks:** `exports/face-masks/masks-01.csv` and `masks-02.csv` also set SEO text. If you import those, do it **before** these files. These files reuse the mask SEO titles, but they replace any mask meta descriptions that had grammar slips (for example "a Ellie Goulding" or a sentence that stops mid-way).

## Counts

| | Products |
|---|---:|
| Products in the 4 Oct export | 58,742 |
| Skipped: archived | 116 |
| Skipped: retro gaming posters handled by the poster agent (`exports/retro-posters/`: the 1,228 single-variant ones plus 2,865 with size and frame variants) | 4,093 |
| Skipped: hidden option helper products (`OPTIONS_HIDDEN_PRODUCT`, e.g. "Your Poster is UPGRADED to A4 Silver Framed") | 26 |
| Already fine: SEO title and meta description both set and within the rules | 738 |
| **In these files** | **53,769** |
| … SEO titles written | 53,588 |
| … meta descriptions written | 53,699 |
| … both written | 53,518 |
| … title only (good meta kept) | 70 |
| … meta only (good title kept) | 181 |

Signed, Valentine's, stadium and other non-gaming prints from the `all-retro-game-posters` collection are included here, because the poster agent doesn't cover them.

Rows by product family: printed-signature prints 13,242 · mugs 7,632 · face masks 6,925 · cards 6,777 · fridge magnets 4,599 · replacement game cases 3,178 · keyrings 2,958 · baby grows 2,127 · Christmas sacks, stockings and baubles 1,049 · clothing 970 · coasters and bar mats 786 · other 736 · stickers and labels 712 · posters and prints 600 · bunting and party 548 · towels 294 · cushions 232 · mouse mats 112 · plaques, signs and medals 108 · pet gifts 104 · minifigure display cases 71 · glassware and bottles 9.

## The rules used

**SEO title** (60 characters or fewer): `<primary keyword> | Foxy Printing`. If the keyword is too long, the ` | Foxy Printing` part is dropped instead of cutting words.
- The keyword is a cleaned version of the product title, with the most important words first. The cleaning:
  - turns ALL CAPS into Title Case, keeping real acronyms (NES, SNES, NFL, UK, TV);
  - removes size lists ("A4 A3 A2 Or A1"), sizes in mm, catalogue codes (KE83, MC1585, SA060917), "(SA)", "(Copy)", "GAME INSPIRED THEME", "HIGH QUALITY", pasted handles and repeated words.
- Family-specific forms, for example:
  - "Cobra Triangle NES Replacement Case";
  - "Extra Innings Retro SNES Fridge Magnet";
  - "Personalised Fimbles Birthday Card";
  - "Carson Wentz NFL Printed Signature Print".
- Duplicate titles in the same family get a distinguishing word from the product title (a colour, a region such as EU, or a number). Where there is nothing to add, they get "Design 2", "Design 3" and so on.
- "Signed / Autographed" becomes **Printed Signature** on prints. On other products (e.g. "Signed For Arsenal" cards) the word is removed.
- "Worlds Best X" becomes **"World's No.1 X"**, so no title says "best". The exceptions are names (George Best) and the game "Best of the Best".
- Swear words in rude product titles are starred out in the SEO title (e.g. "F***ing").
- "Official", "licensed", "authentic", "genuine", "memorabilia", "merchandise" and "limited edition" are removed.

**Meta description** (140–155 characters): natural UK English sentences, made up of a benefit, how it's personalised (when it is), one fact and a reason to buy now.
- Each family has its own set of sentences. The variant is picked by a hash of the handle, so neighbouring products don't read the same.
- Facts come only from `plan/product-facts.md`, for example:
  - cards: 350gsm, A5, free envelope, 1st Class, dispatched the same or next working day;
  - mugs: 11oz ceramic, dishwasher and microwave safe;
  - masks: 350gsm card, eye holes, elastic, board-backed envelope;
  - baby grows: 100% cotton, nickel-free poppers;
  - bunting: A5 flags on 300gsm silk card.
- Families with no confirmed specs (cases, magnets, keyrings, towels, coasters, cushions, stickers and so on) only say "made to order in North Yorkshire" or "custom designs on request". Replacement cases also say "no game included".
- Printed-signature prints say the signature is printed as part of the design.
- No proofs, no "live preview", and no delivery-speed claims except on cards.
- Club, console, show and brand names are kept out of meta descriptions; a generic description leads instead. A celebrity's or athlete's own name is used on masks and prints.
- Rude products get a tasteful, swear-free meta.

## Checks run on the finished files (all passed)
- Every SEO title is 60 characters or fewer, and every meta description is 140–155 characters.
- None contains official, licensed, authentic, genuine, autographed, signed, memorabilia, merchandise, best, cheapest, proofs or "live preview". No meta description contains swearing.
- No ALL CAPS words (apart from real acronyms), no double spaces, no " - -", no leftover brackets.
- No duplicate SEO title within a product family.
- Every handle appears once, and the rows add up.

## Scripts
`tools/seo/build.py`, `tools/seo/family.py` and `tools/seo/write.py`. They build the files from the bulk export JSONL and check them. To re-run, place a fresh `scope.json` (the export without archived products and the poster agent's handles) next to `build.py`, then run `python3 build.py && python3 write.py`.
