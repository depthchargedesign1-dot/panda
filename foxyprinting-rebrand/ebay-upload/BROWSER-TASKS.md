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

## Task 4: NOW (after 1–3). Connect Shopify to eBay with CedCommerce

Follow `shop/CEDCOMMERCE-SETUP.md`, "Owner's steps" 2–7, with these settings:
- **eBay UK only.** Import only the Shopify products tagged `ebay-wave1` (57). Ask the owner before choosing a paid plan.
- **The listings must match the website exactly:** the same title (shortened to 80 characters if needed, keeping the most important words first), the same photos (all of them, up to 24) and **every variation**. Masks have Style × Fitting, and personalised masks have Style × Quantity (3 × 15 = 45). Set prices to the Shopify price for each variation and a fixed quantity of 3 on each.
- **Personalisation:** on the 7 products tagged `ebay-personalised`, turn on eBay's **Personalise** option and paste the instructions for that product from `shop/PERSONALISE-TEXT.md`.
- **Description: important.** Some Shopify descriptions include the phone number, the website address or "live preview / add to basket" lines, and **these must not go on eBay**. Find out whether the app can:
  1. use a description template, or
  2. take the description from a metafield, or
  3. find-and-replace or strip text.

  Tell the owner which of these exist, and **don't upload until the cloud session has replied.** It will then supply clean eBay descriptions (no contact details) in the form the app needs.
- Before uploading, report the eBay category the app suggests for the masks (expected: Costume Masks & Eye Masks, 116724), and the item specifics it fills in.

## Task 5: waiting
After the report on tasks 1–4, the cloud session writes the next steps here (fixes, uploading the 57, then the following waves).
