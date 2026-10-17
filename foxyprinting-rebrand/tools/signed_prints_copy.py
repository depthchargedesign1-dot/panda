"""Reproduction 'signed' prints: title and description update (owner's decisions, 6 Oct 2026).

- Titles: drop "– Reproduction Print"; keep "Printed Signature".
- Body: honest wording instead of "signed print" / "autographed" / "limited edition"; one short
  "high-quality reproduction print" line after the first paragraph; the signed-print disclaimer once,
  at the end; a "Premium Display frames" line on products sold framed.

Usage: python3 signed_prints_copy.py products.jsonl OUT_DIR
Reads a bulk export (id handle title status productType descriptionHtml options{name values}
variants{title sku}) and writes a Shopify product CSV import (one row per variant).
"""
import csv
import hashlib
import json
import os
import re
import sys

REPRO_LINE = ('<p>This is a high-quality reproduction print – the signature is printed as part of the design.</p>')

SIGNED_SENTENCE = ("This is a printed reproduction. The signature is printed as part of the design – "
                   "it is not hand-signed and is not an original autograph.")
DISCLAIMER = ('<h3>Please note</h3>\n<p class="disclaimer">' + SIGNED_SENTENCE +
              " This is an unofficial, fan-made design created and printed by Foxy Printing. It is not "
              "endorsed by, sponsored by, or connected with the person pictured, or their club, team, league, "
              "management, studio or record label. Names are used only to describe the design. All names "
              "and trademarks belong to their respective owners.</p>")

FRAME_LINES = [
    "Our framed options come in Premium Display frames – thick, chunky and very professional, not the cheap thin frames you often see.",
    "Choose a framed size and it arrives in one of our Premium Display frames: thick, chunky and properly professional, not a cheap thin frame.",
    "The framed versions use our Premium Display frames – a thick, chunky, professional finish rather than the flimsy thin frames you often see.",
    "Going framed? Every framed option comes in a Premium Display frame – thick, chunky and very professional, nothing like a cheap thin frame.",
    "Framed prints come in our Premium Display frames, which are thick, chunky and look very professional on the wall – not cheap thin frames.",
]

# ---------------------------------------------------------------- titles

def new_title(title):
    t = re.sub(r"\s*[-–|,]?\s*\(?\bReproduction Print\b\)?", "", title)
    t = re.sub(r"\s*([-–|,])\s*(?=[-–|,]|$)", "", t)  # empty separators left behind
    t = re.sub(r"\s{2,}", " ", t).strip(" -–|,")
    return t

# ---------------------------------------------------------------- body wording

def _cap(m, text):
    """Keep the case style of the matched words on the replacement."""
    w = m.group(0)
    if w.isupper() and len(w) > 3:
        return text.upper()
    if not w[:1].isupper():
        return text
    words = re.findall(r"[A-Za-z]+", w)
    after = m.string[m.end():m.end() + 3]
    if (len(words) > 1 and all(x[0].isupper() for x in words)) or re.match(r"\s+[A-Z]", after):
        return " ".join(x if x in ("a", "of", "with", "the") else x[:1].upper() + x[1:] for x in text.split(" "))
    return text[:1].upper() + text[1:]


def _art(m, text):
    """'an authentic autograph' -> 'a printed signature'; 'his authentic autograph' -> 'his printed signature'."""
    return _cap(m, ("a " + text) if m.group(1) else text)


