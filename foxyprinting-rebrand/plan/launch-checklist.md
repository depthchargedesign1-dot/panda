# Launch checklist: Google Merchant Center & Google Ads

The owner asked (2 Oct 2026) that before the new Foxy Printing site goes live we check whether anything needs updating in Google Merchant Center or Google Ads. Work through this with the owner before publishing the Foxy Pop theme or setting the new products to Active.

## Google Merchant Center (via the Shopify Google & YouTube channel)
- [ ] **Feed sync:** new products (153 drafts + 70 photo gifts + football range) only sync once they're Active and published to the Google & YouTube channel. Check they appear and pass review.
- [ ] **Diagnostics:** check for disapprovals and warnings (missing GTIN, image issues, price mismatch, landing page errors). The products are set as `custom_product = true`, so no GTIN should be needed.
- [ ] **Google fields:** confirm the CSV import (`exports/google-fields/`, 3 Oct 2026) worked. Gender should be unisex, age group kids or adult, and the Google category, colour, condition, custom product and MPN (the new unique SKUs) set on all products.
- [ ] **Google product categories:** spot-check that the `mm-google-shopping.google_product_category` values came through.
- [ ] **Trademarks and policy:** look for disapprovals on products with third-party names (football clubs, celebrities, consoles, PerfectDraft, signed prints). Check the disclaimers show, and that the "Printed Signature / Reproduction Print" titles have been imported.
- [ ] **Shipping and returns:** make sure the delivery settings and return policy match the site (e.g. "Free UK delivery over £30" in the announcement bar).
- [ ] **Landing pages:** new collection and product URLs return 200 once published. No 404s from unpublished collections (the `new-…` and new photo-gift and football collections are unpublished until launch).
- [ ] **Images:** new lifestyle images meet Google's rules (main image = product on a plain background, no promotional overlays). The first image on each new product is the clean product shot.
- [ ] **Structured data and price:** check the Foxy Pop product pages output correct price and availability, so Merchant Center doesn't flag mismatches.

## Google Ads
- [ ] **Shopping and Performance Max:** check that campaigns include the new products, or create listing groups or asset groups for the new ranges (Photo Gifts, Football, Christmas, Kids' Birthday Cards).
- [ ] **Final URLs and sitelinks:** update any ad, sitelink or extension pointing to old collection URLs or pages that changed in the rebuild.
- [ ] **Conversion tracking:** confirm the Google tag and purchase conversions still fire on the new theme (checkout and thank-you page) after the theme switch.
- [ ] **Trademark terms in ad text:** keep club, celebrity and brand names out of ad copy (see CLAUDE.md, Third-party names).
- [ ] **Negative keywords and budgets:** review them for the new ranges.

## Site checks to do at the same time
- [ ] Publish the new collections, and hide the ones in `collection-tidy.md`.
- [ ] Mega menu links all resolve (`foxy-mega-menu`).
- [ ] Preview on mobile: the live theme is now "Foxy Pop 2026 – menu fix" (published 4 Oct 2026). Check it on mobile
