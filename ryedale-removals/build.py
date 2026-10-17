#!/usr/bin/env python3
"""
Ryedale Removals — static site generator.

Edit CONFIG (business details) or any page copy below, then run:

    python3 build.py

Every page in ./site is regenerated. No packages needed beyond Python 3.8+.
The ./site folder is the finished website: upload its contents to any host.
"""
import json
import math
import os
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

# ---------------------------------------------------------------------------
# BUSINESS DETAILS — change these before going live (see README.md)
# The phone numbers below are Ofcom-reserved "drama" numbers that will never
# connect to a real line, so they are safe placeholders.
# ---------------------------------------------------------------------------
CONFIG = {
    "name": "Ryedale Removals",
    "tagline": "Removals & Storage · Helmsley",
    "domain": "https://www.ryedaleremovals.co.uk",
    "phone": "01632 960 123",
    "phone_link": "+441632960123",
    "mobile": "07700 900 123",
    "mobile_link": "+447700900123",
    "email": "hello@ryedaleremovals.co.uk",
    "street": "",  # e.g. "Unit 3, Riccal Drive" — leave blank to show town only
    "town": "Helmsley",
    "county": "North Yorkshire",
    "postcode": "YO62",
    "lat": 54.2465,
    "lng": -1.0611,
    "radius_miles": 30,
    "hours": [
        ("Monday – Friday", "8:00am – 6:00pm"),
        ("Saturday", "8:00am – 4:00pm"),
        ("Sunday", "By arrangement"),
    ],
    "form_action": "send.php",
    "facebook": "",   # full URLs, leave blank to hide
    "instagram": "",
}
C = CONFIG

# ---------------------------------------------------------------------------
# Places within the service area. Distances are calculated (straight line)
# from the Helmsley base, and anything beyond radius_miles is dropped.
# ---------------------------------------------------------------------------
PLACES = [
    # name, lat, lng, major?
    ("Helmsley", 54.2465, -1.0611, True),
    ("Kirkbymoorside", 54.2700, -0.9310, True),
    ("Nawton", 54.2600, -1.0050, False),
    ("Ampleforth", 54.2010, -1.1090, False),
    ("Oswaldkirk", 54.2080, -1.0730, False),
    ("Hovingham", 54.1720, -0.9800, False),
    ("Hutton-le-Hole", 54.3010, -0.9150, False),
    ("Rosedale Abbey", 54.3530, -0.8870, False),
    ("Coxwold", 54.1880, -1.1830, False),
    ("Slingsby", 54.1680, -0.9330, False),
    ("Pickering", 54.2464, -0.7770, True),
    ("Thornton-le-Dale", 54.2350, -0.7210, False),
    ("Malton", 54.1350, -0.7970, True),
    ("Norton", 54.1310, -0.7860, False),
    ("Castle Howard", 54.1210, -0.9060, False),
    ("Sheriff Hutton", 54.0870, -1.0040, False),
    ("Easingwold", 54.1200, -1.1910, True),
    ("Thirsk", 54.2330, -1.3420, True),
    ("Goathland", 54.3990, -0.7170, False),
    ("Castleton", 54.4650, -0.9460, False),
    ("Stokesley", 54.4700, -1.1930, True),
    ("Great Ayton", 54.4890, -1.1390, False),
    ("Guisborough", 54.5350, -1.0560, False),
    ("Northallerton", 54.3390, -1.4340, True),
    ("Bedale", 54.2880, -1.5910, False),
    ("Ripon", 54.1360, -1.5240, True),
    ("Boroughbridge", 54.0960, -1.3970, False),
    ("Haxby", 54.0160, -1.0750, False),
    ("Strensall", 54.0400, -1.0350, False),
    ("York", 53.9600, -1.0810, True),
    ("Stamford Bridge", 53.9890, -0.9140, False),
    ("Pocklington", 53.9310, -0.7790, False),
    ("Scarborough", 54.2830, -0.3990, True),
    ("Whitby", 54.4860, -0.6150, True),
    ("Robin Hood's Bay", 54.4340, -0.5340, False),
    ("Middlesbrough", 54.5740, -1.2350, False),
    ("Filey", 54.2100, -0.2890, False),
    ("Driffield", 54.0060, -0.4410, False),
    ("Harrogate", 53.9920, -1.5370, False),
]


