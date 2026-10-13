# Working notes for Claude

This repo is the shared workspace for Depth Charge Design's online shops. Every
cloud session starts from a fresh copy, so anything Claude should remember
between sessions goes in this file (or `memory/` if it gets long).

## The business

| Store | Platform | Domain | Env var prefix |
|---|---|---|---|
| Foxy Printing (personalised party printing) | Shopify (connector) | foxyprinting.co.uk | n/a, use the Shopify connector |
| Celebrity Poster Prints | BigCommerce | celebrity-poster-prints.com | `BC_POSTERS_` |
| Personalised Cards | BigCommerce | personalised-cards.co.uk | `BC_PCARDS_` |
| Celebrity-Facemasks.com | BigCommerce | celebrity-facemasks.com | `BC_FACEMASKS_` |

All stores are UK, GBP, Europe/London.

## How to reach things

- **BigCommerce:** each store is `BC_<NAME>_ACCESS_TOKEN` + `BC_<NAME>_STORE_HASH`
  in the cloud environment. Base URL `https://api.bigcommerce.com/stores/$HASH/`,
  header `X-Auth-Token`. Run `bigcommerce/check_stores.sh` to see which stores are
  configured and whether each token can write. If a store is missing, the user
  needs to add it in the environment settings and start a new session.
- **Shopify, Gmail, Google Drive, Dropbox, Higgsfield, Magnific, Postiz:** claude.ai
  connectors, so use their tools directly.
- **facebook.com is blocked** by the environment's network policy, so ask the user
  to describe a video or post rather than trying to fetch it.

## Rules

- **Live stores.** Reads are fine. Before any write (products, prices, orders,
  customers, themes, scripts, webhooks), say exactly what will change and get a
  yes first. Prefer a dry run or a single item before bulk changes.
- **Secrets.** Never commit tokens, keys or hashes-with-tokens to the repo, and
  never ask the user to paste them into chat. Tell them to add the values to the
  environment settings instead.
- **Talk plainly.** The user runs the shops and isn't a developer: lead with the
  result, skip jargon, give click-by-click steps for anything they must do.

## Repo layout

| Path | What |
|---|---|
| `leavers-designer/` | Foxy Printing leavers hoodie designer (Shopify theme app). See its README and the `foxy-leavers-designer` skill |
| `bigcommerce/` | BigCommerce helper scripts (`check_stores.sh`) |
| `.claude/skills/` | Project skills |
| everything else | An old pandas checkout the repo was forked from. Ignore unless asked |

## Remember

Add new facts here as they come up (store quirks, preferences, decisions), with
the date. Keep it short.

- 2026-10-13: Old read-only Celebrity Poster Prints token was revoked; the new
  full-access one ("grokbot" API account) replaces it.
- 2026-10-13: Decided against OmniRoute (sends work to other AI providers, insecure
  defaults) and Headroom (compresses context; savings overstated). Claude-Mem only
  makes sense on a local machine, so this file does that job for cloud sessions.
