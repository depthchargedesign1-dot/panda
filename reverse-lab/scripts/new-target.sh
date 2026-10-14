#!/usr/bin/env bash
# Start a new investigation folder from the template.
#   scripts/new-target.sh websites example-shop
#   scripts/new-target.sh games my-game
set -euo pipefail
kind="${1:?usage: new-target.sh <websites|games|apps> <name>}"
name="${2:?usage: new-target.sh <websites|games|apps> <name>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
case "$kind" in websites|games|apps) ;; *) echo "kind must be websites, games or apps" >&2; exit 1 ;; esac
dir="$root/targets/$kind/$name"
[ -e "$dir" ] && { echo "$dir already exists" >&2; exit 1; }
mkdir -p "$dir/evidence"
sed -e "s/{{NAME}}/$name/g" -e "s/{{KIND}}/$kind/g" -e "s/{{DATE}}/$(date +%F)/g" \
  "$root/targets/TEMPLATE.md" > "$dir/README.md"
echo "Created $dir"
