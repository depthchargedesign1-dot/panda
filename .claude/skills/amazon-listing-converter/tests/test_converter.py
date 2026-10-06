#!/usr/bin/env python3
"""Checks the converter on real Foxy Printing products. Run: python3 tests/test_converter.py"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "shopify_to_amazon.py")

with tempfile.TemporaryDirectory() as out:
    r = subprocess.run([sys.executable, SCRIPT, os.path.join(HERE, "shopify_sample.json"),
                        os.path.join(HERE, "shopify_export_sample.csv"), "--out", out,
                        "--template", os.path.join(HERE, "mock_amazon_template.xlsx")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    summary = json.loads(r.stdout)
    feed = json.load(open(next(os.path.join(out, f) for f in os.listdir(out) if f.endswith(".json") and "FEED" in f)))
    msgs = {m["sku"]: m for m in feed["messages"]}

    # IP safety + drafts held back
    assert "FOXY-MUG-SIMON-COWELL" not in msgs
    assert "FOXY-DRAFT-01" not in msgs
    assert summary["held_back"] == 2
    # variations: parent + 5 children, children point at parent, theme set, parent has no offer
    p = msgs["FOXY-SUB-FNPMSZSM-PARENT"]["attributes"]
    assert p["parentage_level"][0]["value"] == "parent" and "purchasable_offer" not in p
    for i in range(1, 6):
        c = msgs[f"FOXY-SUB-FNPMSZSM-0{i}"]["attributes"]
        assert c["child_parent_sku_relationship"][0]["parent_sku"] == "FOXY-SUB-FNPMSZSM-PARENT"
        assert c["variation_theme"][0]["name"] == "STYLE" and c["style"][0]["value"]
    assert msgs["FOXY-SUB-PFSM-BWH-01"]["attributes"]["color"][0]["value"] == "Blue & White Hoops"
    # personalisation detected from tags / title / description
    assert set(summary["custom_templates"]) == {"FOXY - Name", "FOXY - Name + Age + Message", "FOXY - Name + Number"}
    # Amazon Custom must be merchant fulfilled
    assert msgs["Foxy-Mug-X09"]["attributes"]["fulfillment_availability"][0]["fulfillment_channel_code"] == "DEFAULT"
    # contact details removed, valid EAN used, invalid -> exemption
    d = msgs["Foxy-Mug-X09"]["attributes"]["product_description"][0]["value"]
    assert "@" not in d and "foxyprinting" not in d.lower() and ".co.uk" not in d
    assert msgs["Foxy-Mug-X11"]["attributes"]["externally_assigned_product_identifier"][0]["value"] == "5050177994027"
    assert "supplier_declared_has_product_identifier_exemption" in msgs["Foxy-Mug-X09"]["attributes"]
    # internal tags never reach keywords
    for m in feed["messages"]:
        kw = m["attributes"].get("generic_keyword", [{"value": ""}])[0]["value"]
        assert "agenamemessage" not in kw and "facebook" not in kw and "rude" not in kw, kw
        assert len(kw.encode()) < 250
    assert summary["template_columns_left_blank"] == []
print("all converter checks passed")
