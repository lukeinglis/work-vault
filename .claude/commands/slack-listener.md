Start polling #obsidian-luke for commands. Run `/loop 5m /pull-slack` to check the channel every 5 minutes and dispatch any new messages.

This is the listener half of the daily Slack integration. Typical flow:

```
/prep-day          -- posts day header + meeting anchors
/slack-listener    -- starts polling (this command)
...                -- work all day, send commands from Slack
/close-day         -- pulls threads, ports notes, stops listener
```

## Startup

Before entering the loop, run these preflight checks in order. Stop on any failure.

1. **Verify Slack connection:** Make one test call (`mcp__slack__get_channel_history` on C0ASX58TJ4T, limit 1). If it fails with auth errors, tell the user to refresh tokens (`python3 ~/slack-mcp/scripts/setup-slack-mcp.py --refresh-tokens`) and stop.

2. **Check for day header:** Look for today's `-- YYYY-MM-DD --` message in #obsidian-luke. If missing, warn: "No day header found -- run /prep-day first?" and stop.

3. **Pin command reference card:** Check if the channel has a pinned message containing the command reference. If not, pin this message:

   ```
   Commands:
   todo: <text>        -- add to Todo.md
   decision: <text>    -- log a decision
   note: <text>        -- capture to inbox
   meeting: <name>     -- create ad-hoc meeting note
   search: <query>     -- search the vault
   jira: <KEY>         -- look up a Jira ticket

   Or just type naturally -- intent is classified automatically.
   ```

4. **Post listener status:** Post to #obsidian-luke: "Listener active"

5. **Start the loop:** Run `/loop 5m /pull-slack`

## Shutdown

The listener dies when the Claude Code session ends. To stop it gracefully, `/close-day` includes a step that kills the active pull-slack loop before closing out the day. The listener can also be stopped manually by ending the loop.

When stopped (by close-day or session end), the last pull-slack run's checkmark reactions ensure no messages are lost -- the next session picks up where it left off.
