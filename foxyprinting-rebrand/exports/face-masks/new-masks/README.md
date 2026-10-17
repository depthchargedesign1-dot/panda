# New celebrity face masks: draft product import (5 Oct 2026)

These are 1,939 new celebrity and character face masks. Their artwork was in Dropbox but there was no product for them on the store. The artwork is already in Shopify Files (all READY). Every product imports as a **DRAFT** and is **not published** to any sales channel.

Built by `tools/new_masks_build.py`.

| File | Products |
|---|---|
| `00-TEST-3-new-masks.csv` | 3: Paul Lambert (football + club disclaimer), Darth Vader (character), Mark Sheppard (actor + show) |
| `01-new-masks.csv` | 1,000 |
| `02-new-masks.csv` | 936 |
| `skipped.csv` | 189 not built, with the reason for each |
| `preview.csv` | one line per product: file, handle, title, category, age group, SKU, tags, SEO title and meta |

## What each product gets
Each product copies the masks built on 2 Oct (Graeme Swann, Cole Anderson-James and Jack Joseph):
- **Option "Style":** Ready to Wear £2.99 (SKU `FaceMask-<Name>`) and DIY £1.50 (SKU `FaceMask-<Name>-DIY`). Inventory isn't tracked, and selling continues when out of stock.
- **Type, vendor and category:**
  - Type "Celebrity Facemask"
  - Vendor Foxy Printing
  - Category Apparel & Accessories > Costumes & Accessories > Masks
- **Images:**
  1. the mask artwork
  2. the ready-to-wear assembly guide
  3. the DIY assembly guide
  4. the product-info card
  5. the first standard party photo (`MaskUploadimage1`)
  6. the second standard party photo (`MaskUploadImage2`)
- **Description:** unique, house layout, 261–348 words. Written with `tools/mask_copy.py` from the person's name, category and show, and facts from the "Face masks" sheet only.
- **Disclaimer:** the last block of every description:
  - real people get the celebrity template, which names the show where there is one;
  - football and sport blurbs that name a club or national team also get the club wording;
  - characters get the character template, which names the rights holder;
  - LEGO, Compare the Market (Aleksandr Orlov) and Levi's (Flat Eric) get the brand template.
- **SEO:** SEO title of 60 characters or fewer; meta description of 140–155 characters, in whole sentences.
- **Tags:**
  - `celebrity-face-mask`, so the product shows in all-facemasks and best-selling-face-masks;
  - its `mask-<category>` tag (with a sport sub-tag where one applies);
  - `third-party-name`;
  - `new-arrivals`;
  - `foxy-new-masks-oct2026`, so you can find this batch quickly.
- **Google Shopping:**
  - custom_product true, condition new, Masks category, gender unisex, colour Multicolor;
  - MPN = the Ready to Wear SKU;
  - age_group `adult`, except 34 children's characters (Peppa Pig, Toy Story, Postman Pat and others), which are `kids`.

## Import steps (owner)
1. Shopify admin → Products → Import → `00-TEST-3-new-masks.csv`. Leave "Overwrite products with matching handles" **unticked**: these are new products.
2. Open the 3 products and check:
   - they are **Draft** and not on any sales channel;
   - there are 6 images, with the mask first;
   - both Style options show the right prices and SKUs;
   - the description ends with the "Please note" disclaimer;
   - the SEO preview looks right;
   - the Google Shopping metafields are filled in.
3. If all three look right, import `01-new-masks.csv`, then `02-new-masks.csv`.
4. Before you set any of them to Active, see "Before launch" in CLAUDE.md (Merchant Center and Ads checklist).

## Not in the CSV
- **Shopify category metafields:** fabric (Cardboard), age group, target gender and usage type. The 2 Oct templates have them, but CSV import doesn't reliably set metaobject references. They can be added after import with `metafieldsSet`, in batches filtered by the tag `foxy-new-masks-oct2026`.
- **Product-specific photos:** the per-mask back, front-and-back and AI party photos the skill makes for single listings. Each of these 1,939 products uses the 5 shared images instead.

## Skipped (`skipped.csv`)
- **173 already on the store.** The name or the character's name is in an existing mask's title or handle (accents are ignored).
  - 12 of them match only on the handle, because the existing title is spelt differently.
  - 3 of those look like mis-titled store products, where the handle names one person and the title names someone else. Worth a look:
    - `jesse-birdsall-fraser-black-hollyoaks-face-mask`, titled "David Haye";
    - `myra-mcqueen-hollyoaks-face-mask`, titled "Jorgie Porter";
    - `stephanie-waring-hollyoaks-face-mask`, titled "Susannah Constantine".
- **14 generic Halloween or novelty designs** (Scary Clown, Grim Reaper, Pumpkin Man, Acid Smiley and others). They aren't a person or a character, so the celebrity copy doesn't fit. They need their own copy.
- **2 real children:** Princess Charlotte and Prince Louis. Your call.
