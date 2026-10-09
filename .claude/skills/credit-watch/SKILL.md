---
name: credit-watch
description: Audit unused credits across connected AI services (Higgsfield, Magnific) and flag what will be lost at the next monthly reset, then propose concrete work to spend them on. Use this skill whenever the user asks about credits, balances, quotas, allowances, "how many credits do I have", when a plan resets or renews, whether they are wasting or missing out on credits, or whether they should top up or upgrade — and also whenever a scheduled credit sweep fires. Use it even when the user names only one service, because the point is to catch the services they forgot about.
---

# Credit Watch

## Why this exists

Pre-paid monthly allowances are the easiest money to waste. The subscription is already
paid for, so an unspent credit is not a saving — it is a sunk cost that may vanish at the
next renewal. The failure mode is quiet: nothing breaks, no alert fires, the balance just
resets and the month's value is gone.

The specific trap is **asymmetric attention**. One service gets used daily and is
front-of-mind; another sits at 7% utilisation because nobody thought to check it. So the
job here is not "report a number" — it is to find the service that is being forgotten and
put concrete, useful work in front of the user with enough days left to actually do it.

Run this ~7 days before the earliest reset. Seven days is deliberate: enough time to
actually produce something, not so far out that it gets ignored.

## Step 1 — Read every balance

Read `references/services.md` for the per-service tool calls, cycle anchors and caveats.
It is the registry; keep it current as services are added or dropped.

Check **every** service in the registry, not just the one the user mentioned. The
forgotten service is the whole reason this skill exists. Balance reads are free and
read-only, so there is no cost to being thorough.

If a service's tools are not loaded, load them (`ToolSearch`) before concluding anything.
A service you could not reach is **unknown**, not zero — say so rather than omitting it,
because silently dropping a service recreates exactly the blind spot this skill exists to
close.

## Step 2 — Work out what is actually at risk

For each service, establish three things:

1. **Balance** — what is sitting there now.
2. **Days until reset** — from the cycle anchor in the registry.
3. **What the reset does to it** — this is the part that decides whether anything is
   urgent, and it varies by service. Credits that roll over are not at risk and should not
   be presented as if they were. Credits that are zeroed, or an allowance that is
   re-granted up to a cap, are genuinely use-it-or-lose-it.

Where the registry marks rollover behaviour as unconfirmed, say it is unconfirmed. A
confident wrong claim here causes real harm in both directions: panic-spending credits
that were never at risk, or ignoring ones that were.

## Step 3 — Report it

Lead with what is at risk, not with an inventory. Keep it to a table plus a verdict:

```
| Service | Balance | Used this cycle | Resets | At risk |
|---------|---------|-----------------|--------|---------|
```

Then one line per service that needs action, and nothing for the ones that don't. If
everything is healthy, say so in a sentence — a sweep that finds nothing is a good
outcome and does not need padding.

## Step 4 — Propose work, not just numbers

A reminder that says "you have 222,150 credits" changes nothing. A reminder that says
"here are four product shots I can generate this afternoon" gets acted on.

Propose 2–4 concrete jobs sized to the balance and the days remaining, drawn from what
the user actually does — check their connected stores and recent work rather than
inventing generic suggestions. Note the approximate credit cost of each so the user can
choose, and prefer jobs that produce something reusable (a product shot, an ad set, an
upscaled asset) over throwaway generations.

Then stop and let them pick. **Never spend credits to "use them up" without explicit
approval for that specific job** — unrequested spending is the opposite of helpful here,
and a wasted credit the user chose to leave unspent is better than one spent on something
they did not want.

## Step 5 — Log what you observed

Append this sweep's figures to `references/cycle-log.md`. This matters more than it looks:
some services expose a balance but no transaction history, so the only way to learn their
reset date is to watch the numbers move across sweeps. A few logged readings turn an
unknown cycle into a known one.

If an observed reset date contradicts the anchor in `references/services.md`, update the
registry and tell the user their scheduled sweep may need moving.

## Keeping the schedule honest

This skill is the procedure; a Routine on the user's account is what makes it fire. If the
cycle anchor moves, the Routine's cron needs updating too — flag it rather than assuming
the user will notice, since a sweep that fires on the wrong day is worse than useless.
