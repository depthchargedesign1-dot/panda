# Infinite Options – recommended option sets

Each new 2026 product carries one `io-<range>` tag. In Infinite Options, make **one option set per tag**, then use the condition "Product tag is equal to `io-…`" so the set applies to the whole range at once.

**Before you start:** the theme's built-in personaliser (Foxy Pop, `main-product.liquid`) already shows the fields in each product's `foxy.personalise_fields` metafield, with a live preview. Infinite Options is **optional**. Use it for paid add-ons (gift box, extra name, rush printing) or dropdowns. If you use both on one product, **turn one off** (clear the metafield, or exclude the product from the option set). Otherwise customers see every field twice.

How the theme reads labels (keep Infinite Options limits the same):

| Label contains | Field | Limit |
|---|---|---|
| photo, upload, logo, artwork, badge, crest | file upload | jpg/png/pdf |
| message, list, reasons, achievements | multi-line text | 160 |
| number, age | text | 3 |
| initials | text | 4 |
| slogan, team name, colours | text | 40 |
| anything else | text | 24 |
| *(the first label)* | **required** | |

Avoid "number" or "age" inside longer labels (e.g. say "Contact phone", not "Phone number"; "Numerals style", not "Number style"), because the theme would cut them to 3 characters.

Key: **T** = text box, **TA** = multi-line text, **F** = file upload, **D** = dropdown, **S** = colour swatch. `*` = required.

---

### io-photo-gifts (45): slates, metal panels, acrylic, clocks, frames, tiles, jigsaws, keyrings, magnets, coasters, plaques
- Photo upload* – F
- Name – T, 24
- Message – TA, 160
- Date – T, 24 (keepsakes, anniversaries, memorials)
- Clocks: Numerals style – D (Arabic / Roman / None)
- Optional paid add-on: Gift box – D (No / Yes +£)

