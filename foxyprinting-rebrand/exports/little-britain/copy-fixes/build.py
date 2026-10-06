"""Little Britain mask copy fixes (6 Oct 2026).

Builds after.json and mutation-variables.json from the new copy below.
before.json is the live state read from Shopify just before the push.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent

SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Size: 297 x 210 mm (A4), a full adult-size face</li>
<li>Material: 350gsm silk card, full-colour digital print</li>
<li>Finish: semi-waterproof</li>
<li>Fit: one size for adults; elastic and sticky tabs included</li>
<li>Pre-cut eye holes; cut to the shape of the face</li>
<li>Packaging: board-backed envelope</li>
</ul>
<h3>Delivery</h3>
<p>Printed in our UK workshop and posted to you flat. Dispatch and postage options are shown at checkout.</p>"""


def character_disclaimer(name):
    return (
        "<h3>Please note</h3>\n"
        f'<p class="disclaimer">This is an unofficial design inspired by {name}, a character from Little Britain, '
        "made for fun and fancy dress. It is not official merchandise and is not endorsed by, sponsored by, "
        "or connected with Little Britain, the BBC, Matt Lucas or David Walliams, or any of their licensees, "
        "and none of them has approved this product. The names are used only to describe the design. "
        "All names, characters and trademarks belong to their respective owners.</p>"
    )


WALLIAMS_DISCLAIMER = (
    "<h3>Please note</h3>\n"
    '<p class="disclaimer">This is an unofficial novelty product made for fun and fancy dress. '
    "David Walliams has not endorsed, sponsored or approved this product, and Foxy Printing has no connection "
    "with him, or with Little Britain, the BBC or any of their licensees. The names are used only to describe "
    "the design. All trademarks belong to their respective owners.</p>"
)

WALLIAMS_OPENING = (
    "<p>This David Walliams face mask is a giggle for a noughties comedy party, a sketch show night or a "
    "double-act costume. Walliams is the comedian and children's author who played Lou Todd, Andy's "
    "long-suffering carer, in Little Britain, so pair it with a friend in an Andy Pipkin mask and you're sorted.</p>"
)

OLD_WALLIAMS_OPENING = (
    "<p>Andy Pipkin is the wheelchair-using character from Little Britain, played by David Walliams "
    "opposite Lou. Yeah I know! This mask is a giggle for a noughties comedy party, a sketch show night "
    "or a pair costume.</p>"
)
OLD_WALLIAMS_DISCLAIMER_RE = re.compile(r"<h3>Please note</h3>\n<p class=\"disclaimer\">.*?</p>", re.S)

NEW = {}

# --- Vicky Pollard: disclaimer only -------------------------------------------------
NEW["9369892744"] = {"disclaimer": character_disclaimer("Vicky Pollard"),
                     "replace": [("let the comedian face do the talking", "let the face do the talking")]}

# --- Lou Todd: full rewrite ---------------------------------------------------------
NEW["8125539352827"] = {
    "descriptionHtml": """<p>This Lou Todd face mask is the easy way to turn up as the patient, put-upon carer from one of Britain's best-loved sketch shows. It's a guaranteed laugh at a noughties comedy night, a stag or hen do or a fancy dress birthday.</p>
<h2>Lou Todd Face Mask for Fancy Dress</h2>
<p>We print Lou's face in full colour on thick 350gsm silk card, cut it to shape and pre-cut the eye holes, so it's ready to wear in seconds. Elastic and sticky tabs are included. Going as a pair? Team this card face mask with our Andy Pipkin mask and you've got the full Lou and Andy costume. Need a face we don't stock, like the groom or the birthday girl? Send us a clear photo and we'll make a custom mask.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Instantly recognisable Little Britain fancy dress with no costume shopping needed</li>
<li>Full A4 size (297 x 210 mm), so it covers an adult face</li>
<li>Thick 350gsm silk card that holds its shape all night</li>
<li>Semi-waterproof finish copes with spilt drinks and outdoor parties</li>
<li>A cheap, cheerful stag do mask that's brilliant in group photos</li>
</ul>
""" + SPECS + """
<p>Order a Lou Todd face mask for yourself, or a few comedy face masks so the whole group can join in.</p>
""" + character_disclaimer("Lou Todd"),
    "seo": {
        "title": "Lou Todd Face Mask | Foxy Printing",
        "description": "Turn up as Lou with this Lou Todd face mask. Printed on thick 350gsm card, cut to shape with eye holes, elastic included. Ideal for stag and hen dos.",
    },
}

