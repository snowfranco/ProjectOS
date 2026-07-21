# PMAWS — Project Management Agentic Workflow System

A personal operating system for managing, organizing, and learning from many
AI-built projects at once, without drowning in scaffolding, drift, or
half-finished ideas. This repo (also called **ProjectOS**) is the central
control repo: it holds the reusable skills, the two automation agents, and the
house standard that every other project repo follows.

**One hard rule:** one source of truth, split by lifecycle. If it changes when
code changes it lives in the repo; if it changes when priorities change it lives
in Notion; nothing lives in both. There is exactly one write path into a repo
(Claude Code), which is what keeps the docs and the commits from disagreeing.

For the full system design, architecture diagrams, discovery funnel, and roadmap,
read **[docs/PMAWS.md](docs/PMAWS.md)**.

## What's in here

```
.github/workflows/   sentinel.yml · doc-drift.yml · doc-drift-guard.yml
skills/              project-os · session-start · session-close · drain-inbox
sentinel/            sentinel.py · SETUP.md
docs/                PMAWS.md   (the authoritative long-form design)
content/             published articles
PROJECT_OS.md        concise operating file (points at docs/PMAWS.md)
ROADMAP.md           Status Board + phase detail
PARKING_LOT.md       deferred items
AGENTS.md            conventions (CLAUDE.md is a symlink to it)
```

## The four skills

Project-agnostic procedures, one folder per skill under `skills/`:

| Skill | When it runs | What it does |
|-------|--------------|--------------|
| `project-os` | once per repo | Bootstraps or standardizes the four OS files in the house format. |
| `session-start` | start of a session | Reads the OS files from disk and rehydrates context. Connector-free. |
| `session-close` | end of every session | Captures state back into the repo (and Notion if connected). The forcing function. |
| `drain-inbox` | start of a session | Pulls this project's queued items from the Notion Inbox into the repo. Needs Notion. |

### Installing the skills

Skills load from `~/.claude/skills/`. Symlink each one so edits in this repo stay
live (or `cp -r` if you prefer a frozen copy):

```bash
mkdir -p ~/.claude/skills
for s in project-os session-start session-close drain-inbox; do
  ln -s "$(pwd)/skills/$s" ~/.claude/skills/$s
done
```

`session-start` and `session-close` work on any account, including a local-only
Claude Code with no GitHub or Notion connector. `drain-inbox` no-ops without Notion.

## The two agents

Both run on GitHub Actions so they fire whether or not a machine is on. Neither
ever writes to a repo's files; the repo is authoritative and everything else
mirrors it. Full deploy steps, secrets, and failure modes are in
**[sentinel/SETUP.md](sentinel/SETUP.md)**.

### 1. Doc Drift Guard

Weekly, per repo. Compares docs against code and opens a single `doc-drift` issue
in the repo when code outruns the docs. The logic is a reusable workflow
(`.github/workflows/doc-drift-guard.yml`); each repo adds a thin caller
(`.github/workflows/doc-drift.yml`) that points at this repo `@main`. Deploy by
rolling the caller out one repo at a time (SETUP.md §1).

### 2. Portfolio Sentinel

Daily, central. `sentinel/sentinel.py` reads each Active repo's last commit and
`⏳` next line, writes **Last Touched** and **Next Action** back to the Notion
Portfolio, and sends one Telegram digest. Stdlib-only Python 3.12, no
dependencies. Deploy: add the five Actions secrets (`NOTION_TOKEN`, `NOTION_DB_ID`,
`GH_PAT`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`), run a dry-run from the Actions
tab, then enable the daily schedule (SETUP.md §2).

## The daily loop

```
git pull
session-start      → reads the OS files, flags doc drift, drains inbox (if Notion)
  ... work ...
session-close      → updates docs, logs decisions, writes the exact next step, commits
git push
```

## Conventions

See **[AGENTS.md](AGENTS.md)** (canonical; `CLAUDE.md` symlinks to it). Role tags
`[HU]`/`[AI]`/`[INFERRED]`, inline file citations, no em dashes, ADR-format
decisions. Secrets belong in GitHub Actions secrets, never in the repo.
