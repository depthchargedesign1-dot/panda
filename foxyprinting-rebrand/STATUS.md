# Foxy Printing – live status board

Read this first in every new session. Keep it short: update it when something starts, finishes or needs the owner.
Last updated: 6 Oct 2026, evening.

## Waiting on the owner (answer these and a lot unblocks)
| # | Question | Unblocks |
|---|---|---|
| 1 | Dispatch time (working days) for flags, mugs, hats, masks | "fast turnaround" copy, Amazon handling time |
| 2 | Packed weights: 11oz mug, bobble hat, each flag size | Shopify postage, Amazon, eBay |
| 3 | Frame material and depth (prints) | "Premium Display frame" copy |
| 4 | Flag print: hem/bleed for 25 mm binding, eyelet count/spacing, which printer and roll width | flag templates |
| 5 | Hat: badge size and placement on the cuff, press settings, mirror? | hat artwork |
| 6 | Sticker sizes: sweet jar, kids name labels, helmet decals, gift tags, die-cut, product labels, thank-you, kiss-cut sheet; second size for rectangles and ovals | 7 sticker templates |
| 7 | Christmas last posting dates | publish Christmas gift guide |
| 8 | Blank game cases: supplier, sizes, photos | 6 draft cases |
| 9 | OK to delete: 21 "trerrace" duplicate draft flags (Shopify); broken BR3W UP Wales SVG and first Farm Shop SVG (Dropbox) | tidy-up |
| 10 | Unpublish from FB/IG, TikTok and Google: 9 club baby grows, Ed Sheeran and Billie Eilish posters, Scottie Barnes and Andy Burnham masks, older sensitive-figure masks (Shopify blocks me from unpublishing) | copyright rule |
| 11 | Approve: 284 exact duplicates to draft; rewrite 2,708 print descriptions with false claims; Man City Treble flag with trophies (keep, redesign or remove) | Merchant Center health |
| 12 | Preview and publish theme "Foxy Pop 2026 – mug tiles" (`189453861245`): compact banners site-wide + "Shop by type" tiles on ALL MUGS. Preview: https://foxyprinting.co.uk/collections/all-mugs?preview_theme_id=189453861245 | shorter collection headers everywhere, mug tiles |
| 13 | Connect Postiz as a Claude connector (see below) | posting to FB, IG and TikTok |
| 14 | Unpublish request-any-facemask from Google, FB/IG and TikTok (now shows celebrity masks: Sabrina Carpenter, Rosé, Luke Littler, Zara Larsson, Lisa, Graeme Swann). Archive the Jimmy Savile and Rolf Harris masks? Allow a collage main image (image tool upload blocked)? | copyright rule, reputation |

## Owner's import queue (one file each morning and bedtime; reminders run 07:52 and 21:52 UK)
See `exports/IMPORT-SCHEDULE.md`. Order: SEO 02-CLEAN → age 01 → age 02-CLEAN → masks TEST then 01–04 → mug descriptions TEST, 01, 02-rude → prints TEST then 01–04.