def miles(lat1, lng1, lat2, lng2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


TOWNS = []
for n, la, ln, major in PLACES:
    d = miles(C["lat"], C["lng"], la, ln)
    if d <= C["radius_miles"]:
        TOWNS.append({"name": n, "lat": la, "lng": ln, "major": major, "miles": round(d)})
TOWNS.sort(key=lambda t: t["miles"])


def slugify(s):
    return "".join(ch if ch.isalnum() else "-" for ch in s.lower()).replace("--", "-").strip("-").replace("'", "")


# ---------------------------------------------------------------------------
# Icons (inline SVG, stroke = currentColor)
# ---------------------------------------------------------------------------
ICON_PATHS = {
    "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "van": '<path d="M2 7h11v9H2z"/><path d="M13 10h4l4 4v2h-8z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "office": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    "piano": '<rect x="3" y="5" width="18" height="12" rx="1.5"/><path d="M3 11h18M7 11v6M11 11v6M15 11v6M7 11V8M17 11V8"/><path d="M5 17v3M19 17v3"/>',
    "box": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    "tools": '<path d="M14.5 6.5a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.5-1.5a4 4 0 0 0-5-5L13 5z"/><path d="m3 21 6-6"/><path d="M4 4l5 5"/>',
    "storage": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M3 9h18M3 14h18M10 6.5h4M10 11.5h4M10 16.5h4"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.4 8.3 8 9 4.6-.7 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pound": '<path d="M16 6.5A4 4 0 0 0 8.5 8v4.5c0 3-1 5-2.5 6.5H18M6 13h8"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "check": '<path d="M5 12.5 9.5 17 19 7.5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.2A5 5 0 0 1 21.5 19"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON_PATHS[name]}</svg>')


LOGO_SVG = (
    '<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#1b3a29"/>'
    '<path d="M6 30c6-7 10-9 15-6s9 1 13-4 6-5 8-4v20H6z" fill="#8a3f74"/>'
    '<path d="M6 34c7-4 13-5 19-3s11 1 17-2v8H6z" fill="#2f6a4c"/>'
    '<path d="M12 22h13v8H12zM25 24h5l3 3v3h-8z" fill="#fff"/>'
    '<circle cx="16" cy="31" r="2.2" fill="#e3a83b"/><circle cx="29" cy="31" r="2.2" fill="#e3a83b"/></svg>'
)


def img(name, alt, size=800, cls="", eager=False, sizes="(max-width: 700px) 100vw, 50vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1600.webp 1600w" sizes="{sizes}">'
            f'<img{c} src="assets/img/{name}-1600.jpg" alt="{escape(alt)}" width="1600" height="1000" {load}></picture>')


# ---------------------------------------------------------------------------
# Services — content drawn from the original template's service list:
# Domestic, International, Special Furniture, Reassembly & Packing,
# Deposit (storage), Cleaning, Fleet / small vans, Cargo / commercial.
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "house-removals", "group": "Removals", "icon": "home", "image": "domestic",
        "title": "House Removals", "nav": "House removals",
        "short": "Full-service home moves across Ryedale, the Moors and the Vale of York — from one-bed cottages to large farmhouses.",
        "headline": "House removals from Helmsley and across Ryedale",
        "intro": "Moving home is one of the biggest days in anyone’s life. Our uniformed, trained crews take the weight off — careful wrapping, safe loading and a calm, organised move day, whether you’re moving across Helmsley or 30 miles across North Yorkshire.",
        "body": [
            ("A move planned around you", "Every house move starts with a free survey, in person or by video call. We look at access, parking, stairs and the items that need extra care, then give you a clear, fixed written quote — no hourly meter running on the day and no surprises afterwards."),
            ("Protection as standard", "Furniture is blanket-wrapped, mattresses and sofas go into protective covers, and floors, door frames and banisters are protected at both properties. Fragile items are packed by the crew if you choose our packing service, and everything is loaded methodically so it comes off in the right order."),
            ("Rural and village moves", "Farm tracks, narrow lanes, stone steps and tight village squares are everyday work for us. We choose the right size vehicle for the access — and where a big lorry won’t fit, we shuttle with a smaller van so nothing is carried further than it needs to be."),
        ],
        "includes": ["Free home or video survey", "Fixed-price written quote", "Uniformed, trained removal crew", "Furniture blankets, sofa and mattress covers", "Floor and doorway protection", "Goods-in-transit insurance", "Beds and wardrobes dismantled & rebuilt", "Flexible dates, including Saturdays"],
        "faq": [
            ("How far in advance should I book?", "Four to six weeks is ideal, especially for Fridays and the end of the month, which are the busiest days. We can often help at shorter notice, so call us even if your completion date is next week."),
            ("What if my completion date moves?", "It happens all the time. Let us know as soon as you can and we’ll move your booking to the new date wherever we have capacity — there’s no charge for changing a date with reasonable notice."),
            ("Do you move on the same day as completion?", "Yes — most of our house moves are completion-day moves. We load in the morning and wait for the keys, keeping you updated throughout."),
        ],
    },
    {
        "slug": "man-and-van", "group": "Removals", "icon": "van", "image": "team",
        "title": "Man & Van", "nav": "Man & van / small moves",
        "short": "Flexible, fully-insured small moves, single items, student moves and flat moves — two-man crews available.",
        "headline": "Man and van hire in Helmsley, Ryedale and North Yorkshire",
        "intro": "Not every move needs a full removal lorry. For flats, small cottages, single items, eBay and auction collections or student moves, our man-and-van service gives you the same care and insurance as a full removal, at a price that fits a smaller job.",
        "body": [
            ("Small moves done properly", "You get a clean, modern van with blankets, straps and a sack truck — not just a driver. Choose one person if you’re happy to help lift, or a two-person crew so you don’t have to lift a thing."),
            ("Collections and deliveries", "Bought a dresser at an auction in Thirsk or a sofa from a shop in York? We collect, wrap and deliver single items and part-loads across our 30-mile area and beyond."),
            ("Students and first homes", "Moving into halls or a first flat in York, Scarborough or Middlesbrough? We’ll fit you in around term dates and handle the stairs."),
        ],
        "includes": ["One- or two-person crews", "Blankets, straps and sack truck", "Single items and part loads", "Auction and shop collections", "Student and flat moves", "Goods-in-transit insurance"],
        "faq": [
            ("Is man and van cheaper than a full removal?", "For smaller moves, usually yes. If your move turns out to be bigger than a van load, we’ll tell you honestly and quote for the right vehicle rather than making two trips."),
            ("Can you deliver a single item?", "Yes. Single items, furniture from a shop or auction purchases are a big part of our van work."),
        ],
    },
    {
        "slug": "office-removals", "group": "Removals", "icon": "office", "image": "office",
        "title": "Office & Commercial Removals", "nav": "Office & commercial",
        "short": "Office, shop, surgery and workshop relocations planned to keep downtime to a minimum — evenings and weekends available.",
        "headline": "Office and commercial removals across North Yorkshire",
        "intro": "Moving a business is about keeping it running. We plan office, shop, surgery, holiday-let and workshop moves around your trading hours — including evenings and weekends — so your team can walk in and get straight back to work.",
        "body": [
            ("Planned to the hour", "We visit your premises, agree a move plan and a labelling system, and supply crates and packing materials in advance. On the day, a crew lead keeps everything on schedule."),
            ("IT, files and furniture", "Computers and screens are wrapped and boxed, filing cabinets moved securely, and desks and workstations dismantled and rebuilt at the new site exactly where your floor plan says."),
            ("Holiday lets and hospitality", "Ryedale has hundreds of holiday cottages, B&Bs and pubs. We handle furniture changeovers, refurb clear-outs and deliveries between guests, working around tight changeover days."),
        ],
        "includes": ["Pre-move site visit and plan", "Out-of-hours and weekend moves", "Crate hire and labelling system", "IT and equipment wrapping", "Desk and workstation dismantling", "Holiday let furniture changeovers", "Secure document handling", "Business storage"],
        "faq": [
            ("Can you move us over a weekend?", "Yes. Many business moves happen on a Friday evening and Saturday so you’re trading as normal on Monday."),
            ("Do you supply crates?", "We can supply plastic crates and boxes ahead of the move so your team can pack their own desks."),
        ],
    },
    {
        "slug": "long-distance-removals", "group": "Removals", "icon": "globe", "image": "longdistance",
        "title": "Long Distance & European Removals", "nav": "Long distance & Europe",
        "short": "Moving out of Yorkshire? Door-to-door moves to anywhere in the UK, plus European moves handled with trusted partners.",
        "headline": "Long distance and European removals from Ryedale",
        "intro": "Based in Helmsley and covering everywhere within 30 miles, we also move families out of the area — to anywhere in the UK, and on to Europe. Same crew, same care, door to door.",
        "body": [
            ("Anywhere in the UK", "From Helmsley to London, Edinburgh or Cornwall, we load, drive and unload ourselves. Longer moves are planned with overnight stops where needed, so you know exactly when we’ll arrive."),
            ("Moving to Europe", "For moves to France, Spain, Ireland and beyond, we pack and load here in North Yorkshire and work with trusted European partners for the crossing and delivery, with help on customs paperwork and inventories."),
            ("Moving to the Moors", "Relocating here from elsewhere in the UK? We regularly bring families into Ryedale, so we know the lanes, the villages and the access issues before we arrive."),
        ],
        "includes": ["UK-wide door-to-door moves", "European moves via trusted partners", "Full export packing", "Detailed inventory", "Customs paperwork guidance", "Storage-in-transit if dates don’t line up"],
        "faq": [
            ("Do you go outside the 30-mile area?", "Yes. Our local area is everywhere within 30 miles of Helmsley, but we move customers from or to anywhere in the UK and arrange European moves."),
            ("What if there’s a gap between moving out and moving in?", "We can store your belongings safely until your new home is ready, then deliver on the day you choose."),
        ],
    },
    {
        "slug": "specialist-items", "group": "Removals", "icon": "piano", "image": "antiques",
        "title": "Pianos, Antiques & Specialist Items", "nav": "Pianos, antiques & specialist",
        "short": "Pianos, antiques, artwork, grandfather clocks, gym equipment and heavy furniture moved with the right kit and know-how.",
        "headline": "Piano, antique and specialist furniture removals",
        "intro": "Some items need more than strong arms. Upright pianos, family antiques, long-case clocks, artwork, range cookers, safes and gym equipment all need the right equipment, planning and a crew who has done it before.",
        "body": [
            ("Pianos", "Upright pianos are moved on padded piano skids and wheeled boards, fully wrapped and strapped. For grand pianos and very difficult access we’ll survey first and quote accordingly."),
            ("Antiques and artwork", "Period furniture, mirrors and paintings are wrapped in acid-free tissue, bubble wrap and blankets, with custom cartons for artwork. Ideal for antique dealers and auction houses too."),
            ("Heavy and awkward items", "Stone garden ornaments, cast-iron baths, range cookers, safes, hot tubs and gym equipment — tell us what it is and we’ll bring the right kit and enough people."),
        ],
        "includes": ["Upright piano moves", "Antique and period furniture", "Artwork and mirror cartons", "Long-case and grandfather clocks", "Range cookers, safes and gym equipment", "Garden statues and stonework", "Dealer and auction deliveries"],
        "faq": [
            ("Do you move grand pianos?", "Please call us — we’ll look at the access and the instrument first and advise on the best approach."),
            ("Can you deliver from an auction house?", "Yes, we regularly collect from auctions and antique dealers across North Yorkshire."),
        ],
    },
    {
        "slug": "packing-services", "group": "Services", "icon": "box", "image": "packing",
        "title": "Packing & Packing Materials", "nav": "Packing & materials",
        "short": "Full or part packing by our crew, fragile-only packing, and boxes, tape and bubble wrap delivered to your door.",
        "headline": "Professional packing services and packing materials",
        "intro": "Packing takes far longer than most people expect. Let our team do it — the whole house, just the kitchen, or only the fragile items — using proper double-walled cartons and plenty of wrapping.",
        "body": [
            ("Full packing service", "Usually the day before your move, our team packs your entire home, room by room, with every box labelled by room and contents. On move day, we just load and go."),
            ("Fragile-only packing", "Happy to pack books and clothes yourself? We’ll just pack the china, glassware, pictures, mirrors and lamps — the items that are most likely to be damaged if packed in a hurry."),
            ("Boxes and materials", "We supply strong removal cartons, wardrobe boxes, tape, tissue and bubble wrap, delivered free with your booked move."),
            ("Unpacking", "We can also unpack at the other end, place items in cupboards and take away all the empty boxes and wrapping."),
        ],
        "includes": ["Full or part packing", "Fragile-only packing", "Double-walled removal cartons", "Hanging wardrobe boxes", "Acid-free tissue and bubble wrap", "Every box labelled by room", "Unpacking and debris removal"],
        "faq": [
            ("How long does packing take?", "Most three-bedroom homes are packed by our crew in a single day, the day before the move."),
            ("Can I just buy boxes?", "Yes — we sell boxes and packing materials and deliver them free with a booked move."),
        ],
    },
    {
        "slug": "furniture-reassembly", "group": "Services", "icon": "tools", "image": "assembly",
        "title": "Dismantling & Reassembly", "nav": "Dismantling & reassembly",
        "short": "Beds, wardrobes, tables and flat-pack taken apart, moved safely and rebuilt in your new home — fixings bagged and labelled.",
        "headline": "Furniture dismantling and reassembly",
        "intro": "Big beds, fitted wardrobes, extending tables and flat-pack furniture rarely fit through cottage doors in one piece. Our crews bring the tools, take items apart carefully and rebuild them in your new home.",
        "body": [
            ("Nothing lost", "Every screw, bolt and fitting is bagged and labelled with the item it belongs to, so your furniture goes back together exactly as it came apart."),
            ("Rebuilt where you want it", "Tell us which room each piece goes in and we’ll rebuild it there — so your beds are made up and ready on the first night."),
            ("Flat-pack assembly", "Bought new furniture for the new house? We can assemble flat-pack items for you, too."),
        ],
        "includes": ["Beds and bunk beds", "Wardrobes and sliding-door robes", "Dining and extending tables", "Flat-pack furniture assembly", "Wall-mounted TVs taken down", "Fixings bagged and labelled"],
        "faq": [
            ("Is dismantling included in a house move?", "Standard beds and wardrobes are included in our house removal quotes. Large fitted or complex items are noted during the survey."),
        ],
    },
    {
        "slug": "storage", "group": "Services", "icon": "storage", "image": "storage",
        "title": "Secure Storage", "nav": "Short & long term storage",
        "short": "Safe, organised and affordable short or long-term storage — perfect between completion dates, during renovations or for business stock.",
        "headline": "Short and long-term storage in North Yorkshire",
        "intro": "Safe, organised and affordable. Whether your new home isn’t ready, you’re renovating, downsizing or working abroad, we collect your belongings, store them securely and deliver them back whenever you need them.",
        "body": [
            ("Collected and delivered", "No hiring a van and doing it yourself — we pack, collect and inventory your items, store them, and bring them back to your new address."),
            ("Secure and dry", "Belongings are stored in a secure, monitored, dry facility, with an inventory so you know exactly what’s where."),
            ("As long as you need", "From a week between completions to a year or more, storage is charged weekly so you only pay for the time you use."),
        ],
        "includes": ["Short and long-term storage", "Collection and delivery", "Full inventory", "Secure, monitored facility", "Weekly pricing", "Business and stock storage"],
        "faq": [
            ("Can I access my items in storage?", "Yes, by appointment. Let us know what you need and we’ll have it ready, or deliver it to you."),
            ("Is my storage insured?", "Storage insurance is available — ask us for details when you get your quote."),
        ],
    },
    {
        "slug": "cleaning", "group": "Services", "icon": "sparkle", "image": "cleaning",
        "title": "End of Move Cleaning", "nav": "End of move cleaning",
        "short": "Move-out, end-of-tenancy and move-in cleans so you can hand over the keys and arrive somewhere fresh.",
        "headline": "End of tenancy and move-out cleaning",
        "intro": "The last thing you want after a day of moving is a mop. Add a professional clean to your move and leave your old home spotless for the buyer or landlord, or have your new home cleaned before you arrive.",
        "body": [
            ("Move-out and end-of-tenancy", "A thorough top-to-bottom clean once the house is empty: kitchens, ovens, bathrooms, skirting boards, windows inside and floors — helping you get your deposit back."),
            ("Move-in cleans", "Arrive to a fresh, clean home. We can clean your new property before the furniture goes in."),
            ("Holiday let and pre-sale cleans", "Getting a property ready for photos, viewings or the first guests? We can help with that too."),
        ],
        "includes": ["End-of-tenancy cleans", "Move-out cleans for sellers", "Move-in cleans", "Kitchen and oven cleaning", "Bathroom deep clean", "Holiday let and pre-sale cleans"],
        "faq": [
            ("Can I book cleaning without a removal?", "Yes, cleaning can be booked on its own, though it’s easiest to arrange alongside your move."),
        ],
    },
]
SVC = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# Area pages — a short, specific paragraph for each main town.
# ---------------------------------------------------------------------------
AREA_COPY = {
    "Helmsley": ("Our home town", "Helmsley is where we’re based, so local moves here are our bread and butter. From stone cottages off the Market Place to new homes on the edge of town and farms out towards Rievaulx and Duncombe Park, we know the parking, the narrow streets and the busy market days.", ["Rievaulx", "Harome", "Beadlam", "Sproxton", "Carlton", "Pockley"]),
    "Kirkbymoorside": ("Five minutes down the A170", "Kirkbymoorside and the moorland villages to the north — Gillamoor, Fadmoor and Hutton-le-Hole — are minutes from our base. Plenty of moves here involve farmhouses, long drives and narrow lanes, and we plan the right size vehicle for each one.", ["Gillamoor", "Fadmoor", "Keldholme", "Sinnington", "Nawton", "Hutton-le-Hole"]),
    "Pickering": ("Gateway to the Moors", "From period townhouses near the castle to cottages in Thornton-le-Dale and Middleton, Pickering moves are frequent for us. We plan around the Monday market and the summer visitor traffic on the A170.", ["Thornton-le-Dale", "Middleton", "Newton-on-Rawcliffe", "Lockton", "Marishes", "Kirby Misperton"]),
    "Malton": ("Malton & Norton", "Malton’s Georgian streets, flats above shops on the Market Place and the family homes over the river in Norton all have their own access challenges. We’ll arrange parking and plan the load so the move runs smoothly on either side of the Derwent.", ["Norton", "Old Malton", "Amotherby", "Swinton", "Rillington", "Settrington"]),
    "Easingwold": ("The Forest of Galtres", "Easingwold and the villages around it — Crayke, Husthwaite, Alne and Tollerton — combine new-build estates with older village properties. We regularly move families between here, York and Ryedale.", ["Crayke", "Husthwaite", "Alne", "Tollerton", "Huby", "Stillington"]),
    "Thirsk": ("Over (or round) Sutton Bank", "Thirsk is just over Sutton Bank from Helmsley. Our smaller vans take the A170 straight over; our larger removal lorries take the safer route round, avoiding the steep gradient and hairpin bends. Either way, you get a crew that knows the area.", ["Sowerby", "Topcliffe", "Sutton-under-Whitestonecliffe", "Kilburn", "Carlton Miniott", "Dalton"]),
    "York": ("City moves, done properly", "York’s medieval centre, footstreets and terraced streets in areas like South Bank, Clifton and Fulford mean parking and access need planning. We arrange parking suspensions where needed and bring a smaller shuttle van when a lorry can’t get close. We also cover Haxby, Strensall, Huntington and the outer villages.", ["Haxby", "Strensall", "Huntington", "Clifton", "Fulford", "Bishopthorpe"]),
    "Northallerton": ("The county town", "From Romanby and Brompton to the villages along the A684 and A19, Northallerton moves are a regular trip for us across the Hambleton Hills.", ["Romanby", "Brompton", "Osmotherley", "Thornton-le-Beans", "Yafforth", "Ainderby Steeple"]),
    "Stokesley": ("Over the top through Bilsdale", "The B1257 through Bilsdale links Helmsley with Stokesley and Great Ayton — one of the most scenic removal routes in England. We move families across Stokesley, Great Ayton, Hutton Rudby and Guisborough.", ["Great Ayton", "Hutton Rudby", "Swainby", "Kildale", "Guisborough", "Chop Gate"]),
    "Ripon": ("The cathedral city", "Ripon sits at the western edge of our 30-mile area. Period terraces around the cathedral, homes on the newer estates and the villages towards Boroughbridge are all covered.", ["Bishop Monkton", "Littlethorpe", "Sharow", "Boroughbridge", "Kirkby Malzeard", "North Stainley"]),
    "Scarborough": ("The coast", "South Cliff flats with lots of stairs, steep streets in the Old Town and family homes in Scalby, Newby, Seamer and Eastfield — we’re used to them all. We plan parking and allow time for the stairs so there are no surprises.", ["Scalby", "Newby", "Seamer", "Eastfield", "Cayton", "Burniston"]),
    "Whitby": ("Steep streets and narrow yards", "Whitby’s yards, ginnels and steep streets — especially on the East Side — make it one of the trickiest towns to move in. We survey access carefully, bring the right size vehicle over the A169 and carry items by hand where we need to. We cover Sleights, Ruswarp, Sandsend and Robin Hood’s Bay too.", ["Sleights", "Ruswarp", "Sandsend", "Robin Hood's Bay", "Grosmont", "Hawsker"]),
}


