Close out a day: pull emails, merge Gemini notes, port scratch pad notes to meeting files, summarize the day, then prep tomorrow.

**Usage:** `/close-day` (defaults to today) or `/close-day 2026-04-08`

## Steps (execute in this order)

### Step 1: Pull emails

- Run the `/pull-emails` flow to grab any new Gemini notes or emails that arrived today
- Wait for this to complete before proceeding

### Step 2: Route any remaining Gemini notes to meetings

**Rule: one file per meeting, everything consolidated.**

Most Gemini notes are eagerly matched by `/pull-emails` (step 4) and never land in inbox. This step catches stragglers -- notes that arrived after the last pull-emails run, or that failed to match eagerly.

- Check `04-Inbox/` for any files with `source: gemini-meeting-notes` or `from: gemini-notes@google.com` in frontmatter
- For each Gemini note:
  - Extract the meeting name and date from the title (format: `Notes: "Meeting Name" Mon DD, YYYY`)
  - Match to an existing meeting note in `03-Meetings/` using the same matching logic as `/pull-emails` step 4
  - **If a matching meeting note exists:**
    - Store the full Gemini content in `03-Meetings/<type>/_transcripts/YYYY-MM-DD-meeting-slug-gemini.md`
    - Update the meeting file's `transcript:` frontmatter to point to the `_transcripts/` file
    - If `## Notes` already has hand-taken content (not just placeholder), add a `## Gemini Summary` section at the end
    - If `## Notes` is empty/placeholder, populate it with the Gemini content and still add `## Gemini Summary`
    - Extract action items from Gemini's "Suggested next steps" into `## Action Items` (append, don't overwrite existing)
    - Add `**Source:** [Gemini Notes](url)` at the end of the `## Gemini Summary` section
    - Add recording link to frontmatter `recording:` field if present
  - **If no matching meeting note exists:**
    - Create a new meeting note using the same classification logic as `/prep-day` step 4
    - Store Gemini content in the appropriate `_transcripts/` folder
    - Populate the meeting file with Gemini content in both `## Notes` and `## Gemini Summary`
  - Delete the Gemini note file from `04-Inbox/` after processing

### Step 3: Stop the Slack listener

- If a `/slack-listener` loop is active, stop it before pulling Slack threads (avoids race conditions)
- Find the active pull-slack cron/task and cancel it
- Post to #obsidian-luke: "Listener stopped -- closing day"
- If no listener is running, skip silently

### Step 4: Catch up on Slack meeting threads (#obsidian-luke, C0ASX58TJ4T)

