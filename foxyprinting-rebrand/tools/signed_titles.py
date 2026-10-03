"""Honest titles for reproduction 'signed' prints: the signature is printed, not hand-signed."""
import re

def fix_title(title, product_type=""):
    t = title
    # Drop the product type pasted in front of many titles ("Signed Footballer Posters, Signed Footballer Prints ...").
    for prefix in sorted({p.strip() for p in re.split(r",", product_type or "") if p.strip()}, key=len, reverse=True):
        t = re.sub(r"^\s*" + re.escape(prefix) + r"[\s,]*", "", t, flags=re.I)
    t = re.sub(r"\b(hand[- ]?)?signed\s+(and\s+)?autographed\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bhand[- ]?signed\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bsigned\s+autograph\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bautographed\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bsigned\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bautograph\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\b(Printed Signature)(\s+Printed Signature)+\b", r"\1", t)
    t = re.sub(r"\bPhoto Signature\b|\bSignatur\b", "", t, flags=re.I)
    t = re.sub(r"\bfor Fans (&|and) Memorabilia (Enthusiasts|Collectors)\b", "Gift for Fans", t, flags=re.I)
    t = re.sub(r"\b(memorabilia|merch)\b", "Wall Art", t, flags=re.I)
    # Words that imply an authentic, official or scarce item (owner approved removal, 2 Oct 2026).
    t = re.sub(r"\blimited[- ]edition\b", "", t, flags=re.I)
    t = re.sub(r"\b(official|authentic|genuine|certified|COA|collectible|collectable|merchandise)\b", "", t, flags=re.I)
    # Keep only the first "Printed Signature".
    first = re.search(r"Printed Signature", t, flags=re.I)
    if first:
        t = t[:first.end()] + re.sub(r"\s*\bPrinted Signature\b", "", t[first.end():], flags=re.I)
    t = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", t, flags=re.I)  # "Gift Gift" -> "Gift"
    t = re.sub(r"\s*([-–|,])\s*(?=[-–|,])", " ", t)  # collapse empty separators ("- –")
    t = re.sub(r"\s+([-–|])\s+", r" \1 ", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" -–,")
    # Drop repeated or empty segments ("Fan Gift – Gift").
    parts, seen = [], set()
    for seg in re.split(r"\s+[-–|]\s+", t):
        key = seg.strip().lower()
        if key and key not in seen and not any(key in s2 for s2 in seen):
            parts.append(seg.strip()); seen.add(key)
    t = " – ".join(parts)
    if "reproduction" not in t.lower():
        t += " – Reproduction Print"
    return t
