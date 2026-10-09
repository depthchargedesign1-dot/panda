/* Foxy Pop theme — core interactions (no dependencies). */
(function () {
  'use strict';

  /* ---------- Announcement rotator ---------- */
  document.querySelectorAll('[data-rotator]').forEach((el) => {
    const items = el.children;
    if (items.length < 2) return;
    let i = 0;
    const ms = (parseInt(el.dataset.interval, 10) || 5) * 1000;
    setInterval(() => {
      items[i].classList.remove('is-active');
      i = (i + 1) % items.length;
      items[i].classList.add('is-active');
    }, ms);
  });

  /* ---------- Mega menu ---------- */
  const nav = document.querySelector('[data-mega-nav]');
  if (nav) {
    const items = Array.from(nav.querySelectorAll('[data-mega-item]'));
    const canHover = window.matchMedia('(hover: hover)').matches;
    let closeTimer = 0;
    let openTimer = 0;

    const open = (item) => {
      items.forEach((other) => { if (other !== item) close(other); });
      item.classList.add('is-open');
      const trigger = item.querySelector('[data-mega-trigger]');
      if (trigger) trigger.setAttribute('aria-expanded', 'true');
    };
    const close = (item) => {
      item.classList.remove('is-open');
      const trigger = item.querySelector('[data-mega-trigger]');
      if (trigger) trigger.setAttribute('aria-expanded', 'false');
    };
    const closeAll = () => items.forEach(close);

    items.forEach((item) => {
      const trigger = item.querySelector('[data-mega-trigger]');
      if (!trigger) return;
      trigger.addEventListener('click', () => (item.classList.contains('is-open') ? close(item) : open(item)));
      if (canHover) {
        // Hover intent. The bar can wrap onto two rows, so moving the mouse down from a department to its
        // open panel can pass over another department. Switching therefore needs the pointer to rest on the
        // new department briefly, and is skipped while the pointer is heading down towards the open panel.
        item.addEventListener('mouseenter', () => {
          clearTimeout(closeTimer);
          clearTimeout(openTimer);
          const current = items.find((x) => x.classList.contains('is-open'));
          if (current === item) return;
          const tryOpen = () => {
            if (current && headingToPanel(current)) { openTimer = setTimeout(tryOpen, 120); return; }
            open(item);
          };
          openTimer = setTimeout(tryOpen, current ? 260 : 140);
        });
        item.addEventListener('mouseleave', () => {
          clearTimeout(openTimer);
          closeTimer = setTimeout(() => close(item), 260);
        });
      }
    });

    // Recent pointer positions, used to tell "moving down into the open panel" from "choosing another department".
    const trail = [];
    if (canHover) {
      document.addEventListener('mousemove', (e) => {
        trail.push({ x: e.clientX, y: e.clientY, t: performance.now() });
        if (trail.length > 6) trail.shift();
      }, { passive: true });
    }
    const headingToPanel = (openItem) => {
      const panel = openItem.querySelector('[data-mega-panel]');
      if (!panel || trail.length < 2) return false;
      const a = trail[0];
      const b = trail[trail.length - 1];
      if (performance.now() - b.t > 150) return false; // the pointer has stopped: the customer is choosing
      const top = panel.getBoundingClientRect().top;
      const dx = Math.abs(b.x - a.x);
      const dy = b.y - a.y;
      return dy > 0 && dy >= dx * 0.6 && b.y < top + 4;
    };
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openItem = items.find((x) => x.classList.contains('is-open'));
        if (openItem) { close(openItem); const t = openItem.querySelector('[data-mega-trigger]'); if (t) t.focus(); }
      }
    });
    document.addEventListener('click', (e) => { if (!nav.contains(e.target)) closeAll(); });
  }

  /* ---------- Mobile drawer ---------- */
  const drawer = document.querySelector('[data-drawer]');
  if (drawer) {
    const openers = document.querySelectorAll('[data-drawer-open]');
    const setOpen = (on) => {
      drawer.classList.toggle('is-open', on);
      drawer.setAttribute('aria-hidden', String(!on));
      openers.forEach((b) => b.setAttribute('aria-expanded', String(on)));
      document.body.style.overflow = on ? 'hidden' : '';
      if (on) { const c = drawer.querySelector('.drawer__close'); if (c) c.focus(); }
    };
    openers.forEach((b) => b.addEventListener('click', () => setOpen(true)));
    drawer.querySelectorAll('[data-drawer-close]').forEach((b) => b.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && drawer.classList.contains('is-open')) setOpen(false); });
  }

  /* ---------- Countdown ---------- */
  document.querySelectorAll('[data-countdown]').forEach((el) => {
    const target = new Date(el.dataset.countdown.replace(' ', 'T')).getTime();
    if (isNaN(target)) return;
    const d = el.querySelector('[data-days]');
    const h = el.querySelector('[data-hours]');
    const m = el.querySelector('[data-mins]');
    const tick = () => {
      const diff = Math.max(0, target - Date.now());
      d.textContent = Math.floor(diff / 864e5);
      h.textContent = String(Math.floor((diff % 864e5) / 36e5)).padStart(2, '0');
      m.textContent = String(Math.floor((diff % 36e5) / 6e4)).padStart(2, '0');
    };
    tick();
    setInterval(tick, 30000);
  });

  /* ---------- Money ---------- */
  function formatMoney(cents) {
    const fmt = (window.FoxyTheme && window.FoxyTheme.moneyFormat) || '£{{amount}}';
    const value = (cents / 100).toFixed(2);
    return fmt.replace(/\{\{\s*(\w+)\s*\}\}/, (_, key) => {
      if (key === 'amount_no_decimals') return Math.round(cents / 100).toString();
      if (key === 'amount_with_comma_separator') return value.replace('.', ',');
      return value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    });
  }

  /* ---------- Product form ---------- */
  const section = document.querySelector('[data-product-section]');
  const productJsonEl = document.querySelector('[data-product-json]');
  if (section && productJsonEl) {
    const product = JSON.parse(productJsonEl.textContent);
    const form = section.querySelector('[data-product-form]');
    const idInput = form.querySelector('[data-variant-id]');
    const addBtn = form.querySelector('[data-add-button]');
    const priceEl = section.querySelector('[data-price]');
    const strings = (window.FoxyTheme && window.FoxyTheme.strings) || {};
    const confirm = form.querySelector('[data-confirm]');

    const selectedOptions = () => {
      const opts = [];
      form.querySelectorAll('[data-option-index]:checked').forEach((input) => { opts[+input.dataset.optionIndex] = input.value; });
      return opts;
    };

    const update = () => {
      const opts = selectedOptions();
      const variant = product.variants.find((v) => v.options.every((o, i) => opts[i] === undefined || opts[i] === o));
      if (variant) {
        idInput.value = variant.id;
        if (priceEl) priceEl.textContent = formatMoney(variant.price);
        addBtn.disabled = !variant.available || (confirm && !confirm.checked);
        addBtn.textContent = variant.available ? strings.addToCart : strings.soldOut;
        const url = new URL(window.location.href);
        url.searchParams.set('variant', variant.id);
        window.history.replaceState({}, '', url);
      } else {
        addBtn.disabled = true;
        addBtn.textContent = strings.unavailable;
      }
      document.dispatchEvent(new CustomEvent('foxy:variant-change', { detail: { variant, options: opts } }));
    };
    form.addEventListener('change', (e) => { if (e.target.matches('[data-option-index]')) update(); });

    if (confirm) {
      addBtn.disabled = true;
      confirm.addEventListener('change', () => update());
    }

    form.querySelectorAll('[data-qty]').forEach((btn) => btn.addEventListener('click', () => {
      const input = form.querySelector('input[name="quantity"]');
      input.value = Math.max(1, (parseInt(input.value, 10) || 1) + parseInt(btn.dataset.qty, 10));
    }));

    form.addEventListener('submit', (e) => {
      const missing = Array.from(form.querySelectorAll('[data-required]')).filter((f) => (f.type === 'file' ? !f.files.length : !f.value.trim()));
      if (missing.length) {
        e.preventDefault();
        missing[0].focus();
        missing.forEach((f) => { f.style.borderColor = 'var(--fx-sale)'; });
        return;
      }
      addBtn.disabled = true;
      addBtn.textContent = '…';
    });

    // Thumbnails switch between the product photos (shown first) and the live preview (last).
    const liveView = section.querySelector('[data-live-view]');
    const photoView = section.querySelector('[data-photo-view]');
    const thumbs = Array.from(section.querySelectorAll('[data-thumbs] button'));
    const showStage = (btn) => {
      thumbs.forEach((b) => b.setAttribute('aria-current', String(b === btn)));
      const live = !!(btn && btn.hasAttribute('data-thumb-live'));
      if (liveView) liveView.hidden = !live;
      if (photoView) {
        photoView.hidden = live && !!liveView;
        if (!live && btn) {
          photoView.src = btn.dataset.thumb;
          const img = btn.querySelector('img');
          photoView.alt = btn.getAttribute('aria-label') || (img && img.alt) || '';
        }
      }
    };
    thumbs.forEach((btn) => btn.addEventListener('click', () => showStage(btn)));
    const liveThumb = section.querySelector('[data-thumb-live]');
    window.FoxyGallery = {
      showLive: () => { if (liveThumb) showStage(liveThumb); },
      isLive: () => !!(liveView && !liveView.hidden)
    };
    section.querySelectorAll('[data-show-preview]').forEach((btn) => btn.addEventListener('click', () => {
      window.FoxyGallery.showLive();
      const stage = section.querySelector('[data-stage]');
      if (stage && stage.getBoundingClientRect().bottom < 80) stage.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
    // Picking a variant (e.g. Rose Gold) shows that variant's photo unless the customer is looking at their design.
    document.addEventListener('foxy:variant-change', (e) => {
      const v = e.detail && e.detail.variant;
      const id = v && v.featured_media && v.featured_media.id;
      if (!id || window.FoxyGallery.isLive()) return;
      const btn = thumbs.find((b) => b.dataset.mediaId === String(id));
      if (btn) showStage(btn);
    });

    update();
  }

  /* ---------- Collection: search within + sub-category chips ---------- */
  document.querySelectorAll('[data-col-search]').forEach((box) => {
    const input = box.querySelector('[data-col-search-input]');
    const form = box.querySelector('[data-col-search-form]');
    const q = box.querySelector('[data-col-search-q]');
    const chips = Array.from(box.querySelectorAll('[data-chip]'));
    const more = box.querySelector('[data-col-search-more]');
    const empty = box.querySelector('[data-col-search-empty]');
    const scope = box.dataset.scope || '';

    const filterChips = () => {
      const term = input.value.trim().toLowerCase();
      let visible = 0;
      chips.forEach((chip) => {
        const match = !term || chip.dataset.chip.includes(term);
        const extraHidden = !term && chip.classList.contains('is-extra') && !box.classList.contains('is-expanded');
        chip.hidden = !match || extraHidden;
        if (!chip.hidden) visible++;
      });
      if (more) more.hidden = !!term || box.classList.contains('is-expanded');
      if (empty) empty.hidden = !term || visible > 0;
    };

    if (more) more.addEventListener('click', () => {
      box.classList.add('is-expanded');
      more.setAttribute('aria-expanded', 'true');
      filterChips();
    });
    input.addEventListener('input', filterChips);
    form.addEventListener('submit', (e) => {
      const term = input.value.trim();
      if (!term) { e.preventDefault(); return; }
      // Exactly one matching chip: go straight to that sub-category.
      const hits = chips.filter((c) => !c.hidden);
      if (hits.length === 1 && hits[0].dataset.chip === term.toLowerCase()) {
        e.preventDefault();
        window.location.href = hits[0].href;
        return;
      }
      q.value = scope ? `${term} AND ${scope}` : term;
    });
    filterChips();
  });

  /* ---------- Collection: filters & sorting ---------- */
  const facetToggle = document.querySelector('[data-facets-toggle]');
  if (facetToggle) {
    facetToggle.addEventListener('click', () => {
      const facets = document.querySelector('[data-facets]');
      const on = !facets.classList.contains('is-open');
      facets.classList.toggle('is-open', on);
      facetToggle.setAttribute('aria-expanded', String(on));
    });
  }
  document.querySelectorAll('[data-facets-form]').forEach((form) => {
    form.addEventListener('change', () => form.submit());
  });
  const sort = document.querySelector('[data-sort]');
  if (sort) {
    sort.addEventListener('change', () => {
      const url = new URL(window.location.href);
      url.searchParams.set('sort_by', sort.value);
      url.searchParams.delete('page');
      window.location.href = url.toString();
    });
  }
})();