def area_slug(town):
    return f"removals-{slugify(town)}.html"


AREA_TOWNS = [t for t in TOWNS if t["name"] in AREA_COPY]

# ---------------------------------------------------------------------------
# FAQs (also used for FAQPage structured data)
# ---------------------------------------------------------------------------
FAQS = [
    ("What area do you cover?", f"We’re based in Helmsley and cover everywhere within {C['radius_miles']} miles — including York, Malton, Pickering, Kirkbymoorside, Thirsk, Easingwold, Northallerton, Stokesley, Ripon, Scarborough and Whitby. We also do long-distance moves to anywhere in the UK and arrange European moves."),
    ("How much does a removal cost?", "Every move is different, so we give a free, fixed-price quote after a quick survey (in person or by video). The price depends on the volume of belongings, access at both ends, the distance and any extras like packing or storage."),
    ("Are my belongings insured?", "Yes. Our moves include goods-in-transit insurance and we hold public liability insurance. Ask us for details of the cover and any options to increase it for high-value items."),
    ("How far in advance should I book?", "Four to six weeks is ideal, particularly for Fridays, month ends and the summer. We can often help at shorter notice — just call."),
    ("Do I need to empty drawers and wardrobes?", "Light clothing can usually stay in chests of drawers, and we bring wardrobe boxes for hanging clothes. Heavy items, liquids and anything fragile should be packed separately."),
    ("What won’t you move?", "We can’t carry hazardous items such as gas bottles, petrol, paint thinners, fireworks or ammunition. We’ll also ask you to keep valuables, jewellery, important documents and medication with you."),
    ("Do you work weekends?", "Yes, we move on Saturdays as standard and on Sundays by arrangement — handy for business moves."),
    ("Can you store my things between houses?", "Yes. We offer short and long-term storage, collected from your old home and delivered to your new one when you’re ready."),
    ("Do you take a deposit?", "A small deposit secures your date. The balance is due before or on the day of the move — your quote will set out the terms clearly."),
    ("What if it rains?", "This is Yorkshire — we’re ready for it. We use floor protection, covers and blankets so your belongings stay dry and your floors stay clean."),
]

TIPS = [
    ("Start with what you don’t use", "Declutter before you pack. Every item you sell, donate or recycle is one less thing to wrap, move and unpack — and it can bring your quote down."),
    ("Use the right boxes", "Small boxes for books and heavy items, larger boxes for light things like bedding. Keep each box under about 20kg so it can be lifted safely."),
    ("Label every box on the side", "Write the room and a short description on two sides (not just the top — boxes get stacked). Mark fragile boxes clearly."),
    ("Pack plates on their edge", "Plates travel far better stood on edge like records, each wrapped, with crumpled paper at the bottom and top of the box."),
    ("Pack a first-night box", "Kettle, mugs, tea, phone chargers, toilet roll, bedding, towels, basic tools, medication and something for the kids and pets. Keep it with you."),
    ("Photograph your cables", "Snap the back of the TV and router before unplugging so setting up is easy, and bag screws and remotes together."),
    ("Defrost the freezer", "Switch off and defrost the fridge-freezer at least 24 hours before moving day, and leave the doors ajar to stop it smelling."),
    ("Tell people you’re moving", "Council tax, utilities, broadband, DVLA, your bank, GP and dentist, and set up Royal Mail redirection for a few months."),
]

# ---------------------------------------------------------------------------
# Guides (blog articles)
# ---------------------------------------------------------------------------
GUIDES = [
    {
        "slug": "moving-house-checklist", "image": "room",
        "title": "The complete moving house checklist",
        "desc": "An eight-week countdown to moving day — what to do, when, so nothing gets forgotten.",
        "body": """
<p>A good move is mostly planning. Use this countdown from the day you agree a sale or sign a tenancy, and moving day will be far calmer.</p>
<h2>Eight weeks to go</h2>
<ul><li>Get removal quotes and book your survey. Popular dates (Fridays, month ends, summer) go early.</li><li>Start decluttering room by room — loft, garage and shed first.</li><li>If you rent, check your notice period and what the landlord expects at check-out.</li><li>Start a moving folder for quotes, contracts and contact numbers.</li></ul>
<h2>Six weeks to go</h2>
<ul><li>Book your removal company and any packing, storage or cleaning.</li><li>Order boxes and packing materials (we deliver them free with a booked move).</li><li>Arrange time off work, and childcare or pet care for moving day.</li><li>Measure large furniture and check it will fit in the new home.</li></ul>
<h2>Four weeks to go</h2>
<ul><li>Start packing things you won’t need: books, spare bedding, out-of-season clothes, ornaments.</li><li>Tell your council, utilities, broadband provider, bank, employer, GP, dentist, insurers and DVLA.</li><li>Set up Royal Mail redirection.</li><li>Arrange parking at both properties if access is tight.</li></ul>
<h2>Two weeks to go</h2>
<ul><li>Confirm your date and times with us, and give us any access details for the new property.</li><li>Run down the freezer and food cupboards.</li><li>Dispose of anything we can’t carry: paint, gas bottles, chemicals and fuel.</li></ul>
<h2>The day before</h2>
<ul><li>Defrost the fridge-freezer.</li><li>Pack your first-night box and a bag of essentials.</li><li>Charge your phone and keep keys, documents and valuables together.</li></ul>
<h2>Moving day</h2>
<ul><li>Take meter readings and photographs.</li><li>Do a final walk round: lofts, cupboards, sheds and behind doors.</li><li>Leave keys and manuals for the new owners.</li><li>At the new home, show the crew where each room is and put the kettle on.</li></ul>
<blockquote>Want us to do most of this for you? Our <a href="packing-services.html">packing service</a> and <a href="cleaning.html">end of move cleaning</a> take the two most time-consuming jobs off your list.</blockquote>
""",
    },
    {
        "slug": "packing-tips", "image": "boxes",
        "title": "How to pack like a professional remover",
        "desc": "The packing techniques our crews use every day, so your belongings arrive in one piece.",
        "body": """
<p>Most breakages happen because boxes are overfilled, underfilled or badly labelled. Here’s how our crews pack.</p>
<h2>Get the right materials</h2>
<p>Use double-walled removal cartons rather than supermarket boxes, plenty of packing paper or tissue, bubble wrap for fragile items and good quality tape. Wardrobe boxes let you hang clothes straight in.</p>
<h2>Heavy items in small boxes</h2>
<p>Books, tins and tools go in small cartons; bedding, cushions and lampshades in large ones. Keep each box to a weight one person can lift comfortably.</p>
<h2>Fill every gap</h2>
<p>A box that rattles will break. Fill gaps with crumpled paper, tea towels or soft items so nothing can move, and make sure the lid closes flat so boxes stack safely.</p>
<h2>Plates on edge, glasses upright</h2>
<p>Wrap plates individually and stand them on their edge. Wrap glasses and stand them upright, with paper stuffed inside. Put a layer of crumpled paper at the bottom and top of every fragile box.</p>
<h2>Label clearly</h2>
<p>Write the destination room and contents on two sides, and add “FRAGILE” and “THIS WAY UP” where needed. A colour sticker per room makes unloading quicker.</p>
<h2>Pack room by room</h2>
<p>Finish one room before starting the next, and start with the rooms you use least. Leave the kitchen and bathroom until last.</p>
<h2>Keep the essentials separate</h2>
<p>Pack a first-night box and a personal bag with documents, medication, chargers, keys and valuables, and take them with you in the car.</p>
<blockquote>Short of time? We can pack the whole house, or just the fragile items, the day before your move. <a href="packing-services.html">See our packing service</a>.</blockquote>
""",
    },
    {
        "slug": "moving-to-the-north-york-moors", "image": "village",
        "title": "Moving to Ryedale and the North York Moors: what to know",
        "desc": "Practical advice for moving into a rural home in and around Helmsley, Pickering, Malton and the Moors.",
        "body": """
<p>Ryedale and the North York Moors are wonderful places to live — market towns, stone villages, moorland and the coast within reach. Moving to a rural home does bring a few practical things worth thinking about.</p>
<h2>Check access early</h2>
<p>Narrow lanes, low bridges, farm tracks, cattle grids and steep drives can all limit the size of vehicle that can reach a property. Tell your remover about access at the survey; we’ll plan the right vehicle, or shuttle with a smaller van.</p>
<h2>Plan your route</h2>
<p>Some moorland roads, including Sutton Bank and parts of the Moors, have steep gradients and tight bends that large vehicles avoid. A local remover will already know the best route for a loaded lorry.</p>
<h2>Think about the season</h2>
<p>Winter can bring snow and ice on higher roads, and summer brings visitor traffic on the A170 and coast roads. Keep your dates flexible if you can, and talk to us about the best time of day to move.</p>
<h2>Services and utilities</h2>
<ul><li>Many rural homes use oil or LPG heating rather than mains gas — check tank levels and supplier details before completion.</li><li>Some properties have private water supplies or septic tanks; ask the seller for maintenance records.</li><li>Check broadband and mobile coverage at the exact postcode.</li><li>Ryedale is now part of North Yorkshire Council for council tax, bins and planning.</li></ul>
<h2>Listed buildings and conservation areas</h2>
<p>Many homes in Helmsley, Pickering, Malton and the villages are listed or within conservation areas, and the North York Moors National Park has its own planning authority. Check what permissions you’d need before planning changes.</p>
<h2>Get to know the area</h2>
<p>Market days, village shows, farm shops and walking routes from the front door — moving here is about the lifestyle. We’ve moved hundreds of families into the area, and we’re always happy to share local tips on moving day.</p>
<blockquote>Moving into Ryedale from elsewhere in the UK? See our <a href="long-distance-removals.html">long distance removals</a>.</blockquote>
""",
    },
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
NAV = [
    ("index.html", "Home", None),
    (None, "Removals", [s for s in SERVICES if s["group"] == "Removals"]),
    (None, "Services", [s for s in SERVICES if s["group"] == "Services"]),
    ("areas.html", "Areas", None),
    ("fleet.html", "Fleet", None),
    ("about.html", "About", None),
    ("tips-faq.html", "FAQ", None),
    ("contact.html", "Contact", None),
]


def address_line():
    parts = [C["street"], C["town"], C["county"], C["postcode"]]
    return ", ".join(p for p in parts if p)


def business_schema():
    data = {
        "@context": "https://schema.org",
        "@type": "MovingCompany",
        "name": C["name"],
        "url": C["domain"] + "/",
        "telephone": C["phone_link"],
        "email": C["email"],
        "image": C["domain"] + "/assets/img/hero-1600.jpg",
        "logo": C["domain"] + "/assets/img/logo.svg",
        "priceRange": "££",
        "address": {"@type": "PostalAddress", "streetAddress": C["street"] or None, "addressLocality": C["town"],
                    "addressRegion": C["county"], "postalCode": C["postcode"], "addressCountry": "GB"},
        "geo": {"@type": "GeoCoordinates", "latitude": C["lat"], "longitude": C["lng"]},
        "areaServed": {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": C["lat"], "longitude": C["lng"]},
                       "geoRadius": str(round(C["radius_miles"] * 1609.34))},
        "openingHours": ["Mo-Fr 08:00-18:00", "Sa 08:00-16:00"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Removal services",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"]}} for s in SERVICES]},
    }
    data["address"] = {k: v for k, v in data["address"].items() if v}
    same = [u for u in (C["facebook"], C["instagram"]) if u]
    if same:
        data["sameAs"] = same
    return data


