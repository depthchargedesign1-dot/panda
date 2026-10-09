# eBay upload project: plan (started 9 Oct 2026)

**Goal:** list the Foxy Printing range on eBay UK using CSV files, in this order (owner's choice): **masks → posters → mugs → baby grows**.

**Why CSV:** the eBay API connection fails, so everything goes through eBay's own bulk upload instead: **Seller Hub > Reports > Uploads**. Those files are made here and the owner uploads them.

The earlier eBay files (number plate mugs, 6 Oct) are in `../exports/ebay/number-plate-mugs/`. They use the same CSV layout as the files planned here, and they are ready to upload.

## What's in this folder

| File | What it is |
|---|---|
| `lists/0-summary.csv` | Counts per category and tier |
| `lists/1-masks.csv` | All 7,042 live masks, sorted: tier A first, then B, C, X; best sellers first inside each tier |
| `lists/1b-masks-test-batch-top50.csv` | The 50 best-selling celebrity masks (real people only, no Disney/Muppets/Star Wars characters) for a small eBay test |
| `lists/2-posters.csv` | All 17,267 live posters and prints |
| `lists/3-mugs.csv` | All 7,516 live mugs |
| `lists/4-baby-grows.csv` | All 2,192 live baby grows / vests |
| `tools/build_lists.py` | Rebuilds the lists from a fresh Shopify export (see the docstring) |
| `source/` | The Shopify export used (`active.jsonl.gz`, live products on 9 Oct 2026 07:45 UTC) and 12 months of sales by product title |

Each list row has these columns:
- `batch`: the upload file it goes in, e.g. `M-A-01` (masks, tier A, file 1). Each batch holds 500 products.
- `tier`, `tier_reason` (see the tiers below).
- `sold_12m`: units sold on Shopify in the last 12 months.
- `title`, `title_chars` and `ebay_title_ok` (eBay titles are 80 characters at most).
- `product_type`, `variants`, `options`, prices, image count and main image.
- Shopify link and product id.

## The tiers: how likely eBay is to accept each item

eBay is stricter than Shopify. Rights owners report listings through eBay's VeRO programme, and eBay removes them. Too many removals can restrict or suspend the seller account. That puts the whole eBay shop at risk, not just the listing. So each product is sorted by risk:

| Tier | Meaning | What to do |
|---|---|---|
| **A** | Our own designs and personalised items: no other person's or brand's name or face | List first |
| **B** | A third-party name in the text only (club names, stadiums, car makes, film/TV characters, memes), or adult wording | Spot-check each batch, then list |
| **C** | A real person's face, name or printed signature (celebrity masks, Printed Signature posters, celebrity mugs), or film-studio artwork | **Owner's decision.** eBay's "faces, names and signatures" policy says you can't list an item showing someone's image, name or signature unless that person made or authorised it. Start with a small test batch if at all |
| **X** | Don't list on eBay: club crests and logos, console/game box art (Nintendo and Sega report listings often), notorious people (e.g. Epstein masks: eBay's offensive-material policy), checkout add-ons ("Your Poster is UPGRADED…", "Baby Vest Upgrade") | Leave off eBay |

## The numbers (live store, 9 Oct 2026)

