---
name: project-os
description: >
  Bootstrap or standardize the project OS files in a repo. Use when starting a
  new project, onboarding an existing/vibe-coded repo that has no docs, or
  bringing an inconsistent repo up to the house standard. Triggers: "set up
  project-os", "initialize the OS files", "bootstrap docs", "backfill
  documentation", "standardize this repo", "add PROJECT_OS", or any time a repo
  is missing PROJECT_OS.md / ROADMAP.md / PARKING_LOT.md / CLAUDE.md or has them
  in the wrong format. Produces the four files in the house format, tagged by
  evidence, with a GAP list for the human to fill.
---

# project-os

## What this is

The bootstrapper for a project's durable memory. It creates (or repairs) the
four files that let any fresh session — a new chat, a different model,
future-you — rehydrate context without a re-briefing. This is the static half of
context engineering: durable, on-demand project knowledge that lives in the repo
and gets read at session start.

Run it once per repo. After that, `session-close` keeps the files current and
you rarely touch this skill again.

## The four files, and the hard rule

Every repo standardizes on exactly four files in the repo root:

- **PROJECT_OS.md** — what this is, stack, architecture as it actually is, key
  decisions, known constraints, and the Decisions Log. The calm, authoritative
  file. Changes rarely.
- **ROADMAP.md** — a Status Board plus phase/feature detail. The current-state
  file. Uses the house status vocabulary (see "ROADMAP status board" below).
- **PARKING_LOT.md** — deferred features, bugs, ideas. The churning worklist.
- **CLAUDE.md** — conventions the agent must follow. Loaded every session, so
  keep it lean.

Hard rule: durable truth (decisions, architecture, constraints) lives in
PROJECT_OS. Churning worklist lives in PARKING_LOT. Never mix them — different
lifecycles, different writers.

## House format (non-negotiable)

Match this exactly; it is the established Snow style.

- **Role tags on every substantive line**: `[HU]` human-owned (provided or
  confirmed by the human), `[AI]` authored by the assistant from the codebase,
  `[INFERRED]` a default the assistant chose rather than a deliberate decision.
- **Inline file citations** in parentheses after claims drawn from code, e.g.
  `(package.json, next.config.mjs)`. A claim about the code that cites no file is
  suspect.
- **No em dashes.** Use commas, colons, or parentheses.
- **A header note** at the top of PROJECT_OS stating the tag legend and flagging
  any `[INFERRED]` entries.
- **Section order in PROJECT_OS**: Purpose → Stack → Architecture as it actually
  is → Key decisions (from the code) → Known constraints → Decisions Log.

## ROADMAP status board (house standard)

ROADMAP.md has two parts: a Status Board (at-a-glance table) and Phase Detail
(one subsection per phase for a future agent with no context).

The Status Board is the source of truth; the detail is the explanation. Use this
exact status vocabulary — it is the house standard:

`✅ shipped` · `🔄 in progress` · `⏳ next` · `💡 planned` · `🅿️ parked`

Status Board table shape:

```markdown
## Status Board

| Phase | What | Status | Shipped |
|-------|------|--------|---------|
| 1 | Core pipeline | ✅ shipped | 2026-04 |
| 2 | Scoring module | 🔄 in progress | — |
| 3 | Hypothesis registry | 💡 planned | — |
```

Rules for the board:
- Shipped phases are never deleted — they are architectural history.
- Parked items stay on the board as `🅿️ parked` with "(see PARKING_LOT.md)" in
  their detail; the board flags that they exist, the detail lives in the parking
  lot.
- `⏳ next` marks the ONE thing that is actually next. Not three things. One.
- Update a "Last updated: YYYY-MM-DD" line at the top on every change.

Each Phase Detail subsection carries: what was built, key files touched,
decisions made (brief rationale, or a pointer to the Decisions Log for the full
ADR), open items (pointer to PARKING_LOT.md), and what it unlocks.

## Procedure

### A. If the repo has NO OS files (bootstrap / backfill)

