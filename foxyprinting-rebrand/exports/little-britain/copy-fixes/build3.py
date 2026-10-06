"""Last follow-ups (6 Oct 2026): elastic wording on pair + Characters Pack, MOVIES/mask-film-stars tag clean-up,
main-image alt text. Text edits are exact string replacements on the live HTML (asserted)."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
G = "gid://shopify/Product/"
EDITS = {
 "16063694635389": [
  ("We print each face in full colour from our own artwork, cut it to shape and cut out the eye holes, so all you do is pull on the elastic. Pick Ready to Wear and we fit the elastic and sticky tabs for you, or choose DIY and we send them loose so you can fit them yourselves.",
   "We print each face in full colour from our own artwork. Ready to Wear masks come cut to shape with the eye holes already cut out, and the elastic and sticky tabs are supplied for you to attach. DIY masks are print only, so you cut them out yourselves, and the elastic and sticky tabs are supplied with these too."),
  ("<li>Pre-cut eye holes so you can see where you're going</li>", "<li>Ready to Wear masks have pre-cut eye holes, so you can see where you're going</li>")],
 "16063694668157": [
  ("Each face is printed in full colour from our own artwork, cut to shape, and the eye holes are already cut out. Choose Ready to Wear and we fit the elastic and sticky tabs, or pick DIY and we send them loose to fit yourself, which keeps the price down.",
   "Each face is printed in full colour from our own artwork. Choose Ready to Wear and the masks come cut to shape with the eye holes already cut out, with the elastic and sticky tabs supplied for you to attach. Pick DIY and you get the printed masks to cut out yourself, plus the elastic and sticky tabs, which keeps the price down."),
  ("<li>A ready-made group costume for four, at less than the price of one shop-bought mask</li>", "<li>A ready-made group costume for four, all in one envelope</li>"),
  ("<li>Eye holes cut out for you, so nobody walks into a door</li>", "<li>Ready to Wear eye holes come cut out, so nobody walks into a door</li>")],
}
SEO = {"16063694668157": {"title": None, "description": "Four comedy sketch character face masks in one pack, printed on thick card, with elastic and sticky tabs supplied. An easy group costume for any party."}}
TAG_FIX = ["8125549805819", "8195091595515", "8125539352827", "9530623624", "9530620744"]
TAGS_REMOVE = ["MOVIES", "mask-film-stars"]
TAGS_ADD = ["mask-comedians", "TV STARS"]
ALTS = {
 "gid://shopify/MediaImage/32937062564091": "Little Britain face mask 3-pack with Lou Todd, Andy Pipkin and Vicky Pollard printed card masks",
 "gid://shopify/MediaImage/33842693177595": "Little Britain face mask 3-pack: Lou Todd, Andy Pipkin and Vicky Pollard card masks with eye holes",
 "gid://shopify/MediaImage/2625119125579": "Andy Pipkin face mask, a printed card fancy dress mask cut to shape with eye holes",
 "gid://shopify/MediaImage/2625123024971": "Bubbles DeVere face mask, a printed card fancy dress mask cut to shape with eye holes",
 "gid://shopify/MediaImage/2625116110923": "David Walliams face mask, a printed card celebrity mask cut to shape with eye holes",
 "gid://shopify/MediaImage/5530912882763": "David Walliams face mask printed on card, cut to shape with eye holes for fancy dress",
 "gid://shopify/MediaImage/2625115258955": "David Walliams face mask, full-colour card celebrity mask with pre-cut eye holes",
 "gid://shopify/MediaImage/33982670045435": "David Walliams face mask, a card comedian mask cut to shape with eye holes",
}

def main():
    before = json.loads((HERE / "before3.json").read_text())
    variables = {}
    for pid, edits in EDITS.items():
        h = before[pid]["descriptionHtml"]
        for a, b in edits:
            assert a in h, (pid, a[:40]); h = h.replace(a, b)
        assert "we fit" not in h and "fitted" not in h
        inp = {"id": G + pid, "descriptionHtml": h}
        if pid in SEO:
            inp["seo"] = {"description": SEO[pid]["description"]}
            assert 140 <= len(SEO[pid]["description"]) <= 155, len(SEO[pid]["description"])
        variables["p" + pid] = inp
    variables["files"] = [{"id": k, "alt": v} for k, v in ALTS.items()]
    (HERE / "mutation3-variables.json").write_text(json.dumps(variables, ensure_ascii=False))
    (HERE / "after3.json").write_text(json.dumps({"productUpdate": variables, "tagsRemove": {p: TAGS_REMOVE for p in TAG_FIX},
        "tagsAdd": {p: TAGS_ADD for p in TAG_FIX}}, indent=2, ensure_ascii=False))
    print("ok")

if __name__ == "__main__":
    main()
