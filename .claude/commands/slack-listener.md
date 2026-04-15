Start polling your Slack command channel for commands. Run `/loop 5m /pull-slack` to check the channel every 5 minutes.

Typical daily workflow:

```
/prep-day          -- posts day header + meeting anchors
/slack-listener    -- starts polling (this command)
...                -- work all day, send commands from Slack
/close-day         -- pulls threads, ports notes, summarizes
```
