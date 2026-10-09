"""PUT cleaned images to Shopify staged-upload targets.
Input lines: <media_id> <uuid> <filename> <signature> <x-goog-date>
Prints: <media_id> <http status> <resourceUrl>"""
import sys, subprocess
CLEAN = sys.argv[1]
BASE = 'https://shopify-staged-uploads.storage.googleapis.com/tmp/17749115/files/'
for line in sys.stdin:
    if not line.strip(): continue
    mid, uuid, fn, sig, date = line.split()
    url = (f'{BASE}{uuid}/{fn}?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=merchant-assets%40shopify-tiers.iam.gserviceaccount.com'
           f'%2F{date[:8]}%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date={date}&X-Goog-Expires=604800&X-Goog-SignedHeaders=host&X-Goog-Signature={sig}')
    code = subprocess.run(['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', '-X', 'PUT', '-H', 'Content-Type: image/jpeg',
                           '--data-binary', f'@{CLEAN}/{mid}.jpg', url], capture_output=True, text=True).stdout
    print(mid, code, f'{BASE}{uuid}/{fn}', flush=True)
