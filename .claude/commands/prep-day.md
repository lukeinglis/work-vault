Prep a day's meetings by fetching calendar events, creating meeting note shells, populating the weekly scratch pad, and providing a high-level daily focus summary.

**Usage:** `/prep-day` (defaults to today) or `/prep-day tomorrow` or `/prep-day 2026-04-10`

## Execution Rules

- Execute every step in order. Do not skip, combine, or abbreviate steps.
- Before processing a list, state its count: "Found N events" / "N meetings to create" / "N emails pulled."
- After completing a step that produces outputs, confirm: "Step N complete: created X, skipped Y."
- If a step fails or partially completes, state what succeeded and what did not before moving on.

## Steps

1. **Determine the target date:**
   - Parse the argument: no arg = today, `tomorrow` = today + 1, or an explicit `YYYY-MM-DD`
   - Determine the day of week (Monday, Tuesday, etc.)
   - Determine the ISO week number to find the right weekly note file (`02-Weekly/YYYY-Www.md`)

2. **Fetch calendar events:**
   - Use `get_events` with `user_google_email: "{{GOOGLE_EMAIL}}"`, `calendar_id: "primary"`
   - Set `time_min` to start of target date in America/New_York (use `-05:00` during EST Nov-Mar, `-04:00` during EDT Mar-Nov)
   - Set `time_max` to end of target date using the same offset
   - Set `detailed: true` to get attendees and descriptions
   - Timezone: `America/New_York`. Always determine the current UTC offset before building the timestamp

3. **Filter events:**
   - Skip all-day events that were declined or have no response
   - Skip timed events the user has declined
   - Skip timed events with no other attendees (focus time, personal blocks), UNLESS the event has a Google Meet link or the description references a group/session/presentation. Those are broadcast invites where attendees aren't individually listed; treat them as real meetings
   - **Surface accepted all-day events as context** (OOO markers, holidays, reminders). These don't become meeting notes; they appear as a "Context" line in the daily output (e.g., "OOO: Person X", "Holiday: Summit")
   - Keep all remaining timed events (meetings, syncs, 1:1s, etc.)
   - State: "Found N calendar events. After filtering: M meetings, K context events (all-day)."

4. **Ensure the weekly note exists** (`02-Weekly/YYYY-Www.md`):
   - If the file doesn't exist, create it from `Templates/weekly.md` with the correct week label

5. **Reconcile existing meeting blocks with today's calendar:**
   - Read the weekly note and find the `### DayName` section for the target day
   - Compare any existing `####` meeting blocks against the fetched calendar events (match by meeting name, fuzzy)
   - **Not on calendar + no real content** (just a `-` stub): remove the block
   - **Not on calendar + has user content** (prep notes, links, etc.): keep the block but prepend `> Not on today's calendar` above it
   - **On calendar + already listed**: leave as-is
   - **On calendar + not yet listed**: will be added in step 8
   - This makes `/prep-day` safe to re-run when meetings change

6. **Scan Todo.md:**
   - Read `Todo.md` (table format)
   - Identify tasks due today or overdue (past due date)
   - Identify tasks due tomorrow ("coming up")
   - Note any `cc` or `both` tasks that may need input
   - Store results for use by both Slack posting (step 9) and Daily Focus (step 10)

7. **For each new meeting, gather auto-prep context then create the meeting note:**
   - Path: `03-Meetings/<series-folder>/YYYY-MM-DD-slugified-meeting-name.md` for recurring meetings (use existing folder), or `03-Meetings/_one-off/` for non-recurring
   - If the file already exists (e.g., from a previous prep), skip it

   State: "N new meetings to create (M already exist, skipped)."

   **7a. Auto-prep (lightweight, always runs):**

   For **recurring meetings** (series folder exists in `03-Meetings/`):
   - Find the most recent meeting note in the series folder
   - Extract any unresolved action items, open loops, or follow-ups from it
   - Add a reference link to that note (e.g., "Last meeting: [[2026-04-23-training-hub-weekly-sync]]")
   - Check for a known shared agenda doc (e.g., Training Hub Google Doc `1MC7XPeiBcFbzcs0apMB0Bq7J-EJILJIjw6s2xPDTHds`). If one exists, fetch it and include any new agenda items

   For **meetings tied to an initiative** (infer from series name or attendees):
   - Link to the relevant `01-Components/<name>/_overview.md`
   - Surface any current blockers or upcoming deadlines from that overview

   For **one-off meetings:**
   - Include the calendar description and attendee list only, no deep search

   Cap auto-prep at 3-4 bullets + reference links per meeting. This is a scan, not research.

   **7b. Create the meeting note shell:**

   ```
   ---
   title: "MEETING_NAME"
   date: YYYY-MM-DD
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

   - AUTO_PREP_BULLET_1
   - AUTO_PREP_BULLET_2
   - Ref: [[link-to-last-meeting]] | [[link-to-overview]]

   ## Notes

   _Populated from scratch pad or transcript._

   -

   ## Decisions

   -

   ## Action Items

   - [ ] _task_ @owner

   ## Follow-ups

   -

   ## Gemini Summary

   _Auto-generated. Populated by /close-day or /pull-emails when Gemini notes arrive._

   ```

