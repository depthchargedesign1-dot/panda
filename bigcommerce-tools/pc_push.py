#!/usr/bin/env python3
"""Push changes to the Personalised Cards BigCommerce store.

All commands default to DRY RUN. Add --apply to write. Every write is
logged to <scratch>/push-log.jsonl with the previous value, so anything
can be put back.

  python3 pc_push.py <scratch> shipping  [--apply]      # 1st Class rate -> £2.99
  python3 pc_push.py <scratch> prices    [--apply]      # product price (A5) and A4 adjuster
  python3 pc_push.py <scratch> descriptions [--apply] [--ids 1,2] [--limit N]

Prices: product base price = A5 price; the "Choose Card Size" modifier gets a
relative adjuster on A4 (and A6 if PC_A6_PRICE is set) so the storefront shows
the right total for each size.
"""
from __future__ import annotations
import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bc

A5_PRICE = float(os.environ.get("PC_A5_PRICE", "3.49"))
A4_PRICE = float(os.environ.get("PC_A4_PRICE", "6.99"))
A6_PRICE = os.environ.get("PC_A6_PRICE")            # unset = same as A5
SHIP_RATE = float(os.environ.get("PC_SHIP_RATE", "2.99"))
STORE = "pc"


def log(scratch, rec):
    rec["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(f"{scratch}/push-log.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")


def done_ids(scratch, kind):
    ids = set()
    try:
        for line in open(f"{scratch}/push-log.jsonl"):
            r = json.loads(line)
            if r.get("kind") == kind and r.get("ok"):
                ids.add(r["id"])
    except FileNotFoundError:
        pass
    return ids


# ----------------------------------------------------------- shipping ----
def cmd_shipping(scratch, apply):
    for z in bc.api(STORE, "v2/shipping/zones"):
        for m in bc.api(STORE, f"v2/shipping/zones/{z['id']}/methods"):
            if m["type"] == "perorder" and "1st class" in m["name"].lower():
                old = m["settings"]["rate"]
                print(f"zone {z['name']}: '{m['name']}' rate {old} -> {SHIP_RATE}")
                if apply and float(old) != SHIP_RATE:
                    bc.api(STORE, f"v2/shipping/zones/{z['id']}/methods/{m['id']}", method="PUT",
                           body={"settings": {"rate": SHIP_RATE}})
                    log(scratch, {"kind": "shipping", "id": m["id"], "zone": z["id"], "old": old, "new": SHIP_RATE, "ok": True})
                    print("  applied")
    if not apply:
        print("(dry run: add --apply to write)")


# ------------------------------------------------------------- prices ----
def cmd_prices(scratch, apply, limit=None):
    P = json.load(open(f"{scratch}/products.json"))
    skip = done_ids(scratch, "price")
    todo = [p for p in P if p["id"] not in skip]
    if limit: todo = todo[:limit]
    print(f"{len(todo)} products to price (A5 £{A5_PRICE:.2f}, A4 £{A4_PRICE:.2f}, A6 {'£'+A6_PRICE if A6_PRICE else 'same as A5'}); {len(skip)} already done")
    if not apply:
        print("(dry run: add --apply to write)"); return
    # 1) base prices in batches of 10
    for i in range(0, len(todo), 10):
        chunk = todo[i:i+10]
        body = [{"id": p["id"], "price": A5_PRICE} for p in chunk]
        bc.api(STORE, "v3/catalog/products", method="PUT", body=body)
        for p in chunk:
            log(scratch, {"kind": "price", "id": p["id"], "old": p["price"], "new": A5_PRICE, "ok": True})
        # 2) size adjusters, one product at a time
        for p in chunk:
            mods = bc.api(STORE, f"v3/catalog/products/{p['id']}/modifiers")["data"]
            size = next((m for m in mods if "size" in m["display_name"].lower()), None)
            if not size:
                log(scratch, {"kind": "adjuster", "id": p["id"], "ok": False, "err": "no size modifier"}); continue
            for v in size["option_values"]:
                lab = v["label"].upper()
                target = None
                if lab.startswith("A4"): target = round(A4_PRICE - A5_PRICE, 2)
                elif lab.startswith("A6") and A6_PRICE: target = round(float(A6_PRICE) - A5_PRICE, 2)
                elif lab.startswith("A5") or lab.startswith("A6"): target = 0
                if target is None: continue
                cur = (v.get("adjusters") or {}).get("price") or {}
                if cur.get("adjuster") == "relative" and float(cur.get("adjuster_value") or 0) == target:
                    continue
                adj = {"adjusters": {"price": {"adjuster": "relative", "adjuster_value": target}}} if target else {"adjusters": {"price": None}}
                bc.api(STORE, f"v3/catalog/products/{p['id']}/modifiers/{size['id']}/values/{v['id']}", method="PUT", body=adj)
                log(scratch, {"kind": "adjuster", "id": p["id"], "value_id": v["id"], "label": v["label"], "old": cur, "new": target, "ok": True})
        print(f"  priced {min(i+10, len(todo))}/{len(todo)}", flush=True)


# ------------------------------------------------------- descriptions ----
def cmd_descriptions(scratch, apply, ids=None, limit=None):
    P = {p["id"]: p for p in json.load(open(f"{scratch}/products.json"))}
    R = json.load(open(f"{scratch}/rewrite.json"))
    skip = done_ids(scratch, "description")
    todo = [int(k) for k in R if int(k) not in skip and (not ids or int(k) in ids)]
    if limit: todo = todo[:limit]
    print(f"{len(todo)} descriptions to push; {len(skip)} already done")
    if not apply:
        print("(dry run: add --apply to write)"); return
    for i in range(0, len(todo), 10):
        chunk = todo[i:i+10]
        body = [{"id": pid, "description": R[str(pid)]["description"],
                 "page_title": R[str(pid)]["page_title"],
                 "meta_description": R[str(pid)]["meta_description"]} for pid in chunk]
        try:
            bc.api(STORE, "v3/catalog/products", method="PUT", body=body)
        except bc.BCError as e:
            # fall back to one at a time so one bad record doesn't block ten
            for rec in body:
                try:
                    bc.api(STORE, f"v3/catalog/products/{rec['id']}", method="PUT", body={k: v for k, v in rec.items() if k != "id"})
                    log(scratch, {"kind": "description", "id": rec["id"], "old": {k: P[rec["id"]].get(k) for k in ("description", "page_title", "meta_description")}, "ok": True})
                except bc.BCError as e2:
                    log(scratch, {"kind": "description", "id": rec["id"], "ok": False, "err": str(e2)[:300]})
                    print("  FAILED", rec["id"], str(e2).splitlines()[0])
            continue
        for pid in chunk:
            log(scratch, {"kind": "description", "id": pid, "old": {k: P[pid].get(k) for k in ("description", "page_title", "meta_description")}, "ok": True})
        print(f"  pushed {min(i+10, len(todo))}/{len(todo)}", flush=True)


def main(argv):
    scratch, cmd = argv[0], argv[1]
    apply = "--apply" in argv
    ids = {int(x) for x in argv[argv.index("--ids") + 1].split(",")} if "--ids" in argv else None
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None
    if cmd == "shipping": cmd_shipping(scratch, apply)
    elif cmd == "prices": cmd_prices(scratch, apply, limit)
    elif cmd == "descriptions": cmd_descriptions(scratch, apply, ids, limit)
    else: print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
