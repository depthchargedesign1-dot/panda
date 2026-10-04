# Retro gaming posters: A4 price £4.99 and new descriptions

Prepared 4 Oct 2026 from a full export of the collection **all-retro-game-posters** (13,775 products).
Nothing has been changed on the live store. These are import files for you to run in Shopify admin.

## What we found in the collection

The collection holds more than retro gaming posters, so only part of it is in the import:

| Group | Products | In the import? |
|---|---:|---|
| Retro gaming posters, one "Default Title" variant at £2.99 | 1,229 | **Yes: 1,228** (the "REQUEST ANY GAME POSTER" listing is left out; it needs its own copy) |
| Retro gaming posters with 13 size and frame variants (A4 £4.99 to A3 framed £19.99) | 2,865 | No. Their A4 is already £4.99. Their descriptions are the same junk text, though (see "Your decisions") |
| Other retro gaming posters (Sega Saturn "WWF In Your House" at £4.99 with a non-default variant; "theadams-family" with 3 variants at £2.99, £9.99 and £14.99) | 2 | No |
| Signed and "signature style" prints, stadium posters, Valentine's prints | 9,679 | No. They aren't gaming posters |

Every product that was left out is listed in `odd_ones.csv` with the reason.

## Files

| File | Rows | What it is |
|---|---:|---|
| `00-TEST-3-products.csv` | 3 | Test import: Shining Force 2 (Mega Drive), Shanghai II Dagon's Eye (SNES), Shaolin (PlayStation) |
| `01-retro-posters-1-1228.csv` | 1,228 | The full import (about 2 MB, well under Shopify's 15 MB limit) |
| `samples.md` | 5 | Five full sample descriptions from different consoles |
| `odd_ones.csv` | 12,547 | Everything in the collection that isn't in the import, with the reason |
| `parsed_names.csv` | 1,228 | Current title, the game name and console we took from it, the new SEO title. Check any odd names here |
| `parse_fallbacks.csv` | 2 | Titles we couldn't get a game name from (they get console-only copy, e.g. "GameCube Retro Gaming Poster") |
| `export_summary.csv` | 13,775 | The export with no description HTML: handle, title, type, status, tags, variants, prices, SKUs |

Scripts: `tools/retro_poster_copy.py` (builds the files from the bulk-export JSONL) and `tools/retro_poster_check.py` (checks them).

## What the import changes

For each of the 1,228 products:
- **Body (HTML):** a new description of about 185–220 words in UK English. It has an opening paragraph, one H2, "Why you'll love it" bullets (rotated so neighbouring products don't read the same), "Size & details", "Delivery", a closing line and a **Please note** disclaimer (the video game template naming Nintendo, Sega, Sony, Atari or SNK, otherwise the game's publisher). There are no hyphenated handles, no ALL CAPS and no "official/licensed/genuine" claims.
- **SEO title** (60 characters or fewer), e.g. "Super Mario Kart Retro Gaming Poster | Foxy Printing".
- **SEO description** (140–155 characters).
- **Tags:** every existing tag is kept and `third-party-name` is added. The Tags column replaces all tags, so don't edit it down.
- **Variant price:** £2.99 to **£4.99**.

These stay the same: **Title** (sent unchanged), **Variant SKU** (sent unchanged), the "Title / Default Title" option, and the images, status, vendor, product type and collections (not in the file, so the import should leave them alone. The test file is how you confirm that). The 204 draft products stay drafts.

The paper weight and finish are not mentioned. The old text said "170gsm Silk", but the fact sheet has that marked **ASK**. Tell us if it's right and we'll add it to the sheet and the copy.

## How to import

1. **Do the Infinite Options check first (see the warning below).**
2. Shopify admin, then **Products**, then **Import**. Choose `00-TEST-3-products.csv` and tick **"Overwrite products with matching handles"**. Upload and import.
3. Open the 3 test products in admin and on the shop and check:
   - the **title, images and SKU are unchanged**;
   - the **price is £4.99** and the status is the same as before;
   - the new description, SEO title and meta description show up, and the tags include `third-party-name`;
   - the A3/A2/A1 add-on prices come out right (see the warning).
4. If all is well, import `01-retro-posters-1-1228.csv` the same way (overwrite ticked). Shopify emails you when it's done.
5. Spot-check a few products afterwards, e.g. one Game Boy, one Atari and one Intellivision poster.

## WARNING: Infinite Options size add-ons

The A3, A2 and A1 sizes on these single-variant posters come from the **Infinite Options** app (products tagged "Poster Options"), not from Shopify variants. If those add-ons are set up as a price **on top of** the base price, **every size goes up by £2** when the base changes from £2.99 to £4.99:

| Size | Your standard price | Add-on needed at £2.99 base | Add-on needed at £4.99 base |
|---|---:|---:|---:|
| A4 | £4.99 | n/a (base) | n/a (base) |
| A3 | £8.99 | +£6.00 | **+£4.00** |
| A2 | £12.99 | +£10.00 | **+£8.00** |
| A1 | £19.99 | +£17.00 | **+£15.00** |

Before the full import, open the **"Poster Options"** option set in Infinite Options and **lower each size add-on by £2**, or confirm the totals already come out at A3 £8.99, A2 £12.99 and A1 £19.99. Re-check on a test product after the test import.

Also note:
- **92 of the 1,228** (91 Game Boy and 1 GameCube) **don't have the "Poster Options" tag**, so they may not show any size add-ons at all. Their handles are in `parsed_names.csv` (column "has Poster Options tag" = False). Add the tag if they should have the sizes.
- The Game Boy titles say "A2 A3 Or A4" (no A1), so their copy lists A4, A3 or A2 only. Check that the option set matches.

## Your decisions

1. **The 2,865 multi-variant gaming posters** (A4 to A0 plus framed) have the same poor hyphenated descriptions and no disclaimer. Their prices are already right. Do you want the same new copy for them? That would be a description, SEO and tags import with no price change.
2. **The Infinite Options add-on prices** (warning above).
3. **The 92 posters without the "Poster Options" tag:** add the tag or not?
4. **"REQUEST ANY GAME POSTER"** (handle `102-dalmations-sega-dreamcast-retro-gaming-poster-a4-a3-a2-or-a1`, £2.99): it should get its own copy and price. What should it cost?
5. **Two titles we couldn't parse** (`parse_fallbacks.csv`): "X - Sega Megadrive…" and "Th Ps3 Gamecube…". They get console-only copy. Fix the titles if you know which games they are.
6. Some current titles have typos from the original listings (e.g. "Donkeykong", "Toe Jaman Dearl", "Temco N Ba"). The new copy uses the names as written. Titles were left unchanged, as you asked.
7. **Paper weight and finish** for posters: confirm (the old copy said 170gsm silk).
