/*
 * Foxy Leavers Designer — rendering engine.
 *
 * Shared by the product-page designer, the staff Print Studio and the command-line renderer, so the
 * customer's preview, their proof and the 300 dpi print file are the same drawing at different sizes.
 *
 * Every print area is laid out in a fixed reference space 1000 units wide (height follows the area's
 * real proportions). Text is measured once at 100px and scaled, so layout never depends on output size.
 */
(function (root) {
  'use strict';

  var REF = 1000;

  /* ------------------------------------------------------------------ catalogue */

  var FONTS = [
    { name: 'Anton', weight: 400, cat: 'Bold' },
    { name: 'Bebas Neue', weight: 400, cat: 'Bold' },
    { name: 'Oswald', weight: 700, cat: 'Bold' },
    { name: 'Archivo Black', weight: 400, cat: 'Bold' },
    { name: 'Montserrat', weight: 800, cat: 'Bold' },
    { name: 'Russo One', weight: 400, cat: 'Bold' },
    { name: 'Graduate', weight: 400, cat: 'Varsity' },
    { name: 'Alfa Slab One', weight: 400, cat: 'Varsity' },
    { name: 'Bungee', weight: 400, cat: 'Varsity' },
    { name: 'Black Ops One', weight: 400, cat: 'Varsity' },
    { name: 'Saira Stencil One', weight: 400, cat: 'Varsity' },
    { name: 'Pacifico', weight: 400, cat: 'Script' },
    { name: 'Lobster', weight: 400, cat: 'Script' },
    { name: 'Great Vibes', weight: 400, cat: 'Script' },
    { name: 'Dancing Script', weight: 700, cat: 'Script' },
    { name: 'Satisfy', weight: 400, cat: 'Script' },
    { name: 'Kaushan Script', weight: 400, cat: 'Script' },
    { name: 'Yellowtail', weight: 400, cat: 'Script' },
    { name: 'Permanent Marker', weight: 400, cat: 'Fun' },
    { name: 'Bangers', weight: 400, cat: 'Fun' },
    { name: 'Luckiest Guy', weight: 400, cat: 'Fun' },
    { name: 'Fredoka', weight: 700, cat: 'Fun' },
    { name: 'Caveat', weight: 700, cat: 'Fun' },
    { name: 'Playfair Display', weight: 900, cat: 'Classic' },
    { name: 'Abril Fatface', weight: 400, cat: 'Classic' },
    { name: 'Cinzel', weight: 700, cat: 'Classic' }
  ];
  var FONT_BY_NAME = {};
  FONTS.forEach(function (f) { FONT_BY_NAME[f.name] = f; });

  // Print (ink / DTF film) colours.
  var INKS = [
    { id: 'white', name: 'White', hex: '#FFFFFF' },
    { id: 'black', name: 'Black', hex: '#141414' },
    { id: 'gold', name: 'Gold', hex: '#C9A227' },
    { id: 'silver', name: 'Silver', hex: '#B9BFC7' },
    { id: 'hot-pink', name: 'Hot Pink', hex: '#FF2D87' },
    { id: 'baby-pink', name: 'Baby Pink', hex: '#F7B3CD' },
    { id: 'red', name: 'Red', hex: '#D7182A' },
    { id: 'orange', name: 'Orange', hex: '#FF6A13' },
    { id: 'yellow', name: 'Yellow', hex: '#FFD23F' },
    { id: 'lime', name: 'Neon Lime', hex: '#B6F23A' },
    { id: 'green', name: 'Green', hex: '#1E9E4A' },
    { id: 'teal', name: 'Teal', hex: '#00B8A9' },
    { id: 'sky', name: 'Sky Blue', hex: '#6EC6F0' },
    { id: 'royal', name: 'Royal Blue', hex: '#1F4FC1' },
    { id: 'navy', name: 'Navy', hex: '#14213D' },
    { id: 'purple', name: 'Purple', hex: '#7A2BF5' }
  ];

  // AWDis Just Hoods colours (approximate screen shades of the supplier swatches).
  var GARMENTS = [
    { id: 'arctic-white', name: 'Arctic White', hex: '#F3F3F1' },
    { id: 'jet-black', name: 'Jet Black', hex: '#1C1C1F' },
    { id: 'deep-black', name: 'Deep Black', hex: '#0E0E10' },
    { id: 'charcoal', name: 'Charcoal', hex: '#3B3E44' },
    { id: 'storm-grey', name: 'Storm Grey', hex: '#5D6269' },
    { id: 'heather-grey', name: 'Heather Grey', hex: '#A8AAAF' },
    { id: 'oxford-navy', name: 'Oxford Navy', hex: '#1F2A44' },
    { id: 'french-navy', name: 'New French Navy', hex: '#1A2140' },
    { id: 'ink-blue', name: 'Ink Blue', hex: '#26344F' },
    { id: 'royal-blue', name: 'Royal Blue', hex: '#2149A6' },
    { id: 'sapphire', name: 'Sapphire Blue', hex: '#1677C6' },
    { id: 'airforce-blue', name: 'Airforce Blue', hex: '#5B7DA8' },
    { id: 'hawaiian-blue', name: 'Hawaiian Blue', hex: '#13A0D0' },
    { id: 'sky-blue', name: 'Sky Blue', hex: '#8CC5E8' },
    { id: 'fire-red', name: 'Fire Red', hex: '#C3132C' },
    { id: 'red-hot-chilli', name: 'Red Hot Chilli', hex: '#A3172C' },
    { id: 'burgundy', name: 'Burgundy', hex: '#6B1A2C' },
    { id: 'hot-pink', name: 'Hot Pink', hex: '#E2317D' },
    { id: 'candyfloss-pink', name: 'Candyfloss Pink', hex: '#F49AC1' },
    { id: 'baby-pink', name: 'Baby Pink', hex: '#F4C3D5' },
    { id: 'purple', name: 'Purple', hex: '#4B2A82' },
    { id: 'lavender', name: 'Lavender', hex: '#BBA8DB' },
    { id: 'kelly-green', name: 'Kelly Green', hex: '#1F8A3D' },
    { id: 'bottle-green', name: 'Bottle Green', hex: '#1E4A34' },
    { id: 'olive-green', name: 'Olive Green', hex: '#5A5C3A' },
    { id: 'jade', name: 'Jade', hex: '#1B9C88' },
    { id: 'mint', name: 'Mint', hex: '#A6DBC6' },
    { id: 'sun-yellow', name: 'Sun Yellow', hex: '#F4C20D' },
    { id: 'gold', name: 'Gold', hex: '#E0A526' },
    { id: 'orange-crush', name: 'Orange Crush', hex: '#F06A22' },
    { id: 'desert-sand', name: 'Desert Sand', hex: '#D7C2A0' },
    { id: 'nude', name: 'Nude', hex: '#D8B6A0' },
    { id: 'caramel-latte', name: 'Caramel Latte', hex: '#A7805C' },
    { id: 'hot-chocolate', name: 'Hot Chocolate', hex: '#4A3227' },
    { id: 'white', name: 'White', hex: '#FAFAF8' }
  ];
  var COLLEGE_COLOURS = GARMENTS.filter(function (g) { return g.id !== 'gold' && g.id !== 'white'; });

  // Two-tone garments come in fixed body / contrast colourways (body first, as AWDis names them).
  function ways(list) {
    return list.map(function (pair) { return { body: pair[0], trim: pair[1] }; });
  }

  /*
   * Garments. Print areas are in millimetres; k is mockup pixels per mm.
   * colours: a list of single colours, or `colourways` of body + contrast (sleeves etc.).
   */
  // Print areas in millimetres. The adult back is the full 40 x 50 cm press.
  var ADULT_AREAS = {
    back: { w: 400, h: 500, label: 'Back' },
    chest: { w: 100, h: 100, label: 'Front left chest' },
    centre: { w: 300, h: 220, label: 'Front centre' },
    personal: { w: 90, h: 40, label: 'Front right chest' },
    sleeve: { w: 70, h: 400, label: 'Left sleeve' }
  };
  var KIDS_AREAS = {
    back: { w: 300, h: 375, label: 'Back' },
    chest: { w: 80, h: 80, label: 'Front left chest' },
    centre: { w: 230, h: 170, label: 'Front centre' },
    personal: { w: 75, h: 34, label: 'Front right chest' },
    sleeve: { w: 55, h: 300, label: 'Left sleeve' }
  };
  var KIDS_SIZES = ['3-4 yrs', '5-6 yrs', '7-8 yrs', '9-11 yrs', '12-13 yrs'];

  /*
   * photo: where each print area sits on the real garment photos (1000 x 1000, drawn at y + 50 in the
   * 1000 x 1100 preview), and k = photo pixels per millimetre of print.
   */
  var PRODUCTS = {
    'college-hoodie': {
      name: 'College Hoodie 2.0', code: 'JH001', mockup: 'hoodie', k: 0.97, areas: ADULT_AREAS, kidsAreas: KIDS_AREAS,
      blurb: '280gsm, 80% ringspun cotton / 20% polyester, double-layer hood, kangaroo pocket.',
      colours: COLLEGE_COLOURS,
      sizes: KIDS_SIZES.concat(['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']), price: 18.99,
      upcharge: { '3-4 yrs': -3, '5-6 yrs': -3, '7-8 yrs': -3, '9-11 yrs': -3, '12-13 yrs': -3, '2XL': 2, '3XL': 2, '4XL': 4, '5XL': 4 },
      photo: {
        k: 0.95,
        back: { view: 'back', cx: 500, top: 308 },
        chest: { view: 'front', cx: 622, top: 252 },
        centre: { view: 'front', cx: 500, top: 236 },
        personal: { view: 'front', cx: 380, top: 262 },
        sleeve: { view: 'front', line: [772, 330, 800, 860], t: 0.5 }
      }
    },
    'baseball-hoodie': {
      name: 'Baseball Hoodie', code: 'JH009', mockup: 'baseball', k: 0.97, areas: ADULT_AREAS,
      blurb: '280gsm two-tone hoodie with contrast raglan sleeves and contrast hood lining.',
      colourways: ways([
        ['jet-black', 'fire-red'], ['jet-black', 'gold'], ['jet-black', 'sapphire'], ['jet-black', 'arctic-white'],
        ['charcoal', 'jet-black'], ['charcoal', 'heather-grey'], ['heather-grey', 'jet-black'],
        ['heather-grey', 'oxford-navy'], ['oxford-navy', 'heather-grey'], ['oxford-navy', 'burgundy'],
        ['arctic-white', 'jet-black'], ['burgundy', 'charcoal'], ['baby-pink', 'heather-grey']
      ]),
      sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL'], price: 21.99, upcharge: { '2XL': 2 },
      photo: {
        k: 0.92,
        back: { view: 'back', cx: 500, top: 250 },
        chest: { view: 'front', cx: 600, top: 262 },
        centre: { view: 'front', cx: 500, top: 250 },
        personal: { view: 'front', cx: 395, top: 272 },
        sleeve: { view: 'front', line: [745, 330, 775, 880], t: 0.5 }
      }
    },
    'varsity-jacket': {
      name: 'Varsity Jacket', code: 'JH043', mockup: 'varsity', k: 0.97,
      areas: {
        back: { w: 400, h: 480, label: 'Back' },
        chest: ADULT_AREAS.chest,
        personal: ADULT_AREAS.personal,
        sleeve: { w: 70, h: 380, label: 'Left sleeve' }
      },
      blurb: '280gsm varsity jacket with contrast sleeves, striped ribbed collar, cuffs and hem, and popper fastening.',
      colourways: ways([
        ['jet-black', 'white'], ['jet-black', 'fire-red'], ['jet-black', 'sun-yellow'], ['jet-black', 'hot-pink'],
        ['jet-black', 'heather-grey'], ['jet-black', 'charcoal'], ['oxford-navy', 'white'], ['oxford-navy', 'heather-grey'],
        ['oxford-navy', 'burgundy'], ['burgundy', 'heather-grey'], ['fire-red', 'white'], ['royal-blue', 'white'],
        ['sapphire', 'heather-grey'], ['kelly-green', 'white'], ['purple', 'white'], ['heather-grey', 'white']
      ]),
      sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL'], price: 29.99, upcharge: { '2XL': 2 },
      photo: {
        k: 0.88,
        back: { view: 'back', cx: 495, top: 232 },
        chest: { view: 'front', cx: 592, top: 262 },
        personal: { view: 'front', cx: 405, top: 275 },
        sleeve: { view: 'front', line: [760, 300, 830, 800], t: 0.5 }
      }
    }
  };
  var DEFAULT_PRODUCT = 'college-hoodie';

  // The colour choices for a garment: [{ id, name, body, trim }] (hex values).
  function photoSet() { return root.LEAVERS_PHOTOS || null; }

  function colourOptions(productKey) {
    var key = PRODUCTS[productKey] ? productKey : DEFAULT_PRODUCT;
    var p = PRODUCTS[key], ph = photoSet();
    if (ph && ph.products[key]) {
      return ph.products[key].map(function (c) {
        return { id: c.id, name: c.name, body: c.hex, trim: c.trim || c.hex, front: ph.base + c.front, back: ph.base + c.back };
      });
    }
    if (p.colourways) {
      return p.colourways.map(function (w) {
        var b = byId(GARMENTS, w.body), t = byId(GARMENTS, w.trim);
        return { id: w.body + '--' + w.trim, name: b.name + ' / ' + t.name, body: b.hex, trim: t.hex };
      });
    }
    return p.colours.map(function (g) { return { id: g.id, name: g.name, body: g.hex, trim: g.hex }; });
  }
  // A black (or black-bodied) garment first: the default white print reads on it.
  function defaultColour(productKey) {
    var opts = colourOptions(productKey);
    var prefs = ['jet-black', 'black-smoke'];
    for (var j = 0; j < prefs.length; j++) {
      for (var i = 0; i < opts.length; i++) if (opts[i].id.indexOf(prefs[j]) === 0) return opts[i].id;
    }
    return opts[0].id;
  }
  function colourOf(d) {
    var opts = colourOptions(d.product);
    for (var i = 0; i < opts.length; i++) if (opts[i].id === d.garment) return opts[i];
    return opts[0];
  }
  function bodyHex(d) { return colourOf(d).body; }
  function trimHex(d) { return colourOf(d).trim; }

  var BACK_TEMPLATES = [
    { id: 'year-names', name: 'Names in the Year', blurb: 'Every name packed inside a giant year — the classic.', names: true },
    { id: 'heart', name: 'Heart of Names', blurb: 'Your year group fills a big heart.', names: true },
    { id: 'star', name: 'Star of the Show', blurb: 'Names packed into a five-point star.', names: true },
    { id: 'text-block', name: 'Stacked Block', blurb: 'Names stretched edge-to-edge in a bold block.', names: true },
    { id: 'class-of', name: 'Class Of', blurb: 'Script heading, big year, names in neat columns.', names: true },
    { id: 'badge', name: 'College Badge', blurb: 'Round crest with your school around the ring.', names: true },
    { id: 'shirt', name: 'Squad Shirt', blurb: 'Football-shirt number with the squad underneath.', names: true },
    { id: 'name-wall', name: 'Name Wall', blurb: 'Big heading over a wall of names in columns.', names: true },
    { id: 'year-only', name: 'Year Only', blurb: 'Clean and bold — no names.', names: false }
  ];

  var FRONT_STYLES = [
    { id: 'none', name: 'Plain front', area: null },
    { id: 'chest-text', name: 'Chest badge', area: 'chest' },
    { id: 'chest-letter', name: 'Varsity letter', area: 'chest' },
    { id: 'chest-logo', name: 'School logo', area: 'chest' },
    { id: 'centre-college', name: 'Big college front', area: 'centre' },
    { id: 'centre-stack', name: 'Big stacked front', area: 'centre' }
  ];

  var PERSONAL_POSITIONS = [
    { id: 'none', name: 'No personal name' },
    { id: 'sleeve', name: 'Down the sleeve', area: 'sleeve' },
    { id: 'chest-right', name: 'Front right chest', area: 'personal' },
    { id: 'back-top', name: 'Back, above design', area: null }
  ];

  var ICONS = {
    none: null,
    star: 'M50 4 L61.8 37.9 L97.6 38.6 L69 60.3 L79.4 94.6 L50 74.2 L20.6 94.6 L31 60.3 L2.4 38.6 L38.2 37.9 Z',
    heart: 'M50 28 C50 10 30 0 17 5 C2 10 -2 33 8 50 C20 70 40 82 50 100 C60 82 80 70 92 50 C102 33 98 10 83 5 C70 0 50 10 50 28 Z',
    crown: 'M8 78 L16 26 L36 52 L50 14 L64 52 L84 26 L92 78 Z M10 84 H90 V96 H10 Z',
    cap: 'M50 14 L97 36 L50 58 L3 36 Z M24 47 V68 C24 80 76 80 76 68 V47 L50 60 Z M88 40 H92 V70 H88 Z M84 70 H96 V82 H84 Z',
    bolt: 'M60 2 L18 56 H45 L36 98 L82 40 H55 Z',
    football: 'M50 4 A46 46 0 1 0 50.01 4 Z M50 30 L69 44 L62 66 L38 66 L31 44 Z',
    music: 'M38 14 L88 4 V68 A13 11 0 1 1 78 58 V26 L48 32 V78 A13 11 0 1 1 38 68 Z',
    flower: 'M50 38 C50 10 72 6 72 26 C92 18 98 42 76 50 C98 58 92 82 72 74 C72 94 50 90 50 62 C50 90 28 94 28 74 C8 82 2 58 24 50 C2 42 8 18 28 26 C28 6 50 10 50 38 Z'
  };
  var ICON_NAMES = { none: 'No icon', star: 'Star', heart: 'Heart', crown: 'Crown', cap: 'Grad cap', bolt: 'Lightning', football: 'Football', music: 'Music', flower: 'Flower' };

  var SAMPLE_NAMES = ('Olivia Smith\nJack Taylor\nAmelia Brown\nNoah Wilson\nIsla Evans\nHarry Thomas\nAva Roberts\n' +
    'George Johnson\nMia Walker\nLeo Wright\nEmily Hughes\nOscar Green\nGrace Hall\nCharlie Wood\nSophia Clarke\n' +
    'Freddie Lewis\nLily Harris\nAlfie Turner\nFreya Martin\nArchie Cooper\nEvie King\nTheo Baker\nPoppy Hill\n' +
    'Jacob Ward\nRosie Morris\nFinley Moore\nElla Scott\nTommy Price\nMaisie Bell\nReuben Ali').split('\n');

  function defaultDesign(productKey) {
    return {
      v: 1,
      product: PRODUCTS[productKey] ? productKey : DEFAULT_PRODUCT,
      garment: defaultColour(PRODUCTS[productKey] ? productKey : DEFAULT_PRODUCT),
      back: {
        template: 'year-names',
        title: 'LEAVERS',
        year: '27',
        school: 'YOUR SCHOOL NAME',
        names: SAMPLE_NAMES.slice(),
        nameCase: 'upper',
        nameFont: 'Oswald',
        displayFont: 'Anton',
        ink: 'white',
        accent: 'hot-pink',
        twoTone: false,
        repeat: true,
        outline: true,
        logo: false
      },
      front: { style: 'chest-text', line1: 'LEAVERS', line2: '2027', icon: 'star', font: 'Graduate', logoUrl: '' },
      personal: { position: 'sleeve', text: '', font: 'Pacifico' }
    };
  }

  /* ------------------------------------------------------------------ helpers */

  function byId(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return list[0];
  }
  function inkHex(id) { return byId(INKS, id).hex; }
  function garmentHex(id) { return byId(GARMENTS, id).hex; }

  function luminance(hex) {
    var n = parseInt(hex.slice(1), 16);
    var c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map(function (v) {
      v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  function contrastRatio(a, b) {
    var la = luminance(a), lb = luminance(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  }
  function shade(hex, amt) {
    var n = parseInt(hex.slice(1), 16);
    var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    var t = amt < 0 ? 0 : 255, p = Math.abs(amt);
    r = Math.round((t - r) * p + r); g = Math.round((t - g) * p + g); b = Math.round((t - b) * p + b);
    return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
  }

  function makeCanvas(w, h) {
    if (typeof document !== 'undefined') {
      var c = document.createElement('canvas'); c.width = w; c.height = h; return c;
    }
    return new OffscreenCanvas(w, h);
  }

  function fontSpec(name, size) {
    var f = FONT_BY_NAME[name] || FONTS[0];
    return f.weight + ' ' + size + 'px "' + f.name + '", sans-serif';
  }

  function fontsCssUrl() {
    var fams = FONTS.map(function (f) {
      var fam = 'family=' + f.name.replace(/ /g, '+');
      return f.weight !== 400 ? fam + ':wght@' + f.weight : fam;
    });
    return 'https://fonts.googleapis.com/css2?' + fams.join('&') + '&display=block';
  }

  var mctx = makeCanvas(8, 8).getContext('2d');
  var measureCache = new Map();
  var layoutCache = new Map();

  // Glyph metrics at 100px.
  function measure(font, text) {
    var key = font + '\u0001' + text;
    var m = measureCache.get(key);
    if (!m) {
      mctx.font = fontSpec(font, 100);
      var t = mctx.measureText(text);
      m = {
        w: t.width,
        asc: t.actualBoundingBoxAscent || 70,
        desc: t.actualBoundingBoxDescent || 0,
        l: t.actualBoundingBoxLeft || 0,
        r: t.actualBoundingBoxRight || t.width
      };
      measureCache.set(key, m);
    }
    return m;
  }
  function capHeight(font) { return measure(font, 'HXE').asc / 100; }

  function remember(cache, key, fn) {
    if (cache.has(key)) return cache.get(key);
    var v = fn();
    if (cache.size > 80) cache.delete(cache.keys().next().value);
    cache.set(key, v);
    return v;
  }

  function resetMetrics() { measureCache.clear(); layoutCache.clear(); }
  if (typeof document !== 'undefined' && document.fonts && document.fonts.addEventListener) {
    document.fonts.addEventListener('loadingdone', resetMetrics);
  }

  function fontsUsed(d) {
    var list = [d.back.nameFont, d.back.displayFont, d.front.font, d.personal.font, 'Pacifico'];
    return list.filter(function (f, i) { return f && list.indexOf(f) === i; });
  }

  // Waits for the Google Fonts stylesheet itself: until it has loaded, document.fonts.load() finds no faces
  // and resolves straight away, which would let a print file go out in a fallback font.
  function fontSheetReady() {
    var link = document.querySelector('link[href*="fonts.googleapis.com"]');
    if (!link || link.sheet) return Promise.resolve();
    return new Promise(function (res) {
      link.addEventListener('load', res); link.addEventListener('error', res);
      setTimeout(res, 8000);
    });
  }

  function loadFonts(d, all) {
    if (typeof document === 'undefined' || !document.fonts) return Promise.resolve();
    var names = all ? FONTS.map(function (f) { return f.name; }) : fontsUsed(d);
    return fontSheetReady().then(function () {
      return Promise.all(names.map(function (n) {
        return document.fonts.load(fontSpec(n, 40), 'AaBb0123').catch(function () { });
      }));
    }).then(function () { resetMetrics(); });
  }

  function fontsMissing(d) {
    if (typeof document === 'undefined' || !document.fonts) return [];
    return fontsUsed(d).filter(function (n) { return !document.fonts.check(fontSpec(n, 40), 'Aa'); });
  }

  function formatName(s, mode) {
    s = String(s).replace(/\s+/g, ' ').trim();
    if (mode === 'upper') return s.toUpperCase();
    if (mode === 'title') return s.toLowerCase().replace(/(^|[\s\-'])(\S)/g, function (m, a, b) { return a + b.toUpperCase(); });
    return s;
  }
  function cleanNames(d) {
    return (d.back.names || []).map(function (n) { return formatName(n, d.back.nameCase); }).filter(Boolean);
  }

  /* ------------------------------------------------------------------ text drawing */

  // Largest size at which the text's actual ink fits in maxW x maxH.
  function fitSize(font, text, maxW, maxH) {
    var m = measure(font, text);
    var gw = Math.max(m.l + m.r, 1), gh = Math.max(m.asc + m.desc, 1);
    return Math.max(0, Math.min(maxW / gw, maxH / gh) * 100);
  }

  // Draws text centred on its ink box inside box. opts: maxSize, stroke, strokeWidth, align ('centre'|'left').
  function drawFit(ctx, text, font, box, colour, opts) {
    opts = opts || {};
    if (!text) return null;
    var sw = opts.stroke ? opts.strokeWidth || 6 : 0;
    var inset = opts.noShrink ? 0 : sw;
    var size = fitSize(font, text, box.w - inset * 2, box.h - inset * 2);
    if (opts.maxSize) size = Math.min(size, opts.maxSize);
    if (size <= 0.5) return null;
    var m = measure(font, text), k = size / 100;
    var gw = (m.l + m.r) * k, gh = (m.asc + m.desc) * k;
    var left = opts.align === 'left' ? box.x + inset : box.x + (box.w - gw) / 2;
    var x = left + m.l * k;
    var y = box.y + (box.h - gh) / 2 + m.asc * k;
    ctx.font = fontSpec(font, size);
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    if (sw) {
      ctx.lineJoin = 'round';
      ctx.miterLimit = 2;
      ctx.strokeStyle = opts.stroke;
      ctx.lineWidth = sw * 2;
      ctx.strokeText(text, x, y);
    }
    if (colour) { ctx.fillStyle = colour; ctx.fillText(text, x, y); }
    return { x: left, y: box.y + (box.h - gh) / 2, w: gw, h: gh, size: size };
  }

  // Text on a circle. top=true reads clockwise over the top; false reads left-to-right under the bottom.
  function drawArcText(ctx, text, font, size, cx, cy, radius, top, colour, spacing) {
    if (!text) return;
    var k = size / 100, ls = spacing || 1.06;
    var chars = Array.from(text);
    var widths = chars.map(function (ch) { return measure(font, ch).w * k * ls; });
    var total = widths.reduce(function (a, b) { return a + b; }, 0);
    var span = total / radius;
    ctx.font = fontSpec(font, size);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = colour;
    var a = top ? -Math.PI / 2 - span / 2 : Math.PI / 2 + span / 2;
    chars.forEach(function (ch, i) {
      var half = widths[i] / 2 / radius;
      var ac = top ? a + half : a - half;
      ctx.save();
      ctx.translate(cx + radius * Math.cos(ac), cy + radius * Math.sin(ac));
      ctx.rotate(top ? ac + Math.PI / 2 : ac - Math.PI / 2);
      ctx.fillText(ch, 0, 0);
      ctx.restore();
      a = top ? a + 2 * half : a - 2 * half;
    });
  }

  function arcSizeFor(font, text, bandH, radius, maxAngle) {
    var cap = capHeight(font);
    var size = bandH / cap;
    var w = measure(font, text).w / 100 * 1.06;
    if (w * size / radius > maxAngle) size = maxAngle * radius / w;
    return size;
  }

  function drawIcon(ctx, name, box, colour) {
    var d = ICONS[name];
    if (!d || typeof Path2D === 'undefined') return;
    var s = Math.min(box.w, box.h) / 100;
    ctx.save();
    ctx.translate(box.x + (box.w - 100 * s) / 2, box.y + (box.h - 100 * s) / 2);
    ctx.scale(s, s);
    ctx.fillStyle = colour;
    ctx.fill(new Path2D(d), 'evenodd');
    ctx.restore();
  }

  // Draws `content` and keeps only the parts inside `shape` (both drawn in the ctx's current reference space).
  function clipped(ctx, content, shape) {
    var c = ctx.canvas;
    var layer = makeCanvas(c.width, c.height);
    var lx = layer.getContext('2d');
    lx.setTransform(ctx.getTransform());
    content(lx);
    lx.globalCompositeOperation = 'destination-in';
    lx.fillStyle = '#000';
    shape(lx);
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.drawImage(layer, 0, 0);
    ctx.restore();
  }

  /* ------------------------------------------------------------------ name layouts */

  function shapeMask(shape, box) {
    var scale = 0.5;
    var mw = Math.max(1, Math.ceil(box.w * scale)), mh = Math.max(1, Math.ceil(box.h * scale));
    var c = makeCanvas(mw, mh), x = c.getContext('2d', { willReadFrequently: true });
    x.setTransform(scale, 0, 0, scale, -box.x * scale, -box.y * scale);
    x.fillStyle = '#000';
    shape(x);
    var data = x.getImageData(0, 0, mw, mh).data;
    return { data: data, w: mw, h: mh, scale: scale, box: box };
  }

  function spansAt(mask, yRef) {
    var row = Math.floor((yRef - mask.box.y) * mask.scale);
    var out = [];
    if (row < 0 || row >= mask.h) return out;
    var start = -1, base = row * mask.w * 4;
    for (var x = 0; x <= mask.w; x++) {
      var on = x < mask.w && mask.data[base + x * 4 + 3] > 127;
      if (on && start < 0) start = x;
      if (!on && start >= 0) { out.push([mask.box.x + start / mask.scale, mask.box.x + x / mask.scale]); start = -1; }
    }
    return out;
  }
  function intersectSpans(a, b) {
    var out = [];
    a.forEach(function (s) {
      b.forEach(function (t) {
        var x0 = Math.max(s[0], t[0]), x1 = Math.min(s[1], t[1]);
        if (x1 > x0) out.push([x0, x1]);
      });
    });
    return out;
  }

  // Names fill the shape with no gaps: each row is packed, then stretched edge to edge when drawn.
  var FILL = { lead: 1.16, squeeze: 0.8, maxStretch: 1.7, minK: 0.3 };
  // Top and bottom of the filled part of the mask, so rows can be fitted to the shape exactly.
  function maskBounds(mask) {
    var top = -1, bottom = -1;
    for (var r = 0; r < mask.h; r++) {
      for (var c = 0, base = r * mask.w * 4; c < mask.w; c++) {
        if (mask.data[base + c * 4 + 3] > 127) { if (top < 0) top = r; bottom = r; break; }
      }
    }
    if (top < 0) return { y: mask.box.y, h: mask.box.h };
    return { y: mask.box.y + top / mask.scale, h: (bottom - top + 1) / mask.scale };
  }
  function packShape(names, font, mask, box, size, repeat) {
    var n = names.length;
    var bounds = mask.bounds || (mask.bounds = maskBounds(mask));
    // Whole rows from the top of the shape to the bottom: no strip left empty.
    var nRows = Math.max(1, Math.round(bounds.h / (size * capHeight(font) * FILL.lead)));
    var lineH = bounds.h / nRows;
    var gap = size * 0.28;
    var widths = names.map(function (s) { return measure(font, s).w * size / 100; });
    var rows = [], i = 0;
    for (var row = 0; row < nRows; row++) {
      var y = bounds.y + row * lineH;
      if (!repeat && i >= n) break;
      var spans = intersectSpans(spansAt(mask, y + lineH * 0.2), spansAt(mask, y + lineH * 0.8));
      for (var s = 0; s < spans.length; s++) {
        if (!repeat && i >= n) break;
        var x0 = spans[s][0], x1 = spans[s][1], span = x1 - x0;
        if (span < size * 0.5) continue;
        var items = [], used = 0, guard = 0;
        while (guard++ < 500) {
          if (!repeat && i >= n) break;
          var w = widths[i % n];
          var need = items.length ? used + gap + w : w;
          // Names may be squeezed a little to fit one more in, so rows end flush.
          if (need * FILL.squeeze > span) break;
          items.push({ idx: i % n, k: 1 }); used = need; i++;
        }
        // Narrow strokes: a smaller, condensed name rather than an empty stroke.
        if (!items.length) {
          var wn = widths[i % n];
          var k = Math.min(1, span / (wn * 0.6));
          if (k >= FILL.minK) { items.push({ idx: i % n, k: k }); used = wn * k; i++; }
        }
        if (items.length) rows.push({ y: y, x0: x0, x1: x1, items: items, used: used });
      }
    }
    return { rows: rows, all: i >= n, size: size, lineH: lineH, gap: gap, widths: widths };
  }

  function layoutShape(key, names, font, shape, box) {
    return remember(layoutCache, key, function () {
      var mask = shapeMask(shape, box);
      if (!names.length) return { rows: [], size: 0 };
      var lo = 2, hi = box.h / 3;
      for (var it = 0; it < 22; it++) {
        var mid = (lo + hi) / 2;
        if (packShape(names, font, mask, box, mid, false).all) lo = mid; else hi = mid;
      }
      // Keep names small enough to run down the narrow strokes of a digit, not just the wide bars.
      var widths = [];
      for (var y = box.y; y < box.y + box.h; y += 4) spansAt(mask, y).forEach(function (sp) { widths.push(sp[1] - sp[0]); });
      widths.sort(function (a, b) { return a - b; });
      var nameW = names.map(function (s) { return measure(font, s).w; }).sort(function (a, b) { return a - b; });
      if (widths.length) {
        var narrow = widths[Math.floor(widths.length * 0.3)];
        lo = Math.min(lo, narrow * 1.5 / nameW[Math.floor(nameW.length / 2)] * 100);
      }
      // Every name appears at least once; the rest of the shape is filled by repeating them.
      return packShape(names, font, mask, box, Math.max(lo, 2), true);
    });
  }

  function drawShapeNames(ctx, lay, names, font, colours) {
    if (!lay.rows.length) return;
    var size = lay.size, cap = capHeight(font);
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
    var count = 0;
    lay.rows.forEach(function (r) {
      var span = r.x1 - r.x0, n = r.items.length;
      var natural = r.items.reduce(function (a, it) { return a + lay.widths[it.idx] * it.k; }, 0);
      var gaps = lay.gap * (n - 1);
      // Stretch (or squeeze) the names so the row runs the full width of the stroke.
      var sx = Math.max(0.35, Math.min(FILL.maxStretch, (span - gaps) / natural));
      var extra = span - gaps - natural * sx;
      var gap = lay.gap + (n > 1 && extra > 0 ? extra / (n - 1) : 0);
      var x = r.x0 + (n === 1 && extra > 0 ? extra / 2 : 0);
      r.items.forEach(function (it) {
        var sz = size * it.k;
        ctx.font = fontSpec(font, sz);
        ctx.fillStyle = colours[count++ % colours.length];
        ctx.save();
        ctx.translate(x, r.y + lay.lineH / 2 + cap * sz / 2);
        ctx.scale(sx, 1);
        ctx.fillText(names[it.idx], 0, 0);
        ctx.restore();
        x += lay.widths[it.idx] * it.k * sx + gap;
      });
    });
  }

  // Columns: picks the column count that gives the biggest names.
  function drawColumns(ctx, names, font, box, colours, opts) {
    opts = opts || {};
    var n = names.length;
    if (!n) return;
    var maxW = Math.max.apply(null, names.map(function (s) { return measure(font, s).w; })) / 100;
    var cap = capHeight(font), lh = opts.lineHeight || 1.7;
    var best = null;
    for (var cols = 1; cols <= Math.min(opts.maxCols || 6, n); cols++) {
      var rows = Math.ceil(n / cols);
      var size = Math.min((box.w / cols) * 0.9 / maxW, box.h / (rows * cap * lh), opts.maxSize || 1e9);
      if (!best || size > best.size * 1.02) best = { cols: cols, rows: rows, size: size };
    }
    var colW = box.w / best.cols, rowH = best.size * cap * lh;
    var top = box.y + (box.h - rowH * best.rows) / 2;
    ctx.font = fontSpec(font, best.size);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    if (opts.dividers && best.cols > 1) {
      ctx.fillStyle = opts.dividers;
      for (var c = 1; c < best.cols; c++) ctx.fillRect(box.x + c * colW - 1.5, top, 3, rowH * best.rows);
    }
    names.forEach(function (s, i) {
      var col = Math.floor(i / best.rows), row = i % best.rows;
      ctx.fillStyle = colours[i % colours.length];
      ctx.fillText(s, box.x + colW * (col + 0.5), top + rowH * (row + 0.5) + best.size * cap / 2);
    });
  }

  // Stacked block: each line stretched to the full width.
  function drawBlock(ctx, d, box, names, colours, accent) {
    var font = d.back.nameFont, disp = d.back.displayFont;
    var spaceW = measure(font, 'M').w * 0.45;
    var head = [d.back.title, d.back.year].filter(Boolean).join(' ').trim();
    var school = (d.back.school || '').trim();
    var capN = capHeight(font), lead = 0.3;
    var headH = head ? Math.min(box.h * 0.2, box.w / (measure(disp, head).l + measure(disp, head).r) * 100 * capHeight(disp)) : 0;
    var schoolH = school ? Math.min(box.h * 0.08, box.w / (measure(disp, school).l + measure(disp, school).r) * 100 * capHeight(disp)) : 0;
    var avail = box.h - headH - schoolH - (head ? headH * lead : 0) - (school ? schoolH * lead * 2 : 0);
    var widths = names.map(function (s) { return measure(font, s).w; });

    function split(nLines) {
      var total = widths.reduce(function (a, b) { return a + b + spaceW; }, -spaceW);
      var target = total / nLines, lines = [], cur = [], acc = 0;
      widths.forEach(function (w, i) {
        var add = cur.length ? acc + spaceW + w : w;
        if (cur.length && add > target && Math.abs(add - target) > Math.abs(acc - target) && lines.length < nLines - 1) {
          lines.push({ items: cur, w: acc }); cur = []; acc = 0; add = w;
        }
        cur.push(i); acc = add;
      });
      if (cur.length) lines.push({ items: cur, w: acc });
      var h = 0;
      lines.forEach(function (l) { l.size = Math.min(box.w / l.w * 100, avail * 0.3 / capN); h += l.size * capN * (1 + lead); });
      return { lines: lines, h: h - (lines.length ? lines[lines.length - 1].size * capN * lead : 0) };
    }
    var best = names.length ? split(1) : { lines: [], h: 0 };
    for (var nL = 2; nL <= names.length; nL++) {
      var s = split(nL);
      if (s.h > avail) break;
      best = s;
    }
    var scale = best.h > avail ? avail / best.h : 1;
    var extra = best.h < avail && best.lines.length > 1 ? (avail - best.h) / (best.lines.length - 1) : 0;
    extra = Math.min(extra, avail * 0.04);
    var used = best.h * scale + extra * Math.max(best.lines.length - 1, 0);
    var y = box.y + (box.h - (used + headH + schoolH + (head ? headH * lead : 0) + (school ? schoolH * lead * 2 : 0))) / 2;
    if (head) {
      drawFit(ctx, head, disp, { x: box.x, y: y, w: box.w, h: headH }, accent);
      y += headH * (1 + lead);
    }
    var count = 0;
    best.lines.forEach(function (l) {
      var size = l.size * scale, k = size / 100, lw = l.w * k;
      var x = box.x + (box.w - lw) / 2;
      ctx.font = fontSpec(font, size);
      ctx.textAlign = 'left';
      ctx.textBaseline = 'alphabetic';
      var base = y + capN * size;
      l.items.forEach(function (idx) {
        ctx.fillStyle = colours[count++ % colours.length];
        ctx.fillText(names[idx], x, base);
        x += (widths[idx] + spaceW) * k;
      });
      y += capN * size * (1 + lead) + extra;
    });
    if (school) {
      y += schoolH * lead - capN * (best.lines.length ? best.lines[best.lines.length - 1].size * scale : 0) * lead;
      drawFit(ctx, school, disp, { x: box.x, y: y, w: box.w, h: schoolH }, accent);
    }
  }

  /* ------------------------------------------------------------------ shapes */

  function yearShape(d, box) {
    var font = d.back.displayFont, text = d.back.year || '27';
    return function (x) { drawFit(x, text, font, box, '#000'); };
  }
  // Heart and star are plain paths, so the same geometry fills the mask, clips the names and draws the outline.
  function heartPath(box) {
    var s = Math.min(box.w / 100, box.h / 100);
    var p = new Path2D();
    p.addPath(new Path2D(ICONS.heart), new DOMMatrix().translate(box.x + (box.w - 100 * s) / 2, box.y + (box.h - 100 * s) / 2).scale(s));
    return p;
  }
  function starPath(box) {
    var r = Math.min(box.w, box.h * 1.05) / 2, cx = box.x + box.w / 2, cy = box.y + box.h / 2 + r * 0.06;
    var p = new Path2D();
    for (var i = 0; i < 10; i++) {
      var rr = i % 2 ? r * 0.52 : r, a = -Math.PI / 2 + i * Math.PI / 5;
      if (i) p.lineTo(cx + rr * Math.cos(a), cy + rr * Math.sin(a)); else p.moveTo(cx + rr * Math.cos(a), cy + rr * Math.sin(a));
    }
    p.closePath();
    return p;
  }

  /* ------------------------------------------------------------------ back templates */

  function renderBack(ctx, d, H) {
    var b = d.back, ink = inkHex(b.ink), accent = inkHex(b.accent);
    var names = cleanNames(d);
    var colours = b.twoTone ? [ink, accent] : [ink];
    var disp = b.displayFont, top = 0;
    var personal = d.personal && d.personal.position === 'back-top' && (d.personal.text || '').trim();
    if (personal && b.template !== 'shirt') {
      drawFit(ctx, personal, d.personal.font, { x: 60, y: 10, w: REF - 120, h: H * 0.1 }, accent);
      top = H * 0.13;
    }
    var backLogo = b.logo ? logoImage(d) : null;
    if (b.logo && b.template !== 'badge') {
      var lb = { x: REF * 0.3, y: top, w: REF * 0.4, h: H * 0.15 };
      drawLogoIn(ctx, d, backLogo, lb, accent);
      top += H * 0.17;
    }
    var box = { x: 0, y: top, w: REF, h: H - top };
    var Y = function (f) { return box.y + box.h * f; };
    var keyBase = [b.template, names.join('|'), b.nameFont, disp, b.year, b.repeat, Math.round(box.y), Math.round(box.h)].join('#');

    switch (b.template) {
      case 'heart':
      case 'star': {
        drawFit(ctx, [b.title, b.year].filter(Boolean).join(' '), disp, { x: 40, y: Y(0), w: REF - 80, h: box.h * 0.13 }, accent);
        var sbox = { x: 0, y: Y(0.16), w: REF, h: box.h * 0.73 };
        var spath = b.template === 'heart' ? heartPath(sbox) : starPath(sbox);
        var shape = function (x) { x.fill(spath); };
        var lay = layoutShape(keyBase, names, b.nameFont, shape, sbox);
        clipped(ctx, function (x) { drawShapeNames(x, lay, names, b.nameFont, colours); }, shape);
        if (b.outline) { ctx.save(); ctx.strokeStyle = accent; ctx.lineWidth = 7; ctx.lineJoin = 'round'; ctx.stroke(spath); ctx.restore(); }
        drawFit(ctx, b.school, disp, { x: 60, y: Y(0.92), w: REF - 120, h: box.h * 0.07 }, accent);
        break;
      }
      case 'text-block':
        drawBlock(ctx, d, { x: 10, y: box.y + 10, w: REF - 20, h: box.h - 20 }, names, colours, accent);
        break;
      case 'class-of': {
        drawFit(ctx, b.title ? capitalise(b.title) : 'Class of', 'Pacifico', { x: 80, y: Y(0), w: REF - 160, h: box.h * 0.13 }, accent);
        drawFit(ctx, b.year, disp, { x: 0, y: Y(0.14), w: REF, h: box.h * 0.27 }, ink, b.outline ? { stroke: accent, strokeWidth: 7 } : null);
        ctx.fillStyle = accent;
        ctx.fillRect(REF * 0.2, Y(0.445), REF * 0.6, 5);
        drawColumns(ctx, names, b.nameFont, { x: 0, y: Y(0.47), w: REF, h: box.h * 0.44 }, colours, { maxSize: 70 });
        drawFit(ctx, b.school, disp, { x: 60, y: Y(0.93), w: REF - 120, h: box.h * 0.065 }, accent);
        break;
      }
      case 'badge': {
        var R = Math.min(REF * 0.46, box.h * 0.27), cx = REF / 2, cy = Y(0.02) + R;
        ctx.save();
        ctx.strokeStyle = accent; ctx.lineWidth = 12;
        ctx.beginPath(); ctx.arc(cx, cy, R - 6, 0, Math.PI * 2); ctx.stroke();
        ctx.lineWidth = 5;
        ctx.beginPath(); ctx.arc(cx, cy, R * 0.66, 0, Math.PI * 2); ctx.stroke();
        ctx.restore();
        var band = R * 0.34 - 12, mid = (R - 12 + R * 0.66) / 2;
        var tSize = arcSizeFor(disp, b.school, band * 0.62, mid, Math.PI * 0.95);
        drawArcText(ctx, b.school, disp, tSize, cx, cy, mid - capHeight(disp) * tSize / 2, true, ink);
        var bSize = arcSizeFor(disp, b.title, band * 0.62, mid, Math.PI * 0.6);
        drawArcText(ctx, b.title, disp, bSize, cx, cy, mid + capHeight(disp) * bSize / 2, false, ink);
        drawIcon(ctx, 'star', { x: cx - mid - band * 0.22, y: cy - band * 0.22, w: band * 0.44, h: band * 0.44 }, accent);
        drawIcon(ctx, 'star', { x: cx + mid - band * 0.22, y: cy - band * 0.22, w: band * 0.44, h: band * 0.44 }, accent);
        if (b.logo) drawLogoIn(ctx, d, backLogo, { x: cx - R * 0.47, y: cy - R * 0.47, w: R * 0.94, h: R * 0.94 }, accent);
        else drawFit(ctx, b.year, disp, { x: cx - R * 0.5, y: cy - R * 0.4, w: R, h: R * 0.8 }, accent);
        drawColumns(ctx, names, b.nameFont, { x: 0, y: cy + R + box.h * 0.04, w: REF, h: box.h - (cy + R - box.y) - box.h * 0.05 }, colours, { maxSize: 70 });
        break;
      }
      case 'shirt': {
        var head = personal || b.title;
        drawFit(ctx, head, disp, { x: 60, y: Y(0), w: REF - 120, h: box.h * 0.12 }, ink);
        drawFit(ctx, b.year, disp, { x: 70, y: Y(0.14), w: REF - 140, h: box.h * 0.46 }, ink, { stroke: accent, strokeWidth: 9 });
        drawColumns(ctx, names, b.nameFont, { x: 20, y: Y(0.63), w: REF - 40, h: box.h * 0.29 }, colours, { maxSize: 56, maxCols: 4 });
        drawFit(ctx, b.school, disp, { x: 80, y: Y(0.935), w: REF - 160, h: box.h * 0.06 }, accent);
        break;
      }
      case 'name-wall': {
        drawFit(ctx, b.title, disp, { x: 0, y: Y(0), w: REF, h: box.h * 0.14 }, ink);
        drawFit(ctx, [b.school, b.year].filter(Boolean).join(' · '), disp, { x: 80, y: Y(0.16), w: REF - 160, h: box.h * 0.06 }, accent);
        drawColumns(ctx, names, b.nameFont, { x: 0, y: Y(0.25), w: REF, h: box.h * 0.75 }, colours, { maxSize: 80, dividers: accent });
        break;
      }
      case 'year-only': {
        drawFit(ctx, b.title, disp, { x: 0, y: Y(0.05), w: REF, h: box.h * 0.17 }, accent);
        drawFit(ctx, b.year, disp, { x: 0, y: Y(0.25), w: REF, h: box.h * 0.55 }, ink, b.outline ? { stroke: accent, strokeWidth: 9 } : null);
        drawFit(ctx, b.school, disp, { x: 60, y: Y(0.84), w: REF - 120, h: box.h * 0.09 }, accent);
        break;
      }
      default: { // year-names
        drawFit(ctx, b.title, disp, { x: 0, y: Y(0), w: REF, h: box.h * 0.14 }, accent);
        var ybox = { x: 0, y: Y(0.16), w: REF, h: box.h * 0.74 };
        var yshape = yearShape(d, ybox);
        var ylay = layoutShape(keyBase, names, b.nameFont, yshape, ybox);
        clipped(ctx, function (x) { drawShapeNames(x, ylay, names, b.nameFont, colours); }, yshape);
        if (b.outline) {
          drawFit(ctx, b.year, disp, ybox, null, { stroke: accent, strokeWidth: 3, noShrink: true });
        }
        drawFit(ctx, b.school, disp, { x: 60, y: Y(0.92), w: REF - 120, h: box.h * 0.075 }, accent);
      }
    }
  }

  function capitalise(s) { s = String(s).toLowerCase(); return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ------------------------------------------------------------------ front + personal */

  var logoCache = new Map();
  function logoImage(d) {
    var src = d._logoSrc || d.front.logoUrl;
    if (!src) return null;
    var img = logoCache.get(src);
    if (!img && typeof Image !== 'undefined') {
      img = new Image();
      img.crossOrigin = 'anonymous';
      img.src = src;
      logoCache.set(src, img);
    }
    return img && img.complete && img.naturalWidth ? img : null;
  }
  // The school logo can go on the front chest, on the back, or both.
  function usesLogo(d) {
    return d.front.style === 'chest-logo' || !!(d.back && d.back.logo);
  }
  function loadLogo(d) {
    var src = d._logoSrc || d.front.logoUrl;
    if (!src || !usesLogo(d) || typeof Image === 'undefined') return Promise.resolve();
    logoImage(d);
    var img = logoCache.get(src);
    if (img.complete) return Promise.resolve();
    return new Promise(function (res) { img.onload = img.onerror = function () { res(); }; });
  }

  // Fit the logo inside box; before one is uploaded, the preview shows a dashed "YOUR LOGO" placeholder (never printed).
  function drawLogoIn(ctx, d, img, box, colour) {
    if (img) {
      var s = Math.min(box.w / img.naturalWidth, box.h / img.naturalHeight);
      var w = img.naturalWidth * s, h = img.naturalHeight * s;
      ctx.drawImage(img, box.x + (box.w - w) / 2, box.y + (box.h - h) / 2, w, h);
    } else if (!d._print) {
      var pad = Math.min(box.w, box.h) * 0.06;
      ctx.save();
      ctx.strokeStyle = colour; ctx.setLineDash([30, 20]); ctx.lineWidth = 10;
      ctx.strokeRect(box.x + pad, box.y + pad, box.w - pad * 2, box.h - pad * 2);
      ctx.restore();
      drawFit(ctx, 'YOUR LOGO', 'Oswald', { x: box.x + box.w * 0.2, y: box.y + box.h * 0.38, w: box.w * 0.6, h: box.h * 0.24 }, colour);
    }
  }

  function renderFront(ctx, d, H) {
    var f = d.front, ink = inkHex(d.back.ink), accent = inkHex(d.back.accent);
    var font = f.font || d.back.displayFont;
    switch (f.style) {
      case 'chest-text': {
        var hasIcon = f.icon && f.icon !== 'none';
        if (hasIcon) drawIcon(ctx, f.icon, { x: 300, y: 20, w: 400, h: 300 }, accent);
        var y0 = hasIcon ? 360 : 120;
        drawFit(ctx, f.line1, font, { x: 20, y: y0, w: REF - 40, h: hasIcon ? 340 : 440 }, ink);
        drawFit(ctx, f.line2, 'Pacifico', { x: 80, y: y0 + (hasIcon ? 380 : 480), w: REF - 160, h: 220 }, accent);
        break;
      }
      case 'chest-letter': {
        // Chenille-style patch: highlight colour letter with a thick main-colour outline.
        var letter = (f.line1 || 'L').trim().slice(0, 2).toUpperCase();
        drawFit(ctx, letter, font, { x: 30, y: 30, w: REF - 60, h: REF - 60 }, accent, { stroke: ink, strokeWidth: 34 });
        break;
      }
      case 'chest-logo': {
        drawLogoIn(ctx, d, logoImage(d), { x: 60, y: 30, w: REF - 120, h: f.line1 ? 700 : 940 }, accent);
        if (f.line1) drawFit(ctx, f.line1, font, { x: 20, y: 760, w: REF - 40, h: 220 }, ink);
        break;
      }
      case 'centre-college': {
        var R = 900, cx = REF / 2, cy = 120 + R;
        var size = arcSizeFor(font, f.line1, H * 0.22, R, 0.95);
        drawArcText(ctx, f.line1, font, size, cx, cy, R, true, ink, 1.04);
        drawFit(ctx, f.line2, 'Pacifico', { x: 40, y: H * 0.3, w: REF - 80, h: H * 0.42 }, accent);
        drawFit(ctx, d.back.year, font, { x: 300, y: H * 0.72, w: 400, h: H * 0.25 }, ink, d.back.outline ? { stroke: accent, strokeWidth: 6 } : null);
        break;
      }
      case 'centre-stack': {
        drawFit(ctx, f.line1, font, { x: 0, y: 0, w: REF, h: H * 0.56 }, ink);
        drawFit(ctx, f.line2, 'Pacifico', { x: 60, y: H * 0.6, w: REF - 120, h: H * 0.38 }, accent);
        break;
      }
    }
  }

  function renderPersonal(ctx, d, H, key) {
    var text = (d.personal.text || '').trim();
    if (!text) {
      if (d._print) return;
      text = 'Your name';
    }
    var colour = inkHex(d.back.accent);
    if (key === 'sleeve') {
      // Reads top-to-bottom down the sleeve.
      ctx.save();
      ctx.translate(REF, 0);
      ctx.rotate(Math.PI / 2);
      drawFit(ctx, text, d.personal.font, { x: H * 0.03, y: REF * 0.08, w: H * 0.94, h: REF * 0.84 }, colour);
      ctx.restore();
    } else {
      drawFit(ctx, text, d.personal.font, { x: 10, y: 10, w: REF - 20, h: H - 20 }, colour);
    }
  }

  /* ------------------------------------------------------------------ print areas */

  function product(d) { return PRODUCTS[d.product] || PRODUCTS[DEFAULT_PRODUCT]; }
  function isKids(size) { return KIDS_SIZES.indexOf(size) >= 0; }
  // Print areas for this design: kids sizes print smaller.
  function areasOf(d) { var p = product(d); return isKids(d.size) && p.kidsAreas ? p.kidsAreas : p.areas; }
  function frontStyle(d) { return byId(FRONT_STYLES, d.front.style); }
  function personalPos(d) { return byId(PERSONAL_POSITIONS, d.personal.position); }

  // The areas this design prints on, in print order.
  function printAreas(d, forPreview) {
    var areas = areasOf(d), out = [];
    function add(key) { if (areas[key]) out.push({ key: key, mm: areas[key], label: areas[key].label }); }
    add('back');
    var fs = frontStyle(d);
    if (fs.area) add(areas[fs.area] ? fs.area : 'chest');
    var pp = personalPos(d);
    if (pp.area && (forPreview || (d.personal.text || '').trim())) add(pp.area);
    return out;
  }

  function renderArea(canvas, d, key) {
    var mm = areasOf(d)[key];
    var ctx = canvas.getContext('2d');
    var H = REF * mm.h / mm.w, s = canvas.width / REF;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.setTransform(s, 0, 0, s, 0, 0);
    if (key === 'back') renderBack(ctx, d, H);
    else if (key === 'chest' || key === 'centre') renderFront(ctx, d, H);
    else renderPersonal(ctx, d, H, key);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
  }

  function areaCanvas(d, key, widthPx) {
    var mm = areasOf(d)[key];
    var w = Math.max(1, Math.round(widthPx)), h = Math.max(1, Math.round(widthPx * mm.h / mm.w));
    var c = makeCanvas(w, h);
    renderArea(c, d, key);
    return c;
  }

  /* ------------------------------------------------------------------ garment mockups */

  // All garments are drawn in a 1000 x 1100 box.
  var G = {
    hoodieBody: 'M395 150 C340 158 290 170 252 192 C205 215 175 260 160 330 L100 860 L102 905 L198 918 L205 872 L258 470 L262 980 L266 1032 L734 1032 L738 980 L742 470 L795 872 L802 918 L898 905 L900 860 L840 330 C825 260 795 215 748 192 C710 170 660 158 605 150 Q500 205 395 150 Z',
    hoodFront: 'M352 182 C326 46 420 -4 500 -4 C580 -4 674 46 648 182 Q500 236 352 182 Z',
    hoodOpening: 'M408 172 C396 84 444 48 500 48 C556 48 604 84 592 172 Q500 222 408 172 Z',
    hoodBack: 'M345 212 C318 50 410 -4 500 -4 C590 -4 682 50 655 212 Q500 246 345 212 Z',
    pocket: 'M318 720 L682 720 L714 948 L286 948 Z',
    teeBody: 'M400 150 C345 158 300 168 262 186 L118 300 L176 474 L262 432 L262 1032 L738 1032 L738 432 L824 474 L882 300 L738 186 C700 168 655 158 600 150 Q500 214 400 150 Z'
  };
  // Where each print area sits on the mockup: centre x, top y, and rotation for the sleeve.
  var PLACES = {
    back: { view: 'back', cx: 500, top: 232 },
    chest: { view: 'front', cx: 622, top: 285 },
    centre: { view: 'front', cx: 500, top: 268 },
    personal: { view: 'front', cx: 378, top: 300 },
    sleeve: { view: 'front', line: [772, 300, 852, 860], t: 0.47 }
  };

  var SLEEVES = {
    raglan: [
      'M405 152 L0 60 L0 1100 L256 1100 L256 470 Q300 300 405 152 Z',
      'M595 152 L1000 60 L1000 1100 L744 1100 L744 470 Q700 300 595 152 Z'
    ],
    setIn: [
      'M252 192 L0 150 L0 1100 L256 1100 L256 470 C282 400 282 260 252 192 Z',
      'M748 192 L1000 150 L1000 1100 L744 1100 L744 470 C718 400 718 260 748 192 Z'
    ]
  };

  function drawGarment(ctx, d, view, layer) {
    var p = product(d), type = p.mockup;
    var base = bodyHex(d), trim = trimHex(d);
    var hooded = type === 'hoodie' || type === 'baseball' || type === 'zip';
    var body = new Path2D(type === 'tee' ? G.teeBody : G.hoodieBody);
    var line = function (hex) { return luminance(hex) > 0.5 ? shade(hex, -0.28) : shade(hex, -0.45); };
    var outline = line(base);
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    if (layer === 'base') {
      if (hooded) {
        var hood = new Path2D(view === 'back' ? G.hoodBack : G.hoodFront);
        ctx.fillStyle = base; ctx.fill(hood);
        ctx.strokeStyle = outline; ctx.lineWidth = 3; ctx.stroke(hood);
      }
      ctx.fillStyle = base;
      ctx.fill(body);

      ctx.save();
      ctx.clip(body);
      // Contrast sleeves on the two-tone garments.
      var sleeves = type === 'baseball' ? SLEEVES.raglan : type === 'varsity' ? SLEEVES.setIn : null;
      if (sleeves) {
        ctx.fillStyle = trim;
        sleeves.forEach(function (sp) { ctx.fill(new Path2D(sp)); });
      }
      if (type !== 'tee') {
        // Ribbed hem and cuffs (cuffs follow the sleeve colour).
        ctx.fillStyle = base;
        ctx.fillRect(250, 982, 500, 60);
        ctx.fillStyle = type === 'baseball' ? trim : base;
        ctx.beginPath(); ctx.moveTo(95, 858); ctx.lineTo(210, 870); ctx.lineTo(205, 930); ctx.lineTo(90, 920); ctx.closePath(); ctx.fill();
        ctx.beginPath(); ctx.moveTo(905, 858); ctx.lineTo(790, 870); ctx.lineTo(795, 930); ctx.lineTo(910, 920); ctx.closePath(); ctx.fill();
        if (type === 'varsity') {
          // Varsity stripes in the sleeve colour.
          ctx.fillStyle = trim;
          ctx.fillRect(250, 996, 500, 7); ctx.fillRect(250, 1012, 500, 7);
          ctx.strokeStyle = trim; ctx.lineWidth = 6;
          ctx.beginPath();
          ctx.moveTo(98, 880); ctx.lineTo(207, 892); ctx.moveTo(97, 896); ctx.lineTo(206, 908);
          ctx.moveTo(902, 880); ctx.lineTo(793, 892); ctx.moveTo(903, 896); ctx.lineTo(794, 908);
          ctx.stroke();
        }
      }
      // Soft shading so the garment reads as fabric.
      var g = ctx.createLinearGradient(100, 0, 900, 0);
      g.addColorStop(0, 'rgba(0,0,0,0.22)'); g.addColorStop(0.18, 'rgba(0,0,0,0.04)');
      g.addColorStop(0.5, 'rgba(255,255,255,0.05)'); g.addColorStop(0.82, 'rgba(0,0,0,0.04)'); g.addColorStop(1, 'rgba(0,0,0,0.22)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, 1000, 1100);
      var v = ctx.createLinearGradient(0, 150, 0, 1040);
      v.addColorStop(0, 'rgba(255,255,255,0.06)'); v.addColorStop(1, 'rgba(0,0,0,0.12)');
      ctx.fillStyle = v; ctx.fillRect(0, 0, 1000, 1100);
      ctx.restore();

      ctx.strokeStyle = outline;
      ctx.lineWidth = 3;
      ctx.stroke(body);
      ctx.lineWidth = 2;
      ctx.beginPath();
      if (type === 'tee') {
        ctx.moveTo(262, 186); ctx.quadraticCurveTo(275, 320, 262, 432);
        ctx.moveTo(738, 186); ctx.quadraticCurveTo(725, 320, 738, 432);
        ctx.moveTo(130, 335); ctx.lineTo(186, 455);
        ctx.moveTo(870, 335); ctx.lineTo(814, 455);
        ctx.moveTo(264, 1010); ctx.lineTo(736, 1010);
      } else {
        if (type === 'baseball') {
          ctx.moveTo(405, 152); ctx.quadraticCurveTo(300, 300, 258, 470);
          ctx.moveTo(595, 152); ctx.quadraticCurveTo(700, 300, 742, 470);
        } else {
          ctx.moveTo(252, 192); ctx.bezierCurveTo(282, 260, 282, 400, 258, 470);
          ctx.moveTo(748, 192); ctx.bezierCurveTo(718, 260, 718, 400, 742, 470);
        }
        ctx.moveTo(262, 982); ctx.lineTo(738, 982);
        ctx.moveTo(100, 860); ctx.lineTo(205, 872);
        ctx.moveTo(900, 860); ctx.lineTo(795, 872);
      }
      ctx.stroke();

      if (view === 'front') {
        if (hooded) {
          // Hood lining: contrast on the baseball hoodie.
          var lining = type === 'baseball' ? trim : base;
          ctx.fillStyle = shade(lining, luminance(lining) > 0.5 ? -0.22 : -0.4);
          var op = new Path2D(G.hoodOpening);
          ctx.fill(op); ctx.stroke(op);
        } else {
          crewNeck(ctx, base, outline, type === 'varsity' ? trim : null, 214, 186);
        }
        if (type === 'hoodie' || type === 'baseball') {
          ctx.save(); ctx.setLineDash([7, 7]); ctx.stroke(new Path2D(G.pocket)); ctx.restore();
          ctx.stroke(new Path2D(G.pocket));
        }
        if (type === 'zip') {
          ctx.beginPath(); ctx.moveTo(330, 760); ctx.lineTo(300, 940); ctx.moveTo(670, 760); ctx.lineTo(700, 940); ctx.stroke();
        }
        if (type === 'varsity') {
          // Welt pockets.
          ctx.lineWidth = 3;
          ctx.stroke(new Path2D('M300 700 L328 692 L362 862 L334 870 Z'));
          ctx.stroke(new Path2D('M700 700 L672 692 L638 862 L666 870 Z'));
        }
      } else {
        if (hooded) {
          ctx.beginPath(); ctx.moveTo(500, 0); ctx.lineTo(500, 226); ctx.stroke();
        } else {
          crewNeck(ctx, base, outline, type === 'varsity' ? trim : null, 172, 158);
        }
      }
    } else if (layer === 'over' && view === 'front') {
      if (type === 'hoodie' || type === 'baseball') {
        var cordBase = type === 'baseball' ? trim : base;
        var cord = luminance(cordBase) > 0.5 ? shade(cordBase, -0.15) : shade(cordBase, 0.85);
        ctx.strokeStyle = cord; ctx.lineWidth = 7;
        ctx.beginPath();
        ctx.moveTo(468, 196); ctx.quadraticCurveTo(458, 300, 462, 392);
        ctx.moveTo(532, 196); ctx.quadraticCurveTo(542, 300, 538, 392);
        ctx.stroke();
        ctx.fillStyle = shade(cord, -0.2);
        ctx.fillRect(457, 388, 10, 26); ctx.fillRect(533, 388, 10, 26);
      }
      if (type === 'zip') {
        ctx.strokeStyle = '#8f949b'; ctx.lineWidth = 9;
        ctx.beginPath(); ctx.moveTo(500, 180); ctx.lineTo(500, 1032); ctx.stroke();
        ctx.fillStyle = '#b8bdc4'; ctx.fillRect(492, 200, 16, 34);
      }
      if (type === 'varsity') {
        // Front opening and popper studs.
        ctx.strokeStyle = outline; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(500, 186); ctx.lineTo(500, 1032); ctx.stroke();
        [250, 390, 530, 670, 810, 950].forEach(function (y) {
          ctx.beginPath(); ctx.arc(500, y, 11, 0, Math.PI * 2);
          ctx.fillStyle = '#E4E6EA'; ctx.fill();
          ctx.strokeStyle = '#8A8F96'; ctx.lineWidth = 2; ctx.stroke();
        });
      }
    }
  }

  // Ribbed crew collar; `stripe` adds the varsity stripe.
  function crewNeck(ctx, base, outline, stripe, dip, innerDip) {
    ctx.save();
    ctx.fillStyle = base;
    ctx.strokeStyle = outline;
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(395, 150); ctx.quadraticCurveTo(500, dip, 605, 150);
    ctx.lineTo(585, 140); ctx.quadraticCurveTo(500, innerDip, 415, 140); ctx.closePath();
    ctx.fill(); ctx.stroke();
    if (stripe) {
      ctx.strokeStyle = stripe; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(404, 146); ctx.quadraticCurveTo(500, (dip + innerDip) / 2 + 1, 596, 146); ctx.stroke();
    }
    ctx.restore();
  }

  // Garment photos: loaded once, then every redraw is instant. Listen for "leavers:photo" to redraw.
  var photoCache = new Map();
  function photoImage(url) {
    if (!url || typeof Image === 'undefined') return null;
    var img = photoCache.get(url);
    if (!img) {
      img = new Image();
      img.crossOrigin = 'anonymous';
      img.decoding = 'async';
      img.onload = function () {
        if (typeof window !== 'undefined' && window.dispatchEvent) window.dispatchEvent(new CustomEvent('leavers:photo', { detail: url }));
      };
      img.src = url;
      photoCache.set(url, img);
    }
    return img.complete && img.naturalWidth ? img : null;
  }
  function photoUrl(d, view) {
    var c = colourOf(d);
    return view === 'back' ? c.back : c.front;
  }
  function hasPhotos(d) { return !!(colourOf(d).front && product(d).photo); }
  function loadPhotos(d) {
    if (!hasPhotos(d)) return Promise.resolve();
    return Promise.all(['front', 'back'].map(function (v) {
      var url = photoUrl(d, v), img = photoImage(url) || photoCache.get(url);
      if (!img || (img.complete && img.naturalWidth)) return null;
      return new Promise(function (res) { img.addEventListener('load', res); img.addEventListener('error', res); });
    }));
  }

  function drawPrint(ctx, d, a, place, k, S, quality) {
    var w = a.mm.w * k, h = a.mm.h * k;
    var c = areaCanvas(d, a.key, w * S * (quality || 1.5));
    ctx.save();
    ctx.globalAlpha = 0.97;
    if (place.line) {
      var L = place.line, dx = L[2] - L[0], dy = L[3] - L[1];
      ctx.translate(L[0] + dx * place.t, L[1] + dy * place.t);
      ctx.rotate(-Math.atan2(dx, dy));
      ctx.drawImage(c, -w / 2, -h / 2, w, h);
    } else {
      ctx.drawImage(c, place.cx - w / 2, place.top, w, h);
    }
    ctx.restore();
  }

  function renderMockup(canvas, d, view, opts) {
    opts = opts || {};
    var ctx = canvas.getContext('2d');
    var S = canvas.width / 1000;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var p = product(d);
    var photos = hasPhotos(d) && !opts.drawn;

    if (photos) {
      // Real garment photo, with the print placed where it is pressed on the garment.
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      var pv = view === 'detail' ? 'back' : view;
      var img = photoImage(photoUrl(d, pv));
      ctx.setTransform(S, 0, 0, S, 0, 0);
      if (view === 'detail') {
        // Zoom in on the back print.
        var bp = p.photo.back, bmm = areasOf(d).back, bw = bmm.w * p.photo.k, bh = bmm.h * p.photo.k;
        var z = 1000 / (bh * 1.18);
        var cx = bp.cx, cy = 50 + bp.top + bh / 2;
        ctx.translate(500, 550);
        ctx.scale(z, z);
        ctx.translate(-cx, -cy);
      }
      if (img) ctx.drawImage(img, 0, 50, 1000, 1000);
      else {
        ctx.fillStyle = '#F2F2F2';
        ctx.fillRect(0, 50, 1000, 1000);
      }
      if (!opts.blank) {
        ctx.translate(0, 50);
        printAreas(d, true).forEach(function (a) {
          var place = p.photo[a.key];
          if (!place || place.view !== pv) return;
          drawPrint(ctx, d, a, place, p.photo.k, S * (view === 'detail' ? 2.5 : 1), opts.quality);
        });
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      return !!img;
    }

    if (opts.background) { ctx.fillStyle = opts.background; ctx.fillRect(0, 0, canvas.width, canvas.height); }
    if (view === 'detail') {
      // Close-up of the back print on the garment colour.
      var mm = areasOf(d).back;
      ctx.fillStyle = bodyHex(d);
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      var h = canvas.height * 0.92, w = h * mm.w / mm.h;
      if (w > canvas.width * 0.92) { w = canvas.width * 0.92; h = w * mm.h / mm.w; }
      var c = areaCanvas(d, 'back', w);
      ctx.drawImage(c, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
      return true;
    }

    ctx.setTransform(S, 0, 0, S, 0, 0);
    drawGarment(ctx, d, view, 'base');
    if (!opts.blank) printAreas(d, true).forEach(function (a) {
      var place = PLACES[a.key];
      if (!place || place.view !== view) return;
      if (p.mockup === 'tee' && a.key === 'sleeve') return;
      drawPrint(ctx, d, a, place, p.k, S, opts.quality);
    });
    drawGarment(ctx, d, view, 'over');
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    return true;
  }

  /* ------------------------------------------------------------------ print files */

  var CRC_TABLE = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
      t[n] = c >>> 0;
    }
    return t;
  })();
  function crc32(bytes) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  // Adds a pHYs chunk so RIP / DTF software opens the file at the right physical size.
  function pngWithDpi(buffer, dpi) {
    var src = new Uint8Array(buffer);
    var ppm = Math.round(dpi / 0.0254);
    var chunk = new Uint8Array(21);
    var dv = new DataView(chunk.buffer);
    dv.setUint32(0, 9);
    chunk.set([0x70, 0x48, 0x59, 0x73], 4); // pHYs
    dv.setUint32(8, ppm); dv.setUint32(12, ppm); chunk[16] = 1;
    dv.setUint32(17, crc32(chunk.subarray(4, 17)));
    var ihdrEnd = 8 + 8 + 13 + 4;
    var out = new Uint8Array(src.length + chunk.length);
    out.set(src.subarray(0, ihdrEnd), 0);
    out.set(chunk, ihdrEnd);
    out.set(src.subarray(ihdrEnd), ihdrEnd + chunk.length);
    return out;
  }

  function canvasToPng(canvas, dpi) {
    var toBlob = canvas.convertToBlob ? canvas.convertToBlob({ type: 'image/png' }) : new Promise(function (res, rej) {
      canvas.toBlob(function (b) { b ? res(b) : rej(new Error('Could not export PNG')); }, 'image/png');
    });
    return toBlob.then(function (b) { return b.arrayBuffer(); })
      .then(function (buf) { return new Blob([pngWithDpi(buf, dpi)], { type: 'image/png' }); });
  }

  function slug(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40); }

  function renderPrintFiles(d, opts) {
    opts = opts || {};
    var dpi = opts.dpi || 300;
    var pd = Object.assign({}, d, { _print: true });
    return Promise.all([loadFonts(pd), loadLogo(pd)]).then(function () {
      var missing = fontsMissing(pd);
      if (missing.length) throw new Error('Fonts not loaded: ' + missing.join(', ') + ' — check the internet connection and try again');
      var jobs = printAreas(pd, false).map(function (a) {
        var w = Math.round(a.mm.w / 25.4 * dpi), h = Math.round(a.mm.h / 25.4 * dpi);
        var c = makeCanvas(w, h);
        renderArea(c, pd, a.key);
        var name = [opts.prefix || 'leavers', d.product, slug(d.size), a.key, slug(d.personal.text)].filter(Boolean).join('_') + '_' + dpi + 'dpi.png';
        return canvasToPng(c, dpi).then(function (blob) {
          return { key: a.key, label: a.label, mm: a.mm, width: w, height: h, filename: name, blob: blob, canvas: c };
        });
      });
      return Promise.all(jobs);
    });
  }

  /* ------------------------------------------------------------------ design codes */

  function strip(d) {
    return JSON.parse(JSON.stringify(d, function (k, v) { return k.charAt(0) === '_' ? undefined : v; }));
  }
  function b64url(bytes) {
    var s = '';
    for (var i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function unb64url(s) {
    s = s.replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    var bin = atob(s), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function streamBytes(bytes, stream) {
    return new Response(new Blob([bytes]).stream().pipeThrough(stream)).arrayBuffer().then(function (b) { return new Uint8Array(b); });
  }

  // Compact, URL-safe design code: "z" + deflated JSON, or "j" + plain JSON where compression isn't available.
  function encode(d) {
    var bytes = new TextEncoder().encode(JSON.stringify(strip(d)));
    if (typeof CompressionStream === 'undefined') return Promise.resolve('j' + b64url(bytes));
    return streamBytes(bytes, new CompressionStream('deflate-raw')).then(function (z) { return 'z' + b64url(z); });
  }
  function decode(code) {
    code = String(code || '').trim();
    var m = code.match(/[#&?]d=([A-Za-z0-9_\-]+)/);
    if (m) code = m[1];
    var kind = code.charAt(0), bytes = unb64url(code.slice(1));
    var p = kind === 'z' ? streamBytes(bytes, new DecompressionStream('deflate-raw')) : Promise.resolve(bytes);
    return p.then(function (b) { return upgrade(JSON.parse(new TextDecoder().decode(b))); });
  }
  function upgrade(d) {
    var base = defaultDesign(d.product);
    return {
      v: 1, product: base.product,
      garment: d.garment || base.garment, size: d.size || '',
      back: Object.assign(base.back, d.back || {}),
      front: Object.assign(base.front, d.front || {}),
      personal: Object.assign(base.personal, d.personal || {})
    };
  }

  function priceFor(productKey, size) {
    var p = PRODUCTS[productKey] || PRODUCTS[DEFAULT_PRODUCT];
    return Math.round((p.price + ((p.upcharge || {})[size] || 0)) * 100) / 100;
  }

  root.LeaversEngine = {
    REF: REF,
    FONTS: FONTS, INKS: INKS, GARMENTS: GARMENTS, PRODUCTS: PRODUCTS, DEFAULT_PRODUCT: DEFAULT_PRODUCT,
    colourOptions: colourOptions, defaultColour: defaultColour, colourOf: colourOf, hasPhotos: hasPhotos, loadPhotos: loadPhotos, isKids: isKids, KIDS_SIZES: KIDS_SIZES, bodyHex: bodyHex, trimHex: trimHex,
    BACK_TEMPLATES: BACK_TEMPLATES, FRONT_STYLES: FRONT_STYLES, PERSONAL_POSITIONS: PERSONAL_POSITIONS,
    ICON_NAMES: ICON_NAMES, SAMPLE_NAMES: SAMPLE_NAMES,
    defaultDesign: defaultDesign, upgrade: upgrade,
    fontsCssUrl: fontsCssUrl, fontSpec: fontSpec, loadFonts: loadFonts, fontsMissing: fontsMissing, loadLogo: loadLogo, usesLogo: usesLogo,
    cleanNames: cleanNames, formatName: formatName,
    inkHex: inkHex, garmentHex: garmentHex, contrastRatio: contrastRatio, byId: byId,
    printAreas: printAreas, renderArea: renderArea, areaCanvas: areaCanvas, renderMockup: renderMockup,
    renderPrintFiles: renderPrintFiles, canvasToPng: canvasToPng, pngWithDpi: pngWithDpi,
    encode: encode, decode: decode, priceFor: priceFor
  };
})(typeof window !== 'undefined' ? window : self);
