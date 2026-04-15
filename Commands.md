---
title: Commands
tags: [reference]
---

# Commands

## Vault Commands

| Command               | What it does                                                                                                                |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `/decision <text>`    | Log a decision quickly from natural language. Auto-routes to the right component's decisions/ folder. |
| `/prep-day [date]`    | Fetches calendar events, creates meeting note shells, and populates the scratch pad for the target day (defaults to today). |
| `/close-day [date]`   | Pulls emails, merges AI meeting notes, ports scratch pad notes to meeting files, summarizes the day, then preps tomorrow.   |
| `/pull-emails`        | Pulls labeled emails from Gmail into the vault inbox, then removes the label.                                               |
| `/pull-slack`         | Dispatches commands from your Slack command channel: todo, decision, note, meeting, search, jira.                           |
| `/slack-listener`     | Starts polling your Slack command channel every 5 minutes. Run after `/prep-day` to listen all day.                         |
| `/jira-vault-sync`    | Syncs initiative overviews with current Jira state and reports changes.                                                     |
| `/research [component]` | Runs deep competitive/adjacent landscape research for one or all components.                                              |
