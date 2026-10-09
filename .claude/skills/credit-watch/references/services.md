# Service registry

Every credit-metered service, how to read it, and what its reset actually does.
Update this file whenever a service is added, dropped, or a cycle anchor is observed to
have moved.

## Higgsfield

- **Plan observed:** Plus
- **Read balance:** `mcp__Higgsfield__balance` → `{credits, subscription_plan_type}`
- **Read history:** `mcp__Higgsfield__transactions` (paginated, newest first; `cursor` is
  an offset, so you can jump deep rather than page through thousands of rows)
- **Cycle anchor:** the **8th of the month**, around **17:50–18:35 UTC**
- **Monthly grant:** ~1,125–1,200 credits (varied between the two observed cycles)
- **Rollover:** leftover credits **did** carry over on the Oct 8 2026 renewal — a balance
  of 0.24 survived into the new cycle. Treat Higgsfield as rolling over, with one caveat
  below.

**The caveat worth understanding.** The Sep 8 2026 ledger shows a
`Subscription Credits Reset` of −195 that zeroed the balance before the new grant. That
looked like routine use-it-or-lose-it behaviour, but it sat alongside two grants an hour
apart (+270, then +1,125), which is the signature of a **plan change**, not a renewal. The
next renewal carried the balance over instead. So: the −195 was almost certainly tied to
the upgrade, and normal renewals appear to roll over. This is inferred from two cycles —
if a third renewal zeroes the balance, correct this file.

**Finding grants in the ledger:** nearly every row is a spend. Probe with `size: 1` at
increasing `cursor` offsets to bracket the date range, then read a window around the
boundary. Grants appear as `action: "grant"`, named `Subscription Credits`.

## Magnific

- **Plan observed:** Premium
- **Read balance:** `mcp__Magnific__account_balance` →
  `plan.{tier, isPaidPlan, isUnlimitedMode}` and
  `credits.{available, totalPlan, spent, hasExtraCredits}`
- **Read history:** none available — `account_balance` explicitly carries no history
- **Cycle anchor:** **unknown.** Must be learned by observation.
- **Allowance:** `totalPlan` 240,000
- **Rollover:** unknown, and the shape of the data suggests a capped re-grant rather than
  accumulation (`available + spent ≈ totalPlan`), which would make it use-it-or-lose-it.
  Do not assert this until observed.

**How to learn the cycle without a history endpoint.** `credits.spent` counts usage within
the current cycle. When a new cycle begins, `spent` drops back toward 0 and `available`
returns toward `totalPlan`. Log both figures on every sweep (Step 5) and the date `spent`
collapses is the reset date. Two or three sweeps should pin it down.

**This is the service at risk.** As of 9 Oct 2026: 222,150 of 240,000 available, 17,850
spent — **7.4% utilisation**. If this allowance does not roll over, the overwhelming
majority of it is being discarded every cycle. Lead with Magnific in the report until
utilisation improves or rollover is confirmed.

## Connected but not credit-metered

Check these only if the user asks; they have no credit allowance to waste.

- **Shopify** (Foxy Printing, foxyprinting.co.uk) — no credit meter. Useful as the *source
  of work* for spending credits: products needing shots, ads or upscales.
- **Gmail / Google Drive / Dropbox** — storage quotas, not resetting credit allowances.
  Storage fills up rather than resetting, so it is a different problem; mention only if
  near a limit.
- **GitHub, Claude Docs** — no credit meter.

## Adding a service

A service belongs here once it has a **pre-paid allowance that resets**. For each one
record: how to read the balance, how to read history (or that there is none), the cycle
anchor, the allowance size, and whether unused credits survive the reset — that last field
is the one that decides urgency, so never leave it blank. Write `unknown` and a note on
how to find out.
