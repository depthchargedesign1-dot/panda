# Phase 3 status (6 Oct 2026)
- Fresh recursive listing: phase3/list/all-p01..p22.json (13,054 entries) taken before any phase-3 action.
- MH/JB variant moves: listing showed NONE of the 58 in phase2/mhjb-entries.json had been moved (all still at source, dest names free).
  Submitted all 58 as one move job (autorename=false). operation_id saved in phase3/mhjb-op.txt. Result -> phase2/jobMHJB.json.
- 07:55 my MH/JB job failed (duplicated paths): the other agent's identical job had already moved all 58 at 07:53 (mhjb-moves-log.csv). Nothing to redo.
- Rename plan: tools/rename_plan.py + tools/rename_overrides.py -> rename-plan.csv (5,307), rename-skipped.csv, rename-conflicts.csv.
  Batches: phase3/batches/b01..b11.json (folder-id destinations). renames-log.csv starts all 'pending'; tools/rename_log.py fills status from a fresh re-listing.
- 08:12 INCIDENT (no harm): a move call for batch a01 was sent before the batch file had been read back, and 36 of its 54
  entries were wrong (ids not in the plan, one id belonging to /CREATIVE SUITE 6/.../Media_db.db). The job id came back
  INVALID and nothing ran: checked by metadata that the first planned file (BEN AINSLEY.JPG), all 9 wrong in-root ids and
  the Media_db.db id are unchanged, and two wrong destinations do not exist. Record: phase3/incident/sent-0812.json.
  From here every batch is sent only from lines read back from phase3/b250/*.txt (250 per batch), and each job result
  is checked against its batch by tools/check_job.py before the next one. phase3/batches/ (500s) is superseded.
- 08:11-08:12 a01 entries 1-125 renamed: 125/125 success (path-based).
- Owner asked (via coordinator) for as few move calls as possible: remaining work packed by tools/rename_batches_1000.py into
  phase3/b1000/p1-01..06 (normal renames + case-only step 1 to TMPCASE, 5,180) and p2-01..02 (TMPCASE -> final, 1,611).
p1-01 submitted 08:3x op=AUACi-3dEYi-UEr4BFQ-_8GS1XZpDYMZS1tI8c7OsAjG3_JIJZbCdot2ChixgQ8G2EfQtc0QWQM4h-L2DQgUSubUJKzLy0wNksgiXptOQf0WyiXMG38DoAaDpoFVWw8RigzSqkJSX-Vo3xiXQDwvvfQ4lCtvRJb05YdxTrarUxIf9ZaCkt1hDNjstmB663jXZzenOYhPLtwtF8jYu-vrMh3bi_Jye-HYnuGT2oi8CzagpA
- Known imperfect names in p1-01 to correct in pass 2 (rename again): MOVIE STARS/"Gus Bad.jpg" -> "Gus (Breaking Bad) 2.jpg";
  "Gease (Sandy2).jpg" -> "Sandy (Grease) 2.jpg"; "Adrian Brody JB.jpg" -> "Adrien Brody JB.jpg".
- 08:55 sent p1-01 (op AUACi-3d...) completed: 1000/1000 success, result phase3/results/sent-p1-01.json
- 08:58 review before next batch: fixed Scarface->Scar, LOTR abbreviations, Boy George, MK1, TOWIE's, Hassini, Donald+Trump,
  acronyms (NKOTB, JFK, LMFAO, SZA, C3PO), Gandhi, Sweden, number leftovers (overrides). Plan/batches regenerated:
  p1 4,174 (p1-01..05), p2 1,612 (adds pass-2 fixes for already-sent "Aragorn Lotr.jpg" and "Lotr (Gollum).jpg" in CARTOON).
- p1-01 (new numbering) saved as phase3/sent/p1-02.json before sending.
- 09:06 sent p1-02 (= b1000/p1-01 after review; saved sent/p1-02.json) op=AUCZyQyhAoUkIgBxIrWyTpFf9SnVM1ALpTAkTqvncOA91_z77NuakLeLiNkizOdbVkXh6N9dwgeEYiNUAuB_Azhn3bneoz8NJJoclYPsPYzEucsYMkXjvF4ARSJmvIfbZYZF-9GQypfKrRlNbe1d71BxLcU4euCIwObKbLbn3AL4s5ExeI25hUuCgxN7HvAi_xS9MqiUakvfA-6D9-2jyfMC8coxbJDQSSij4FEnDyp07A
