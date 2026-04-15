---
title: Automation
tags: [reference, tooling]
---

# Automation & Tooling

Reference for all automation set up in this vault.

## Email Pull (Gmail -> Vault)

Pulls emails into `04-Inbox/` as markdown files for triage.

### How it works (MCP -- recommended)

1. Label emails in Gmail with **z - Obsidian** (or your capture label)
2. Run `/pull-emails` in Claude Code
3. Claude Code reads Gmail via the Google Workspace MCP server, creates markdown files, routes AI meeting notes to the right meeting files, and removes the label
4. Run "process my inbox" to triage new items into the right vault folders

Requires the Google Workspace MCP server. See `docs/mcp-setup.md`.

### Fallback: Script-Based Pull (no MCP required)

If you can't use the MCP server (e.g., enterprise auth restrictions), there's an Apps Script + Python pipeline in `scripts/email-pull/`:

1. **Apps Script** (`Code.gs`) runs hourly in Google, exports labeled emails to a Google Sheet, and saves attachments to Drive
2. **Python script** (`pull_emails.py`) downloads the Sheet as CSV and converts each row to a markdown file in `04-Inbox/`

**Setup:**
1. Create a Google Sheet (e.g., "Obsidian Email Export")
2. Add Apps Script (`scripts/email-pull/Code.gs`) via Extensions > Apps Script
3. Authorize Gmail + Drive access on first run
4. Set hourly trigger: Apps Script > Triggers > `exportEmails` every hour
5. Publish Sheet "Emails" tab as CSV
6. Save the Sheet URL in `scripts/email-pull/sheet_url.txt`

**Usage:**
```bash
python3 scripts/email-pull/pull_emails.py          # import new emails
python3 scripts/email-pull/pull_emails.py --dry-run # preview only
```

**Troubleshooting:**
- **"No new emails"** -- the Apps Script trigger may not have run yet. Run `exportEmails` manually in Apps Script.
- **Want to re-import** -- delete `scripts/email-pull/.imported_ids.json` and run again.

## Jira Sync (`/jira-vault-sync`)

Syncs Jira ticket state into initiative `_overview.md` files. Invoke with `/jira-vault-sync` in Claude Code. Requires Jira MCP server to be configured.

## Slack Integration

Two-way communication with a dedicated Slack channel:
- `/prep-day` posts the day's schedule
- `/pull-slack` reads commands from the channel
- `/close-day` pulls meeting threads back into the vault

See `docs/mcp-setup.md` for Slack MCP server setup.
