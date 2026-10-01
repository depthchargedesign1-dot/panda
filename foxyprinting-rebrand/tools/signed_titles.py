"""Honest titles for reproduction 'signed' prints: the signature is printed, not hand-signed."""
import re

def fix_title(title, product_type=""):
    t = title
    # Drop the product type pasted in front of many titles ("Signed Footballer Posters, Signed Footballer Prints ...").
    for prefix in sorted({p.strip() for p in re.split(r",", product_type or "") if p.strip()}, key=len, reverse=True):
        t = re.sub(r"^\s*" + re.escape(prefix) + r"[\s,]*", "", t, flags=re.I)
    t = re.sub(r"\b(hand[- ]?)?signed\s+(and\s+)?autographed\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bsigned\s+autograph\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bautographed\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bsigned\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\bautograph\b", "Printed Signature", t, flags=re.I)
    t = re.sub(r"\b(Printed Signature)(\s+Printed Signature)+\b", r"\1", t)
    t = re.sub(r"\bPhoto Signature\b|\bSignatur\b", "", t, flags=re.I)
    t = re.sub(r"\b(memorabilia|merch)\b", "Gift", t, flags=re.I)
    t = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", t, flags=re.I)  # "Gift Gift" -> "Gift"
    t = re.sub(r"\s{2,}", " ", t).strip(" -–,")
    if "reproduction" not in t.lower():
        t += " – Reproduction Print"
    return t
