# BigCommerce store access

Each store is a pair of environment variables in the cloud environment
(environment menu → Edit → Network secrets, or environment variables):

| Variable | Value |
|---|---|
| `BC_<NAME>_ACCESS_TOKEN` | Access token from Settings → API → Store-level API accounts |
| `BC_<NAME>_STORE_HASH` | The code after `/stores/` in the API path |

`<NAME>` is any short label (e.g. `CPP`, `FOXY`). Start a new session after
adding them, then run:

    bigcommerce/check_stores.sh

It lists every configured store, what each token can read, and whether it can
modify the catalog. It makes no changes.