def header(active):
    items = []
    for href, label, children in NAV:
        if children:
            sub = "".join(f'<li><a href="{s["slug"]}.html">{escape(s["nav"])}</a></li>' for s in children)
            act = " active" if active in [s["slug"] + ".html" for s in children] else ""
            items.append(f'<li><button class="nav-link{act}" aria-expanded="false" type="button">{label} ▾</button><ul class="dropdown">{sub}</ul></li>')
        else:
            act = " active" if href == active else ""
            items.append(f'<li><a class="nav-link{act}" href="{href}">{label}</a></li>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="container">
  <span class="tb-msg">Helmsley-based removals covering everywhere within {C['radius_miles']} miles</span>
  <span class="tb-links"><a href="tel:{C['phone_link']}">{icon('phone', '').replace('<svg', '<svg width="14" height="14" style="vertical-align:-2px;margin-right:4px"')}{C['phone']}</a><a href="mailto:{C['email']}">{C['email']}</a></span>
</div></div>
<header class="site-header"><div class="container">
  <a class="logo" href="index.html" aria-label="{C['name']} home">{LOGO_SVG}<span class="logo-text">{C['name']}<small>{C['tagline']}</small></span></a>
  <nav class="nav" aria-label="Main">
    <ul>{''.join(items)}</ul>
    <div class="nav-mobile-cta"><a class="btn btn-primary" href="quote.html">Get a free quote</a><a class="btn btn-outline" href="tel:{C['phone_link']}">Call {C['phone']}</a></div>
  </nav>
  <div class="header-cta">
    <a class="header-phone" href="tel:{C['phone_link']}">{C['phone']}</a>
    <a class="btn btn-primary" href="quote.html">Free quote</a>
    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" type="button">{icon('menu')}</button>
  </div>
</div></header>"""


def footer():
    rem = "".join(f'<li><a href="{s["slug"]}.html">{escape(s["nav"])}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="{area_slug(t["name"])}">Removals {escape(t["name"])}</a></li>' for t in AREA_TOWNS[:8])
    social = ""
    if C["facebook"]:
        social += f'<li><a href="{C["facebook"]}" rel="noopener">Facebook</a></li>'
    if C["instagram"]:
        social += f'<li><a href="{C["instagram"]}" rel="noopener">Instagram</a></li>'
    return f"""<footer class="site-footer">
  <div class="container footer-main">
    <div>
      <a class="logo" href="index.html">{LOGO_SVG}<span class="logo-text">{C['name']}<small>{C['tagline']}</small></span></a>
      <p>Friendly, careful removals, packing and storage from our base in Helmsley — covering Ryedale, the North York Moors, the Vale of York and the coast, everywhere within {C['radius_miles']} miles.</p>
      <ul>{social}</ul>
    </div>
    <div><h4>Services</h4><ul>{rem}</ul></div>
    <div><h4>Areas we cover</h4><ul>{areas}<li><a href="areas.html">All areas →</a></li></ul></div>
    <div><h4>Get in touch</h4><ul>
      <li><a href="tel:{C['phone_link']}">{C['phone']}</a></li>
      <li><a href="tel:{C['mobile_link']}">{C['mobile']}</a> (mobile)</li>
      <li><a href="mailto:{C['email']}">{C['email']}</a></li>
      <li>{escape(address_line())}</li>
      <li style="margin-top:1rem"><a class="btn btn-gold" href="quote.html">Get a free quote</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom"><div class="container">
    <span>© <span data-year>{date.today().year}</span> {C['name']}. All rights reserved.</span>
    <ul><li><a href="guides.html">Moving guides</a></li><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li><li><a href="sitemap.xml">Sitemap</a></li></ul>
  </div></div>
</footer>
<div class="mobile-bar"><a class="call" href="tel:{C['phone_link']}">{icon('phone')} Call us</a><a class="quote" href="quote.html">{icon('calendar')} Free quote</a></div>"""


def page(filename, title, desc, body, schema=None, og_image="hero", active=None, noindex=False):
    full_title = title if C["name"] in title else f"{title} | {C['name']}"
    url = C["domain"] + "/" + ("" if filename == "index.html" else filename)
    schemas = [business_schema()] + (schema or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C['name']}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C['domain']}/assets/img/{og_image}-1600.jpg">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1b3a29">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{ld}
</head>
<body>
{header(active or filename)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    PAGES.append((filename, noindex))


PAGES = []


def breadcrumb(items):
    links = " / ".join(f'<a href="{h}">{escape(t)}</a>' if h else escape(t) for h, t in items)
    return f'<div class="breadcrumb"><a href="index.html">Home</a> / {links}</div>'


def breadcrumb_schema(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": C["domain"] + "/"}]
    for i, (h, t) in enumerate(items, start=2):
        e = {"@type": "ListItem", "position": i, "name": t}
        if h:
            e["item"] = C["domain"] + "/" + h
        lst.append(e)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


def page_hero(title, lead, image, crumbs, extra=""):
    return f"""<section class="page-hero">
  <div class="hero-media">{img(image, '', eager=True, sizes='100vw')}</div>
  <div class="container">
    {breadcrumb(crumbs)}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    {extra}
  </div>
</section>"""


def cta_band(title="Ready to get moving?", text="Get a free, no-obligation fixed-price quote — usually within one working day."):
    return f"""<section class="section"><div class="container"><div class="cta-band reveal">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="actions"><a class="btn btn-gold" href="quote.html">Get my free quote</a><a class="btn btn-light" href="tel:{C['phone_link']}">{icon('phone')} {C['phone']}</a></div>
</div></div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{escape(q)}</summary><div class="answer"><p>{escape(a)}</p></div></details>' for q, a in faqs) + "</div>"


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def service_cards(services, with_img=True):
    out = []
    for s in services:
        im = f'<div class="card-img">{img(s["image"], s["title"], sizes="(max-width: 640px) 100vw, 33vw")}</div>' if with_img else ""
        ic = "" if with_img else f'<div class="card-icon">{icon(s["icon"])}</div>'
        out.append(f"""<article class="card reveal">{im}<div class="card-body">{ic}<h3>{escape(s['title'])}</h3><p>{escape(s['short'])}</p><a class="card-link" href="{s['slug']}.html">Find out more</a></div></article>""")
    return "".join(out)


TRUST = f"""<section class="trust"><div class="container">
  <div class="trust-item">{icon('pin')}<div>Local to Helmsley<span>Covering {C['radius_miles']} miles around</span></div></div>
  <div class="trust-item">{icon('pound')}<div>Fixed-price quotes<span>Free survey, no hidden extras</span></div></div>
  <div class="trust-item">{icon('shield')}<div>Fully insured<span>Goods in transit & public liability</span></div></div>
  <div class="trust-item">{icon('users')}<div>Trained, uniformed crews<span>Careful, friendly and on time</span></div></div>
</div></section>"""


# ---------------------------------------------------------------------------
# Area map (SVG drawn from real coordinates)
# ---------------------------------------------------------------------------
def area_map_svg(highlight=None):
    size, pad = 600, 30
    R = (size - 2 * pad) / 2
    cx = cy = size / 2
    kx = math.cos(math.radians(C["lat"])) * 69.17
    ky = 69.0

    def xy(la, ln):
        dx = (ln - C["lng"]) * kx
        dy = (la - C["lat"]) * ky
        s = R / C["radius_miles"]
        return cx + dx * s, cy - dy * s

    rings = ""
    for m in (10, 20, 30):
        r = R * m / C["radius_miles"]
        rings += (f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{"rgba(227,168,59,.06)" if m == 30 else "none"}" '
                  f'stroke="rgba(255,255,255,{.35 if m == 30 else .16})" stroke-width="{1.6 if m == 30 else 1}" stroke-dasharray="{"0" if m == 30 else "4 5"}"/>'
                  f'<text x="{cx + 4}" y="{cy - r + 14:.1f}" fill="rgba(255,255,255,.45)" font-size="10" font-family="Inter, sans-serif">{m} miles</text>')
    # Place labels without collisions: major towns first, try right/left/below/above,
    # and drop the label (keeping the dot) if there is no free spot.
    boxes = [(cx - 60, cy - 14, cx + 60, cy + 40)]  # reserve space for the base label

    def free(b):
        return all(b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3] for o in boxes) and b[0] > 6 and b[2] < size - 6

    dots, labels = "", ""
    for t in sorted(TOWNS, key=lambda t: (not t["major"], t["miles"])):
        if t["name"] == C["town"]:
            continue
        x, y = xy(t["lat"], t["lng"])
        minor = "" if t["major"] else " minor"
        rr = 4.5 if t["major"] else 3
        fs = 11 if t["major"] else 10
        w = len(t["name"]) * fs * 0.56
        spot = None
        for ax, tx, ty in (("start", x + 7, y + 4), ("end", x - 7, y + 4), ("middle", x, y + 16), ("middle", x, y - 8)):
            x0 = tx if ax == "start" else tx - w if ax == "end" else tx - w / 2
            b = (x0 - 1, ty - fs, x0 + w + 1, ty + 3)
            if free(b):
                spot = (ax, tx, ty)
                boxes.append(b)
                break
        label = f'<text x="{spot[1]:.1f}" y="{spot[2]:.1f}" text-anchor="{spot[0]}">{escape(t["name"])}</text>' if spot else ""
        dot = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}"><title>{escape(t["name"])} – {t["miles"]} miles</title></circle>'
        if t["name"] in AREA_COPY:
            labels += f'<a class="town{minor}" href="{area_slug(t["name"])}">{dot}{label}</a>'
        else:
            labels += f'<g class="town{minor}">{dot}{label}</g>'
    towns = labels
    hx, hy = cx, cy
    return f"""<svg viewBox="0 0 {size} {size}" role="img" aria-label="Map of the {C['radius_miles']}-mile area we cover around {C['town']}">
  <defs><radialGradient id="g" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#2f6a4c"/><stop offset="1" stop-color="#1b3a29"/></radialGradient></defs>
  <rect width="{size}" height="{size}" rx="18" fill="url(#g)"/>
  {rings}
  <text x="{size - 26}" y="40" fill="rgba(255,255,255,.55)" font-size="12" font-weight="700" text-anchor="middle" font-family="Inter, sans-serif">N</text>
  <path d="M{size - 26} 46 l-6 14 h12z" fill="rgba(255,255,255,.55)"/>
  <text x="{size - 40}" y="{cy + 90}" fill="rgba(160,200,220,.5)" font-size="12" font-style="italic" text-anchor="end" font-family="Inter, sans-serif">North Sea</text>
  {towns}
  <circle cx="{hx}" cy="{hy}" r="18" fill="rgba(138,63,116,.35)"/><circle cx="{hx}" cy="{hy}" r="9" fill="#8a3f74" stroke="#fff" stroke-width="2.5"/>
  <text x="{hx}" y="{hy + 32}" text-anchor="middle" fill="#fff" font-size="14" font-weight="700" font-family="Inter, sans-serif">{C['town']} base</text>
</svg>"""


