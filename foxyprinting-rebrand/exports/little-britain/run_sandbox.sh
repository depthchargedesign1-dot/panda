#!/bin/bash
# Runs in the Higgsfield sandbox. Args: BG_PAIR_URL BG_PACK_URL  (targets.json = {"file": "staged PUT url"} in CWD)
set -e
RAW=https://raw.githubusercontent.com/depthchargedesign1-dot/panda/claude/foxyprinting-rebrand-shopify-usf2x9/foxyprinting-rebrand
CF=https://d2ol7oe51mr4n9.cloudfront.net/user_3HUr7G8la20J0fiH66SaF8cNGi7
pip install -q numpy "opencv-python-headless<5" reportlab pikepdf >/dev/null 2>&1 || true
mkdir -p src out
curl -sfo lb_build.py "$RAW/exports/little-britain/lb_build.py"
curl -sfo mask_cutline.py "$RAW/tools/artwork/mask_cutline.py"
curl -sfo README.txt "$RAW/exports/little-britain/README%20-%20how%20to%20print%20and%20cut.txt"
curl -sfo src/lou.jpg $CF/041491c7-f99a-4c61-a109-bd6f2971cfe1.jpg
curl -sfo src/andy.jpg $CF/a2654bcf-0cd9-4580-874f-81e94e3ff0df.jpg
curl -sfo src/vicky.jpg $CF/eee552e0-dca2-4862-a26f-64f3651e479a.jpg
curl -sfo src/bubbles.png $CF/5492ffeb-ebb7-4c30-bf28-ba3379b3d9b7.png
python3 lb_build.py src out "$1" "$2"
python3 mask_cutline.py out/art/*.jpg --out out/cut
mk(){ d="$1"; shift; mkdir -p "z/$d"; for n in "$@"; do cp out/cut/"$n"* out/art/"$n.jpg" "z/$d/"; done; cp README.txt "z/$d/README - how to print and cut.txt"; (cd z && zip -qr "../out/$d.zip" "$d"); }
mk lou-and-andy-couple-mask-pair-artwork "Lou Todd" "Andy Pipkin"
mk little-britain-characters-face-mask-pack-artwork "Vicky Pollard" "Lou Todd" "Andy Pipkin" "Bubbles DeVere"
ls -la out out/cut
python3 - <<'PY'
import json, subprocess
for f, u in json.load(open("targets.json")).items():
    ct = "application/zip" if f.endswith(".zip") else "image/jpeg"
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: " + ct, "--data-binary", "@out/" + f, u], capture_output=True, text=True)
    print(r.stdout, f)
PY
cd out && convert little-britain-characters-face-mask-pack-check.jpg lou-and-andy-couple-mask-pair-check.jpg -append -resize 1200x review.jpg
convert cut/*check.png -resize x380 +append -quality 70 cutreview.jpg
md5sum *.zip
