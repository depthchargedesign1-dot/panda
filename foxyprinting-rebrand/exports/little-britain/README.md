# Little Britain face masks (6 Oct 2026)

## Store search (existing products, not recreated)
| Mask | Product | Notes |
|---|---|---|
| Vicky Pollard | gid://shopify/Product/9369892744 `vicky-pollard-face-mask` | ACTIVE, house copy; disclaimer uses the celebrity template, no `third-party-name` tag |
| Lou Todd | gid://shopify/Product/8125539352827 `lou-little-britain-celebrity-face-mask-fancy-dress-cardboard-costume-mask` | ACTIVE, OLD-style copy (inline styles, phone number, img), no disclaimer |
| Andy Pipkin | gid://shopify/Product/9530634184 `andy-pipkins-celebrity-face-mask` | ACTIVE, title spelt "Pipkins", copy calls him a "film star" |
| Bubbles DeVere | gid://shopify/Product/9530648776 `bubbles-de-celebrity-face-mask` | ACTIVE, title "Bubbles De" |
| Matt Lucas | gid://shopify/Product/8249158926587 | ACTIVE, house copy |
| David Walliams | 8225435910395, 9530620744, 9530623624, 4328415592523 | ACTIVE; 9530623624 + 4328415592523 copy wrongly says Walliams plays Andy (he plays Lou) |
| Little Britain 3-pack (Lou, Andy, Vicky) | 8125549805819 (£5.99), 8195091595515 (£5.90) | duplicates of each other, old copy |

No source artwork in Dropbox for Marjorie Dawes, Daffyd Thomas, Emily Howard or Carol Beer, so they were not made.
Ting Tong not made (CLAUDE.md: no racial caricature products).

## Created
| Product | ID | SKUs | Price (RTW / DIY) |
|---|---|---|---|
| Lou and Andy Couple Face Mask Pair | gid://shopify/Product/16063694635389 | FaceMask-LouAndAndyPair / -DIY | £4.99 / £2.99 |
| Little Britain Characters Face Mask Pack (Vicky, Lou, Andy, Bubbles) | gid://shopify/Product/16063694668157 | FaceMask-LittleBritainCharactersPack / -DIY | £7.99 / £4.99 |

Images: built by `lb_build.py` in the Higgsfield sandbox from the owner's existing Dropbox artwork (no AI faces).
The party image is an AI-generated empty party table (no people) with the real mask artwork composited on it.
Print/cut artwork: `tools/artwork/mask_cutline.py --eyes-json` (eye centres from `lb_build.py`), zipped to Shopify Files:
- https://cdn.shopify.com/s/files/1/1774/9115/files/lou-and-andy-couple-mask-pair-artwork.zip?v=1791276348 (md5 411d7aae09214932a88e54ecd479f4c1)
- https://cdn.shopify.com/s/files/1/1774/9115/files/little-britain-characters-face-mask-pack-artwork.zip?v=1791276348 (md5 6424a7200631beaad994c3d9895aaf0f)

Source resolution at A4: Vicky and Andy 300 dpi; Lou ~100 dpi; Bubbles ~48 dpi (best available). Bleed beyond cut: 2 mm (tool default).

## Run
`run_sandbox.sh BG_PAIR_URL BG_PACK_URL` in the Higgsfield sandbox with `targets.json` (Shopify staged PUT URLs).

## Fonts
The production artwork (print/cut PDFs and SVGs, both masks in the pair and all four in the pack) uses **no fonts**: only the face image and vector cut lines.
So no `Fonts/` subfolder is needed in the Dropbox folders. The listing photos (`-mask-01`, `-02-back`, `-03-front-back`) have labels in Montserrat Bold/Regular (SIL OFL 1.1, Google Fonts), but they are flattened JPEGs, not editable artwork.

## Copy fixes (6 Oct 2026, `copy-fixes/`)
`before.json` (live state), `build.py` (new copy + checks), `after.json`, `mutation.graphql` + `mutation-variables.json` (one aliased productUpdate/tagsAdd push), `verify.json` (re-read).
- Character masks (Vicky, Lou, Andy, Bubbles): combined disclaimer (Little Britain, BBC, Matt Lucas, David Walliams). Lou fully rewritten in house format; Andy and Bubbles rewritten (no "film star"/"Oscars"; "Pipkin").
- David Walliams: 9530623624 + 4328415592523 now say he played Lou; 8225435910395 rewritten from old copy; 9530620744 SEO no longer has "Little Britain"; disclaimers say "him".
- `third-party-name` added to 9530623624, 4328415592523, 8225435910395, 8249158926587 (Matt Lucas).
- 3-packs (8125549805819, 8195091595515) untouched.
