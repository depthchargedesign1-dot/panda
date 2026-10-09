# Tasks for Claude in Chrome (eBay)

**Claude in Chrome: read this first.** The eBay session on the cloud (claude.ai/code) writes the jobs here, and you carry them out in the owner's logged-in Chrome. Work from the top. Do only the tasks marked **NOW**, in order, then stop and report back to the owner.

Rules:
- Never type, ask for or store passwords, card details or tokens. The owner types those in.
- Ask the owner before you pay for anything, end or delete a listing, or list anything on eBay that isn't named in the task.
- Report: when you finish, give the owner a short summary to paste back to the cloud session. Say what you did, what you set, and **every error or warning word for word**. Include item numbers and links where you see them.
- Follow eBay UK's rules on every listing. The owner insists on no contact details anywhere, so none of these: phone numbers (e.g. 01439 771468), email addresses, website addresses or links (foxyprinting.co.uk, www., http), "call us", WhatsApp, social media handles, or text asking buyers to buy outside eBay.

All the files named below are in `foxyprinting-rebrand/ebay-upload/` on branch `claude/foxyprinting-rebrand-shopify-usf2x9` of github.com/depthchargedesign1-dot/panda.

---

## Task 1: NOW. Check the eBay account (look only, change nothing)

Use ebay.co.uk Seller Hub. Report the following:
1. **Account:** the seller username, business or private account, seller level (Top Rated / Above Standard / Below Standard) and any account warnings or restrictions.
2. **Selling limits:** Seller Hub > Overview, "monthly limits": the number of items and the amount left.
3. **Shop:** whether there's an eBay Shop subscription (which level), and the shop name.
4. **Business policies:** whether they're switched on, and the names of every existing postage, returns and payment policy.
5. **"Message to seller"** (needed for the Personalise box): is it on?
6. **Current listings:** the number of active listings, plus unsold and ended ones in the last 90 days. Give the main types of item (masks, mugs and so on).
7. **Contact details in current listings.** In Seller Hub > Listings > Active, search the listings (and, if possible, the descriptions) for: `01439`, `07`, `@`, `www`, `http`, `.co.uk`, `call`, `phone`, `email`, `whatsapp`, `facebook`, `instagram`. Write down the item number and title of every listing that has any of them.
8. **Policy problems:** any listings eBay has flagged, removed or marked as problems (Seller Hub > Performance, plus eBay messages about policies, VeRO or intellectual property) in the last 12 months.
9. **Apps:** any apps already connected to the eBay account (Account > Permissions or Third-party app access), e.g. an old Shopify channel.

## Task 2: NOW. Take contact details out of current eBay listings

Do this for each listing you found in task 1, step 7:
- **Revise** the listing (Edit). Delete the phone number, email, web address or "call us" line from the title, description and item specifics, and leave everything else as it is. Save.
- If a listing is from an eBay template with the details built in, fix the template once, then re-save the listings that use it.
- **Don't end or delete any listing.** If one can't be fixed by editing, list it for the owner instead.
- Report the item numbers you fixed, and any you couldn't fix.

## Task 3: NOW. Shop settings and business policies

Follow `shop/SHOP-SETUP.md` steps 1–3:
- Create the policies `FOXY Royal Mail 24`, `FOXY 30 Day Returns` and `FOXY Payment`. If similar policies already exist, tell the owner and ask whether to reuse them rather than make duplicates.
- Turn on "message to seller".
- Shop logo, billboard and description: the images are in `shop/` (store-logo-300.png, store-billboard-1280x288.jpg). Download them from GitHub, then upload them in eBay.
- Make the shop categories in `SHOP-SETUP.md` and report their numbers.

## Task 3b: NOW. Full account settings check and completion (owner, 9 Oct: "check all my policies, all the settings, all the details for the store and setup; complete it all so it's fully functional")

Go through every area below in Seller Hub and My eBay > Account. For each setting, note what it was, then fix it to the target. If something needs the owner's decision or money (marked **ASK**), stop and ask the owner. Report a before → after table.

