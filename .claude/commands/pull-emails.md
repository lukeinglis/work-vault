Pull emails labeled for vault capture from Gmail into the vault inbox intake folder, then remove the label.

**Usage:** `/pull-emails`

## Prerequisites
- Google Workspace MCP server configured
- Gmail label created (default: "z - Obsidian") for tagging emails to import
- See `docs/mcp-setup.md` for full setup instructions

## Steps

1. **Search Gmail** for emails with the capture label using `mcp__google-workspace__search_gmail_messages`

2. **Load imported IDs tracker** (`scripts/email-pull/.imported_ids.json`) to avoid duplicates

3. **Fetch full content** for new messages using `mcp__google-workspace__get_gmail_messages_content_batch`

4. **Handle AI meeting notes specially** (e.g., Google Gemini meeting summaries):
   - Detect by subject line pattern (e.g., "Meeting notes from...")
   - Extract Google Doc URL if present
   - Match to existing meeting files by meeting name
   - Fetch the doc content and store in the meeting's `_transcripts/` folder
   - Update meeting file frontmatter with transcript link

5. **Handle meeting recording emails** similarly:
   - Match to existing meeting files
   - Update meeting file frontmatter with recording link

6. **Create intake files** in `04-Inbox/intake/` for all other emails:
   - Filename: `YYYY-MM-DD-subject-slug.md`
   - Frontmatter: title, captured date, source: email, processed: false
   - Body: sender, recipients, date, email content, links, attachments

7. **Add message IDs** to the imported tracker to prevent re-import

8. **Remove the capture label** from processed messages (keeps inbox clean)

9. **Report results**: count of imported, skipped, and routed messages

## Alternative: Script-Based Pull
If you prefer a script-based approach instead of MCP-based, see `scripts/email-pull/` for a Google Apps Script + Python pipeline that exports via Google Sheets.
