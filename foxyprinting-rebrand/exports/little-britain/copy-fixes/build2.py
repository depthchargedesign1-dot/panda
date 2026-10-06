"""Little Britain follow-ups (6 Oct 2026, owner decisions): 3-pack copy, Walliams titles,
Andy/Bubbles tags, Lou alt text, pair meta, Matt Lucas disclaimer. Writes after2.json and
mutation2-variables.json; before2.json is the live state read just before the push."""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
G = "gid://shopify/Product/"

LB_DISCLAIMER = (
    "<h3>Please note</h3>\n"
    '<p class="disclaimer">This is an unofficial design inspired by Lou Todd, Andy Pipkin and Vicky Pollard, '
    "characters from Little Britain, made for fun and fancy dress. It is not official merchandise and is not "
    "endorsed by, sponsored by, or connected with Little Britain, the BBC, Matt Lucas or David Walliams, or any "
    "of their licensees, and none of them has approved this product. The names are used only to describe the "
    "design. All names, characters and trademarks belong to their respective owners.</p>"
)

PACK_SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Contents: 3 masks (Lou Todd, Andy Pipkin and Vicky Pollard)</li>
<li>Size: each mask is 297 x 210 mm (A4), a full adult-size face</li>
<li>Material: 350gsm silk card, full-colour digital print</li>
<li>Finish: semi-waterproof</li>
<li>Fit: one size for adults; elastic and sticky tabs included with every mask</li>
<li>Pre-cut eye holes; each mask is cut to the shape of the face</li>
<li>Packaging: all three posted flat in one board-backed envelope</li>
</ul>
<h3>Delivery</h3>
<p>Printed in our UK workshop and posted to you. Dispatch and postage options are shown at checkout.</p>"""

PACK1 = """<p>This Little Britain face mask 3-pack is made for three mates who want to turn up as a gang: Lou, Andy and Vicky in one order. It's a sure-fire laugh at a stag do, a hen night or a fancy dress birthday, and nobody has to argue over who gets which face.</p>
<h2>Little Britain Face Mask 3-Pack for Groups</h2>
<p>You get three card face masks: Lou Todd, Andy Pipkin and Vicky Pollard. We print each one in full colour on thick 350gsm silk card, cut it to the shape of the face and pre-cut the eye holes. Elastic and sticky tabs come with every mask, so you're ready to go in a couple of minutes. Want to add someone from your own group? Send us a clear photo and we'll make a custom mask to go with the set.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Three costumes sorted in one go, with no wigs or face paint</li>
<li>Better value than buying the three comedy character masks one by one</li>
<li>Thick 350gsm card that keeps its shape on a long night out</li>
<li>Semi-waterproof finish, so a spilt pint won't finish it off</li>
<li>Instantly recognisable in stag and hen do group photos</li>
</ul>
""" + PACK_SPECS + """
<p>Got a bigger group? Add our Bubbles DeVere mask or the Lou and Andy pair to the 3-pack and the whole table is covered.</p>
""" + LB_DISCLAIMER

PACK2 = """<p>Throwing a noughties night? This Little Britain face mask 3-pack gives you three of the show's best-known faces in one envelope, ready for a comedy-themed birthday, a quiz night or a photo booth that needs a bit of mischief.</p>
<h2>Little Britain Face Mask 3-Pack – Lou, Andy and Vicky</h2>
<p>Inside are Lou Todd, Andy Pipkin and Vicky Pollard, each printed in full colour on 350gsm silk card. Every mask is cut to shape with the eye holes already cut out, and we include elastic and sticky tabs for each one. If you'd like a friend's face printed as a fourth mask, send us a clear, front-facing photo and we'll make it.</p>
<h3>Why you'll love it</h3>
<ul>
<li>A ready-made sketch show line-up for a themed party</li>
<li>Full A4 masks that cover an adult face properly</li>
<li>Bright, sharp digital print that looks great on camera</li>
<li>Light enough to wear all evening, sturdy enough to pass round</li>
<li>Arrives flat and crease-free in a board-backed envelope</li>
</ul>
""" + PACK_SPECS + """
<p>These noughties fancy dress masks make a cheap and cheerful prop for a birthday roast or a retro telly night in.</p>
""" + LB_DISCLAIMER

MATT_OLD_DISC = re.compile(r'<p class="disclaimer">.*?</p>', re.S)
MATT_NEW_DISC = (
    '<p class="disclaimer">This is an unofficial novelty product made for fun and fancy dress. Matt Lucas has not '
    "endorsed, sponsored or approved this product, and Foxy Printing has no connection with him, or with Little "
    "Britain, the BBC, The Great British Bake Off or its producers, or any of their licensees. The names are used "
    "only to describe the design. All names and trademarks belong to their respective owners.</p>"
)

UPDATES = {
    "8125549805819": {"descriptionHtml": PACK1, "seo": {
        "title": "Comedy Sketch Show Face Mask 3-Pack | Foxy Printing",
        "description": "Three card face masks in one order: Lou, Andy and Vicky. Thick 350gsm card, cut to shape with eye holes, elastic included. Perfect for stag and hen dos."}},
    "8195091595515": {"descriptionHtml": PACK2, "seo": {
        "title": "Noughties Comedy Fancy Dress Mask Pack | Foxy Printing",
        "description": "Plan a noughties night with this pack of three comedy character face masks. A4 size on 350gsm silk card, eye holes cut, elastic and sticky tabs included."}},
    "9530623624": {"title": "David Walliams 2 Face Mask – Fancy Dress Cardboard Costume Mask"},
    "4328415592523": {"title": "David Walliams 3 Face Mask – Fancy Dress Cardboard Costume Mask"},
    "9530620744": {"title": "David Walliams 4 Face Mask – Fancy Dress Cardboard Costume Mask"},
    "16063694635389": {"seo": {
        "title": "Comedy Double Act Couple Face Masks | Foxy Printing",
        "description": "Turn up as a famous comedy double act with this pair of Lou and Andy card face masks. Pre-cut eye holes, elastic supplied, posted flat in a sturdy envelope."}},
    "8249158926587": {"matt": True},
}
TAGS_ADD = {
    "8125549805819": ["third-party-name"], "8195091595515": ["third-party-name"],
    "9530634184": ["mask-comedians", "TV STARS"], "9530648776": ["mask-comedians", "TV STARS"],
}
TAGS_REMOVE = {"9530634184": ["mask-film-stars", "MOVIES"], "9530648776": ["mask-film-stars", "MOVIES"]}
LOU_ALTS = {
    "gid://shopify/MediaImage/32937038086395": "Lou Todd face mask, a printed card fancy dress mask cut to shape with eye holes",
    "gid://shopify/MediaImage/33842656477435": "Card face mask print and size information for the Lou Todd face mask",
    "gid://shopify/MediaImage/33842656510203": "How to fit the elastic to the Lou Todd face mask",
    "gid://shopify/MediaImage/33842656542971": "Size and card details for the Lou Todd face mask",
    "gid://shopify/MediaImage/33842656608507": "Custom photo mask option shown alongside the Lou Todd face mask",
}


def main():
    before = json.loads((HERE / "before2.json").read_text())
    after, problems, variables = {}, [], {}
    for pid, u in UPDATES.items():
        inp = {"id": G + pid}
        if u.get("matt"):
            html = before[pid]["descriptionHtml"]
            assert MATT_OLD_DISC.search(html)
            inp["descriptionHtml"] = MATT_OLD_DISC.sub(lambda _: MATT_NEW_DISC, html)
        for k in ("title", "descriptionHtml", "seo"):
            if k in u:
                inp[k] = u[k]
        if "seo" in inp:
            s = inp["seo"]
            if len(s["title"]) > 60 or "Little Britain" in s["title"]:
                problems.append(f"{pid} seo title")
            if not 140 <= len(s["description"]) <= 155:
                problems.append(f"{pid} meta {len(s['description'])}")
        if "descriptionHtml" in inp:
            h = inp["descriptionHtml"]
            words = len(re.sub(r"<[^>]+>", " ", h).split())
            if h.count("<h2>") > 1 or "style=" in h or "<img" in h:
                problems.append(f"{pid} html")
            inp_words = words
        else:
            inp_words = None
        variables[f"p{pid}"] = inp
        after[pid] = dict(inp, words=inp_words)
    if PACK1 == PACK2:
        problems.append("packs identical")
    out = {"productUpdate": after, "tagsAdd": TAGS_ADD, "tagsRemove": TAGS_REMOVE, "lou_alt_text": LOU_ALTS}
    (HERE / "after2.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    variables["files"] = [{"id": k, "alt": v} for k, v in LOU_ALTS.items()]
    (HERE / "mutation2-variables.json").write_text(json.dumps(variables, ensure_ascii=False))
    for pid, a in after.items():
        print(pid, a["words"], a.get("seo", {}).get("title"), len(a.get("seo", {}).get("description", "")))
    print("PROBLEMS:", problems or "none")


if __name__ == "__main__":
    main()