# (pattern, replacement) – applied in order, case-insensitive. A replacement starting with "@"
# keeps the case of the first letter of the match.
RULES = [
    # Hashtag blocks: drop tags that claim a signed/authentic item (#SignedMemorabilia, #AutographedPrint ...).
    (r"[ \t]*#\w*(signed|autograph|memorabilia|limited_?edition|authentic|genuine|official|merch)\w*", ""),
    (r"A Limited Edition Signed Print by your amazing ([^.<]+?)\s*\.", r"A print of your amazing \1, with a printed signature."),
    (r"A Limited Edition Signed Print by your amazing ([^.<]+?)(?=\s*<)", r"A print of your amazing \1, with a printed signature."),
    (r"(framed or un-framed) Signed Print\s+(They are)", r"\1 print with a printed signature. \2"),
    (r"Printed Signed (Poster|Print)s?\b", r"Printed Signature \1"),
    (r"\b(an?\s+)?(?:genuine|authentic|authenticated|exclusive|real)\s+(?:autograph|signature)\b", "&printed signature"),
    (r"\b(genuine|authentic|authenticated|exclusive|real)\s+(autographs|signatures)\b", "@printed signatures"),
    (r"\b(?:personally|officially|directly)\s+signed\s+(?:and\s+authenticated\s+)?by\b", "@printed with the signature of"),
    (r"\b(?:personally\s+)?signed\s+it\b", "@has the signature printed on it"),
    (r"\b(has|have|had)\s+been\s+(?:\w+\s+)?(?:signed|autographed)\s+by\b", r"\1 the printed signature of"),
    (r"\bis\s+(?:\w+ly\s+)?(?:signed|autographed)\s+by\b", "carries the printed signature of"),
    (r"\bare\s+(?:\w+ly\s+)?(?:signed|autographed)\s+by\b", "carry the printed signature of"),
    (r"\b(?:signed|autographed)\s+by\b", "@with the printed signature of"),
    (r"\b(?:signed|autographed)\s+(?:and|&amp;|&)\s+framed\b", "@framed printed signature"),
    (r"\b(?:signed\s+)?autographed\s+merch\b(?!\s*print)", "@printed signature"),
    (r"\b(?:signed|autographed)\s+piece\b", "@print"),
    (r"\b(limited[- ]edition\s+)?(hand[- ]?)?(signed|autographed)\s+(and\s+)?(autographed\s+)?(limited[- ]edition\s+)?(prints)\b", "@prints with a printed signature"),
    (r"\b(limited[- ]edition\s+)?(hand[- ]?)?(signed|autographed)\s+(and\s+)?(autographed\s+)?(limited[- ]edition\s+)?(print)\b", "@print with a printed signature"),
    (r"\bautograph(ed)?\s+merch\s*print\b", "@print with a printed signature"),
    (r"\b(signed|autographed)\s+merch\b", "@printed signature"),
    (r"\bmerchprint\b", "@print"),
    (r"\bautograph\s+print\b", "@printed signature print"),
    (r"\b(hand[- ]?)?signed\s+(and\s+|&amp;\s+|&\s+)?autographed\b", "@printed signature"),
    (r"\bhand[- ]?signed\b", "@printed signature"),
    (r"\bautographed\b", "@printed signature"),
    (r"\bsigned\b", "@printed signature"),
    (r"\blimited[- ]edition\s+", ""),
    (r"\blimited[- ]edition\b", ""),
    (r"\bauthentic-looking\b", "@eye-catching"),
    (r"\b(their|your|the)\s+collectors'?\s+memorabilia\b", r"\1 wall"),
    (r"\bmerch\s*memorabilia\b", "@wall art"),
    (r"\bmemorabilia\b", "@wall art"),
    (r"\b(printed signature)(\s+printed signature)+\b", r"\1"),
    (r"\bwith a printed signature\s+(printed\s+)?with the (printed\s+)?signature of\b", "with the printed signature of"),
    (r"\bprinted\s+printed signature\b", "@printed signature"),
]
RULES = [(re.compile(p, re.I), r) for p, r in RULES]

# Text that must survive untouched (disclaimers, honest phrasing, Royal Mail "Signed For").
PROTECT = re.compile(
    r'<p class="disclaimer">.*?</p>'
    r"|\bnot\s+(an?\s+)?(original\s+)?(hand[- ]?signed|signed|autographed|original autograph)\b(\s+(and|or)\s+(is\s+)?not\s+an\s+original\s+autograph)?"
    r"|\bsigned[- ]for\b|\brecorded\s*(and|&amp;|&)?\s*signed\b|\bsign(ed)?\s+up\b"
    r"|\b(was|were|got|he|she|they|who|had|has|then|later|eventually|subsequently)\s+signed\s+(for|with|by|a|an|his|her|their|on|up|as|to|from)\b"
    r"|\bsigned\s+(with|a\s+(new\s+)?(contract|deal|two|three|four|five|one|record)|on\s+loan|to\s+(the|a)\s+\w+\s+label)\b"
    r"|<[^>]+>",  # never edit inside tags (attributes, URLs)
    re.I | re.S)


