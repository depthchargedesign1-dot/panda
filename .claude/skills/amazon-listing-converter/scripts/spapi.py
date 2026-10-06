#!/usr/bin/env python3
"""spapi - Foxy Printing's connection to the Amazon Selling Partner API (UK / EU endpoint).

Credentials come ONLY from environment variables (never put them in files or chat):
  SPAPI_CLIENT_ID       LWA client id of your SP-API app (Seller Central > Apps > Develop apps)
  SPAPI_CLIENT_SECRET   LWA client secret
  SPAPI_REFRESH_TOKEN   refresh token from "Authorise" on your private (self-authorised) app
  SPAPI_SELLER_ID       your merchant token / seller id (Seller Central > Settings > Account info)
Optional: SPAPI_MARKETPLACE (default A1F83G8C2ARO7P = amazon.co.uk), SPAPI_ENDPOINT, SPAPI_LWA_URL.

Commands (read-only unless stated):
  check                         test the connection: token + marketplaces you can sell in
  search-types KEYWORDS         find Amazon product types, e.g. "mug"
  product-type TYPE [--out F]   download the listing schema for a product type (e.g. DRINKING_CUP)
  get SKU                       show one listing with its issues
  validate FEED.json [--report R.json]
                                VALIDATION_PREVIEW of every message - Amazon checks, nothing changes
  submit FEED.json --confirm    WRITES to Amazon: sends the JSON_LISTINGS_FEED. Refuses unless a clean
                                validation report for the same SKUs exists (under 24h old)
  feed-status FEED_ID [--out F] feed progress, then downloads the processing report when DONE
"""
import argparse, datetime, gzip, hashlib, json, os, sys, time, urllib.error, urllib.parse, urllib.request

ENDPOINT = os.environ.get("SPAPI_ENDPOINT", "https://sellingpartnerapi-eu.amazon.com").rstrip("/")
LWA_URL = os.environ.get("SPAPI_LWA_URL", "https://api.amazon.com/auth/o2/token")
MARKETPLACE = os.environ.get("SPAPI_MARKETPLACE", "A1F83G8C2ARO7P")
UA = "FoxyPrinting-mugkit/1.0 (Language=Python)"
_token = {"value": None, "exp": 0}


def need(name):
    v = os.environ.get(name, "").strip()
    if not v:
        sys.exit(f"missing environment variable {name} - add it to the environment settings (see SKILL.md)")
    return v


