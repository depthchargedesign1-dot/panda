/*
 * Foxy live personaliser
 * Draws a live mockup of the customer's design on a <canvas> as they type.
 * Mockups: card (front + inside), drinkware (cylindrical wrap), apparel, bauble, box, flat (plaques, blocks, slate, wood, acrylic),
 * and "photo": the product's own photo with a proof card of everything the customer has entered.
 * A drawn mockup is only used when the product really is that shape (see resolveMode); anything else
 * (bobble hats, scarves, footballs, cufflinks…) uses "photo", so a hat never shows up as a T-shirt.
 * No external dependencies. Values are submitted as normal line item properties by the product form.
 */
(function () {
  'use strict';

  const root = document.querySelector('[data-product-section]');
  const canvas = root && root.querySelector('[data-personaliser-canvas]');
  const configEl = document.querySelector('[data-personaliser-config]');
  if (!canvas || !configEl) return;

  const config = JSON.parse(configEl.textContent);
  // `ctx` is rebound while painting offscreen layers (see offscreen()), so every helper draws on the active layer.
  let ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const css = getComputedStyle(document.documentElement);
  const brand = {
    orange: css.getPropertyValue('--fx-primary').trim() || '#FF6A13',
    pink: css.getPropertyValue('--fx-pink').trim() || '#FF2D87',
    purple: css.getPropertyValue('--fx-purple').trim() || '#7A2BF5',
    teal: css.getPropertyValue('--fx-teal').trim() || '#00B8A9',
    yellow: css.getPropertyValue('--fx-yellow').trim() || '#FFC83D',
    ink: css.getPropertyValue('--fx-ink').trim() || '#1D1240',
    tint: css.getPropertyValue('--fx-tint').trim() || '#FFF4EA'
  };
  const title = (config.title || '').toLowerCase();
  const kindText = (title + ' ' + (config.productType || '')).toLowerCase();

  // Each drawn mockup is only trusted for products that really look like it.
  const MOCKUP_FITS = {
    card: /\b(cards?|invitations?|invites?)\b/,
    drinkware: /\b(mugs?|cups?|glass(es)?|tumblers?|bottles?|flasks?|flutes?|tankards?|steins?|jars?)\b/,
    apparel: /\b(t-?shirts?|tees?|hoodies?|sweatshirts?|jumpers?|vests?|baby ?grows?|bodysuits?|totes?|bags?|aprons?|bandanas?|bibs?|sash(es)?|pyjamas?)\b/,
    bauble: /\b(baubles?|ornaments?|decorations?)\b|magic key/,
    box: /\b(box(es)?|advent|game cases?|sleeves?|calendars?)\b/,
    flat: /\b(slates?|plaques?|blocks?|acrylic|wooden|wood|signs?|coasters?|keyrings?|magnets?|tags?|medals?|frames?|panels?|tiles?|prints?|posters?|bookmarks?|led|golf balls?|awards?|stands?|clocks?|placemats?|jigsaws?|canvas|chopping|boards?)\b/
  };
  function resolveMode() {
    const m = String(config.mockup || 'photo').toLowerCase();
    const fits = MOCKUP_FITS[m];
    if (fits && fits.test(kindText)) return m;
    return 'photo';
  }
  const mode = resolveMode();

  const state = {
    view: 'front',
    font: (config.fonts && config.fonts[0] || 'Baloo 2').trim(),
    colour: (config.colours && config.colours[0] || brand.ink).trim(),
    variantOptions: [],
    fields: [],
    base: null,
    showPhoto: false
  };

  /* ------------------------------------------------------------------ fields */

  const ROLE_RULES = [
    ['photo', /photo|upload|logo|artwork|scan/],
    ['secondary', /message|list|reasons|achievements|recipe|text$/],
    ['number', /age|number|year|date|est|weight|time|due/],
    ['primary', /.*/]
  ];

  function roleFor(label) {
    const l = label.toLowerCase();
    for (const [role, re] of ROLE_RULES) if (re.test(l)) return role;
    return 'primary';
  }

  root.querySelectorAll('[data-field]').forEach((input) => {
    const label = input.dataset.fieldLabel || '';
    const field = { input, label, kind: input.dataset.fieldKind, role: roleFor(label), value: '', image: null };
    // A lone text field is always the headline, even if its label looks like a message.
    state.fields.push(field);
    const counter = input.closest('.field') && input.closest('.field').querySelector('[data-count]');
    if (field.kind === 'image') {
      input.addEventListener('change', () => {
        const file = input.files && input.files[0];
        const thumb = input.closest('.field').querySelector('[data-upload-thumb]');
        if (!file) { field.image = null; draw(); return; }
        const url = URL.createObjectURL(file);
        const img = new Image();
        img.onload = () => { field.image = img; started(); draw(); };
        img.src = url;
        if (thumb) thumb.innerHTML = '<img alt="" src="' + url + '">';
      });
    } else {
      input.addEventListener('input', () => {
        field.value = input.value;
        started();
        if (counter) counter.textContent = input.value.length + '/' + input.maxLength;
        draw();
      });
    }
  });

  // The stage shows the product photo first; the first time the customer personalises, switch to their design.
  let hasStarted = false;
  function started() {
    if (hasStarted) return;
    hasStarted = true;
    if (window.FoxyGallery) window.FoxyGallery.showLive();
  }

  const textFields = state.fields.filter((f) => f.kind !== 'image');
  if (textFields.length && !textFields.some((f) => f.role === 'primary')) textFields[0].role = 'primary';

  function get(role) {
    const f = state.fields.find((x) => x.role === role && x.kind !== 'image');
    return f ? { text: f.value.trim(), placeholder: f.input.placeholder || f.label, empty: !f.value.trim() } : null;
  }
  function photo() {
    const f = state.fields.find((x) => x.kind === 'image');
    return f ? f.image : null;
  }
  function hasPhotoField() { return state.fields.some((x) => x.kind === 'image'); }

  /* ------------------------------------------------------------------ controls */

  root.querySelectorAll('[data-font]').forEach((btn) => btn.addEventListener('click', () => {
    state.font = btn.dataset.font;
    root.querySelector('[data-font-input]').value = state.font;
    root.querySelectorAll('[data-font]').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    loadFont(state.font).then(draw);
  }));
  root.querySelectorAll('[data-colour]').forEach((btn) => btn.addEventListener('click', () => {
    state.colour = btn.dataset.colour;
    root.querySelector('[data-colour-input]').value = state.colour;
    root.querySelectorAll('[data-colour]').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    draw();
  }));
  root.querySelectorAll('[data-view]').forEach((btn) => btn.addEventListener('click', () => {
    state.view = btn.dataset.view;
    root.querySelectorAll('[data-view]').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    draw();
  }));
  document.addEventListener('foxy:variant-change', (e) => {
    state.variantOptions = (e.detail && e.detail.options) || [];
    const v = e.detail && e.detail.variant;
    const src = v && v.featured_media && v.featured_media.preview_image && v.featured_media.preview_image.src;
    if (mode === 'photo' && src) loadBase(src + (src.indexOf('?') === -1 ? '?' : '&') + 'width=1200');
    draw();
  });

  function loadFont(name) {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    return document.fonts.load('700 48px "' + name + '"').catch(() => {});
  }

  function loadBase(src) {
    const img = new Image();
    img.onload = () => { state.base = img; draw(); };
    img.src = src;
  }
  // The photo proof always needs the product photo; drawn mockups use it only when the theme setting allows.
  if (config.baseImage && (config.useBaseImage !== false || mode === 'photo')) loadBase(config.baseImage);

  /* ------------------------------------------------------------------ helpers */

  function fontStr(size, family, weight) {
    return (weight || 700) + ' ' + Math.round(size) + 'px "' + (family || state.font) + '", "Baloo 2", system-ui, sans-serif';
  }

  function fitText(text, maxWidth, maxSize, minSize, family) {
    let size = maxSize;
    ctx.font = fontStr(size, family);
    while (size > (minSize || 14) && ctx.measureText(text).width > maxWidth) {
      size -= 2;
      ctx.font = fontStr(size, family);
    }
    return size;
  }

  function drawFitted(t, x, y, maxWidth, maxSize, opts) {
    if (!t) return;
    const o = opts || {};
    const text = t.empty ? t.placeholder : t.text;
    const target = o.ctx || ctx;
    const size = fitText(text, maxWidth, maxSize, o.minSize || 16, o.family);
    target.save();
    target.font = fontStr(size, o.family);
    target.textAlign = o.align || 'center';
    target.textBaseline = 'middle';
    target.globalAlpha = t.empty ? 0.38 : 1;
    if (o.stroke) {
      target.lineJoin = 'round';
      target.lineWidth = Math.max(4, size / 7);
      target.strokeStyle = o.stroke;
      target.strokeText(text, x, y);
    }
    target.fillStyle = o.colour || state.colour;
    target.fillText(text, x, y);
    target.restore();
  }

  function wrapLines(text, maxWidth, size, family) {
    ctx.font = fontStr(size, family, 600);
    const lines = [];
    text.split(/\n/).forEach((para) => {
      let line = '';
      para.split(/\s+/).forEach((word) => {
        const test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxWidth && line) { lines.push(line); line = word; } else { line = test; }
      });
      lines.push(line);
    });
    return lines;
  }

  function drawWrapped(t, x, y, maxWidth, maxHeight, maxSize, opts) {
    if (!t) return;
    const o = opts || {};
    const text = t.empty ? t.placeholder : t.text;
    let size = maxSize;
    let lines = wrapLines(text, maxWidth, size, o.family);
    while (size > 14 && lines.length * size * 1.25 > maxHeight) {
      size -= 2;
      lines = wrapLines(text, maxWidth, size, o.family);
    }
    ctx.save();
    ctx.font = fontStr(size, o.family, 600);
    ctx.fillStyle = o.colour || state.colour;
    ctx.textAlign = o.align || 'center';
    ctx.textBaseline = 'middle';
    ctx.globalAlpha = t.empty ? 0.38 : 1;
    const total = lines.length * size * 1.25;
    lines.forEach((line, i) => ctx.fillText(line, x, y - total / 2 + size * 0.62 + i * size * 1.25));
    ctx.restore();
  }

  function roundRect(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

  function drawCover(img, x, y, w, h, c) {
    const target = c || ctx;
    const s = Math.max(w / img.width, h / img.height);
    const sw = w / s;
    const sh = h / s;
    target.drawImage(img, (img.width - sw) / 2, (img.height - sh) / 2, sw, sh, x, y, w, h);
  }

  function photoSlot(x, y, w, h, r, c) {
    const target = c || ctx;
    const img = photo();
    if (!img && !hasPhotoField()) return false;
    target.save();
    roundRect(target, x, y, w, h, r);
    target.clip();
    if (img) {
      drawCover(img, x, y, w, h, target);
    } else {
      target.fillStyle = 'rgba(255,255,255,.55)';
      target.fillRect(x, y, w, h);
      target.fillStyle = 'rgba(29,18,64,.45)';
      target.font = fontStr(Math.min(h / 6, w / 9), 'Baloo 2');
      target.textAlign = 'center';
      target.textBaseline = 'middle';
      target.fillText('📷 Your photo', x + w / 2, y + h / 2);
    }
    target.restore();
    return true;
  }

  function background() {
    const g = ctx.createLinearGradient(0, 0, W, H);
    g.addColorStop(0, '#FFF7F0');
    g.addColorStop(1, '#F6F0FF');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    // soft confetti dots
    const dots = [[90, 120, 14, brand.yellow], [900, 160, 10, brand.pink], [130, 860, 12, brand.teal], [880, 880, 16, brand.purple], [520, 70, 8, brand.orange]];
    dots.forEach(([x, y, r, c]) => { ctx.globalAlpha = 0.5; ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); });
    ctx.globalAlpha = 1;
  }

  function shadow(blur, offsetY) {
    ctx.shadowColor = 'rgba(29,18,64,.25)';
    ctx.shadowBlur = blur;
    ctx.shadowOffsetY = offsetY;
  }
  function noShadow() { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }

  function optionColour(fallback) {
    const map = {
      red: '#C8102E', gold: '#D4AF37', silver: '#C0C4CC', clear: 'rgba(220,235,255,.55)', green: '#1E7B4F',
      black: '#1F1F24', white: '#FFFFFF', cream: '#F3E9D2', pink: '#F7B6CF', sage: '#A9BFA4', lilac: '#C8B6E8',
      navy: '#1E2A55', grey: '#B9BCC4', heather: '#C9CBD1', blue: '#3D7BE0', frosted: 'rgba(235,240,245,.85)'
    };
    for (const v of state.variantOptions) {
      const key = String(v).toLowerCase();
      for (const name in map) if (key.indexOf(name) !== -1) return map[name];
    }
    return fallback;
  }

  /* ------------------------------------------------------------------ design panel
   * Renders photo + headline + message into a rectangle. Used by every mockup.
   */
  function designPanel(x, y, w, h, opts) {
    const o = opts || {};
    const primary = get('primary');
    const secondary = get('secondary');
    const number = get('number');
    const hasPhoto = hasPhotoField();
    let cursor = y;
    if (hasPhoto) {
      const ph = h * (primary || secondary ? 0.62 : 0.9);
      photoSlot(x + w * 0.06, y + h * 0.04, w * 0.88, ph, Math.min(w, h) * 0.04);
      cursor = y + h * 0.04 + ph;
    }
    const remaining = y + h - cursor;
    if (number && !hasPhoto) {
      drawFitted(number, x + w / 2, cursor + remaining * 0.22, w * 0.5, remaining * 0.32, { stroke: o.stroke, colour: o.colour });
      cursor += remaining * 0.38;
    }
    const rem2 = y + h - cursor;
    if (primary) {
      drawFitted(primary, x + w / 2, cursor + rem2 * (secondary ? 0.3 : 0.5), w * 0.9, Math.min(rem2 * (secondary ? 0.42 : 0.7), w * 0.22), { stroke: o.stroke, colour: o.colour });
    }
    if (secondary) {
      drawWrapped(secondary, x + w / 2, cursor + rem2 * (primary ? 0.72 : 0.5), w * 0.86, rem2 * (primary ? 0.45 : 0.85), Math.min(56, w * 0.09), { colour: o.colour });
    }
    if (number && hasPhoto) {
      drawFitted(number, x + w - w * 0.12, y + h * 0.1, w * 0.18, w * 0.12, { stroke: '#fff', colour: o.colour });
    }
  }

  /* ------------------------------------------------------------------ mockups */

  function drawCard() {
    background();
    const primary = get('primary');
    const secondary = get('secondary');
    const number = get('number');
    if (state.view === 'inside') {
      // Open card: two pages
      shadow(40, 18);
      ctx.fillStyle = '#fff';
      roundRect(ctx, 90, 170, 410, 640, 10); ctx.fill();
      roundRect(ctx, 500, 170, 410, 640, 10); ctx.fill();
      noShadow();
      const lg = ctx.createLinearGradient(440, 0, 560, 0);
      lg.addColorStop(0, 'rgba(0,0,0,0)'); lg.addColorStop(0.5, 'rgba(0,0,0,.12)'); lg.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = lg; ctx.fillRect(440, 170, 120, 640);
      ctx.fillStyle = brand.tint; roundRect(ctx, 110, 190, 370, 600, 6); ctx.fill();
      ctx.font = fontStr(34, 'Baloo 2'); ctx.fillStyle = 'rgba(29,18,64,.25)'; ctx.textAlign = 'center';
      ctx.fillText('🦊 Foxy Printing', 295, 760);
      const msg = secondary || primary;
      drawWrapped(msg, 705, 470, 340, 500, 54, { family: state.font === 'Baloo 2' ? 'Caveat' : state.font });
      return;
    }
    // Front
    const x = 230; const y = 90; const w = 540; const h = 780;
    shadow(46, 22);
    ctx.fillStyle = '#fff';
    roundRect(ctx, x, y, w, h, 10); ctx.fill();
    noShadow();
    ctx.save();
    roundRect(ctx, x, y, w, h, 10); ctx.clip();
    if (state.base) {
      drawCover(state.base, x, y, w, h);
    } else {
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, brand.pink); g.addColorStop(0.55, brand.orange); g.addColorStop(1, brand.yellow);
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
      for (let i = 0; i < 40; i++) {
        ctx.fillStyle = [brand.purple, brand.teal, '#fff', brand.yellow][i % 4];
        ctx.globalAlpha = 0.7;
        ctx.save();
        ctx.translate(x + ((i * 97) % w), y + ((i * 53) % (h * 0.45)));
        ctx.rotate(i);
        ctx.fillRect(-6, -14, 12, 28);
        ctx.restore();
      }
      ctx.globalAlpha = 1;
      ctx.font = fontStr(84, 'Pacifico', 400); ctx.fillStyle = '#fff'; ctx.textAlign = 'center';
      ctx.fillText('Happy', x + w / 2, y + 250);
      ctx.fillText('Birthday', x + w / 2, y + 360);
    }
    ctx.restore();
    // Highlight band on the left edge (card fold)
    const fold = ctx.createLinearGradient(x, 0, x + 26, 0);
    fold.addColorStop(0, 'rgba(0,0,0,.18)'); fold.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = fold; ctx.fillRect(x, y, 26, h);

    if (config.zone && state.base) { drawZone(x, y, w, h); return; }
    if (hasPhotoField()) photoSlot(x + 110, y + 410, w - 220, 220, 16);
    if (number) {
      ctx.save(); shadow(18, 8);
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x + w - 95, y + 100, 66, 0, Math.PI * 2); ctx.fill();
      noShadow(); ctx.restore();
      drawFitted(number, x + w - 95, y + 104, 100, 76, { colour: brand.pink });
    }
    const nameY = hasPhotoField() ? y + h - 110 : y + h - 220;
    drawFitted(primary || secondary, x + w / 2, nameY, w - 80, 110, { stroke: '#fff' });
  }

  function drawPhotoZone() {
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, W, H);
    const s = Math.min(W / state.base.width, H / state.base.height);
    const iw = state.base.width * s;
    const ih = state.base.height * s;
    const ix = (W - iw) / 2;
    const iy = (H - ih) / 2;
    ctx.drawImage(state.base, ix, iy, iw, ih);
    drawZone(ix, iy, iw, ih);
  }

  function drawZone(x, y, w, h) {
    const z = config.zone;
    const t = get('primary') || get('secondary');
    if (z.font) state.font = z.font;
    drawFitted(t, x + (z.x + z.w / 2) * w, y + (z.y + z.h / 2) * h, z.w * w, z.h * h, { colour: z.color || state.colour, stroke: z.stroke });
  }

  function cylinderWrap(src, dx, dy, dw, dh) {
    // Map the flat design onto a cylinder by sampling columns with an arcsine curve.
    const sw = src.width;
    const steps = Math.round(dw);
    for (let i = 0; i < steps; i++) {
      const u = (i + 0.5) / steps;             // 0..1 across the visible face
      const theta = Math.asin(u * 2 - 1);      // -pi/2..pi/2
      const sx = ((theta / Math.PI) + 0.5) * sw; // 0..sw
      const shade = Math.cos(theta);
      ctx.globalAlpha = 0.35 + 0.65 * shade;
      ctx.drawImage(src, Math.max(0, Math.min(sw - 1, sx)), 0, 1, src.height, dx + i, dy, 1.6, dh);
    }
    ctx.globalAlpha = 1;
  }

  function offscreen(w, h, paint) {
    const c = document.createElement('canvas');
    c.width = Math.round(w); c.height = Math.round(h);
    const prev = ctx;
    ctx = c.getContext('2d');
    try { paint(); } finally { ctx = prev; }
    return c;
  }

  function drawDrinkware() {
    background();
    const isMug = /mug|cup\b|coffee|enamel/.test(title) && !/can cup/.test(title);
    const isGlass = /glass|flute|can cup|jar|wine|gin|pint|whisky/.test(title);
    const isTumbler = /tumbler|bottle|flask/.test(title);
    const body = optionColour(isGlass ? 'rgba(225,240,255,.55)' : '#FFFFFF');
    let x = 300; let y = 220; let w = 400; let h = 560;
    if (isMug) { x = 250; y = 280; w = 420; h = 440; }
    if (/40oz/.test(title)) { x = 320; y = 170; w = 360; h = 660; }
    if (/flute|wine|gin/.test(title)) { x = 340; y = 160; w = 320; h = 380; }

    // Lid / straw for tumblers & can cups
    if (isTumbler || /can cup/.test(title)) {
      ctx.fillStyle = /can cup/.test(title) ? '#C9A97A' : '#2A2A33';
      shadow(20, 6); roundRect(ctx, x - 6, y - 50, w + 12, 56, 18); ctx.fill(); noShadow();
      if (/can cup|40oz/.test(title)) { ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.fillRect(x + w * 0.6, y - 210, 22, 170); }
    }
    // Handle
    if (isMug || /40oz/.test(title)) {
      ctx.lineWidth = 46; ctx.strokeStyle = body === '#FFFFFF' ? '#EDEAF2' : body;
      ctx.beginPath(); ctx.arc(x + w + 10, y + h * 0.45, h * 0.22, -Math.PI / 2.2, Math.PI / 2.2); ctx.stroke();
    }
    // Body
    shadow(40, 20);
    ctx.fillStyle = body;
    roundRect(ctx, x, y, w, h, /flute|wine|gin/.test(title) ? 120 : 28); ctx.fill();
    noShadow();
    if (/flute|wine|gin/.test(title)) { // stem
      ctx.fillStyle = 'rgba(225,240,255,.8)'; ctx.fillRect(x + w / 2 - 10, y + h, 20, 220);
      ctx.beginPath(); ctx.ellipse(x + w / 2, y + h + 230, 110, 24, 0, 0, Math.PI * 2); ctx.fill();
    }
    // Design wrapped round the body
    const dark = /#1F1F24|#2A2A33|#1E2A55/.test(body);
    const design = offscreen(w * 1.6, h * 0.62, () => {
      designPanel(0, 0, w * 1.6, h * 0.62, { colour: dark && state.colour === brand.ink ? '#fff' : state.colour });
    });
    cylinderWrap(design, x + 10, y + h * 0.19, w - 20, h * 0.62);
    // Specular highlight + edge shading
    const hl = ctx.createLinearGradient(x, 0, x + w, 0);
    hl.addColorStop(0, 'rgba(0,0,0,.18)'); hl.addColorStop(0.18, 'rgba(255,255,255,.0)');
    hl.addColorStop(0.28, 'rgba(255,255,255,.55)'); hl.addColorStop(0.34, 'rgba(255,255,255,0)');
    hl.addColorStop(0.85, 'rgba(0,0,0,.05)'); hl.addColorStop(1, 'rgba(0,0,0,.22)');
    ctx.fillStyle = hl; roundRect(ctx, x, y, w, h, 28); ctx.fill();
  }

  function shirtPath(c, cx, top, s, kind) {
    c.beginPath();
    if (kind === 'bodysuit') {
      c.moveTo(cx - 120 * s, top);
      c.quadraticCurveTo(cx, top + 60 * s, cx + 120 * s, top);
      c.lineTo(cx + 250 * s, top + 90 * s); c.lineTo(cx + 200 * s, top + 200 * s); c.lineTo(cx + 170 * s, top + 180 * s);
      c.lineTo(cx + 170 * s, top + 520 * s);
      c.quadraticCurveTo(cx + 120 * s, top + 640 * s, cx + 40 * s, top + 680 * s); c.lineTo(cx - 40 * s, top + 680 * s);
      c.quadraticCurveTo(cx - 120 * s, top + 640 * s, cx - 170 * s, top + 520 * s);
      c.lineTo(cx - 170 * s, top + 180 * s); c.lineTo(cx - 200 * s, top + 200 * s); c.lineTo(cx - 250 * s, top + 90 * s);
    } else if (kind === 'tote') {
      c.rect(cx - 250 * s, top + 120 * s, 500 * s, 560 * s);
    } else if (kind === 'bandana') {
      c.moveTo(cx - 330 * s, top + 120 * s); c.lineTo(cx + 330 * s, top + 120 * s); c.lineTo(cx, top + 640 * s);
    } else {
      c.moveTo(cx - 110 * s, top);
      c.quadraticCurveTo(cx, top + 70 * s, cx + 110 * s, top);
      c.lineTo(cx + 330 * s, top + 90 * s); c.lineTo(cx + 280 * s, top + 280 * s); c.lineTo(cx + 210 * s, top + 250 * s);
      c.lineTo(cx + 210 * s, top + 700 * s); c.lineTo(cx - 210 * s, top + 700 * s); c.lineTo(cx - 210 * s, top + 250 * s);
      c.lineTo(cx - 280 * s, top + 280 * s); c.lineTo(cx - 330 * s, top + 90 * s);
    }
    c.closePath();
  }

  function drawApparel() {
    background();
    let kind = 'tee';
    if (/baby grow|vest|bodysuit|outfit/.test(title)) kind = 'bodysuit';
    if (/bag|tote|sash|apron|blanket|bib/.test(title)) kind = 'tote';
    if (/bandana/.test(title)) kind = 'bandana';
    const fabric = optionColour(/hi-vis/.test(title) ? '#D9F23A' : /christmas jumper/.test(title) ? '#C8102E' : '#FFFFFF');
    const cx = 500; const top = 140; const s = 1;
    if (kind === 'tote') { // handles
      ctx.lineWidth = 26; ctx.strokeStyle = '#E8DCC4';
      ctx.beginPath(); ctx.arc(cx, top + 130, 150, Math.PI, 0); ctx.stroke();
    }
    shadow(40, 18);
    ctx.fillStyle = kind === 'tote' && fabric === '#FFFFFF' ? '#F3EBDD' : fabric;
    shirtPath(ctx, cx, top, s, kind); ctx.fill();
    noShadow();
    // Fabric shading
    ctx.save(); shirtPath(ctx, cx, top, s, kind); ctx.clip();
    const sh = ctx.createLinearGradient(cx - 300, 0, cx + 300, 0);
    sh.addColorStop(0, 'rgba(0,0,0,.10)'); sh.addColorStop(0.5, 'rgba(255,255,255,.06)'); sh.addColorStop(1, 'rgba(0,0,0,.12)');
    ctx.fillStyle = sh; ctx.fillRect(0, 0, W, H);
    ctx.restore();
    const darkFabric = /#1F1F24|#1E2A55|#C8102E|#1E7B4F/.test(fabric);
    const colour = darkFabric && state.colour === brand.ink ? '#FFFFFF' : state.colour;
    let area = [cx - 150, top + 190, 300, 330];
    if (kind === 'bodysuit') area = [cx - 120, top + 170, 240, 300];
    if (kind === 'tote') area = [cx - 190, top + 220, 380, 400];
    if (kind === 'bandana') area = [cx - 160, top + 170, 320, 200];
    designPanel(area[0], area[1], area[2], area[3], { colour });
  }

  function drawBauble() {
    background();
    const cx = 500; const cy = 560; const r = 300;
    ctx.strokeStyle = '#C8A24A'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(cx, 40); ctx.lineTo(cx, cy - r - 60); ctx.stroke();
    ctx.fillStyle = '#C8A24A'; roundRect(ctx, cx - 50, cy - r - 70, 100, 70, 10); ctx.fill();
    const flat = /wooden|santa|key/.test(title);
    const base = optionColour(flat ? '#E9C99B' : '#C8102E');
    shadow(50, 24);
    if (/key/.test(title)) {
      ctx.fillStyle = '#D4AF37';
      ctx.beginPath(); ctx.arc(cx, cy - 120, 150, 0, Math.PI * 2); ctx.fill();
      ctx.fillRect(cx - 34, cy - 10, 68, 330); ctx.fillRect(cx, cy + 220, 110, 40); ctx.fillRect(cx, cy + 280, 80, 40);
      noShadow();
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(cx, cy - 120, 110, 0, Math.PI * 2); ctx.fill();
      drawFitted(get('primary'), cx, cy - 120, 190, 64, { colour: state.colour === '#FFFFFF' ? brand.ink : state.colour });
      return;
    }
    const g = ctx.createRadialGradient(cx - r * 0.35, cy - r * 0.4, r * 0.1, cx, cy, r);
    g.addColorStop(0, '#ffffff'); g.addColorStop(0.18, base); g.addColorStop(1, shade(base, -0.35));
    ctx.fillStyle = flat ? base : g;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
    noShadow();
    ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, r * 0.82, 0, Math.PI * 2); ctx.clip();
    const colour = state.colour === brand.ink && !flat ? '#FFFFFF' : state.colour;
    designPanel(cx - r * 0.7, cy - r * 0.62, r * 1.4, r * 1.24, { colour, stroke: flat ? null : 'rgba(0,0,0,.25)' });
    ctx.restore();
    if (!flat) { // gloss
      ctx.fillStyle = 'rgba(255,255,255,.35)';
      ctx.beginPath(); ctx.ellipse(cx - r * 0.38, cy - r * 0.45, r * 0.22, r * 0.12, -0.6, 0, Math.PI * 2); ctx.fill();
    }
  }

  function shade(hex, amt) {
    if (!/^#([0-9a-f]{6})$/i.test(hex)) return 'rgba(0,0,0,.4)';
    const n = parseInt(hex.slice(1), 16);
    const f = (c) => Math.max(0, Math.min(255, Math.round(c + c * amt)));
    return 'rgb(' + f(n >> 16) + ',' + f((n >> 8) & 255) + ',' + f(n & 255) + ')';
  }

  function drawBox() {
    background();
    const christmas = /christmas|advent|selection|elf|santa/.test(title);
    const game = /game case/.test(title);
    if (game) {
      // Video game case: portrait case with spine and cover art
      const x = 270; const y = 90; const w = 470; const h = 800;
      shadow(46, 22); ctx.fillStyle = '#1E4FBF'; roundRect(ctx, x - 26, y, w + 26, h, 18); ctx.fill(); noShadow();
      ctx.fillStyle = '#163C93'; ctx.fillRect(x - 26, y, 26, h);
      ctx.save(); roundRect(ctx, x + 14, y + 70, w - 28, h - 90, 6); ctx.clip();
      const g = ctx.createLinearGradient(0, y, 0, y + h);
      g.addColorStop(0, brand.purple); g.addColorStop(1, brand.pink);
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
      designPanel(x + 14, y + 70, w - 28, h - 90, { colour: state.colour === brand.ink ? '#fff' : state.colour, stroke: 'rgba(0,0,0,.35)' });
      ctx.restore();
      ctx.fillStyle = '#fff'; ctx.font = fontStr(30, 'Bebas Neue', 400); ctx.textAlign = 'left';
      ctx.fillText('FOXY GAMES', x + 20, y + 48);
      return;
    }
    const front = christmas ? '#B0122B' : brand.purple;
    const top = christmas ? '#D61F3A' : brand.pink;
    const side = christmas ? '#7E0C1F' : shade(brand.purple.startsWith('#') ? brand.purple : '#7A2BF5', -0.3);
    const x = 200; const y = 330; const w = 520; const h = 470; const d = 120;
    shadow(50, 26);
    ctx.fillStyle = front; ctx.fillRect(x, y, w, h);
    noShadow();
    ctx.fillStyle = top;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + d, y - d * 0.75); ctx.lineTo(x + w + d, y - d * 0.75); ctx.lineTo(x + w, y); ctx.closePath(); ctx.fill();
    ctx.fillStyle = side;
    ctx.beginPath(); ctx.moveTo(x + w, y); ctx.lineTo(x + w + d, y - d * 0.75); ctx.lineTo(x + w + d, y + h - d * 0.75); ctx.lineTo(x + w, y + h); ctx.closePath(); ctx.fill();
    // ribbon
    ctx.fillStyle = christmas ? '#D4AF37' : brand.yellow;
    ctx.fillRect(x + w * 0.5 - 18, y, 36, h);
    ctx.beginPath(); ctx.moveTo(x + w * 0.5 - 18 + d * 0.0, y); ctx.lineTo(x + w * 0.5 - 18 + d, y - d * 0.75); ctx.lineTo(x + w * 0.5 + 18 + d, y - d * 0.75); ctx.lineTo(x + w * 0.5 + 18, y); ctx.fill();
    // label plate
    ctx.fillStyle = '#fff';
    shadow(14, 6); roundRect(ctx, x + 60, y + 90, w - 120, h - 180, 22); ctx.fill(); noShadow();
    if (christmas) {
      ctx.font = fontStr(40, 'Pacifico', 400); ctx.fillStyle = '#B0122B'; ctx.textAlign = 'center';
      ctx.fillText(/advent/.test(title) ? 'Advent' : 'Christmas Eve', x + w / 2, y + 150);
    }
    designPanel(x + 80, y + (christmas ? 175 : 110), w - 160, h - (christmas ? 280 : 220), { colour: state.colour === '#FFFFFF' ? brand.ink : state.colour });
  }

  function material() {
    if (/slate/.test(title)) return 'slate';
    if (/wood|bamboo|chopping|bottle opener|jigsaw|milestone|lead hook/.test(title)) return 'wood';
    if (/acrylic|led|block|plaque|sign|stand|award|topper|place names|table numbers/.test(title)) return 'acrylic';
    if (/metal|tag|medal|power bank|charging|mirror/.test(title)) return 'metal';
    if (/golf ball/.test(title)) return 'golf';
    return 'paper';
  }

  function drawFlat() {
    background();
    const m = material();
    if (m === 'golf') {
      const cx = 500; const cy = 500; const r = 330;
      shadow(50, 24);
      const g = ctx.createRadialGradient(cx - 110, cy - 130, 40, cx, cy, r);
      g.addColorStop(0, '#fff'); g.addColorStop(1, '#D9DDE5');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); noShadow();
      ctx.fillStyle = 'rgba(0,0,0,.05)';
      for (let i = 0; i < 160; i++) { const a = i * 2.39996; const rr = Math.sqrt(i / 160) * r * 0.95; ctx.beginPath(); ctx.arc(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr, 9, 0, Math.PI * 2); ctx.fill(); }
      ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, r * 0.7, 0, Math.PI * 2); ctx.clip();
      designPanel(cx - r * 0.6, cy - r * 0.5, r * 1.2, r * 1.0, {});
      ctx.restore();
      return;
    }
    const round = /coaster|round|disc|tag|medal|heart/.test(title) && !/set of 4/.test(title);
    let x = 170; let y = 150; let w = 660; let h = 700;
    if (/door|office|house sign/.test(title)) { y = 300; h = 400; }
    if (/bookmark|bottle opener/.test(title)) { x = 380; w = 240; y = 90; h = 820; }
    if (/keyring|magnet|tag|medal/.test(title)) { x = 260; y = 230; w = 480; h = 540; }
    if (/led/.test(title)) { h = 600; y = 110; }
    shadow(50, 24);
    const fills = {
      slate: '#3A3D44', wood: '#D7A86E', acrylic: 'rgba(255,255,255,.75)', metal: '#C9CED6', paper: '#FFFFFF'
    };
    ctx.fillStyle = fills[m];
    if (round) { ctx.beginPath(); ctx.arc(500, 500, 320, 0, Math.PI * 2); ctx.fill(); x = 220; y = 220; w = 560; h = 560; }
    else { roundRect(ctx, x, y, w, h, m === 'slate' ? 6 : 22); ctx.fill(); }
    noShadow();
    // material texture
    ctx.save();
    if (round) { ctx.beginPath(); ctx.arc(500, 500, 320, 0, Math.PI * 2); } else { roundRect(ctx, x, y, w, h, 22); }
    ctx.clip();
    if (m === 'wood') {
      ctx.strokeStyle = 'rgba(120,70,20,.18)'; ctx.lineWidth = 3;
      for (let i = 0; i < 26; i++) { ctx.beginPath(); ctx.moveTo(x, y + i * 30); ctx.bezierCurveTo(x + w * 0.3, y + i * 30 + 14, x + w * 0.6, y + i * 30 - 14, x + w, y + i * 30 + 6); ctx.stroke(); }
    } else if (m === 'slate') {
      let seed = 7; // deterministic speckle so the slate doesn't shimmer while typing
      const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      for (let i = 0; i < 900; i++) { ctx.fillStyle = 'rgba(255,255,255,' + (rand() * 0.05) + ')'; ctx.fillRect(x + rand() * w, y + rand() * h, 3, 3); }
    } else if (m === 'acrylic') {
      const g = ctx.createLinearGradient(x, y, x + w, y + h);
      g.addColorStop(0, 'rgba(255,255,255,.9)'); g.addColorStop(0.5, 'rgba(220,235,255,.5)'); g.addColorStop(1, 'rgba(255,255,255,.9)');
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    } else if (m === 'metal') {
      const g = ctx.createLinearGradient(x, y, x + w, y);
      for (let i = 0; i <= 10; i++) g.addColorStop(i / 10, i % 2 ? '#E7EAF0' : '#BFC5CF');
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
    const pad = Math.min(w, h) * 0.08;
    const colour = m === 'slate' && state.colour === brand.ink ? '#FFFFFF' : state.colour;
    designPanel(x + pad, y + pad, w - pad * 2, h - pad * 2, { colour });
    ctx.restore();
    if (m === 'acrylic') { // bevel highlight
      ctx.strokeStyle = 'rgba(255,255,255,.95)'; ctx.lineWidth = 6;
      if (round) { ctx.beginPath(); ctx.arc(500, 500, 316, 0, Math.PI * 2); ctx.stroke(); } else { roundRect(ctx, x + 3, y + 3, w - 6, h - 6, 20); ctx.stroke(); }
    }
    if (/led/.test(title)) { // LED base
      shadow(30, 10); ctx.fillStyle = '#26232E'; roundRect(ctx, x - 30, y + h - 10, w + 60, 120, 18); ctx.fill(); noShadow();
      ctx.fillStyle = 'rgba(255,200,61,.35)'; ctx.fillRect(x, y + h - 30, w, 20);
    }
  }

  /* ------------------------------------------------------------------ photo proof
   * The product's real photo with a clean card listing what will be printed.
   */
  function shortLabel(label) {
    return label.replace(/\s*\((?:optional|e\.g\.?[^)]*)\)/ig, '').replace(/\s+e\.g\..*$/i, '').trim();
  }

  function drawPhotoProof() {
    // With a text zone (foxy.preview_zone), draw the customer's text straight onto the product photo,
    // e.g. the name on a stocking cuff, instead of the proof card.
    if (config.zone && state.base) { drawPhotoZone(); return; }
    const texts = state.fields.filter((f) => f.kind !== 'image');
    const filled = texts.filter((f) => f.value.trim());
    // Show what they've typed; before they start, show the first few fields as faint placeholders.
    const rows = (filled.length ? filled : texts.slice(0, 3)).slice(0, 4);
    const withPhoto = hasPhotoField();
    const rowH = rows.length > 2 ? 78 : 96;
    const cardH = rows.length || withPhoto ? Math.max(withPhoto ? 290 : 0, 74 + rows.length * rowH + 20) : 0;

    // Product photo sits above the card so the card never covers it.
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, W, H);
    const areaH = cardH ? H - cardH - 64 : H;
    if (state.base) {
      const s = Math.min(W / state.base.width, areaH / state.base.height);
      const iw = state.base.width * s;
      const ih = state.base.height * s;
      ctx.drawImage(state.base, (W - iw) / 2, (areaH - ih) / 2 + 10, iw, ih);
    } else {
      background();
    }
    if (!cardH) return;

    const pad = 34;
    const x = 50; const w = W - 100; const y = H - cardH - 34;

    ctx.save();
    shadow(40, 14);
    ctx.fillStyle = 'rgba(255,255,255,.95)';
    roundRect(ctx, x, y, w, cardH, 26); ctx.fill();
    noShadow();
    ctx.restore();

    ctx.save();
    ctx.font = fontStr(24, 'Baloo 2', 800);
    ctx.fillStyle = brand.purple;
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText('YOUR PERSONALISATION', x + pad, y + 40);
    ctx.restore();

    let tx = x + pad;
    let tw = w - pad * 2;
    if (withPhoto) {
      const ps = Math.min(cardH - 90, 230);
      photoSlot(x + pad, y + 70, ps, ps, 18);
      tx = x + pad * 2 + ps;
      tw = w - pad * 3 - ps;
    }
    rows.forEach((f, i) => {
      const ry = y + 74 + i * rowH;
      ctx.save();
      ctx.font = fontStr(20, 'Baloo 2', 700);
      ctx.fillStyle = 'rgba(29,18,64,.55)';
      ctx.textAlign = 'left'; ctx.textBaseline = 'top';
      ctx.fillText(shortLabel(f.label).toUpperCase(), tx, ry);
      ctx.restore();
      const empty = !f.value.trim();
      const value = empty ? (f.input.placeholder || f.label) : f.value.replace(/\s*\n\s*/g, ' ');
      drawFitted({ text: value, placeholder: value, empty }, tx, ry + 24 + (rowH - 30) / 2, tw, rowH - 34, { align: 'left', minSize: 18 });
    });
  }

  /* ------------------------------------------------------------------ render loop */

  // A small copy of the preview sits inside the personaliser so phone users can see it while typing.
  const mini = root.querySelector('[data-personaliser-mini]');
  const miniCtx = mini && mini.getContext('2d');

  let raf = 0;
  function draw() {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(render);
  }

  function render() {
    ctx.clearRect(0, 0, W, H);
    switch (mode) {
      case 'photo': drawPhotoProof(); break;
      case 'card': drawCard(); break;
      case 'drinkware': drawDrinkware(); break;
      case 'apparel': drawApparel(); break;
      case 'bauble': drawBauble(); break;
      case 'box': drawBox(); break;
      default: drawFlat();
    }
    if (mini) {
      miniCtx.clearRect(0, 0, mini.width, mini.height);
      miniCtx.drawImage(canvas, 0, 0, mini.width, mini.height);
    }
  }

  window.FoxyPersonaliser = { redraw: draw, state, mode };
  loadFont(state.font).then(draw);
  draw();
})();
