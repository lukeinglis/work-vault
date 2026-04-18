Prep a day's meetings by fetching calendar events, creating meeting note shells, populating the weekly scratch pad, and providing a high-level daily focus summary.

**Usage:** `/prep-day` (defaults to today) or `/prep-day tomorrow` or `/prep-day 2026-04-10`

## Steps

1. **Determine the target date:**
   - Parse the argument: no arg = today, `tomorrow` = today + 1, or an explicit `YYYY-MM-DD`
   - Determine the day of week (Monday, Tuesday, etc.)
   - Determine the ISO week number to find the right weekly note file (`02-Weekly/YYYY-Www.md`)

2. **Fetch calendar events:**
   - Use `get_events` with `user_google_email: "linglis@redhat.com"`, `calendar_id: "primary"`
   - Set `time_min` to start of target date (e.g., `2026-04-08T00:00:00-04:00`)
   - Set `time_max` to end of target date (e.g., `2026-04-08T23:59:59-04:00`)
   - Set `detailed: true` to get attendees and descriptions
   - Timezone: `America/New_York` (EST/EDT)

3. **Filter events:**
   - Skip all-day events that were declined or have no response
   - Skip timed events the user has declined
   - Skip timed events with no other attendees (focus time, personal blocks)
   - **Surface accepted all-day events as context** (OOO markers, holidays, reminders). These don't become meeting notes -- they appear as a "Context" line in the daily output (e.g., "OOO: Person X", "Holiday: Summit")
   - Keep all remaining timed events -- meetings, syncs, 1:1s, etc.

