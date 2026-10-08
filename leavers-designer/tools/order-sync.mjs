#!/usr/bin/env node
/*
 * Leavers order sync: finds new Shopify orders with leavers hoodies/jackets, renders their 300 dpi print files
 * and saves them to Dropbox:
 *
 *   /Leavers Hoodie and Jackets ORDERS/<order number>/
 *       <order>_1of3_<garment>_<colour>_<size>_x<qty>_back.png      (one PNG per print area, per hoodie line)
 *       <order>_1of3_..._proof.jpg                                   (front + back mockup to check against)
 *       <order>_order-details.txt                                    (customer, every line, every name)
 *       <order>_school-logo.<ext>                                    (customer's original logo, if any)
 *
 * When everything for an order is saved, the order is tagged "leavers-files-saved" in Shopify so it is never done twice.
 * Runs every 15 minutes from .github/workflows/leavers-print-files.yml; can also be run by hand:
 *
 *   node leavers-designer/tools/order-sync.mjs [--order 1042] [--dry-run]
 *
 * Environment:
 *   SHOPIFY_SHOP              naughty-but-nice-mugs.myshopify.com
 *   SHOPIFY_ADMIN_TOKEN       Admin API access token (read_orders, write_orders)
 *     or SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET   (Dev Dashboard app; token fetched with client credentials)
 *   DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN   (or DROPBOX_TOKEN for a quick manual run)
 *   LEAVERS_DROPBOX_FOLDER    default "/Leavers Hoodie and Jackets ORDERS"
 *   LEAVERS_LOOKBACK_DAYS     default 5 (orders older than this are not looked at)
 *   LEAVERS_DPI               default 300
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch {
  ({ chromium } = await import(pathToFileURL(path.join(process.execPath, '../../lib/node_modules/playwright/index.mjs')).href));
}

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const flag = name => args.includes('--' + name);
const opt = (name, def) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : def; };

const env = process.env;
const SHOP = (env.SHOPIFY_SHOP || 'naughty-but-nice-mugs.myshopify.com').replace(/^https?:\/\//, '').replace(/\/$/, '');
const API = env.SHOPIFY_API_VERSION || '2026-07';
const ROOT = env.LEAVERS_DROPBOX_FOLDER || '/Leavers Hoodie and Jackets ORDERS';
const DONE_TAG = 'leavers-files-saved';
const LOOKBACK = parseInt(env.LEAVERS_LOOKBACK_DAYS || '5', 10);
const DPI = parseInt(env.LEAVERS_DPI || '300', 10);
const ONLY = opt('order', null);
const DRY = flag('dry-run');

const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);

/* ---------------------------------------------------------------- Shopify */

async function shopifyToken() {
  if (env.SHOPIFY_ADMIN_TOKEN) return env.SHOPIFY_ADMIN_TOKEN;
  if (!env.SHOPIFY_CLIENT_ID || !env.SHOPIFY_CLIENT_SECRET) throw new Error('Set SHOPIFY_ADMIN_TOKEN, or SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET');
  const r = await fetch(`https://${SHOP}/admin/oauth/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'client_credentials', client_id: env.SHOPIFY_CLIENT_ID, client_secret: env.SHOPIFY_CLIENT_SECRET })
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.access_token) throw new Error(`Shopify token request failed (${r.status}): ${JSON.stringify(j)}`);
  return j.access_token;
}

let shopToken;
async function gql(query, variables) {
  shopToken = shopToken || await shopifyToken();
  for (let attempt = 0; ; attempt++) {
    const r = await fetch(`https://${SHOP}/admin/api/${API}/graphql.json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': shopToken },
      body: JSON.stringify({ query, variables })
    });
    const j = await r.json().catch(() => ({}));
    const throttled = r.status === 429 || (j.errors || []).some(e => e.extensions && e.extensions.code === 'THROTTLED');
    if (throttled && attempt < 5) { await new Promise(res => setTimeout(res, 2000 * (attempt + 1))); continue; }
    if (!r.ok || j.errors) throw new Error(`Shopify API error (${r.status}): ${JSON.stringify(j.errors || j)}`);
    return j.data;
  }
}

