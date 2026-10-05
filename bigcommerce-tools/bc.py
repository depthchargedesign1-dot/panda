#!/usr/bin/env python3
"""Small BigCommerce admin client for the three stores that share one login.

Stores (short names used everywhere in this tool):
  cpp  Celebrity Poster Prints   https://www.celebrity-poster-prints.com
  cfm  Celebrity Face Masks
  pc   Personalised Cards

Credentials are read from environment variables only (never from files):
  BC_<STORE>_STORE_HASH     e.g. lf3pkcn41h
  BC_<STORE>_ACCESS_TOKEN   store-level API account token (X-Auth-Token)
where <STORE> is CPP, CFM or PC.

Usage:
  python3 bc.py check                  # connect to every configured store
  python3 bc.py check cpp              # one store
  python3 bc.py orders cpp [--days 30] # order counts by status + recent orders
  python3 bc.py storefront cpp         # public site: HTTP status, redirects, title
  python3 bc.py get cpp v2/store       # raw GET on any endpoint (v2/... or v3/...)

Only standard-library modules are used, so it runs anywhere Python 3 does.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

STORES = {
    "cpp": "Celebrity Poster Prints",
    "cfm": "Celebrity Face Masks",
    "pc": "Personalised Cards",
}

API_BASE = "https://api.bigcommerce.com/stores/{hash}/{path}"
UA = "foxy-bc-tools/0.1 (+https://github.com/depthchargedesign1-dot/panda)"


class BCError(RuntimeError):
    pass


def creds(store: str) -> tuple[str, str]:
    key = store.upper()
    h = os.environ.get(f"BC_{key}_STORE_HASH", "").strip()
    t = os.environ.get(f"BC_{key}_ACCESS_TOKEN", "").strip()
    if not h or not t:
        raise BCError(
            f"{STORES.get(store, store)}: set BC_{key}_STORE_HASH and "
            f"BC_{key}_ACCESS_TOKEN in the environment (not in the chat)."
        )
    return h, t


def api(store: str, path: str, params: dict | None = None, method: str = "GET",
        body: dict | None = None, timeout: int = 30):
    """Call the BigCommerce Management API. Returns parsed JSON (or None for 204)."""
    store_hash, token = creds(store)
    url = API_BASE.format(hash=store_hash, path=path.lstrip("/"))
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "X-Auth-Token": token,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": UA,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if resp.status == 204 or not raw:
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        hint = {
            401: "token rejected: check the access token",
            403: "token lacks the scope for this endpoint, or the store hash is wrong",
            404: "endpoint or store hash not found",
            429: "rate limited: wait and retry",
        }.get(e.code, "")
        raise BCError(f"HTTP {e.code} on {method} {path}: {hint}\n{detail}") from None
    except urllib.error.URLError as e:
        raise BCError(
            f"could not reach api.bigcommerce.com ({e.reason}). "
            "If this is a cloud session, api.bigcommerce.com must be on the "
            "environment's allowed domains."
        ) from None


# ---------- commands ----------

def cmd_check(stores: list[str]) -> int:
    ok = True
    for s in stores:
        name = STORES[s]
        print(f"== {name} ({s})")
        try:
            info = api(s, "v2/store")
        except BCError as e:
            ok = False
            print(f"   FAILED: {e}")
            continue
        print(f"   store name : {info.get('name')}")
        print(f"   domain     : {info.get('domain')}")
        print(f"   secure URL : {info.get('secure_url')}")
        print(f"   plan       : {info.get('plan_name')} ({info.get('plan_level')})")
        print(f"   status     : {info.get('status')}")
        print(f"   currency   : {info.get('currency')}  tz: {info.get('timezone', {}).get('name')}")
        # quick counts; each needs its own scope so report but don't fail
        for label, path, params in (
            ("products", "v3/catalog/products", {"limit": 1}),
            ("orders", "v2/orders/count", None),
        ):
            try:
                r = api(s, path, params)
                if label == "products":
                    n = r.get("meta", {}).get("pagination", {}).get("total")
                else:
                    n = r.get("count")
                print(f"   {label:<11}: {n}")
            except BCError as e:
                print(f"   {label:<11}: unavailable ({str(e).splitlines()[0]})")
    return 0 if ok else 1


def cmd_orders(store: str, days: int) -> int:
    statuses = api(store, "v2/order_statuses") or []
    print(f"== {STORES[store]}: order counts by status")
    total = 0
    for st in statuses:
        r = api(store, "v2/orders/count", {"status_id": st["id"]})
        n = r.get("count", 0)
        total += n
        flag = "  <- to ship" if st["name"] in (
            "Awaiting Fulfillment", "Awaiting Shipment", "Awaiting Pickup", "Partially Shipped") else ""
        print(f"   {st['name']:<22} {n:>6}{flag}")
    print(f"   {'all statuses':<22} {total:>6}")

    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    recent = api(store, "v2/orders", {"min_date_created": since, "sort": "date_created:desc", "limit": 20}) or []
    print(f"\n   last {days} days: {len(recent)} order(s) shown (max 20)")
    for o in recent:
        print(f"   #{o['id']:<7} {o['date_created'][:16]:<17} {o['status']:<22} "
              f"{o['currency_code']} {o['total_inc_tax']:>8}  {o['billing_address'].get('country_iso2','')}")
    return 0


def cmd_storefront(store: str) -> int:
    """Check the public site without credentials: status, redirects, title."""
    try:
        info = api(store, "v2/store")
        url = info.get("secure_url") or f"https://{info.get('domain')}"
    except BCError:
        url = {"cpp": "https://www.celebrity-poster-prints.com/"}.get(store)
        if not url:
            print("no credentials and no known URL for this store")
            return 1
    print(f"== {STORES[store]} storefront: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 " + UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read(300_000).decode("utf-8", "replace")
            print(f"   HTTP {resp.status}  final URL: {resp.geturl()}")
            m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
            print(f"   title      : {(m.group(1).strip() if m else '(none)')[:120]}")
            for needle, meaning in (
                ("store is currently closed", "BigCommerce 'store closed' page"),
                ("Under Maintenance", "maintenance mode"),
                ("down for maintenance", "maintenance mode"),
                ("not found", "possible 404 text"),
            ):
                if needle.lower() in html.lower():
                    print(f"   note       : page contains '{needle}' ({meaning})")
            print(f"   stencil    : {'yes' if 'stencil' in html.lower() or 'bigcommerce' in html.lower() else 'not detected'}")
    except urllib.error.HTTPError as e:
        print(f"   HTTP {e.code} {e.reason}")
        return 1
    except urllib.error.URLError as e:
        print(f"   unreachable: {e.reason}")
        return 1
    return 0


def cmd_get(store: str, path: str, params: list[str]) -> int:
    q = dict(p.split("=", 1) for p in params) if params else None
    print(json.dumps(api(store, path, q), indent=2))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check"); p.add_argument("store", nargs="?", choices=STORES)
    p = sub.add_parser("orders"); p.add_argument("store", choices=STORES); p.add_argument("--days", type=int, default=30)
    p = sub.add_parser("storefront"); p.add_argument("store", choices=STORES)
    p = sub.add_parser("get"); p.add_argument("store", choices=STORES); p.add_argument("path")
    p.add_argument("params", nargs="*", help="key=value query params")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "check":
            stores = [a.store] if a.store else [s for s in STORES if os.environ.get(f"BC_{s.upper()}_ACCESS_TOKEN")]
            if not stores:
                print("No stores configured. Set BC_CPP_/BC_CFM_/BC_PC_ STORE_HASH and ACCESS_TOKEN.")
                return 1
            return cmd_check(stores)
        if a.cmd == "orders":
            return cmd_orders(a.store, a.days)
        if a.cmd == "storefront":
            return cmd_storefront(a.store)
        if a.cmd == "get":
            return cmd_get(a.store, a.path, a.params)
    except BCError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
