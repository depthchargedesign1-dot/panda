/*
 * Foxy Leavers Print Studio — turns an order's "_Print files" link into the 300 dpi PNGs for the printer.
 * Open the link from the order in Shopify admin (or paste it here). Needs leavers-engine.js.
 */
(function () {
  'use strict';
  var E = window.LeaversEngine;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function mount(root) {
    root.classList.add('lps');
    root.innerHTML =
      '<h1>Leavers Print Studio</h1>' +
      '<p>Open the <b>_Print files</b> link from the order in Shopify admin, or paste it (or the design code) below.</p>' +
      '<textarea rows="3" data-code placeholder="https://foxyprinting.co.uk/pages/leavers-print-studio#d=z…"></textarea>' +
      '<div class="lps-row">' +
      '  <button type="button" class="lps-btn" data-load>Load design</button>' +
      '  <label>Order no. <input type="text" data-order size="10" placeholder="#1234"></label>' +
      '  <label>Resolution <select data-dpi><option value="300">300 dpi (standard)</option><option value="360">360 dpi</option><option value="150">150 dpi (quick check)</option></select></label>' +
      '</div>' +
      '<p class="lps-error" data-error role="alert"></p>' +
      '<div data-result hidden>' +
      '  <div class="lps-grid">' +
      '    <canvas width="1000" height="1100" data-front aria-label="Front mockup"></canvas>' +
      '    <canvas width="1000" height="1100" data-back aria-label="Back mockup"></canvas>' +
      '    <div><table data-summary></table></div>' +
      '  </div>' +
      '  <h2>Names on the back <small data-count></small></h2><ol class="lps-names" data-names></ol>' +
      '  <div class="lps-row"><button type="button" class="lps-btn" data-render>Generate print files</button><button type="button" class="lps-btn lps-btn--ghost" data-all hidden>Download all</button><span data-status></span></div>' +
      '  <div class="lps-files" data-files></div>' +
      '</div>';

    var $ = function (s) { return root.querySelector(s); };
    var design = null, files = [];

    function load(code) {
      $('[data-error]').textContent = '';
      $('[data-files]').innerHTML = '';
      $('[data-all]').hidden = true;
      return E.decode(code).then(function (d) {
        design = d;
        return Promise.all([E.loadFonts(d), E.loadLogo(d), E.loadPhotos(d)]).then(function () { show(d); });
      }).catch(function (e) {
        $('[data-result]').hidden = true;
        $('[data-error]').textContent = 'That doesn\'t look like a leavers design code (' + e.message + ').';
      });
    }

    function show(d) {
      $('[data-result]').hidden = false;
      E.renderMockup($('[data-front]'), d, 'front');
      E.renderMockup($('[data-back]'), d, 'back');
      var P = E.PRODUCTS[d.product];
      var rows = [
        ['Garment', P.name + (P.code ? ' — AWDis ' + P.code : '')],
        ['Colour', E.colourOf(d).name + ' (' + E.bodyHex(d) + (P.colourways ? ' / ' + E.trimHex(d) : '') + ')'],
        ['Back design', E.byId(E.BACK_TEMPLATES, d.back.template).name],
        ['Wording', [d.back.title, d.back.year, d.back.school].filter(Boolean).join(' · ')],
        ['Fonts', d.back.nameFont + ' (names) / ' + d.back.displayFont + ' (headings)'],
        ['Print colours', E.byId(E.INKS, d.back.ink).name + ' ' + E.inkHex(d.back.ink) + ' + ' + E.byId(E.INKS, d.back.accent).name + ' ' + E.inkHex(d.back.accent)],
        ['Front', E.byId(E.FRONT_STYLES, d.front.style).name + (d.front.logoUrl ? ' — <a href="' + esc(d.front.logoUrl) + '" target="_blank" rel="noopener">original logo</a>' : '')],
        ['Personal', (d.personal.text || '—') + ' (' + E.byId(E.PERSONAL_POSITIONS, d.personal.position).name + ', ' + d.personal.font + ')'],
        ['Print areas', E.printAreas(d).map(function (a) { return a.label + ' ' + a.mm.w + '×' + a.mm.h + ' mm'; }).join('<br>')]
      ];
      $('[data-summary]').innerHTML = rows.map(function (r) { return '<tr><th>' + r[0] + '</th><td>' + (r[0] === 'Front' || r[0] === 'Print areas' ? r[1] : esc(r[1])) + '</td></tr>'; }).join('');
      var names = E.cleanNames(d);
      $('[data-count]').textContent = '(' + names.length + ')';
      $('[data-names]').innerHTML = names.map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('');
    }

    function render() {
      if (!design) return;
      var dpi = parseInt($('[data-dpi]').value, 10) || 300;
      var order = $('[data-order]').value.replace(/[^A-Za-z0-9]+/g, '');
      $('[data-status]').textContent = 'Rendering at ' + dpi + ' dpi…';
      $('[data-files]').innerHTML = '';
      files.forEach(function (f) { URL.revokeObjectURL(f.url); });
      return E.renderPrintFiles(design, { dpi: dpi, prefix: order ? 'order' + order : 'leavers' }).then(function (out) {
        files = out.map(function (f) { f.url = URL.createObjectURL(f.blob); return f; });
        files.forEach(function (f) {
          var box = document.createElement('div');
          box.className = 'lps-file';
          var thumb = document.createElement('canvas');
          thumb.width = 240; thumb.height = Math.round(240 * f.height / f.width);
          var tx = thumb.getContext('2d');
          tx.fillStyle = E.bodyHex(design); tx.fillRect(0, 0, thumb.width, thumb.height);
          tx.drawImage(f.canvas, 0, 0, thumb.width, thumb.height);
          box.appendChild(thumb);
          var info = document.createElement('div');
          info.innerHTML = '<strong>' + esc(f.label) + '</strong><br>' + f.mm.w + ' × ' + f.mm.h + ' mm · ' + f.width + ' × ' + f.height + ' px · ' +
            (f.blob.size / 1048576).toFixed(1) + ' MB<br><small>Shown on the garment colour; the PNG itself is transparent.</small><br><a href="' + f.url + '" download="' + esc(f.filename) + '">Download PNG</a>';
          box.appendChild(info);
          $('[data-files]').appendChild(box);
        });
        $('[data-all]').hidden = !files.length;
        $('[data-status]').textContent = files.length + ' file' + (files.length === 1 ? '' : 's') + ' ready — transparent PNG, ' + dpi + ' dpi.';
      }).catch(function (e) {
        $('[data-status]').textContent = '';
        $('[data-error]').textContent = 'Could not render: ' + e.message + (design.front.logoUrl ? ' (if this mentions a tainted canvas, download the logo and place it by hand)' : '');
      });
    }

    $('[data-load]').addEventListener('click', function () { load($('[data-code]').value); });
    $('[data-render]').addEventListener('click', render);
    $('[data-all]').addEventListener('click', function () {
      files.forEach(function (f, i) {
        setTimeout(function () {
          var a = document.createElement('a');
          a.href = f.url; a.download = f.filename;
          document.body.appendChild(a); a.click(); a.remove();
        }, i * 400);
      });
    });

    function fromHash() {
      if (/[#&]d=/.test(location.hash)) {
        $('[data-code]').value = location.href;
        load(location.hash);
      }
    }
    window.addEventListener('hashchange', fromHash);
    fromHash();
    return { load: load, render: render };
  }

  window.LeaversStudio = { mount: mount };
  function autoMount() {
    document.querySelectorAll('[data-leavers-studio]').forEach(function (el) { if (!el.__lps) el.__lps = mount(el); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', autoMount); else autoMount();
})();
