# ROADMAP — PMAWS

**Last updated:** 2026-07-21
**Status vocabulary:** ✅ shipped · 🔄 in progress · ⏳ next · 💡 planned · 🅿️ parked

> This board is the system-level roadmap for PMAWS, mirrored from `docs/PMAWS.md`
> §5 and kept current here. The Status Board is the source of truth; the Phase
> Detail below explains each line for a future agent with no context. Shipped
> phases are never deleted, they are architectural history.

## Status Board

| Phase | What | Status | Shipped / Note |
|-------|------|--------|----------------|
| 1 | Notion truth layer (Portfolio, Beliefs, Inbox) | ✅ shipped | built + populated |
| 2 | Portfolio cull (3 Active / 3 Frozen cap) | ✅ shipped | Gabay, Sienna, Workout App active |
| 3 | Repo OS-file standard (4 files, house format) | ✅ shipped | in all active repos |
| 3b | This repo standardized to its own standard | ✅ shipped | 2026-07-21 (this session) |
| 4 | Core skills (project-os, session-start, session-close, drain-inbox) | ✅ shipped | connector-aware |
| 5 | Doc Drift Guard | 🔄 in progress | reusable + caller written; deploy pending |
| 6 | Gabay concierge $0 test | ⏳ next | THE actual next action (a demand test, not more infra) |
| 7 | Discovery skill + LENSES.md | 💡 planned | the gate rubric |
| 8 | Sub-agent bench (redteam, landscape-scout) | 💡 planned | build after a real loop run |
| 9 | Portfolio Sentinel (daily digest + repo→Notion sync) | 🔄 in progress | code written + in-repo; deploy (secrets, dry-run) pending |
| 10 | Content Miner → Sienna | 💡 planned | feeds the flywheel |
| — | Frameshift Intelligence OS harvest | 🅿️ parked | frozen; preserve-then-delete pass (see PARKING_LOT.md) |

**Standing reminder:** infrastructure is the comfortable place to hide. The
system's own next action (Phase 6) is a demand test, not more building.

## Phase Detail

### Phase 1 — Notion truth layer ✅
[HU] Portfolio, Belief Ledger, and Inbox databases built and populated in Notion.
Notion holds priority-lifecycle truth (docs/PMAWS.md §3.1). Unlocks the two-tier
source of truth and every Notion-aware skill.

### Phase 2 — Portfolio cull ✅
[HU] The 3-Active cap enforced; current Active set is Gabay, Sienna, Workout App
(docs/PMAWS.md §5). Unlocks focus: a fourth Active forces something out.

### Phase 3 — Repo OS-file standard ✅
[HU] The four-file house standard (PROJECT_OS, ROADMAP, PARKING_LOT, CLAUDE→AGENTS)
defined and rolled out to active repos (skills/project-os/SKILL.md). Unlocks
connector-free rehydration and drift detection.

### Phase 3b — PMAWS standardized to its own standard ✅
[HU] 2026-07-21. All PMAWS files, previously unorganized and unpushed, moved into
the house layout, and this repo's own OS files bootstrapped from docs/PMAWS.md.
Key paths: .github/workflows/{sentinel,doc-drift,doc-drift-guard}.yml,
skills/<name>/SKILL.md, sentinel/{sentinel.py,SETUP.md}, docs/PMAWS.md. Unlocks:
the central repo now dogfoods the standard it enforces, and the Sentinel can read
this repo's ⏳ line like any other.

### Phase 4 — Core skills ✅
[HU] project-os, session-start, session-close, drain-inbox all built and
connector-aware (skills/). session-start and the session loop run with no
connector; drain-inbox no-ops without Notion. Unlocks the daily loop on any account.

### Phase 5 — Doc Drift Guard 🔄
[AI] The reusable workflow (.github/workflows/doc-drift-guard.yml) and this repo's
caller (.github/workflows/doc-drift.yml) are the deployment mechanism; deploy is
rolling out per repo (sentinel/SETUP.md §1). Open items: confirm the reusable
guard is on the default branch, then roll callers out one repo at a time. Full
detail in sentinel/SETUP.md.

### Phase 6 — Gabay concierge $0 test ⏳
[HU] The single next action for the whole system: run a $0 / 48-hour concierge
demand test for Gabay (the OFW legal-info product) whose demand is unvalidated
despite heavy build (docs/PMAWS.md §5). This is deliberately not a PMAWS-repo
build task; the point is to stop building infrastructure and test real demand.

### Phase 7 — Discovery skill + LENSES.md 💡
[HU] The gate rubric that decides whether to build at all, drawn from the discovery
canon as a stage function (docs/PMAWS.md §4, §3.4). Planned.

### Phase 8 — Sub-agent bench 💡
[HU] A redteam / landscape-scout sub-agent bench under ~/.claude/agents, to be
built after a real loop run proves what is actually needed (docs/PMAWS.md §3.5).

### Phase 9 — Portfolio Sentinel 🔄
[AI] Code is written and now lives in this repo: sentinel/sentinel.py (stdlib-only
Python 3.12) and .github/workflows/sentinel.yml (daily cron). It reads each Active
repo's last commit and ⏳ line, writes Last Touched and Next Action back to Notion,
and sends one Telegram digest. Open items: add the five Actions secrets, run a
dry-run from the Actions tab, then enable the schedule (sentinel/SETUP.md §2).
This is what removes the manual Notion sync on the local-only account.

### Phase 10 — Content Miner → Sienna 💡
[HU] A weekly job that mines committed build artifacts for content angles and feeds
Sienna, the content flywheel (docs/PMAWS.md §3.2, §4). Planned.

### Parked — Frameshift Intelligence OS harvest 🅿️
[HU] Frozen. A preserve-then-delete harvest pass is owed before deletion
(docs/PMAWS.md §5, §6.6). See PARKING_LOT.md.
