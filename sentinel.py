#!/usr/bin/env python3
"""
Portfolio Sentinel.

Reads the Notion Portfolio, checks each project's GitHub repo, writes the
repo-derived truth back to Notion, and sends a digest to Telegram.

Direction of truth: repo -> Notion. The repo is authoritative for project
state; Notion is the mirror. The Sentinel never writes to a repo.

Env vars required:
  NOTION_TOKEN        Notion internal integration token
  NOTION_DB_ID        Portfolio database id
  GH_PAT              GitHub PAT with 'repo' scope (needed for private repos)
  TELEGRAM_TOKEN      bot token
  TELEGRAM_CHAT_ID    chat to post the digest to

Optional:
  STALL_DAYS          days before an Active project is flagged (default 14)
  DRY_RUN             set to "1" to print without writing or sending
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DB_ID = os.environ["NOTION_DB_ID"]
GH_PAT = os.environ.get("GH_PAT", "")
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TG_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
STALL_DAYS = int(os.environ.get("STALL_DAYS", "14"))
DRY_RUN = os.environ.get("DRY_RUN") == "1"

NOTION_VERSION = "2022-06-28"
TODAY = datetime.now(timezone.utc).date()


# ----------------------------------------------------------------- helpers

def request(url, method="GET", headers=None, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        raise RuntimeError(f"{method} {url} -> {e.code}: {body}") from None


def notion(path, method="GET", payload=None):
    return request(
        f"https://api.notion.com/v1{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
        },
        payload=payload,
    )


def github(path):
    headers = {"Accept": "application/vnd.github+json"}
    if GH_PAT:
        headers["Authorization"] = f"Bearer {GH_PAT}"
    return request(f"https://api.github.com{path}", headers=headers)


def plain(prop):
    """Flatten a Notion property to a plain python value."""
    if not prop:
        return None
    t = prop.get("type")
    if t == "title":
        return "".join(x["plain_text"] for x in prop["title"]) or None
    if t == "rich_text":
        return "".join(x["plain_text"] for x in prop["rich_text"]) or None
    if t == "select":
        return prop["select"]["name"] if prop["select"] else None
    if t == "url":
        return prop["url"]
    if t == "date":
        return prop["date"]["start"] if prop["date"] else None
    return None


# ------------------------------------------------------------ notion reads

def fetch_portfolio():
    rows, cursor = [], None
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        res = notion(f"/databases/{NOTION_DB_ID}/query", "POST", payload)
        rows.extend(res["results"])
        if not res.get("has_more"):
            return rows
        cursor = res["next_cursor"]


# ------------------------------------------------------------ github reads

REPO_RE = re.compile(r"github\.com[:/]+([^/]+)/([^/.\s]+)")


def parse_repo(url):
    m = REPO_RE.search(url or "")
    return (m.group(1), m.group(2)) if m else (None, None)


def last_commit(owner, repo):
    try:
        commits = github(f"/repos/{owner}/{repo}/commits?per_page=1")
        return commits[0]["commit"]["committer"]["date"][:10] if commits else None
    except RuntimeError as e:
        print(f"  ! commits: {e}", file=sys.stderr)
        return None


NEXT_RE = re.compile(r"^.*?⏳\s*(?:next\s*[:\-|]?\s*)?(.+?)\s*$", re.I)


def next_action(owner, repo):
    """Pull the single ⏳ next item out of ROADMAP.md."""
    try:
        f = github(f"/repos/{owner}/{repo}/contents/ROADMAP.md")
        text = base64.b64decode(f["content"]).decode("utf-8", "replace")
    except RuntimeError:
        return None
    for line in text.splitlines():
        if "⏳" in line:
            cleaned = re.sub(r"[|*#\-]+", " ", line).strip()
            m = NEXT_RE.match(cleaned)
            if m:
                return m.group(1).strip()[:400]
    return None


def docs_stale(owner, repo):
    """True if code commits landed after the OS docs last moved."""
    try:
        doc = github(f"/repos/{owner}/{repo}/commits?path=ROADMAP.md&per_page=1")
        if not doc:
            return False
        doc_date = doc[0]["commit"]["committer"]["date"]
        newer = github(f"/repos/{owner}/{repo}/commits?since={doc_date}&per_page=10")
        code = [c for c in newer if not c["commit"]["message"].startswith("docs:")]
        return len(code) >= 5
    except RuntimeError:
        return False


# ----------------------------------------------------------- notion writes

def update_row(page_id, last_touched, next_act):
    props = {}
    if last_touched:
        props["Last Touched"] = {"date": {"start": last_touched}}
    if next_act:
        props["Next Action"] = {
            "rich_text": [{"type": "text", "text": {"content": next_act}}]
        }
    if not props:
        return
    if DRY_RUN:
        print(f"  [dry-run] would write {list(props)}")
        return
    notion(f"/pages/{page_id}", "PATCH", {"properties": props})


# ------------------------------------------------------------------ digest

def send(text):
    if DRY_RUN or not (TG_TOKEN and TG_CHAT):
        print("\n--- DIGEST ---\n" + text)
        return
    request(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        method="POST",
        payload={"chat_id": TG_CHAT, "text": text, "parse_mode": "HTML"},
    )


def days_since(iso):
    if not iso:
        return None
    return (TODAY - datetime.fromisoformat(iso[:10]).date()).days


# -------------------------------------------------------------------- main

def main():
    actives, alerts = [], []

    for row in fetch_portfolio():
        p = row["properties"]
        name = plain(p.get("Name")) or "(unnamed)"
        tier = plain(p.get("Tier"))
        stage = plain(p.get("Stage"))
        repo_url = plain(p.get("Repo"))
        kill_by = plain(p.get("Kill By Date"))

        if tier in ("Frozen", "Dead"):
            continue

        print(f"* {name} [{tier}]")
        owner, repo = parse_repo(repo_url)

        commit_date = next_act = None
        stale = False
        if owner:
            commit_date = last_commit(owner, repo)
            next_act = next_action(owner, repo)
            stale = docs_stale(owner, repo)
            update_row(row["id"], commit_date, next_act)
        else:
            alerts.append(f"⚠️ <b>{name}</b>: no valid GitHub repo URL")

        stalled = days_since(commit_date)
        actives.append(
            {
                "name": name,
                "stage": stage,
                "next": next_act,
                "stalled": stalled,
                "stale": stale,
            }
        )

        if stalled is not None and stalled >= STALL_DAYS:
            alerts.append(f"🥶 <b>{name}</b>: {stalled}d since last commit")
        if stale:
            alerts.append(f"📄 <b>{name}</b>: docs behind the code")
        if kill_by:
            left = (datetime.fromisoformat(kill_by[:10]).date() - TODAY).days
            if left < 0:
                alerts.append(f"☠️ <b>{name}</b>: kill-by passed {abs(left)}d ago")
            elif left <= 7:
                alerts.append(f"⏰ <b>{name}</b>: kill-by in {left}d")

    lines = [f"<b>Portfolio — {TODAY:%a %d %b}</b>", ""]
    for a in actives:
        touch = f"{a['stalled']}d ago" if a["stalled"] is not None else "no commits"
        lines.append(f"<b>{a['name']}</b> · {a['stage'] or '?'} · {touch}")
        lines.append(f"  ⏳ {a['next'] or 'no next action set'}")
    if alerts:
        lines += ["", "<b>Needs attention</b>"] + alerts
    if len(actives) > 3:
        lines += ["", f"⚠️ {len(actives)} active projects. The cap is 3."]

    send("\n".join(lines))
    print("\ndone.")


if __name__ == "__main__":
    main()
