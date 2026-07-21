# Deploying the automation layer

Two agents, both running on GitHub Actions so they fire whether or not either of
your machines is on.

| Agent | Runs | Watches | Writes to |
|-------|------|---------|-----------|
| Doc Drift Guard | weekly, per repo | docs vs code in that repo | a GitHub issue in that repo |
| Portfolio Sentinel | daily, central | every Active repo | the Notion Portfolio + Telegram |

Direction of truth for both: the repo is authoritative, everything else mirrors
it. Neither agent ever writes to a repo's files.

---

## 1. Doc Drift Guard

### 1a. Host the reusable workflow (once)

In your central repo (`snowfranco/ProjectOS`), commit the reusable workflow to
`.github/workflows/doc-drift-guard.yml`.

The central repo must be **public**, or on a plan that allows sharing reusable
workflows across private repos. If it is private and sharing is not available,
copy the caller-plus-logic into each repo instead of using `workflow_call`.

### 1b. Add the caller to each repo

In every Active repo, add `.github/workflows/doc-drift.yml`:

```yaml
name: Doc drift
on:
  schedule:
    - cron: "0 13 * * 1"   # Mondays 09:00 Toronto
  workflow_dispatch:

jobs:
  guard:
    uses: snowfranco/ProjectOS/.github/workflows/doc-drift-guard.yml@main
    permissions:
      contents: read
      issues: write
```

Override thresholds per repo where the cadence differs:

```yaml
    with:
      commit_threshold: 10
```

### 1c. Verify

Run it manually from the Actions tab (`workflow_dispatch`). On a repo whose docs
are current it should do nothing; on one that is behind it opens a single
`doc-drift` labelled issue. Re-running after you fix the docs closes it.

Roll it out to one repo first, watch it fire once, then add the rest.

---

## 2. Portfolio Sentinel

### 2a. Create a Notion integration

1. https://www.notion.so/my-integrations -> **New integration**, internal, name
   it "PMAWS Sentinel". Copy the token (`ntn_...`).
2. Open the **Portfolio** database in Notion -> `...` menu -> **Connections** ->
   add "PMAWS Sentinel". Without this step the API returns 404 and it looks like
   a bad database id.
3. Get the database id from the URL. In
   `notion.so/<workspace>/<32-char-id>?v=<view-id>` the id is the 32-char string
   **before** the `?`, not the view id.

### 2b. Create a GitHub PAT

The default `GITHUB_TOKEN` only reaches the repo the workflow runs in, so the
Sentinel needs a PAT to read your other repos.

Settings -> Developer settings -> Personal access tokens -> fine-grained. Grant
**Contents: read-only** on all your project repos. Copy the token.

### 2c. Add secrets

In the central repo, Settings -> Secrets and variables -> Actions:

| Secret | Value |
|--------|-------|
| `NOTION_TOKEN` | the integration token |
| `NOTION_DB_ID` | the 32-char Portfolio database id |
| `GH_PAT` | the fine-grained PAT |
| `TELEGRAM_TOKEN` | from @BotFather |
| `TELEGRAM_CHAT_ID` | message the bot, then read `chat.id` from `https://api.telegram.org/bot<TOKEN>/getUpdates` |

### 2d. Commit and dry-run

Commit `sentinel/sentinel.py` and `.github/workflows/sentinel.yml`. Then run it
from the Actions tab with **dry_run = true**. It prints what it would write and
sends nothing. Check the log for:

- every Active project found
- a sensible last-commit date per repo
- a `⏳ next` item pulled from each ROADMAP

Then run it for real.

### 2e. What it does each morning

For every project not Frozen or Dead:

1. Reads the repo's last commit date -> writes **Last Touched**.
2. Reads the `⏳` line from `ROADMAP.md` -> writes **Next Action**.
3. Checks whether code commits outnumber doc commits -> flags drift.
4. Checks kill-by dates and stall thresholds.
5. Sends one Telegram digest.

This is what removes the manual Notion sync on the local-only account. CC2
commits and you push; the Sentinel does the rest.

---

## Failure modes worth knowing

**Notion 404 on the database.** Almost always the integration is not connected
to the database (step 2a.2), not a wrong id.

**Next Action comes back empty.** The ROADMAP has no `⏳` line, or it is on a
row the regex cannot parse. The status board convention is one `⏳` marking the
single next thing; if a repo has none, that is a real finding, not a bug.

**Everything reports "no commits".** The PAT lacks access to that repo. Check the
fine-grained token's repository list.

**GitHub disables the schedule.** Actions cron is paused on repos with no
activity for 60 days. The central repo gets commits often enough that this is
unlikely, but if the digest silently stops, check the Actions tab first.

**Cron drift.** Scheduled workflows can start several minutes late under load.
Irrelevant for a daily digest; do not build anything time-critical on it.

---

## Deliberate non-goals

- The Sentinel does **not** write to repos. One write path (Claude Code) stays
  the rule.
- It does **not** touch `Tier`, `Stage`, or `Kill By Date`. Those are your
  judgement calls; the agent only reports on them.
- It does **not** create Portfolio rows. New projects are added deliberately,
  which is where the 3-Active cap gets enforced.
