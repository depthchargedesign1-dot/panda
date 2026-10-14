#!/usr/bin/env bash
# Open a URL in a throwaway Chromium that REA can observe over CDP, then list its tabs.
#   scripts/browser.sh https://example.com          (headless)
#   HEADED=1 scripts/browser.sh https://example.com (visible window, so you can click around)
# Then: rea analyze-web-bundle http://127.0.0.1:9222 <target_id> --format json
set -euo pipefail
url="${1:?usage: browser.sh <url>}"
port="${CDP_PORT:-9222}"
chrome="${CHROME:-}"
if [ -z "$chrome" ]; then
  for c in /opt/pw-browsers/chromium-*/chrome-linux/chrome google-chrome chromium chromium-browser \
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then chrome="$c"; break; fi
  done
fi
[ -n "$chrome" ] || { echo "No Chromium/Chrome found; set CHROME=/path/to/chrome" >&2; exit 1; }
profile="$(mktemp -d)"
flags=(--remote-debugging-port="$port" --user-data-dir="$profile" --no-first-run)
[ "${HEADED:-0}" = 1 ] || flags+=(--headless=new)
[ "$(id -u)" = 0 ] && flags+=(--no-sandbox)
"$chrome" "${flags[@]}" "$url" >/dev/null 2>&1 &
echo "Chromium pid $! on CDP port $port (profile $profile). Stop it with: kill $!"
sleep 3
rea list-browser-targets "http://127.0.0.1:$port" --format md