## Running or recently finished
- This Girl / This Guy mugs (6 Oct, owner approved): 152 duplicate dog mugs (`foxyprinting-dog-mugs-Nw`) set to DRAFT, their twins stay ACTIVE (log `exports/this-girl-this-guy/2026-10-06-duplicates-drafted.csv`). Title typos fixed on 145 products (title + SEO + description + alt where the typo appeared; handles unchanged; log `2026-10-06-title-typos.csv`). **Owner: the printed artwork itself still has some typos** (e.g. TIQUANDO, GRINDER, WHEATEN TERRIOR seen in the mug photos), so reprint/re-shoot those designs.
- Mug descriptions (6 Oct): checked all 6,332 mugs (excluding This Guy/This Girl and the rude/funny number plate mugs). 6,275 empty or poor descriptions rewritten (6,081 normal + 194 rude; 40 skipped, see skipped.csv), 2,298 with a third-party disclaimer + `third-party-name` tag (tags added via API). Vendor set to Foxy Printing on 1,577 mugs and Google fields fixed via API (mpn = SKU on 6,321; category, age group, colour etc. where missing). Body text goes in by CSV import (queue #7a/#7b). Audit of missing SEO title/meta (3,691) and empty alt text (3,230): `exports/mug-descriptions/2026-10-06/audit-all-mugs.csv`. Owner to look at: SKUs with swear words (copied into Google mpn), King Charles mugs with "OFFICIAL" in SKU/title, an R. Kelly mug.
- Personalised Name Word Art (6 Oct): all 53 products (Pink/Blue Letter A–Z) now have Size options A4/A3/A2/A1 print only and A4/A3 Black or Silver framed (£4.99–£29.99, A. J. Green structure), new SKUs, mpn, sizes + Premium Display frames line in the description. The wider Word Art Prints collection (219 products: number, pet, hobby and "Pop Figures" word art) was NOT changed; ask the owner if they want the same. Record: `exports/word-art/2026-10-06-sizes/`.
- New mask collections (6 Oct): YouTuber & Influencer (77), K-Pop (56), The Traitors (27). Smart collections on tags `youtuber-masks` / `kpop-masks` / `traitors-masks`, added to the Celebrity Face Masks menu. New BTS/Traitors/creator masks need the matching tag. Record: `exports/face-masks/2026-10-06-new-collections/`.
- Mask pairing packs (6 Oct, owner approved): 3 LIVE on all 5 channels: BTS 5-pack (Jimin, V, RM, Suga, J-Hope; £6.99, Spice Girls/1D structure), Liam & Noel Gallagher brothers pair and Travis Kelce & Taylor Swift couple pair (Ready to Wear £4.99 / DIY £2.99, Lou and Andy structure). Main images: masks side by side, no text (tools/mask_pack_images.py). Dubois v Wardley fight pack SKIPPED (no artwork for either boxer). No single Jin/Jungkook mask yet, so the BTS pack is 5 members. Record: exports/face-masks/2026-10-06-packs/.
- Trending 100 masks (6 Oct): 17 new celebrity masks LIVE (ACTIVE, Online Store, Shop, Google, FB/IG, TikTok) from the Dropbox artwork: Liam Gallagher, Travis Kelce, Matt Damon, Jerry Hall, BTS Jimin/V/RM/Suga/J-Hope (tag kpop-masks), Florence Welch, Mark Ronson, Ben Price, Andrew Garfield, Nicholas Hoult, Jeff Hordley, Joel Dommett, Gwen (Melanie Walters). Style Ready Cut/DIY x Fitting Elastic/Stick (2.99/3.49/1.50/2.00). Print+cut PDFs in Shopify Files, cut SVG + links in Dropbox `/AI DESIGNS 2026/<title> - <SKU>/`. Mrs Brown skipped (agnes-brown-mrs-brown-boys-face-mask exists). Manifest `exports/face-masks/2026-10-06-trending-100/built-masks.csv`; builder `tools/trending_masks_build.py`. Owner to glance at: Florence Welch art is low-res (595x842); Jimin cut outline (pale hair); BTS 5-pack + Oasis brothers + Kelce/Swift couple pack are natural pairings (not made).
- Request Any Celebrity Face Mask (6 Oct): new title, copy and SEO; new main image "REQUEST A FACEMASK" with 6 faces (tools/request_mask_hero.py, exports/face-masks/2026-10-06-request-mask/). Sex and City request mask ARCHIVED (owner asked).
- Mug sub-collections (done 6 Oct): new smart collection funny-number-plate-mugs (20 mugs, Online Store + Shop). 14 mug collections have new 1800x600 headers (`foxy.header_image`, live now) and `foxy.compact_header`; ALL MUGS has `foxy.subcollections`. 23 compact auto banners `foxy-header-<group>-compact.jpg` added to Files (originals kept). Theme copy "Foxy Pop 2026 – mug tiles" `189453861245` (duplicated from live "field fix", Infinite Options embed on) waits for the owner to publish. Record: `exports/mug-subheaders/manifest.json`.
- Rude number plate mugs: live (website and Shop only). Teaser ads in `exports/social/2026-10-06-rude-mugs/`, not posted.
- TikTok ads (mug, masks, Wales flag): made, not posted. See `exports/social/2026-10-06-tiktok-ads.md`.
- Amazon test (mug, hat, flag): `exports/amazon/2026-10-06-test/`; exporter `tools/amazon_export.py`.

## Connections
Shopify ✅ · Dropbox ✅ (never delete) · Google Drive ✅ · Gmail ✅ (drafts only, never send) · Higgsfield ✅ (TikTok needs the owner's form) · GitHub ✅ (works in Accept edits mode) · Postiz ⏳ (add custom connector `https://api.postiz.com/mcp/<API key>`) · eBay/Amazon/BigCommerce ❌ (CSV/xlsx files only).

## Known blocks (don't retry; ask the owner)
- Shopify MCP blocks unpublish, bulk mutations, and probably delete.
- Uploading local files to Higgsfield from here is blocked, but the Higgsfield sandbox can download, edit and PUT files to a `media_upload` URL; then `fileCreate` from that Higgsfield URL. Shopify staged URLs must never go to Higgsfield.
- foxyprinting.co.uk and Higgsfield CloudFront are not reachable from this machine. cdn.shopify.com and *.dl.dropboxusercontent.com ARE allowed now (owner added them 6 Oct): download Dropbox art with download_link + local curl, render locally, upload with stagedUploadsCreate (PUT, Content-Type header only) + productCreateMedia.
