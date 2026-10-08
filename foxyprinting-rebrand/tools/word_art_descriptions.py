"""Rewrite the 53 "Personalised Name Word Art Poster Print" descriptions and tidy
their images (8 Oct 2026). Owner: "you need to check the descriptions of the word
art posters something is wrong" and "there seems to be a birthday card image??".

Facts come only from the owner's old copy (see plan/product-facts.md, "Personalised
name word art prints"). Usage:
  python3 tools/word_art_descriptions.py <out_dir>
Reads exports/word-art/2026-10-06-sizes/after.json (variant ids) and
<out_dir>/media_before.txt (media ids + file names). Writes <out_dir>/plan.json
(per product: new HTML, alts, media moves, variant media) and
<out_dir>/batch_NN.graphql + batch_NN.vars.json (4 products per call)."""
import json, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFTER = os.path.join(ROOT, "exports/word-art/2026-10-06-sizes/after.json")

FIELDS = ["Name (shown largest)", "Your words message (20–30 words, separated by commas)"]

OPENINGS = [
    "A personalised name word art print is one of those gifts that people keep for years, and this one is built around a big {c} letter {L}, filled with the words that mean the most to them.",
    "Looking for a gift with real meaning? This personalised name word art print turns a big {c} letter {L} into a keepsake made entirely from their name and the words you choose.",
    "Our personalised name word art print takes a bold {c} letter {L} and fills it with a name and a list of words that sum someone up: their hobbies, their habits, the people they love.",
    "Every personalised name word art print we make is different, because every word on it comes from you. This design is a big {c} letter {L}, ideal for a name beginning with {L}.",
    "This personalised name word art print is a lovely way to put a name on the wall. A big {c} letter {L} is filled with their name and the little words that tell their story.",
    "If you want a gift that feels personal rather than picked off a shelf, this personalised name word art print is it: a striking {c} letter {L} made from their name and your words.",
    "Celebrate someone special with a personalised name word art print: a big {c} letter {L}, packed with their name and the words that describe them best.",
    "We design each personalised name word art print around one big {c} letter {L}, then fill it with the name and words you type in, so it really is a one-off.",
]
OPEN2 = [
    "It makes gorgeous new baby wall art for a nursery or bedroom.",
    "It's a thoughtful christening gift and a cheerful nursery print in one.",
    "Grandparents, godparents and new parents love them.",
    "It suits a nursery, a bedroom or the family living room.",
]
H2 = [
    "Your personalised name word art print, made with your words",
    "How your personalised name word art print comes together",
    "Create a personalised name word art print in two boxes",
    "Make your own personalised name word art print",
]
HOW = [
    "Type their name in the first box; it appears once, in pride of place. In the second box, type 20 to 30 words separated by commas: hobbies, nicknames, family names, favourite places. We repeat them in different sizes, fonts and shades to fill the letter {L}. The preview shows your details before you add it to your basket.",
    "The name box comes first, and whatever you type there is shown once, nice and big. Then add 20 to 30 words, with a comma between each, about the things and people they love. We repeat your words in different sizes, fonts and shades until the {c} letter {L} is full. Check the preview before you order.",
    "Fill in two boxes: the name, which sits once prominently in the design, and your word list of 20 to 30 words separated by commas. We repeat the words randomly in different sizes, fonts and shades across the letter {L}, and the preview shows what you've typed next to the print photo.",
]
TIPS = [
    "Tips: use single words or phrases of no more than three words, put commas between them and check your spelling. No icons, emoji or accented letters, please. We print exactly what you type.",
    "Single words work best, and no phrase should be longer than three words. Check the spelling carefully, as we print exactly what you enter. Icons, emoji and accents can't be included.",
    "Keep to single words or short phrases (three words at most), separated by commas, and leave out emoji, icons and accented letters. We print exactly what you type, so read it through once more.",
]
BULLETS = [
    "One of a kind: every word comes from you, so no two prints are the same",
    "Their name stands out once, and your other words repeat in different sizes, fonts and shades",
    "High-quality full-colour print, made to order in our own workshop",
    "Four print-only sizes, from a shelf-sized A4 to a statement A1",
    "Premium Display frames in black or silver: thick, chunky and very professional, not cheap thin frames",
    "Ready to display: A3 frames have a clip on the back for hanging, and A4 frames have a stand",
]
CLOSINGS = [
    "A lovely christening gift or new baby wall art piece, and a gift that will still be on the wall years from now.",
    "Perfect for a new baby, a christening, a birthday or a new home, and a thoughtful Christmas present for the family.",
    "Pick a name, choose your words and we'll do the rest. It makes a brilliant personalised birthday gift or a heart-warming Christmas present.",
    "Make it the centrepiece of a nursery, or give it as new home wall art with all the family's names and favourite things.",
    "A gift for a new baby, a godchild or a grandchild that they'll treasure long after the party is over.",
    "Whether it's for a birthday, a christening, a new home or Christmas morning, this is a gift they'll keep.",
    "Order one for the little one in your life, or a set of letters for brothers and sisters to hang side by side.",
]


