# Email Pull - Gmail to Vault Inbox

Pulls emails labeled "z - Obsidian" in Gmail into `04-Inbox/` as markdown files.
Uses Google Apps Script + Google Sheets as a bridge (no GCP project required).

## How it works

1. **You** label emails in Gmail with "z - Obsidian"
2. **Apps Script** exports them to a Google Sheet and saves attachments to Drive
3. **Local script** reads the Sheet and writes markdown files to the vault
4. **You** run "process my inbox" with Claude Code to triage them

## Setup (~5 min)

### 1. Create the Google Sheet

1. Create a new Google Sheet (name it "Obsidian Email Export" or similar)
2. Go to **Extensions > Apps Script**
3. Delete any default code and paste the contents of `Code.gs` from this directory
4. Click **Save** (Ctrl+S)
5. Click **Run** (the play button) with `exportEmails` selected
6. Authorize when prompted (grants access to Gmail and Drive)

### 2. Publish the Sheet as CSV

1. In the Google Sheet, go to **File > Share > Publish to web**
2. Select the **"Emails"** tab (not "Entire Document")
3. Change format from "Web page" to **"Comma-separated values (.csv)"**
4. Click **Publish**
5. Copy the URL
6. Paste it into `sheet_url.txt` in this directory:
   ```bash
   echo "https://docs.google.com/spreadsheets/d/e/YOUR_ID/pub?gid=0&single=true&output=csv" > sheet_url.txt
   ```

### 3. Run the local script

```bash
# Preview what would be imported
./pull-emails --dry-run

# Import emails
./pull-emails

# Verbose output
./pull-emails -v
```

## Optional: automatic export

Set up a time trigger so Apps Script exports emails automatically:

1. In Apps Script, click the clock icon (Triggers) in the left sidebar
2. Click **+ Add Trigger**
3. Function: `exportEmails`, Event source: Time-driven, Type: Minutes/Hours
4. Choose your interval (e.g., every hour)

With this, emails are exported to the Sheet automatically. You just run `./pull-emails` locally when you want to pull them into the vault.

## Attachments

Attachments are saved to a Google Drive folder called "Obsidian Email Attachments", organized by date and subject. The markdown files link to them as clickable Drive URLs.

## Files

| File | Purpose |
|------|---------|
| `Code.gs` | Apps Script to paste into Google Sheets |
| `pull_emails.py` | Local script that reads Sheet CSV and writes markdown |
| `pull-emails` | Shell wrapper for `pull_emails.py` |
| `sheet_url.txt` | Your published Sheet CSV URL (gitignored) |
| `.imported_ids.json` | Tracks imported message IDs (gitignored) |