# ---------------------------------------------------------------------------
# Vehicle illustrations for the fleet page
# ---------------------------------------------------------------------------
def vehicle_svg(kind):
    if kind == "small":
        body = '<rect x="40" y="38" width="120" height="50" rx="6"/><path d="M160 50h30l22 22v16h-52z"/><path d="M166 56h22l14 14h-36z" fill="#cfe0d5"/>'
        w = '<circle cx="78" cy="92" r="12"/><circle cx="184" cy="92" r="12"/>'
    elif kind == "luton":
        body = '<rect x="20" y="18" width="160" height="70" rx="5"/><path d="M180 44h26l20 22v22h-46z"/><path d="M184 50h20l16 16h-36z" fill="#cfe0d5"/>'
        w = '<circle cx="60" cy="92" r="12"/><circle cx="200" cy="92" r="12"/>'
    else:
        body = '<rect x="6" y="10" width="196" height="78" rx="5"/><path d="M202 34h22l18 18v36h-40z"/><path d="M206 40h16l14 14h-30z" fill="#cfe0d5"/>'
        w = '<circle cx="40" cy="92" r="12"/><circle cx="74" cy="92" r="12"/><circle cx="216" cy="92" r="12"/>'
    return (f'<svg class="vehicle" viewBox="0 0 250 110" aria-hidden="true"><g fill="#24503a">{body}</g>'
            f'<g fill="#1d2420" stroke="#e3a83b" stroke-width="4">{w}</g>'
            f'<rect x="0" y="104" width="250" height="3" rx="1.5" fill="#ddd5c7"/></svg>')


# ---------------------------------------------------------------------------
# PAGES
# ---------------------------------------------------------------------------
def build_home():
    major = [t for t in TOWNS if t["major"] and t["name"] != C["town"]]
    town_chips = "".join(
        f'<li><a href="{area_slug(t["name"])}">{escape(t["name"])} <small>{t["miles"]} mi</small></a></li>' if t["name"] in AREA_COPY
        else f'<li><span>{escape(t["name"])} <small>{t["miles"]} mi</small></span></li>' for t in major)
    body = f"""
<section class="hero">
  <div class="hero-media">{img('hero', 'Two Ryedale Removals crew members unloading boxes from a removal van', eager=True, sizes='100vw')}</div>
  <div class="container"><div class="hero-content">
    <span class="eyebrow" style="color:var(--gold)">Removals · Packing · Storage · Cleaning</span>
    <h1>Moving home in North Yorkshire? <em>We’ll carry it from here.</em></h1>
    <p class="lead">Careful, friendly removals from our base in Helmsley — covering Ryedale, the North York Moors, York and the coast, everywhere within {C['radius_miles']} miles.</p>
    <div class="hero-actions"><a class="btn btn-gold" href="quote.html">Get a free quote</a><a class="btn btn-light" href="tel:{C['phone_link']}">{icon('phone')} {C['phone']}</a></div>
    <ul class="hero-points"><li>{icon('check')} Free survey & fixed price</li><li>{icon('check')} Fully insured</li><li>{icon('check')} Packing, storage & cleaning</li></ul>
  </div></div>
</section>
{TRUST}

<section class="section">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">What we do</span><h2>Every part of your move, under one roof</h2>
    <p class="lead">From a single sofa to a full farmhouse, an office to a move across the country — plus the packing, storage and cleaning that go with it.</p></div>
    <div class="grid grid-3">{service_cards(SERVICES)}</div>
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">How it works</span><h2>Preparing, collecting, delivering</h2>
    <p class="lead">Moving can’t be made much easier than this.</p></div>
    <div class="grid grid-3 steps" style="row-gap:48px">
      <div class="step reveal"><h3>Preparing</h3><p>We survey your home in person or by video, then send a clear fixed-price quote. Once booked, we deliver boxes and help plan every detail — including packing if you’d like us to do it.</p></div>
      <div class="step reveal"><h3>Collecting</h3><p>On the day, our uniformed crew protects your floors and doorways, wraps your furniture and loads the van methodically, so everything comes off in the right order.</p></div>
      <div class="step reveal"><h3>Delivering</h3><p>We unload room by room, rebuild beds and furniture where you want them, and take away the packing materials. All that’s left to do is put the kettle on.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split-media reveal">{img('team', 'Removal crew carrying boxes to the van')}<div class="badge"><strong>{C['radius_miles']} miles</strong>covered around our Helmsley base</div></div>
    <div class="reveal">
      <span class="eyebrow">Some words about us</span>
      <h2>A local removal company that treats your home like our own</h2>
      <p>{C['name']} is a Helmsley-based removal company serving the towns, villages and farms of Ryedale and the surrounding area. We’re big enough to handle large house and office moves, and small enough that you’ll speak to the same friendly team from your first call to the last box.</p>
      <p>Our mission is simple: a move that is <strong>careful, on time and on budget</strong>, with no surprises on the day.</p>
      <ul class="ticks"><li>Clear, fixed-price written quotes</li><li>Trained, uniformed and courteous crews</li><li>Modern vehicles in every size, from vans to removal lorries</li><li>Local knowledge of every lane, village and town in our area</li></ul>
      <a class="btn btn-outline" href="about.html">More about us</a>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="container area-wrap">
    <div class="area-map reveal">{area_map_svg()}</div>
    <div class="reveal">
      <span class="eyebrow">Areas we cover</span>
      <h2>Everywhere within {C['radius_miles']} miles of Helmsley</h2>
      <p class="lead">From the moors to the coast and down into the Vale of York, we know the roads, the villages and the access before we arrive.</p>
      <ul class="town-list">{town_chips}</ul>
      <a class="btn btn-primary" href="areas.html">See all areas we cover</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split reverse">
    <div class="split-media reveal">{img('storage', 'Boxes stored on racking in a secure storage facility')}</div>
    <div class="reveal">
      <span class="eyebrow">Storage</span>
      <h2>Short and long-term storage: safe, organised, affordable</h2>
      <p>Completion dates that don’t line up? Renovating or downsizing? We collect, inventory and store your belongings securely, then deliver them to your new home when you’re ready.</p>
      <ul class="ticks"><li>Collection and delivery included</li><li>Secure, dry, monitored facility</li><li>Charged weekly — only pay for what you use</li></ul>
      <a class="btn btn-outline" href="storage.html">About our storage</a>
    </div>
  </div>
</section>

<section class="section section-green">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Why choose us</span><h2>Moving made calm</h2></div>
    <div class="grid grid-4">
      <div class="reveal"><div class="card-icon" style="background:rgba(255,255,255,.08);color:var(--gold)">{icon('clock')}</div><h3>On time</h3><p>We arrive when we say we will and keep you updated throughout the day.</p></div>
      <div class="reveal"><div class="card-icon" style="background:rgba(255,255,255,.08);color:var(--gold)">{icon('shield')}</div><h3>Careful</h3><p>Blankets, covers and floor protection on every job — your belongings and home stay safe.</p></div>
      <div class="reveal"><div class="card-icon" style="background:rgba(255,255,255,.08);color:var(--gold)">{icon('pound')}</div><h3>Honest prices</h3><p>A fixed price agreed in writing before the move, with nothing added on the day.</p></div>
      <div class="reveal"><div class="card-icon" style="background:rgba(255,255,255,.08);color:var(--gold)">{icon('leaf')}</div><h3>Truly local</h3><p>Based in Helmsley, we know Ryedale’s lanes, villages and market towns inside out.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <div class="section-head reveal"><span class="eyebrow">Questions</span><h2>Frequently asked questions</h2></div>
    {faq_block(FAQS[:5])}
    <p class="center mt-2"><a class="btn btn-outline" href="tips-faq.html">More tips & FAQs</a></p>
  </div>
</section>
{cta_band("Looking for a quality, affordable removals service?")}
"""
    page("index.html", f"{C['name']} | Removals in Helmsley, Ryedale & North Yorkshire",
         f"Helmsley-based removal company covering everywhere within {C['radius_miles']} miles — York, Malton, Pickering, Thirsk, Scarborough & Whitby. House & office moves, packing, storage and cleaning. Free fixed-price quotes.",
         body, schema=[faq_schema(FAQS[:5])])


