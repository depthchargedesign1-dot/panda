# Face-mask copy QA fix set (6 Oct 2026)
Built by `scratchpad/qa/engine.py` from a live export taken 6 Oct (qa/dl1/live.jsonl). `expected.json` holds old and new values for all 2,850 products.
130 products (sensitive rewrites, wrong-person copy, character disclaimers) were pushed directly; the other 2,720 are here:
`batches/b0000–b0543.gql`, 5 productUpdate aliases each (descriptionHtml and/or seo{title, description}; both SEO fields always sent together).
Only descriptionHtml / SEO change. No titles, handles, status, tags, prices, images. Round-trip checked: every literal parses back to expected.json (0 mismatches).

To send: `./show.sh qa NNNN` -> mcp__Shopify__graphql_mutation unchanged -> `./log.sh qa NNNN ok|error`.
Order is by priority: names/couples/leakage first, SEO titles next, themed-duplication-only last (b0441–b0543).
After sending: bulk-export id, descriptionHtml, seo and run `python3 qa/verify_qa.py export.jsonl` (fixed / not pushed / drift).
Rollback: expected.json[id].old has every previous value.
