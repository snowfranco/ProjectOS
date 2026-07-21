# AGENTS.md — PMAWS conventions

Canonical rules file. `CLAUDE.md` is a symlink to this. Keep it short and
hand-curated: it loads every session, so a rule buried in bloat is a rule the
agent learns to half-ignore. When a rule grows into a procedure, move it into a
skill under `skills/` and reclaim the budget.

## The hard rule

One source of truth, split by lifecycle. Changes with code, it lives in the repo.
Changes with priorities, it lives in Notion. Nothing lives in both. When unsure,
ask whether a terminal agent needs to read it; if yes, it goes in the repo.

One write path into the repo: Claude Code. The architect (Claude.ai) reads the
repo, never writes it.

## Writing style (house format)

- Role-tag substantive lines: `[HU]` human-owned, `[AI]` authored from the code,
  `[INFERRED]` a default the assistant chose, not a decision.
- Cite files inline after any claim about the code: `(sentinel/sentinel.py)`.
  A code claim with no citation is suspect.
- No em dashes. Use commas, colons, or parentheses.
- Decisions use ADR format (Context / Decision / Consequence), newest first,
  supersede-never-delete. A constraint-forced workaround is a decision; log it and
  say it was a workaround.

## Repo layout

- `PROJECT_OS.md` — concise operating file; points to `docs/PMAWS.md` for detail.
- `ROADMAP.md` — Status Board (`✅ 🔄 ⏳ 💡 🅿️`) + phase detail. One `⏳` only.
- `PARKING_LOT.md` — deferred items, one dated line each.
- `AGENTS.md` (+ `CLAUDE.md` symlink) — this file.
- `docs/PMAWS.md` — the authoritative long-form system design.
- `skills/<name>/SKILL.md` — one folder per skill.
- `sentinel/` — the Portfolio Sentinel (`sentinel.py`, `SETUP.md`).
- `.github/workflows/` — `sentinel.yml`, `doc-drift.yml`, `doc-drift-guard.yml`.

## Discipline

- Stages track evidence, not code. Never advance a Stage because code grew.
- Run `session-start` before work, `session-close` after every session.
- Secrets live in GitHub Actions secrets and are read from env, never committed.
- Path coupling: `.github/workflows/sentinel.yml` runs `python sentinel/sentinel.py`.
  Do not move the script without updating the workflow.
- The Sentinel is stdlib-only Python. Keep it dependency-free so the Action needs
  no install step.
