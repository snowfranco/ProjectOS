# PROJECT_OS — PMAWS

**Purpose (short):** A personal operating system for managing, organizing, and
learning from many AI-built projects at once, without drowning in scaffolding,
drift, or half-finished ideas.
**Owner:** Snow · **Status:** Live (core loop operational) · **Last updated:** 2026-07-21

> Tag legend: `[HU]` human-owned (provided or confirmed by Snow) · `[AI]`
> authored from the codebase · `[INFERRED]` a default chosen by the assistant,
> not a deliberate decision. No `[INFERRED]` entries carry architectural weight
> below; any that appear are flagged inline.
>
> This is the concise operating file. The full system design, rationale, and
> content-flywheel notes live in `docs/PMAWS.md` (the authoritative long form).
> This file exists so a fresh session can rehydrate in two minutes; read
> `docs/PMAWS.md` when you need the why behind any of it.

---

## Purpose

- [HU] PMAWS (Project Management Agentic Workflow System, also "ProjectOS") is
  Snow's meta-system: the repo that manages every other project repo (docs/PMAWS.md).
- [HU] It fixes recurring portfolio failures: reinvented scaffolding, a leaky
  idea funnel, lossy handoffs, doc drift, buried content, stalled last miles, and
  the re-briefing tax paid at the start of every session (docs/PMAWS.md §1).
- [HU] It must force culls, not just organize, because building the management
  system is itself a way to avoid shipping (docs/PMAWS.md §1, §5).

## Stack

- [AI] Skills: four project-agnostic procedures as Markdown with YAML
  frontmatter, one `SKILL.md` per skill (skills/project-os, skills/session-start,
  skills/session-close, skills/drain-inbox).
- [AI] Sentinel agent: a single-file Python 3.12 script, standard library only
  (urllib, json, base64, re, datetime), no third-party dependencies
  (sentinel/sentinel.py).
- [AI] Automation: GitHub Actions workflows (.github/workflows/sentinel.yml,
  doc-drift.yml, and the reusable doc-drift-guard.yml).
- [AI] External integrations, all via raw HTTP from the Sentinel: Notion API
  (`2022-06-28`), GitHub REST API, Telegram Bot API (sentinel/sentinel.py).
- [HU] Notion is the second truth store (Portfolio, Belief Ledger, Inbox
  databases); the repo layer is GitHub (docs/PMAWS.md §3.1).

## Architecture as it actually is

- [HU] One hard rule at the center: one source of truth, split by lifecycle.
  Changes with code, it lives in the repo (GitHub). Changes with priorities, it
  lives in Notion. Nothing lives in both (docs/PMAWS.md §2).
- [HU] Exactly one write path into any repo: Claude Code. The architect
  (Claude.ai) reads GitHub but never writes it, which is what prevents drift
  between what was discussed and what was committed (docs/PMAWS.md §3.2).
- [AI] Two agents run without the human, both on GitHub Actions so they fire
  whether or not a machine is on (sentinel/SETUP.md):
  - Doc Drift Guard: weekly, per repo, compares docs vs code, opens one
    `doc-drift` issue in the repo when code outruns docs. Reusable via
    `workflow_call`; each repo adds a thin caller (.github/workflows/doc-drift.yml
    calls .github/workflows/doc-drift-guard.yml).
  - Portfolio Sentinel: daily, central. Reads each Active repo's last commit and
    `⏳` next line, writes Last Touched and Next Action back to the Notion
    Portfolio, and sends one Telegram digest (sentinel/sentinel.py,
    .github/workflows/sentinel.yml).
- [AI] Path coupling that must hold: .github/workflows/sentinel.yml runs
  `python sentinel/sentinel.py`, so the script must stay at that exact path
  (.github/workflows/sentinel.yml line 35).
- [HU] The session loop works on any account: session-start reads the four OS
  files from disk and rehydrates context; session-close captures state back into
  the repo (and Notion if connected). No connector is required for the core loop
  (docs/PMAWS.md §3.3, skills/session-start/SKILL.md).
- [HU] Stages track evidence, not build progress. A heavily-built product can sit
  at "Demand" because the code is real but demand is unproven (docs/PMAWS.md §3.4).

## Key decisions (from the code and docs)

- [HU] AGENTS.md is the canonical conventions file; CLAUDE.md is a symlink to it,
  so the same rules are never maintained twice and the setup ports to other agents
  (AGENTS.md, CLAUDE.md, skills/project-os/SKILL.md "Portability").
- [AI] The Sentinel writes back only Last Touched and Next Action, and never
  touches Tier, Stage, or Kill By Date, and never creates Portfolio rows: those
  are human judgement calls (sentinel/sentinel.py `update_row`, sentinel/SETUP.md
  "Deliberate non-goals").
- [AI] The Sentinel is stdlib-only on purpose, so the Action needs no
  `pip install` step and cannot break on a dependency (sentinel/sentinel.py imports).
- [HU] Secrets (Notion token, GH PAT, Telegram token and chat id) live in GitHub
  Actions secrets and are read from env, never committed (sentinel/sentinel.py
  reads `os.environ`, .github/workflows/sentinel.yml `env:` block).

