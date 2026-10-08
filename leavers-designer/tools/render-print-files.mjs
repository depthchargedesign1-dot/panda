#!/usr/bin/env node
/*
 * Server-side print files: renders the 300 dpi PNGs for a leavers design without opening a browser window.
 *
 *   node tools/render-print-files.mjs "<_Print files link or design code>" [--out dir] [--dpi 300] [--prefix order1234]
 *   node tools/render-print-files.mjs --order order.json [--out dir]     # Shopify order JSON (REST or webhook payload)
 *
 * Uses Playwright's Chromium with the same engine the website uses, so files match the customer's proof exactly.
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
const opt = (name, def) => { const i = args.indexOf('--' + name); return i >= 0 ? args.splice(i, 2)[1] : def; };
const out = opt('out', 'print-files');
const dpi = parseInt(opt('dpi', '300'), 10);
const prefix = opt('prefix', 'leavers');
const orderFile = opt('order', null);

const jobs = [];
if (orderFile) {
  const order = JSON.parse(fs.readFileSync(orderFile, 'utf8'));
  const o = order.order || order;
  for (const li of o.line_items || []) {
    const props = Array.isArray(li.properties) ? Object.fromEntries(li.properties.map(p => [p.name, p.value])) : (li.properties || {});
    const link = props['_Print files'];
    if (link) jobs.push({ code: link, prefix: `order${String(o.name || o.order_number || '').replace(/\D/g, '')}_line${li.id}_x${li.quantity}` });
  }
} else if (args[0]) {
  jobs.push({ code: args[0], prefix });
}
if (!jobs.length) {
  console.error('Usage: render-print-files.mjs "<print files link | design code>" [--out dir] [--dpi 300]\n       render-print-files.mjs --order order.json');
  process.exit(1);
}

fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(pathToFileURL(path.join(here, '../demo/print-studio.html')).href);
await page.waitForFunction(() => window.LeaversEngine);

for (const job of jobs) {
  const files = await page.evaluate(async ({ code, dpi, prefix }) => {
    const E = window.LeaversEngine;
    const d = await E.decode(code);
    await E.loadFonts(d);
    await document.fonts.ready;
    const rendered = await E.renderPrintFiles(d, { dpi, prefix });
    const toB64 = async blob => {
      const bytes = new Uint8Array(await blob.arrayBuffer());
      let s = '';
      for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
      return btoa(s);
    };
    return Promise.all(rendered.map(async f => ({ name: f.filename, w: f.width, h: f.height, b64: await toB64(f.blob) })));
  }, { code: job.code, dpi, prefix: job.prefix });
  for (const f of files) {
    const file = path.join(out, f.name);
    fs.writeFileSync(file, Buffer.from(f.b64, 'base64'));
    console.log(`${file}  ${f.w}x${f.h}px @ ${dpi}dpi`);
  }
}
await browser.close();
