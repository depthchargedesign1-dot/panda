# AI pet portrait preview: plan

**Goal (owner, 2 Oct 2026):**
1. The customer uploads a photo of their cat or dog on a pet portrait product (e.g. "Your pet as Churchill").
2. An AI puts *their* pet into that character's artwork.
3. They see a **watermarked** preview, so it can't be downloaded and used for free.
4. They order the size and frame they want.
5. The order carries the clean, full-resolution image for printing.

**Phase 1 (live now in the drafts):** the product has a "Pet photo upload" field. The team makes the portrait and emails a proof. Nothing below is needed for this to work.

## Phase 2: how the AI preview works

```
Customer's browser (Foxy Pop product page)
  │ 1. uploads pet photo + picks character/version
  ▼
Shopify App Proxy  (/apps/pet-preview  → keeps the API key off the page)
  │
  ▼
Small server (Cloudflare Worker or Vercel function)
  │ 2. checks rate limit (e.g. 3 previews per visitor per hour)
  │ 3. sends pet photo + character artwork + prompt to an image AI
  │ 4. stores the CLEAN result privately (e.g. Cloudflare R2 / S3)
  │ 5. returns a small WATERMARKED, low-res preview + a preview ID
  ▼
Product page shows the preview; "Add to basket" saves the preview ID
as a line item property (e.g. _pet_preview_id) → appears on the order
  │
  ▼
Fulfilment: team (or a Flow / webhook) uses the preview ID to fetch the
clean full-resolution file for printing
```

### Pieces to build
| Piece | What it does | Where |
|---|---|---|
| Theme snippet `pet-preview.liquid` + JS | Upload box, "Create my preview" button, spinner, watermarked result, preview ID saved to the cart | Foxy Pop theme (unpublished) |
| App proxy | Lets the page call our server on foxyprinting.co.uk without exposing keys | Shopify custom app (Partner or store-created app) |
| Preview server | Calls the AI, adds the watermark (e.g. diagonal "FOXY PRINTING – PREVIEW" tiles), stores the clean file, rate-limits | Cloudflare Worker (cheap and fast) or Vercel |
| Storage | Keeps clean files for e.g. 30 days | Cloudflare R2 or S3 |
| Order link | Clean-file link attached to the order (metafield or note) | Shopify Flow or an orders/create webhook |

### Image AI options
These all accept a reference image plus an instruction such as "put this dog's face into this Churchill portrait in the same painted style":
- An image-editing model through an API (e.g. OpenAI image edits, Google Gemini image, or a Replicate model). Cost is roughly a few pence per preview at preview resolution.
- Higgsfield (already used for product photos) can do this in our workflow, but it isn't designed to be called from a public website. Check its API terms before using it for customer previews.

### Safeguards
- Watermark and low resolution on everything the browser sees. The clean file is never sent to the browser.
- Rate limits and a simple bot check stop people running up AI costs.
- Accept only images (jpg/png/heic). Reject anything that isn't a pet. Most image APIs also have their own safety filters.
- Privacy: say in the product description and privacy policy that uploaded photos are used only to make the preview and order, and are deleted after N days.

## What we need from the owner
1. Pick the **AI provider** and create an API key (or let Claude recommend one after a quick test with the 8 sample pet photos in Dropbox `PET PORTRAITS - Copy/PET IMAGES`).
2. A **Cloudflare** (or Vercel) account for the small server and storage. The free or low tiers are enough to start.
3. Agreement to create a **custom app** in Shopify admin (Settings → Apps → Develop apps) for the app proxy.
4. A budget cap per month for AI previews.

When those are ready, Claude can write the server, theme snippet and app config, test with the sample pet photos, and leave it switched off on the live theme until the owner approves.
