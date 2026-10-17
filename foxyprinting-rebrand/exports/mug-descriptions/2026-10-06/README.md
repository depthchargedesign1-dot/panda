# Mug descriptions: what's in this folder (6 Oct 2026)

We went through all 6,332 mugs on the shop. These were left out:
- This Guy / This Girl mugs, which are being done separately;
- rude number plate mugs;
- funny number plate mugs.

Most mugs had no description, or one that was poor: old eBay text, ALL CAPS, the same text copied across hundreds of mugs, or lists of hashtags. We wrote a new description for each one. Every description is different and is written from the mug fact sheet: 11oz ceramic, dishwasher and microwave safe, printed in-house.

## The numbers
- **6,332 mugs checked.** 1,154 had no description, 5,161 had a poor one and 17 were already fine.
- **6,275 new descriptions** written: 6,081 normal mugs and 194 rude mugs. The rude mugs are cheeky in tone, the swear words are starred out (e.g. F*ck), and each one has a line saying it's adult humour.
- **2,298 mugs** use someone else's name: a celebrity, club, band, TV show or brand. Each one gets a "Please note" disclaimer at the bottom saying it's unofficial. They also now have the `third-party-name` tag, which has already been added on the shop.
- **40 mugs were not rewritten.** They're listed in `skipped.csv` with the reason:
  - 26 aren't standard 11oz ceramic mugs (thermal mugs, a coaster and similar), and the mug fact sheet doesn't cover them;
  - 12 make fun of a condition or use a slur (e.g. "Cure for Turettes"). Do you want to keep them?
  - 2 are just called "Worlds Best Mug(s)", so we couldn't tell who they're for.

## Already fixed on the shop (no import needed)
- **Vendor:** set to "Foxy Printing" on 1,577 mugs. Before, it showed things like "Celebrity Mugs", "Motor Mugs" or "King Charles III Official Merchandise & Gifts".
- **Google Shopping fields:**
  - the MPN now matches the mug's SKU on 6,322 mugs (it used to be an old 2022 "SKU + number" code);
  - category, age group, colour, condition, gender and "custom product" filled in where they were missing or wrong.
- Every change is listed in `api-fixes-log.csv` (old value → new value).
- We checked again afterwards with a fresh export. Everything has landed.

## How to import (only after the files already in the queue)
Follow the order in `exports/IMPORT-SCHEDULE.md`. These are #7a and #7b, after the face masks and before the signed prints.

1. **Test file first:** `00-TEST-6-mugs.csv` (3 normal mugs and 3 rude mugs).
   - Shopify admin → Products → Import → choose the file.
   - **Tick "Overwrite products with matching handles".**
   - When the "import complete" email arrives, open the 6 mugs on the site and check the descriptions look right. They are:
     - World's Best Distribution Manager;
     - The Future Mrs Aaron Chalmers;
     - Personalised Brazil Football Birthday;
     - I Normally Have 7 Inches;
     - AR*EBADGER;
     - Beat Me Bite Me.
2. Then import **`01-mug-descriptions.csv`** (6,081 mugs, 9.7 MB). Tick "Overwrite" again.
3. Wait for the email, then import **`02-rude-mug-descriptions.csv`** (194 rude mugs). Tick "Overwrite" again.

The files only change the **description**. Titles, status (active or draft), options and SKUs are copied exactly as they are now, so nothing else moves. Mugs with more than one option (e.g. red or black handle) have one row per option.

## Other files
- `audit-all-mugs.csv` lists every mug with:
  - what was wrong with the description;
  - whether it was rewritten;
  - SEO title and meta missing: 3,132 mugs, but all except 2 are already fixed by the SEO import waiting in the queue (#1);
  - image alt text empty: 2,115 mugs;
  - the vendor **before** the fix.
- `third-party-names.csv` shows which name triggered each disclaimer.

## Things worth a look
- **Swear words in SKUs:** some SKUs contain swear words, e.g. `FOXY-MUG-PUT-THE-KETTLE-ON-CUNT-…` and `FOXY-MUG-AWESOME-FUCKING-DICK-…`. Google uses the SKU as the MPN, so Merchant Center may flag them. Do you want them renamed?
- **King Charles coronation mugs:** they still have "Official" in the title and SKU. We don't call products official, so we'd suggest removing it.
- **R. Kelly:** there's an R. Kelly mug. You may want to archive it.
- **Spelling:** "The Furture Mrs Margot Robbie" is misspelled in the title.
- **Unpublishing:** mugs with a celebrity, club or brand name should be on the website only, not on Google, Facebook/Instagram or TikTok, but Shopify won't let us unpublish them. It needs doing in Shopify admin.
