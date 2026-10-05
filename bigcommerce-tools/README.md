# BigCommerce API access (three stores, one login)

Shaun's BigCommerce login reaches three stores. Each store needs its **own**
store-level API account, because a token only works for the store it was
made in.

| short name | store | store hash |
|---|---|---|
| `cpp` | Celebrity Poster Prints (www.celebrity-poster-prints.com) | `lf3pkcn41h` |
| `cfm` | Celebrity Face Masks | find in the admin URL (see below) |
| `pc`  | Personalised Cards | find in the admin URL (see below) |

The store hash is the part after `store-` in the admin URL, e.g.
`https://store-lf3pkcn41h.mybigcommerce.com/manage/` gives `lf3pkcn41h`.

## 1. Create a store-level API account (repeat for each store)

1. Log in to the store's admin and go to **Settings** (cog) → under
   *API*, click **Store-level API accounts** → **Create API account**.
2. Token type: **V2/V3 API token**.
3. Name: `Claude read access` (or similar).
4. OAuth scopes: start **read-only** so nothing can be changed by mistake:
   - Content: read-only
   - Checkout content: none
   - Customers: read-only
   - Information & settings: read-only
   - Marketing: read-only
   - Orders: read-only
   - Order transactions: read-only
   - Products: read-only
   - Themes: read-only
   - Carts: read-only
   - Sites & routes: read-only
   - Channel settings: read-only
   - Store logs: read-only
   - Storefront API tokens: none

   Write scopes can be added later for a specific job, store by store.
5. Click **Save**. BigCommerce shows the **Access Token** once and also
   downloads a `.txt` file with it. Keep that file private.

## 2. Store the tokens in the cloud environment (never in the chat)

In the Claude Code session's title bar open the cloud environment menu →
**Edit** → add these as environment variables (or under *API credentials*
if that section is offered):

```
BC_CPP_STORE_HASH=lf3pkcn41h
BC_CPP_ACCESS_TOKEN=<token from step 1>
BC_CFM_STORE_HASH=<hash>
BC_CFM_ACCESS_TOKEN=<token>
BC_PC_STORE_HASH=<hash>
BC_PC_ACCESS_TOKEN=<token>
```

Also under **Network access** add these to *Allowed domains* (or pick a
broader level), keeping the default package-manager list:

```
api.bigcommerce.com
www.celebrity-poster-prints.com
celebrity-poster-prints.com
store-lf3pkcn41h.mybigcommerce.com
```
plus the public domains of the other two stores.

A **new session** picks the variables up.

## 3. Test

```
python3 bigcommerce-tools/bc.py check          # all configured stores
python3 bigcommerce-tools/bc.py orders cpp     # order counts by status
python3 bigcommerce-tools/bc.py storefront cpp # public site health
python3 bigcommerce-tools/bc.py get cpp v2/store
```

`check` prints store name, domain, plan, status, product count and order
count for each store. A `401` means the token is wrong; a `403` means a
scope is missing.

## Notes

- Tokens are read from the environment only. Nothing in this folder
  stores a token, and `.txt` token files must not be committed.
- The API base is `https://api.bigcommerce.com/stores/{hash}/` with the
  `X-Auth-Token` header. Endpoints used here: `v2/store`, `v2/orders`,
  `v2/orders/count`, `v2/order_statuses`, `v3/catalog/products`.
- The older `celebrity-poster-prints-orders` skill drives the admin UI in a
  browser; this tool replaces that for cloud sessions.
