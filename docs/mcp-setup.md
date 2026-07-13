# MCP Server Setup Guide

This vault uses [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers to connect Claude Code to external services. MCP servers run locally and give Claude Code access to APIs like Jira, Slack, Google Workspace, and browser automation.

## Overview

| MCP Server | Purpose | Required For |
|------------|---------|-------------|
| **Jira** | Read/write Jira tickets | `/jira-vault-sync`, Jira lookups |
| **Slack** | Read/post Slack messages | `/prep-day`, `/pull-slack`, `/close-day` |
| **Google Workspace** | Gmail, Calendar, Drive, Docs | `/pull-emails`, `/prep-day`, `/close-day` |
| **Browser MCP** | Browser automation | Web research, screenshots |

You don't need all of them. Start with what you use, add more later.

## Configuration Files

MCP servers are configured in JSON files:

- **`~/.mcp.json`** -- Global config (available to Claude Code in any directory)
- **`.mcp.json`** (vault root) -- Project-level config (only available in this vault)

The vault ships with Browser MCP in `.mcp.json`. Add others to `~/.mcp.json` so they're available everywhere.

## 1. Jira MCP Server

Connects Claude Code to your Jira instance for reading/writing tickets.

### Install

```bash
# Uses uvx (Python) -- install uv first if needed: https://docs.astral.sh/uv/
uvx mcp-atlassian --help
```

### Configure

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "jira": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-org.atlassian.net",
        "JIRA_USERNAME": "your-email@company.com",
        "JIRA_API_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

### Get Your API Token

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a label (e.g., "Claude Code")
4. Copy the token into `JIRA_API_TOKEN`

### Verify

```bash
# In Claude Code, try:
# "Look up PROJ-123 in Jira"
```

### Notes
- Some enterprise Jira instances (e.g., with SSO) may not support direct API tokens. The MCP server package handles auth differently than raw curl.
- If you get 401 errors, check if your org requires a different auth flow.

---

## 2. Slack MCP Server

Connects Claude Code to Slack for reading channels and posting messages.

### Option A: Official Slack MCP (Recommended)

The official Slack MCP server from Anthropic:

```bash
npm install -g @anthropic-ai/mcp-server-slack
```

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-YOUR-BOT-TOKEN",
        "SLACK_USER_TOKEN": "xoxp-YOUR-USER-TOKEN"
      }
    }
  }
}
```

### Option B: Container-Based (For Enterprise/Custom Auth)

If your Slack workspace requires special auth handling:

1. Clone or build a container-based MCP server
2. Create a wrapper script (e.g., `~/.local/share/slack-mcp/run-slack-mcp.sh`)
3. Reference the script in your config:

```json
{
  "mcpServers": {
    "slack": {
      "command": "/path/to/your/run-slack-mcp.sh"
    }
  }
}
```

### Getting Slack Tokens

**Bot Token (xoxb-):**
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app (or use existing)
3. Under **OAuth & Permissions**, add scopes:
   - `channels:history`, `channels:read`, `chat:write`, `reactions:write`
   - `search:read`, `users:read`
4. Install the app to your workspace
5. Copy the **Bot User OAuth Token**

**User Token (xoxp-):**
- Same app, under **OAuth & Permissions**, copy the **User OAuth Token**
- Needed for: search, reading channels the bot isn't in

### Setting Up Your Command Channel

1. Create a private Slack channel (e.g., `#obsidian-yourname`)
2. Invite your bot to the channel
3. Get the channel ID: right-click channel name > Copy Link > last segment of URL
4. Update `.claude/commands/pull-slack.md` with your channel ID

---

## 3. Google Workspace MCP Server

Connects Claude Code to Gmail, Google Calendar, Drive, and Docs.

### Install

```bash
uvx workspace-mcp --help
```

### Configure

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tool-tier", "core"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "GOCSPX-YOUR_CLIENT_SECRET"
      }
    }
  }
}
```

### Getting Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable these APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Docs API
   - Apps Script API
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth client ID**
6. Application type: **Desktop app**
7. Copy the Client ID and Client Secret

### First Run Auth

On first use, the MCP server will open a browser window for OAuth consent. Authorize the requested permissions. The token is cached locally after that.

### Gmail Label Setup

For the `/pull-emails` flow:
1. In Gmail, create a label called `z - Obsidian` (or your preferred name)
2. Label emails you want to capture into the vault
3. The `/pull-emails` command reads labeled emails and removes the label after import

---

## 4. Browser MCP Server

Already configured in the vault's `.mcp.json`. Gives Claude Code the ability to navigate web pages, take screenshots, and interact with browser elements.

### How It Works

```json
{
  "mcpServers": {
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    }
  }
}
```

No additional setup needed. It launches a headless browser on demand.

---

## Enabling MCP Servers in Claude Code

After configuring `~/.mcp.json`, you need to enable the servers in Claude Code:

1. **Project-level servers** (`.mcp.json` in vault root) are enabled per-project in `.claude/settings.local.json`:

```json
{
  "enableAllProjectMcpServers": true
}
```

2. **Global servers** (`~/.mcp.json`) are available automatically but may need permission grants. Claude Code will prompt you the first time a tool is used.

3. **Check server status** in Claude Code:
   - Type `/mcp` to see connected MCP servers and their status

---

## Troubleshooting

### Server won't start
- Check that the command exists: `which uvx`, `which npx`
- Try running the command manually to see error output
- Check `~/.mcp.json` for JSON syntax errors

### Authentication failures
- Jira: Verify API token is valid, check if your org blocks API access
- Slack: Verify bot is invited to the channels you're reading
- Google: Re-run OAuth flow by deleting cached tokens (location varies by package)

### Permissions
- Claude Code will prompt for permission the first time each MCP tool is used
- Grant permissions individually or use `.claude/settings.local.json` to pre-allow tools
- Example pre-allow in `settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__jira__jira_search",
      "mcp__jira__jira_get_issue",
      "mcp__slack__get_channel_history",
      "mcp__slack__post_message",
      "mcp__google-workspace__get_events",
      "mcp__google-workspace__search_gmail_messages"
    ]
  }
}
```

### Testing a server
In Claude Code, try a simple read operation:
- Jira: "Look up PROJ-123"
- Slack: "What channels am I in on Slack?"
- Google: "What meetings do I have today?"
- Browser: "Take a screenshot of google.com"
