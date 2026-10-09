# CedCommerce eBay Integration: set-up for Foxy Printing (9 Oct 2026)

The owner chose CedCommerce (9 Oct) to connect Shopify to eBay UK instead of uploading CSV files.

**Only the owner can install it.** Installing a Shopify app and logging in to eBay inside it needs the owner's own Shopify admin and eBay login. Claude can't do this from the cloud session, and nobody should ever paste a password or token in chat.

## Already done by Claude (Shopify side)

- Checked 9 Oct: no eBay app is installed yet. The sales channels are Online Store, Shop, Google & YouTube, Facebook & Instagram, TikTok, Snapchat Ads, Inbox, Cdiscount, Cazaar, POS, Buy Button and Mobile App.
- Tagged the products for the first wave, so the app can import just these and not all 30,000:

| Tag | Products |
|---|---|
| `ebay-wave1` | all 57 below |
| `ebay-test-50` | the 50 best-selling celebrity masks (`lists/1b-masks-test-batch-top50.csv`) |
| `ebay-personalised` | the 7 personalised photo masks (tier A in `lists/1-masks.csv`) |

## Plan cost

The free plan only allows a one-time upload of about 10 products and manages up to 100. The 57 products need **Bronze**, which is about $19 a month or $199 a year and covers 100 uploads a month and 2,000 managed products. Check the live price on the app page, because sources disagree. Later waves (thousands of masks, posters and mugs) need a higher plan, so pick it when we get there.

## Owner's steps (about 30 minutes)

1. **Business policies in eBay first.** Do step 1 of `SHOP-SETUP.md` (`FOXY Royal Mail 24`, `FOXY 30 Day Returns`, `FOXY Payment`) and step 2 ("message to seller" on). CedCommerce reads the policies from eBay, so they have to exist first.
2. **Install:** Shopify admin > Apps > search "CedCommerce eBay Integration" > Install. Approve the permissions.
3. **Connect eBay:** choose **eBay UK (ebay.co.uk)**, log in to the Foxy eBay seller account in the eBay window and accept. Item location: Kirkbymoorside, YO62 6AR, United Kingdom.
4. **Import only the wave:** in the app's product import, choose **Import by filter > Tag = `ebay-wave1`**. Don't import everything.
5. **Order settings:** turn on order sync (eBay orders come into Shopify), with inventory at 3 per listing (owner's rule: quantity 3). In the app's inventory or price rules, set a **fixed quantity of 3**, not Shopify stock.
6. **Make two profiles (templates)** in the app:

| Profile | Products (filter) | eBay category | Policies | Item specifics |
|---|---|---|---|---|
| Foxy Personalised Masks | tag `ebay-personalised` | Costume Masks & Eye Masks (116724, to be checked in the app's category picker) | the three FOXY policies | Brand: Foxy Printing; Type: Face Mask; Material: Card; Size: One Size; Department: Adults; Country of manufacture: United Kingdom; **Personalise: Yes** + instructions "Type the names in the box. Send your photo through eBay messages after you buy." |
| Foxy Celebrity Masks Test | tag `ebay-test-50` | same | same | same, without Personalise |

7. **Upload:** select the products in each profile > Upload/List on eBay.
8. **Tell Claude when it's done.** Paste the app's error list or screenshot it. Claude fixes the Shopify side (titles, specifics) and tells you what to change in the app.

## Things to check in the app before upload

- **Titles:** eBay cuts at 80 characters. 76 of the test masks have long titles. Use the app's title rule or ask Claude to make the eBay titles. `uploads/*.report.txt` already has the shortened titles.
- **Description:** the app sends the Shopify description, which mentions the live preview and the website. Pick the app's description template option if there is one, and paste in `templates/listing.html` (no links or phone numbers, which eBay doesn't allow).
- **Price:** the Shopify price by default. Add a price rule (e.g. +20%) if you want eBay prices higher to cover fees (`SHOP-SETUP.md` explains why).
- **Variants:** masks have Style (Ready Cut / DIY) x Fitting (Elastic / Stick). The personalised masks have 3 styles x 15 pack sizes, and eBay allows up to 250 variations, so that's fine.

## After upload

Watch the 50-mask test for 2–3 weeks for VeRO or faces/names removals (see `uploads/README.md`). Don't upload the CSV files too, or every listing will be on eBay twice. The CSVs stay as a backup route only.
