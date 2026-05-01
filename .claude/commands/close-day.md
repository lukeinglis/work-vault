Close out a day: pull emails, merge Gemini notes, port scratch pad notes to meeting files, summarize the day, then prep tomorrow.

**Usage:** `/close-day` (defaults to today) or `/close-day 2026-04-08`

## Execution Rules

- Execute every step in order. Do not skip, combine, or abbreviate steps.
- Before processing a list, state its count: "Found N Gemini notes" / "N meetings to port" / "N threads to check."
- After completing a step that produces outputs, confirm: "Step N complete: processed X, skipped Y."
- If a step fails or partially completes, state what succeeded and what did not before moving on.

## Steps

### Step 1: Pull emails

- Invoke `/pull-emails` using the Skill tool. This is a catch-up pull for emails that arrived since the morning `/prep-day` run. Wait for it to complete before proceeding. Do not inline its logic.
- State: "Pull-emails complete: N new emails processed."

### Step 2: Route any remaining Gemini notes to meetings

**Rule: one file per meeting, everything consolidated.**

Most Gemini notes are eagerly matched by `/pull-emails` (step 4) and never land in inbox. This step catches stragglers -- notes that arrived after the last pull-emails run, or that failed to match eagerly.

- Check `04-Inbox/` for any files with `source: gemini-meeting-notes` or `from: gemini-notes@google.com` in frontmatter
- State: "Found N Gemini notes in inbox." If 0, skip to Step 3.
- For each Gemini note:
  - Extract the meeting name and date from the title (format: `Notes: "Meeting Name" Mon DD, YYYY`)
  - Match to an existing meeting note in `03-Meetings/` using the same matching logic as `/pull-emails` step 4
  - **If a matching meeting note exists:**
    - Store the full Gemini content in `03-Meetings/<series-folder>/_transcripts/YYYY-MM-DD-meeting-slug-gemini.md`
    - Update the meeting file's `transcript:` frontmatter to point to the `_transcripts/` file
    - If `## Notes` already has hand-taken content (not just placeholder), add a `## Gemini Summary` section at the end
    - If `## Notes` is empty/placeholder, populate it with the Gemini content and still add `## Gemini Summary`
    - Extract action items from Gemini's "Suggested next steps" into `## Action Items` (append, don't overwrite existing)
    - Add `**Source:** [Gemini Notes](url)` at the end of the `## Gemini Summary` section
    - Add recording link to frontmatter `recording:` field if present
  - **If no matching meeting note exists:**
    - Create a new meeting note in the appropriate series folder (use existing `03-Meetings/<series-folder>/` if one matches, otherwise `03-Meetings/_one-off/`)
    - Store Gemini content in the series folder's `_transcripts/` subfolder
    - Populate the meeting file with Gemini content in both `## Notes` and `## Gemini Summary`
  - Delete the Gemini note file from `04-Inbox/` after processing
- State: "Step 2 complete: N Gemini notes routed (M matched existing meetings, K created new)."

### Step 3: Stop the Slack listener

- If a `/slack-listener` loop is active, stop it before pulling Slack threads (avoids race conditions)
- Find the active pull-slack cron/task and cancel it
- Post to #{{SLACK_CHANNEL_NAME}}: "Listener stopped -- closing day"
- If no listener is running, skip silently

### Step 4: Catch up on Slack meeting threads (#{{SLACK_CHANNEL_NAME}}, {{SLACK_CHANNEL_ID}})