This is a catch-up pass. During the day, `/pull-slack` (via the listener) captures thread replies directly to meeting note `## Notes` in real-time. This step picks up anything it missed (e.g., listener wasn't running, replies came in after the last poll).

- Use `mcp__slack__get_channel_history` to read today's messages from the channel
- Identify meeting thread anchors (format: `[HH:MM] Meeting Name` as first line)
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
- For each `#### HH:MM -- Meeting Name [type]` block in the scratch pad:
  - Read the bullets under it (these are the user's hand-taken notes)
  - If there are actual notes (not just empty `-`):
    - Find the corresponding meeting note in `03-Meetings/<type>/`
    - **Check if `## Notes` already has content** (from pull-slack thread capture or earlier processing)
      - If yes: merge scratch pad notes above existing content with a `**From scratch pad:**` header. Don't duplicate lines that already appear.
      - If no: write scratch pad notes into `## Notes`
    - If Gemini content was already merged in Step 2, keep both: hand-taken notes first, then `## Gemini Summary`
  - Replace the `####` block in the scratch pad with a collapsed link:
    `- HH:MM -- Meeting Name -> [[03-Meetings/type/YYYY-MM-DD-meeting-name]]`
  - If the `####` block has NO notes AND the meeting file has NO content (no Gemini, no Slack thread notes):
    - Delete the empty meeting note file from `03-Meetings/`
    - Remove the entry from the scratch pad entirely (meeting didn't happen or wasn't relevant)

### Step 6: Summarize Claude Code sessions and GitHub activity

Run this before the day summary so session data is upgraded and available.

**Session summaries:**
- Load all JSON files in `07-Usage/sessions/` from the last 7 days (by filename prefix). For each, check if its `start`/`end` time range overlaps the target date -- i.e., the session's `start` is before end-of-target-day AND `end` is on or after start-of-target-day. This catches resumed sessions that span multiple days and are filed under their original start date.
- For each session that overlaps the target date:
  - Check `summary_type` field:
    - If `"llm"` -- skip, already has a quality summary
    - If `"heuristic"` or `null` -- upgrade it with an LLM-generated summary
  - To generate an LLM summary: read the transcript at the path stored in the session's `cwd` + `.claude/projects/` (the `session_id` field maps to the transcript filename)
  - Generate a 1-2 sentence summary of what the session accomplished based on the transcript content, tool calls, and files touched
  - Write the summary back into the session JSON's `summary` field and set `summary_type` to `"llm"`
  - Verify `initiatives` field -- the SessionEnd hook infers these from project name and file paths. Correct if wrong, add any missing (use transcript content for context)

**GitHub activity (PRs and direct pushes):**
- Run `gh search prs --author=lukeinglis --created=YYYY-MM-DD` to find PRs created today
- For each PR found, capture: repo, number, title, state, additions, deletions
- Also check for direct commits (not just PRs) in work repos. For each repo below, run `gh api repos/{repo}/commits?author=lukeinglis&since=YYYY-MM-DDT00:00:00Z&until=YYYY-MM-DDT23:59:59Z` to get direct commits:
  - `lukeinglis/its_hub_demo`
  - `lukeinglis/its_hub_luke`
  - `Red-Hat-AI-Innovation-Team/its_hub`
  - `Red-Hat-AI-Innovation-Team/sdg_hub`
  - `Red-Hat-AI-Innovation-Team/Red-Hat-AI-Innovation-Team.github.io`
- Filter out personal repos (FantasyBaseball, FantasyFootball, Luke) and fork-sync repos (sdg_hub_luke)
- Write GitHub activity into a `github` field on each matching session JSON (match by cwd/repo name)
- If PRs or commits don't match a session (e.g., done outside Claude Code), log them in a separate `07-Usage/sessions/YYYY-MM-DD-github.json` file

**Sync missing sessions:**
- Run `python3 07-Usage/sync-sessions.py` to backfill any sessions the SessionEnd hook missed (e.g., sessions exited with Ctrl+C). This is idempotent and safe to run repeatedly.

**Dashboard update:**
- Run `python3 07-Usage/rollup.py` to regenerate `_dashboard.md` from all session JSONs
- On Fridays (or if the user requests it), add `--insights` to regenerate the deep insights section. On other days, cached insights from the last weekly run are reused automatically.
- The script handles all rollups: Today, This Week, This Month, YTD, All Time, daily breakdown, charts, insights, and recent accomplishments

### Step 7: Summarize the day

- Read all content under `### DayName` for the target day (including the collapsed meeting links and any free-form notes)
- Read the meeting notes that were populated today (the full content in `03-Meetings/`)
- Read the session JSONs identified in step 6 (those whose start/end range overlaps the target date, now upgraded to LLM-quality summaries)
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
2. Read the meeting notes that were populated this week (follow the `[[03-Meetings/...]]` links)
3. Write a curated summary to `02-Weekly/_summaries/YYYY-Www-summary.md`:
   - 10-20 bullets covering: key decisions, patterns, learnings, open loops, things that shipped
   - Write in Luke's voice: concise, bullet-heavy, no fluff, no hedging
   - Group by theme (initiative, cross-cutting, vault/tooling) not by day
4. Flip `summarized: true` in the weekly note's frontmatter

### Step 10: Prep next working day (optional)

- Skip this step if the user passed `--no-prep` or if local time is after 9pm
- Determine the next working day (skip weekends: if today is Friday, prep Monday)
- Run the `/prep-day` flow for that day
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
- **Meeting in scratch pad but not in 03-Meetings/:** The user added it manually. Create the meeting note file during the port step using the `[type]` tag from the scratch pad.
- **Meeting in 03-Meetings/ but not in scratch pad:** The user deleted it. If it has Gemini content, keep it. If empty, delete it.
- **Re-running /close-day:** Safe to re-run. Already-ported meetings (collapsed links) are skipped. Slack threads already merged are detected by the `**From Slack:**` separator. Summary is overwritten with latest.
- **Slack MCP auth failure:** If the Slack channel read fails, log the error and continue with the rest of the close-day flow. Don't block email/Gemini/scratch pad processing.
