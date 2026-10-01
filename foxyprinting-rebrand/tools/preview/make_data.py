"""Builds tools/preview/data.json (mock store data for the offline theme preview) from the plan."""
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "plan"))
sys.path.insert(0, str(ROOT / "tools"))
import build_plan  # noqa: E402
import mega_menu  # noqa: E402

EMOJI = [("bauble|decoration|key", "🎄"), ("christmas eve|advent|selection|reindeer|santa|elf", "🎅"), ("can cup|tumbler", "🥤"),
         ("glass|flute", "🥂"), ("bottle", "🧴"), ("mug|cup", "☕"), ("candle", "🕯️"), ("jar", "🍬"), ("baby", "👶"),
         ("dog|pet", "🐶"), ("hoodie|t-shirt|jumper|pyjama|polo", "👕"), ("bag", "👜"), ("golf", "⛳"), ("dart", "🎯"),
         ("game", "🎮"), ("phone", "📱"), ("slate", "🪨"), ("wood|bamboo", "🪵"), ("acrylic|photo", "💎"), ("card", "💌"),
         ("sticker|label", "🏷️"), ("box", "📦"), ("wedding", "💍"), ("halloween|trick", "🎃"), ("easter", "🐣")]
PALETTE = [("#FF6A13", "#FFC83D"), ("#FF2D87", "#FF6A13"), ("#7A2BF5", "#FF2D87"), ("#00B8A9", "#7A2BF5"), ("#FFC83D", "#00B8A9")]


def emoji(title):
    import re
    t = title.lower()
    for pat, e in EMOJI:
        if re.search(pat, t):
            return e
    return "🎁"


def svg(title, i):
    a, b = PALETTE[i % len(PALETTE)]
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
         f"<stop offset='0' stop-color='{a}'/><stop offset='1' stop-color='{b}'/></linearGradient></defs>"
         f"<rect width='600' height='600' fill='url(#g)'/><circle cx='480' cy='110' r='120' fill='rgba(255,255,255,.18)'/>"
         f"<circle cx='300' cy='300' r='170' fill='rgba(255,255,255,.92)'/>"
         f"<text x='300' y='350' font-size='150' text-anchor='middle'>{emoji(title)}</text></svg>")
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(s)


def product(p, i, url="#"):
    cents = [round(price * 100) for _, price in p["values"]]
    variants = [{"id": 50000 + i * 20 + n, "title": v, "options": [v], "price": c, "compare_at_price": None, "available": True}
                for n, ((v, _), c) in enumerate(zip(p["values"], cents))]
    only_default = p["option"] == "Title"
    media = {"src": svg(p["title"], i), "alt": p["title"], "media_type": "image"}
    return {
        "title": p["title"], "handle": p["handle"], "url": url, "type": p["product_type"],
        "description": p["body"], "tags": p["tags"],
        "price": min(cents), "price_min": min(cents), "price_varies": len(set(cents)) > 1,
        "compare_at_price": None, "variants": variants, "selected_or_first_available_variant": variants[0],
        "has_only_default_variant": only_default,
        "options_with_values": [] if only_default else [{"name": p["option"], "values": [v for v, _ in p["values"]], "selected_value": p["values"][0][0]}],
        "featured_media": media, "media": [media],
        "metafields": {"foxy": {"mockup": {"value": p["mockup"]},
                                "personalise_fields": {"value": p["personalise"] or None}}},
    }


def main():
    plan = build_plan.build()
    pages = {
        "personalised-glass-can-cup-with-bamboo-lid-straw-16oz": "product-can-cup.html",
        "personalised-christmas-eve-box": "product-christmas-eve-box.html",
        "personalised-name-bauble": "product-bauble.html",
        "personalised-kids-t-shirt": "product-tshirt.html",
        "personalised-photo-slate-plaque": "product-slate.html",
        "personalised-video-game-case-put-yourself-on-the-cover": "product-game-case.html",
        "personalised-40oz-tumbler-with-handle": "product-tumbler.html",
    }
    prods = [product(p, i, pages.get(p["handle"], "#")) for i, p in enumerate(plan)]
    # A greeting card using the card template (front + inside preview), like the existing 6,000+ card range.
    card = product({"title": "Happy Birthday Confetti Personalised Card", "handle": "happy-birthday-confetti-card",
                    "product_type": "Personalised Cards", "body": "<p>Printed inside and out on 350gsm card with envelope.</p>",
                    "tags": ["Birthday Card", "personalised", "trending"], "values": [("Standard A5", 2.99), ("Large A4", 4.99)],
                    "option": "Size", "mockup": "card", "personalise": None}, 900, "product-card.html")
    card["featured_media"] = None
    card["media"] = []
    card["template"] = "product.card"
    prods.insert(0, card)
    pages["happy-birthday-confetti-card"] = "product-card.html"

    trending = [p["handle"] for p in prods if "trending" in p["tags"]][:12]
    christmas = [p["handle"] for p in prods if any(t in p["tags"] for t in ("wave-1",))][:8]
    data = {
        "menu": mega_menu.as_json(),
        "products": prods,
        "collections": {
            "trending": {"title": "Trending Personalised Gifts", "products": trending,
                         "description": "<p>The gifts everyone's talking about — all personalised and printed in the UK.</p>",
                         "filters": [
                             {"label": "Product type", "type": "list", "active_values": [], "values": [
                                 {"label": "Drinkware", "value": "drinkware", "count": 12, "param_name": "filter.p.product_type", "active": False},
                                 {"label": "Clothing", "value": "clothing", "count": 30, "param_name": "filter.p.product_type", "active": False},
                                 {"label": "Christmas", "value": "christmas", "count": 22, "param_name": "filter.p.product_type", "active": False}]},
                             {"label": "Recipient", "type": "list", "active_values": [], "values": [
                                 {"label": "For Her", "value": "her", "count": 40, "param_name": "filter.p.m.custom.recipient", "active": False},
                                 {"label": "For Him", "value": "him", "count": 35, "param_name": "filter.p.m.custom.recipient", "active": False},
                                 {"label": "For Kids", "value": "kids", "count": 28, "param_name": "filter.p.m.custom.recipient", "active": False}]},
                             {"label": "Price", "type": "price_range", "active_values": [],
                              "min_value": {"param_name": "filter.v.price.gte", "value": None},
                              "max_value": {"param_name": "filter.v.price.lte", "value": None}}]},
            "christmas": {"title": "Christmas 2026", "products": christmas},
        },
        "productPages": pages,
    }
    out = Path(__file__).with_name("data.json")
    out.write_text(json.dumps(data))
    print("wrote", out, len(prods), "products")


if __name__ == "__main__":
    main()
