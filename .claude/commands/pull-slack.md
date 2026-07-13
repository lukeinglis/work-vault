Pull and process messages from #{{SLACK_CHANNEL_NAME}} ({{SLACK_CHANNEL_ID}}) via Slack MCP tools. Handles command dispatch and general channel pulls. Called directly or via `/slack-listener` (which runs `/loop 5m /pull-slack`).

## Notifications

All thread replies must @mention the user (`<@{{SLACK_USER_ID}}>`) so Slack sends a push notification. This ensures the user sees confirmations on their phone/desktop regardless of channel notification settings.

## Channel Reference

See `scripts/slack-pull/Slack Channels.md` for the full list of tracked channels and IDs.

## Execution Rules

- Execute every step in order. Do not skip, combine, or abbreviate steps.
- Before processing a list, state its count: "Found N messages" / "N thread anchors to check."
- After completing a step that produces outputs, confirm: "Step N complete: processed X, skipped Y."
- If a step fails or partially completes, state what succeeded and what did not before moving on.

## Steps

### Step 1: Read new messages from #{{SLACK_CHANNEL_NAME}}

1. Use `mcp__slack__get_channel_history` on channel {{SLACK_CHANNEL_ID}}
2. Filter to messages since the last check:
   - On first run of the day, process all messages after today's day header (the `-- YYYY-MM-DD --` message posted by `/prep-day`)
   - On subsequent runs (via `/loop`), process messages since the last processed timestamp
   - Track the last processed timestamp in memory during the session (no file needed -- session-scoped)
3. Skip messages posted by this integration (avoid processing our own replies)
4. Skip thread replies in the top-level message scan (threads are handled separately in step 3)
5. State: "Found N new messages since last check (M already processed via checkmark, K to dispatch)."

### Step 2: Dispatch commands

For each new top-level message, match the prefix and route:

**`todo:` -- Add to Todo.md**
- Parse the text after the prefix
- Add a new row to the appropriate section of Todo.md (default: This Week, owner: (you))
- If a due date is mentioned (e.g., "by Thursday", "due 4/18"), parse it and set the date column
- Reply in thread: "<@{{SLACK_USER_ID}}> Added to Todo.md: <task text>"

**`decision:` -- Log a decision**
- Parse the text after the prefix
- Run the `/decision` flow with the text as input
- Reply in thread: "<@{{SLACK_USER_ID}}> Decision logged: <file path>"

**`note:` -- Capture to inbox**
- Parse the text after the prefix
- Write to `04-Inbox/intake/YYYY-MM-DD-slack-note-<short-slug>.md` with frontmatter:
  ```
  ---
  title: "<first ~60 chars>"
  created: YYYY-MM-DD
  tags: [slack, inbox]
  source: {{SLACK_CHANNEL_NAME}}
  ---
  ```
- Reply in thread: "<@{{SLACK_USER_ID}}> Captured to intake"

**`meeting:` -- Create an ad-hoc meeting note**
- Parse the text after the prefix for meeting name and any context/notes
- This is for spur-of-the-moment meetings -- a quick way to capture context that gets formalized into a proper meeting note
- Create a meeting note in the appropriate series folder (use existing `03-Meetings/<series-folder>/` if one matches, otherwise `03-Meetings/_one-off/YYYY-MM-DD-<slugified-name>.md`) using the standard meeting note template
- If context/notes were included after the meeting name, add them to the `## Notes` section
- Add a `####` block to today's scratch pad in the weekly note (use current time as the time slot)
- Post a meeting message to #{{SLACK_CHANNEL_NAME}} in the same format as prep-day meeting messages:
  ```
  [HH:MM] Meeting Name
  ---
  (any context provided)
  ```
- This message becomes a thread anchor for notes, just like prep-day meetings
- Reply in the original command thread: "<@{{SLACK_USER_ID}}> Meeting created: <file path> -- posted to channel for notes"

**`search:` -- Search the vault**
- Parse the query after the prefix
- Search across vault files using Grep (content) and Glob (filenames)
- Reply in thread with top results (max 5):
  - File path, matching line or title, relevance
- If no results: "<@{{SLACK_USER_ID}}> No matches found for: <query>"

