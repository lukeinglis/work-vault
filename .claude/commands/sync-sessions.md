Summarize Claude Code sessions and GitHub activity for a target date. Called by `/close-day` or standalone.

**Usage:** `/sync-sessions` (defaults to today) or `/sync-sessions 2026-04-28`

## Execution Rules

- Execute every step in order. Do not skip, combine, or abbreviate steps.
- Before processing a list, state its count.
- After completing a step that produces outputs, confirm what was done.
- If a step fails or partially completes, state what succeeded and what did not before moving on.

## Steps

### Step 1: Sync missing sessions

- Run `python3 07-Usage/sync-sessions.py` to backfill any sessions the SessionEnd hook missed (e.g., sessions exited with Ctrl+C). This is idempotent and safe to run repeatedly.

### Step 2: Upgrade session summaries

- Load all JSON files in `07-Usage/sessions/` from the last 7 days (by filename prefix). For each, check if its `start`/`end` time range overlaps the target date, i.e., the session's `start` is before end-of-target-day AND `end` is on or after start-of-target-day. This catches resumed sessions that span multiple days.
- State: "Found N sessions overlapping target date."
- For each session that overlaps the target date:
  - Check `summary_type` field:
    - If `"llm"` -- skip, already has a quality summary
    - If `"heuristic"` or `null` -- upgrade it with an LLM-generated summary
  - To generate an LLM summary: read the transcript at the path stored in the session's `cwd` + `.claude/projects/` (the `session_id` field maps to the transcript filename)
  - Generate a 1-2 sentence summary of what the session accomplished based on the transcript content, tool calls, and files touched
  - Write the summary back into the session JSON's `summary` field and set `summary_type` to `"llm"`
  - Verify `initiatives` field -- the SessionEnd hook infers these from project name and file paths. Correct if wrong, add any missing (use transcript content for context)

### Step 3: Collect GitHub activity

- Run `gh search prs --author={{GITHUB_USERNAME}} --created=YYYY-MM-DD` to find PRs created on the target date
- For each PR found, capture: repo, number, title, state, additions, deletions
- Also check for direct commits (not just PRs) in work repos. For each repo below, run `gh api repos/{repo}/commits?author={{GITHUB_USERNAME}}&since=YYYY-MM-DDT00:00:00Z&until=YYYY-MM-DDT23:59:59Z` to get direct commits:
  - `{{GITHUB_USERNAME}}/your-repo-1`
  - `{{GITHUB_USERNAME}}/your-repo-2`
  - `your-org/project-repo`
  <!-- Add your repos here. See docs/setup-integrations.md -->
- Filter out personal repos (repos not related to your work) and fork-sync repos (sdg_hub_luke)
- Write GitHub activity into a `github` field on each matching session JSON (match by cwd/repo name)
- If PRs or commits don't match a session (e.g., done outside Claude Code), log them in a separate `07-Usage/sessions/YYYY-MM-DD-github.json` file
- State: "Found N PRs, M direct commits across K repos."

### Step 4: Update dashboard

- Run `python3 07-Usage/rollup.py` to regenerate `_dashboard.md` from all session JSONs
- On Fridays (or if the user requests it), add `--insights` to regenerate the deep insights section. On other days, cached insights from the last weekly run are reused automatically.

### Step 5: Report

State: "Synced N sessions (M upgraded to LLM summary). GitHub: P PRs, C commits. Dashboard updated."
