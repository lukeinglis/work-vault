Prep a day's meetings by fetching calendar events, creating meeting note shells, populating the weekly scratch pad, and providing a daily focus summary.

**Usage:** `/prep-day` (today) or `/prep-day tomorrow` or `/prep-day 2026-04-10`

## Steps

1. **Determine target date** and find (or create) the weekly note file (`02-Weekly/YYYY-Www.md`)

2. **Fetch Google Calendar events** for the target date using `mcp__google-workspace__get_events`
   - Filter out: all-day events, declined events, focus time, OOO blocks
   - Sort by start time

3. **Classify each meeting** by type:
   - Match against known recurring meetings in `03-Meetings/`
   - One-off meetings go to `03-Meetings/_one-off/`

4. **Create meeting note shells** for each meeting that doesn't already have one:
   - Use `Templates/meeting.md`
   - Filename: `YYYY-MM-DD-short-topic.md`
   - Fill: title, date, type, attendees from calendar event
   - Tag initiatives from frontmatter if the meeting maps to a known initiative

5. **Add meeting blocks to the scratch pad** in the weekly note:
   - Under the correct day-of-week heading
   - Format: `- **HH:MM** [[03-Meetings/path/to/note|Meeting Title]]`
   - Sorted by start time

6. **Post to Slack** (if Slack MCP is configured):
   - Post a day header message to your command channel
   - Post individual meeting anchor messages as thread replies

7. **Build Daily Focus summary** from:
   - Todo.md scan (tasks due today/tomorrow)
   - Recent emails (if email integration is configured)
   - Initiative pulse check (read `_overview.md` files for blockers/status)

8. **Report** meetings created and schedule summary

## Prerequisites
- Google Workspace MCP server configured (for calendar access)
- Slack MCP server configured (optional, for Slack posting)
- Weekly note for the target week must exist or will be created from template