def reword(text):
    """Apply RULES outside protected spans. Returns new text."""
    out, last = [], 0
    for m in PROTECT.finditer(text):
        out.append(_reword_plain(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(_reword_plain(text[last:]))
    return "".join(out)


def _reword_plain(s):
    if not s:
        return s
    for rx, rep in RULES:
        if rep.startswith("&"):
            s = rx.sub(lambda m, r=rep[1:]: _art(m, r), s)
        elif rep.startswith("@"):
            s = rx.sub(lambda m, r=rep[1:]: _cap(m, r), s)
        else:
            s = rx.sub(rep, s)
    return s


# The rules above are applied segment by segment (between tags). A phrase like
# "<strong>Signed</strong> Print" is still caught word by word by the generic rules.

STYLED_SPAN = re.compile(r'<span\s+style="[^"]*font-size[^"]*">', re.I)


def unwrap_font_spans(p):
    """Remove font-size spans in a paragraph we touched, only when all its spans are those spans."""
    opens = re.findall(r"<span\b[^>]*>", p, re.I)
    if opens and all(STYLED_SPAN.fullmatch(o) for o in opens) and len(opens) == len(re.findall(r"</span>", p, re.I)):
        p = STYLED_SPAN.sub("", p)
        p = re.sub(r"</span>", "", p, flags=re.I)
    return p


PARA = re.compile(r"<p\b[^>]*>.*?</p>", re.I | re.S)


def reword_body(body):
    """Reword paragraph by paragraph; strip font-size spans only in paragraphs that changed."""
    out, last = [], 0
    for m in PARA.finditer(body):
        gap = body[last:m.start()]
        out.append(reword(gap))
        p = m.group(0)
        q = reword(p)
        if q != p:
            q = unwrap_font_spans(q)
        out.append(q)
        last = m.end()
    out.append(reword(body[last:]))
    return "".join(out)


def plain(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def insert_after_first_para(body, snippet):
    m = re.search(r"</p>", body, re.I)
    if m and m.start() < 3000:
        return body[:m.end()] + "\n" + snippet + body[m.end():]
    m = re.search(r"(<br\s*/?>\s*)+", body, re.I)
    if m and m.start() < 1500:
        return body[:m.end()] + snippet + "\n" + body[m.end():]
    return snippet + "\n" + body


def ensure_disclaimer(body):
    """Signed-print disclaimer once, at the end, under <h3>Please note</h3>."""
    discs = list(re.finditer(r'<p class="disclaimer">(.*?)</p>', body, re.I | re.S))
    if not discs:
        return body.rstrip() + "\n" + DISCLAIMER, "added"
    d = discs[-1]
    inner = d.group(1)
    if re.search(r"not hand-signed", inner, re.I):
        return body, "kept"
    # Existing sports/celebrity disclaimer: combine into one paragraph.
    new_inner = SIGNED_SENTENCE + " " + inner.strip()
    return body[:d.start(1)] + new_inner + body[d.end(1):], "combined"


def is_framed_value(v):
    v = v.strip().lower()
    if re.search(r"\b(un-?framed|no frame|without (a )?frame|print only|unframed)\b", v):
        return False
    return bool(re.search(r"\bframe[ds]?\b|\b(black|silver|gold|white|oak|wood(en)?)\b", v))


def has_frames(product):
    for o in product.get("options") or []:
        for v in o.get("values") or []:
            if is_framed_value(v):
                return True
    for v in product.get("_variants", []):
        if is_framed_value(v.get("title") or ""):
            return True
    return False


def is_signature_print(product):
    text = product["title"] + " " + re.sub(r'<p class="disclaimer">.*?</p>', "", product.get("descriptionHtml") or "", flags=re.S)
    return bool(re.search(r"sign|autograph", text, re.I))


def new_body(product):
    body = product.get("descriptionHtml") or ""
    notes = {}
    # A few posters got "Reproduction Print" in the title without being signature prints at all
    # (retro club-colour posters, team champions posters). Only their title changes.
    if not is_signature_print(product):
        return body, {"repro_line": "not a signature print", "disclaimer": "unchanged"}
    b = reword_body(body)
    top = plain(b)[:500].lower()
    if "reproduction" in top:
        notes["repro_line"] = "skipped"
    else:
        b = insert_after_first_para(b, REPRO_LINE)
        notes["repro_line"] = "added"
    if has_frames(product):
        if "Premium Display frame" not in b:
            i = int(hashlib.md5(product["handle"].encode()).hexdigest(), 16) % len(FRAME_LINES)
            line = "<p>" + FRAME_LINES[i] + "</p>"
            if notes["repro_line"] == "added":
                b = b.replace(REPRO_LINE, REPRO_LINE + "\n" + line, 1)
            else:
                b = insert_after_first_para(b, line)
        notes["frame"] = True
    b, notes["disclaimer"] = ensure_disclaimer(b)
    return b, notes


# ---------------------------------------------------------------- export reading

def load(jsonl):
    prods, order = {}, []
    with open(jsonl) as f:
        for line in f:
            o = json.loads(line)
            if "__parentId" in o:
                prods[o["__parentId"]]["_variants"].append(o)
            else:
                o["_variants"] = []
                prods[o["id"]] = o
                order.append(o["id"])
    return [prods[i] for i in order]


def in_scope(p):
    return "Reproduction Print" in (p.get("title") or "")


HEAD = ["Handle", "Title", "Status", "Body (HTML)", "Option1 Name", "Option1 Value", "Option2 Name",
        "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU"]


def rows_for(p, title, body):
    opts = p.get("options") or []
    names = [o["name"] for o in opts][:3]
    rows = []
    for i, v in enumerate(p["_variants"]):
        vals = [s.strip() for s in (v.get("title") or "").split(" / ")]
        if len(names) == 1:
            vals = [v.get("title") or ""]
        r = {"Handle": p["handle"], "Variant SKU": v.get("sku") or ""}
        for k in range(3):
            r[f"Option{k+1} Value"] = vals[k] if k < len(names) and k < len(vals) else ""
            r[f"Option{k+1} Name"] = names[k] if (i == 0 and k < len(names)) else ""
        if i == 0:
            r.update({"Title": title, "Status": p["status"].lower(), "Body (HTML)": body})
        rows.append(r)
    return rows


if __name__ == "__main__":
    src, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    prods = [p for p in load(src) if in_scope(p)]
    result = []
    for p in prods:
        b, notes = new_body(p)
        result.append((p, new_title(p["title"]), b, notes))
    json.dump([{"handle": p["handle"], "id": p["id"], "old_title": p["title"], "title": t,
                "old_body": p.get("descriptionHtml") or "", "body": b, "notes": n,
                "status": p["status"], "variants": len(p["_variants"])} for p, t, b, n in result],
              open(os.path.join(out_dir, "changes.json"), "w"))

    def write(name, items):
        with open(os.path.join(out_dir, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEAD)
            w.writeheader()
            for p, t, b, n in items:
                w.writerows(rows_for(p, t, b))

    # Test file: one framed 9-size print, one single-variant print, one 13-option poster.
    by = {p["handle"]: (p, t, b, n) for p, t, b, n in result}
    test = []
    for want in (lambda p: len(p["_variants"]) == 8 and p["status"] == "ACTIVE",
                 lambda p: len(p["_variants"]) == 1 and p["status"] == "ACTIVE" and "Signed Autographed Merch" in (p.get("descriptionHtml") or ""),
                 lambda p: len(p["_variants"]) == 13 and p["status"] == "ACTIVE"):
        test.append(next(r for r in result if want(r[0]) and r not in test))
    write("00-TEST-3-products.csv", test)

    # Split the rest into files under ~15 MB.
    limit = 14_500_000
    chunk, size, k = [], 0, 1
    for r in result:
        est = len(r[2].encode()) + 200 * len(r[0]["_variants"]) + 400
        if chunk and size + est > limit:
            write(f"{k:02d}-signed-prints.csv", chunk); k += 1; chunk, size = [], 0
        chunk.append(r); size += est
    if chunk:
        write(f"{k:02d}-signed-prints.csv", chunk)
    print(len(result), "products,", k, "files")