| Area | Target |
|---|---|
| Business details (Account > Personal info) | Business seller. Business name **Foxy Printing**, trading address Kirkbymoorside YO62 6AR (the owner confirms the full address), a business email the owner chooses. eBay shows these to buyers by law, which is allowed. They don't go in listings. VAT number: **ASK** whether registered. |
| Payments and payouts | Bank account verified, payout schedule (**ASK**: daily or weekly), no holds or verification requests outstanding. Report any "action needed". |
| Postage preferences | Item location Kirkbymoorside, YO62 6AR. Combined postage on: £0 for each extra item, matching `FOXY Royal Mail 24`. Dispatch time to match the policy. Royal Mail / Click & Drop link: report whether it's connected, and **ASK** before connecting. Domestic only for now (no eBay International Shipping until the owner says). |
| Business policies | Only the three FOXY policies are the defaults. Old policies: list them and **ASK** before deleting any. Returns: 30 days, buyer pays. Personalised items can be returned only if faulty, as stated in the listing. |
| Buyer requirements / blocked buyers | Block buyers with unpaid item strikes (2 in 12 months) and buyers outside the postage area. Keep the rest at eBay's defaults. |
| Communication | "Message to seller" (Personalise box) ON. Automatic replies/FAQs: add one FAQ, "How do I send my photo? Send it to us through eBay messages after you buy." No contact details in any reply. |
| Offers / Best Offer | Off for now (made-to-order low prices). **ASK** if the owner wants it. |
| Out-of-stock option | ON, so listings at quantity 0 stay alive and keep their sales history. |
| Feedback | Automatic positive feedback to buyers once they've paid: ON. |
| Promoted listings | **ASK**: none until the owner sets a budget or ad rate. Don't switch on general/standard campaigns. |
| Time away / holiday | Off. Report if it's on. |
| Shop (Store) | Name, logo, billboard and description from `shop/SHOP-SETUP.md`. Shop categories made. Shop subscription level: report it, and **ASK** before changing it. Shop newsletters: off. |
| Seller Hub > Performance | Report seller level, defects, late dispatch rate and the tracking upload rate. Note anything below standard. |
| Notifications | Email the owner about new orders, messages and policy notices. |
| Security | 2-step verification: report whether it's on and suggest the owner turns it on. You don't change it. |

When done, write "eBay account ready" in the report, plus anything still waiting for the owner.

## Task 4: NOW (after 1–3b). Upload the first two CSV files (owner, 9 Oct: no CedCommerce subscription, use CSV)

**Don't subscribe to CedCommerce.** If it's already installed, leave it, but don't import or upload anything with it, or the listings would be duplicated.

1. Download these two files from GitHub (open each link, then click "Download raw file"):
   - https://github.com/depthchargedesign1-dot/panda/blob/claude/foxyprinting-rebrand-shopify-usf2x9/foxyprinting-rebrand/ebay-upload/uploads/M-A-01-personalised-photo-masks.csv
   - https://github.com/depthchargedesign1-dot/panda/blob/claude/foxyprinting-rebrand-shopify-usf2x9/foxyprinting-rebrand/ebay-upload/uploads/M-TEST-50-celebrity-masks.csv
2. The three FOXY policies (task 3) must exist first. Their names must match exactly.
3. Seller Hub > Reports > Uploads > **Upload template**. Upload `M-A-01-personalised-photo-masks.csv` first. Wait for it to finish, then download the **results file** and copy every error or warning word for word.
4. Open one of the new personalised listings and check:
   - the Personalise box shows next to Buy It Now (it can take about 15 minutes);
   - the variations (Style × Number of Masks) and prices look right;
   - there's no phone number or web address anywhere.
5. Then upload `M-TEST-50-celebrity-masks.csv` the same way, and get its results file too.
6. Report the number of listings created, the item numbers, every error, and how one listing looks (a screenshot is fine).

## Task 5: waiting
After the report on tasks 1–4, the cloud session writes the next steps here (fixes, uploading the 57, then the following waves).
