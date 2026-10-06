// render.js - turn the mugkit HTML/SVG page into a 300 dpi PNG plus PDF and mirrored PDF.
// usage: node render.js page.html widthMM heightMM out.png out.pdf out-mirrored.pdf
// Needs the playwright package (global is fine: NODE_PATH=$(npm root -g)).
const { chromium } = require("playwright");
const fs = require("fs");

(async () => {
  const [html, wmm, hmm, png, pdf, mpdf] = process.argv.slice(2);
  const w = parseFloat(wmm), h = parseFloat(hmm);
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const browser = await chromium.launch(opts);
  const scale = 300 / 96;
  const cssW = (w / 25.4) * 96, cssH = (h / 25.4) * 96;
  const page = await browser.newPage({
    viewport: { width: Math.ceil(cssW), height: Math.ceil(cssH) },
    deviceScaleFactor: scale,
  });
  await page.goto("file://" + html);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: png, clip: { x: 0, y: 0, width: cssW, height: cssH } });
  const pdfOpts = { width: `${w}mm`, height: `${h}mm`, printBackground: true,
                    margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: "1" };
  await page.pdf({ path: pdf, ...pdfOpts });
  await page.evaluate(() => document.body.classList.add("m"));
  await page.pdf({ path: mpdf, ...pdfOpts });
  await browser.close();
  for (const f of [png, pdf, mpdf]) if (!fs.existsSync(f)) { console.error("missing " + f); process.exit(1); }
})().catch((e) => { console.error(e); process.exit(1); });
