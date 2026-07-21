---
name: session-start
description: >
  Run at the START of any work session on a project repo, before doing work. Reads
  the repo's OS files from local disk and rehydrates full project context so you
  can begin cold without a re-briefing. Triggers: "session start", "let's begin",
  "pick up where we left off", "where were we", "load the project", "what's next
  here", or opening a repo to work after time away. Connector-free: works on any
  Claude Code account, including local-only ones with no GitHub or Notion access.
---

# session-start

## What this is

The read half of the session loop, and the cure for the re-briefing tax. Instead
of you re-explaining the project, this reads the durable files already sitting in
the repo and reconstructs context from them. It is the static half of context
engineering in action: rehydrate from disk, not from the human's memory.

Runs entirely on local files and git. No connector required. This is what lets a
local-only account (no GitHub, no Notion) still use the full workflow.

## Procedure

### 1. Read the four OS files, in this order

From the repo root:

1. `PROJECT_OS.md` — what this is, stack, architecture, constraints, and the
   Decisions Log. This is the foundation; read it first.
2. `ROADMAP.md` — the Status Board and, critically, the `⏳ next` item and the
   `Next` section. This is where you are.
3. `PARKING_LOT.md` — what is deferred, so you do not re-solve or re-raise it.
4. `CLAUDE.md` (or `AGENTS.md`) — the conventions you must follow this session.

If any file is missing, say so and suggest running `project-os` to create it.
Do not proceed as if the missing context does not exist.

### 2. Check git for what changed since the docs last moved

Run `git log --oneline -15` and `git log -1 --format=%cI -- PROJECT_OS.md
ROADMAP.md`. If code commits landed after the docs last moved, the docs may be
stale. Flag it: "N commits since the docs last updated — the roadmap may not
reflect the latest code." This is the same signal the Doc Drift Guard uses,
surfaced at the moment it is most useful.

### 3. Drain the inbox — only if Notion is available

If the Notion connector is present, run `drain-inbox` now to pull anything queued
for this project before you start. If it is not available (local-only account),
skip silently. Do not treat its absence as an error.

### 4. Orient the human

Give a short, honest briefing. Not a wall of text — the point is a fast start:

```
=== SESSION START: <project> ===
Where we are: <1-2 lines on current state, from ROADMAP + last commits>
Your next action: <the exact ⏳ next item from ROADMAP>
Watch out for: <any high-priority parked item or known constraint that's relevant>
Doc freshness: <"docs current" or "N commits since docs — may be stale">
===
```

Then stop and let the human confirm or redirect. Do not start working until they
point you at the task. The `⏳ next` item is a strong suggestion, not a command —
they may have a different priority today.

## Guardrails

- **Read before you act.** Never start editing code before reading the OS files.
  The whole point is to act with context, not to guess and re-derive it.
- **Surface staleness, do not hide it.** If the docs and the code disagree, the
  human needs to know before they trust the roadmap. Say it plainly.
- **Do not re-raise parked items as if they were new.** If something is in
  PARKING_LOT, it was a conscious deferral. Respect it unless the human reopens it.
- **Connector-free is the default.** Everything essential here runs on local
  files. Notion is a bonus, never a requirement.
