Pull and process messages from your Slack command channel via Slack MCP tools.

**Usage:** `/pull-slack`

## Prerequisites
- Slack MCP server configured (see `docs/mcp-setup.md`)
- A dedicated Slack channel for vault commands (e.g., #obsidian-yourname)
- Channel ID configured in this command (update the ID below after setup)

## Configuration
Update this channel ID to match your command channel:
```
COMMAND_CHANNEL_ID = "YOUR_CHANNEL_ID"
```

## Steps

1. **Read new messages** from the command channel using `mcp__slack__get_channel_history`
   - Filter to messages since last pull (track via timestamp)

2. **Dispatch commands** based on message prefix:
   - `todo:` -- Add to Todo.md (Next Up section with source link)
   - `decision:` -- Log a decision via `/decision` flow
   - `note:` -- Capture to `04-Inbox/intake/` for later triage
   - `meeting:` -- Create an ad-hoc meeting note in `03-Meetings/_one-off/`
   - `search:` -- Search the vault and reply in thread
   - `jira:` -- Look up a Jira ticket and reply in thread
   - Natural language -- Classify intent:
     - If it looks like a task, treat as `todo:`
     - If it looks like a decision, treat as `decision:`
     - If it references a Jira ticket (e.g., KEY-123), treat as `jira:`
     - Otherwise, capture to inbox

3. **Add reaction** to processed messages (e.g., checkmark emoji) using `mcp__slack__add_reaction`

4. **Report results** -- count of messages processed by type

## Continuous Polling
To poll automatically, use: `/loop 5m /pull-slack`
This checks the channel every 5 minutes. Start after `/prep-day` and stop at `/close-day`.