4. **Classify each meeting by type** using the meeting name. Apply these rules in order:

   **manager-1on1:**
   - `luke/tushar`, `luke tushar`, `1:1`, `1-1` (with Tushar)

   **bu/** (business unit cross-team):
   - `inference pod`, `ai bu cross team`, `ai bu pm collab`, `pm / cai`, `pm/cai`

   **leadership:**
   - `tushar - extended`, `tushar extended`, `ai eng/ai bu roadmap`, `what's new and what's next`, `whats new`, `dry run`

   **component/** (AI Innovation team and hub-specific):
   - `ai innovation team`, `training hub`, `its_hub`, `its-hub`, `itshub`, `its hub`, `sdg`, `pod sync`, `model customization`, `model customisation`, `connecting data to models`, `yi - luke`, `yi/luke`

   **other/** (default):
   - Everything else: hiring, demos, deep dives, ad-hoc meetings

5. **Read the weekly note file** (`02-Weekly/YYYY-Www.md`):
   - If the file doesn't exist, create it from `Templates/weekly.md` with the correct week label
   - Find the `### DayName` section for the target day

6. **Check for existing meeting blocks:**
   - If the scratch pad already has `####` meeting blocks for this day, do NOT overwrite them
   - Only add NEW meetings that aren't already listed (match by meeting name, fuzzy)
   - This makes `/prep-day` safe to re-run mid-day when new meetings are added

7. **Scan Todo.md:**
   - Read `Todo.md` (table format)
   - Identify tasks due today or overdue (past due date)
   - Identify tasks due tomorrow ("coming up")
   - Note any `cc` or `both` tasks that may need input
   - Store results for use by both Slack posting (step 10) and Daily Focus (step 11)

8. **For each new meeting, create a meeting note shell:**
   - Path: `03-Meetings/<type>/YYYY-MM-DD-slugified-meeting-name.md`
   - If the file already exists (e.g., from a previous prep), skip it
   - Use this template:

   ```
   ---
   title: "MEETING_NAME"
   date: YYYY-MM-DD
   type: "TYPE"
   attendees: [ATTENDEE_NAMES]
   initiatives: []
   transcript: ""
   recording: ""
   tags: [meeting]
   ---

   # MEETING_NAME

   **Date:** YYYY-MM-DD
   **Attendees:** ATTENDEE_NAMES

   ## Prep

   _What I want to get out of this meeting._

   -

   ## Notes

   _Populated from scratch pad or transcript._

   -

   ## Decisions

   -

   ## Action Items

   - [ ] _task_ -- @owner

   ## Follow-ups

   -

   ## Gemini Summary

   _Auto-generated. Populated by /close-day or /pull-emails when Gemini notes arrive._

   ```

9. **Add meeting blocks to the scratch pad** under the `### DayName` section:
   - Insert BEFORE the `**Summary:**` line
   - Format each meeting as:

   ```
   #### HH:MM -- Meeting Name [type]

   - prep bullet 1 (if exists)
   - prep bullet 2
   ```

   - If the meeting note's `## Prep` section has non-placeholder content, include those bullets under the meeting block
   - If prep is empty/placeholder, leave a bare `-` stub
   - Sort meetings by start time
   - Keep any existing free-form bullets that were already under `### DayName` (don't overwrite user content)

10. **Post to Slack (#obsidian-luke, C0ASX58TJ4T):**

   Check channel history for today first to avoid duplicates on re-run. If a day header for today already exists, skip this entire step.

   **10a. Post day header:**

   Post a single overview message to the channel:

   ```
   -- YYYY-MM-DD (DayName) --

   Context: OOO: Person X | Holiday: Y

   N meetings today:
   - HH:MM Meeting Name
   - HH:MM Meeting Name
   - HH:MM Meeting Name

   Tasks due:
   - Task 1
   - Task 2
   (or "None" if nothing due today)
   ```

   Rules:
   - Context line only appears if there are accepted all-day events; omit the line entirely otherwise
   - Tasks due: from the Todo scan (step 7), only items due today or overdue
   - No command reference card -- pin that once in the channel instead

   **10b. Post individual meeting messages (only for meetings with prep):**

   Only post a separate message for meetings where the `## Prep` section has non-placeholder content. Meetings with empty prep stay in the day header list only.

   ```
   [HH:MM] Meeting Name
   Attendees: Name1, Name2, Name3
   ---
   - Prep bullet 1
   - Prep bullet 2
   ```

   Rules:
   - One message per meeting (only those with prep), posted in chronological order
   - Attendees: use first names only, skip the user's own name
   - These messages become thread anchors -- the user replies with notes during the meeting
   - On re-run after prep is added to a meeting note, post the individual message if not already posted

11. **Build the Daily Focus summary (~4 bullets max):**

   Pull from four sources and distill to the ~4 most actionable items. This is a scan, not a report.

   **Sources:**

   **a) Todo.md** (from step 7):
   - Due today, overdue, coming up tomorrow

   **b) Recent emails:**
   - Use `search_gmail_messages` with query: `label:z - Obsidian after:YYYY/MM/DD` where the date is the previous day
   - Only search the labeled set (the curated intake). If no labeled emails exist, nudge: "consider running /pull-emails"
   - **Skip noise:** calendar accepts/declines/tentatives, noreply auto-notifications (unless actionable like Jira assignments), bounce-backs, read receipts, OOO replies, newsletters/digests
   - For each remaining email: one-line summary (sender, subject, why it matters)

   **c) Initiative pulse:**
   - Read each `01-Components/<name>/_overview.md`
   - Surface blockers, upcoming deadlines, or items marked urgent/critical
   - Skip initiatives with nothing pressing

   **d) Hub repo pulse:**
   - Check `Red-Hat-AI-Innovation-Team/its_hub`, `sdg_hub`, `training_hub` via `gh` CLI
   - Recent PRs (merged/opened in last 24h), recent issues (opened in last 24h), releases (last 7 days)
   - Skip dependabot/renovate, CI/linting/typo PRs unless they indicate a build break
   - Cap at 5 items per repo. If quiet, say "quiet"

   **Output:** Flatten all sources into ~4 bullets, prioritizing by urgency. Each bullet names the source type. Example:
   - Overdue: ITS blog post (due Mon)
   - Email: Kai re: OLS engineering manager -- needs follow-up
   - its_hub: 2 PRs merged (reward-hub refactor, docs update)
   - Fine-Tuning: nothing pressing, sdg_hub/training_hub quiet

12. **Jira vault sync (Mondays only):**

   Skip this step if the target day is not Monday.

   - Run the `/jira-vault-sync` flow to sync initiative overviews with current Jira state
   - Include the sync summary in the daily focus output (e.g., "Jira: 2 ITS status changes, 1 new Fine-Tuning ticket")
   - This ensures the week starts with overviews that reflect the latest Jira state

13. **Report what was done (3 sentences max):**

   Example: "Prepped 5 meetings for Thursday, added 2 with prep notes to scratch pad. 2 tasks overdue, 3 emails flagged. its_hub had 2 PRs merged; other repos quiet."