# --- Andy Pipkin: full rewrite (was "film star", "Pipkins") ---------------------------
NEW["9530634184"] = {
    "descriptionHtml": """<p>This Andy Pipkin face mask brings one of British comedy's most famous characters to your party: the man who always wants it, then doesn't. It's perfect for a noughties comedy night, a stag or hen do, or a fancy dress birthday.</p>
<h2>Andy Pipkin Face Mask for Fancy Dress</h2>
<p>We print Andy's face in full colour on thick 350gsm silk card, cut it to shape and pre-cut the eye holes. Elastic and sticky tabs are included, so it's ready to wear in seconds. Pair it with our Lou Todd mask for a ready-made Lou and Andy costume. Want a mask of someone who isn't in our range, like the groom or a mate? Send us a clear photo and we'll make a custom mask.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Easy Little Britain fancy dress: just add a cardigan and a grumpy face</li>
<li>Full A4 size (297 x 210 mm), so it covers an adult face</li>
<li>Thick 350gsm silk card holds its shape all night</li>
<li>Semi-waterproof finish copes with spilt drinks and outdoor parties</li>
<li>A cheap comedy face mask that steals every group photo</li>
</ul>
""" + SPECS + """
<p>Grab an Andy Pipkin face mask for a themed birthday, or a stag do mask for the whole group, and get the camera ready.</p>
""" + character_disclaimer("Andy Pipkin"),
    "seo": {
        "title": "Andy Pipkin Face Mask | Foxy Printing",
        "description": "Turn up as Andy with this Andy Pipkin face mask. Full-colour print on thick 350gsm card, cut to shape with eye holes and elastic. Great for stag dos.",
    },
}

# --- Bubbles DeVere: was framed as a "film star", disclaimer lacked Lucas/Walliams ----
NEW["9530648776"] = {
    "descriptionHtml": """<p>Our Bubbles DeVere face mask is a quick way to get everyone laughing, whether it's a noughties comedy night, a hen do or a spa-themed birthday. Add a dressing gown and some big jewellery, or keep it simple and let the face do the talking.</p>
<h2>Bubbles DeVere Face Mask for Fancy Dress</h2>
<p>We print this comedy character mask in full colour on thick 350gsm silk card, cut it to the shape of the face and pre-cut the eye holes. Elastic and sticky tabs are included, so it's ready to wear in seconds. Want a mask of someone who isn't in our range, like the bride-to-be? Send us a clear photo and we'll make a custom mask.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Instant Little Britain fancy dress with no costume hunting</li>
<li>Brilliant for hen party photo booths and group shots</li>
<li>Thick 350gsm silk card holds its shape all night</li>
<li>Semi-waterproof finish copes with spilt drinks and outdoor parties</li>
<li>Full A4 size (297 x 210 mm), so it covers an adult face</li>
</ul>
""" + SPECS + """
<p>A Bubbles DeVere face mask is a cheap and cheerful way to make a hen do one to remember. Pair it with our Vicky Pollard and Lou and Andy masks for a full comedy line-up.</p>
""" + character_disclaimer("Bubbles DeVere"),
    "seo": {
        "title": "Bubbles DeVere Face Mask | Foxy Printing",
        "description": "Make the hen do with a Bubbles DeVere face mask. Printed on thick 350gsm silk card, cut to shape with eye holes, elastic and sticky tabs included.",
    },
}

# --- David Walliams 9530623624 + 4328415592523: wrong character (Andy -> Lou) ----------
NEW["9530623624"] = {
    "replace_opening": True,
    "disclaimer": WALLIAMS_DISCLAIMER,
    "seo": {
        "title": "David Walliams Face Mask | Foxy Printing",
        "description": "Turn up as the comedian with this David Walliams face mask. A4 size on thick 350gsm card, cut to shape with eye holes, elastic and sticky tabs included.",
    },
}
NEW["4328415592523"] = {
    "replace_opening": True,
    "disclaimer": WALLIAMS_DISCLAIMER,
    "seo": {
        "title": "David Walliams Celebrity Face Mask | Foxy Printing",
        "description": "Get the party started with a David Walliams celebrity face mask. Full-colour print on 350gsm card, cut to shape with elastic. Great for a comedy night.",
    },
}

