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
| 12 | Mug header images: OK the rude-mugs banner? Allow Higgsfield sandbox so I can check and crop images? (theme tiles need a new theme copy; field fix went live 6 Oct) | mug collection headers + tiles |
| 13 | Connect Postiz as a Claude connector (see below) | posting to FB, IG and TikTok |

## Owner's import queue (one file each morning and bedtime; reminders run 07:52 and 21:52 UK)
See `exports/IMPORT-SCHEDULE.md`. Order: SEO 02-CLEAN → age 01 → age 02-CLEAN → masks TEST then 01–04 → prints TEST then 01–04.

## Running or recently finished
- Mug sub-collections: new collection funny-number-plate-mugs (20 mugs) live; 12 header images generated in Higgsfield, not uploaded (paused: sandbox denied). Tiles need a new theme copy.
- Rude number plate mugs: live (website and Shop only). Teaser ads in `exports/social/2026-10-06-rude-mugs/`, not posted.
- TikTok ads (mug, masks, Wales flag): made, not posted. See `exports/social/2026-10-06-tiktok-ads.md`.
- Amazon test (mug, hat, flag): `exports/amazon/2026-10-06-test/`; exporter `tools/amazon_export.py`.

## Connections
Shopify ✅ · Dropbox ✅ (never delete) · Google Drive ✅ · Gmail ✅ (drafts only, never send) · Higgsfield ✅ (TikTok needs the owner's form) · GitHub ✅ (works in Accept edits mode) · Postiz ⏳ (add custom connector `https://api.postiz.com/mcp/<API key>`) · eBay/Amazon/BigCommerce ❌ (CSV/xlsx files only).

## Known blocks (don't retry; ask the owner)
- Shopify MCP blocks unpublish, bulk mutations, and probably delete.
- Uploading our own files to Higgsfield is blocked; Shopify Files (staged upload from here) → public CDN URL → Higgsfield import works.
- cdn.shopify.com, foxyprinting.co.uk and Higgsfield CloudFront are not reachable from this machine.