const ORDERS = `query($q: String!, $after: String) {
  orders(first: 50, after: $after, query: $q, sortKey: CREATED_AT) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id name tags createdAt cancelledAt displayFinancialStatus
      customer { displayName }
      email
      lineItems(first: 100) { nodes { name quantity variantTitle customAttributes { key value } } }
    }
  }
}`;

async function leaversOrders() {
  const since = new Date(Date.now() - LOOKBACK * 864e5).toISOString().slice(0, 10);
  const q = ONLY ? `name:${ONLY.replace(/^#/, '')}` : `created_at:>=${since} -tag:${DONE_TAG}`;
  const out = [];
  let after = null;
  do {
    const d = await gql(ORDERS, { q, after });
    for (const o of d.orders.nodes) {
      if (o.cancelledAt) continue;
      if (!ONLY && o.tags.includes(DONE_TAG)) continue;
      const lines = o.lineItems.nodes
        .map(li => ({ ...li, props: Object.fromEntries(li.customAttributes.map(a => [a.key, a.value])) }))
        .filter(li => li.props['_Print files']);
      if (lines.length) out.push({ ...o, lines });
    }
    after = d.orders.pageInfo.hasNextPage ? d.orders.pageInfo.endCursor : null;
  } while (after);
  return out;
}

async function markDone(order) {
  const d = await gql(`mutation($id: ID!, $tags: [String!]!) { tagsAdd(id: $id, tags: $tags) { userErrors { message } } }`, { id: order.id, tags: [DONE_TAG] });
  const errs = d.tagsAdd.userErrors;
  if (errs.length) throw new Error('Could not tag order: ' + errs.map(e => e.message).join('; '));
}

/* ---------------------------------------------------------------- Dropbox */

let dbxToken;
async function dropboxToken() {
  if (dbxToken) return dbxToken;
  if (env.DROPBOX_REFRESH_TOKEN) {
    const r = await fetch('https://api.dropboxapi.com/oauth2/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: env.DROPBOX_REFRESH_TOKEN, client_id: env.DROPBOX_APP_KEY || '', client_secret: env.DROPBOX_APP_SECRET || '' })
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || !j.access_token) throw new Error(`Dropbox token request failed (${r.status}): ${JSON.stringify(j)}`);
    return (dbxToken = j.access_token);
  }
  if (env.DROPBOX_TOKEN) return (dbxToken = env.DROPBOX_TOKEN);
  throw new Error('Set DROPBOX_APP_KEY, DROPBOX_APP_SECRET and DROPBOX_REFRESH_TOKEN (or DROPBOX_TOKEN)');
}

// Dropbox-API-Arg is an HTTP header, so anything outside ASCII must be \u-escaped.
const headerJSON = o => JSON.stringify(o).replace(/[\u007f-￿]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));

async function upload(dropboxPath, bytes) {
  if (DRY) { log('  (dry run) would save', dropboxPath, (bytes.length / 1048576).toFixed(1) + ' MB'); return; }
  const token = await dropboxToken();
  const CHUNK = 100 * 1048576;
  const call = (url, arg, body) => fetch(url, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + token, 'Dropbox-API-Arg': headerJSON(arg), 'Content-Type': 'application/octet-stream' },
    body
  }).then(async r => { const t = await r.text(); if (!r.ok) throw new Error(`Dropbox ${url.split('/').pop()} failed (${r.status}): ${t}`); return t ? JSON.parse(t) : {}; });
  const commit = { path: dropboxPath, mode: 'overwrite', autorename: false, mute: true };
  if (bytes.length <= CHUNK) return call('https://content.dropboxapi.com/2/files/upload', commit, bytes);
  // Big files go up in pieces.
  const start = await call('https://content.dropboxapi.com/2/files/upload_session/start', { close: false }, bytes.subarray(0, CHUNK));
  let offset = CHUNK;
  while (bytes.length - offset > CHUNK) {
    await call('https://content.dropboxapi.com/2/files/upload_session/append_v2', { cursor: { session_id: start.session_id, offset }, close: false }, bytes.subarray(offset, offset + CHUNK));
    offset += CHUNK;
  }
  return call('https://content.dropboxapi.com/2/files/upload_session/finish', { cursor: { session_id: start.session_id, offset }, commit }, bytes.subarray(offset));
}

