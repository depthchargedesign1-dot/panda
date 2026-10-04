# Retro gaming posters: A4 price £4.99 and new descriptions

Prepared 4 Oct 2026 from a full export of the collection **all-retro-game-posters** (13,775 products).
Nothing has been changed on the live store. These are import files for you to run in Shopify admin.

There are two separate jobs here:

- **Job A: 1,228 single-variant posters.** The A4 price changes from £2.99 to **£4.99**, and they get new copy, SEO and tags.
- **Job B: 2,866 multi-variant posters.** They get new copy, SEO and tags only. Their **variants and prices don't change**.

Between them, these files cover the SEO for every retro gaming poster. The SEO-only files for the rest of the store skip gaming posters.

## What's in the collection

| Group | Products | Where it goes |
|---|---:|---|
| Retro gaming posters, one "Default Title" variant at £2.99 | 1,229 | **Job A: 1,228.** "REQUEST ANY GAME POSTER" is left out because it needs its own copy |
| Retro gaming posters with 13 variants (A4 to A0 print only, plus framed A4 and A3) | 2,865 | **Job B** |
| `theadams-family` ("Tetris Blast", Game Boy, 3 variants: A4 £2.99, A3 £9.99, A2 £14.99) | 1 | **Job B** (copy only, prices left as they are) |
| Sega Saturn "WWF In Your House" (1 non-default variant, £4.99) | 1 | Left out |
| Signed and "signature style" prints, stadium posters, Valentine's prints | 9,679 | Left out: they aren't gaming posters |

Every product that was left out is listed in `odd_ones.csv` (9,681 rows) with the reason.

## Files

| File | Rows | Size | What it is |
|---|---:|---:|---|
| `00-TEST-3-products.csv` | 3 | 5 KB | Job A test: Shining Force 2 (Mega Drive), Shanghai II Dagon's Eye (SNES), Shaolin (PlayStation) |
| `01-retro-posters-1-1228.csv` | 1,228 | 2.1 MB | Job A full import |
| `00-TEST-3-multivariant.csv` | 3 | 5 KB | Job B test: Crash Bandicoot (PlayStation), Legend of Oasis (Sega Saturn), Double Dragon II (NES) |
| `02-retro-posters-multivariant-1-1-1500.csv` | 1,500 | 2.4 MB | Job B, part 1 |
| `02-retro-posters-multivariant-2-1501-2866.csv` | 1,366 | 2.2 MB | Job B, part 2 |
| `samples.md` | 8 | | Full sample descriptions: 5 from Job A, 3 from Job B |
| `parsed_names.csv` / `parsed_names_multivariant.csv` | 1,228 / 2,866 | | Current title, the game name and console we took from it, the new SEO title, and whether it has the Poster Options tag (plus the variants, for Job B) |
| `parse_fallbacks.csv` | 4 | | Titles we couldn't get a game name from. They get console-only copy, e.g. "GameCube Retro Gaming Poster" |
| `odd_ones.csv` | 9,681 | | Everything left out, with the reason |
| `export_summary.csv` | 13,775 | | The export with no description HTML: handle, title, type, status, tags, variants, prices, SKUs |

All files are well under Shopify's 15 MB import limit.

Scripts:
- `tools/retro_poster_copy.py` builds the files from the bulk-export JSONL.
- `tools/retro_poster_check.py` checks them. On the last run, every check passed:
  - one H2 per product;
  - 185–220 words each;
  - no hyphen-joined handles, ALL CAPS, banned words, placeholders or inline styles;
  - a disclaimer on every product;
  - SEO title 60 characters or fewer, meta description 140–155;
  - `third-party-name` tag added and all existing tags kept;
  - Job A: titles and SKUs unchanged, every price 2.99 → 4.99;
  - Job B: the size list matches each product's real variants;
  - no handle in both jobs.

## What the import changes

**Both jobs:**
- **Body (HTML):** a new description of about 185–220 words in UK English. It has:
  - an opening paragraph with the keyword "<Game> retro gaming poster";
  - one H2;
  - "Why you'll love it" bullets, rotated so neighbouring products don't read the same;
  - "Size & details";
  - "Delivery";
  - a closing line;
  - a **Please note** disclaimer: the video game template naming Nintendo, Sega, Sony, Atari or SNK, otherwise the game's publisher.

  There are no hyphenated handles, no ALL CAPS and no "official/licensed/genuine" claims. Three game names had "Official"/"Licensed" in the title ("Official PlayStation Magazine 10/13", "Pacman Tengen Licensed"), so the copy calls them "PlayStation Magazine 10" and "Pacman Tengen".
- **SEO title** (60 characters or fewer), e.g. "Super Mario Kart Retro Gaming Poster | Foxy Printing".
- **SEO description** (140–155 characters).
- **Tags:** every existing tag is kept and `third-party-name` is added. The Tags column replaces all tags, so don't edit it down.

**Job A only:** the variant price goes from £2.99 to **£4.99**. The Title and Variant SKU are sent unchanged, along with the "Title / Default Title" option.