def describe(i, colour, L):
    c = colour.lower()
    f = lambda s: s.format(c=c, L=L)
    rest = [x for x in BULLETS if "Premium Display" not in x]
    b = (rest[i % 5:] + rest[:i % 5])[:3]
    b.insert(i % 4, BULLETS[4])  # always highlight the Premium Display frames
    parts = [
        f"<p>{f(OPENINGS[i % 8])} {OPEN2[i % 4]}</p>",
        f"<h2>{H2[i % 4]}</h2>",
        f"<p>{f(HOW[i % 3])}</p>",
        f"<p>{TIPS[(i // 3) % 3]}</p>",
        "<h3>Why you'll love it</h3>",
        "<ul>" + "".join(f"<li>{x}</li>" for x in b) + "</ul>",
        "<h3>Size &amp; details</h3>",
        "<ul>"
        f"<li>Design: a big {c} letter {L} filled with your name and 20–30 words</li>"
        "<li>Print only: A4 (210 x 297 mm), A3 (297 x 420 mm), A2 (420 x 594 mm) or A1 (594 x 841 mm)</li>"
        "<li>Paper: A4 on 350gsm card, A3 on 170gsm gloss, A2 and A1 on 210gsm gloss</li>"
        "<li>Framed: A4 (with a stand) or A3 (with a hanging clip) in a black or silver Premium Display frame</li>"
        "</ul>",
        "<h3>Delivery</h3>",
        "<p>Your personalised name word art print is posted the next working day, or the same day if you order before 12pm, by Royal Mail.</p>",
        f"<p>{CLOSINGS[i % 7]}</p>",
    ]
    return "\n".join(parts)


def words(h):
    return len(re.sub(r"<[^>]+>", " ", html.unescape(h)).split())


def check(h):
    probs = []
    if h.count("<h2") != 1: probs.append("h2")
    low = h.replace("350gsm card", "").lower()
    for bad in ("style=", "<h4", "#", "<span", "<div", "card", "greeting", "white"):
        if bad in low:
            probs.append(bad)
    if re.search(r"<(\w+)[^>]*>\s*</\1>", h): probs.append("empty tag")
    n = words(h)
    if not 180 <= n <= 350: probs.append(f"words={n}")
    return probs


def kind(name):
    for k in ("BLACKFRAME", "SILVERFRAME", "WHITEFRAME", "GREETINGSCARD", "POSTERONLY", "PRINTONLY"):
        if name.endswith(k) or re.search(k + r"(_[0-9a-f]+)?$", name):
            return {"POSTERONLY": "PRINT", "PRINTONLY": "PRINT"}.get(k, k)
    return None


