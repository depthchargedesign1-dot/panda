# Ryedale Removals: website

A complete, ready-to-launch website for a removal company based in **Helmsley, North Yorkshire**, covering everywhere within **30 miles**.

This rebuilds the "Ryedale Removals" template from `Dropbox/AI DESIGNS 2026/Ryedale Removals`. Every service in that template is kept, with new copy and real photography:

| Original template page | New page(s) |
|---|---|
| Domestic removals | `house-removals.html` |
| International removals | `long-distance-removals.html` (UK-wide + European) |
| Special furnitures / heavy furniture | `specialist-items.html` (pianos, antiques, heavy items) |
| Reassembly & packing | `packing-services.html` + `furniture-reassembly.html` |
| Deposit / long & short term storage | `storage.html` |
| Cleaning | `cleaning.html` |
| The fleet (small van open/covered, medium van, truck) | `fleet.html` + `man-and-van.html` |
| Cargo service | `office-removals.html` (office, commercial, holiday lets) |
| Quotation wizard | `quote.html` (5-step quote form) |
| About us | `about.html` |
| Tips and FAQ | `tips-faq.html` |
| Blog / blog post | `guides.html` + 3 full articles |
| Contact us | `contact.html` |

It also adds:
- an **Areas we cover** page with a map drawn from real coordinates
- **12 town landing pages** (York, Malton, Pickering, Whitby, Scarborough and more), each with its own local copy
- privacy, terms, thank-you and 404 pages
- a sitemap, robots.txt and full SEO markup

## What's in the folder

```
ryedale-removals/
├── build.py        ← all page copy + business details; regenerates the site
├── README.md
└── site/           ← THE WEBSITE: upload the contents of this folder
    ├── *.html      (36 pages)
    ├── send.php    (form handler)
    ├── sitemap.xml, robots.txt, site.webmanifest, .htaccess
    └── assets/ (css, js, img)
```

The site is plain HTML, CSS and JavaScript. It has no framework or build step and works on any host.

## Before going live: replace the placeholders

Open `build.py`, edit the `CONFIG` block at the top, then run `python3 build.py`. That updates every page at once.

| Setting | Placeholder | Notes |
|---|---|---|
| `phone` / `phone_link` | 01632 960 123 | Ofcom-reserved fictional number. It never connects. |
| `mobile` / `mobile_link` | 07700 900 123 | Ofcom-reserved fictional number |
| `email` | hello@ryedaleremovals.co.uk | Also set it in `site/send.php` (`$TO`, `$FROM`) |
| `domain` | https://www.ryedaleremovals.co.uk | Used for canonical URLs, the sitemap and social sharing |
| `street` | blank | Add a yard/unit address if there is one |
| `hours` | Mon–Fri 8–6, Sat 8–4 | |
| `facebook` / `instagram` | blank | Links appear in the footer once filled in |
| `radius_miles` | 30 | Changing it re-filters towns and redraws the map |

**Check the claims match the real business.** The copy says the company offers fixed-price quotes, goods-in-transit and public liability insurance, a secure storage facility, cleaning, European moves through partners, and Saturday working. Remove anything the business doesn't do: edit the `SERVICES` list in `build.py` and rebuild.

There are **no fake reviews or star ratings** on the site. Once the business has genuine Google reviews, add a reviews section or widget.

## Forms

The quote and contact forms post to `send.php`. It works on any standard PHP host (cPanel, 20i, Krystal, IONOS and so on) and includes a hidden spam trap. Set `$TO` and `$FROM` at the top of the file.

**No PHP?** (For example on Netlify, Cloudflare Pages or GitHub Pages.) Create a free form at formspree.io, put its URL in `CONFIG["form_action"]` and rebuild. The forms already send `Accept: application/json`, which Formspree expects.

## Hosting

Upload everything **inside `site/`** to the web root (`public_html`). The included `.htaccess` sets the custom 404 page, compression and caching on Apache hosts.

After launch:
1. Submit `https://yourdomain/sitemap.xml` in Google Search Console.
2. Create or claim the Google Business Profile with the same name, phone and area. Use a service-area business set to a 30-mile radius.

## Photos

The 13 photos were licensed from Freepik/Magnific on a Premium plan, so no attribution is needed. The licence allows commercial use on this website. For a handover, the buyer should ideally swap in their own photos of their vans and crew: replace the files in `site/assets/img/` and keep the same names. Each image has `-1600.jpg`, `-1600.webp` and `-800.webp` versions.

## Rebranding

Colours and fonts are CSS variables at the top of `site/assets/css/style.css`. The logo is the `LOGO_SVG` constant in `build.py`.