/* ---------------------------------------------------------------- rendering */

const safe = s => String(s || '').replace(/[\\/:*?"<>|#%]+/g, '').replace(/\s+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').slice(0, 40);

async function renderLine(page, code, prefix) {
  return page.evaluate(async ({ code, dpi, prefix }) => {
    const E = window.LeaversEngine;
    const d = await E.decode(code);
    await Promise.all([E.loadFonts(d), E.loadLogo(d), E.loadPhotos(d)]);
    await document.fonts.ready;
    // Never print without the customer's logo: if it can't be loaded, fail so the order is retried next run.
    if (E.usesLogo(d)) {
      const ok = await new Promise(res => {
        const img = new Image(); img.crossOrigin = 'anonymous';
        img.onload = () => res(img.naturalWidth > 0); img.onerror = () => res(false);
        img.src = d.front.logoUrl || '';
      });
      if (!ok) throw new Error('school logo could not be loaded: ' + (d.front.logoUrl || '(no logo uploaded)'));
    }
    const toB64 = async blob => {
      const bytes = new Uint8Array(await blob.arrayBuffer());
      let s = '';
      for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
      return btoa(s);
    };
    const files = await E.renderPrintFiles(d, { dpi, prefix });
    // Proof: back (big) and front side by side on the real garment photo.
    const proof = document.createElement('canvas');
    proof.width = 2400; proof.height = 1400;
    const x = proof.getContext('2d');
    x.fillStyle = '#fff'; x.fillRect(0, 0, proof.width, proof.height);
    ['back', 'front'].forEach((view, i) => {
      const c = document.createElement('canvas'); c.width = 1200; c.height = 1320;
      // _print hides the "Your name" / "YOUR LOGO" placeholders, so the proof shows exactly what is printed.
      E.renderMockup(c, Object.assign({}, d, { _print: true }), view, { quality: 2 });
      x.drawImage(c, i * 1200, 40, 1200, 1320);
    });
    x.fillStyle = '#1D1240'; x.font = '600 34px sans-serif';
    x.fillText(prefix + ' · ' + E.PRODUCTS[d.product].name + ' · ' + E.colourOf(d).name + ' · ' + (d.size || '') + ' · PROOF', 30, 44);
    const proofBlob = await new Promise(res => proof.toBlob(res, 'image/jpeg', 0.88));
    return {
      names: E.cleanNames(d),
      logoUrl: E.usesLogo(d) ? d.front.logoUrl : '',
      product: E.PRODUCTS[d.product].name, colour: E.colourOf(d).name, size: d.size || '',
      files: await Promise.all(files.map(async f => ({ name: f.filename, label: f.label, w: f.width, h: f.height, mm: f.mm, b64: await toB64(f.blob) }))),
      proof: await toB64(proofBlob)
    };
  }, { code, dpi: DPI, prefix });
}

function orderDetails(order, results) {
  const L = [];
  L.push(`ORDER ${order.name}   ${new Date(order.createdAt).toLocaleString('en-GB', { timeZone: 'Europe/London' })}`);
  L.push(`Customer: ${order.customer ? order.customer.displayName : ''} ${order.email ? '<' + order.email + '>' : ''}`);
  L.push(`Payment: ${order.displayFinancialStatus}`);
  L.push('');
  results.forEach((r, i) => {
    L.push(`--- Line ${i + 1} of ${results.length}: ${r.line.name}  x${r.line.quantity}`);
    for (const [k, v] of Object.entries(r.line.props)) if (!k.startsWith('_')) L.push(`  ${k}: ${v}`);
    L.push(`  Print files: ${r.files.map(f => `${f.name} (${f.label}, ${f.mm.w}x${f.mm.h} mm, ${f.w}x${f.h} px @ ${DPI} dpi)`).join('\n               ')}`);
    L.push(`  Re-open in Print Studio: ${r.line.props['_Print files']}`);
    if (r.names.length) {
      L.push(`  Names on the back (${r.names.length}) — check spelling:`);
      r.names.forEach((n, j) => L.push(`    ${String(j + 1).padStart(3)}. ${n}`));
    }
    L.push('');
  });
  return L.join('\r\n');
}

/* ---------------------------------------------------------------- main */

const orders = await leaversOrders();
log(`${orders.length} leavers order${orders.length === 1 ? '' : 's'} to save` + (ONLY ? ` (order ${ONLY})` : ''));
if (!orders.length) process.exit(0);

const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(pathToFileURL(path.join(here, '../demo/print-studio.html')).href);
await page.waitForFunction(() => window.LeaversEngine);

let failed = 0;
for (const order of orders) {
  const num = order.name.replace(/^#/, '');
  const folder = `${ROOT}/${num}`;
  log(`Order ${order.name}: ${order.lines.length} leavers line(s) → ${folder}`);
  try {
    const results = [];
    const logos = new Map();
    for (const [i, line] of order.lines.entries()) {
      const r0 = await page.evaluate(async code => {
        const E = window.LeaversEngine, d = await E.decode(code);
        return { product: E.PRODUCTS[d.product].name, colour: E.colourOf(d).name, size: d.size || '' };
      }, line.props['_Print files']);
      // The engine adds garment, size, print area and personal name to each file name.
      const prefix = [num, `${i + 1}of${order.lines.length}`, safe(r0.colour), `x${line.quantity}`].join('_');
      const r = await renderLine(page, line.props['_Print files'], prefix);
      results.push({ ...r, line });
      for (const f of r.files) {
        const bytes = Buffer.from(f.b64, 'base64');
        await upload(`${folder}/${f.name}`, bytes);
        log(`  saved ${f.name}  ${f.w}x${f.h}px  ${(bytes.length / 1048576).toFixed(1)} MB`);
      }
      await upload(`${folder}/${prefix}_${safe(r0.product)}_${safe(r0.size)}_proof.jpg`, Buffer.from(r.proof, 'base64'));
      if (r.logoUrl && !logos.has(r.logoUrl)) {
        logos.set(r.logoUrl, true);
        const res = await fetch(r.logoUrl);
        if (res.ok) {
          const ext = (r.logoUrl.split('?')[0].match(/\.(png|jpe?g|svg|webp)$/i) || [, 'png'])[1].toLowerCase();
          await upload(`${folder}/${num}_school-logo${logos.size > 1 ? '-' + logos.size : ''}.${ext}`, Buffer.from(await res.arrayBuffer()));
          log('  saved school logo');
        } else console.error(`  could not download logo ${r.logoUrl} (${res.status})`);
      }
    }
    await upload(`${folder}/${num}_order-details.txt`, Buffer.from('﻿' + orderDetails(order, results), 'utf8'));
    if (!DRY) await markDone(order);
    log(`Order ${order.name} done${DRY ? ' (dry run, not tagged)' : ', tagged ' + DONE_TAG}`);
  } catch (e) {
    failed++;
    console.error(`Order ${order.name} FAILED: ${e.message}`);
  }
}
await browser.close();
if (failed) { console.error(`${failed} order(s) failed — they will be retried on the next run.`); process.exit(1); }