def build_service(s):
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    sections = "".join(f"<h2>{escape(h)}</h2><p>{escape(p)}</p>" for h, p in s["body"])
    includes = "".join(f"<li>{escape(i)}</li>" for i in s["includes"])
    active_cls = ' class="active"'
    side_links = "".join(f'<li><a href="{o["slug"]}.html"{active_cls if o is s else ""}>{escape(o["title"])}</a></li>' for o in SERVICES)
    major = [t for t in TOWNS if t["major"]]
    towns = ", ".join(t["name"] for t in major[:-1]) + " and " + major[-1]["name"]
    body = f"""
{page_hero(escape(s['headline']), escape(s['short']), s['image'], [(None, s['group']), (None, s['title'])],
           f'<div class="hero-actions"><a class="btn btn-gold" href="quote.html?service={s["slug"]}">Get a free quote</a><a class="btn btn-light" href="tel:{C["phone_link"]}">{icon("phone")} {C["phone"]}</a></div>')}
<section class="section">
  <div class="container layout-side">
    <div class="prose">
      <p class="lead">{escape(s['intro'])}</p>
      <div class="split-media mb-2">{img(s['image'], s['title'])}</div>
      {sections}
      <h2>What’s included</h2>
      <ul class="ticks cols-2">{includes}</ul>
      <h2>Where we work</h2>
      <p>We’re based in {C['town']} and provide {s['title'].lower()} everywhere within {C['radius_miles']} miles, including {towns}, plus all the villages in between. <a href="areas.html">See our full coverage area</a>.</p>
      <h2>Questions about {escape(s['title'].lower())}</h2>
      {faq_block(s['faq'])}
    </div>
    <aside class="sidebar">
      <div class="side-box dark"><h3>Get a free quote</h3><p>Fixed-price quotes, usually within one working day.</p><a class="big-phone" href="tel:{C['phone_link']}">{C['phone']}</a><a class="btn btn-gold" href="quote.html?service={s['slug']}">Request a quote</a></div>
      <div class="side-box"><h3>All services</h3><ul>{side_links}</ul></div>
    </aside>
  </div>
</section>
<section class="section section-sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Also available</span><h2>Make your move easier</h2></div>
    <div class="grid grid-3">{service_cards(others[:3] if s['group'] == 'Services' else [o for o in others if o['group'] == 'Services'][:3])}</div>
  </div>
</section>
{cta_band()}
"""
    svc_schema = {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "description": s["intro"],
                  "serviceType": s["title"], "provider": {"@type": "MovingCompany", "name": C["name"], "url": C["domain"] + "/"},
                  "areaServed": [{"@type": "City", "name": t["name"]} for t in major]}
    page(f"{s['slug']}.html", f"{s['title']} in Helmsley, Ryedale & North Yorkshire",
         f"{s['short']} Based in Helmsley, covering {C['radius_miles']} miles including York, Malton, Pickering and the coast.",
         body, schema=[svc_schema, faq_schema(s["faq"]), breadcrumb_schema([(None, s["group"]), (f"{s['slug']}.html", s["title"])])],
         og_image=s["image"])


def build_areas():
    rows = "".join(
        f'<tr><td>{f"<a href={chr(34)}{area_slug(t["name"])}{chr(34)}>{escape(t["name"])}</a>" if t["name"] in AREA_COPY else escape(t["name"])}</td><td>{t["miles"]} miles</td></tr>'
        for t in TOWNS if t["name"] != C["town"])
    cards = "".join(f"""<article class="card reveal"><div class="card-body"><span class="tag">{t['miles']} miles from base</span><h3 style="margin-top:.7rem">{escape(t['name'])}</h3><p>{escape(AREA_COPY[t['name']][0])} — {escape(', '.join(AREA_COPY[t['name']][2][:3]))} and nearby.</p><a class="card-link" href="{area_slug(t['name'])}">Removals in {escape(t['name'])}</a></div></article>""" for t in AREA_TOWNS)
    body = f"""
{page_hero(f"Areas we cover: {C['radius_miles']} miles around Helmsley", "From the North York Moors to the coast and the Vale of York — local removals, packing and storage across Ryedale, Hambleton, Scarborough and York.", 'village', [(None, 'Areas we cover')])}
<section class="section">
  <div class="container area-wrap">
    <div class="area-map reveal">{area_map_svg()}</div>
    <div class="reveal">
      <span class="eyebrow">Our local area</span>
      <h2>Local removals, wherever you are in our {C['radius_miles']}-mile area</h2>
      <p>We’re based in {C['town']}, right at the centre of North Yorkshire. That puts the whole of Ryedale, the North York Moors National Park, the Howardian Hills, the Vale of York, Thirsk and Northallerton, and the coast from Whitby to Scarborough within easy reach.</p>
      <p>Being local means lower travel costs for you, crews who know the roads and access, and a team that can be with you early in the morning on moving day.</p>
      <p class="notice"><strong>Moving further afield?</strong> We also move customers to and from anywhere in the UK, and arrange European moves. <a href="long-distance-removals.html">Long distance removals →</a></p>
    </div>
  </div>
</section>
<section class="section section-sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Towns we cover</span><h2>Removals in your town</h2></div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
<section class="section">
  <div class="container narrow">
    <div class="section-head reveal"><h2>Distance from our Helmsley base</h2><p class="muted">Straight-line distances to towns and villages in our area. Don’t see yours? If it’s within {C['radius_miles']} miles of Helmsley, we cover it.</p></div>
    <table class="dist-table reveal"><thead><tr><th>Town / village</th><th>Distance</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
</section>
{cta_band()}
"""
    page("areas.html", f"Areas We Cover — Removals within {C['radius_miles']} Miles of Helmsley",
         f"{C['name']} covers everywhere within {C['radius_miles']} miles of Helmsley: York, Malton, Pickering, Kirkbymoorside, Thirsk, Easingwold, Northallerton, Stokesley, Ripon, Scarborough and Whitby.",
         body, schema=[breadcrumb_schema([("areas.html", "Areas we cover")])], og_image="village")


def build_area(t):
    heading, para, villages = AREA_COPY[t["name"]]
    name = t["name"]
    nearby = [o for o in AREA_TOWNS if o["name"] != name][:6]
    near_links = "".join(f'<li><a href="{area_slug(o["name"])}">{escape(o["name"])}</a></li>' for o in nearby)
    vill = "".join(f"<li><span>{escape(v)}</span></li>" for v in villages)
    svc_list = "".join(f'<li><a href="{s["slug"]}.html">{escape(s["title"])}</a></li>' for s in SERVICES)
    dist = "our home base" if name == C["town"] else f"about {t['miles']} miles from our {C['town']} base"
    body = f"""
{page_hero(f"Removals in {escape(name)}", f"House removals, man & van, packing, storage and cleaning in {escape(name)} — {dist}.", 'domestic' if name != 'Helmsley' else 'hero', [('areas.html', 'Areas'), (None, name)],
           f'<div class="hero-actions"><a class="btn btn-gold" href="quote.html">Get a free quote</a><a class="btn btn-light" href="tel:{C["phone_link"]}">{icon("phone")} {C["phone"]}</a></div>')}
<section class="section">
  <div class="container layout-side">
    <div class="prose">
      <span class="eyebrow">{escape(heading)}</span>
      <h2 style="margin-top:0">Your local removal company for {escape(name)}</h2>
      <p class="lead">{escape(para)}</p>
      <p>Whether you’re moving within {escape(name)}, into the area or out of it, {C['name']} gives you a free survey, a clear fixed-price quote and a friendly, careful crew on the day. We bring the right size vehicle for your street and protect your home at both ends.</p>
      <h3>Villages and areas near {escape(name)}</h3>
      <ul class="town-list">{vill}</ul>
      <h3>Our services in {escape(name)}</h3>
      <ul class="ticks cols-2">{svc_list}</ul>
      <h3>Why {escape(name)} customers choose us</h3>
      <ul class="ticks"><li>Local crews who know {escape(name)}’s streets, parking and access</li><li>Free home or video survey and a fixed written price</li><li>Fully insured, with blankets and covers on every job</li><li>Packing, storage and cleaning available in one booking</li></ul>
    </div>
    <aside class="sidebar">
      <div class="side-box dark"><h3>Moving in {escape(name)}?</h3><p>Get a free, fixed-price quote.</p><a class="big-phone" href="tel:{C['phone_link']}">{C['phone']}</a><a class="btn btn-gold" href="quote.html">Request a quote</a></div>
      <div class="side-box"><h3>Nearby areas</h3><ul>{near_links}<li><a href="areas.html">All areas →</a></li></ul></div>
    </aside>
  </div>
</section>
{cta_band(f"Moving to or from {escape(name)}?")}
"""
    page(area_slug(name), f"Removals {name} — House & Office Removals in {name}",
         f"Local removals in {name}, North Yorkshire. House moves, man & van, packing, storage and cleaning from {C['name']} — {dist}. Free fixed-price quotes.",
         body, schema=[breadcrumb_schema([("areas.html", "Areas"), (area_slug(name), name)])], og_image="domestic")


def build_fleet():
    vans = [
        ("small", "Small van", "Single items, small flats, student moves, auction collections", [("Load space", "Around 10 m³"), ("Crew", "1–2 people"), ("Typical move", "Studio / single items")], "Narrow lanes, city centres and quick local jobs."),
        ("luton", "Luton van", "Covered box van with tail-lift for one and two-bedroom homes", [("Load space", "Around 20 m³"), ("Crew", "2 people"), ("Typical move", "1–2 bedroom home")], "Cottages, flats and part-loads — with a tail-lift for heavy items."),
        ("lorry", "Removal lorry", "Large purpose-built removal vehicle for family homes and offices", [("Load space", "Around 40 m³+"), ("Crew", "3–4 people"), ("Typical move", "3–5 bedroom home")], "Family homes, farmhouses and office relocations in one trip."),
    ]
    cards = ""
    for kind, name, sub, specs, best in vans:
        dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in specs)
        cards += f'<article class="fleet-card reveal">{vehicle_svg(kind)}<h3>{name}</h3><p class="muted">{sub}</p><dl>{dl}</dl><p class="best"><strong>Best for:</strong> {best}</p></article>'
    body = f"""
{page_hero("Our fleet", "The right vehicle for every move — from nimble vans for village lanes to full-size removal lorries.", 'team', [(None, 'Our fleet')])}
<section class="section">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Vehicles</span><h2>Choosing the right size</h2><p class="lead">We’ll recommend the right vehicle during your survey. Where a lorry can’t reach your door, we use a smaller van to shuttle, so nothing is carried further than it needs to be.</p></div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
<section class="section section-sand">
  <div class="container split">
    <div class="split-media reveal">{img('packing', 'Crew wrapping a sofa in protective covers before loading')}</div>
    <div class="reveal">
      <span class="eyebrow">Equipped for care</span>
      <h2>Every vehicle carries the kit to do the job properly</h2>
      <ul class="ticks"><li>Furniture blankets and quilted covers</li><li>Mattress and sofa covers</li><li>Floor runners and door-frame protectors</li><li>Straps, ties and load bars</li><li>Sack trucks, dollies and piano boards</li><li>Tool kits for dismantling and reassembly</li></ul>
      <a class="btn btn-primary" href="quote.html">Get a free quote</a>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("fleet.html", "Our Fleet — Removal Vans & Lorries",
         "Small vans, Luton vans with tail-lifts and full-size removal lorries — the right vehicle for every move across Helmsley, Ryedale and North Yorkshire.",
         body, schema=[breadcrumb_schema([("fleet.html", "Our fleet")])], og_image="team")


def build_about():
    body = f"""
{page_hero(f"About {C['name']}", "The art of moving, done the Yorkshire way: careful, honest and on time.", 'team', [(None, 'About us')])}
<section class="section">
  <div class="container split">
    <div class="split-media reveal">{img('domestic', 'Removal crew wrapping and moving furniture in a home')}</div>
    <div class="reveal">
      <span class="eyebrow">Some words about us</span>
      <h2>A Helmsley removal company, serving the heart of North Yorkshire</h2>
      <p>{C['name']} is a local removal company based in {C['town']}, on the edge of the North York Moors. We move families, businesses and individual items across Ryedale and everywhere within {C['radius_miles']} miles — from moorland villages and market towns to York and the coast.</p>
      <p>We started with a simple idea: people should be able to book a removal company and stop worrying. That means turning up on time, protecting your home, handling your belongings like they were our own, and charging the price we quoted.</p>
    </div>
  </div>