def access_token():
    if _token["value"] and time.time() < _token["exp"] - 60:
        return _token["value"]
    body = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": need("SPAPI_REFRESH_TOKEN"),
                                   "client_id": need("SPAPI_CLIENT_ID"),
                                   "client_secret": need("SPAPI_CLIENT_SECRET")}).encode()
    req = urllib.request.Request(LWA_URL, body, {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        sys.exit(f"Login with Amazon refused the credentials (HTTP {e.code}): {detail}")
    _token.update(value=d["access_token"], exp=time.time() + int(d.get("expires_in", 3600)))
    return _token["value"]


def call(method, path, params=None, body=None, retries=5):
    url = ENDPOINT + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retries):
        req = urllib.request.Request(url, data, method=method, headers={
            "x-amz-access-token": access_token(), "Content-Type": "application/json",
            "Accept": "application/json", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(min(2 ** attempt, 20))
                continue
            try:
                err = json.loads(raw)
            except ValueError:
                err = {"raw": raw[:500]}
            raise SystemExit(f"SP-API {method} {path} -> HTTP {e.code}: {json.dumps(err)[:800]}")
    raise SystemExit("SP-API: too many retries")


def seller_id():
    return need("SPAPI_SELLER_ID")


def q(s):
    return urllib.parse.quote(s, safe="")


# ----------------------------------------------------------------------------- commands
def cmd_check(_a):
    d = call("GET", "/sellers/v1/marketplaceParticipations")
    rows = []
    for p in d.get("payload", []):
        m, part = p.get("marketplace", {}), p.get("participation", {})
        rows.append({"id": m.get("id"), "name": m.get("name"), "country": m.get("countryCode"),
                     "selling": part.get("isParticipating"), "suspended": part.get("hasSuspendedListings")})
    uk = any(r["id"] == MARKETPLACE and r["selling"] for r in rows)
    print(json.dumps({"connected": True, "marketplaces": rows, "uk_ready": uk}, indent=1))
    if not uk:
        print(f"WARNING: not participating in marketplace {MARKETPLACE}", file=sys.stderr)


def cmd_search_types(a):
    d = call("GET", "/definitions/2020-09-01/productTypes",
             {"keywords": a.keywords, "marketplaceIds": MARKETPLACE, "locale": "en_GB"})
    print(json.dumps([{"name": t.get("name"), "display": t.get("displayName")} for t in d.get("productTypes", [])],
                     indent=1))


def cmd_product_type(a):
    d = call("GET", f"/definitions/2020-09-01/productTypes/{q(a.type)}",
             {"marketplaceIds": MARKETPLACE, "requirements": "LISTING", "locale": "en_GB"})
    link = (d.get("schema") or {}).get("link", {}).get("resource")
    out = {"productType": d.get("productType"), "version": d.get("productTypeVersion")}
    if link:
        with urllib.request.urlopen(urllib.request.Request(link, headers={"User-Agent": UA}), timeout=60) as r:
            schema = json.load(r)
        out["required"] = schema.get("required", [])
        path = a.out or f"{a.type}-schema.json"
        json.dump(schema, open(path, "w"), indent=1)
        out["schema_file"] = path
        themes = (schema.get("properties", {}).get("variation_theme", {}).get("items", {})
                  .get("properties", {}).get("name", {}).get("enum"))
        out["variation_themes"] = themes
    print(json.dumps(out, indent=1))


def cmd_get(a):
    d = call("GET", f"/listings/2021-08-01/items/{q(seller_id())}/{q(a.sku)}",
             {"marketplaceIds": MARKETPLACE, "includedData": "summaries,issues,attributes,offers", "issueLocale": "en_GB"})
    print(json.dumps(d, indent=1)[:20000])


def feed_messages(path):
    feed = json.load(open(path, encoding="utf-8"))
    return feed, feed.get("messages", [])


def digest(msgs):
    return hashlib.sha256(json.dumps([[m["sku"], m["attributes"]] for m in msgs], sort_keys=True).encode()).hexdigest()


def cmd_validate(a):
    feed, msgs = feed_messages(a.feed)
    sid = seller_id()
    results = []
    for m in msgs:
        body = {"productType": m["productType"], "requirements": m.get("requirements", "LISTING"),
                "attributes": m["attributes"]}
        d = call("PUT", f"/listings/2021-08-01/items/{q(sid)}/{q(m['sku'])}", {
            "marketplaceIds": MARKETPLACE, "mode": "VALIDATION_PREVIEW", "issueLocale": "en_GB"}, body)
        issues = d.get("issues", [])
        errs = [i for i in issues if i.get("severity") == "ERROR"]
        results.append({"sku": m["sku"], "status": d.get("status"), "errors": len(errs),
                        "warnings": len(issues) - len(errs),
                        "issues": [{"severity": i.get("severity"), "code": i.get("code"),
                                    "message": i.get("message"), "attributes": i.get("attributeNames")} for i in issues]})
        mark = "OK " if not errs else "ERR"
        print(f"{mark} {m['sku']}: {len(errs)} errors, {len(issues) - len(errs)} warnings")
        time.sleep(0.25)  # stay inside the putListingsItem rate limit
    report = {"feed": os.path.abspath(a.feed), "digest": digest(msgs), "seller_id": sid, "marketplace": MARKETPLACE,
              "validated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "total_errors": sum(r["errors"] for r in results), "results": results}
    rp = a.report or os.path.splitext(a.feed)[0] + " - VALIDATION.json"
    json.dump(report, open(rp, "w"), indent=1)
    print(json.dumps({"report": rp, "skus": len(results), "total_errors": report["total_errors"],
                      "clean": report["total_errors"] == 0}, indent=1))


def cmd_submit(a):
    feed, msgs = feed_messages(a.feed)
    rp = a.report or os.path.splitext(a.feed)[0] + " - VALIDATION.json"
    if not a.confirm:
        sys.exit("refusing: submit writes to your live Amazon catalogue - re-run with --confirm after Shaun approves")
    if not os.path.exists(rp):
        sys.exit(f"refusing: no validation report ({rp}) - run validate first")
    rep = json.load(open(rp))
    age = datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(rep["validated_at"])
    if rep["digest"] != digest(msgs):
        sys.exit("refusing: the feed changed since it was validated - validate again")
    if rep["total_errors"]:
        sys.exit(f"refusing: validation found {rep['total_errors']} errors - fix them and validate again")
    if age.total_seconds() > 86400:
        sys.exit("refusing: validation is older than 24 hours - validate again")
    feed["header"]["sellerId"] = seller_id()
    payload = json.dumps(feed, ensure_ascii=False).encode("utf-8")
    ctype = "application/json; charset=UTF-8"
    doc = call("POST", "/feeds/2021-06-30/documents", body={"contentType": ctype})
    up = urllib.request.Request(doc["url"], payload, method="PUT", headers={"Content-Type": ctype})
    with urllib.request.urlopen(up, timeout=120) as r:
        if r.status not in (200, 201):
            sys.exit(f"feed upload failed HTTP {r.status}")
    f = call("POST", "/feeds/2021-06-30/feeds", body={"feedType": "JSON_LISTINGS_FEED",
                                                      "marketplaceIds": [MARKETPLACE],
                                                      "inputFeedDocumentId": doc["feedDocumentId"]})
    print(json.dumps({"submitted": True, "feedId": f.get("feedId"), "messages": len(msgs),
                      "next": f"python3 spapi.py feed-status {f.get('feedId')}"}, indent=1))


def cmd_feed_status(a):
    f = call("GET", f"/feeds/2021-06-30/feeds/{q(a.feed_id)}")
    out = {"feedId": a.feed_id, "status": f.get("processingStatus"), "created": f.get("createdTime"),
           "finished": f.get("processingEndTime")}
    if f.get("resultFeedDocumentId"):
        doc = call("GET", f"/feeds/2021-06-30/documents/{q(f['resultFeedDocumentId'])}")
        with urllib.request.urlopen(urllib.request.Request(doc["url"], headers={"User-Agent": UA}), timeout=120) as r:
            raw = r.read()
        if doc.get("compressionAlgorithm") == "GZIP":
            raw = gzip.decompress(raw)
        res = json.loads(raw)
        path = a.out or f"feed-{a.feed_id}-result.json"
        json.dump(res, open(path, "w"), indent=1)
        out["summary"] = res.get("summary")
        out["issues"] = [{"sku": i.get("sku"), "severity": i.get("severity"), "message": i.get("message")}
                         for i in res.get("issues", [])][:50]
        out["result_file"] = path
    print(json.dumps(out, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    s = sub.add_parser("search-types"); s.add_argument("keywords")
    s = sub.add_parser("product-type"); s.add_argument("type"); s.add_argument("--out")
    s = sub.add_parser("get"); s.add_argument("sku")
    s = sub.add_parser("validate"); s.add_argument("feed"); s.add_argument("--report")
    s = sub.add_parser("submit"); s.add_argument("feed"); s.add_argument("--report"); s.add_argument("--confirm", action="store_true")
    s = sub.add_parser("feed-status"); s.add_argument("feed_id"); s.add_argument("--out")
    a = ap.parse_args()
    {"check": cmd_check, "search-types": cmd_search_types, "product-type": cmd_product_type, "get": cmd_get,
     "validate": cmd_validate, "submit": cmd_submit, "feed-status": cmd_feed_status}[a.cmd](a)


if __name__ == "__main__":
    main()