| Wave | Category | A (list first) | B (check first) | C (high risk) | X (don't list) | Total |
|---|---|---|---|---|---|---|
| 1 | Masks | 7 | 24 | 6,946 | 65 | 7,042 |
| 2 | Posters & prints | 206 | 170 | 13,524 | 3,367 | 17,267 |
| 3 | Mugs | 3,478 | 2,095 | 1,942 | 1 | 7,516 |
| 4 | Baby grows | 1,315 | 875 | 0 | 2 | 2,192 |

**The big point: almost all masks (99%) and most posters (78%) are pictures of real people, which is tier C.** Your best sellers are tier C too: David Attenborough (238 sold), Gerwyn Price, Daniel Farke and Claudia Winkleman. On eBay that is the riskiest part of the range. Mugs and baby grows are mostly safe.

Notes on the counts:
- **Poster sales figures look low** because many poster titles were changed this week. Sales are matched by title, so older sales under the old titles don't count.
- **Titles over 80 characters:** 849 masks, 6,663 posters, 654 mugs and 334 baby grows. These titles have to be shortened for eBay. The CSV builder will do this, keeping the most important words first.
- The tiers come from keyword rules. Spot-check every batch before upload, because some items will be in the wrong tier.

## Suggested order

### Wave 1: masks
1. **M-A-01:** 7 personalised photo masks (stag, hen, birthday, office party, leaving do, wedding, your own face). No celebrity, so they're safe.
2. **M-B-01:** 24 Halloween and kids masks, plus the "Request Any Celebrity Face Mask" service (144 sold). Check each one first. Film or TV characters (Muppets, Minions, Michael Myers) are high risk. The request listing's pictures mustn't show real celebrities.
3. **Celebrity test (only if the owner says go):** `lists/1b-masks-test-batch-top50.csv` holds 50 best sellers (1,306 sold between them in 12 months), real people only. Upload them and watch for 2–3 weeks for removals or policy emails.
   - If no listings get pulled, roll out the rest of tier C in batches of 500, best sellers first.
   - If listings do get pulled, stop. Keep celebrity masks on Shopify and other channels.
4. Never on eBay: the 65 tier X masks (club face coverings, Epstein masks).

### Wave 2: posters and prints
1. **P-A-01:** 206 word art prints, pet portraits ("your dog as Napoleon"), city travel print sets, the birth announcement and the family name print.
2. **P-B-01:** 170 stadium travel posters and club "Tiny Men Big Balls" posters (club names in the text), plus "Inspired By Pop Figures" word art. Check them first.
3. Tier C: 13,524 Printed Signature posters, unofficial celebrity posters and film poster packs.
   - The same test-first approach applies.
   - eBay also has an autographed items policy. Printed signatures must be described clearly as reproductions, and eBay may want "Reproduction" in the title, even though it was taken out of the Shopify titles. Check this before any upload.
4. Never: 3,367 retro gaming posters (Nintendo, Sega, PlayStation, Neo Geo box art) and placeholder or add-on items ("Poster Size", "Copy of …").

### Wave 3: mugs
1. **U-A-01 to U-A-07:** 3,478 mugs in 7 files of 500. These are the occupational "World's Best …" range, personalised names, birthday, This Guy/This Girl, coach and teacher, and cartoon animals.
2. **U-B:** 2,095 mugs to check first.
   - Football club mugs (Kilmarnock, Celtic, Partick Thistle are the top sellers).
   - Adult or rude mugs. eBay doesn't allow profanity in titles, so put these in their own files.
   - Brand or character names (Budweiser, Batman).
3. Tier C: 1,942 celebrity mugs. These are high risk.
4. The 10 + 10 number plate mugs are already done in `../exports/ebay/number-plate-mugs/`.

### Wave 4: baby grows
1. **B-A-01 to B-A-03:** 1,315 baby grows.
2. **B-B:** 875 with club or brand names, e.g. "Me and My Uncle Love Arsenal" and "My Daddy Drives A BMW". Check them first.
3. **Blocked until the owner answers the size question below.** eBay requires a Size item specific for baby clothing, and the fact sheet still says ASK.

## Owner's answers (9 Oct 2026)

- **Celebrity test: yes**, do the 50-mask test ("we have sold masks on eBay before").
- **Postage:** charge postage, unless eBay promotes free postage. In that case give free postage and put the price up. I found no evidence that eBay UK ranks free postage higher, so the first files charge postage through the `FOXY Royal Mail 24` policy (£2.99, £0 per additional item, matching Shopify). See `shop/SHOP-SETUP.md`.
- **Quantity:** 3 per listing or variation.
- **Baby grows:** 4 sizes: 0–3, 3–6, 6–9 and 9–12 months (now in `plan/product-facts.md`).
- **Personalisation:** use eBay's **Personalise** item specific plus instructions. It needs "message to seller" turned on (`shop/SHOP-SETUP.md` step 2).
- **Selling limits:** "great", no limit worries.
- **eBay shop and template:** built in `shop/` and `templates/listing.html`.

Not uploaded yet: the 24 tier-B masks.
- Several are adult performers (Johnny Sins, Bonnie Blue, Lilly Phillips) or "evil" parody masks of real people (Phillip Schofield, Diddy, Peter Mandelson, Tommy Robinson).
- These carry extra eBay risk: the adult-content and offensive-material policies, plus defamation complaints.
- They stay off eBay unless the owner asks for them.

## Original questions (answered above, kept for reference)

1. **Go / no-go on celebrity items (tier C):** yes to a 50-mask test, or keep celebrity items off eBay?
2. **eBay category IDs** for masks, posters, mugs and baby grows. Seller Hub > Create listing > search the item; the ID shows there. I won't guess them, because a wrong ID rejects the row.
3. **Business policy names** (Account > Business policies) for postage, returns and payment, or leave them blank to use your defaults.
4. **Quantity per listing.** Number plate mugs used 10, since everything is made to order.
5. **Baby grows:** sizes, which blank brand you use now, and the print method. These are still marked ASK in `plan/product-facts.md`.
6. **Personalisation:** eBay has no live preview or name boxes. Buyers add the name in the order note or by message after purchase. OK to say "message us the name after purchase" in the description?
7. **Your eBay selling limits.** Seller Hub shows how many items and how much money you can list per month. A new or limited account can't take thousands of listings at once.
   - eBay may also charge insertion fees beyond your free listing allowance, so check your plan before uploading tens of thousands.
   - From community posts (not official): about 14.9 MB per file, and possibly a daily cap of around 2,000 new listings. That's why the batches are 500.

## Next steps (Claude)

1. ~~Build `tools/ebay_csv.py`~~ Done 9 Oct. It turns a batch from these lists into an eBay upload CSV in the same format as the number plate mug files:
   - an `Add` action and `CustomLabel` = Shopify SKU;
   - the title cut to 80 characters;
   - item specifics;
   - pictures from Shopify, up to 12;
   - variations, such as Style/Fitting for masks and Size/Frame for posters;
   - a clean HTML description with the Shopify-only lines removed (live preview, basket, phone number), keeping the disclaimer.
2. ~~Make the first files~~ Done 9 Oct: `uploads/M-A-01-personalised-photo-masks.csv` and `uploads/M-TEST-50-celebrity-masks.csv` (see `uploads/README.md`).
3. Keep `STATUS.md` updated with each upload and anything eBay rejects.

To rebuild the lists after the range changes, run a new Shopify export (query in `tools/build_lists.py`), then:

```
python3 -I tools/build_lists.py <active.jsonl> source/sales365.json lists/
```

Sources for the eBay rules above:
- [eBay faces, names and signatures policy](https://www.ebay.com/help/policies/prohibited-restricted-items/faces-names-signatures-policy?id=4291). This is eBay.com; I couldn't find the eBay UK version of the page.
- [eBay UK autographed items policy](https://www.ebay.co.uk/help/policies/prohibited-restricted-items/autographed-items-policy?id=4283).
- [eBay UK bulk listing tools](https://www.ebay.co.uk/help/selling/ebay-tools/bulk-listing-tools?id=4160).
- File size and daily limit: eBay community posts ([1](https://community.ebay.com/t5/Seller-Tools/File-Exchange-Limit-Increase-Requests-Here/m-p/34682433/highlight/true), [2](https://community.ebay.com/t5/Seller-Tools/File-Exchange-Limit-Increase-Requests-Here/m-p/32530508/highlight/true)), not official.

## eBay account facts (owner's screenshot, 9 Oct 2026)

- Monthly limits: 10M items and £10M (423,421 items and £3.6M used), so effectively no limit.
- **Featured Shop** subscription. Free listing allowances per month (1 Oct to 1 Nov): **fixed price 1,500** (586 used, 914 left) and auctions 600 (3 used). Listings beyond that pay insertion fees, so plan each month's files to fit what's left. E.g. this month: 57 test listings, then up to about 850 more.
- The account already has many live listings. Check for duplicates of our masks before the upload (browser task 1, step 10).