</section>
<section class="section section-sand">
  <div class="container grid grid-3">
    <div class="feature reveal"><div class="card-icon">{icon('star')}</div><h3>Our mission</h3><p>To give every customer a calm, well-organised move, delivered by friendly people who take pride in their work.</p></div>
    <div class="feature reveal"><div class="card-icon">{icon('leaf')}</div><h3>Our philosophy</h3><p>Honest advice, fair fixed prices and doing the job properly — the kind of service that earns recommendations from neighbours.</p></div>
    <div class="feature reveal"><div class="card-icon">{icon('pin')}</div><h3>Our area</h3><p>We know Ryedale’s lanes, villages and towns, from Rosedale to Malton and Thirsk to Scarborough. Local knowledge makes moves smoother.</p></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">What sets us apart</span><h2>The details that make a difference</h2></div>
    <div class="grid grid-4">
      <div class="feature reveal"><div class="card-icon">{icon('clock')}</div><h3>Fast, organised moves</h3><p>Methodical loading and a clear plan for the day mean less waiting and a quicker move.</p></div>
      <div class="feature reveal"><div class="card-icon">{icon('check')}</div><h3>Secure checklist</h3><p>Inventories, labelled fixings and a final walk-round so nothing is left behind.</p></div>
      <div class="feature reveal"><div class="card-icon">{icon('piano')}</div><h3>Heavy furniture</h3><p>Pianos, antiques, range cookers and safes moved with the right equipment.</p></div>
      <div class="feature reveal"><div class="card-icon">{icon('office')}</div><h3>Commercial service</h3><p>Office, shop and holiday-let moves planned around your business.</p></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    page("about.html", f"About Us — Helmsley Removal Company",
         f"{C['name']} is a friendly, local removal company based in Helmsley, serving Ryedale, the North York Moors, York and the coast within {C['radius_miles']} miles.",
         body, schema=[breadcrumb_schema([("about.html", "About us")])], og_image="team")


def build_tips():
    tips = "".join(f'<div class="feature reveal"><h3>{i}. {escape(t)}</h3><p>{escape(d)}</p></div>' for i, (t, d) in enumerate(TIPS, 1))
    body = f"""
{page_hero("Removal tips & FAQ", "Answers to the questions we’re asked most, and our crews’ best advice for a smoother move.", 'room', [(None, 'Tips & FAQ')])}
<section class="section">
  <div class="container narrow">
    <div class="section-head reveal"><span class="eyebrow">FAQ</span><h2>Frequently asked questions</h2></div>
    {faq_block(FAQS)}
  </div>
</section>
<section class="section section-sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">From our crews</span><h2>Top removal tips</h2></div>
    <div class="grid grid-4">{tips}</div>
    <p class="center mt-2"><a class="btn btn-outline" href="guides.html">Read our moving guides</a></p>
  </div>
</section>
{cta_band()}
"""
    page("tips-faq.html", "Removal Tips & Frequently Asked Questions",
         "Answers to common removal questions — costs, insurance, booking, packing and storage — plus our crews’ top moving tips.",
         body, schema=[faq_schema(FAQS), breadcrumb_schema([("tips-faq.html", "Tips & FAQ")])], og_image="room")


def build_guides():
    cards = "".join(f"""<article class="card reveal"><div class="card-img">{img(g['image'], g['title'], sizes='(max-width: 640px) 100vw, 33vw')}</div><div class="card-body"><h3>{escape(g['title'])}</h3><p>{escape(g['desc'])}</p><a class="card-link" href="{g['slug']}.html">Read guide</a></div></article>""" for g in GUIDES)
    body = f"""
{page_hero("Moving guides", "Practical advice from our removal crews to help you plan, pack and settle in.", 'boxes', [(None, 'Moving guides')])}
<section class="section"><div class="container"><div class="grid grid-3">{cards}</div></div></section>
{cta_band()}
"""
    page("guides.html", "Moving Guides & Advice", "Moving checklists, packing tips and advice on moving to Ryedale and the North York Moors from Helmsley’s local removal company.",
         body, schema=[breadcrumb_schema([("guides.html", "Moving guides")])], og_image="boxes")
    for g in GUIDES:
        others = "".join(f'<li><a href="{o["slug"]}.html">{escape(o["title"])}</a></li>' for o in GUIDES if o is not g)
        body = f"""
{page_hero(escape(g['title']), escape(g['desc']), g['image'], [('guides.html', 'Moving guides'), (None, g['title'])])}
<section class="section">
  <div class="container layout-side">
    <article class="prose">{g['body']}</article>
    <aside class="sidebar">
      <div class="side-box dark"><h3>Need a hand?</h3><p>Free, fixed-price removal quotes across North Yorkshire.</p><a class="big-phone" href="tel:{C['phone_link']}">{C['phone']}</a><a class="btn btn-gold" href="quote.html">Get a quote</a></div>
      <div class="side-box"><h3>More guides</h3><ul>{others}<li><a href="tips-faq.html">Tips & FAQ</a></li></ul></div>
    </aside>
  </div>
</section>
{cta_band()}
"""
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
               "image": f"{C['domain']}/assets/img/{g['image']}-1600.jpg", "author": {"@type": "Organization", "name": C["name"]},
               "publisher": {"@type": "Organization", "name": C["name"]}}
        page(f"{g['slug']}.html", g["title"], g["desc"], body,
             schema=[art, breadcrumb_schema([("guides.html", "Moving guides"), (f"{g['slug']}.html", g["title"])])], og_image=g["image"])


def form_open(name, cls="", attrs=""):
    return (f'<form class="{cls}" action="{C["form_action"]}" method="post" data-ajax {attrs}>'
            f'<input type="hidden" name="form" value="{name}">'
            f'<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>')


def address_fields(prefix, title):
    p = prefix
    return f"""<h3>{title}</h3>
<div class="form-grid">
  <div class="full"><label for="{p}_address">Address</label><input type="text" id="{p}_address" name="{p}_address" data-label="{title} – address" autocomplete="street-address"></div>
  <div><label for="{p}_town">Town / village</label><input type="text" id="{p}_town" name="{p}_town" data-label="{title} – town" required></div>
  <div><label for="{p}_postcode">Postcode</label><input type="text" id="{p}_postcode" name="{p}_postcode" data-label="{title} – postcode" required autocomplete="postal-code"></div>
  <div><label for="{p}_type">Property type</label><select id="{p}_type" name="{p}_type" data-label="{title} – property type"><option value="">Select…</option><option>Detached house</option><option>Semi-detached house</option><option>Terraced house / cottage</option><option>Bungalow</option><option>Flat / apartment</option><option>Farmhouse</option><option>Office / commercial</option><option>Storage unit</option><option>Other</option></select></div>
  <div><label for="{p}_floor">Floor</label><select id="{p}_floor" name="{p}_floor" data-label="{title} – floor"><option value="">Select…</option><option>Ground floor</option><option>First floor</option><option>Second floor</option><option>Third floor or higher</option></select></div>
  <div><label for="{p}_lift">Lift</label><select id="{p}_lift" name="{p}_lift" data-label="{title} – lift"><option value="">Select…</option><option>No lift needed</option><option>With lift</option><option>Without lift (stairs)</option></select></div>
  <div><label for="{p}_parking">Parking & access</label><select id="{p}_parking" name="{p}_parking" data-label="{title} – parking"><option value="">Select…</option><option>Driveway</option><option>On-street, easy</option><option>On-street, restricted / busy</option><option>Narrow lane or track</option><option>Not sure</option></select></div>
  <div class="full"><label for="{p}_notes">Access notes <span class="opt">(optional)</span></label><input type="text" id="{p}_notes" name="{p}_notes" data-label="{title} – access notes" placeholder="e.g. steep drive, low bridge, steps to front door"></div>
</div>"""


def build_quote():
    svc_checks = "".join(
        f'<label class="check"><input type="checkbox" name="services[]" value="{escape(s["title"])}" data-slug="{s["slug"]}" data-label="Services"> {escape(s["title"])}</label>' for s in SERVICES)
    extras = ["Packing service", "Fragile-only packing", "Boxes & materials", "Dismantling & reassembly", "Storage", "End of move cleaning", "Piano", "Antiques / artwork", "Range cooker / heavy items"]
    extra_checks = "".join(f'<label class="check"><input type="checkbox" name="extras[]" value="{e}" data-label="Extras"> {e}</label>' for e in extras)
    body = f"""
{page_hero("Get a free removal quote", "Tell us about your move and we’ll send a free, fixed-price quote — usually within one working day.", 'boxes', [(None, 'Free quote')])}
<section class="section section-sand">
  <div class="container layout-side">
    <div class="form-card">
      <ol class="wizard-progress" aria-hidden="true"><li>Your move</li><li>Moving from</li><li>Moving to</li><li>Extras</li><li>Your details</li></ol>
      {form_open('Quote request', '', 'data-wizard data-success="Thank you! Your quote request has been sent. We’ll be in touch within one working day."')}
        <div class="wizard-step">
          <h3>About your move</h3>
          <fieldset><legend>What do you need?</legend><div class="check-grid">{svc_checks}</div></fieldset>
          <div class="form-grid">
            <div><label for="move_date">Preferred moving date</label><input type="date" id="move_date" name="move_date" data-label="Preferred date"></div>
            <div><label for="flexible">Are your dates flexible?</label><select id="flexible" name="flexible" data-label="Flexible dates"><option value="">Select…</option><option>Yes, flexible</option><option>Within a week or two</option><option>No, fixed date</option><option>Don’t know yet</option></select></div>
            <div><label for="bedrooms">Size of move</label><select id="bedrooms" name="bedrooms" data-label="Size of move" required><option value="">Select…</option><option>Single item(s)</option><option>Studio / 1 bedroom</option><option>2 bedrooms</option><option>3 bedrooms</option><option>4 bedrooms</option><option>5+ bedrooms</option><option>Office / commercial</option></select></div>
            <div><label for="survey">Survey preference</label><select id="survey" name="survey" data-label="Survey"><option value="">Select…</option><option>Home visit</option><option>Video call</option><option>No survey needed (small move)</option></select></div>
          </div>
        </div>
        <div class="wizard-step">{address_fields('from', 'Moving from')}</div>
        <div class="wizard-step">{address_fields('to', 'Moving to')}</div>
        <div class="wizard-step">
          <h3>Extras & special items</h3>
          <fieldset><legend>Anything else we can help with?</legend><div class="check-grid">{extra_checks}</div></fieldset>
          <label for="inventory">Describe your property and belongings <span class="opt">(rooms, large furniture, anything heavy or valuable)</span></label>
          <textarea id="inventory" name="inventory" data-label="Belongings"></textarea>
        </div>
        <div class="wizard-step">
          <h3>Your details</h3>
          <div class="form-grid">
            <div><label for="q_name">Full name</label><input type="text" id="q_name" name="name" data-label="Name" required autocomplete="name"></div>
            <div><label for="q_phone">Phone</label><input type="tel" id="q_phone" name="phone" data-label="Phone" required autocomplete="tel"></div>
            <div class="full"><label for="q_email">Email</label><input type="email" id="q_email" name="email" data-label="Email" required autocomplete="email"></div>
            <div class="full"><label for="q_message">Anything else? <span class="opt">(optional)</span></label><textarea id="q_message" name="message" data-label="Message" style="min-height:90px"></textarea></div>
          </div>
          <h4 class="mt-2">Check your details</h4>
          <dl class="summary-list" data-summary></dl>
          <p class="form-note">By sending this form you agree to us contacting you about your move. See our <a href="privacy.html">privacy policy</a>.</p>
        </div>
        <div class="wizard-nav">
          <button type="button" class="btn btn-outline" data-prev>← Back</button>
          <span style="margin-left:auto;display:flex;gap:.8rem">
            <button type="button" class="btn btn-primary" data-next>Next →</button>
            <button type="submit" class="btn btn-primary">Send my quote request</button>
          </span>
        </div>
        <div class="form-status" role="status" aria-live="polite"></div>
      </form>
    </div>
    <aside class="sidebar">
      <div class="side-box dark"><h3>Prefer to talk?</h3><p>Call us for a quick chat about your move.</p><a class="big-phone" href="tel:{C['phone_link']}">{C['phone']}</a><p style="margin:0">{C['hours'][0][0]}: {C['hours'][0][1]}<br>{C['hours'][1][0]}: {C['hours'][1][1]}</p></div>
      <div class="side-box"><h3>What happens next?</h3><ul class="ticks" style="margin:0"><li>We review your details</li><li>We arrange a survey if needed</li><li>You get a fixed written price</li><li>Book your date with a small deposit</li></ul></div>
    </aside>
  </div>
</section>
"""
    page("quote.html", "Get a Free Removal Quote", f"Request a free, fixed-price removal quote from {C['name']} — house moves, man & van, office moves, packing, storage and cleaning across North Yorkshire.",
         body, schema=[breadcrumb_schema([("quote.html", "Free quote")])], og_image="boxes")


