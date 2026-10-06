# Phase 3 status (6 Oct 2026)
- Fresh recursive listing: phase3/list/all-p01..p22.json (13,054 entries) taken before any phase-3 action.
- MH/JB variant moves: listing showed NONE of the 58 in phase2/mhjb-entries.json had been moved (all still at source, dest names free).
  Submitted all 58 as one move job (autorename=false). operation_id saved in phase3/mhjb-op.txt. Result -> phase2/jobMHJB.json.
- 07:55 my MH/JB job failed (duplicated paths): the other agent's identical job had already moved all 58 at 07:53 (mhjb-moves-log.csv). Nothing to redo.
- Rename plan: tools/rename_plan.py + tools/rename_overrides.py -> rename-plan.csv (5,307), rename-skipped.csv, rename-conflicts.csv.
  Batches: phase3/batches/b01..b11.json (folder-id destinations). renames-log.csv starts all 'pending'; tools/rename_log.py fills status from a fresh re-listing.
