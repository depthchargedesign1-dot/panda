# eBay upload: funny number plate mugs

> **Ready to upload (updated 6 Oct 2026, main picture changed).** All 10 designs use the single full-wrap plate design (200 x 70 mm), and the
> picture URLs point at the Shopify images (rendered locally with `tools/artwork/number_plate_mug_local_mockups.py`).
> The **main (first) picture is now the two-mug "both ends" view**, so the whole registration shows in search results - the same
> as the main photo on Shopify / Google Shopping.

File: `ebay-number-plate-mugs-upload.csv` (eBay File Exchange / Seller Hub "Reports > Uploads" format, eBay UK, GBP).

Contains all 10 mugs (BR3W UP, B15 CU1T, 2 SUG4RS, D3C4F N0, BO55 MUG, WFH 4EVA, NAP T1ME, D4D T4X1, F1X3D 1T, SN00 ZED), all live on Shopify.
Each listing is one parent row plus 5 variation rows (Country = GB, Scotland, Wales, Northern Ireland, Ireland), £7.99 each,
custom label = Shopify SKU, pictures = Shopify CDN URLs (the country picture is attached to each variation).
Parent pictures, in order: the two-mug "both ends" view (main picture), GB mockup, Scotland, Wales, Northern Ireland, Ireland, and the flat plate artwork.
The main picture is the `main` key in the URLs file.
The URLs come from the Shopify API and are stored in `exports/number-plate-mugs/shopify-image-urls.json`. If the images change, update that file and
re-run `python3 tools/artwork/number_plate_mugs.py ebay exports/number-plate-mugs/shopify-image-urls.json`.

Item specifics: Brand Foxy Printing, Type Mug, Material Ceramic, Capacity 11oz, Colour White, Theme Novelty,
Features Dishwasher Safe | Microwave Safe, Country of Manufacture United Kingdom. Condition: New (1000).

## Upload steps
1. Open the CSV and fill the **\*Category** column with the eBay UK category ID for *Cups & Mugs*
   (Seller Hub > Listings > Create listing > search "mug" shows the ID). It is left blank on purpose so we don't guess an ID.
2. Fill **ShippingProfileName**, **ReturnProfileName** and **PaymentProfileName** with the names of your business policies
   (Account > Business policies), or delete those columns to use your defaults.
3. Check the **\*Quantity** on the variation rows (set to 10 each; mugs are made to order).
4. Seller Hub > Reports > Uploads > Upload template > choose the CSV. Wait for the processing report and download the results file.
5. Fix any rows the report flags (usually category-specific required item specifics) and re-upload just those rows.
6. Check each listing preview: title, variation pictures and the description (it's the Shopify HTML).

Titles are 80 characters or less and contain no third-party names. The plates are novelty designs, not real registrations.

## Rude number plate mugs (separate file, 6 Oct 2026)

File: `rude-number-plate-mugs-ebay.csv` - the 10 adult-humour plates (A33 HOI3, B3LL 3ND, 8008 I3S, CL1 NT, D1K H34D,
N0B H34D, P3N 15, T05 53R, W4N K3R, W3T W1P3), same layout as the main file: one parent row + 5 Country variation rows
each, £7.99, custom label = Shopify SKU (FOXY-SUB-RNPM...), main picture = the two-mug "both ends" view.
Built with `python3 tools/artwork/rude_number_plate_mugs.py ebay exports/rude-number-plate-mugs/shopify-image-urls.json`
(picture URLs are the Shopify CDN files without the ?v= cache-buster).

**Read before uploading - eBay restricts profanity.** eBay's offensive-material policy does not allow profanity or
obscene language in listing titles, and its filters can block or remove listings whose title or pictures show it, even
disguised with numbers. The titles here never spell a word out (only the plate as written plus "Adult Humour"), but the plates
themselves are the joke, so expect some of them (most likely CL1 NT, W4N K3R, D1K H34D, B3LL 3ND) to be blocked or
pulled. Suggestions:
- Upload this file separately from the main number plate file, so a rejected row does not hold up the clean range.
- If eBay flags a listing, drop that design from eBay rather than re-listing it; repeated violations can hurt the account.
- Pick an adult/novelty-appropriate category and keep "Adult Humour" in the title so buyers know what they are getting.
The same steps as above apply (fill *Category, business policies and quantities, then Seller Hub > Reports > Uploads).