**`jira:` -- Look up a Jira ticket**
- Parse the Jira key after the prefix (e.g., PROJ-1234, STRAT-567)
- Use `mcp__jira__jira_get_issue` to fetch the ticket
- Reply in thread with: summary, status, assignee, priority, and link
- Also supports natural language Jira queries (e.g., "find the latest RFE on inference-time scaling") -- use `mcp__jira__jira_search` with JQL to find matching tickets and reply with results

**No prefix (natural language / plain text / forwarded messages)** -- Classify intent
- Do NOT blindly route to intake. Read the message and classify the intent:
  - If it asks to find, look up, pull, or check something in **Jira** (mentions RFE, ticket, {{JIRA_PROJECT_STRAT}}, {{JIRA_PROJECT_RFE}}, {{JIRA_PROJECT_ENG}}, epic, story, feature) -> treat as a `jira:` command. Use `mcp__jira__jira_search` with appropriate JQL and reply with results in thread.
  - If it asks to **search** or find something in the vault, notes, meetings, or decisions -> treat as a `search:` command
  - If it reads like a **task or action item** (mentions "need to", "follow up", "remind me", "don't forget") -> treat as a `todo:` command
  - If it reads like a **decision** ("decided", "we agreed", "going with") -> treat as a `decision:` command
  - If it's a forwarded message or a general note with no clear action -> route to intake
- Always reply in thread (with `<@{{SLACK_USER_ID}}>` mention) with what action was taken and the result
- When in doubt about intent, execute the most likely action rather than defaulting to intake

### Step 3: Read meeting threads

Identify ALL meeting thread anchors for today (messages matching `[HH:MM]` format posted by `/prep-day` or the `meeting:` command). State: "Found N thread anchors to check." Process each one. Do not stop early.

For each meeting thread anchor:

1. Use `mcp__slack__get_thread` to read the full thread
2. Identify new replies since the last check:
   - Skip replies already marked with `:white_check_mark:` reaction
   - Skip replies posted by this integration (our own bot messages)
3. Match the thread anchor to its meeting note file:
   - Parse the meeting name from the anchor message
   - Find the corresponding file in `03-Meetings/` by date + slugified name
   - If no matching file found, skip (orphaned thread)
4. Append new replies to the meeting note's `## Notes` section:
   - Add each reply as a bullet point: `- <message text>`
   - Preserve message order (chronological)
   - Don't try to structure or summarize -- raw capture only
   - If the Notes section still has the placeholder (`_Populated from scratch pad or transcript._`), replace it
5. Mark each processed reply with `:white_check_mark:` reaction

This keeps meeting notes populated in near-real-time. `/close-day` still does the final cleanup and summarization pass.

### Step 4: Confirm processing

After processing all top-level messages (step 2), add a checkmark reaction (`:white_check_mark:`) to each processed message using `mcp__slack__add_reaction`. This prevents reprocessing on the next loop run -- skip any message that already has this reaction.

### Step 5: Report

When run manually: one line per action taken, e.g., "Processed 3 commands (2 todos, 1 decision). 4 already processed, skipped."

When run via `/loop`: only report if commands were actually processed (stay silent on empty checks).

## Channel Summaries (on request)

Only do this if the user explicitly asks for channel summaries. Do NOT run automatically.

1. For each tracked channel the user specifies:
   - Use `mcp__slack__get_channel_history` to pull recent messages (default: last 24 hours)
   - Summarize key discussions, decisions, action items, and links shared
2. Write a combined summary to `04-Inbox/intake/YYYY-MM-DD-slack-channel-summaries.md`

## Tracked Channels as Search Context

When a `search:` or `jira:` command (or natural language query) references a topic, the tracked channels in `scripts/slack-pull/Slack Channels.md` are the first places to look for Slack context. Use `mcp__slack__search_channel_messages` scoped to the relevant channel(s) before falling back to `mcp__slack__search_messages` for cross-channel search.

## Token Issues

If MCP tools fail with auth errors:
- Tell the user their Slack token needs refreshing
- Run: `python3 {{SLACK_TOKEN_REFRESH_CMD}} --refresh-tokens`
- Stop processing
