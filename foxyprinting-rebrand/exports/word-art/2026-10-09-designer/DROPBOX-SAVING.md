# Word art orders: saving the print file to Dropbox with the order number

Every word art order line now carries its print-ready file. When the customer adds to basket, the designer makes the PNG at print size (A4–A1, 3 mm bleed, up to 300 dpi) and Shopify stores it with the line as the hidden property `_Print file`, which is a `https://cdn.shopify.com/...` link. The order also shows Name, Words, Colours, Font and Layout code, and `_Print spec` gives the size, dpi and pixels.

The goal: `/WORD ART ORDERS/<order number> - <product title> - <size>.png` appears in Dropbox by itself.

## Options

| | How it works | Good | Not so good |
|---|---|---|---|
| **A. Shopify Flow (recommended)** | Flow's "Order created" trigger loops over the line items. Any line with a `_Print file` sends one HTTP request to Dropbox's `files/save_url`, and Dropbox downloads the file from Shopify straight into the folder. | Free, built into Shopify, runs within seconds of every order, works when no one is at a computer, and needs no Claude session. | A one-off setup: a small Dropbox app plus its key, pasted into Flow by you. |
| B. Zapier / Make | "Shopify: New order" → "Dropbox: Upload file" from the URL. | No code, easy to read. | Monthly fee once you're past the free tasks; one more account to look after. |
| C. Scheduled Claude routine | A routine checks new orders every hour and saves the files. | Nothing to set up in Dropbox. | The Dropbox connector can't save binary files or save from a link, so it would still need a Dropbox key in the environment. It's slower, costs usage, and depends on Claude being available. |

**Recommendation: A (Shopify Flow).** It's the most reliable and costs nothing.

## Setting up option A (about 15 minutes, done by you; never paste keys into chat)

1. **Make a Dropbox app.** Go to https://www.dropbox.com/developers/apps → *Create app* → *Scoped access* → *Full Dropbox* → name it `Foxy Flow`. On the **Permissions** tab, tick `files.content.write` and press Submit.
2. **Get a long-life refresh token.** Dropbox access keys run out after 4 hours, so Flow uses a refresh token to get a fresh key on each order. In the app's Settings, note the *App key* and *App secret*. Then open this link (put in your app key), allow it, and copy the code:
   `https://www.dropbox.com/oauth2/authorize?client_id=APP_KEY&response_type=code&token_access_type=offline`
   Swap the code for a refresh token once (Terminal / PowerShell):
   `curl https://api.dropboxapi.com/oauth2/token -d code=THE_CODE -d grant_type=authorization_code -u APP_KEY:APP_SECRET`
   Keep the `refresh_token` from the reply somewhere safe. It doesn't expire.
3. **Build the Flow** (Shopify admin → Apps → Flow → Create workflow):
   - Trigger: **Order created**.
   - Action: **Send HTTP request** (get a fresh Dropbox key)
     - Method `POST`, URL `https://api.dropboxapi.com/oauth2/token`
     - Header `Content-Type: application/x-www-form-urlencoded`
     - Body: `grant_type=refresh_token&refresh_token=REFRESH_TOKEN&client_id=APP_KEY&client_secret=APP_SECRET`
       (use Flow's *Secrets* for these values if your Flow version offers them)
   - Action: **Run code**, which reads `access_token` from that reply and lists each line with a print file:
     ```js
     export default function main(input) {
       const token = JSON.parse(input.sendHttpRequest.body).access_token;
       const files = [];
       for (const li of input.order.lineItems) {
         const url = (li.customAttributes || []).find(a => a.key === '_Print file')?.value || '';
         if (!url.startsWith('https://')) continue;
         const ext = url.split('?')[0].toLowerCase().endsWith('.jpg') ? '.jpg' : '.png';
         const clean = s => String(s || '').replace(/[\\/:*?"<>|]/g, '-').trim();
         files.push({
           path: `/WORD ART ORDERS/${clean(input.order.name.replace('#', ''))} - ${clean(li.title)} - ${clean(li.variantTitle)}${ext}`,
           url
         });
       }
       return { token, files };
     }
     ```
   - **For each** item in `runCode.files` → **Send HTTP request**
     - Method `POST`, URL `https://api.dropboxapi.com/2/files/save_url`
     - Headers `Authorization: Bearer {{runCode.token}}` and `Content-Type: application/json`
     - Body `{"path": "{{filesForeachitem.path}}", "url": "{{filesForeachitem.url}}"}`
4. Turn the workflow on. When you're happy, place one test order (a 100% discount code is easiest) and check that the file lands in `/WORD ART ORDERS/`. I'll only place a test order myself if you ask me to.

If the same order line has quantity 2, one file is saved (one design, printed twice). Two different designs in one order make two files.

## If a file is ever missing
The order still shows Name, Words, Colours, Font and the **Layout code** (e.g. `WA1.s75ax0.original.anton`). Together with the product, those identify the exact layout, and `_Print spec` says what size and dpi was made. A small "re-make from Layout code" page for production is on the to-do list.