## Known constraints

- [AI] The reusable Doc Drift Guard requires this central repo to be public, or on
  a plan that allows sharing reusable workflows across private repos; otherwise the
  caller-plus-logic must be copied into each repo (sentinel/SETUP.md §1a).
- [AI] The doc-drift.yml caller references the guard `@main`, so the guard workflow
  must exist on the default branch before any caller can succeed
  (.github/workflows/doc-drift.yml).
- [AI] Notion returns 404 if the integration is not connected to the Portfolio
  database, which looks like a bad database id but is not (sentinel/SETUP.md
  "Failure modes").
- [AI] GitHub pauses Actions cron on repos with no activity for 60 days; a silent
  digest stop is usually this (sentinel/SETUP.md "Failure modes").
- [HU] The 3-Active portfolio cap is a hard rule the system exists to enforce; the
  Sentinel only reports a breach, it does not fix it (docs/PMAWS.md §6.5,
  sentinel/sentinel.py digest tail).

## Decisions Log (newest first)

### [2026-07-21] [HU] Adopted the original doc-drift workflows; placed them in .github/workflows
Context: The real doc-drift-guard.yml and doc-drift.yml surfaced (added on main at the
repo root). The originals are richer than the reconstruction (a day_threshold input,
$GITHUB_OUTPUT plumbing, one issue edited in place), and root-level workflow files do
not run on GitHub Actions.
Decision: Adopt both originals, relocate them into .github/workflows/, delete the root
copies, and correct the caller's uses: path from snowfranco/pmaws to snowfranco/ProjectOS.
Consequence: The real guard is now the one hosted centrally. The reconstruction below is
superseded. Root files are gone so a merge back to main stays clean.

### [2026-07-21] [AI] Reconstructed doc-drift-guard.yml from the SETUP.md spec (workaround) — SUPERSEDED by the entry above
Context: The reusable Doc Drift Guard was marked "written" in the docs but was not in
the initial upload, and the new .github/workflows/doc-drift.yml caller references it.
Decision: Reconstruct a faithful reusable workflow from the behavior documented in
sentinel/SETUP.md (weekly cadence via the caller, a commit_threshold input, opening or
updating and later closing a single doc-drift issue) rather than leave the caller
pointing at a missing file.
Consequence: The structure is complete and the caller works. This is a workaround: if
the original surfaces, replace this reconstruction (tracked in PARKING_LOT.md).

### [2026-07-21] [HU] Standardize PMAWS's own repo to the house structure
Context: All PMAWS files existed locally but unorganized and unpushed. PMAWS is a
project like any other and must follow the standard it enforces on every other repo.
Decision: Move files into the house layout (.github/workflows, skills/<name>/SKILL.md,
sentinel/, docs/, content/), and bootstrap this repo's own OS files (PROJECT_OS,
ROADMAP, PARKING_LOT, AGENTS with a CLAUDE symlink) sourced from docs/PMAWS.md.
Consequence: The central repo now dogfoods its own standard. The full design stays
in docs/PMAWS.md; PROJECT_OS is the concise pointer so sessions rehydrate fast.

### [2026-07-16] [HU] AGENTS.md canonical, tool names symlinked to it
Context: Rules duplicated across agent-specific files (CLAUDE.md, GEMINI.md) drift
and double the maintenance the day a better tool ships.
Decision: Keep one canonical AGENTS.md and symlink CLAUDE.md (and any future tool
file) to it. Keep it short and hand-curated; grown-up procedures become skills.
Consequence: One file to maintain; the setup moves to a new agent in an afternoon.
Bloated auto-generated rules files are rejected on purpose (skills/project-os/SKILL.md).

### [2026-07-16] [HU] One source of truth, split by lifecycle; one write path to the repo
Context: Project truth lives in git; priority truth lives in Notion; mixing them
guarantees drift, and multiple writers into the repo guarantee the docs and the
commits disagree.
Decision: If it changes with code it lives in the repo; if it changes with
priorities it lives in Notion; nothing lives in both. Claude Code is the only writer
into the repo; Claude.ai reads but never writes.
Consequence: Drift has one cause to hunt, not many. The architect cannot silently
diverge the repo from the plan (docs/PMAWS.md §2, §3.2).

### [2026-07-16] [HU] Stages track evidence, not code
Context: The top way projects die is building something nobody wanted, and code
growth masquerades as progress.
Decision: A project's Stage advances only on validated evidence (problem, demand,
usage), never because more code was written.
Consequence: The board stays honest even against the builder's optimism; a
well-built product can correctly sit at "Demand" (docs/PMAWS.md §3.4).

### [2026-07-16] [AI] Decisions Log uses ADR format, supersede-never-delete
Context: A one-line "we chose X" is useless in six months; the record of what forced
a choice, and why it later changed, is the valuable part.
Decision: Log every non-trivial decision as Context / Decision / Consequence, newest
first, and mark superseded entries rather than deleting them.
Consequence: The reasoning survives; a future backfill will not mistake a
constraint-forced workaround for intended design (skills/project-os/SKILL.md).
