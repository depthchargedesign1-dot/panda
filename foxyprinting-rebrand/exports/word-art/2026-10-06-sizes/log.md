# Personalised Name Word Art: sizes and framed options (6 Oct 2026)

Owner's request: "Personalised Name Word Art on foxy, all products need the framed print and size options adding".

## Scope
53 products whose title contains "Personalised Name Word Art" (26 Pink Letter A–Z, incl. two titled "Pink Letter D"; 26 Blue Letter A–Z). All ACTIVE, none DRAFT. List: `list.json`. Before: `before.json`. Mid-run snapshot: `mid.json`. After: `after.json`.

## What changed (all 53, verified by re-reading after.json: 0 problems)
- Option "Title / Default Title" renamed to "Size" / "A4 Print Only" with `productOptionUpdate` (keeps the original variant id, so Google Merchant item ids, stock and order history stay), then 7 variants added with `productVariantsBulkCreate`:
  A4 Print Only £4.99 (unchanged, compare-at £6.99 kept), A3 Print Only £9.99, A2 Print Only £12.99, A1 Print Only £19.99, A4 Print + Black Frame £19.99, A4 Print + Silver Frame £19.99, A3 Print + Black Frame £29.99, A3 Print + Silver Frame £29.99 (structure and prices copied from the A. J. Green printed signature prints). All 53 had A4 at £4.99, so no price exceptions.
- New variants copy the old variant's settings: taxable, inventory DENY, tracked, 1,000 in stock at Unit 1 Balmforth Business Park, requires shipping, country GB, HS 491191, no compare-at price.
- Weights: print-only sizes keep the old 800 g; framed A4 740 g, framed A3 1,300 g (copied from the A. J. Green AF-1 framed variants).
- SKUs: old SKU + `-A4`, `-A3`, `-A2`, `-A1`, `-A4-BLK`, `-A4-SLV`, `-A3-BLK`, `-A3-SLV` (424 SKUs, all unique; none existed before).
- `mm-google-shopping.mpn` set to the A4 SKU (was a junk "FSP-40643-A4 0119318…" value). Other Google fields untouched.
- Description (existing copy kept): the first sentence that promised "Black, Silver, White or Gold Frames … A3, A4 or as a card" now matches the real options; a `<h3>Size &amp; details</h3>` list (A4 210 x 297 mm, A3 297 x 420 mm, A2 420 x 594 mm, A1 594 x 841 mm) and the Premium Display frames line were added after the paper list. "Ready to hang" was left out because the existing copy says A4 frames come with a stand.
- SEO title set to "Personalised Word Art Print <Colour> Letter <X> | Foxy Printing" (41 had none); meta descriptions re-sent unchanged.
- Template suffix, tags and status unchanged. These products have no `foxy.*` live-preview metafields and no personalised template (before or after).

## Problems hit
- `productUpdate` with only `seo.title` clears the meta description: caught on the test product and restored; the rollout always sends both.
- New variants inherit the default variant's compare-at price unless `compareAtPrice: null` is sent: fixed on the test product, sent on the rollout.
- The MCP caps a GraphQL document at 16 KB, so the rollout ran in two phases: create variants from one shared `$V` variable, then set SKUs by variant id. Some calls returned "upstream_error" but had completed; state was re-read before each next step.

Tool: `tools/word_art_sizes.py`.