### io-christmas (22): baubles, decorations, stockings, Christmas Eve boxes, Santa letters, jumpers, PJs
- Name* (or Child's name / Family name) – T, 24
- Year – T, 24 (pre-fill "2026")
- Message – TA, 160
- Photo upload – F (photo baubles, decorations and boxes only)
- Santa letter: Age – T, 3 · Achievements – TA, 160 · Town – T, 24 · Wish list – TA, 160
- Clothing: Size – D (from the product's variants, so don't duplicate it)

### io-drinkware (19): tumblers, glasses, bottles, travel cups, flasks
- Name* – T, 24
- Message – TA, 160
- Initials – T, 4
- Photo upload – F (not on clear glass where print is white-only)
- Pattern – D (sublimation range)
- Hip flask / flutes: Date – T, 24

### io-mugs (5)
- Name* (Names for couples' mugs) – T, 24
- Photo upload – F
- Message – TA, 160
- Date – T, 24

### io-business (19): business cards, flyers, stickers, labels, signs, review/QR stands, workwear, mailer boxes
- Artwork upload* (or Logo upload*) – F (PDF preferred)
- Business name – T, 24
- Contact details list – TA, 160
- Colours – T, 40, or S if you have fixed brand colours
- Print notes (message) – TA, 160
- Review / QR stands: Review link (message) / QR link (message) – TA, 160 (URLs are long)
- Vouchers: First voucher no. – T, 24 · Voucher value – T, 24
- Workwear: Staff name – T, 24 · Back text – T, 24
- Optional paid add-on: Design service – D (I have artwork / Design it for me +£)

### io-pets (12)
- Pet name* (or Pet photo*) – T, 24 / F
- Photo upload – F
- Message – TA, 160
- ID tags and bandanas: Contact phone – T, 24
- Memorial items: Dates – T, 24
- Pattern / Background colours – D or S

### io-kids-school (11): name labels, bottles, lunch boxes and bags, PE bags, pencil cases, kids' cups, placemats, tooth fairy tin
- Name* – T, 24
- Class – T, 24
- Icon – D (football, unicorn, dinosaur…)
- Theme – D
- Age – T, 3
- Message – TA, 160
- Photo upload – F (sublimated items only)

### io-party (10): cake and cupcake toppers, favour/treat/popcorn boxes, sashes, Halloween bags and boxes
- Name* (or Text* for sashes) – T, 24
- Age – T, 3
- Theme – D
- Colours – S
- Top line (e.g. Happy Birthday) – T, 24
- Message – TA, 160
- Logo upload – F (cupcake boxes for bakers)

### io-baby (9): bibs, vests, blankets, birth prints, keepsake boxes, milestone discs, scan plaques
- Name* (Baby's name) – T, 24
- Birth date – T, 24
- Weight / Birth weight – T, 24 · Time – T, 24 · Place of birth – T, 24
- Message – TA, 160
- Photo upload / Scan photo upload – F
- Colours – S (milestone discs)

### io-clothing (9): adult/kids tees, hoodies, sweatshirts, caps, sibling and Halloween tees
- Name* (or Photo/design upload*) – T, 24 / F
- Age or Number – T, 3
- Slogan / Slogan text – T, 40
- Photo upload / Design upload – F
- Initials – T, 4 (sweatshirts)
- Print position – D (Front / Back / Both +£)

### io-home-textiles (8): cushions, blankets, tea towels, aprons, tote bags
- Photo upload* (or Name*) – F / T, 24
- Name – T, 24
- Message (or Recipe/Message) – TA, 160
- Date – T, 24
- Aprons: Title e.g. Head Chef – T, 24

### io-home-gifts (6): slate house signs, cheese and chopping boards, bottle openers, candles, sweet jars
- Name* / Family name* / House number* – T
- Est. year – T, 24
- Message – TA, 160
- Photo or Recipe/handwriting upload – F
- House sign: House name, Street name – T, 24 · Design – D
- Sweet jar: Label text – T, 24 · Fill – D (Empty / Filled +£)

### io-weddings (6): favour boxes, welcome signs, table numbers, place names, invitations, photo booth props
- Names* (Couple's names) or Guest names list* – T, 24 / TA
- Wedding date – T, 24
- Venue – T, 24
- RSVP details – T, 24
- Message – TA, 160
- Colours – S
- Table numbers or names list – TA, 160

### io-occasions (6): Valentine's, Mother's Day, Easter
- Name* / Names* – T, 24
- Message – TA, 160
- Age – T, 3 (Easter)
- Date / Anniversary date – T, 24
- Reasons list – TA, 160 (Reasons jar)
- Photo upload – F (slate heart)

### io-plush-toys (5): teddies, bunnies, plush keyrings
- Name* – T, 24
- Message / Short message – TA, 160
- Date / Date of birth – T, 24
- Photo upload – F (printed t-shirt only)
- Initials – T, 4 (bunny keyring)

### io-golf-darts (5): golf balls, ball markers, gift sets/boxes, dart flights
- Name* (or Photo/logo upload*) – T, 24 / F
- Initials – T, 4
- Message – TA, 160 (gift box lid)
- Nickname – T, 24 · Colours – S (dart flights)

### io-tech-accessories (5): phone cases, chargers, power banks, mirrors, notebooks
- Photo upload* (or Name*) – F / T, 24
- Name – T, 24
- Message – TA, 160
- Initials – T, 4 (mirror, notebook)
- Phone model – D (only if it isn't already a variant)

### io-gaming (4): custom game cases, game case cards, controller and laptop skins
- Photo upload* – F
- Name – T, 24
- Game title – T, 24 (made-up title text, no real game logos)
- Age – T, 3 (card) · Inside message – TA, 160
- Gamer tag – T, 24 (skins)

### io-awards (3): medal inserts, acrylic trophies, round award plaques
- Club logo upload* / Logo upload* (or Name*) – F
- Award title – T, 24
- Winner name – T, 24
- Season or year – T, 24
- Event date – T, 24 (medals)

### io-teamwear (3): school leavers hoodies, club hoodies, kit name and number printing
- School name* / Logo upload* / Name* – T, 24 / F
- Year – T, 24
- Class names list – TA, 160 (if more than 160 characters, ask for a file upload)
- School badge upload / Logo upload – F
- Number – T, 3 · Team name – T, 40 · Colours – S

### io-trade-transfers (3): UV DTF cup wraps, UV DTF and DTF gang sheets
- Artwork upload* – F (PNG with transparent background, 300 dpi)
- Quantity of each design – T, 24
- Print notes (message) – TA, 160

### io-gift-boxes (2): letterbox gift box, gift tags
- Name* / From name* – T, 24
- To name – T, 24
- Message – TA, 160
- Photo upload – F (letterbox box)

### io-cards-adult (1): pop-up 3D birthday card
- Name* – T, 24
- Age – T, 3
- Front message – TA, 160
- Inside message – TA, 160
- Envelope colour – S (optional)

*`io-cards-kids` is reserved for kids' birthday cards (Child's name*, Age, Message (inside), Photo upload), but no 2026 product uses it yet.*

---

**Not tagged:** Mug Gift Box Add-On and Bauble Gift Box Add-On. They are plain packaging, not personalised, so they need no option set. Offer them as a paid "Add a gift box" dropdown in the mug and bauble sets instead.

**Football range:** `foxy-src-football` products use `io-football` and are managed separately.
