import re

def _has(rx, *s):
    return any(re.search(rx, x or "", re.I) for x in s)


def family(o):
    t = o["title"] or ""
    pt = o["productType"] or ""
    tags = " ".join(o.get("tags") or [])
    cat = ((o.get("category") or {}) or {}).get("fullName") or ""
    if _has(r"face ?mask|facemask|celebrity mask|footballer masks|\bmasks?\b.*(fancy dress|party)|^masks$|tv stars|request a facemask|costume mask|halloween mask|face mask bundle", pt) \
            or _has(r"face ?mask|cardboard mask|party mask|celebrity mask|card mask", t):
        if not _has(r"mouse|mug|card\b|poster|print", pt):
            return "mask"
    if _has(r"lego", pt, t) and _has(r"display", t):
        return "display"
    if _has(r"replacement|case or cover|game case|\bcase\b", pt) or _has(r"replacement game case|case or cover|ugc style|replacement case", t):
        if not _has(r"phone|tablet|pencil", pt, t):
            return "case"
    if _has(r"magnet", pt) or _has(r"fridge magnet|\bmagnet\b", t):
        return "magnet"
    if _has(r"keyring|key ring", pt, t):
        return "keyring"
    if _has(r"mouse ?mat|desk mat|gaming mat", pt, t):
        return "mousemat"
    if _has(r"signed|autograph|printed signature", t) and not _has(r"card", pt) and _has(r"print|poster|frame|photo|a6|picture|signed|autograph", t + " " + pt):
        if not _has(r"\bmug\b|baby grow|baby vest|bodysuit|t-?shirt|keyring|magnet|cushion|towel", t):
            return "signed"
    if _has(r"baby vest|baby grow|bodysuit|babygrow", pt, t):
        return "babygrow"
    if _has(r"\bmugs?\b|clarence|alchemy|keep calm support|coach mugs|this guy|this girl|full wrap", pt) or _has(r"\bmug\b", t):
        if not _has(r"coaster", t):
            return "mug"
    if _has(r"t-?shirt|\btee\b|hoodie|sweatshirt|jumper", t) and not _has(r"baby|bodysuit|mug|card", t):
        return "clothing"
    if _has(r"word art", t):
        return "poster"
    if _has(r"invite|invitation", pt, t):
        return "party"
    if _has(r"card", pt) and not _has(r"business|loyalty|poster card|a6", pt) or _has(r"birthday card|\bcard$|christmas card|valentines? card|anniversary card|father'?s day card|mother'?s day card|\bxmas card", t):
        if not _has(r"business card|loyalty card|poster card", t):
            return "card"
    if _has(r"stocking|santa sack|bauble|christmas eve box|ornament|\badvent\b", pt, t):
        return "christmas"
    if _has(r"coaster|bar mat|bar runner|placemat", pt, t):
        return "coaster"
    if _has(r"cushion|pillow", pt, t) and not _has(r"treat box|pillow box", t):
        return "cushion"
    if _has(r"towel", pt, t):
        return "towel"
    if _has(r"bunting|banner|party|wrapping paper|cake topper|treat box|favour box|pillow box|balloon", pt, t):
        return "party"
    if _has(r"pet portrait|bandana|dog bowl|pet bowl|\bpet\b|\bdog\b collar", pt) or _has(r"pet portrait|dog bandana|pet bandana|dog bowl", t):
        return "pets"
    if _has(r"glass|tumbler|stein|bottle|travel mug|kids cups", pt) or _has(r"pint glass|gin glass|wine glass|champagne flute|whisky glass|glass can|tumbler|\bstein\b|water bottle", t):
        return "glassware"
    if _has(r"sticker|decal|label", pt, t):
        return "sticker"
    if _has(r"t-?shirt|hoodie|jumper|apparel|shirts|clothing|workwear|teamwear|bucket hat|bobble hat|\bcap\b|pyjama|sock|scarf|tops", pt) or _has(r"t-?shirt|\btee\b|hoodie|sweatshirt|jumper|\bcap\b|bobble hat|bucket hat|pyjamas|socks|scarf", t):
        return "clothing"
    if _has(r"plaque|\bsigns?\b|door sign|pump clip|award|medal|plate", pt) or _has(r"plaque|\bsign\b|door hanger|pub sign|metal sign|medal|commemorative plate", t):
        return "plaque"
    if _has(r"poster|print|wall art|artwork|wall decor|football gift|walking dead|gavin and stacey", pt) or _has(r"poster|\bprint\b|word art|wall art|canvas", t):
        return "poster"
    return "generic"
