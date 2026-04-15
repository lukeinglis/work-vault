Close out a day: pull emails, merge meeting notes, port scratch pad notes to meeting files, summarize the day, then prep tomorrow.

**Usage:** `/close-day` (defaults to today) or `/close-day 2026-04-08`

## Steps

1. **Pull emails** via `/pull-emails` (if email integration is configured)
   - Import any new emails labeled for vault capture
   - Route meeting-related emails (e.g., Gemini summaries, recordings) to matching meeting notes

2. **Route meeting notes from email to meeting files**
   - Match AI meeting summaries (e.g., Google Gemini notes) to existing meeting files
   - Merge into the `## Gemini Summary` section of the matching meeting note
   - Update frontmatter with recording links if present

3. **Pull Slack messages** (if Slack MCP is configured)
   - Read your command channel for any messages/commands posted during the day
   - Process todo, decision, note, and other command types

4. **Port scratch pad notes to meeting files**
   - Read the day's scratch pad section in the weekly note
   - For each meeting listed, check if there are inline notes under the meeting link
   - Port those notes to the meeting file's `## Notes` section

5. **Summarize the day**
   - Add a `**Summary:**` line under the day's scratch pad section
   - 3-5 bullet summary: key decisions, progress, blockers, follow-ups

6. **Summarize Claude Code sessions and activity**
   - Log session stats to `07-Usage/` if session tracking is enabled

7. **Weekly cleanup** (Fridays only)
   - Walk Todo.md: archive done items, demote unfinished This Week to Next Up
   - Suggest promotions from Next Up to This Week for next week
   - Write end-of-week summary to `02-Weekly/_summaries/`

8. **Prep next working day**
   - Run prep-day logic for the next business day (skip weekends)

## Meeting Name Matching
The command normalizes meeting names for matching:
- Strips dates, prefixes, common suffixes
- Compares against folder names in `03-Meetings/`
- Falls back to fuzzy matching when exact match fails
