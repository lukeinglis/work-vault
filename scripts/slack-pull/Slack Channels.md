---
title: Slack Channels
tags: [reference, slack, mcp]
---

# Slack Channels

Channels tracked by the `/pull-slack` integration.

## Tracked Channels

| Channel | ID | Why |
|---|---|---|
| #team-engineering | C0EXAMPLE01 | Team channel |
| #project-alpha | C0EXAMPLE02 | Initiative working group |
| #general-pm | C0EXAMPLE03 | Cross-functional PM channel |

## Self-DM

| Channel | ID | Purpose |
|---|---|---|
| Self-DM ({{USER_NAME}}) | {{DM_ID}} | Direct messages to self |

## Special Channels

| Channel | ID | Purpose |
|---|---|---|
| #{{SLACK_CHANNEL_NAME}} | {{SLACK_CHANNEL_ID}} | Two-way command channel (prep, notes, commands) |
| #obsidian-log | {{LOG_CHANNEL_ID}} | MCP server diagnostic logs (separate from conversation) |

## Adding a New Channel

1. In Slack, right-click the channel name > **Copy link**
2. The URL looks like: `https://{{SLACK_WORKSPACE_DOMAIN}}/archives/C0EXAMPLE01`
3. The channel ID is the last segment (e.g., `C0EXAMPLE01`)
4. Add a row to the **Tracked Channels** table above

## How It Works

Channel access is via the Slack MCP server (`mcp__slack__*` tools). No local database or scripts needed.

**Daily flow:**
1. `/prep-day` posts day header + meeting anchors to #{{SLACK_CHANNEL_NAME}}
2. `/slack-listener` polls the channel every 5 minutes for commands (todo, decision, note, meeting, search, jira)
3. `/close-day` reads meeting threads and ports notes back to the vault

**Direct tools:**
- **Channel history**: `mcp__slack__get_channel_history` or `mcp__slack__search_channel_messages`
- **Message search**: `mcp__slack__search_messages` for cross-channel search
- **Threads**: `mcp__slack__get_thread` for full thread context

## Setup

- MCP server registered in `~/.mcp.json` (runs via podman container)
- Tokens stored at `~/.local/share/slack-mcp/tokens.env` (600 perms)
- To refresh tokens: `python3 {{SLACK_TOKEN_REFRESH_CMD}} --refresh-tokens`
