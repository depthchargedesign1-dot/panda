// Offline preview: renders the real theme Liquid with mock store data into static HTML.
// Usage: NODE_PATH=<dir with liquidjs> node tools/preview/render.mjs <outDir>
// This is a design/QA aid only — Shopify-specific objects are approximated.
import { Liquid, Tag } from 'liquidjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(here, '../..');
const THEME = path.join(ROOT, 'theme');
const OUT = path.resolve(process.argv[2] || path.join(ROOT, 'preview/site'));
const data = JSON.parse(fs.readFileSync(path.join(here, 'data.json'), 'utf8'));
fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });
for (const f of fs.readdirSync(path.join(THEME, 'assets'))) fs.copyFileSync(path.join(THEME, 'assets', f), path.join(OUT, 'assets', f));

const locale = JSON.parse(fs.readFileSync(path.join(THEME, 'locales/en.default.json'), 'utf8'));
const settingsSchema = JSON.parse(fs.readFileSync(path.join(THEME, 'config/settings_schema.json'), 'utf8'));

// `globals` mirrors Shopify, where settings/routes are visible inside {% render %} snippets.
const engine = new Liquid({ root: [path.join(THEME, 'snippets')], extname: '.liquid', strictFilters: true, jsTruthy: false, globals: {} });

/* ---------------- helpers ---------------- */
const kw = (args) => Object.fromEntries(args.filter(Array.isArray));
const money = (c) => '£' + (Number(c || 0) / 100).toFixed(2);

function schemaOf(file) {
  const src = fs.readFileSync(file, 'utf8');
  const m = src.match(/{%-?\s*schema\s*-?%}([\s\S]*?){%-?\s*endschema\s*-?%}/);
  return m ? JSON.parse(m[1]) : {};
}
function defaults(list) {
  const out = {};
  for (const s of list || []) if (s.id) out[s.id] = s.default !== undefined ? s.default : (s.type === 'checkbox' ? false : null);
  return out;
}

const fonts = {
  type_heading_font: { family: 'Poppins', fallback_families: 'sans-serif', weight: 700 },
  type_body_font: { family: 'Nunito Sans', fallback_families: 'sans-serif', weight: 400 }
};
const settings = {};
for (const group of settingsSchema) Object.assign(settings, defaults(group.settings));
Object.assign(settings, fonts);

engine.options.globals.settings = settings;

/* menus */
const toLinks = (items) => (items || []).map((i) => ({ title: i.title, url: i.url, links: toLinks(i.items) }));
const linklists = {
  'foxy-mega-menu': { title: 'Foxy Mega Menu', links: toLinks(data.menu) },
  'main-menu': { title: 'Shop', links: toLinks(data.menu.slice(0, 6).map((m) => ({ title: m.title, url: m.url }))) },
  information: { title: 'Help', links: toLinks([{ title: 'Contact us', url: '#' }, { title: 'FAQs', url: '#' }, { title: 'Delivery', url: '#' }, { title: 'Track my order', url: '#' }]) },
  'about-us-menu': { title: 'About', links: toLinks([{ title: 'About Foxy Printing', url: '#' }, { title: 'Our printers', url: '#' }, { title: 'Trade & wholesale', url: '#' }, { title: 'Blog', url: '#' }]) },
  footer: { title: 'Legal', links: toLinks([{ title: 'Privacy policy', url: '#' }, { title: 'Terms of service', url: '#' }, { title: 'Refund policy', url: '#' }]) }
};

/* products & collections */
const products = data.products.map((p, i) => ({ ...p, id: 1000 + i }));
const byHandle = Object.fromEntries(products.map((p) => [p.handle, p]));
const collections = Object.fromEntries(Object.entries(data.collections).map(([handle, c], i) => [handle, {
  id: i + 3, handle, title: c.title, url: 'collection.html', description: c.description || '',
  products: c.products.map((h) => byHandle[h]).filter(Boolean), products_count: c.products.length,
  all_products_count: c.products.length, image: null,
  sort_options: [{ value: 'best-selling', name: 'Best selling' }, { value: 'price-ascending', name: 'Price, low to high' }, { value: 'created-descending', name: 'Newest' }],
  default_sort_by: 'best-selling', filters: c.filters || []
}]));

