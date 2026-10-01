# Foxyprinting.co.uk Rebrand

The rebrand of [foxyprinting.co.uk](https://www.foxyprinting.co.uk): a new Shopify theme, a review of the current catalogue, and a 153-line new product plan for the new UV, UV DTF, DTF and flatbed-cutter kit.

| Folder | What's in it |
|---|---|
| [`plan/strategy.md`](plan/strategy.md) | **Start here.** Catalogue review, what to fix, what each machine unlocks, launch waves, go-live checklist |
| [`plan/product-lines.md`](plan/product-lines.md) | All 153 new product lines by mega-menu department: machine, wave, trend score, options, RRP, personalisation |
| [`plan/new-products-shopify-import.csv`](plan/new-products-shopify-import.csv) | The same products as a Shopify product CSV (all drafts) |
| [`plan/catalogue.py`](plan/catalogue.py), [`plan/mega_menu.py`](plan/mega_menu.py) | Source data for the products and the mega menu. Edit these, then run `python3 tools/build_plan.py` |
| [`theme/`](theme) | **Foxy Pop** Shopify OS 2.0 theme: colourful Vistaprint-style layout, 3-level mega menu, live product personaliser |
| [`dist/foxy-pop-theme.zip`](dist) | Upload-ready theme zip (Online Store → Themes → Add theme → Upload zip) |
| [`preview/screenshots/`](preview/screenshots) | Screenshots of the theme rendered offline with sample data |
| [`tools/`](tools) | Plan builder, offline preview renderer, generated Admin API payloads |

## Already done in the Shopify store (all hidden from customers)
- **153 draft products** tagged `foxy-new-2026`, with prices, variants, unique SKUs, the `personalised` template and `foxy.mockup` / `foxy.personalise_fields` metafields that drive the live preview.
- **34 unpublished smart collections** (handles start `new-`), one per range, populated by `range-…` tags.
- **"Foxy Mega Menu"** navigation (handle `foxy-mega-menu`): 11 departments, 227 links mixing existing and new collections.

To undo: filter products by tag `foxy-new-2026` and delete them, delete the `new-…` collections, and delete the Claude Mega Menu.

## Rebuild
```bash
python3 tools/build_plan.py                 # regenerate CSV, product-lines.md and API payloads
cd tools/preview && npm i && python3 make_data.py && node render.mjs ../../preview/site   # offline preview
cd theme && zip -r ../dist/foxy-pop-theme.zip .   # repackage theme
```
