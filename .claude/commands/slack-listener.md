Start polling your Slack command channel for commands. Uses Claude Code's built-in `/loop` skill to run `/pull-slack` on a recurring interval.

Run `/loop 5m /pull-slack` to check the channel every 5 minutes.

Typical daily workflow:

```
/prep-day          -- posts day header + meeting anchors
/slack-listener    -- starts polling (this command)
...                -- work all day, send commands from Slack
/close-day         -- pulls threads, ports notes, summarizes
```

Note: `/loop` is a built-in Claude Code skill that runs a command on a recurring interval. It keeps a Claude Code session open in the background.
