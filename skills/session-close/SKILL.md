---
name: session-close
description: >
  Run at the END of any work session on a project repo, before you stop. This is
  the forcing function that keeps documentation from rotting and the Notion
  portfolio honest. Triggers: "close out", "wrap up", "session close", "end of
  session", "let's stop here", "done for today", or any time the user is finishing
  work on a repo and wants state captured before context is lost. Updates the repo
  OS files (ROADMAP, PARKING_LOT, PROJECT_OS decisions log), writes the exact next
  step, emits a handoff block, and updates the project's Notion Portfolio row.
---

# session-close

## What this is

The single most important skill in the system. Everything else can rot; this is
what prevents it. At the end of a work session it captures state into durable
places (the repo, Notion) so that the next session — or a different model, or
future-you three weeks from now — can pick up cold without you re-explaining
anything.

Run it EVERY session. Not just the big ones. The habit is the value.

## The hard rule it enforces

Truth lives in exactly one place, split by lifecycle:

- **Changes with code** → the repo (ROADMAP.md, PARKING_LOT.md, PROJECT_OS.md).
- **Changes with priorities** → Notion (Portfolio row).

Never write the same fact to both. This skill moves each piece of state to its
correct home and nowhere else.

## Procedure

Work through these in order. Do not skip a step because "nothing changed" —
say so explicitly instead. An honest "no decisions this session" is a valid
output; a silent omission is not.

### 1. Read current state first

Before writing anything, read the repo's `ROADMAP.md`, `PARKING_LOT.md`, and the
Decisions Log section of `PROJECT_OS.md`. You are editing reality, not
regenerating it. Preserve everything that is still true.

### 2. Update the ROADMAP

Move anything shipped this session from `In progress` / `Next` to `Done`, dated.
Move anything newly started into `In progress`. Do not invent future roadmap
items — that is the user's call, not yours. If the user named a next thing, put
it under `Next`; otherwise leave `Next` as it was.

### 3. Drain deferrals into the PARKING_LOT

Anything raised this session and consciously deferred — a bug noticed but not
fixed, a "we'll do this properly later", a stubbed function, a hardcoded value
that is temporary — gets one line in `PARKING_LOT.md` with enough context to
survive the trip. Format:

```
- [YYYY-MM-DD] <what> — <why deferred / what the real version looks like>
```

The test for a parking-lot entry: could you act on it in three weeks having
forgotten everything about today? If not, add context until you could.

### 4. Log decisions into PROJECT_OS

Any genuine decision made this session — a choice with alternatives that were
rejected — gets one line at the TOP of the Decisions Log section in
`PROJECT_OS.md` (newest first). Tag it `[HU]` if the human decided, `[AI]` if you
proposed and they accepted. Format:

```
- [YYYY-MM-DD] [HU] Chose X over Y because Z.
```

A workaround forced by a constraint IS a decision — log it, and say it was a
workaround, so a future backfill doesn't mistake it for an intended design.

Do NOT log non-decisions. "Wrote some code" is not a decision. "Chose Postgres
over a dedicated vector DB to avoid an extra moving part" is.

### 5. Write the exact next step

In `ROADMAP.md` under `Next`, or in a `## Next session` block at the top if the
repo uses one, write the single first action for next time. It must be concrete
enough to start on without thinking: a verb, a file, a goal. "Fix the provider
routing" is too vague. "In `router.py`, make `select_provider()` fall back to
the secondary when the primary returns 429; test with the mock in
`test_router.py`" is right.

### 6. Emit a handoff block

Print this to the conversation (do not write it to a file — it is for the user
to copy if they start a fresh chat):

```
=== HANDOFF: <project> — <date> ===
Shipped this session: <1-3 bullets>
Current state: <where things stand, honestly>
Next action: <the exact first step from step 5>
Open risks / watch-outs: <anything that will bite next time>
Blocked on: <if anything, else "nothing">
===
```

