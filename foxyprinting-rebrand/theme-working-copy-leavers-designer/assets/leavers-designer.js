/*
 * Foxy Leavers Designer — product-page app.
 * Needs leavers-engine.js. Mount with LeaversDesigner.mount(element, config); see sections/leavers-designer.liquid.
 */
(function () {
  'use strict';
  var E = window.LeaversEngine;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function money(cents, format) {
    var amount = (cents / 100).toFixed(2);
    return (format || '£{{amount}}').replace(/\{\{\s*amount[a-z_]*\s*\}\}/, amount);
  }
  function debounce(fn, ms) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }
  function shortHash(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h >>> 0).toString(36).toUpperCase();
  }

  var SHAPE_TEMPLATES = ['year-names', 'heart', 'star'];

  function mount(root, config) {
    config = config || {};
    var productKey = config.product && E.PRODUCTS[config.product] ? config.product : E.DEFAULT_PRODUCT;
    var P = E.PRODUCTS[productKey];
    var d = E.defaultDesign(productKey);
    if (!P.areas.sleeve && d.personal.position === 'sleeve') d.personal.position = 'chest-right';

    // Size -> variant. Shopify variants come from the product JSON; the demo builds its own.
    var variants = (config.variants || []).map(function (v) {
      return { id: v.id, size: v.option1 || v.title, price: v.price, available: v.available !== false };
    });
    if (!variants.length) {
      variants = P.sizes.map(function (s, i) { return { id: 'demo-' + i, size: s, price: Math.round(E.priceFor(productKey, s) * 100), available: true }; });
    }
    var sizes = variants.map(function (v) { return v.size; });
    function variantFor(size) { for (var i = 0; i < variants.length; i++) if (variants[i].size === size) return variants[i]; return null; }

    var ui = {
      view: 'back',
      fontTarget: 'nameFont',
      fontCat: 'All',
      mode: 'single',
      size: sizes[Math.min(2, sizes.length - 1)],
      qty: 1,
      rows: [{ name: '', size: sizes[Math.min(2, sizes.length - 1)], qty: 1 }],
      logoFile: null,
      busy: false
    };

    root.classList.add('ld');
    root.innerHTML = template();
    var $ = function (sel) { return root.querySelector(sel); };
    var $$ = function (sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); };

    /* ---------------------------------------------------------------- markup */

    function template() {
      // Small round colour swatches, like Ralawise: two-tone garments show body / sleeve colour split diagonally.
      var swatches = E.colourOptions(productKey).map(function (c) {
        return '<button type="button" class="ld-gswatch" data-garment="' + c.id + '" style="--b:' + c.body + ';--t:' + c.trim + '" title="' + esc(c.name) + '" aria-label="' + esc(c.name) + '"></button>';
      }).join('');
      // Other garments in the range (Shopify passes the collection's products; the demo links to itself).
      var siblings = (!config.demo ? config.siblings || [] : Object.keys(E.PRODUCTS).map(function (k) {
        return { key: k, title: E.PRODUCTS[k].name, url: '?garment=' + k, price: Math.round(E.PRODUCTS[k].price * 100) };
      })).filter(function (sib) { return E.PRODUCTS[sib.key]; });
      var garmentPicker = siblings.length > 1 ? '<p class="ld-label">Garment</p><div class="ld-garments">' + siblings.map(function (sib) {
        var current = sib.key === productKey;
        return '<a class="ld-garment" href="' + esc(sib.url) + '"' + (current ? ' aria-current="page"' : '') + '>' +
          '<canvas width="120" height="132" data-product-thumb="' + esc(sib.key) + '"></canvas>' +
          '<strong>' + esc(E.PRODUCTS[sib.key].name) + '</strong><small>' + esc(E.PRODUCTS[sib.key].code || '') +
          (sib.price ? ' · from ' + money(sib.price, config.moneyFormat) : '') + '</small></a>';
      }).join('') + '</div>' : '';
      var templates = E.BACK_TEMPLATES.map(function (t) {
        return '<button type="button" class="ld-template" data-template="' + t.id + '"><canvas width="150" height="190" data-thumb="' + t.id + '"></canvas><strong>' + esc(t.name) + '</strong><small>' + esc(t.blurb) + '</small></button>';
      }).join('');
      var inks = function (attr) {
        return E.INKS.map(function (c) {
          return '<button type="button" class="ld-swatch ld-swatch--ink" ' + attr + '="' + c.id + '" style="--c:' + c.hex + '" title="' + esc(c.name) + '" aria-label="' + esc(c.name) + '"></button>';
        }).join('');
      };
      var cats = ['All', 'Bold', 'Varsity', 'Script', 'Fun', 'Classic'];
      var fronts = E.FRONT_STYLES.filter(function (f) { return !f.area || P.areas[f.area]; }).map(function (f) {
        return '<button type="button" class="ld-pill" data-front="' + f.id + '">' + esc(f.name) + '</button>';
      }).join('');
      var icons = Object.keys(E.ICON_NAMES).map(function (k) { return '<option value="' + k + '">' + esc(E.ICON_NAMES[k]) + '</option>'; }).join('');
      var fontOptions = E.FONTS.map(function (f) { return '<option value="' + esc(f.name) + '">' + esc(f.name) + ' (' + f.cat + ')</option>'; }).join('');
      var positions = E.PERSONAL_POSITIONS.filter(function (p) { return !p.area || P.areas[p.area]; }).map(function (p) {
        return '<button type="button" class="ld-pill" data-position="' + p.id + '">' + esc(p.name) + '</button>';
      }).join('');
      var sizePills = sizes.map(function (s) { return '<button type="button" class="ld-pill" data-size="' + esc(s) + '">' + esc(s) + '</button>'; }).join('');

      return '' +
        '<div class="ld__preview">' +
        '  <div class="ld__stage">' +
        '    <div class="ld-tabs" role="tablist">' +
        '      <button type="button" role="tab" data-view="front">Front</button>' +
        '      <button type="button" role="tab" data-view="back">Back</button>' +
        '      <button type="button" role="tab" data-view="detail">Close-up</button>' +
        '    </div>' +
        '    <canvas class="ld__canvas" data-preview role="img" aria-label="Live preview of your leavers design"></canvas>' +
        '    <div class="ld__stage-foot">' +
        '      <button type="button" class="ld-btn ld-btn--ghost" data-open-proof>🔍 See the actual print files</button>' +
        '      <span class="ld__hint">What you see is exactly what we print.</span>' +
        '    </div>' +
        '  </div>' +
        '</div>' +
        '<div class="ld__panel">' +
        '  <details class="ld-step" open><summary><span class="ld-step__n">1</span> Garment &amp; colour <em data-garment-name></em></summary>' +
        garmentPicker +
        '    <p class="ld-label">' + esc(P.name) + ' colour' + (P.colourways ? ' (body / sleeves)' : '') + ' — ' + E.colourOptions(productKey).length + ' options</p>' +
        '    <div class="ld-gswatches">' + swatches + '</div>' +
        '    <p class="ld-colour-name">Colour: <strong data-colour-name></strong></p>' +
        '  </details>' +
        '  <details class="ld-step" open><summary><span class="ld-step__n">2</span> Back design</summary>' +
        '    <div class="ld-templates">' + templates + '</div>' +
        '  </details>' +
        '  <details class="ld-step" open><summary><span class="ld-step__n">3</span> Wording &amp; names</summary>' +
        '    <div class="ld-grid3">' +
        '      <label class="ld-field"><span>Heading</span><input type="text" maxlength="24" data-bind="back.title"></label>' +
        '      <label class="ld-field"><span>Year</span><input type="text" maxlength="6" data-bind="back.year" placeholder="26 or 2026"></label>' +
        '    </div>' +
        '    <label class="ld-field"><span>School name (in full)</span><input type="text" maxlength="80" data-bind="back.school" placeholder="e.g. Oakfield Primary School"></label>' +
        '    <div class="ld-field" data-names-field><span>Names for the back — one box per pupil <b data-name-count></b></span>' +
        '      <div class="ld-names" data-name-list></div>' +
        '      <div class="ld-row ld-row--wrap"><button type="button" class="ld-chip" data-name-add>+ Add a name</button>' +
        '        <button type="button" class="ld-chip" data-names-paste-toggle hidden>Paste a whole list</button></div>' +
        '      <label class="ld-field" data-names-paste><span>All pupils’ names in full — type or paste one name per line</span><textarea rows="10" data-names spellcheck="false" placeholder="Olivia Smith&#10;Jack Taylor&#10;Amelia-Rose Johnson&#10;…"></textarea>' +
        '        <p class="ld-note">The name boxes above update as you go. Please check every spelling: we print exactly what you type.</p></label>' +
        '    </div>' +
        '    <div class="ld-row ld-row--wrap" data-names-tools>' +
        '      <button type="button" class="ld-chip" data-names-action="sort">Sort A–Z</button>' +
        '      <button type="button" class="ld-chip" data-names-action="dedupe">Remove duplicates</button>' +
        '      <button type="button" class="ld-chip" data-names-action="first">First names only</button>' +
        '      <button type="button" class="ld-chip" data-names-action="sample">Sample names</button>' +
        '      <button type="button" class="ld-chip" data-names-action="clear">Clear</button>' +
        '      <select class="ld-select" data-bind="back.nameCase" aria-label="Name style"><option value="upper">UPPERCASE</option><option value="title">Title Case</option><option value="asis">As typed</option></select>' +
        '    </div>' +
        '    <div class="ld-row ld-row--wrap">' +
        '      <label class="ld-check" data-repeat-opt><input type="checkbox" data-bind="back.repeat"> Repeat names to fill the shape</label>' +
        '      <label class="ld-check"><input type="checkbox" data-bind="back.twoTone"> Two-tone names</label>' +
        '      <label class="ld-check"><input type="checkbox" data-bind="back.outline"> Outline</label>' +
        '    </div>' +
        '  </details>' +
        '  <details class="ld-step" open><summary><span class="ld-step__n">4</span> Fonts &amp; print colours</summary>' +
        '    <div class="ld-seg" role="group" aria-label="Which text">' +
        '      <button type="button" data-font-target="nameFont">Names font</button>' +
        '      <button type="button" data-font-target="displayFont">Heading &amp; year font</button>' +
        '    </div>' +
        '    <div class="ld-row ld-row--wrap ld-cats">' + cats.map(function (c) { return '<button type="button" class="ld-chip" data-font-cat="' + c + '">' + c + '</button>'; }).join('') + '</div>' +
        '    <div class="ld-fonts" data-fonts></div>' +
        '    <p class="ld-label">Main print colour <span data-ink-name></span></p><div class="ld-swatches">' + inks('data-ink') + '</div>' +
        '    <p class="ld-label">Highlight colour <span data-accent-name></span></p><div class="ld-swatches">' + inks('data-accent') + '</div>' +
        '    <p class="ld-note" data-contrast-warning hidden>⚠️ That print colour is hard to see on this garment — try a lighter or darker one.</p>' +
        '  </details>' +
        '  <details class="ld-step"><summary><span class="ld-step__n">5</span> Front design</summary>' +
        '    <div class="ld-row ld-row--wrap">' + fronts + '</div>' +
        '    <div class="ld-grid3" data-front-fields>' +
        '      <label class="ld-field" data-front-line1><span>Main text</span><input type="text" maxlength="30" data-bind="front.line1"></label>' +
        '      <label class="ld-field" data-front-line2><span>Script text</span><input type="text" maxlength="24" data-bind="front.line2"></label>' +
        '      <label class="ld-field" data-front-icon><span>Icon</span><select class="ld-select" data-bind="front.icon">' + icons + '</select></label>' +
        '      <label class="ld-field" data-front-font><span>Font</span><select class="ld-select" data-bind="front.font">' + fontOptions + '</select></label>' +
        '    </div>' +
        '    <label class="ld-field ld-upload" data-front-logo><span>Upload your school logo (PNG with a clear background works best)</span>' +
        '      <input type="file" accept="image/png,image/jpeg,image/svg+xml,image/webp" data-logo></label>' +
        '  </details>' +
        '  <details class="ld-step"><summary><span class="ld-step__n">6</span> Personal name or nickname</summary>' +
        '    <div class="ld-row ld-row--wrap">' + positions + '</div>' +
        '    <div class="ld-grid3" data-personal-fields>' +
        '      <label class="ld-field" data-personal-single><span>Name or nickname</span><input type="text" maxlength="20" data-bind="personal.text" placeholder="e.g. SMITHY"></label>' +
        '      <label class="ld-field"><span>Font</span><select class="ld-select" data-bind="personal.font">' + fontOptions + '</select></label>' +
        '    </div>' +
        '    <p class="ld-note" data-personal-group-note hidden>Ordering for a group? Add each person\'s name in step 7.</p>' +
        '  </details>' +
        '  <details class="ld-step" open><summary><span class="ld-step__n">7</span> Sizes &amp; order</summary>' +
        '    <div class="ld-seg" role="group" aria-label="Order type">' +
        '      <button type="button" data-mode="single">Just me</button>' +
        '      <button type="button" data-mode="group">Whole group</button>' +
        '    </div>' +
        '    <div data-single>' +
        '      <p class="ld-label">Size</p><div class="ld-row ld-row--wrap">' + sizePills + '</div>' +
        '      <div class="ld-row"><span class="ld-label">Quantity</span><div class="ld-qty"><button type="button" data-qty="-1" aria-label="Fewer">−</button><input type="number" min="1" value="1" data-qty-input aria-label="Quantity"><button type="button" data-qty="1" aria-label="More">+</button></div></div>' +
        '    </div>' +
        '    <div data-group hidden>' +
        '      <p class="ld-note">One line per hoodie. Everyone gets the same back; each person\'s own name goes where you chose in step 6.</p>' +
        '      <div class="ld-table" data-rows></div>' +
        '      <div class="ld-row ld-row--wrap"><button type="button" class="ld-chip" data-add-row>+ Add person</button><button type="button" class="ld-chip" data-toggle-paste>Paste a list</button><button type="button" class="ld-chip" data-rows-from-names>Use names from the back</button></div>' +
        '      <div data-paste hidden><label class="ld-field"><span>Paste lines like <code>Smithy, M</code> or <code>Olivia Smith, 9-11 yrs</code></span><textarea rows="5" data-paste-text></textarea></label><button type="button" class="ld-btn ld-btn--ghost" data-paste-apply>Add these people</button></div>' +
        '    </div>' +
        '    <div class="ld-total"><span data-total-label>Total</span><strong data-total></strong></div>' +
        '    <label class="ld-check ld-confirm"><input type="checkbox" data-confirm> I\'ve checked every name, the spelling and the preview — print it exactly as shown.</label>' +
        '    <button type="button" class="ld-btn ld-btn--primary" data-add>Add to basket</button>' +
        '    <p class="ld-msg" data-msg role="status" aria-live="polite"></p>' +
        '  </details>' +
        '</div>' +
        '<dialog class="ld-proof" data-proof aria-labelledby="ld-proof-title">' +
        '  <div class="ld-proof__head"><h2 id="ld-proof-title">Your print files</h2><button type="button" class="ld-proof__close" data-close-proof aria-label="Close">✕</button></div>' +
        '  <p class="ld-note">These are the artwork files our printer receives, printed at 300 dpi at the sizes shown (displayed here on your garment colour).</p>' +
        '  <div class="ld-proof__files" data-proof-files></div>' +
        '  <div class="ld-row ld-row--wrap"><button type="button" class="ld-btn ld-btn--ghost" data-download-proof>Download a proof to share</button></div>' +
        '</dialog>';
    }

    /* ---------------------------------------------------------------- binding */

    function getPath(path) { return path.split('.').reduce(function (o, k) { return o[k]; }, d); }
    function setPath(path, v) {
      var parts = path.split('.'), last = parts.pop();
      parts.reduce(function (o, k) { return o[k]; }, d)[last] = v;
    }

    $$('[data-bind]').forEach(function (el) {
      var path = el.getAttribute('data-bind');
      var ev = el.type === 'checkbox' || el.tagName === 'SELECT' ? 'change' : 'input';
      el.addEventListener(ev, function () {
        setPath(path, el.type === 'checkbox' ? el.checked : el.value);
        if (path === 'back.nameCase' || path === 'back.repeat') thumbsSoon();
        if (/font/.test(path)) E.loadFonts(d).then(refresh);
        refresh();
      });
    });

    var namesBox = $('[data-names]');
    var nameList = $('[data-name-list]');
    namesBox.value = d.back.names.join('\n');

    function namesChanged() {
      refresh(); thumbsSoon();
    }
    // One text box per pupil, plus an empty box at the end for the next name.
    function renderNameList(focusIndex) {
      nameList.innerHTML = d.back.names.map(function (n, i) {
        return '<div class="ld-name"><span class="ld-name__n">' + (i + 1) + '</span>' +
          '<input type="text" maxlength="40" value="' + esc(n) + '" data-name-i="' + i + '" aria-label="Name ' + (i + 1) + '" spellcheck="false">' +
          '<button type="button" data-name-del="' + i + '" aria-label="Remove ' + esc(n || 'name') + '">✕</button></div>';
      }).join('') +
        '<div class="ld-name ld-name--new"><span class="ld-name__n">' + (d.back.names.length + 1) + '</span>' +
        '<input type="text" maxlength="40" data-name-new placeholder="Type a name and press Enter" aria-label="Add a name" spellcheck="false"></div>';
      if (focusIndex != null) {
        var el = focusIndex >= d.back.names.length ? nameList.querySelector('[data-name-new]') : nameList.querySelector('[data-name-i="' + focusIndex + '"]');
        if (el) el.focus();
      }
    }
    function addNewName(input) {
      var v = input.value.trim();
      if (!v) return false;
      input.value = '';
      d.back.names.push(v);
      namesBox.value = d.back.names.join('\n');
      renderNameList(d.back.names.length);
      namesChanged();
      return true;
    }
    nameList.addEventListener('input', function (e) {
      var i = e.target.getAttribute('data-name-i');
      if (i == null) return;
      d.back.names[+i] = e.target.value;
      namesBox.value = d.back.names.join('\n');
      $('[data-name-count]').textContent = '(' + E.cleanNames(d).length + ')';
      namesChanged();
    });
    nameList.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      e.preventDefault();
      if (e.target.hasAttribute('data-name-new')) { addNewName(e.target); return; }
      var i = +e.target.getAttribute('data-name-i');
      var next = nameList.querySelector('[data-name-i="' + (i + 1) + '"]') || nameList.querySelector('[data-name-new]');
      if (next) next.focus();
    });
    nameList.addEventListener('focusout', function (e) {
      if (e.target.hasAttribute('data-name-new')) { if (addNewName(e.target)) return; }
      if (e.target.hasAttribute('data-name-i') && !e.target.value.trim()) {
        d.back.names.splice(+e.target.getAttribute('data-name-i'), 1);
        namesBox.value = d.back.names.join('\n');
        setTimeout(function () { renderNameList(); namesChanged(); });
      }
    });
    nameList.addEventListener('click', function (e) {
      var del = e.target.getAttribute('data-name-del');
      if (del == null) return;
      d.back.names.splice(+del, 1);
      namesBox.value = d.back.names.join('\n');
      renderNameList();
      namesChanged();
    });
    $('[data-name-add]').addEventListener('click', function () {
      var input = nameList.querySelector('[data-name-new]');
      if (input) { input.focus(); input.scrollIntoView({ block: 'nearest' }); }
    });
    $('[data-names-paste-toggle]').addEventListener('click', function () {
      var box = $('[data-names-paste]');
      box.hidden = !box.hidden;
      if (!box.hidden) namesBox.focus();
    });
    namesBox.addEventListener('input', function () {
      d.back.names = namesBox.value.split(/\n/).map(function (s) { return s.trim(); }).filter(Boolean);
      renderNameList();
      namesChanged();
    });
    $$('[data-names-action]').forEach(function (b) {
      b.addEventListener('click', function () {
        var act = b.getAttribute('data-names-action'), list = d.back.names;
        if (act === 'sort') list = list.slice().sort(function (a, b2) { return a.localeCompare(b2, 'en', { sensitivity: 'base' }); });
        if (act === 'dedupe') list = list.filter(function (n, i) { return list.map(function (x) { return x.toLowerCase(); }).indexOf(n.toLowerCase()) === i; });
        if (act === 'first') list = list.map(function (n) { return n.split(' ')[0]; });
        if (act === 'sample') list = E.SAMPLE_NAMES.slice();
        if (act === 'clear') list = [];
        d.back.names = list;
        namesBox.value = list.join('\n');
        renderNameList();
        refresh(); thumbsSoon();
      });
    });

    function clickGroup(attr, fn) {
      $$('[' + attr + ']').forEach(function (b) {
        b.addEventListener('click', function () { fn(b.getAttribute(attr), b); refresh(); });
      });
    }
    clickGroup('data-garment', function (id) {
      d.garment = id;
      // Keep the print readable when switching between dark and light garments.
      var bg = E.bodyHex(d);
      if (E.contrastRatio(E.inkHex(d.back.ink), bg) < 2) d.back.ink = E.contrastRatio('#FFFFFF', bg) > E.contrastRatio('#141414', bg) ? 'white' : 'black';
      thumbsSoon();
    });
    clickGroup('data-template', function (id) { d.back.template = id; ui.view = 'back'; });
    clickGroup('data-ink', function (id) { d.back.ink = id; thumbsSoon(); });
    clickGroup('data-accent', function (id) { d.back.accent = id; thumbsSoon(); });
    clickGroup('data-front', function (id) {
      d.front.style = id;
      ui.view = 'front';
      if (/^centre/.test(id) && d.personal.position === 'chest-right') d.personal.position = P.areas.sleeve ? 'sleeve' : 'back-top';
    });
    clickGroup('data-position', function (id) { d.personal.position = id; ui.view = id === 'back-top' ? 'back' : 'front'; });
    clickGroup('data-view', function (v) { ui.view = v; });
    clickGroup('data-font-target', function (t) { ui.fontTarget = t; renderFonts(); });
    clickGroup('data-font-cat', function (c) { ui.fontCat = c; renderFonts(); });
    clickGroup('data-mode', function (m) { ui.mode = m; });
    clickGroup('data-size', function (s) { ui.size = s; d.size = s; });

    $('[data-qty-input]').addEventListener('input', function (e) { ui.qty = Math.max(1, parseInt(e.target.value, 10) || 1); refresh(); });
    $$('[data-qty]').forEach(function (b) {
      b.addEventListener('click', function () {
        ui.qty = Math.max(1, ui.qty + parseInt(b.getAttribute('data-qty'), 10));
        $('[data-qty-input]').value = ui.qty; refresh();
      });
    });

    $('[data-logo]').addEventListener('change', function (e) {
      var file = e.target.files && e.target.files[0];
      ui.logoFile = file || null;
      d._logoSrc = file ? URL.createObjectURL(file) : '';
      E.loadLogo(d).then(refresh);
    });

    /* ---------------------------------------------------------------- fonts grid */

    function renderFonts() {
      var current = d.back[ui.fontTarget];
      var sample = ui.fontTarget === 'nameFont' ? (E.cleanNames(d)[0] || 'OLIVIA SMITH') : (d.back.title || 'LEAVERS') + ' ' + (d.back.year || '');
      $('[data-fonts]').innerHTML = E.FONTS.filter(function (f) { return ui.fontCat === 'All' || f.cat === ui.fontCat; }).map(function (f) {
        return '<button type="button" class="ld-font" data-font="' + esc(f.name) + '" aria-pressed="' + (f.name === current) + '">' +
          '<span style="font-family:\'' + esc(f.name) + '\';font-weight:' + f.weight + '">' + esc(sample) + '</span><small>' + esc(f.name) + '</small></button>';
      }).join('');
      $$('[data-font-target]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-font-target') === ui.fontTarget)); });
      $$('[data-font-cat]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-font-cat') === ui.fontCat)); });
    }
    $('[data-fonts]').addEventListener('click', function (e) {
      var b = e.target.closest('[data-font]');
      if (!b) return;
      d.back[ui.fontTarget] = b.getAttribute('data-font');
      E.loadFonts(d).then(function () { refresh(); thumbsSoon(); });
      renderFonts();
    });

    /* ---------------------------------------------------------------- group rows */

    function renderRows() {
      var opts = function (sel) { return sizes.map(function (s) { return '<option' + (s === sel ? ' selected' : '') + '>' + esc(s) + '</option>'; }).join(''); };
      var showName = d.personal.position !== 'none';
      $('[data-rows]').innerHTML = '<div class="ld-table__head"><span>' + (showName ? 'Name / nickname' : 'Who it\'s for (not printed)') + '</span><span>Size</span><span>Qty</span><span></span></div>' +
        ui.rows.map(function (r, i) {
          return '<div class="ld-table__row" data-row="' + i + '">' +
            '<input type="text" maxlength="20" value="' + esc(r.name) + '" data-row-name aria-label="Name for hoodie ' + (i + 1) + '">' +
            '<select data-row-size aria-label="Size for hoodie ' + (i + 1) + '">' + opts(r.size) + '</select>' +
            '<input type="number" min="1" value="' + r.qty + '" data-row-qty aria-label="Quantity for hoodie ' + (i + 1) + '">' +
            '<button type="button" data-row-remove aria-label="Remove hoodie ' + (i + 1) + '">✕</button></div>';
        }).join('');
    }
    $('[data-rows]').addEventListener('input', function (e) {
      var row = e.target.closest('[data-row]');
      if (!row) return;
      var r = ui.rows[+row.getAttribute('data-row')];
      if (e.target.matches('[data-row-name]')) r.name = e.target.value;
      if (e.target.matches('[data-row-size]')) r.size = e.target.value;
      if (e.target.matches('[data-row-qty]')) r.qty = Math.max(1, parseInt(e.target.value, 10) || 1);
      if (e.target.matches('[data-row-name]') && +row.getAttribute('data-row') === 0) { d.personal.text = r.name; draw(); }
      updateTotal();
    });
    $('[data-rows]').addEventListener('change', function (e) {
      if (e.target.matches('[data-row-size]')) { ui.rows[+e.target.closest('[data-row]').getAttribute('data-row')].size = e.target.value; updateTotal(); }
    });
    $('[data-rows]').addEventListener('click', function (e) {
      if (!e.target.matches('[data-row-remove]')) return;
      ui.rows.splice(+e.target.closest('[data-row]').getAttribute('data-row'), 1);
      if (!ui.rows.length) ui.rows.push({ name: '', size: ui.size, qty: 1 });
      renderRows(); updateTotal();
    });
    $('[data-add-row]').addEventListener('click', function () {
      ui.rows.push({ name: '', size: ui.rows[ui.rows.length - 1].size, qty: 1 }); renderRows(); updateTotal();
      var inputs = $$('[data-row-name]'); inputs[inputs.length - 1].focus();
    });
    $('[data-toggle-paste]').addEventListener('click', function () { $('[data-paste]').hidden = !$('[data-paste]').hidden; });
    function matchSize(s) {
      s = String(s || '').trim().toLowerCase().replace(/\s+/g, ' ');
      s = { 'xxl': '2xl', 'xxxl': '3xl', 'small': 's', 'medium': 'm', 'large': 'l', 'extra large': 'xl', 'x-large': 'xl', 'xs/s': 'xs' }[s] || s;
      for (var i = 0; i < sizes.length; i++) if (sizes[i].toLowerCase() === s) return sizes[i];
      for (i = 0; i < sizes.length; i++) if (sizes[i].toLowerCase().replace(/[^a-z0-9]/g, '').indexOf(s.replace(/[^a-z0-9]/g, '')) === 0 && s) return sizes[i];
      return null;
    }
    $('[data-paste-apply]').addEventListener('click', function () {
      var lines = $('[data-paste-text]').value.split(/\n/).map(function (l) { return l.trim(); }).filter(Boolean);
      var added = lines.map(function (l) {
        var parts = l.split(/[,\t;]/);
        var size = parts.length > 1 ? matchSize(parts[parts.length - 1]) : null;
        var name = (size ? parts.slice(0, -1).join(',') : l).trim();
        return { name: name, size: size || ui.rows[0].size, qty: 1, guessed: !size };
      });
      ui.rows = ui.rows.filter(function (r) { return r.name; }).concat(added);
      if (!ui.rows.length) ui.rows.push({ name: '', size: ui.size, qty: 1 });
      renderRows(); updateTotal();
      var guessed = added.filter(function (r) { return r.guessed; }).length;
      msg(added.length + ' people added.' + (guessed ? ' ' + guessed + ' had no size we recognised — please check their sizes.' : ''));
      $('[data-paste-text]').value = '';
      $('[data-paste]').hidden = true;
    });
    $('[data-rows-from-names]').addEventListener('click', function () {
      ui.rows = d.back.names.map(function (n) { return { name: n, size: ui.rows[0].size, qty: 1 }; });
      if (!ui.rows.length) ui.rows.push({ name: '', size: ui.size, qty: 1 });
      renderRows(); updateTotal();
      msg('Added a line for everyone on the back — now pick each person\'s size.');
    });

    /* ---------------------------------------------------------------- drawing */

    var canvas = $('[data-preview]');
    var drawQueued = false;
    function draw() {
      if (drawQueued) return;
      drawQueued = true;
      requestAnimationFrame(function () {
        drawQueued = false;
        var w = Math.round(Math.min(canvas.clientWidth || 600, 900) * Math.min(window.devicePixelRatio || 1, 2));
        if (canvas.width !== w) { canvas.width = w; canvas.height = Math.round(w * 1.1); }
        E.renderMockup(canvas, d, ui.view, { background: '#F6F2EE' });
      });
    }

    function drawGarmentThumbs() {
      $$('canvas[data-garment-thumb]').forEach(function (c) {
        E.renderMockup(c, { product: productKey, garment: c.getAttribute('data-garment-thumb') }, 'front', { blank: true });
      });
      $$('[data-product-thumb]').forEach(function (c) {
        var key = c.getAttribute('data-product-thumb');
        var td = JSON.parse(JSON.stringify(d));
        td.product = key;
        if (key !== productKey) td.garment = E.defaultColour(key);
        E.renderMockup(c, td, 'back', { quality: 1 });
      });
    }

    var thumbsSoon = debounce(function () {
      drawGarmentThumbs();
      $$('[data-thumb]').forEach(function (c) {
        var t = c.getAttribute('data-thumb');
        var td = JSON.parse(JSON.stringify(d));
        td.back.template = t;
        var ctx = c.getContext('2d');
        ctx.fillStyle = E.bodyHex(d);
        ctx.fillRect(0, 0, c.width, c.height);
        var a = E.areaCanvas(td, 'back', c.width * 0.86);
        var h = a.height * (c.width * 0.86) / a.width;
        ctx.drawImage(a, c.width * 0.07, (c.height - h) / 2, c.width * 0.86, h);
      });
    }, 350);

    function msg(text, isError) {
      var el = $('[data-msg]');
      el.textContent = text || '';
      el.classList.toggle('ld-msg--error', !!isError);
    }

    function orderItems() {
      if (ui.mode === 'single') return [{ name: d.personal.text || '', size: ui.size, qty: ui.qty }];
      return ui.rows;
    }
    function updateTotal() {
      var items = orderItems(), total = 0, count = 0;
      items.forEach(function (r) { var v = variantFor(r.size); if (v) total += v.price * r.qty; count += r.qty; });
      $('[data-total]').textContent = money(total, config.moneyFormat);
      $('[data-total-label]').textContent = 'Total for ' + count + ' ' + (count === 1 ? 'item' : 'items');
      $('[data-add]').textContent = ui.mode === 'group' ? 'Add ' + count + ' to basket' : 'Add to basket';
    }

    function refresh() {
      var t = E.byId(E.BACK_TEMPLATES, d.back.template);
      $$('[data-garment]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-garment') === d.garment)); });
      $$('[data-template]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-template') === d.back.template)); });
      $$('[data-ink]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-ink') === d.back.ink)); });
      $$('[data-accent]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-accent') === d.back.accent)); });
      $$('[data-front]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-front') === d.front.style)); });
      $$('[data-position]').forEach(function (b) {
        var id = b.getAttribute('data-position');
        b.setAttribute('aria-pressed', String(id === d.personal.position));
        b.disabled = id === 'chest-right' && /^centre/.test(d.front.style);
      });
      $$('[data-view]').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-view') === ui.view)); });
      $$('[data-mode]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-mode') === ui.mode)); });
      $$('[data-size]').forEach(function (b) {
        var v = variantFor(b.getAttribute('data-size'));
        b.setAttribute('aria-pressed', String(b.getAttribute('data-size') === ui.size));
        b.disabled = !v || !v.available;
      });
      $('[data-garment-name]').textContent = P.name + ' · ' + E.colourOf(d).name;
      $('[data-colour-name]').textContent = E.colourOf(d).name;
      $('[data-ink-name]').textContent = '— ' + E.byId(E.INKS, d.back.ink).name;
      $('[data-accent-name]').textContent = '— ' + E.byId(E.INKS, d.back.accent).name;
      $('[data-contrast-warning]').hidden = E.contrastRatio(E.inkHex(d.back.ink), E.bodyHex(d)) >= 1.6;
      $('[data-name-count]').textContent = '(' + E.cleanNames(d).length + ')';
      $('[data-names-field]').hidden = !t.names;
      $('[data-names-tools]').hidden = !t.names;
      $('[data-repeat-opt]').hidden = SHAPE_TEMPLATES.indexOf(d.back.template) < 0;

      $$('[data-bind]').forEach(function (el) {
        if (el === document.activeElement) return;
        var v = getPath(el.getAttribute('data-bind'));
        if (el.type === 'checkbox') el.checked = !!v; else el.value = v == null ? '' : v;
      });
      var fs = d.front.style;
      $('[data-front-fields]').hidden = fs === 'none';
      $('[data-front-line2]').hidden = fs === 'chest-logo' || fs === 'chest-letter';
      $('[data-front-line1] span').textContent = fs === 'chest-letter' ? 'Letter(s) — 1 or 2' : 'Main text';
      $('[data-front-icon]').hidden = fs !== 'chest-text';
      $('[data-front-logo]').hidden = fs !== 'chest-logo';
      $('[data-personal-fields]').hidden = d.personal.position === 'none';
      $('[data-personal-single]').hidden = ui.mode === 'group';
      $('[data-personal-group-note]').hidden = ui.mode !== 'group' || d.personal.position === 'none';
      $('[data-single]').hidden = ui.mode !== 'single';
      $('[data-group]').hidden = ui.mode !== 'group';
      updateTotal();
      draw();
    }

    /* ---------------------------------------------------------------- proof */

    var proof = $('[data-proof]');
    $('[data-open-proof]').addEventListener('click', function () {
      var files = $('[data-proof-files]');
      files.innerHTML = '';
      E.printAreas(d, true).forEach(function (a) {
        var art = E.areaCanvas(d, a.key, Math.min(560, a.mm.w * 2.2));
        var c = document.createElement('canvas');
        c.width = art.width; c.height = art.height;
        var cx = c.getContext('2d');
        cx.fillStyle = E.bodyHex(d); cx.fillRect(0, 0, c.width, c.height);
        cx.drawImage(art, 0, 0);
        var fig = document.createElement('figure');
        fig.className = 'ld-proof__file';
        fig.appendChild(c);
        var cap = document.createElement('figcaption');
        var px = Math.round(a.mm.w / 25.4 * 300) + ' × ' + Math.round(a.mm.h / 25.4 * 300) + ' px';
        cap.innerHTML = '<strong>' + esc(a.label) + '</strong> ' + a.mm.w + ' × ' + a.mm.h + ' mm · ' + px + ' @ 300 dpi';
        fig.appendChild(cap);
        files.appendChild(fig);
      });
      if (proof.showModal) proof.showModal(); else proof.setAttribute('open', '');
    });
    $('[data-close-proof]').addEventListener('click', function () { proof.close ? proof.close() : proof.removeAttribute('open'); });
    proof.addEventListener('click', function (e) { if (e.target === proof && proof.close) proof.close(); });
    $('[data-download-proof]').addEventListener('click', function () {
      var out = document.createElement('canvas');
      out.width = 2000; out.height = 1240;
      var ctx = out.getContext('2d');
      ctx.fillStyle = '#F6F2EE'; ctx.fillRect(0, 0, 2000, 1240);
      ['front', 'back'].forEach(function (v, i) {
        var c = document.createElement('canvas'); c.width = 1000; c.height = 1100;
        E.renderMockup(c, d, v);
        ctx.drawImage(c, i * 1000, 20);
      });
      ctx.fillStyle = '#1D1240';
      ctx.font = '600 34px sans-serif';
      ctx.fillText(P.name + ' · ' + E.colourOf(d).name + ' · ' + E.byId(E.BACK_TEMPLATES, d.back.template).name + ' · PROOF', 40, 1200);
      out.toBlob(function (b) {
        var a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = 'leavers-hoodie-proof.png';
        document.body.appendChild(a); a.click(); a.remove();
      });
    });

    /* ---------------------------------------------------------------- basket */

    function properties(design, code) {
      var t = E.byId(E.BACK_TEMPLATES, design.back.template);
      var fs = E.byId(E.FRONT_STYLES, design.front.style);
      var pos = E.byId(E.PERSONAL_POSITIONS, design.personal.position);
      var front = fs.name;
      if (fs.id === 'chest-text' || /^centre/.test(fs.id)) front += ': ' + [design.front.line1, design.front.line2].filter(Boolean).join(' / ');
      if (fs.id === 'chest-letter') front += ': ' + (design.front.line1 || 'L').trim().slice(0, 2).toUpperCase();
      if (fs.id === 'chest-logo') front += design.front.line1 ? ' + "' + design.front.line1 + '"' : '';
      var props = {
        'Garment': P.name + (P.code ? ' (' + P.code + ')' : ''),
        'Colour': E.colourOf(design).name,
        'Back design': t.name,
        'Back wording': [design.back.title, design.back.year, design.back.school].filter(Boolean).join(' · '),
        'Names on back': t.names ? E.cleanNames(design).length + ' names' : 'None',
        'Fonts': design.back.nameFont + ' / ' + design.back.displayFont,
        'Print colours': E.byId(E.INKS, design.back.ink).name + ' + ' + E.byId(E.INKS, design.back.accent).name,
        'Front': front,
        'Personal name': (design.personal.text || '').trim() && pos.id !== 'none' ? design.personal.text.trim() + ' (' + pos.name.toLowerCase() + ')' : 'None',
        '_Print files': (config.studioUrl || '/pages/leavers-print-studio') + '#d=' + code,
        '_Group design': shortHash(JSON.stringify([design.product, design.garment, design.back, design.front.style, design.front.line1, design.front.line2]))
      };
      return props;
    }

    function validate(items) {
      var t = E.byId(E.BACK_TEMPLATES, d.back.template);
      if (t.names && !E.cleanNames(d).length) return 'Add at least one name for the back, or choose the "Year Only" design.';
      if (d.front.style === 'chest-logo' && !ui.logoFile && !d.front.logoUrl) return 'Please upload your school logo, or pick a different front design.';
      for (var i = 0; i < items.length; i++) {
        var v = variantFor(items[i].size);
        if (!v || !v.available) return 'Size ' + items[i].size + ' isn\'t available — please choose another.';
      }
      if (ui.mode === 'group' && d.personal.position !== 'none') {
        var missing = items.filter(function (r) { return !String(r.name).trim(); }).length;
        if (missing) return missing + ' line' + (missing > 1 ? 's have' : ' has') + ' no name. Add a name, or choose "No personal name" in step 6.';
      }
      if (!$('[data-confirm]').checked) return 'Please tick the box to confirm you\'ve checked the design.';
      return null;
    }

    function postJSON(url, body) {
      return fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(body)
      }).then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.description || j.message || 'Could not add to basket'); return j; }); });
    }

    function designFor(item) {
      var copy = JSON.parse(JSON.stringify(d));
      copy.personal.text = d.personal.position === 'none' ? '' : String(item.name || '').trim();
      copy.size = item.size;
      return copy;
    }

    function buildLines(items) {
      return Promise.all(items.map(function (item) {
        var design = designFor(item);
        return E.encode(design).then(function (code) {
          return { id: variantFor(item.size).id, quantity: item.qty, properties: properties(design, code) };
        });
      }));
    }

    $('[data-add]').addEventListener('click', function () {
      if (ui.busy) return;
      var items = orderItems();
      var problem = validate(items);
      if (problem) { msg(problem, true); return; }
      ui.busy = true;
      var btn = $('[data-add]');
      btn.disabled = true;
      msg('Saving your design…');

      var logoStep = Promise.resolve();
      // A new logo goes up with the first hoodie (Shopify stores the file); every line then points at that copy.
      if (d.front.style === 'chest-logo' && ui.logoFile && !config.demo) {
        logoStep = buildLines([items[0]]).then(function (lines) {
          var fd = new FormData();
          fd.append('id', lines[0].id);
          fd.append('quantity', '1');
          Object.keys(lines[0].properties).forEach(function (k) { fd.append('properties[' + k + ']', lines[0].properties[k]); });
          fd.append('properties[_Logo]', ui.logoFile);
          return fetch(config.cartAddUrl || '/cart/add.js', { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
            .then(function (r) { return r.json(); })
            .then(function (line) {
              var url = line.properties && line.properties._Logo;
              if (!url) throw new Error('Your logo didn\'t upload — please try a PNG or JPG under 20 MB.');
              d.front.logoUrl = url;
              // Swap the placeholder line for the real one (now carrying the uploaded logo).
              return postJSON(config.cartChangeUrl || '/cart/change.js', { id: line.key, quantity: 0 });
            });
        });
      }

      logoStep
        .then(function () { return buildLines(items); })
        .then(function (lines) {
          if (config.demo) {
            if (typeof config.onDemoOrder === 'function') config.onDemoOrder(lines, d);
            msg('Demo: ' + lines.length + ' basket line' + (lines.length > 1 ? 's' : '') + ' created — see below.');
            return;
          }
          return postJSON(config.cartAddUrl || '/cart/add.js', { items: lines }).then(function () {
            msg('Added! Taking you to your basket…');
            window.location.href = config.cartUrl || '/cart';
          });
        })
        .catch(function (err) { msg(err.message || 'Something went wrong — please try again.', true); })
        .then(function () { ui.busy = false; btn.disabled = false; });
    });

    /* ---------------------------------------------------------------- start */

    d.size = ui.size;
    renderNameList();
    renderFonts();
    renderRows();
    window.addEventListener('leavers:photo', debounce(function () { draw(); drawGarmentThumbs(); }, 60));
    refresh();
    thumbsSoon();
    E.loadFonts(d, true).then(function () { refresh(); thumbsSoon(); renderFonts(); });
    if (window.ResizeObserver) new ResizeObserver(draw).observe(canvas);
    if (document.fonts && document.fonts.addEventListener) {
      document.fonts.addEventListener('loadingdone', debounce(function () { refresh(); thumbsSoon(); }, 150));
    }

    return { design: d, refresh: refresh, ui: ui };
  }

  window.LeaversDesigner = { mount: mount };

  function autoMount() {
    document.querySelectorAll('[data-leavers-designer]').forEach(function (el) {
      if (el.__ld) return;
      var cfgEl = el.querySelector('script[type="application/json"]');
      var cfg = cfgEl ? JSON.parse(cfgEl.textContent) : {};
      el.__ld = mount(el, cfg);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', autoMount); else autoMount();
})();