This is a catch-up pass. During the day, `/pull-slack` (via the listener) captures thread replies directly to meeting note `## Notes` in real-time. This step picks up anything it missed (e.g., listener wasn't running, replies came in after the last poll).

- Use `mcp__slack__get_channel_history` to read today's messages from the channel
- Identify meeting thread anchors (format: `[HH:MM] Meeting Name` as first line)
- State: "Found N thread anchors. Checking for unprocessed replies."
- For each thread anchor with replies:
  - Use `mcp__slack__get_thread` to read all replies
  - **Skip replies already marked with `:white_check_mark:` reaction** (already processed by pull-slack)
  - Skip bot/system messages
  - For any unprocessed replies:
    - Find the corresponding meeting note in `03-Meetings/`
    - Append as bullets to `## Notes` (after any existing content)
    - Mark each processed reply with `:white_check_mark:` reaction
- If no unprocessed replies found, skip silently

### Step 5: Port scratch pad notes to meeting files

- Read the weekly note (`02-Weekly/YYYY-Www.md`)
- Find the `### DayName` section for the target day
- State: "Found N meeting blocks to process."
- For each `#### HH:MM - Meeting Name` block in the scratch pad:
  - Read the bullets under it (these are the user's hand-taken notes)
  - If there are actual notes (not just empty `-` or `_Notes:_` placeholder):
    - Find the corresponding meeting note in `03-Meetings/`
    - **Check if `## Notes` already has content** (from pull-slack thread capture or earlier processing)
      - If yes: merge scratch pad notes above existing content with a `**From scratch pad:**` header. Don't duplicate lines that already appear.
      - If no: write scratch pad notes into `## Notes`
    - If Gemini content was already merged in Step 2, keep both: hand-taken notes first, then `## Gemini Summary`
  - Replace the `####` block in the scratch pad with a collapsed link:
    `- HH:MM - Meeting Name -> [[03-Meetings/<series-folder>/YYYY-MM-DD-meeting-name]]`
  - If the `####` block has NO notes AND the meeting file has NO content (no Gemini, no Slack thread notes):
    - Delete the empty meeting note file from `03-Meetings/`
    - Remove the entry from the scratch pad entirely (meeting didn't happen or wasn't relevant)
- State: "Step 5 complete: N meetings ported, M empty meetings removed."

### Step 6: Sync sessions and GitHub activity

- Invoke `/sync-sessions` using the Skill tool. Wait for it to complete before proceeding.

### Step 7: Summarize the day

- Before writing, enumerate all sources:
  "Reading: N meeting notes [list all paths], M session summaries [list], scratch pad content for DayName."
  Read ALL listed sources. Then write the summary.
- Write a concise `**Summary:**` for the day:
  - 2-4 sentences capturing: what happened, key decisions, important context, key accomplishments from Claude Code sessions
  - Write in Luke's voice: concise, no fluff, no hedging, no emdash
  - Focus on signal: decisions made, blockers surfaced, things that changed, work shipped

### Step 8: Sync template repo (Fridays only)

Skip this step if the target day is not Friday.

- Run `scripts/sync-template.sh` to copy scaffolding (commands, rules, templates, scripts, settings) from the live vault to `~/projects/work-vault-template/`
- If changes are detected:
  - Show the user a summary of what changed (files modified/added/deleted)
  - Commit with a descriptive message and push to origin/main
  - Use `git -C ~/projects/work-vault-template` for all git commands
- If no changes, skip silently

### Step 9: Weekly cleanup (Fridays only)

Skip this step if the target day is not Friday.

**9a. Todo.md weekly cleanup:**
1. Walk `(you)` tasks in This Week -- ask the user which to roll forward vs. complete vs. drop
2. Report `(cc)` task progress -- completed (awaiting review), in progress, blocked
3. Flag stale `(both)` tasks (no activity in 7+ days)
4. Archive Done items older than 7 days to `99-Archive/completed-todos-YYYY.md`
5. Demote unfinished This Week tasks to Next Up
6. Suggest promotions from Next Up to This Week for the coming week

**9b. End-of-week summary:**
1. Read the full weekly note (`02-Weekly/YYYY-Www.md`) -- all scratch pads, meeting links, daily summaries
2. Enumerate all meeting notes from this week: "This week's meeting notes: [list all paths from wikilinks in scratch pad]. Reading all N before writing."
   Read ALL listed meeting notes.
3. Write a curated summary to `02-Weekly/_summaries/YYYY-Www-summary.md`:
   - 10-20 bullets covering: key decisions, patterns, learnings, open loops, things that shipped
   - Write in Luke's voice: concise, bullet-heavy, no fluff, no hedging
   - Group by theme (initiative, cross-cutting, vault/tooling) not by day
4. Flip `summarized: true` in the weekly note's frontmatter
5. Move the raw weekly note to `02-Weekly/_archive/`

**9c. Metrics capture:**
1. Count the following metrics for this week:
   - `meetings`: count meeting note files created this week (glob `03-Meetings/*/YYYY-MM-DD-*.md` for dates in the week)
   - `tasks_completed`: count items in Todo.md Done section with completion dates in the week
   - `open_loops`: count items in the Open Loops section of the summary just written
   - `decisions_logged`: count new decision files created this week (glob `01-Components/*/decisions/YYYY-MM-DD-*.md`)
   - `cc_sessions`: sum sessions from `07-Usage/` dashboard data for dates in the week
   - `cc_active_hours`: sum active hours from `07-Usage/` dashboard data for dates in the week
2. Add a `metrics` block to the summary file's frontmatter with these values
3. Append a new row to `02-Weekly/_summaries/_trends.md` (both the charts data arrays and the Raw Data table)
4. State: "Metrics captured: N meetings, N tasks completed, N open loops, N decisions, N sessions, N active hours."

### Step 10: Prep next working day (optional)

- Skip this step if the user passed `--no-prep` or if local time is after 9pm
- Determine the next working day (skip weekends: if today is Friday, prep Monday)
- Invoke `/prep-day` using the Skill tool with the next working day as argument.
- This gives a baseline view of what's coming, which the user can review that evening or the next morning

## Report

Keep the report tight -- 5-6 lines max, plus the day summary. Example:

```
Closed Thursday. 2 emails pulled, 1 Gemini note matched. 4 meetings ported (1 removed, empty). 3 sessions (2h 15m), 2 PRs created. Tomorrow: 5 meetings prepped.

Summary: Finalized ITS blog, aligned with Yi on release notes. Blocker: OLS engineering manager outreach stalled. Shipped vault tooling updates across 3 PRs.
```

On Fridays, append one line: "Weekly cleanup: N tasks rolled, N archived. EOW summary written."

## Edge Cases

- **Weekend:** If the target day is Friday, run the Friday steps (8, 9) and prep Monday (Step 10). If Saturday/Sunday, skip Steps 8, 9, and 10.
- **No weekly note:** Create one from the template before proceeding.
- **Meeting in scratch pad but not in 03-Meetings/:** The user added it manually. Create the meeting note file during the port step (use existing series folder or `_one-off/`).
- **Meeting in 03-Meetings/ but not in scratch pad:** The user deleted it. If it has Gemini content, keep it. If empty, delete it.
- **Re-running /close-day:** Safe to re-run. Already-ported meetings (collapsed links) are skipped. Slack threads already merged are detected by the `**From Slack:**` separator. Summary is overwritten with latest.
- **Slack MCP auth failure:** If the Slack channel read fails, log the error and continue with the rest of the close-day flow. Don't block email/Gemini/scratch pad processing.
