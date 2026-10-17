# New poster prints check (9 Oct 2026)

Owner's requests (9 Oct):
1. "upload these products into shopify, check that none are online. there should be 5 images for each poster print" from Dropbox `/BENS FILES/OLD STUFF/FILES FOR DROPBOX/WORK/footballers for ben`.
2. "also add these comedians … to poster prints" from `/BENS FILES/OLD STUFF/FILES FOR DROPBOX/WORK/COMEDY JPEGS/JPEG`.
3. (passed on by the coordinator session) the same for `/BENS FILES/OLD STUFF/FILES FOR DROPBOX/WORK/BEN BOXING/JPEG`, with the no-background image as the main image.

## Result: everything is already online, so nothing was created

| Folder | Files | Designs | Already live | Created |
|---|---|---|---|---|
| footballers for ben | 5,630 | 1,127 (9 top level, 814 in `UPLOADED`, 304 in `DONT KNOW THEM`) | 1,127 | 0 |
| COMEDY JPEGS/JPEG | 180 | 30 | 30 | 0 |
| BEN BOXING/JPEG | 456 | 76 | 76 | 0 |

No products were created or changed, and nothing was published or unpublished. Store checks were read-only (`productByHandle` in aliased batches, plus title searches for any that didn't match). The per-design lists are in `footballers-check.csv`, `comedians-check.csv` and `boxing-check.csv`.

### Footballers
- Each design has 5 files: POSTER ONLY + BLACK/SILVER/GOLD/WHITE FRAME. All are **800 x 800 px web mockups (120–230 KB)**. The folder has **no print master** for any footballer.
- Every design is live, and most are listed **twice**:
  - 2019 range: `<name>-football-player-signed-by-autographed-poster-print`, "<NAME> Football Player Printed Signature Print", 8 size/frame variants (A4–A1 print only; A4/A3 black or silver frame), FP-#### SKUs, type "Football Posters". It has 3 images (poster only, black, silver).
  - 2024 range: `<name>-signed-autographed-footballers-star-print`, "… Printed Signature Footballers Star Poster Print Framed Wall Art Gift", 1 variant (£6.99), SP-###### SKU. It has 4 images (black, white, silver, poster only) with alt text "0", and **no gold-frame image**.
- 928 designs matched the 2019 handle. The other 199 matched the 2024 handle, where "Signed Print" and "Signed Football Print SJ" were dropped from the name, e.g. `neymar-psg-2-…`, `eric-cantona-silver-…`. The two "Harry Kane PERSONALISED" designs are live as `harry-kane-…` and `harry-kane-2-…`.
- `ROMELU LUKAKA (1)` is a single stray Black Frame file belonging to ROMELU LUKAKU (1), which is live.
- The Zidane 1 mockup shows a Real Madrid shirt and competition patch. Club kit and badges appear across this range, so it would be website-only under the badge rule. The existing listings are on more channels than that, and I didn't change them.

### Comedians
- 30 designs, each with a master plus POSTER ONLY + 4 frames. The masters are **3508 x 4961 px at 300 dpi = A3 at 300 dpi** (A2 ≈ 212 dpi, A1 ≈ 150 dpi, so A1 is **too small** for 300 dpi, though it's usually acceptable viewed at distance).
- All 30 are live as `<name>-signed-autographed-comedy-star-print` ("… Printed Signature Comedy Star Poster Print Framed Wall Art Gift", type "Signed Comedian Prints", 1 variant £4.99, 4 images 800 x 800, alt "0"). They're in Celebrity Posters and TV Star Posters (tag `cp-tv`) and on Online Store, Shop, Google, FB/IG and more. They have the clean description layout with the printed-reproduction and celebrity disclaimer.
- There is no separate "Comedy" poster sub-collection. A `cp-comedy` sub-collection under Celebrity Posters › Music, Film & TV would be easy to add if wanted.

### Boxing (BEN BOXING section)
- 76 designs × 6 files (no-background master + POSTER ONLY + 4 frames). Includes boxers, UFC (McGregor, Khabib, Anderson Silva, Nate Diaz), the Kray twins and Tom Hardy "Legend".
- All 76 are live as `<name>-signed-autographed-boxing-star-print` (type "Signed BOXING Prints Posters", 1 variant £6.99, collections Celebrity Posters + `boxing-star-posters`). Most boxers also have the 2019 `…-boxing-signed-by-autographed-poster-print` listing.
- The live listings use the four 800 x 800 frame mockups only. The **no-background master is not the main image** anywhere I checked (e.g. Tyson Fury), and there's no gold-frame image.

## Print files
- Footballers: none in the folder (mockups only). These can't be printed from this folder at any size. The originals must be somewhere else.
- Comedians: masters are A3 at 300 dpi, fine for A4/A3, OK-ish for A2, low for A1.
- Boxing: masters exist; sizes not measured for all 76 (spot-check before A1).

## Issues seen (not changed, owner to decide)
1. **Duplicates**: about 1,100 footballer designs are listed twice (2019 8-variant listing + 2024 single-variant listing), plus older copies for some names (e.g. "Zendine Zidane", "MC####" and "Display-" listings). This is the same family as the 284 duplicates already waiting in STATUS #11.
2. **Artwork wording**: the poster artwork itself says **"SIGNED BY:"** on the name plate (seen on Zidane, Peter Kay). Printed reproductions shouldn't say "signed" under the house rule. It's in the image, so only a redesign fixes it.
3. 2024 listings: alt text "0", gold-frame image missing, single variant (no size options) and tags like "Other Console Posters" / "Signed Athletics Prints" on comedians and boxers.

## Offer
- Add the missing images to the existing 2024 listings: gold frame on all, and the no-background master as the **main** image on the 76 boxing ones (owner's wish). Also write proper alt text. These are adds only, via `productCreateMedia` + `productReorderMedia`.
- Make a Comedy poster sub-collection.
- Draft a plan to merge or draft the 2019/2024 duplicate pairs.
