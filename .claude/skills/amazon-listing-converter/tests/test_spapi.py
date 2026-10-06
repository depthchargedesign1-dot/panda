#!/usr/bin/env python3
"""Runs spapi.py against a local mock of Amazon (LWA + SP-API). Run: python3 tests/test_spapi.py"""
import gzip, json, os, subprocess, sys, tempfile, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "spapi.py")
STATE = {"uploads": [], "puts": []}


class Mock(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, obj, raw=None):
        body = raw if raw is not None else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n)

    def authed(self):
        if self.headers.get("x-amz-access-token") != "AT-123":
            self.send(403, {"errors": [{"code": "Unauthorized"}]})
            return False
        return True

    def do_POST(self):
        b = self.body()
        if self.path == "/auth/o2/token":
            ok = b"refresh_token=RT-good" in b and b"client_secret=CS" in b
            return self.send(200, {"access_token": "AT-123", "expires_in": 3600}) if ok else \
                self.send(400, {"error": "invalid_grant"})
        if not self.authed():
            return
        if self.path == "/feeds/2021-06-30/documents":
            return self.send(201, {"feedDocumentId": "DOC1", "url": f"http://127.0.0.1:{PORT}/upload/DOC1"})
        if self.path == "/feeds/2021-06-30/feeds":
            assert json.loads(b)["feedType"] == "JSON_LISTINGS_FEED"
            return self.send(202, {"feedId": "FEED9"})
        self.send(404, {})

    def do_PUT(self):
        b = self.body()
        if self.path.startswith("/upload/"):
            STATE["uploads"].append(json.loads(b))
            return self.send(200, {}, b"")
        if not self.authed():
            return
        if self.path.startswith("/listings/2021-08-01/items/SELLER1/"):
            assert "mode=VALIDATION_PREVIEW" in self.path
            STATE["puts"].append(self.path)
            sku = self.path.split("/")[5].split("?")[0]
            issues = [{"severity": "ERROR", "code": "90220", "message": "item_name required", "attributeNames": ["item_name"]}] \
                if "BAD" in sku else [{"severity": "WARNING", "code": "1", "message": "add more images"}]
            return self.send(200, {"sku": sku, "status": "VALID" if "BAD" not in sku else "INVALID", "issues": issues})
        self.send(404, {})

    def do_GET(self):
        if self.path == "/result/R1":
            return self.send(200, None, gzip.compress(json.dumps(
                {"summary": {"messagesProcessed": 2, "messagesAccepted": 2, "messagesInvalid": 0}, "issues": []}).encode()))
        if not self.authed():
            return
        if self.path.startswith("/sellers/v1/marketplaceParticipations"):
            return self.send(200, {"payload": [{"marketplace": {"id": "A1F83G8C2ARO7P", "name": "Amazon.co.uk",
                                                                "countryCode": "GB"},
                                                "participation": {"isParticipating": True, "hasSuspendedListings": False}}]})
        if self.path.startswith("/feeds/2021-06-30/feeds/FEED9"):
            return self.send(200, {"processingStatus": "DONE", "resultFeedDocumentId": "R1"})
        if self.path.startswith("/feeds/2021-06-30/documents/R1"):
            return self.send(200, {"url": f"http://127.0.0.1:{PORT}/result/R1", "compressionAlgorithm": "GZIP"})
        self.send(404, {})


srv = HTTPServer(("127.0.0.1", 0), Mock)
PORT = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, SPAPI_ENDPOINT=f"http://127.0.0.1:{PORT}", SPAPI_LWA_URL=f"http://127.0.0.1:{PORT}/auth/o2/token",
           SPAPI_CLIENT_ID="CID", SPAPI_CLIENT_SECRET="CS", SPAPI_REFRESH_TOKEN="RT-good", SPAPI_SELLER_ID="SELLER1",
           NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")


def run(*args, ok=True, e=env):
    r = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, env=e)
    assert (r.returncode == 0) == ok, (args, r.stdout, r.stderr)
    return r


with tempfile.TemporaryDirectory() as d:
    # connection check
    out = json.loads(run("check").stdout)
    assert out["uk_ready"] is True
    # bad refresh token is reported clearly
    r = run("check", ok=False, e=dict(env, SPAPI_REFRESH_TOKEN="RT-bad"))
    assert "refused the credentials" in r.stderr
    # missing credentials
    r = run("check", ok=False, e={k: v for k, v in env.items() if k != "SPAPI_CLIENT_ID"})
    assert "SPAPI_CLIENT_ID" in r.stderr
    feed = {"header": {"sellerId": "YOUR_SELLER_ID", "version": "2.0", "issueLocale": "en_GB"}, "messages": [
        {"messageId": 1, "sku": "FOXY-SUB-A-01", "operationType": "UPDATE", "productType": "DRINKING_CUP",
         "requirements": "LISTING", "attributes": {"item_name": [{"value": "Mug"}]}},
        {"messageId": 2, "sku": "FOXY SUB/B 02", "operationType": "UPDATE", "productType": "DRINKING_CUP",
         "requirements": "LISTING", "attributes": {"item_name": [{"value": "Mug 2"}]}}]}
    fp = os.path.join(d, "feed.json")
    json.dump(feed, open(fp, "w"))
    # submit refuses without --confirm and without validation
    assert "refusing" in run("submit", fp, ok=False).stderr
    assert "no validation report" in run("submit", fp, "--confirm", ok=False).stderr
    # validation is preview-only and URL-encodes SKUs
    v = json.loads(run("validate", fp).stdout.split("\n", 2)[-1])
    assert v["clean"] is True and len(STATE["puts"]) == 2 and "FOXY%20SUB%2FB%2002" in STATE["puts"][1]
    # editing the feed after validation blocks submit
    feed["messages"][0]["attributes"]["item_name"][0]["value"] = "Changed"
    json.dump(feed, open(fp, "w"))
    assert "changed since it was validated" in run("submit", fp, "--confirm", ok=False).stderr
    # a validation with errors blocks submit
    feed["messages"][0]["sku"] = "FOXY-BAD-01"
    json.dump(feed, open(fp, "w"))
    run("validate", fp)
    assert "validation found 1 errors" in run("submit", fp, "--confirm", ok=False).stderr
    # clean validate + confirm -> feed created, seller id filled in
    feed["messages"][0]["sku"] = "FOXY-SUB-A-01"
    json.dump(feed, open(fp, "w"))
    run("validate", fp)
    s = json.loads(run("submit", fp, "--confirm").stdout)
    assert s["feedId"] == "FEED9" and STATE["uploads"][-1]["header"]["sellerId"] == "SELLER1"
    st = json.loads(run("feed-status", "FEED9", "--out", os.path.join(d, "res.json")).stdout)
    assert st["status"] == "DONE" and st["summary"]["messagesAccepted"] == 2
print("all SP-API client checks passed")