8. **Add meeting blocks to the scratch pad** under the `### DayName` section:
   - Insert BEFORE the `**Summary:**` line
   - Format each meeting as:

   ```
   #### HH:MM - Meeting Name

   - prep bullet 1 (if exists)
   - prep bullet 2
   - _Notes:_
   ```

   - If the meeting note's `## Prep` section has non-placeholder content, include those bullets under the meeting block
   - If prep is empty/placeholder, leave a bare `-` stub
   - Always end with `- _Notes:_` as a placeholder for free-hand notes during the meeting
   - Sort meetings by start time
   - Keep any existing free-form bullets that were already under `### DayName` (don't overwrite user content)

9. **Post to Slack (#{{SLACK_CHANNEL_NAME}}, {{SLACK_CHANNEL_ID}}):**

   Check channel history for today first to avoid duplicates on re-run. If a day header for today already exists, skip this entire step.

   **9a. Post day header:**

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
   - Tasks due: from the Todo scan (step 6), only items due today or overdue
   - No command reference card -- pin that once in the channel instead

   **9b. Post individual meeting messages (only for meetings with prep):**

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

10. **Build the Daily Focus summary (~4 bullets max):**

   Pull from four sources and distill to the ~4 most actionable items. This is a scan, not a report.

   Before writing, state which sources are being checked:
   "Sources checked: Todo (N overdue, M due today), Email (searching), Initiatives (3 overviews to read), Hub repos (3 to check)."
   Skip sources only if the API call fails, not by choice.

   **Sources:**

   **a) Todo.md** (from step 7):
   - Due today, overdue, coming up tomorrow
   - State: "Found N overdue tasks, M due today, K due tomorrow." (from step 6)

   **b) Recent emails:**
   - First, invoke `/pull-emails` using the Skill tool. This processes labeled emails into `04-Inbox/` and removes the Gmail label
   - Then scan `04-Inbox/` for any files created today to summarize what was pulled
   - If `/pull-emails` reports no new emails, state that and move on
   - For each pulled email: one-line summary (sender, subject, why it matters)
   - **Skip noise:** calendar accepts/declines/tentatives, noreply auto-notifications (unless actionable like Jira assignments), bounce-backs, read receipts, OOO replies, newsletters/digests

   **c) Initiative pulse:**
   - First, invoke `/jira-vault-sync` using the Skill tool to update overview files with current Jira state
   - Then read each `01-Components/<name>/_overview.md`
   - Surface blockers, upcoming deadlines, status changes, or items marked urgent/critical
   - Skip initiatives with nothing pressing

   **d) Hub repo pulse:**
   - Check `{{YOUR_ORG}}/{{REPO_1}}`, `{{REPO_2}}`, `{{REPO_3}}` via `gh` CLI
   - Recent PRs (merged/opened in last 24h), recent issues (opened in last 24h), releases (last 7 days)
   - Skip dependabot/renovate, CI/linting/typo PRs unless they indicate a build break
   - Cap at 5 items per repo. If quiet, say "quiet"

   **Output:** Flatten all sources into ~4 bullets, prioritizing by urgency. Each bullet names the source type. Example:
   - Overdue: ITS blog post (due Mon)
   - Email: Kai re: OLS engineering manager -- needs follow-up
   - its_hub: 2 PRs merged (reward-hub refactor, docs update)
   - Fine-Tuning: nothing pressing, sdg_hub/training_hub quiet

11. **Deep competitive research (Mondays only):**

   **Gate:** Check if target day is Monday. If not Monday, skip to Step 12 and state: "Step 11: skipped (not Monday)."

   - Invoke `/research all --depth deep` using the Skill tool to update all four competitive landscape briefs
   - This launches four parallel background agents (ITS, Fine-Tuning, AI Innovation, Red Hat AI) -- each takes 20-30 minutes
   - Kick this off early so it runs in parallel with the rest of prep
   - Do NOT wait for research to complete before finishing the prep-day report
   - Note in the daily focus output: "Research: deep landscape scan running for all domains (will complete in ~30 min)"

12. **Report what was done (3 sentences max):**

   Example: "Prepped 5 meetings for Thursday, added 2 with prep notes to scratch pad. 2 tasks overdue, 3 emails flagged. its_hub had 2 PRs merged; other repos quiet."

13. **Offer deep prep:**

   After the report, ask: "Want to add deep prep for any of these meetings?"

   List the meetings by time with a one-line note on what auto-prep found. The user can pick one or more, or skip.

   If the user picks a meeting, do a deeper pass:
   - Read the last 2-3 meeting notes in the series (not just the most recent)
   - Search Todo.md for tasks tagged to the relevant initiative
   - Check Jira for recent status changes on related {{JIRA_PROJECT_STRAT}} features
   - Search recent emails for threads involving key attendees
   - If a shared agenda doc exists, pull the full content
   - Write 3-5 substantive prep bullets into the meeting note's `## Prep` section
   - Update the scratch pad block with the new prep bullets
   - Post the meeting's Slack anchor message (step 9b) if not already posted
