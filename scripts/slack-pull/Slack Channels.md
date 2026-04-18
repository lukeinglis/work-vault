---
title: Slack Channels
tags: [reference, slack, mcp]
---

# Slack Channels

Channels tracked by the `/pull-slack` integration.

## Tracked Channels

| Channel | ID | Why |
|---|---|---|
| #ai-innov-openshft-poc | C0ANT8ZLMV4 | ITS OpenShift initiative |
| #labs | C088ZF9E05N | AI Innovation Team channel |
| #rhai-its | C09RJDFTRDG | Public channel for ITS |
| #rhai-sdg-hub | C0987K24BNV | Public channel for SDG |
| #rhai-training-hub | C09937CF05C | Public channel for Training Hub |
| #team-ai-bu | C03UA1YQGR3 | BU Slack channel |
| #team-ai-pm | C07SPJ8TP9N | PM Slack channel |
| #wg-its-hub-rhai | C09NX1S47QW | Private working group ITS channel |
| #wg-lab-ai-first | C0AND2XGKLL | Private working group AI Innovation AI-first initiative |
| #wg-sdg-hub | C0964K4RGFL | Private working group SDG Hub channel |
| #wg-training-hub | C097N4SSRQ8 | Private working group Training Hub channel |
| #ai-bu-models-2-data-pod | C09HP86M2DC | PMM/TMM/PM channel for Connecting Models to Data pillar |
| #proj-atos-de-skills-poc | C09UD69FGCW | Fine-tuning Atos initiative |
| #team-ai-tushar | C094SEKMBUY | Tushar's team channel |
| #wg-chatterbox-integrations-summit | C0AATE90HGC | Chatterbox SDG initiative |
| #random-samples | C088W6L5FPD | Kai's seminar series, research talks |

## Self-DM

| Channel | ID | Purpose |
|---|---|---|
| Self-DM (Luke Inglis) | D08EV8CBY04 | Direct messages to self |

## Special Channels

| Channel | ID | Purpose |
|---|---|---|
| #obsidian-luke | C0ASX58TJ4T | Two-way command channel (prep, notes, commands) |
| #obsidian-log | C0AT2KQAYQN | MCP server diagnostic logs (separate from conversation) |

## Adding a New Channel

1. In Slack, right-click the channel name > **Copy link**
2. The URL looks like: `https://redhat.enterprise.slack.com/archives/C088W6L5FPD`
3. The channel ID is the last segment (e.g., `C088W6L5FPD`)
4. Add a row to the **Tracked Channels** table above

## How It Works

Channel access is via the Slack MCP server (`mcp__slack__*` tools). No local database or scripts needed.

**Daily flow:**
1. `/prep-day` posts day header + meeting anchors to #obsidian-luke
2. `/slack-listener` polls the channel every 5 minutes for commands (todo, decision, note, meeting, search, jira)
3. `/close-day` reads meeting threads and ports notes back to the vault

**Direct tools:**
- **Channel history**: `mcp__slack__get_channel_history` or `mcp__slack__search_channel_messages`
- **Message search**: `mcp__slack__search_messages` for cross-channel search
- **Threads**: `mcp__slack__get_thread` for full thread context

## Setup

- MCP server registered in `~/.mcp.json` (runs via podman container)
- Tokens stored at `~/.local/share/slack-mcp/tokens.env` (600 perms)
- To refresh tokens: `python3 ~/slack-mcp/scripts/setup-slack-mcp.py --refresh-tokens`
