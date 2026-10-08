const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'); const path = require('path');
const [,, jsPath, blanks, fontsDir, outDir] = process.argv;
const zone = JSON.parse(fs.readFileSync(path.join(__dirname, 'zone.json'), 'utf8'));
const cfg = { mockup: 'photo', title: 'Personalised Number Plate Mug – Any Name or Text – Custom Reg Gift – 11oz Ceramic', productType: 'Mugs', tags: [],
  baseImage: zone.bases.GB + '&width=1200', useBaseImage: true, zone, fonts: ['Baloo 2'], colours: ['#111111'] };
const html = `<!doctype html><html><head><style>@font-face{font-family:"Bebas Neue";src:url(/fonts/BebasNeue-Regular.ttf)}</style></head><body>
<div data-product-section><canvas width="1000" height="1000" data-personaliser-canvas style="border:1px solid #ccc"></canvas>
<div class="field"><input data-field data-field-kind="text" data-field-label="Your plate text (max 8 characters)" placeholder="Your plate text (max 8 characters)" maxlength="40"></div>
<div class="field"><input data-field data-field-kind="text" data-field-label="Dealer line on the plate (optional, e.g. Dad’s Garage)" placeholder="x" maxlength="40"></div>
</div><script type="application/json" data-personaliser-config>${JSON.stringify(cfg)}</script><script src="/personaliser.js"></script></body></html>`;
const cases = [['00-empty','',''],['01-BOB','BOB',''],['02-DAD-50','DAD 50',''],['03-GRANDAD1','GRANDAD1',''],['04-max-8-WWWWWWWW','WWWWWWWW',''],
  ['05-max-8-MMMM-MMMM','MMMM MMM',''],['06-GRANDAD1-dealer','GRANDAD1','Dad’s Garage'],['07-BOB-Wales','BOB','','Wales'],['08-DAD-50-NI','DAD 50','','Northern Ireland'],['09-lowercase-dav3','dav3 5!','']];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1020, height: 1020 } });
  let gf = 0;
  await p.route('**/*', async (r) => {
    const u = r.request().url();
    if (u.startsWith('http://t/') && u.endsWith('/')) return r.fulfill({ contentType: 'text/html', body: html });
    if (u.endsWith('/personaliser.js')) return r.fulfill({ contentType: 'application/javascript', body: fs.readFileSync(jsPath) });
    if (u.includes('/fonts/')) return r.fulfill({ contentType: 'font/ttf', body: fs.readFileSync(path.join(fontsDir, path.basename(u))) });
    if (u.startsWith('https://fonts.googleapis.com/css2')) { gf++; const w = /wght@600/.test(u) ? 'SemiBold' : 'Bold';
      return r.fulfill({ contentType: 'text/css', body: `@font-face{font-family:"Barlow Condensed";font-weight:${/wght@600/.test(u)?600:700};src:url(http://t/fonts/BarlowCondensed-${w}.ttf)}` }); }
    if (u.includes('cdn.shopify.com')) { const m = u.match(/preview-blank-(\w+)\.jpg/); if (!m) return r.fulfill({ contentType: 'image/jpeg', body: fs.readFileSync('/tmp/claude-0/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/scratchpad/plate/foxyprinting-rebrand/exports/any-name-number-plate-mug/mockups/FOXY-SUB-PNPMANOT-1-GB.jpg') }); return r.fulfill({ contentType: 'image/jpeg', body: fs.readFileSync(path.join(blanks, `FOXY-SUB-PNPMANOT-preview-blank-${m[1]}.jpg`)) }); }
    return r.abort();
  });
  await p.goto('http://t/');
  await p.waitForTimeout(800);
  for (const [name, text, dealer, country] of cases) {
    await p.evaluate(({ text, dealer, country }) => {
      const ins = document.querySelectorAll('[data-field]');
      ins[0].value = text; ins[0].dispatchEvent(new Event('input'));
      ins[1].value = dealer; ins[1].dispatchEvent(new Event('input'));
      document.dispatchEvent(new CustomEvent('foxy:variant-change', { detail: { options: [country || 'GB'], variant: { featured_media: { preview_image: { src: 'https://cdn.shopify.com/mug-with-sample-text.jpg' } } } } }));
    }, { text, dealer, country });
    await p.waitForTimeout(500);
    await p.locator('canvas').screenshot({ path: path.join(outDir, name + '.png') });
  }
  console.log('google font css requests', gf);
  await b.close();
})();