# --- David Walliams 8225435910395: old copy (inline styles, img, 5 x H2, no disclaimer) -
NEW["8225435910395"] = {
    "descriptionHtml": """<p>This David Walliams face mask is an easy fancy dress win for a comedy night, a book-themed party or a birthday roast. The comedian, children's author and former talent show judge has one of the most recognisable grins on British telly, and now your mate can wear it.</p>
<h2>David Walliams Face Mask for Parties</h2>
<p>We print his face in full colour on thick 350gsm silk card, cut it to shape and pre-cut the eye holes, so it's ready to wear in seconds. Elastic and sticky tabs are included. Can't find the face you need, like the birthday boy or the bride-to-be? Send us a clear photo and we'll make a custom mask.</p>
<h3>Why you'll love it</h3>
<ul>
<li>A fun celebrity face mask for stag and hen dos, birthdays and photo booths</li>
<li>Full A4 size (297 x 210 mm), so it covers an adult face</li>
<li>Thick 350gsm silk card holds its shape all night</li>
<li>Semi-waterproof finish copes with spilt drinks and outdoor parties</li>
<li>Posted flat in a board-backed envelope to keep it crease-free</li>
</ul>
""" + SPECS + """
<p>Order a David Walliams face mask for a comedy fancy dress night, or a few cardboard face masks so the whole group can join in.</p>
""" + WALLIAMS_DISCLAIMER,
    "seo": {
        "title": "David Walliams Comedian Face Mask | Foxy Printing",
        "description": "Turn heads with a David Walliams comedian face mask. Printed on thick 350gsm silk card, cut to shape with eye holes, elastic and sticky tabs included.",
    },
}

# --- David Walliams 9530620744: "Little Britain" in SEO title + meta; "them" -> "him" ----
NEW["9530620744"] = {
    "disclaimer": WALLIAMS_DISCLAIMER,
    "seo": {
        "title": "David Walliams Fancy Dress Face Mask | Foxy Printing",
        "description": "Make a comedy night with a David Walliams fancy dress face mask. 350gsm silk card, cut to shape with eye holes, elastic and sticky tabs included.",
    },
}

TAGS_ADD = {  # third-party-name was missing on these
    "9530623624": ["third-party-name"],
    "4328415592523": ["third-party-name"],
    "8225435910395": ["third-party-name"],
    "8249158926587": ["third-party-name"],
}


def main():
    before = {p["id"].rsplit("/", 1)[1]: p for p in json.loads((HERE / "before.json").read_text())["data"]["nodes"]}
    after, variables, problems = {}, {}, []
    for pid, spec in NEW.items():
        b = before[pid]
        html = spec.get("descriptionHtml", b["descriptionHtml"])
        if spec.get("replace_opening"):
            assert OLD_WALLIAMS_OPENING in html, pid
            html = html.replace(OLD_WALLIAMS_OPENING, WALLIAMS_OPENING)
        for old, new in spec.get("replace", []):
            assert old in html, pid
            html = html.replace(old, new)
        if "disclaimer" in spec:
            assert OLD_WALLIAMS_DISCLAIMER_RE.search(html), pid
            html = OLD_WALLIAMS_DISCLAIMER_RE.sub(lambda _: spec["disclaimer"], html)
        seo = spec.get("seo", b["seo"])
        # checks
        text = re.sub(r"<[^>]+>", " ", html)
        words = len(text.split())
        for bad in ["style=", "<img", "Pipkins", "film star", "Oscars", "[", "01439771468", "authentic", "genuine", "licensed"]:
            if bad in html:
                problems.append(f"{pid}: contains {bad!r}")
        if html.count("<h2>") != 1:
            problems.append(f"{pid}: {html.count('<h2>')} h2")
        if len(seo["title"]) > 60 or "Little Britain" in seo["title"]:
            problems.append(f"{pid}: seo title {seo['title']!r}")
        if not 140 <= len(seo["description"]) <= 155:
            problems.append(f"{pid}: meta {len(seo['description'])} chars")
        after[pid] = {"id": b["id"], "title": b["title"], "descriptionHtml": html, "seo": seo,
                      "tags_added": TAGS_ADD.get(pid, []), "words": words}
        variables[f"p{pid}"] = {"id": b["id"], "descriptionHtml": html, "seo": seo}
    for pid, tags in TAGS_ADD.items():
        after.setdefault(pid, {"id": before[pid]["id"], "title": before[pid]["title"], "tags_added": tags})
    (HERE / "after.json").write_text(json.dumps(after, indent=2, ensure_ascii=False))
    (HERE / "mutation-variables.json").write_text(json.dumps(variables, indent=2, ensure_ascii=False))
    for pid, a in after.items():
        print(pid, a.get("words"), a.get("seo", {}).get("title"), len(a.get("seo", {}).get("description", "")))
    print("PROBLEMS:", problems or "none")


if __name__ == "__main__":
    main()
