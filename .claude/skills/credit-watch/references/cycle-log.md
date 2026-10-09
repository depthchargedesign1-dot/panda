# Cycle log

Observed readings, newest first. Append one block per sweep.

The point of this file is to learn reset dates for services that expose a balance but no
transaction history. Record the figures even when nothing looks interesting — the value is
in the series, not any single reading.

Columns: date read (UTC) · service · balance / allowance · spent this cycle · notes

---

## 2026-10-09

| Service | Balance / allowance | Spent this cycle | Notes |
|---|---|---|---|
| Higgsfield | 1,195.74 | — | Renewed 8 Oct 17:52 UTC, grant +1,200. Prior balance 0.24 **carried over** (1,200 + 0.24 − 4.5 spent = 1,195.74), so no reset-deduct this cycle. |
| Magnific | 222,150 / 240,000 | 17,850 | **7.4% utilisation.** Reset date still unknown — watch for `spent` collapsing toward 0. |

## 2026-10-08 (Higgsfield renewal, reconstructed from ledger)

| Service | Balance / allowance | Spent this cycle | Notes |
|---|---|---|---|
| Higgsfield | 0.24 → 1,200.24 | ~1,125 over the cycle | Grant +1,200 at 17:52 UTC. No `Subscription Credits Reset` row — balance rolled over. |

## 2026-09-08 (Higgsfield, reconstructed from ledger)

| Service | Balance / allowance | Spent this cycle | Notes |
|---|---|---|---|
| Higgsfield | — | — | Earliest ledger entry: 17:41 UTC grant +270. Then at 18:34 UTC: `Subscription Credits Reset` −195, grant +1,125, `Concurrent Boost Credits` +100. Two grants an hour apart = plan change, so the −195 is probably upgrade-related rather than routine renewal behaviour. |
