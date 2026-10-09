# Description & SEO cleanup (Oct 2026)

Fix 2 (descriptions) and Fix 3 (SEO) from `../catalogue-audit/2026-10-09/README.md`. Built by a side session for the main session to hand over. **CSV imports are run by the owner only.** None of these files are in `IMPORT-SCHEDULE.md` yet; the main session adds them.

## 1. Compliance fixes: DONE, pushed straight to the store (9 Oct 2026)
- **318 products** updated through the API (`productUpdate` in batches of 6–12, every result checked; a sample re-read after the push matched).
  - "Limited Edition", "memorabilia", "Autographed"/"Collectible" taken out of titles and copy (reproduction prints now say "Printed Signature" and carry the signed-print disclaimer).
  - The right disclaimer is the last block (`<h3>Please note</h3><p class="disclaimer">`), with the real names filled in.
  - `third-party-name` tag added where it was missing.
  - SEO title (≤ 60) and meta description (140–155) set on every one.
- Plus the 2 royal family 8-pack masks (`7710732189947`, `8062795743483`), fully rewritten.
- Record of exactly what was sent: `compliance-api/applied_2026-10-09.json.gz`. Readable list: `compliance-api/review.csv`. All 318 descriptions on one page: `compliance-api/samples.html`.
- Generator: `tools/compliance_copy.py`.
- **Left out on purpose:**
  - 2 baby grows "Boys/Girls Name Limited Edition": this is the slogan printed on the vest, so they're left for the baby vest rewrite.
  - The "movie memorabilia" hobby coaster: it names a hobby; it doesn't claim the product is memorabilia.
  - The personalised sock: rewritten by hand; its material and sizes are **ASK**.
- Fixed on the way:
  - K-pop masks where the old copy named the member's real name as the "group" (DK, Jun, Wonwoo, The8 → SEVENTEEN).
  - "Evan" mask: the store lists Evan as ENHYPEN, which has no member called Evan, so the group was left out. **Owner: which group is Evan in?**
  - Halloween III title no longer says Michael Myers (he isn't in that film), and the Halloween 6 title now says 1995.

## 2. "[brackets]" (80 products): not a customer-facing problem
All 80 are PerfectDraft Maxi Skins. The "brackets" are Word leftovers (`<!--[if !supportLineBreakNewLine]-->`) **inside HTML comments**, so shoppers never see them. The real problems are that these 82 listings are pasted from Word with inline styles, US spelling ("customize"), no disclaimer (PerfectDraft, Star Wars, Harry Potter, football clubs…) and contradictory specs: the titles say "vinyl sticker" but the handles say "magnetic skin". Their rewrite is waiting on the new **PerfectDraft skins** ASK section in `plan/product-facts.md`.

## 3. Active products with an empty description (49): owner decisions, not copy
| Group | Count | Suggestion |
|---|---|---|
| Poster upgrade helper items ("Poster is UPGRADED to A4 Gold Framed…", A0 upgrade) | 11 | Hide from Google & search (they're add-on items, not products). No copy needed. |
| SNES cases where the handle names a different game from the title (e.g. title "Romance Of The Three Kingdoms II", handle `roger-clemens-mvp-baseball…`) | 15 | Check which game each one really is, then they'll join the SNES case rewrite. |
| "Valentines" mugs built on homophobic slurs ("YOUR A DYKE / FAG / QUEER / FUCKTARD BUT I DO LOVE YOU") | 8 | **Recommend archiving.** No copy written. Marketplaces and Google will reject them anyway. |
| 2016-era items: 100 business cards, address labels (4 sizes), "Copy Of 12 X Personalized Princess Party Stickers", "Personalized Iron Man Kitkat Label", "Poster", "Wedding Gifts", "Rear Print on 123 Bundle" | 10 | Archive, or say which to keep and I'll write them up. |
| "This Girl Loves Ball / Breeding / Dt / Game" mugs | 4 | What do "Breeding" and "Dt" mean on these? Then they get mug copy. |
| "Test Party Bunting" | 1 | It's a test product that is ACTIVE. Set it to draft? |

## 4. SEO titles & meta descriptions: IMPORT FILE READY
- `seo-fill/seo-fill-01.csv`: **3,484 products**, columns `Handle, SEO Title, SEO Description` only (no Title/Status/Body). 0.9 MB. Import with "Overwrite products with matching handles".
- The 318 products from step 1 are excluded (they already have SEO from the API push).
- Where a product already had a valid value, that value is kept as it is. Only missing or broken fields were written: 3 printed gift tins had a meta description cut off mid-sentence ("Great for.").
- Checks on every row:
  - title ≤ 60 characters, meta 140–155 characters;
  - none of the words official / licensed / authentic / genuine / approved / endorsed / signed / autographed / memorabilia / limited edition;
  - no duplicate titles (repeats become "… Design 2", "… Design 3").
- What's in it:
  - **retro gaming posters, 3,307:** game name + "Retro Gaming Poster"; console brand names kept out of the title;
  - **Printed Signature music posters, 67:** "Printed Signature", never "signed";
  - **Santa sacks, 49:** hessian is only mentioned where the title says hessian; XL sacks don't claim a material;
  - **printed gift tins, 30;** **rugby towels, 9:** generic first, "Personalised Rugby Bath Towel – Bradford 1995 Away";
  - **kids' birthday banners, 15;** **football face coverings, 2;** **mugs, 2.**
- `seo-fill/skipped.csv` (31): 25 hidden option-helper products (not for sale), 4 retro posters whose game name can't be read from the title ("X", "D", "Th Ps3", "Mr Super Nintendo"), and "Santa Approved" (the design name contains "approved"; its handle says XL but its title says Small, so it needs checking).
- `seo-fill/notes.csv`: 2 cards that only got a title (no card meta template in this pass).
- Generator: `tools/seo_fill.py` (re-runnable on a fresh export).

**Samples (3 of 3,484):**
| Handle | SEO Title | SEO Description |
|---|---|---|
| `adventure-island` | Adventure Island Retro Gaming Poster \| Foxy Printing | Adventure Island retro gaming poster, a fan-made print made to order in our North Yorkshire workshop. A great gift for any gamer. Order today. |
| `westlife-2-signed-autographed-music-star-print-copy` | Westlife Printed Signature Poster 2 \| Foxy Printing | Fan-made Westlife music poster with a printed signature-style design. Printed to order in North Yorkshire. Order today. Ideal for a bedroom wall. |
| `personalised-santa-paws-bella-santa-sack-xl-extra-large-custom-name` | Personalised Santa Paws Bella XL Santa Sack \| Foxy Printing | Make Christmas Eve magic with a personalised extra large Santa sack: the Santa Paws Bella design, printed with any name in North Yorkshire. Order today. |

**Overlap to know about:** the 4 Oct retro poster import files (`../retro-posters/`, never imported) also set SEO on many of the same posters, plus new body copy, titles and prices. If the owner imports those later, they will overwrite these SEO values with their own (also compliant) ones. Either order is safe.

## 5. Family description rewrites: next
Order: Baby Vest, Kids Cards, Gaming Cards, Movie Cards, Holiday Stockings (+ dedupe), Coasters, SNES cases, NES/SNES posters/magnets/keyrings, Football Posters. Three samples per family will be added here before each full file. Families whose facts are **ASK** in `plan/product-facts.md` wait for the owner's answers.
