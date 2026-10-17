#!/bin/bash
# Higgsfield sandbox: build all mug mockups, review sheets, then wait for targets*.json + GO and PUT to Shopify staged uploads.
cd /home/user && rm -rf w && mkdir -p w/sc w/tex && cd w
RAW=https://raw.githubusercontent.com/depthchargedesign1-dot/panda/$REF/foxyprinting-rebrand
C=https://d8j0ntlcm91z4.cloudfront.net/user_3HUr7G8la20J0fiH66SaF8cNGi7
curl -sfo m.py $RAW/tools/artwork/number_plate_mug_mockups.py
curl -sfo products.json $RAW/exports/number-plate-mugs/products.json
i=0
for f in hf_20261006_085203_2fb082ef-df6e-4475-b7fc-1d94bcf8aaf6 hf_20261006_085202_0f064f45-4de3-4c58-93dc-f722b7829db1 hf_20261006_085200_adcc5b2d-a22c-42e2-9d9f-2e22404c3e0d hf_20261006_085201_f411a218-e784-4969-b251-80e1e444e723 hf_20261006_085201_1526e52d-0305-4a45-a681-6831c1def581 hf_20261006_085201_b3d63c73-dda6-45ab-9c70-9f2429dbb1e4 hf_20261006_085202_ce3bd97d-7dcb-45e7-a8a9-335be4ce9684 hf_20261006_085202_fbc01373-d05f-4b92-8b4d-f5bed017a331 hf_20261006_085608_3e009673-4d08-480d-ba4f-edcee71aef69; do curl -sfo sc/s$i.png $C/$f.png & i=$((i+1)); done
python3 -c "import json;[print(p['sku_base']) for p in json.load(open('products.json'))]" > skus.txt
for sb in $(cat skus.txt); do for c in GB SCO CYM NI IRL; do echo "$RAW/exports/number-plate-mugs/textures/$sb-$c-wrap.png"; done; done > texurls.txt
(cd tex && xargs -P 16 -n 1 curl -sfO < ../texurls.txt); wait
echo "tex: $(ls tex | wc -l)"
python3 m.py sc tex products.json out
cd out && for sb in $(cat ../skus.txt); do montage $sb-*-mockup.jpg $sb-wrap-views.jpg $sb-flat-wrap.jpg $sb-life-*.jpg -tile 3x3 -geometry 300x300+2+2 -quality 70 ../sheet-$sb.jpg; done; cd ..
echo RENDERED
for k in $(seq 1 160); do [ -f GO ] && break; sleep 5; done
python3 - <<'PY'
import json, glob, subprocess
t = {}
for f in sorted(glob.glob("targets*.json")): t.update(json.load(open(f)))
ok = 0
for fn, url in t.items():
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: image/jpeg", "--upload-file", "out/" + fn, url], capture_output=True, text=True)
    ok += r.stdout == "200"
    if r.stdout != "200": print("FAIL", r.stdout, fn)
print("uploaded", ok, "of", len(t))
PY
echo DONE
