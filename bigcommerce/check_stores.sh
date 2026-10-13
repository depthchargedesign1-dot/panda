#!/usr/bin/env bash
# Finds every BigCommerce store configured as a pair of environment variables
#   BC_<NAME>_ACCESS_TOKEN  and  BC_<NAME>_STORE_HASH
# and checks what the token can read and whether it can write. Makes no changes.
set -u

names=$(env | sed -n 's/^BC_\(.*\)_ACCESS_TOKEN=.*/\1/p' | sort)
if [ -z "$names" ]; then
  echo "No stores found. Add BC_<NAME>_ACCESS_TOKEN and BC_<NAME>_STORE_HASH to the environment."
  exit 1
fi

fail=0
for n in $names; do
  tok_var="BC_${n}_ACCESS_TOKEN"; hash_var="BC_${n}_STORE_HASH"
  tok="${!tok_var}"; hash="${!hash_var:-}"
  echo "== $n =="
  if [ -z "$hash" ]; then echo "  missing $hash_var"; fail=1; continue; fi
  base="https://api.bigcommerce.com/stores/$hash"
  auth=(-H "X-Auth-Token: $tok" -H "Accept: application/json" -H "Content-Type: application/json")

  store=$(curl -sS "${auth[@]}" "$base/v2/store")
  name=$(printf '%s' "$store" | python3 -c 'import sys,json
try: d=json.load(sys.stdin); print(d["name"], "-", d["domain"])
except Exception: print("")')
  if [ -z "$name" ]; then echo "  cannot connect (bad token or store hash)"; fail=1; continue; fi
  echo "  store: $name"

  for p in v2/orders v3/catalog/products v3/customers v3/catalog/categories v2/coupons \
           v3/content/scripts v3/themes v3/hooks v2/shipping/zones v3/settings/store/profile; do
    code=$(curl -sS -o /dev/null -w '%{http_code}' "${auth[@]}" "$base/$p?limit=1")
    case $code in 200|204) r=read;; 403) r="NO ACCESS";; *) r="HTTP $code";; esac
    printf '  %-28s %s\n' "$p" "$r"
  done

  # Write probe: an empty product batch update is rejected with 422 when the token
  # may write, and 403 when it is read-only. Nothing is changed either way.
  code=$(curl -sS -o /dev/null -w '%{http_code}' -X PUT "${auth[@]}" -d '[]' "$base/v3/catalog/products")
  case $code in 403) w="read-only";; 401) w="unauthorised";; *) w="can modify (HTTP $code)";; esac
  echo "  catalog write access:        $w"
done
exit $fail
