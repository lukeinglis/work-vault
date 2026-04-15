---
title: Automation
tags: [reference, tooling]
---

# Automation & Tooling

Reference for all automation set up in this vault.

## Email Pull (Gmail -> Vault)

Pulls emails into `04-Inbox/` as markdown files for triage.

### How it works

1. **Apps Script** (runs hourly in Google) exports labeled emails to a Google Sheet and saves attachments to Google Drive
2. **Local script** downloads the Sheet as CSV and converts each row to a markdown file in `04-Inbox/`
3. **Claude Code** triages inbox items into the right vault folders ("process my inbox")

### Day-to-day usage

Label any email in Gmail with your capture label (default: **z - Obsidian**), then run:

```bash
./scripts/email-pull/pull-emails
```

That's it. The script downloads the latest Sheet export, imports new emails, and skips ones already imported.

Options:
- `--dry-run` -- preview what would be imported
- `-v` -- verbose output

### Setup

1. Create a Google Sheet (e.g., "Obsidian Email Export")
2. Add Apps Script (`scripts/email-pull/Code.gs`) via Extensions > Apps Script
3. Authorize Gmail + Drive access on first run
4. Set hourly trigger: Apps Script > Triggers > `exportEmails` every hour
5. Publish Sheet "Emails" tab as CSV
6. Save the Sheet URL in `scripts/email-pull/sheet_url.txt`

### Key files

| File | Purpose |
|------|---------|
| `scripts/email-pull/pull_emails.py` | Python script that converts CSV rows to markdown |
| `scripts/email-pull/Code.gs` | Apps Script source (copy of what's deployed in Google) |
| `scripts/email-pull/.imported_ids.json` | Tracks which emails have been imported (gitignored) |

### Attachments

Email attachments are saved to a Google Drive folder called **Obsidian Email Attachments**, organized by date and subject. Markdown files link to them as clickable Drive URLs.

### Troubleshooting

- **"No new emails"** -- the Apps Script trigger may not have run yet. Go to the Sheet, open Apps Script, and run `exportEmails` manually.
- **Script hangs on download** -- make sure you're logged into Google in your default browser.
- **Want to re-import everything** -- delete `scripts/email-pull/.imported_ids.json` and run again.
- **Want to clear the Sheet** -- run `clearSheet()` in Apps Script.

## Jira Sync (`/jira-vault-sync`)

Syncs Jira ticket state into initiative `_overview.md` files. Invoke with `/jira-vault-sync` in Claude Code. Requires Jira MCP server to be configured.

## Slack Integration

Two-way communication with a dedicated Slack channel:
- `/prep-day` posts the day's schedule
- `/pull-slack` reads commands from the channel
- `/close-day` pulls meeting threads back into the vault

See `docs/mcp-setup.md` for Slack MCP server setup.