def build_contact():
    hours = "".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d, h in C["hours"])
    body = f"""
{page_hero("Contact us", f"Call, email or send us a message — we’re here to help with your move anywhere within {C['radius_miles']} miles of Helmsley.", 'team', [(None, 'Contact')])}
<section class="section">
  <div class="container split" style="align-items:start">
    <div class="reveal">
      <span class="eyebrow">Get in touch</span>
      <h2>Talk to our team</h2>
      <p class="lead">For a quote, the quickest way is our <a href="quote.html">online quote form</a>. For anything else, use the details below.</p>
      <div class="contact-item"><div class="card-icon">{icon('phone')}</div><div><h4>Phone</h4><a href="tel:{C['phone_link']}">{C['phone']}</a><br><a href="tel:{C['mobile_link']}">{C['mobile']}</a> <span class="muted">(mobile)</span></div></div>
      <div class="contact-item"><div class="card-icon">{icon('mail')}</div><div><h4>Email</h4><a href="mailto:{C['email']}">{C['email']}</a></div></div>
      <div class="contact-item"><div class="card-icon">{icon('pin')}</div><div><h4>Based in</h4><p>{escape(address_line())}</p></div></div>
      <div class="contact-item"><div class="card-icon">{icon('clock')}</div><div style="flex:1"><h4>Opening hours</h4><table class="hours">{hours}</table></div></div>
    </div>
    <div class="form-card reveal">
      <h3>Send us a message</h3>
      {form_open('Contact message', '', 'data-success="Thanks for your message — we’ll get back to you shortly."')}
        <div class="form-grid">
          <div><label for="c_name">Name</label><input type="text" id="c_name" name="name" required autocomplete="name"></div>
          <div><label for="c_phone">Phone <span class="opt">(optional)</span></label><input type="tel" id="c_phone" name="phone" autocomplete="tel"></div>
          <div class="full"><label for="c_email">Email</label><input type="email" id="c_email" name="email" required autocomplete="email"></div>
          <div class="full"><label for="c_subject">Subject</label><select id="c_subject" name="subject"><option>General enquiry</option><option>Existing booking</option><option>Storage</option><option>Business / commercial</option><option>Other</option></select></div>
          <div class="full"><label for="c_message">Message</label><textarea id="c_message" name="message" required></textarea></div>
        </div>
        <button class="btn btn-primary mt-2" type="submit">Send message</button>
        <div class="form-status" role="status" aria-live="polite"></div>
        <p class="form-note">We’ll only use your details to reply to you. See our <a href="privacy.html">privacy policy</a>.</p>
      </form>
    </div>
  </div>
</section>
<section class="section section-sand">
  <div class="container area-wrap">
    <div class="area-map reveal">{area_map_svg()}</div>
    <div class="reveal"><span class="eyebrow">Where we work</span><h2>Covering {C['radius_miles']} miles around {C['town']}</h2><p>Ryedale, the North York Moors, Hambleton, the Howardian Hills, the Vale of York, York and the coast from Whitby to Scarborough.</p><a class="btn btn-outline" href="areas.html">See all areas</a></div>
  </div>
</section>
"""
    page("contact.html", "Contact Us", f"Contact {C['name']} in Helmsley — call {C['phone']} or email {C['email']} for removals, storage and packing across North Yorkshire.",
         body, schema=[breadcrumb_schema([("contact.html", "Contact")])], og_image="team")


def build_simple(filename, title, desc, h1, lead, content, noindex=False):
    body = f"""
{page_hero(h1, lead, 'room', [(None, h1)])}
<section class="section"><div class="container"><div class="prose">{content}</div></div></section>
"""
    page(filename, title, desc, body, noindex=noindex)


def build_legal():
    privacy = f"""
<p class="meta">Last updated: {date.today().strftime('%B %Y')}</p>
<p>{C['name']} (“we”, “us”) respects your privacy. This policy explains what personal information we collect through this website and how we use it.</p>
<h2>What we collect</h2>
<p>When you request a quote or contact us, we collect the details you give us: your name, email address, phone number, addresses and information about your move.</p>
<h2>How we use it</h2>
<ul><li>To respond to your enquiry and provide a quote</li><li>To plan and carry out your move, storage or other services</li><li>To keep records required for accounting and insurance</li></ul>
<p>We do not sell your information or use it for unrelated marketing.</p>
<h2>Lawful basis</h2>
<p>We process your information to take steps at your request before entering into a contract, to perform our contract with you, and to meet our legal obligations.</p>
<h2>How long we keep it</h2>
<p>Enquiries that don’t lead to a booking are deleted within 12 months. Records of completed jobs are kept for as long as required for tax and insurance purposes.</p>
<h2>Cookies</h2>
<p>This website does not set tracking or advertising cookies. Fonts are loaded from Google Fonts, which may log your IP address.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete the information we hold about you by emailing <a href="mailto:{C['email']}">{C['email']}</a>. You also have the right to complain to the Information Commissioner’s Office (ico.org.uk).</p>
<h2>Contact</h2>
<p>{C['name']}, {escape(address_line())}. Email <a href="mailto:{C['email']}">{C['email']}</a>, phone {C['phone']}.</p>
"""
    build_simple("privacy.html", "Privacy Policy", f"How {C['name']} collects and uses your personal information.", "Privacy policy", "How we look after your information.", privacy)
    terms = f"""
<p class="meta">Last updated: {date.today().strftime('%B %Y')}</p>
<p class="notice">This is a summary of how we work. Your written quotation and full terms and conditions, supplied when you book, form the contract between us.</p>
<h2>Quotations</h2>
<p>Quotes are fixed for the work and volume described at survey. If the volume, access or services change significantly, we’ll agree a revised price with you before the move.</p>
<h2>Booking and deposits</h2>
<p>A deposit secures your moving date. The balance is payable as set out in your quotation. Dates can be changed with reasonable notice, subject to availability.</p>
<h2>Cancellations</h2>
<p>Please give us as much notice as possible if you need to cancel. Cancellation charges, if any, are set out in your quotation.</p>
<h2>Your responsibilities</h2>
<ul><li>Tell us about any access restrictions, parking issues or items needing special care</li><li>Keep valuables, cash, jewellery, documents and medication with you</li><li>Do not ask us to move hazardous materials (gas bottles, fuel, chemicals, ammunition)</li><li>Defrost fridges and freezers and disconnect appliances before we arrive</li></ul>
<h2>Insurance and liability</h2>
<p>Goods are covered while in our care in line with the insurance details given in your quotation. Please check items on delivery and report any damage within the timescale set out in your terms.</p>
<h2>Storage</h2>
<p>Storage is charged weekly in advance unless otherwise agreed. Goods are held subject to our storage terms, supplied on request.</p>
"""
    build_simple("terms.html", "Terms of Service", f"A summary of {C['name']}’s booking terms.", "Terms of service", "How our quotes, bookings and insurance work.", terms)
    build_simple("thank-you.html", "Thank You", "Thanks for contacting us.", "Thank you!", "Your message has been sent.",
                 f"<p class='lead'>We’ve received your details and will be in touch within one working day. If your move is urgent, please call us on <a href='tel:{C['phone_link']}'>{C['phone']}</a>.</p><p><a class='btn btn-primary' href='index.html'>Back to home</a></p>", noindex=True)
    build_simple("404.html", "Page Not Found", "Page not found.", "Page not found", "Sorry, we couldn’t find that page.",
                 "<p class='lead'>The page may have moved. Try one of these instead:</p><ul class='ticks'><li><a href='index.html'>Home</a></li><li><a href='quote.html'>Get a free quote</a></li><li><a href='areas.html'>Areas we cover</a></li><li><a href='contact.html'>Contact us</a></li></ul>", noindex=True)


def build_extras():
    urls = "".join(
        f"<url><loc>{C['domain']}/{'' if f == 'index.html' else f}</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n"
        for f, noindex in PAGES if not noindex)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\nDisallow: /send.php\n\nSitemap: {C['domain']}/sitemap.xml\n")
    with open(os.path.join(OUT, "site.webmanifest"), "w") as fh:
        json.dump({"name": C["name"], "short_name": "Ryedale Removals", "start_url": "/", "display": "standalone",
                   "background_color": "#ffffff", "theme_color": "#1b3a29",
                   "icons": [{"src": "assets/img/logo.svg", "sizes": "any", "type": "image/svg+xml"},
                             {"src": "assets/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, fh, indent=2)
    with open(os.path.join(OUT, "assets", "img", "logo.svg"), "w") as fh:
        fh.write(LOGO_SVG.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    with open(os.path.join(OUT, ".htaccess"), "w") as fh:
        fh.write("ErrorDocument 404 /404.html\n\n<IfModule mod_expires.c>\n  ExpiresActive On\n  ExpiresByType image/webp \"access plus 1 year\"\n  ExpiresByType image/jpeg \"access plus 1 year\"\n  ExpiresByType image/svg+xml \"access plus 1 year\"\n  ExpiresByType text/css \"access plus 1 month\"\n  ExpiresByType application/javascript \"access plus 1 month\"\n</IfModule>\n\n<IfModule mod_deflate.c>\n  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json\n</IfModule>\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    build_home()
    for s in SERVICES:
        build_service(s)
    build_areas()
    for t in AREA_TOWNS:
        build_area(t)
    build_fleet()
    build_about()
    build_tips()
    build_guides()
    build_quote()
    build_contact()
    build_legal()
    build_extras()
    print(f"Built {len(PAGES)} pages into {OUT}")
    print(f"Towns within {C['radius_miles']} miles: {len(TOWNS)} ({', '.join(t['name'] for t in TOWNS)})")


if __name__ == "__main__":
    main()