### 7. Emit content seeds (only if the project is a content-flywheel target)

If this repo feeds Sienna (the content flywheel), capture candidate angles from
this session. There are TWO kinds, and a good session often produces both.
The specific, concrete detail is always the point — vague seeds are worthless.

**Type A — Build story.** Something that happened: a decision, a debugging war
story, a constraint discovered, a surprising number. Tied to this project.

```
=== CONTENT SEED (build story) ===
Angle: <the specific story, one line>
The detail that makes it real: <the exact bug, the surprising number, the
  wrong assumption that cost three days>
===
```

**Type B — Concept / lesson.** A topic you learned or applied this session that
generalizes beyond this project: RAG vs fine-tuning, golden eval design,
human-in-the-loop patterns, provider abstraction, prompt versioning, chunking
strategy, safety-layer design, and so on. This vein is evergreen and
demonstrates judgment rather than activity — often the higher-value seed.

```
=== CONTENT SEED (concept) ===
Topic: <the concept, e.g. "why we chose RAG over fine-tuning for legal text">
The grounded take: <what YOU actually concluded from doing it, not a textbook
  summary — the opinion you earned by shipping>
Where it showed up: <the concrete moment in this project that taught it>
===
```

Only surface a Type B seed if the session genuinely touched the concept in a way
that earned an opinion. Do not manufacture think-pieces from routine work, and
never emit a concept seed that is just a definition — the grounded, project-born
take is the entire value.

If this repo is not a content target, skip this step entirely.

### 8. Update the Notion Portfolio row (if the connector is available)

The repo is the source of truth for project-internal state; Notion is a mirror.
This step keeps the mirror current.

**If the Notion connector IS available**, update this project's Portfolio row:

- `Next Action` — the exact next step from step 5 (one line).
- `Stage` — move it only if the EVIDENCE moved, not if code moved. Building more
  of an unvalidated product does not advance the stage. Be strict about this.
- `Riskiest belief` — if this session produced evidence for or against it, say so
  and update the linked Belief's `Status` / `Confidence` / `Evidence` fields.

Do NOT touch `Last Touched` — the Sentinel owns that field. Do NOT touch `Tier`
or `Kill By Date` unless the user explicitly asked to.

**If the Notion connector is NOT available** (e.g. a local-only Claude Code
account), skip the write and instead emit the delta in the handoff block, under a
`PORTFOLIO UPDATE` heading, so it can be applied later — by hand from any device,
or automatically by the Sentinel once it runs:

```
=== PORTFOLIO UPDATE (apply in Notion) ===
Project: <name>
Next Action: <the exact next step>
Stage: <new stage, or "unchanged">
Belief update: <belief + new status/confidence, or "none">
===
```

Never fail the session because Notion is unreachable. The repo write is what
matters; the mirror can catch up.

### 9. Commit (and report push status honestly)

Stage and commit the doc changes with a conventional-commit message:

```
docs: session close <date> — <one-line summary>
```

Then push if this account can reach the remote. If it cannot (a local-only
account), do NOT pretend. Commit locally and state plainly in the handoff:
"Committed locally on <branch>, NOT pushed — push from an account with remote
access." Never leave the human guessing whether their work reached GitHub.

This keeps the Doc Drift Guard quiet once the docs reach the remote, because the
docs just moved.

## Guardrails

- **Never invent state.** If you do not know whether something shipped, ask or
  mark it uncertain. A confident fiction in the handoff is worse than a gap.
- **Never advance a Stage because code grew.** Evidence advances stages. This is
  the discipline that keeps the board honest — protect it even against the
  user's optimism.
- **Never write the same fact to both the repo and Notion.** Next Action is the
  one deliberate exception: it lives in ROADMAP (for the terminal) and in the
  Portfolio row (for the phone), because both readers need it. Everything else,
  one home only.
- **Keep it fast.** This runs every session. If it becomes a chore, it stops
  running, and then it is worthless. Terse is correct.