function resolveSetting(def, value) {
  if (value === undefined || value === null || value === '') return value;
  if (def && def.type === 'link_list') return linklists[value] || null;
  if (def && def.type === 'collection') return collections[value] || null;
  return value;
}

/* ---------------- filters ---------------- */
function translate(key, args) {
  let v = key.split('.').reduce((o, k) => (o ? o[k] : undefined), locale);
  const vars = kw(args);
  if (v && typeof v === 'object') v = vars.count === 1 ? v.one : v.other;
  if (typeof v !== 'string') return key;
  return v.replace(/{{\s*(\w+)\s*}}/g, (_, k) => (vars[k] !== undefined ? vars[k] : ''));
}
engine.registerFilter('t', (key, ...args) => translate(key, args));
engine.registerFilter('money', money);
engine.registerFilter('money_without_currency', (c) => (Number(c || 0) / 100).toFixed(2));
engine.registerFilter('image_url', (img) => (img && typeof img === 'object' ? img.src : img) || '');
engine.registerFilter('image_tag', (src, ...args) => {
  const a = kw(args);
  const attrs = Object.entries(a).filter(([k]) => !['widths', 'sizes'].includes(k)).map(([k, v]) => `${k}="${String(v ?? '').replace(/"/g, '&quot;')}"`).join(' ');
  return `<img src="${src}" ${attrs}>`;
});
engine.registerFilter('asset_url', (n) => 'assets/' + n);
engine.registerFilter('stylesheet_tag', (u) => `<link rel="stylesheet" href="${u}">`);
engine.registerFilter('placeholder_svg_tag', (_n, cls) => `<svg class="${cls || ''}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100"/></svg>`);
let fontImported = false;
engine.registerFilter('font_face', () => {
  if (fontImported) return '';
  fontImported = true;
  return "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700;800&family=Nunito+Sans:wght@400;700;800&display=swap');";
});
engine.registerFilter('font_modify', (f) => f);
engine.registerFilter('payment_type_svg_tag', (t) => `<span style="display:inline-block;background:#fff;color:#1D1240;border-radius:4px;padding:2px 6px;font-size:11px;font-weight:800">${t}</span>`);
engine.registerFilter('default_pagination', () => '');
engine.registerFilter('format_code', (c) => c);
engine.registerFilter('default_errors', () => '');
engine.registerFilter('format_address', (a) => a);
engine.registerFilter('handle', (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''));