**Job B only:** the file has just five columns: **Handle, Body (HTML), Tags, SEO Title, SEO Description**. There is one row per product and no Title, option, variant or price columns, so the variants (A4 £4.99, A3 £8.99, A2 £12.99, A1 £19.99, A0 £24.99, framed A4 £14.99, framed A3 £19.99) are left as they are. "Size & details" lists each product's real variants, e.g. "Print only: A4, A3, A2, A1 or A0" and "Framed: A4 or A3 in a black, white, silver or gold frame". The copy only promises a hard-backed envelope for print-only orders, because framed packaging isn't on the fact sheet.

**Not changed in either job:** images, status, vendor, product type and collections. They aren't in the files, so the import should leave them alone, and the test files are how you confirm that. The drafts stay drafts (204 in Job A, 578 in Job B).

The paper weight and finish aren't mentioned. The old text said "170gsm Silk", but the fact sheet has that marked **ASK**.

## How to import

Use Shopify admin, then **Products**, then **Import**, and **always tick "Overwrite products with matching handles"**.

**Job A (price + copy)**
1. **Do the Infinite Options check first (see the warning below).**
2. Import `00-TEST-3-products.csv`. On the 3 test products, check that:
   - the **title, images and SKU are unchanged**;
   - the **price is £4.99** and the status is the same as before;
   - the new description, SEO title, meta description and the `third-party-name` tag show up;
   - the A3/A2/A1 add-on prices come out right.
3. If all is well, import `01-retro-posters-1-1228.csv`.

**Job B (copy only)**
1. Import `00-TEST-3-multivariant.csv`. On Crash Bandicoot, Legend of Oasis and Double Dragon II, check that:
   - **all 13 variants are still there with the same prices and SKUs**: A4 £4.99, A3 £8.99, A2 £12.99, A1 £19.99, A0 £24.99, framed A4 £14.99 and framed A3 £19.99;
   - the **title and images are unchanged** and the status is the same;
   - the new description, SEO title, meta description and the `third-party-name` tag show up.

   This file has no Title or variant columns. If Shopify rejects it, or touches the variants in any way, **stop and tell us**. We'll rebuild Job B with the full variant rows instead.
2. If all is well, import `02-retro-posters-multivariant-1-1-1500.csv`, wait for Shopify's "import complete" email, then import `02-retro-posters-multivariant-2-1501-2866.csv`.

Afterwards, spot-check a few products from each job, e.g. a Game Boy, an Atari, an Intellivision and a Saturn poster.

## WARNING: Infinite Options size add-ons (Job A)

The A3, A2 and A1 sizes on the single-variant posters come from the **Infinite Options** app (products tagged "Poster Options"), not from Shopify variants. If those add-ons are a price **on top of** the base price, **every size goes up by £2** when the base changes from £2.99 to £4.99:

| Size | Your standard price | Add-on needed at £2.99 base | Add-on needed at £4.99 base |
|---|---:|---:|---:|
| A4 | £4.99 | n/a (base) | n/a (base) |
| A3 | £8.99 | +£6.00 | **+£4.00** |
| A2 | £12.99 | +£10.00 | **+£8.00** |
| A1 | £19.99 | +£17.00 | **+£15.00** |

Before the full Job A import, open the **"Poster Options"** option set in Infinite Options and **lower each size add-on by £2**, or confirm the totals already come out at A3 £8.99, A2 £12.99 and A1 £19.99. Re-check on a test product after the test import.

Also note:
- **92 of the 1,228** (91 Game Boy and 1 GameCube) **don't have the "Poster Options" tag**, so they may show no size add-ons at all. In `parsed_names.csv`, their "has Poster Options tag" column is False.
- The Game Boy titles say "A2 A3 Or A4" (no A1), so their copy lists A4, A3 or A2 only.
- **385 of the 2,866 multi-variant posters also have the "Poster Options" tag.** If that option set shows on them, customers could see the add-on sizes as well as the real size and frame variants. Check one on the shop (they're marked True in `parsed_names_multivariant.csv`), and remove the tag from those products if it doubles up.

## Your decisions

1. **The Infinite Options add-on prices** (warning above).
2. **The 92 single-variant posters without the "Poster Options" tag:** add the tag or not?
3. **The 385 multi-variant posters with the "Poster Options" tag:** check for doubled size choices.
4. **`theadams-family`** ("Tetris Blast"): its A4 is still **£2.99** (A3 £9.99, A2 £14.99), out of line with the standard prices. It got new copy only. Do you want its prices changed?
5. **"REQUEST ANY GAME POSTER"** (handle `102-dalmations-sega-dreamcast-retro-gaming-poster-a4-a3-a2-or-a1`, £2.99): it needs its own copy and price.
6. **Sega Saturn "WWF In Your House"** (`sega-saturn-wwf-in-your-house`, a single £4.99 variant that isn't the default): it wasn't touched. Should it get new copy too?
7. **Four titles we couldn't parse** (`parse_fallbacks.csv`): "X - Sega Megadrive…", "Th Ps3 Gamecube…", "Mr Super Nintendo…" and "Sega Saturn D…". They get console-only copy. Fix the titles if you know which games they are.
8. Some current titles have typos from the original listings (e.g. "Donkeykong", "Toe Jaman Dearl", "Temco N Ba"). The new copy uses the names as written, and the titles were left unchanged.
9. **Paper weight and finish** for posters (the old copy said 170gsm silk), and **how framed posters are packed**: tell us and we'll add them to the fact sheet and the copy.
