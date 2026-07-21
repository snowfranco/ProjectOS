---
name: drain-inbox
description: >
  Pull this project's queued items from the Notion Inbox into the repo, then mark
  them drained. Use at the START of a work session on a repo, or whenever the
  human says "drain the inbox", "what did I queue for this project", "pull my
  parked items", "check the inbox", or "sync from Notion". This is the Claude
  Code half of the capture loop: Claude.ai queues thoughts to the Notion Inbox;
  this skill lands them in the repo where they belong. Requires the Notion
  connector.
---

# drain-inbox

## What this is

Half of the capture loop. When you are thinking in Claude.ai (architecture,
future features, a decision) and there is no write path to the repo, you queue
it to the Notion Inbox. This skill, running in Claude Code where the repo lives,
pulls those queued rows into the right repo file and marks them handled.

The Inbox is a QUEUE, not a store. Items pass through it into the repo and then
leave (marked drained). Nothing is meant to live in the Inbox permanently.

## Where things land (routing)

Each Inbox row has a `Type`. Route by it:

- `Feature` / `Idea` / `Bug` → append to **PARKING_LOT.md**
- `Future phase` → add under **Next** in **ROADMAP.md**
- `Decision` → add an entry to the **Decisions Log** in PROJECT_OS.md, in ADR
  format (Context / Decision / Consequence), role-tagged

## Procedure

1. **Identify the project.** Determine which Portfolio row this repo maps to
   (match the repo's git remote against the Portfolio `Repo` URL). If ambiguous,
   ask.

2. **Query the Inbox.** Data source:
   `collection://f3f3e459-6a90-474e-ae31-3a5758e14f0e`. Pull rows where
   `Target project` relates to this project AND `Drained` is unchecked.

   If there are zero undrained rows, say so and stop. That is a clean result,
   not a failure.

3. **Show the human what you found** before writing. A short list: item, type,
   note. Let them veto anything that no longer belongs (the Inbox is a place
   where you notice you queued six things and shipped none — surface that if the
   count is high).

4. **Write each item to its routed destination** in the repo, in the house
   format (role tags, dates, ADR format for decisions). One line per parking-lot
   item with enough context to survive: could you act on it in three weeks
   having forgotten today?

5. **Mark each drained row** `Drained = checked` in Notion. Do not delete the
   rows; the checkbox is the audit trail.

6. **Commit** with a conventional-commit message:
   `docs: drain inbox <date> — <n> items into parking lot / roadmap / decisions`

## Guardrails

- **Never leave a row half-processed.** If you wrote it to the repo, tick
  Drained. If you did not, leave it unchecked. The two must always agree, or the
  next drain double-writes.
- **Someday items have no target.** Rows with a blank `Target project` are the
  human's true someday pile. This skill ignores them — they are not for any
  repo. Leave them alone.
- **Respect the hard rule.** A decision goes to the Decisions Log, not the
  parking lot. A deferred feature goes to the parking lot, not the decisions
  log. Route by lifecycle, not by convenience.
