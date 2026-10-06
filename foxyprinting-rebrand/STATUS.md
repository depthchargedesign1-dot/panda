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
See `exports/IMPORT-SCHEDULE.md`. Order: SEO 02-CLEAN → age 01 → age 02-CLEAN → masks TEST then 01–04 → prints TEST then 01–04.

## Running or recently finished
- Request Any Celebrity Face Mask (6 Oct): new title, copy and SEO; 6 trending celebrity mask photos attached first. Sex and City request mask ARCHIVED (owner asked).
- Mug sub-collections (done 6 Oct): new smart collection funny-number-plate-mugs (20 mugs, Online Store + Shop). 14 mug collections have new 1800x600 headers (`foxy.header_image`, live now) and `foxy.compact_header`; ALL MUGS has `foxy.subcollections`. 23 compact auto banners `foxy-header-<group>-compact.jpg` added to Files (originals kept). Theme copy "Foxy Pop 2026 – mug tiles" `189453861245` (duplicated from live "field fix", Infinite Options embed on) waits for the owner to publish. Record: `exports/mug-subheaders/manifest.json`.
- Rude number plate mugs: live (website and Shop only). Teaser ads in `exports/social/2026-10-06-rude-mugs/`, not posted.
- TikTok ads (mug, masks, Wales flag): made, not posted. See `exports/social/2026-10-06-tiktok-ads.md`.
- Amazon test (mug, hat, flag): `exports/amazon/2026-10-06-test/`; exporter `tools/amazon_export.py`.

## Connections
Shopify ✅ · Dropbox ✅ (never delete) · Google Drive ✅ · Gmail ✅ (drafts only, never send) · Higgsfield ✅ (TikTok needs the owner's form) · GitHub ✅ (works in Accept edits mode) · Postiz ⏳ (add custom connector `https://api.postiz.com/mcp/<API key>`) · eBay/Amazon/BigCommerce ❌ (CSV/xlsx files only).

## Known blocks (don't retry; ask the owner)
- Network policy blocks `*.dl.dropboxusercontent.com` (Dropbox file downloads, 403) as well as cdn.shopify.com. Owner can add both under the environment's Network access > Allowed domains. `tools/request_mask_hero.py` (Request a Facemask main image) is ready and waits on this.
- Shopify MCP blocks unpublish, bulk mutations, and probably delete.
- Uploading local files to Higgsfield from here is blocked, but the Higgsfield sandbox can download, edit and PUT files to a `media_upload` URL; then `fileCreate` from that Higgsfield URL. Shopify staged URLs must never go to Higgsfield.
- cdn.shopify.com, foxyprinting.co.uk and Higgsfield CloudFront are not reachable from this machine.
