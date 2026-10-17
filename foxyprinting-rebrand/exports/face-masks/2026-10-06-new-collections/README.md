# New mask collections (6 Oct 2026)

Owner asked for three new face mask collections. All are smart collections (one TAG equals rule), sorted Best selling, published to Online Store, Shop, Google & YouTube, Facebook & Instagram and TikTok (the collections only; the celebrity products themselves stay website-only as before).

| Collection | ID | Handle / URL | Rule | Products |
|---|---|---|---|---|
| YouTuber & Influencer Face Masks | `gid://shopify/Collection/690588123517` | https://foxyprinting.co.uk/collections/youtuber-influencer-face-masks | tag `youtuber-masks` | 77 |
| K-Pop Face Masks | `gid://shopify/Collection/690588156285` | https://foxyprinting.co.uk/collections/k-pop-face-masks | tag `kpop-masks` | 56 |
| The Traitors Face Masks | `gid://shopify/Collection/690588189053` | https://foxyprinting.co.uk/collections/the-traitors-face-masks | tag `traitors-masks` | 27 |

Counts re-checked after tagging (all ACTIVE). Product IDs: `product-ids.json`. Copy, SEO title and meta: `collection-content.json`.

## How products were picked
- **YouTubers & influencers:** the two 2025 creator batches (Sidemen, Mr Beast, Logan/Jake Paul, streamers, TikTok stars, golf and Minecraft YouTubers), plus older influencer masks (Alexis Ren, Amanda Cerny, Amanda Steele, Cameron Dallas, Bethany Mota, Nella Rose, Yung Filly, Deji, Molly-Mae Hague, Jack Joseph, Cole Anderson-James). Left out: Hide the Pain Harold (meme), Joe Rogan (podcaster), Bianca Censori, Ronan Moloney (not sure he's a creator), athletes and Love Island cast.
- **K-pop:** every mask with `k-pop` in the handle (BLACKPINK, Seventeen, ATEEZ, ENHYPEN, TXT, LE SSERAFIM, P1Harmony, KATSEYE) plus the BTS Jungkook/Jimin mask. Squid Game actors and Kim Jong Un excluded.
- **The Traitors:** store searched for every Celebrity Traitors 2025 and 2026 cast member, host Claudia Winkleman and the civilian winners/finalists. Found: Claudia Winkleman (3), Alan Carr (2), Jonathan Ross, Joe Marler, Nick Mohammed, Stephen Fry (3), Tom Daley (2), Clare Balding (2), Bella Ramsey, James Acaster, James Blunt, Joe Lycett, Julie Hesmondhalgh (2, incl. the Mr Bates mask), Leigh-Anne Pinnock (2), Miranda Hart (2), Ross Kemp, Sebastian Croft.
  - No mask yet (gaps to make): Maya Jama, Romesh Ranganathan, Michael Sheen, Richard E. Grant, Rob Beckett, Jerry Hall, Hannah Fry, Amol Rajan, Joanne McNally, King Kenny, Sharon Rooney, Myha'la; 2025: Cat Burns, Celia Imrie, Charlotte Church, David Olusoga, Elis James, Joe Wilkinson, Kate Garraway, Lucy Beaumont, Mark Bonnar, Niko Omilana, Paloma Faith, Ruth Codd, Tameka Empson; civilians: Harry Clark, Wilf Webster, Leanne Quigley, Jake Brown, Rachel Duffy, Stephen Libby and others.
- Every tagged product also got `third-party-name` (house rule) if it was missing.
- New masks from other sessions join automatically once they carry the tag (e.g. the 5 BTS members need `kpop-masks`; any new Traitors or creator masks need `traitors-masks` / `youtuber-masks`).

## Content
- 170–180 word UK English description each, primary keyword in the first sentence, specs from `plan/product-facts.md` (350gsm silk card, A4 297 x 210 mm, Ready Cut or DIY, elastic and tabs or stick and stickers supplied to attach, board-backed envelope, North Yorkshire), and a one-line unofficial-novelty note.
- SEO titles 37–48 characters; meta descriptions 147–154 characters.

## Header banners
No bespoke banners: `tools/collection_headers.py` / `banner_compact.py` only crop or pad existing photo banners, they can't make text-only ones. Each collection uses the existing masks banner: `foxy.header_image` = `foxy-header-masks-compact.jpg` (`gid://shopify/MediaImage/69872791224701`, 1800x600) and `foxy.compact_header` = true, the same setup as the mug sub-collections.

## Menu
"Celebrity Face Masks" menu (`gid://shopify/Menu/229551752`, handle `celebrity-face-masks`): the three collections were added after "Comedians". All 8 existing items were kept unchanged and re-read afterwards. Backup of the menu before the edit: `menu-celebrity-face-masks-before.json`. The main menu (Shop by category) was not changed.