1. **Investigate from evidence, never assumption.** Read: README, manifest
   (package.json / pyproject / Cargo.toml), config, directory structure, entry
   points. Run `git log --oneline -50` and `git log -1 --format=%cI`. Grep for
   TODO / FIXME / HACK. Infer the stack from dependencies.

2. **Draft the four files** in the house format above.
   - PROJECT_OS: fill every section. "Architecture as it actually is" describes
     the real current state, not the intended one. "Key decisions (from the
     code)" are choices you can see in the code. Known constraints are the
     non-obvious things that would bite a fresh contributor.
   - ROADMAP: reverse-engineer shipped work (from git + working code) as Done.
     Half-built things are In progress. Leave Next empty for the human.
   - PARKING_LOT: every TODO/FIXME found, plus anything the code implies was
     deferred (stubs, mocks, hardcoded temporaries).
   - CLAUDE.md: conventions you can infer (naming, structure, test approach, run
     commands).

3. **Tag every claim** `[KNOWN]` / `[INFERRED]` / `[GAP]` during drafting.
   A `[GAP]` is more useful than a confident fiction. Never invent a purpose, a
   roadmap, or a decision the human never made.

4. **Stop and present the GAP list** as questions before finalizing. Get the
   human's answers, then strip the working tags (keep the permanent
   `[HU]`/`[AI]`/`[INFERRED]` role tags) and write the files.

### B. If the repo HAS OS files but they are inconsistent (standardize)

1. Read the existing files. Preserve everything still true — you are repairing,
   not regenerating.
2. Reformat to the house style: add missing role tags, add file citations, fix
   section order, remove em dashes.
3. Flag anything that looks stale (docs describing code that changed) as a
   question, do not silently rewrite it.
4. Migrate the Decisions Log to ADR format (see below) going forward. Leave old
   one-line entries in place, marked, rather than rewriting history.

## The Decisions Log — ADR format (standard going forward)

New decisions use the ADR (Architecture Decision Record) structure. It is a
long-established standard and it captures the one thing a one-liner loses: what
forced the choice.

```
## Decisions Log (newest first)

### [YYYY-MM-DD] [HU] <short decision title>
Context: <what forced the choice — the problem or constraint>
Decision: <what was chosen>
Consequence: <what we now live with, good and bad>

### [YYYY-MM-DD] [AI] <earlier decision title> — SUPERSEDED by the entry above
Context: ...
Decision: ...
Consequence: ...
```

Two rules do most of the work:

1. **Record what forced the choice.** Six months from now, "we chose X" is
   useless; "we chose X because Y forced it" tells you whether the decision
   still holds.
2. **Supersede, never delete.** Old decisions stay, marked `SUPERSEDED`, because
   the record of why you changed your mind is itself worth keeping.

A workaround forced by a constraint IS a decision — log it, and say it was a
workaround (tag `[INFERRED]` if the assistant chose it), so a future backfill
does not mistake the tape-and-glue for intended design.

## Portability: AGENTS.md as the canonical file

To keep the setup portable across agents (Codex, Gemini CLI, whatever ships
next), make AGENTS.md the canonical rules file and symlink the tool-specific
names to it, so the same rules are never maintained twice:

```
# in the repo root
mv CLAUDE.md AGENTS.md          # if starting from CLAUDE.md
ln -s AGENTS.md CLAUDE.md
# ln -s AGENTS.md GEMINI.md     # add others as needed
```

Keep AGENTS.md short and hand-curated. Bloated, auto-generated rules files hurt
more than they help — the important rules get buried and the agent learns to
half-ignore them. If a section grows from a fact ("we use Vitest") into a
procedure ("to add a test, do these five steps"), move it out into its own skill
and reclaim the context budget.

## Guardrails

- **Evidence over assumption, always.** Every architectural claim cites a file
  or is tagged `[INFERRED]`.
- **Never invent purpose or decisions.** Ask; a GAP beats a fiction.
- **Keep CLAUDE.md / AGENTS.md lean.** It loads every session. Procedures become
  skills, not rules-file bloat.
- **Don't rewrite history.** When standardizing, preserve and supersede; don't
  silently overwrite old decisions.