/* ---------------- tags ---------------- */
engine.registerTag('schema', class extends Tag {
  constructor(token, remain, liquid) {
    super(token, remain, liquid);
    while (remain.length) { const t = remain.shift(); if (t.name === 'endschema') return; }
  }
  * render() { return ''; }
});
for (const [name, end] of [['form', 'endform'], ['paginate', 'endpaginate']]) {
  engine.registerTag(name, class extends Tag {
    constructor(token, remain, liquid) {
      super(token, remain, liquid);
      this.args = token.args;
      this.tpls = [];
      const stream = liquid.parser.parseStream(remain)
        .on('template', (tpl) => this.tpls.push(tpl))
        .on(`tag:${end}`, () => stream.stop())
        .on('end', () => { throw new Error(`tag ${token.getText()} not closed`); });
      stream.start();
    }
    * render(ctx, emitter) {
      if (name === 'paginate') {
        ctx.push({ paginate: { pages: 1, current_page: 1, parts: [] } });
        yield this.liquid.renderer.renderTemplates(this.tpls, ctx, emitter);
        ctx.pop();
      } else {
        ctx.push({ form: { posted_successfully: false, errors: null } });
        emitter.write('<form method="post" action="#">');
        yield this.liquid.renderer.renderTemplates(this.tpls, ctx, emitter);
        emitter.write('</form>');
        ctx.pop();
      }
    }
  });
}
engine.registerTag('sections', class extends Tag {
  constructor(token, remain, liquid) { super(token, remain, liquid); this.group = token.args.replace(/['"]/g, '').trim(); }
  * render(ctx, emitter) {
    const group = JSON.parse(fs.readFileSync(path.join(THEME, 'sections', this.group + '.json'), 'utf8'));
    const globals = ctx.getAll();
    for (const id of group.order) emitter.write(yield renderSection(id, group.sections[id], globals));
  }
});

/* ---------------- section rendering ---------------- */
async function renderSection(id, conf, globals) {
  const file = path.join(THEME, 'sections', conf.type + '.liquid');
  const schema = schemaOf(file);
  const defs = Object.fromEntries((schema.settings || []).map((s) => [s.id, s]));
  const sectionSettings = { ...defaults(schema.settings), ...(conf.settings || {}) };
  for (const k of Object.keys(sectionSettings)) sectionSettings[k] = resolveSetting(defs[k], sectionSettings[k]);
  const blocks = (conf.block_order || []).map((bid) => {
    const b = conf.blocks[bid];
    const bschema = (schema.blocks || []).find((x) => x.type === b.type) || {};
    const bdefs = Object.fromEntries((bschema.settings || []).map((s) => [s.id, s]));
    const bs = { ...defaults(bschema.settings), ...(b.settings || {}) };
    for (const k of Object.keys(bs)) bs[k] = resolveSetting(bdefs[k], bs[k]);
    return { id: bid, type: b.type, settings: bs, shopify_attributes: '' };
  });
  const src = fs.readFileSync(file, 'utf8');
  const html = await engine.parseAndRender(src, { ...globals, section: { id, settings: sectionSettings, blocks } });
  return `<div id="shopify-section-${id}" class="shopify-section">${html}</div>`;
}

async function renderPage(templateName, extra, outName, overrides = {}) {
  const tpl = JSON.parse(fs.readFileSync(path.join(THEME, 'templates', templateName + '.json'), 'utf8'));
  for (const [sid, o] of Object.entries(overrides)) Object.assign(tpl.sections[sid].settings ||= {}, o);
  const globals = {
    settings, linklists, collections, shop: { name: 'Foxy Printing', money_format: '£{{amount}}', customer_accounts_enabled: true, enabled_payment_types: ['visa', 'master', 'american_express', 'paypal', 'apple_pay', 'google_pay'], description: 'Personalised printed gifts' },
    routes: { root_url: 'index.html', cart_url: '#', cart_add_url: '#', search_url: '#', account_url: '#', account_login_url: '#', all_products_collection_url: 'collection.html', account_register_url: '#' },
    request: { locale: { iso_code: 'en' }, page_type: templateName.split('.')[0], origin: '' },
    cart: { item_count: 2, currency: { iso_code: 'GBP' } },
    template: { name: templateName.split('.')[0], suffix: templateName.split('.')[1] || null },
    page_title: extra.page_title || 'Foxy Printing', canonical_url: '', content_for_header: '', customer: null,
    ...extra
  };
  let body = '';
  for (const id of tpl.order) body += await renderSection(id, tpl.sections[id], globals);
  fontImported = false;
  const layout = fs.readFileSync(path.join(THEME, 'layout/theme.liquid'), 'utf8');
  let html = await engine.parseAndRender(layout, { ...globals, content_for_layout: body });
  html = html.replace(/href="\/collections\/[^"]*"/g, 'href="collection.html"');
  fs.writeFileSync(path.join(OUT, outName), html);
  console.log('wrote', outName, (html.length / 1024).toFixed(0) + 'KB');
}

/* ---------------- pages ---------------- */
await renderPage('index', { page_title: 'Personalised Printed Gifts' }, 'index.html', {
  bestsellers: { collection: 'trending' }, christmas_products: { collection: 'christmas' }
});
const col = collections.trending;
await renderPage('collection', { collection: col, page_title: col.title }, 'collection.html');
for (const [handle, out] of Object.entries(data.productPages)) {
  const product = byHandle[handle];
  await renderPage(product.template || 'product.personalised', { product, collection: collections.trending, page_title: product.title }, out,
    { related: { collection: 'trending' } });
}
