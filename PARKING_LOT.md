# PARKING_LOT — PMAWS

Deferred features, bugs, ideas, and gaps. One line each, dated. Newest first.
An item earns a place here only if it carries enough context to act on in three
weeks having forgotten today.

## Open

- [2026-07-21] [AI] `content/agents-md-symlink.md` (the published article) was not in
  the initial upload, so `content/` is empty and untracked (git cannot track an empty
  dir). Drop the article file in and `git add` it. Until then the README link to it is
  a promissory note.
- [2026-07-21] [AI] `doc-drift-guard.yml` was reconstructed from the sentinel/SETUP.md
  spec because the original was not in the upload (docs mark it "written"). If the real
  file resurfaces, replace the reconstruction and diff the behavior (issue title,
  labels, threshold default).
- [2026-07-16] [HU] Sienna and Workout App have `Stage = (tbd)` and the Workout App
  fields are undefined in the Portfolio (docs/PMAWS.md §5). Define them next time
  either project is touched.

## Parked (on the board as 🅿️)

- [2026-07-16] [HU] Frameshift Intelligence OS harvest — frozen. A preserve-then-delete
  pass is owed: harvest real history (decisions, phases, parked items) into the correct
  repo via `project-os` standardize mode, check for orphaned local state, then delete
  (docs/PMAWS.md §5, §6.6).

## Resolved (kept briefly for the audit trail)

- [2026-07-21] [AI] `sentinel/SETUP.md` referenced the central repo as
  `snowfranco/project-os`; corrected to `snowfranco/ProjectOS` in §1a and §1b so the
  reusable-workflow `uses:` path is right.