def main():
    out = sys.argv[1]
    prods = json.load(open(AFTER))["data"]["products"]["nodes"]
    media = {}
    for line in open(os.path.join(out, "media_before.txt")):
        if line.startswith("#") or not line.strip():
            continue
        pid, rest = line.strip().split("|")
        media["gid://shopify/Product/" + pid] = [tuple(x.split(":", 1)) for x in rest.split()]
    plan, seen = [], set()
    for i, p in enumerate(prods):
        m = re.search(r"(Pink|Blue) Letter ([A-Z])$", p["title"])
        colour, L = m.group(1), m.group(2)
        h = describe(i, colour, L)
        assert h not in seen, p["title"]
        seen.add(h)
        probs = check(h)
        assert not probs, (p["title"], probs)
        kinds = {}
        for mid, name in media[p["id"]]:
            kinds.setdefault(kind(name), []).append(mid)
        ok = (len(media[p["id"]]) == 5 and all(len(kinds.get(k, [])) == 1 for k in
              ("PRINT", "BLACKFRAME", "SILVERFRAME", "WHITEFRAME", "GREETINGSCARD")))
        kw = f"Personalised name word art print, {colour.lower()} letter {L}"
        e = {"id": p["id"], "title": p["title"], "handle": p["handle"], "descriptionHtml": h,
             "words": words(h), "images_ok": ok}
        if ok:
            g = lambda k: "gid://shopify/MediaImage/" + kinds[k][0]
            e["alts"] = {g("PRINT"): f"{kw}, print only",
                         g("BLACKFRAME"): f"{kw}, in a black frame",
                         g("SILVERFRAME"): f"{kw}, in a silver frame"}
            e["detach"] = [g("GREETINGSCARD"), g("WHITEFRAME")]
            e["order"] = [g("PRINT"), g("BLACKFRAME"), g("SILVERFRAME")]
            vm = []
            for v in p["variants"]["nodes"]:
                t = v["title"]
                k = "BLACKFRAME" if "Black Frame" in t else "SILVERFRAME" if "Silver Frame" in t else "PRINT" if "Print Only" in t else None
                assert k, t
                vm.append({"id": v["id"], "mediaId": g(k)})
            e["variant_media"] = vm
        plan.append(e)
    json.dump(plan, open(os.path.join(out, "plan.json"), "w"), indent=1, ensure_ascii=False)
    print(len(plan), "products;", sum(e["images_ok"] for e in plan), "with standard images;",
          "word counts", min(e["words"] for e in plan), "-", max(e["words"] for e in plan))
    for e in plan:
        if not e["images_ok"]:
            print("IMAGES LEFT ALONE:", e["title"], e["id"])


def product_ops(n, e):
    """GraphQL fields for one product (description passed as $dN)."""
    pid = json.dumps(e["id"])
    ops = [f'p{n}: productUpdate(product:{{id:{pid}, descriptionHtml:$d{n}, templateSuffix:"personalised"}}) {{ userErrors {{ field message }} }}',
           f't{n}: tagsAdd(id:{pid}, tags:["io-word-art"]) {{ userErrors {{ message }} }}']
    if e["images_ok"]:
        files = [f'{{id:{json.dumps(k)}, alt:{json.dumps(v)}}}' for k, v in e["alts"].items()]
        files += [f'{{id:{json.dumps(k)}, referencesToRemove:[{pid}]}}' for k in e["detach"]]
        ops.append(f'f{n}: fileUpdate(files:[{", ".join(files)}]) {{ userErrors {{ field message code }} }}')
        moves = ", ".join(f'{{id:{json.dumps(k)}, newPosition:"{j}"}}' for j, k in enumerate(e["order"]))
        ops.append(f'r{n}: productReorderMedia(id:{pid}, moves:[{moves}]) {{ mediaUserErrors {{ field message }} }}')
        vs = ", ".join(f'{{id:{json.dumps(v["id"])}, mediaId:{json.dumps(v["mediaId"])}}}' for v in e["variant_media"])
        ops.append(f'v{n}: productVariantsBulkUpdate(productId:{pid}, variants:[{vs}]) {{ userErrors {{ field message }} }}')
    return ops


def batches(out, size=4, skip=()):
    plan = [e for e in json.load(open(os.path.join(out, "plan.json"))) if e["id"] not in skip]
    for b in range(0, len(plan), size):
        chunk = plan[b:b + size]
        lines, mf, vars_ = [], [], {}
        for n, e in enumerate(chunk):
            lines += product_ops(n, e)
            vars_[f"d{n}"] = e["descriptionHtml"]
            mf.append(f'{{ownerId:{json.dumps(e["id"])}, namespace:"foxy", key:"personalise_fields", type:"list.single_line_text_field", value:$pf}}')
            mf.append(f'{{ownerId:{json.dumps(e["id"])}, namespace:"foxy", key:"mockup", type:"single_line_text_field", value:"photo"}}')
        vars_["pf"] = json.dumps(FIELDS, ensure_ascii=False)
        lines.append(f'm: metafieldsSet(metafields:[{", ".join(mf)}]) {{ userErrors {{ field message code }} }}')
        decl = ", ".join([f"$d{n}: String!" for n in range(len(chunk))] + ["$pf: String!"])
        doc = f"mutation({decl}) {{\n" + "\n".join(lines) + "\n}"
        k = b // size + 1
        open(os.path.join(out, f"batch_{k:02d}.graphql"), "w").write(doc)
        json.dump(vars_, open(os.path.join(out, f"batch_{k:02d}.vars.json"), "w"), ensure_ascii=False)
        print(k, [e["title"][-14:] for e in chunk], len(doc), "bytes")


if __name__ == "__main__":
    main()
    if len(sys.argv) > 2:
        batches(sys.argv[1], skip=set(sys.argv[2].split(",")))
