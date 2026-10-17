/* Foxy Printing – Word Art Designer (no dependencies).
 *
 * Fills the product's own artwork shape with the customer's words, like wordart.com, and attaches a
 * print-ready PNG of the design to the basket line, so the order arrives with its print file.
 *
 *   Shape:   an RGBA mask image (product.metafields.foxy.word_art_mask, made by tools/word_art_designer/
 *            make_masks.py): alpha = the shape, RGB = the artwork's own colours. Without one, the shape is
 *            worked out from a flat artwork image or the customer's uploaded picture (non-white / opaque area).
 *   Layout:  a word cloud on an occupancy grid. The name goes in once, as big as it fits; the other words
 *            repeat, largest first and smaller each round, at 0° or 90°, until the shape is full. A seeded
 *            random generator makes every layout repeatable from its Layout code.
 *   Print:   the same placements are redrawn as text at print resolution (not an upscaled preview) for the
 *            chosen A size, with 3 mm bleed, then posted with the line as the file property "_Print file".
 */
(function () {
  'use strict';

  var VERSION = 'WA1';
  var GRID = 260; // occupancy grid cells across the page width
  var DETAIL_GRID = 400; // finer grid for picture-style artwork (dogs, figures)
  var PAPER = { A4: [210, 297], A3: [297, 420], A2: [420, 594], A1: [594, 841] };
  var BLEED_MM = 3;
  var MAX_PRINT_PIXELS = 16.7e6; // iOS Safari's canvas limit; also keeps the upload a sensible size
  var MAX_DPI = 300;

  var FONTS = [
    { id: 'anton', name: 'Anton', css: 'Anton', weight: 400 },
    { id: 'oswald', name: 'Oswald', css: 'Oswald', weight: 600 },
    { id: 'baloo', name: 'Baloo', css: 'Baloo 2', weight: 800 },
    { id: 'fredoka', name: 'Fredoka', css: 'Fredoka', weight: 600 },
    { id: 'pacifico', name: 'Pacifico', css: 'Pacifico', weight: 400 },
    { id: 'lobster', name: 'Lobster', css: 'Lobster', weight: 400 },
    { id: 'marker', name: 'Marker', css: 'Permanent Marker', weight: 400 },
    { id: 'abril', name: 'Abril', css: 'Abril Fatface', weight: 400 },
    { id: 'mix', name: 'Mix', mix: ['anton', 'pacifico', 'oswald', 'baloo'] }
  ];

  // Colour schemes. "original" takes each word's colour from the artwork under it.
  var SCHEMES = [
    { id: 'original', name: 'Original colours' },
    { id: 'rainbow', name: 'Rainbow', gradient: ['#E53935', '#FB8C00', '#FDD835', '#43A047', '#1E88E5', '#5E35B1', '#8E24AA'], ink: '#1D1240' },
    { id: 'pink', name: 'Pinks', palette: ['#E91E63', '#F06292', '#AD1457', '#FF80AB', '#C2185B', '#F48FB1'], ink: '#880E4F' },
    { id: 'blue', name: 'Blues', palette: ['#1E88E5', '#64B5F6', '#0D47A1', '#29B6F6', '#1565C0', '#4FC3F7'], ink: '#0D2A6B' },
    { id: 'purple', name: 'Purples', palette: ['#7B1FA2', '#AB47BC', '#4A148C', '#CE93D8', '#8E24AA', '#9575CD'], ink: '#38006B' },
    { id: 'teal', name: 'Teal & mint', palette: ['#00897B', '#4DB6AC', '#00695C', '#26C6DA', '#00838F', '#80CBC4'], ink: '#004D40' },
    { id: 'warm', name: 'Sunset', palette: ['#E64A19', '#FF7043', '#F9A825', '#D81B60', '#FB8C00', '#C62828'], ink: '#7F1D1D' },
    { id: 'gold', name: 'Gold & brown', palette: ['#B8860B', '#8D6E63', '#C9A227', '#5D4037', '#A1887F', '#D4A017'], ink: '#3E2723' },
    { id: 'mono', name: 'Black & grey', palette: ['#212121', '#616161', '#424242', '#9E9E9E', '#757575'], ink: '#000000' }
  ];

  var SAMPLE_WORDS = 'Love, Family, Happy, Friends, Laugh, Smile, Kind, Funny, Hugs, Home, Adventure, Dream, Sweet, Brave, Sunshine, Cuddles, Forever, Magic, Star, Wonderful';

  function byId(list, id) { for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i]; return list[0]; }

  /* ------------------------------------------------------------------ helpers */

  function rng(seed) { // mulberry32
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hashStr(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function shuffle(arr, rand) { for (var i = arr.length - 1; i > 0; i--) { var j = Math.floor(rand() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; } return arr; }
  function hexToRgb(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function rgbCss(c) { return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')'; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function lum(c) { return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255; }
  // Keep every colour readable on white paper.
  function printable(c) { var l = lum(c); return l > 0.72 ? mix(c, [0, 0, 0], (l - 0.72) / l + 0.08) : c; }

  function cleanText(s, max) {
    return String(s || '')
      .replace(/[\u{1F000}-\u{1FFFF}\u{2600}-\u{27BF}\u{FE0F}\u{200D}]/gu, '') // emoji print as boxes
      .replace(/\s+/g, ' ').trim().slice(0, max || 30);
  }
  function parseWords(text) {
    var seen = {};
    return String(text || '').split(/[,\n;]+/).map(function (w) { return cleanText(w, 24); })
      .filter(function (w) { var k = w.toLowerCase(); if (!w || seen[k]) return false; seen[k] = 1; return true; })
      .slice(0, 40);
  }

  /* ------------------------------------------------------------------ shape */

  // Builds the page and its grid from a mask image. Orientation follows the artwork.
  function buildShape(img, opts) {
    opts = opts || {};
    var iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    var src = [0, 0, iw, ih];
    if (opts.rawImage) { src = contentBox(img, iw, ih); iw = src[2]; ih = src[3]; }
    var landscape = iw > ih * 1.05;
    var grid = opts.grid || GRID;
    var gw = grid, gh = Math.round(grid * (landscape ? 1 / Math.SQRT2 : Math.SQRT2));
    // Artwork area: the mask image already includes its paper margins when it came from make_masks.py.
    var margin = opts.fromPhoto ? 0.04 : 0.09;
    var aw = gw * (1 - 2 * margin), ah = gh - gw * 2 * margin;
    var s = Math.min(aw / iw, ah / ih);
    var dw = iw * s, dh = ih * s, dx = (gw - dw) / 2, dy = (gh - dh) / 2;

    var c = document.createElement('canvas');
    c.width = gw; c.height = gh;
    var ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(img, src[0], src[1], src[2], src[3], dx, dy, dw, dh);
    var px = ctx.getImageData(0, 0, gw, gh).data;

    var n = gw * gh, inside = new Uint8Array(n), col = new Float32Array(n * 3);
    var hasAlpha = false;
    for (var i = 0; i < n; i++) if (px[i * 4 + 3] < 250 && px[i * 4 + 3] > 0) { hasAlpha = true; break; }
    if (opts.rawImage && !hasAlpha) {
      // A flat picture (white background): the shape is everything that isn't paper-white.
      for (i = 0; i < n; i++) {
        var r = px[i * 4], g = px[i * 4 + 1], b = px[i * 4 + 2], a = px[i * 4 + 3];
        inside[i] = a > 128 && (Math.max(Math.abs(255 - r), Math.abs(255 - g), Math.abs(255 - b)) > 40) ? 1 : 0;
      }
      inside = closeAndFill(inside, gw, gh, 3);
    } else {
      for (i = 0; i < n; i++) inside[i] = px[i * 4 + 3] >= 128 ? 1 : 0;
      if (opts.rawImage) inside = closeAndFill(inside, gw, gh, 2);
    }
    var sx = 0, sy = 0, cnt = 0, minX = gw, minY = gh, maxX = 0, maxY = 0, sum = [0, 0, 0];
    for (var y = 0; y < gh; y++) for (var x = 0; x < gw; x++) {
      i = y * gw + x;
      col[i * 3] = px[i * 4]; col[i * 3 + 1] = px[i * 4 + 1]; col[i * 3 + 2] = px[i * 4 + 2];
      if (!inside[i]) continue;
      sx += x; sy += y; cnt++;
      sum[0] += px[i * 4]; sum[1] += px[i * 4 + 1]; sum[2] += px[i * 4 + 2];
      if (x < minX) minX = x; if (x > maxX) maxX = x; if (y < minY) minY = y; if (y > maxY) maxY = y;
    }
    if (cnt < 50) { // nothing usable: fall back to a soft rectangle so the designer still works
      for (y = Math.round(gh * 0.12); y < gh * 0.88; y++) for (x = Math.round(gw * 0.1); x < gw * 0.9; x++) inside[y * gw + x] = 1;
      return buildShapeFromGrid(inside, col, gw, gh, landscape);
    }
    var avg = [sum[0] / cnt, sum[1] / cnt, sum[2] / cnt];
    // Picture-style artwork (a dog's face, a figure) has lots of light and dark: it needs smaller words so
    // the picture reads. Plain shapes (letters, numbers, hearts) look best with bigger, bolder words.
    var lsum = 0, lsq = 0;
    for (i = 0; i < n; i++) if (inside[i]) { var L = (0.2126 * px[i * 4] + 0.7152 * px[i * 4 + 1] + 0.0722 * px[i * 4 + 2]) / 255; lsum += L; lsq += L * L; }
    var lstd = Math.sqrt(Math.max(0, lsq / cnt - (lsum / cnt) * (lsum / cnt)));
    var detailed = !opts.rawImage && lstd > 0.13;
    // Picture designs get a finer grid so many more, smaller words can draw the face/figure.
    if (detailed && !opts.grid) return buildShape(img, Object.assign({}, opts, { grid: DETAIL_GRID }));
    return {
      detailed: detailed, lstd: lstd,
      gw: gw, gh: gh, landscape: landscape, inside: inside, col: col, count: cnt,
      cx: sx / cnt, cy: sy / cnt, box: [minX, minY, maxX, maxY],
      ink: rgbCss(printable(mix(avg, [0, 0, 0], 0.55))),
      avg: avg
    };
  }
  // The part of a customer's picture that isn't white or see-through margin.
  function contentBox(img, iw, ih) {
    var s = Math.min(1, 400 / Math.max(iw, ih)), w = Math.max(1, Math.round(iw * s)), h = Math.max(1, Math.round(ih * s));
    var c = document.createElement('canvas'); c.width = w; c.height = h;
    var x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(img, 0, 0, w, h);
    var d = x.getImageData(0, 0, w, h).data, x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (var yy = 0; yy < h; yy++) for (var xx = 0; xx < w; xx++) {
      var i = (yy * w + xx) * 4;
      if (d[i + 3] > 128 && Math.max(255 - d[i], 255 - d[i + 1], 255 - d[i + 2]) > 40) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (yy < y0) y0 = yy; if (yy > y1) y1 = yy; }
    }
    if (x1 < 0) return [0, 0, iw, ih];
    return [x0 / s, y0 / s, (x1 - x0 + 1) / s, (y1 - y0 + 1) / s];
  }
  function buildShapeFromGrid(inside, col, gw, gh, landscape) {
    var cnt = 0, sx = 0, sy = 0;
    for (var i = 0; i < inside.length; i++) if (inside[i]) { cnt++; sx += i % gw; sy += (i / gw) | 0; col[i * 3] = 120; col[i * 3 + 1] = 60; col[i * 3 + 2] = 200; }
    return { gw: gw, gh: gh, landscape: landscape, inside: inside, col: col, count: cnt, cx: sx / cnt, cy: sy / cnt, box: [0, 0, gw - 1, gh - 1], ink: '#1D1240', avg: [120, 60, 200] };
  }

  // Morphological close (dilate then erode, r cells) and hole fill on a 0/1 grid.
  function closeAndFill(m, w, h, r) {
    function dil(src, val) {
      var out = new Uint8Array(src.length);
      for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) {
        var hit = 0;
        for (var dy = -r; dy <= r && !hit; dy++) {
          var yy = y + dy; if (yy < 0 || yy >= h) { if (val === 0) hit = 1; continue; }
          for (var dx = -r; dx <= r; dx++) {
            var xx = x + dx; if (xx < 0 || xx >= w) { if (val === 0) { hit = 1; break; } continue; }
            if (src[yy * w + xx] === val) { hit = 1; break; }
          }
        }
        out[y * w + x] = val === 1 ? hit : (hit ? 0 : 1);
      }
      return out;
    }
    var closed = dil(dil(m, 1), 0);
    // flood the background from the border; anything it can't reach is inside
    var bg = new Uint8Array(w * h), stack = [];
    for (var x = 0; x < w; x++) { stack.push(x, (h - 1) * w + x); }
    for (var y = 0; y < h; y++) { stack.push(y * w, y * w + w - 1); }
    while (stack.length) {
      var i = stack.pop();
      if (bg[i] || closed[i]) continue;
      bg[i] = 1;
      var cx = i % w, cy = (i / w) | 0;
      if (cx > 0) stack.push(i - 1); if (cx < w - 1) stack.push(i + 1);
      if (cy > 0) stack.push(i - w); if (cy < h - 1) stack.push(i + w);
    }
    var out = new Uint8Array(w * h);
    for (i = 0; i < out.length; i++) out[i] = bg[i] ? 0 : 1;
    return out;
  }

  /* ------------------------------------------------------------------ layout */

  var SPRITE_PX = 3; // pixels per grid cell when rasterising a word
  var spriteCanvas = null, spriteCache = {};

  function fontCss(font, size) { return font.weight + ' ' + size + 'px "' + font.css + '"'; }

  // Grid cells covered by a word, relative to its anchor (baseline centre). size is in grid cells.
  function sprite(text, font, size, rot) {
    var key = font.id + '|' + size.toFixed(2) + '|' + rot + '|' + text;
    if (spriteCache[key]) return spriteCache[key];
    if (!spriteCanvas) spriteCanvas = document.createElement('canvas');
    var ctx = spriteCanvas.getContext('2d', { willReadFrequently: true });
    var fs = size * SPRITE_PX;
    ctx.font = fontCss(font, fs);
    var m = ctx.measureText(text);
    var asc = m.actualBoundingBoxAscent || fs * 0.8, desc = m.actualBoundingBoxDescent || fs * 0.2;
    var left = m.actualBoundingBoxLeft != null ? m.actualBoundingBoxLeft : m.width / 2;
    var right = m.actualBoundingBoxRight != null ? m.actualBoundingBoxRight : m.width / 2;
    var pad = 2;
    var tw = Math.ceil(left + right) + pad * 2, th = Math.ceil(asc + desc) + pad * 2;
    var W = rot ? th : tw, H = rot ? tw : th;
    if (spriteCanvas.width < W || spriteCanvas.height < H) { spriteCanvas.width = Math.max(W, spriteCanvas.width); spriteCanvas.height = Math.max(H, spriteCanvas.height); }
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, spriteCanvas.width, spriteCanvas.height);
    ctx.font = fontCss(font, fs);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#000';
    // anchor position inside the sprite canvas
    var ax, ay;
    if (!rot) { ax = pad + left; ay = pad + asc; ctx.fillText(text, ax, ay); }
    else { ax = pad + asc; ay = pad + right; ctx.translate(ax, ay); ctx.rotate(-Math.PI / 2); ctx.fillText(text, 0, 0); ctx.setTransform(1, 0, 0, 1, 0, 0); }
    var data = ctx.getImageData(0, 0, W, H).data;
    var cells = {}, list = [];
    for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
      if (data[(y * W + x) * 4 + 3] < 60) continue;
      var gx = Math.floor((x - ax) / SPRITE_PX), gy = Math.floor((y - ay) / SPRITE_PX);
      var k = gx + ',' + gy;
      if (!cells[k]) { cells[k] = 1; list.push(gx, gy); }
    }
    var minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
    for (var i = 0; i < list.length; i += 2) { minx = Math.min(minx, list[i]); maxx = Math.max(maxx, list[i]); miny = Math.min(miny, list[i + 1]); maxy = Math.max(maxy, list[i + 1]); }
    var sp = { cells: new Int16Array(list), w: maxx - minx + 1, h: maxy - miny + 1, minx: minx, miny: miny, midx: (minx + maxx) / 2, midy: (miny + maxy) / 2 };
    spriteCache[key] = sp;
    return sp;
  }

  function fits(shape, occ, sp, ox, oy) {
    var c = sp.cells, gw = shape.gw, gh = shape.gh, ins = shape.inside;
    for (var i = 0; i < c.length; i += 2) {
      var x = ox + c[i], y = oy + c[i + 1];
      if (x < 0 || y < 0 || x >= gw || y >= gh) return false;
      var k = y * gw + x;
      if (!ins[k] || occ[k]) return false;
    }
    return true;
  }
  function mark(shape, occ, sp, ox, oy) {
    var c = sp.cells, gw = shape.gw, n = 0;
    for (var i = 0; i < c.length; i += 2) { var k = (oy + c[i + 1]) * gw + ox + c[i]; if (!occ[k]) { occ[k] = 1; n++; } }
    return n;
  }

  // Place the name once, as big as it will go, as near the middle of the shape as possible.
  function placeName(shape, occ, text, font, maxSize) {
    var best = null;
    [0, 1].forEach(function (rot) {
      var size = maxSize;
      for (var tries = 0; tries < 40 && size > 4; tries++, size *= 0.92) {
        var sp = sprite(text, font, size, rot);
        if ((rot ? sp.h : sp.w) > shape.gw * 1.2) continue;
        var pos = nearestFit(shape, occ, sp, rot ? 1 : 2);
        if (pos) {
          if (!best || size > best.size * (rot ? 1.8 : 1)) best = { size: size, rot: rot, sp: sp, x: pos[0], y: pos[1] };
          break;
        }
      }
    });
    if (!best) return null;
    mark(shape, occ, best.sp, best.x, best.y);
    return { t: text, x: best.x, y: best.y, s: best.size, r: best.rot, f: font.id, name: true, cx: best.x + best.sp.midx, cy: best.y + best.sp.midy };
  }
  function nearestFit(shape, occ, sp, step) {
    var b = shape.box, cand = [];
    for (var y = b[1]; y <= b[3]; y += step) for (var x = b[0]; x <= b[2]; x += step) {
      var cx = x - sp.midx, cy = y - sp.midy;
      cand.push([(x - shape.cx) * (x - shape.cx) + (y - shape.cy) * (y - shape.cy) * 1.6, Math.round(cx), Math.round(cy)]);
    }
    cand.sort(function (a, b2) { return a[0] - b2[0]; });
    for (var i = 0; i < cand.length; i++) if (fits(shape, occ, sp, cand[i][1], cand[i][2])) return [cand[i][1], cand[i][2]];
    return null;
  }

  /* Lays out a design. Runs in slices so typing stays smooth; calls onProgress(placements) as it goes
     and resolves with the finished layout. Returns { cancel() }. */
  function layout(shape, design, onProgress, onDone) {
    var cancelled = false;
    var rand = rng(design.seed);
    var font = byId(FONTS, design.font);
    var fontsFor = font.mix ? font.mix.map(function (id) { return byId(FONTS, id); }) : [font];
    var occ = new Uint8Array(shape.gw * shape.gh);
    var out = [];
    var name = cleanText(design.name, 30);
    var words = design.words.length ? design.words.slice() : parseWords(SAMPLE_WORDS);
    var boxW = shape.box[2] - shape.box[0] + 1, boxH = shape.box[3] - shape.box[1] + 1;
    var nameFont = fontsFor[0];
    var nameSize = 0;
    if (name) {
      // Big but not overpowering: the shape and its picture must still read around the name.
      var start = Math.min(boxH * (shape.detailed ? 0.11 : 0.17), (boxW * (shape.detailed ? 0.55 : 0.72) / Math.max(3, name.length)) * 1.9);
      var p = placeName(shape, occ, name, nameFont, start);
      if (p) { out.push(p); nameSize = p.s; }
    }
    var maxWordLen = words.reduce(function (m, w) { return Math.max(m, w.length); }, 4);
    var size = Math.min(nameSize ? nameSize * 0.45 : boxH * 0.1, boxH * (shape.detailed ? 0.04 : 0.075), (boxW / Math.max(4, maxWordLen)) * 1.1);
    var minSize = shape.detailed ? 2.4 : Math.max(2.8, shape.gw / 92);
    // free shape cells to aim at
    var free = [];
    for (var i = 0; i < shape.inside.length; i++) if (shape.inside[i] && !occ[i]) free.push(i);
    shuffle(free, rand);
    var round = 0;

    function step() {
      if (cancelled) return;
      var t0 = performance.now();
      while (performance.now() - t0 < 14) {
        if (size < minSize) { finish(); return; }
        var list = shuffle(words.slice(), rand);
        var copies = round < 2 ? 1 : Math.min(12, round * 2);
        var placedThisRound = 0;
        for (var c = 0; c < copies; c++) {
          for (var w = 0; w < list.length; w++) {
            var f = fontsFor[(w + c + round) % fontsFor.length];
            var s = Math.round(size * (0.85 + rand() * 0.3) * 4) / 4; // quarter-cell steps so word sprites are reused
            var rot = rand() < 0.32 ? 1 : 0;
            if (placeWord(list[w], f, s, rot) || placeWord(list[w], f, s, 1 - rot)) placedThisRound++;
          }
        }
        round++;
        size *= placedThisRound ? 0.88 : 0.8;
        if (out.length > 3000) { finish(); return; }
      }
      if (onProgress) onProgress(out);
      setTimeout(step, 0);
    }
    function placeWord(text, f, s, rot) {
      var sp = sprite(text, f, s, rot);
      if (sp.w > shape.gw || sp.h > shape.gh) return false;
      for (var a = 0; a < 40 && free.length; a++) {
        var idx = Math.floor(rand() * free.length);
        var k = free[idx];
        if (occ[k]) { free[idx] = free[free.length - 1]; free.pop(); a--; continue; }
        var gx = k % shape.gw, gy = (k / shape.gw) | 0;
        // try a few anchors around the free cell so the word can slide into the gap
        for (var j = 0; j < 4; j++) {
          var ox = Math.round(gx - sp.midx + (j % 2 ? -1 : 1) * (j > 1 ? sp.w / 3 : 0)), oy = Math.round(gy - sp.midy);
          if (fits(shape, occ, sp, ox, oy)) {
            mark(shape, occ, sp, ox, oy);
            out.push({ t: text, x: ox, y: oy, s: s, r: rot, f: f.id, cx: ox + sp.midx, cy: oy + sp.midy });
            return true;
          }
        }
      }
      return false;
    }
    function finish() {
      if (cancelled) return;
      var filled = 0;
      for (var i2 = 0; i2 < occ.length; i2++) filled += occ[i2];
      if (onDone) onDone({ placements: out, coverage: filled / shape.count });
    }
    setTimeout(step, 0);
    return { cancel: function () { cancelled = true; } };
  }

  /* ------------------------------------------------------------------ colour + draw */

  function colourFor(shape, scheme, p, i) {
    if (p.name) {
      if (scheme.id === 'original') return shape.ink;
      return scheme.ink;
    }
    if (scheme.id === 'original') {
      var x = Math.max(0, Math.min(shape.gw - 1, Math.round(p.cx))), y = Math.max(0, Math.min(shape.gh - 1, Math.round(p.cy)));
      var k = (y * shape.gw + x) * 3;
      var c = [shape.col[k], shape.col[k + 1], shape.col[k + 2]];
      if (!shape.inside[y * shape.gw + x]) c = shape.avg;
      // a little variety in shade, like the originals
      var v = ((hashStr(p.t + i) % 100) / 100 - 0.5) * 0.25;
      c = v > 0 ? mix(c, [0, 0, 0], v) : mix(c, [255, 255, 255], -v * 0.6);
      return rgbCss(printable(c));
    }
    if (scheme.gradient) {
      var t = Math.max(0, Math.min(1, ((p.cx - shape.box[0]) / Math.max(1, shape.box[2] - shape.box[0])) * 0.8 + ((p.cy - shape.box[1]) / Math.max(1, shape.box[3] - shape.box[1])) * 0.2));
      var g = scheme.gradient, pos = t * (g.length - 1), a = Math.floor(pos), b = Math.min(g.length - 1, a + 1);
      return rgbCss(printable(mix(hexToRgb(g[a]), hexToRgb(g[b]), pos - a)));
    }
    return scheme.palette[hashStr(p.t + '|' + i) % scheme.palette.length];
  }

  // Draws the design. W = pixel width of the page area; ox/oy = where the page starts (bleed offset).
  function draw(ctx, shape, placements, schemeId, W, ox, oy) {
    var scheme = byId(SCHEMES, schemeId);
    var k = W / shape.gw; // pixels per grid cell
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    for (var i = 0; i < placements.length; i++) {
      var p = placements[i], f = byId(FONTS, p.f);
      // the anchor is the text's centre-aligned baseline point, exactly as in sprite()
      ctx.font = fontCss(f, p.s * k);
      ctx.fillStyle = colourFor(shape, scheme, p, i);
      var x = ox + p.x * k, y = oy + p.y * k;
      if (!p.r) ctx.fillText(p.t, x, y);
      else { ctx.save(); ctx.translate(x, y); ctx.rotate(-Math.PI / 2); ctx.fillText(p.t, 0, 0); ctx.restore(); }
    }
    ctx.restore();
  }
  function paperFor(sizeLabel) {
    var m = /A([1-4])/i.exec(sizeLabel || '');
    return m ? 'A' + m[1] : 'A4';
  }

  // Renders the print-ready file: A size + 3 mm bleed each side, up to 300 dpi (capped for phones).
  function renderPrint(shape, placements, schemeId, paper) {
    var mm = PAPER[paper] || PAPER.A4;
    var wmm = shape.landscape ? mm[1] : mm[0], hmm = shape.landscape ? mm[0] : mm[1];
    var Wt = wmm + 2 * BLEED_MM, Ht = hmm + 2 * BLEED_MM;
    var dpi = Math.min(MAX_DPI, Math.floor(Math.sqrt(MAX_PRINT_PIXELS / ((Wt / 25.4) * (Ht / 25.4)))));
    var pxmm = dpi / 25.4;
    var c = document.createElement('canvas');
    c.width = Math.round(Wt * pxmm); c.height = Math.round(Ht * pxmm);
    var ctx = c.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, c.width, c.height);
    // the grid page has the A ratio exactly; scale it to the trimmed page width
    draw(ctx, shape, placements, schemeId, wmm * pxmm, BLEED_MM * pxmm, BLEED_MM * pxmm);
    return { canvas: c, dpi: dpi, mm: [wmm, hmm], spec: paper + (shape.landscape ? ' landscape ' : ' portrait ') + wmm + '×' + hmm + ' mm + ' + BLEED_MM + ' mm bleed, ' + dpi + ' dpi, ' + c.width + '×' + c.height + ' px' };
  }

  function toBlob(canvas, type, q) {
    return new Promise(function (resolve, reject) {
      if (canvas.toBlob) canvas.toBlob(function (b) { b ? resolve(b) : reject(new Error('Could not make the print file')); }, type, q);
      else reject(new Error('Your browser cannot make the print file'));
    });
  }

  function loadImage(src) {
    return new Promise(function (resolve, reject) {
      var im = new Image();
      im.crossOrigin = 'anonymous';
      im.onload = function () { resolve(im); };
      im.onerror = function () { reject(new Error('Could not load the artwork shape')); };
      im.src = src;
    });
  }
  function loadFonts(fontIds) {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    var list = [];
    fontIds.forEach(function (id) {
      var f = byId(FONTS, id);
      (f.mix ? f.mix.map(function (m) { return byId(FONTS, m); }) : [f]).forEach(function (ff) { list.push(document.fonts.load(fontCss(ff, 40), 'AaBb')); });
    });
    return Promise.all(list).catch(function () {});
  }

  function layoutCode(design) {
    return [VERSION, (design.seed >>> 0).toString(36), design.scheme, design.font].join('.');
  }
  function parseCode(code) {
    var p = String(code || '').trim().split('.');
    if (p[0] !== VERSION || p.length < 4) return null;
    return { seed: parseInt(p[1], 36) >>> 0, scheme: p[2], font: p[3] };
  }

  window.WordArtEngine = {
    VERSION: VERSION, FONTS: FONTS, SCHEMES: SCHEMES, PAPER: PAPER, SAMPLE_WORDS: SAMPLE_WORDS,
    buildShape: buildShape, layout: layout, draw: draw, renderPrint: renderPrint, toBlob: toBlob,
    loadImage: loadImage, loadFonts: loadFonts, parseWords: parseWords, cleanText: cleanText,
    paperFor: paperFor, layoutCode: layoutCode, parseCode: parseCode, hashStr: hashStr, byId: byId
  };
})();

