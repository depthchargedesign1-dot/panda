/* Ryedale Removals — site behaviour (no dependencies) */
(function () {
  'use strict';

  // Mobile navigation
  var toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var header = document.querySelector('.site-header');
      document.querySelector('.nav').style.top = header.getBoundingClientRect().bottom + 'px';
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.querySelectorAll('.nav button.nav-link').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.body.classList.remove('nav-open');
      document.querySelectorAll('.nav li.open').forEach(function (li) { li.classList.remove('open'); });
    }
  });

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -60px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Prefill the quote form from ?service=
  var params = new URLSearchParams(location.search);
  var svc = params.get('service');
  if (svc) {
    var box = document.querySelector('input[name="services[]"][data-slug="' + svc + '"]');
    if (box) box.checked = true;
  }

  // Field validation helper
  function validate(scope) {
    var ok = true, first = null;
    scope.querySelectorAll('[required]').forEach(function (f) {
      var bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.toggle('field-error', bad);
      if (bad && !first) first = f;
      if (bad) ok = false;
    });
    if (first) first.focus();
    return ok;
  }

  // Quote wizard
  var wizard = document.querySelector('[data-wizard]');
  if (wizard) {
    var steps = wizard.querySelectorAll('.wizard-step');
    var bars = document.querySelectorAll('.wizard-progress li');
    var current = 0;
    var show = function (i) {
      steps.forEach(function (s, n) { s.classList.toggle('active', n === i); });
      bars.forEach(function (b, n) {
        b.classList.toggle('done', n < i);
        b.classList.toggle('current', n === i);
      });
      current = i;
      var last = i === steps.length - 1;
      wizard.querySelector('[data-prev]').style.visibility = i === 0 ? 'hidden' : 'visible';
      wizard.querySelector('[data-next]').hidden = last;
      wizard.querySelector('[type=submit]').hidden = !last;
      if (last) buildSummary();
      var top = wizard.getBoundingClientRect().top + window.scrollY - 110;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: 'smooth' });
    };
    wizard.querySelectorAll('[data-next]').forEach(function (b) {
      b.addEventListener('click', function () { if (validate(steps[current])) show(current + 1); });
    });
    wizard.querySelectorAll('[data-prev]').forEach(function (b) {
      b.addEventListener('click', function () { show(current - 1); });
    });
    var buildSummary = function () {
      var out = wizard.querySelector('[data-summary]');
      if (!out) return;
      var fd = new FormData(wizard), rows = {}, html = '';
      fd.forEach(function (v, k) {
        if (!v || k === 'website' || k === 'form') return;
        var label = (wizard.querySelector('[name="' + k + '"]') || {}).dataset;
        var name = (label && label.label) || k.replace('[]', '');
        rows[name] = rows[name] ? rows[name] + ', ' + v : v;
      });
      Object.keys(rows).forEach(function (k) {
        html += '<dt>' + esc(k) + '</dt><dd>' + esc(rows[k]) + '</dd>';
      });
      out.innerHTML = html;
    };
    wizard.addEventListener('input', function () { if (current === steps.length - 1) buildSummary(); });
    show(0);
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // AJAX form submission with graceful fallback to a normal POST
  document.querySelectorAll('form[data-ajax]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!validate(form)) { e.preventDefault(); return; }
      if (!window.fetch) return;
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var btn = form.querySelector('[type=submit]');
      if (btn) { btn.disabled = true; btn.dataset.text = btn.innerHTML; btn.innerHTML = 'Sending…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r; })
        .then(function () {
          form.reset();
          status.className = 'form-status ok';
          status.textContent = form.dataset.success || 'Thank you — we’ll be in touch shortly.';
          if (wizard && form === wizard) {
            wizard.querySelectorAll('.wizard-step, .wizard-nav').forEach(function (el) { el.style.display = 'none'; });
          }
        })
        .catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Sorry, something went wrong sending your message. Please call us or email us directly.';
        })
        .then(function () { if (btn) { btn.disabled = false; btn.innerHTML = btn.dataset.text; } });
    });
  });
})();
