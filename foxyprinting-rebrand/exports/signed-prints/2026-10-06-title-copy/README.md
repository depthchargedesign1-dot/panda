# Printed-signature prints: new titles and descriptions (6 Oct 2026)

These files carry the owner's decisions of 6 October 2026 for the **13,434** poster and print listings whose title ended in "– Reproduction Print".

## What changes

**Titles.** "– Reproduction Print" comes off the end. "Printed Signature" stays. No new title contains "signed", "autographed", "limited edition" or "Reproduction Print".

| Before | After |
|---|---|
| Kunal Nayyar Printed Signature Movie Star Poster Print Framed Wall Art Gift – Reproduction Print | Kunal Nayyar Printed Signature Movie Star Poster Print Framed Wall Art Gift |
| Dave Grohl 1 – Printed Signature Music Star Print – Reproduction Print | Dave Grohl 1 – Printed Signature Music Star Print |
| Tyrone Crawford 2 American Football Printed Signature Print – Reproduction Print | Tyrone Crawford 2 American Football Printed Signature Print |

**Descriptions.** The changes are kept small:
- Wording such as "Limited Edition Signed Print", "Signed Print", "Printed Signed Poster", "Signed Autographed Merch", "autographed", "genuine autograph", "signed by" and "memorabilia" now says "print with a printed signature", "Printed Signature" or "wall art". For example, "A Limited Edition Signed Print by your amazing Football Star." now reads "A print of your amazing Football Star, with a printed signature." That fixes all 2,549 "limited edition signed print" descriptions. Hashtags such as #SignedMemorabilia and #AutographedPrint are removed.
- A new line after the first paragraph: *"This is a high-quality reproduction print – the signature is printed as part of the design."* It went into 7,795 descriptions. The other 5,587 already say "reproduction" near the top (for example "A Digital Reproduction of…"), so they didn't need it.
- The signed-print disclaimer appears once, at the end, under **Please note**. 12,489 descriptions get it added. The 893 that already had it are left as they were, together with any club or player wording they had.
- The 3,551 products sold with frame options (Black, Silver, Gold or White frame) get a short line about our **Premium Display frames: thick, chunky and very professional, not cheap thin frames**. There are five wordings, so the line isn't identical on every product. No frame sizes or materials are claimed.
- Font-size styling is removed only from paragraphs that were edited.

**Unchanged:** prices, images, tags, SEO title and description, handles (URLs), variants and status. Each file's Status column holds the product's **current** status: 13,408 active, 22 archived, 3 draft and 1 unlisted.

52 posters (the retro club-colour posters and the "Champions of England Liverpool 2020" posters) had "Reproduction Print" in their title but aren't signature prints. For those, **only the title changes**.

## Files

| File | Products | Rows | Size |
|---|---:|---:|---:|
| `00-TEST-3-products.csv` | 3 | 22 | 14 KB |
| `01-signed-prints.csv` | 3,694 | 28,574 | 10.8 MB |
| `02-signed-prints.csv` | 3,877 | 5,794 | 12.9 MB |
| `03-signed-prints.csv` | 3,992 | 3,992 | 12.8 MB |
| `04-signed-prints.csv` | 1,871 | 1,922 | 8.2 MB |

There is one row per variant. The first row of each product carries the Title, Status and Body. The other rows carry only the Handle, the size option and the SKU, so that Shopify keeps every size and frame option. The 3 test products are also in the main files, and importing them twice does no harm.

`before-after-titles.csv` lists every old and new title. `follow-up-claims.csv` lists products that need a later rewrite (see below).

## How to import: do this LAST

**Import these files after the other pending imports.** The SEO files (`exports/seo/2026-10-06-remaining/01-seo.csv` and then `02-seo-CLEAN.csv`) and the age-group files (`exports/google-fields/2026-10-06-age-group-remaining/01-age-group-gender.csv` and then `02-age-group-gender-CLEAN.csv`) all carry a Title column.

`02-seo-CLEAN.csv` and both age-group files have already been changed to use the **new** titles. Originals are saved next to them as `*.bak-before-title-fix`. `01-seo.csv` was left alone because it was already being imported, so it still has the old "– Reproduction Print" titles for 6,392 products. Importing these signed-print files last puts the right titles back.

1. Shopify admin → **Products** → **Import**.
2. Choose `00-TEST-3-products.csv`, tick **"Overwrite products with matching handles"**, and import.
3. Open the 3 products: A. J. Green, Jos Buttler and Donald "Cowboy" Cerrone. Check that:
   - the title has no "Reproduction Print";
   - the description has the reproduction line near the top and "Please note" at the bottom;
   - every size and frame option, price and image is still there.
4. If they look right, import `01-signed-prints.csv`, `02-signed-prints.csv`, `03-signed-prints.csv` and `04-signed-prints.csv`, one at a time, with the same box ticked.

Don't import the old `02-seo.csv` or `02-age-group-gender.csv` (the non-CLEAN files). They still have the old titles.

## Still to do (owner)
- `follow-up-claims.csv`: 2,708 descriptions are older long "article" copy that still makes claims a printed reproduction can't make. Examples are "comes with a certificate of authenticity", "genuine", "authentic", "officially licensed", "limited availability" and "investment". Swapping words wouldn't fix these safely, because the sentences themselves are untrue. They need a proper rewrite. The new disclaimer is now at the end of each one.
- About 9,880 single-option prints describe frame choices ("framed or un-framed … Sleek Black or Classy Silver Frames") but can only be bought as one option. They did not get the Premium Display frame line.
- Frame material and depth are still **ASK**.

Rebuild: `python3 tools/signed_prints_copy.py <bulk export .jsonl> <out dir>`. The export needs `id handle title status productType descriptionHtml options{name values} variants{title sku}`.