/* ======================================================================== UI */
(function () {
  'use strict';
  var E = window.WordArtEngine;

  function debounce(fn, ms) { var t; return function () { var a = arguments; clearTimeout(t); t = setTimeout(function () { fn.apply(null, a); }, ms); }; }
  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in attrs || {}) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }

  function mount(root, cfg) {
    var form = root.closest('form');
    var section = root.closest('[data-product-section]') || document;
    var $ = function (s) { return root.querySelector(s); };
    var nameInput = $('[data-wa-name]'), wordsInput = $('[data-wa-words]'), countEl = $('[data-wa-count]');
    var msgEl = $('[data-wa-msg]');
    var hidden = {
      name: $('[data-wa-prop="name"]'), words: $('[data-wa-prop="words"]'), colours: $('[data-wa-prop="colours"]'),
      font: $('[data-wa-prop="font"]'), code: $('[data-wa-prop="code"]')
    };
    var design = {
      name: '', words: [],
      seed: E.hashStr(String(cfg.productId || cfg.handle || 'foxy')) >>> 0,
      scheme: cfg.defaultScheme || 'original',
      font: cfg.defaultFont || 'anton'
    };
    var state = { shape: null, placements: [], job: null, done: null, uploadFile: null, variant: null, busy: false };

    // Old two-box personaliser: hidden and switched off while the designer runs (it stays as the fallback).
    if (form) {
      form.classList.add('wa-ready');
      form.querySelectorAll('[data-personaliser] input, [data-personaliser] textarea, [data-personaliser] select').forEach(function (i) {
        i.disabled = true; i.removeAttribute('data-required'); i.required = false;
      });
      // The theme keeps "Add to basket" disabled until the old panel's confirm box is ticked; our own box replaces it.
      // The Infinite Options app's own word box ("Enter words of your choice…") duplicates the designer:
      // hide it and switch its fields off, including fields the app adds after the page has loaded.
      var io = form.querySelector('#infiniteoptions-container');
      var quietIO = function () {
        if (!io || state.failed) return;
        io.querySelectorAll('input, textarea, select').forEach(function (i) {
          i.disabled = true; i.required = false; i.removeAttribute('required'); i.removeAttribute('data-required');
        });
      };
      if (io) {
        quietIO();
        if (window.MutationObserver) { state.ioObserver = new MutationObserver(quietIO); state.ioObserver.observe(io, { childList: true, subtree: true }); }
      }
      var oldConfirm = form.querySelector('[data-personaliser] [data-confirm]');
      if (oldConfirm) { oldConfirm.disabled = false; oldConfirm.checked = true; oldConfirm.dispatchEvent(new Event('change', { bubbles: true })); }
    }
    Object.keys(hidden).forEach(function (k) { if (hidden[k]) hidden[k].disabled = false; });

    /* ---------- preview on the product stage ---------- */
    var stage = section.querySelector('[data-stage]');
    var preview = el('div', { class: 'wa-stage', 'data-wa-stage': '' });
    var canvas = el('canvas', { width: 1000, height: 1414, role: 'img', 'aria-label': 'Preview of your personalised word art' });
    preview.appendChild(canvas);
    preview.appendChild(el('span', { class: 'wa-stage__badge' }, '✏️ Your design'));
    var photo = stage && stage.querySelector('[data-photo-view]');
    if (stage) stage.appendChild(preview); else root.insertBefore(preview, root.firstChild);
    var thumbs = section.querySelector('[data-thumbs]');
    var myThumb = null;
    function showMine(on) {
      preview.hidden = !on;
      if (photo) photo.hidden = on;
      var live = section.querySelector('[data-live-view]'); if (live && on) live.hidden = true;
      if (thumbs) thumbs.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-current', String(on ? b === myThumb : b.getAttribute('aria-current') === 'true' && b !== myThumb)); });
    }
    if (thumbs) {
      var li = el('li');
      myThumb = el('button', { type: 'button', class: 'wa-thumb', 'aria-label': 'Your design' }, '<span aria-hidden="true">✏️</span><small>Your design</small>');
      li.appendChild(myThumb);
      thumbs.insertBefore(li, thumbs.firstChild);
      myThumb.addEventListener('click', function () { showMine(true); });
      thumbs.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b && b !== myThumb) { preview.hidden = true; if (myThumb) myThumb.setAttribute('aria-current', 'false'); } });
    }
    var mini = $('[data-wa-mini]');
    showMine(true);

    function paint(placements) {
      if (!state.shape) return;
      var s = state.shape, W = canvas.width, H = Math.round(W * s.gh / s.gw);
      if (canvas.height !== H) canvas.height = H;
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, W, H);
      E.draw(ctx, s, placements, design.scheme, W, 0, 0);
      if (mini) {
        mini.width = 360; mini.height = Math.round(360 * H / W);
        var m = mini.getContext('2d');
        m.drawImage(canvas, 0, 0, mini.width, mini.height);
      }
    }

    /* ---------- layout ---------- */
    function relayout() {
      if (!state.shape) return;
      if (state.job) state.job.cancel();
      root.classList.add('is-working');
      var d = { name: design.name || (cfg.upload ? 'Your Name' : cfg.sampleName || 'Your Name'), words: design.words, seed: design.seed, font: design.font };
      var resolveDone;
      state.done = new Promise(function (r) { resolveDone = r; });
      state.job = E.layout(state.shape, d, function (p) { state.placements = p; paint(p); }, function (res) {
        state.placements = res.placements; state.coverage = res.coverage;
        paint(res.placements);
        root.classList.remove('is-working');
        resolveDone(res);
      });
      syncHidden();
    }
    var relayoutSoon = debounce(relayout, 450);

    function syncHidden() {
      if (hidden.name) hidden.name.value = design.name;
      if (hidden.words) hidden.words.value = design.words.join(', ');
      if (hidden.colours) hidden.colours.value = E.byId(E.SCHEMES, design.scheme).name;
      if (hidden.font) hidden.font.value = E.byId(E.FONTS, design.font).name;
      if (hidden.code) hidden.code.value = E.layoutCode(design);
    }

    function updateCount() {
      var n = design.words.length;
      if (countEl) countEl.textContent = n + (n === 1 ? ' word' : ' words') + (n < 20 ? ' · aim for 20–30' : n > 30 ? ' · great, lots of variety' : ' · perfect');
    }

    nameInput.addEventListener('input', function () { design.name = E.cleanText(nameInput.value, 30); syncHidden(); relayoutSoon(); });
    wordsInput.addEventListener('input', function () { design.words = E.parseWords(wordsInput.value); updateCount(); syncHidden(); relayoutSoon(); });
    $('[data-wa-shuffle]').addEventListener('click', function () {
      design.seed = (Math.random() * 4294967296) >>> 0;
      showMine(true);
      relayout();
    });

    // colour + font pickers
    root.querySelectorAll('[data-wa-scheme]').forEach(function (b) {
      b.addEventListener('click', function () {
        design.scheme = b.getAttribute('data-wa-scheme');
        root.querySelectorAll('[data-wa-scheme]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        syncHidden(); paint(state.placements); showMine(true);
      });
    });
    root.querySelectorAll('[data-wa-font]').forEach(function (b) {
      b.addEventListener('click', function () {
        design.font = b.getAttribute('data-wa-font');
        root.querySelectorAll('[data-wa-font]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        E.loadFonts([design.font]).then(relayout);
        showMine(true);
      });
    });

    // "Create your own": the customer's picture becomes the shape
    var upload = $('[data-wa-upload]');
    if (upload) upload.addEventListener('change', function () {
      var f = upload.files && upload.files[0];
      if (!f) return;
      if (f.size > 20 * 1024 * 1024) { msg('Please choose a picture under 20 MB.', true); return; }
      state.uploadFile = f;
      var url = URL.createObjectURL(f);
      E.loadImage(url).then(function (img) {
        state.shape = E.buildShape(img, { rawImage: true });
        msg('');
        relayout();
      }).catch(function () { msg('We couldn\'t read that picture. Please try a JPG or PNG.', true); });
    });

    document.addEventListener('foxy:variant-change', function (e) { state.variant = e.detail && e.detail.variant; });

    function msg(t, bad) { if (!msgEl) return; msgEl.textContent = t || ''; msgEl.classList.toggle('is-error', !!bad); }

    function sizeLabel() {
      var v = state.variant;
      if (v) return v.title || v.option1 || '';
      var checked = form && form.querySelector('[data-option-index]:checked');
      return checked ? checked.value : 'A4';
    }

    /* ---------- add to basket with the print file ---------- */
    // If the designer can't start (e.g. the shape image won't load), give the page back its normal panel.
    function standDown(reason) {
      state.failed = true;
      if (window.console) console.warn('Word art designer off:', reason);
      if (form) {
        form.classList.remove('wa-ready');
        form.querySelectorAll('[data-personaliser] input, [data-personaliser] textarea, [data-personaliser] select').forEach(function (i) { i.disabled = false; });
        form.querySelectorAll('[data-personaliser] [data-field]').forEach(function (i, n) { if (n === 0) i.setAttribute('data-required', ''); });
      }
      Object.keys(hidden).forEach(function (k) { if (hidden[k]) hidden[k].disabled = true; });
      if (state.ioObserver) state.ioObserver.disconnect();
      var ioBox = form && form.querySelector('#infiniteoptions-container');
      if (ioBox) ioBox.querySelectorAll('input, textarea, select').forEach(function (i) { i.disabled = false; });
      preview.remove();
      if (myThumb) myThumb.parentNode.remove();
      if (photo) photo.hidden = false;
      root.hidden = true;
    }

    document.addEventListener('submit', function (e) {
      if (e.target !== form || state.failed) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      if (state.busy) return;
      if (!design.name) { msg('Please type the name for your print.', true); nameInput.focus(); return; }
      if (design.words.length < 3) { msg('Please add at least 3 words, separated by commas (20–30 works best).', true); wordsInput.focus(); return; }
      if (cfg.upload && !state.uploadFile) { msg('Please upload your picture or silhouette first.', true); return; }
      var confirmBox = form.querySelector('[data-wa-confirm]');
      if (confirmBox && !confirmBox.checked) { msg('Please tick the box to confirm you\'ve checked your design.', true); return; }
      state.busy = true;
      var buttons = form.querySelectorAll('button[type="submit"]');
      buttons.forEach(function (b) { b.disabled = true; });
      msg('Making your print-ready file…');
      var returnTo = (form.querySelector('[data-return-to]') || {}).value || '';
      var paper = E.paperFor(sizeLabel());
      showMine(true);

      (state.done || Promise.resolve()).then(function () {
        return new Promise(function (r) { setTimeout(r, 30); });
      }).then(function () {
        var fd = new FormData(form);
        syncHidden();
        fd.set('properties[Layout code]', E.layoutCode(design));
        var made;
        try { made = E.renderPrint(state.shape, state.placements, design.scheme, paper); } catch (err) { made = null; }
        var fileStep = made ? E.toBlob(made.canvas, 'image/png').then(function (b) {
          return b.size > 18 * 1024 * 1024 ? E.toBlob(made.canvas, 'image/jpeg', 0.93) : b;
        }) : Promise.resolve(null);
        return fileStep.catch(function () { return null; }).then(function (blob) {
          var base = (cfg.handle || 'word-art').slice(0, 60) + '-' + paper;
          if (blob) {
            fd.append('properties[_Print file]', blob, base + (blob.type === 'image/jpeg' ? '.jpg' : '.png'));
            fd.set('properties[_Print spec]', made.spec);
          } else {
            fd.set('properties[_Print file]', 'Not attached: re-create from the Layout code');
          }
          if (state.uploadFile) fd.append('properties[_Your picture]', state.uploadFile, state.uploadFile.name);
          fd.delete('return_to');
          msg('Adding to your basket…');
          return fetch(cfg.cartAddUrl || '/cart/add.js', { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
            .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.description || j.message || 'Could not add to basket'); return j; }); });
        });
      }).then(function (line) {
        if (cfg.demo) { if (cfg.onDemoOrder) cfg.onDemoOrder(line); msg('Demo: added.'); return; }
        msg('Added! Taking you to your basket…');
        window.location.href = returnTo === '/checkout' ? '/checkout' : (cfg.cartUrl || '/cart');
      }).catch(function (err) {
        msg((err && err.message) || 'Something went wrong. Please try again.', true);
      }).then(function () {
        state.busy = false;
        buttons.forEach(function (b) { b.disabled = false; });
      });
    }, true);

    /* ---------- start ---------- */
    syncHidden();
    updateCount();
    var fontsReady = E.loadFonts(E.FONTS.map(function (f) { return f.id; }));
    var shapeReady;
    if (!cfg.upload && !cfg.maskUrl && !cfg.imageUrl) {
      shapeReady = Promise.reject(new Error('no artwork image'));
    } else if (cfg.upload && !cfg.maskUrl) {
      shapeReady = E.loadImage(cfg.sampleShapeUrl || cfg.imageUrl).then(function (img) { return E.buildShape(img, { rawImage: true }); });
    } else if (cfg.maskUrl) {
      shapeReady = E.loadImage(cfg.maskUrl).then(function (img) { return E.buildShape(img, { fromPhoto: true }); });
    } else {
      shapeReady = E.loadImage(cfg.imageUrl).then(function (img) { return E.buildShape(img, { rawImage: true }); });
    }
    Promise.all([shapeReady, fontsReady]).then(function (r) { state.shape = r[0]; relayout(); })
      .catch(function (err) { if (cfg.upload) msg((err && err.message) || 'The designer could not start.', true); else standDown(err && err.message); });

    var api = { design: design, state: state, relayout: relayout, paint: paint };
    root.__wa = api;
    return api;
  }

  window.WordArtDesigner = { mount: mount };
  function autoMount() {
    document.querySelectorAll('[data-word-art]').forEach(function (root) {
      if (root.__wa) return;
      var c = root.querySelector('script[type="application/json"]');
      try { mount(root, c ? JSON.parse(c.textContent) : {}); } catch (e) { if (window.console) console.error('Word art designer', e); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', autoMount); else autoMount();
})();
