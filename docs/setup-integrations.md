# Integration Setup Guide

The vault's slash commands use `{{PLACEHOLDER}}` variables for personal configuration. This guide explains each placeholder and how to set it up.

## Quick Setup

Run this from the vault root to replace all placeholders at once. Fill in your values first:

```bash
# Set your values
GOOGLE_EMAIL="you@company.com"
SLACK_CHANNEL_ID="C0XXXXXXXXX"
SLACK_USER_ID="U0XXXXXXXXX"
SLACK_CHANNEL_NAME="my-vault-channel"
GITHUB_USERNAME="your-github-handle"

# Replace in all command files
find .claude/commands -name '*.md' -exec sed -i '' \
  -e "s/{{GOOGLE_EMAIL}}/$GOOGLE_EMAIL/g" \
  -e "s/{{SLACK_CHANNEL_ID}}/$SLACK_CHANNEL_ID/g" \
  -e "s/{{SLACK_USER_ID}}/$SLACK_USER_ID/g" \
  -e "s/{{SLACK_CHANNEL_NAME}}/$SLACK_CHANNEL_NAME/g" \
  -e "s/{{GITHUB_USERNAME}}/$GITHUB_USERNAME/g" \
  {} +
```

For Jira and repo-specific placeholders, see the sections below and edit the relevant command files directly.

## Placeholder Reference

### Google Workspace

| Placeholder | Used in | Description |
|-------------|---------|-------------|
| `{{GOOGLE_EMAIL}}` | prep-day, pull-emails | Your Google Workspace email for calendar and Gmail access |

**Setup:**
1. Your Google Workspace email (the one tied to your calendar and Gmail)
2. In Gmail, create a label called `z - Obsidian`
3. Set up a Gmail filter to auto-label emails you want pulled into the vault (e.g., meeting notes, action items)
4. The `/pull-emails` command searches for `label:z---obsidian` (three dashes, Gmail's internal format for `z - Obsidian`)

**MCP server:** See [mcp-setup.md](mcp-setup.md) for Google Workspace MCP configuration.

### Slack

| Placeholder | Used in | Description |
|-------------|---------|-------------|
| `{{SLACK_CHANNEL_ID}}` | pull-slack, slack-listener, prep-day, close-day | Channel ID for your vault command channel |
| `{{SLACK_USER_ID}}` | pull-slack | Your Slack user ID (for @mention notifications) |
| `{{SLACK_CHANNEL_NAME}}` | pull-slack, slack-listener, close-day | Channel name (without #) |
| `{{SLACK_TOKEN_REFRESH_CMD}}` | pull-slack, slack-listener | Command to refresh Slack tokens when auth fails |

**Setup:**

1. **Create a private Slack channel** for vault commands (e.g., `#vault-commands`). This is your two-way interface: Claude posts schedules and meeting anchors here, and you send commands from your phone.

2. **Find the channel ID:**
   - Open the channel in Slack
   - Click the channel name at the top
   - Scroll to the bottom of the "About" panel
   - Copy the Channel ID (starts with `C`)

3. **Find your user ID:**
   - Click your profile picture in Slack
   - Click "Profile"
   - Click the three dots (...) menu
   - "Copy member ID" (starts with `U`)

4. **Token refresh command:** This depends on how you set up Slack MCP auth. Replace `{{SLACK_TOKEN_REFRESH_CMD}}` with whatever command refreshes your Slack tokens (e.g., `python3 ~/my-slack-mcp/refresh.py`).

**MCP server:** See [mcp-setup.md](mcp-setup.md) for Slack MCP configuration.

### GitHub

| Placeholder | Used in | Description |
|-------------|---------|-------------|
| `{{GITHUB_USERNAME}}` | sync-sessions | Your GitHub username for PR and commit tracking |

**Setup:**
1. Replace `{{GITHUB_USERNAME}}` with your GitHub handle
2. In `.claude/commands/sync-sessions.md`, update the repo list to include the repos you want to track for daily commit activity:
   ```
   - `your-username/your-repo-1`
   - `your-org/project-repo`
   ```

### Jira (optional)

These placeholders appear in `jira-vault-sync.md`, `research.md`, `pull-slack.md`, and `prep-day.md`. Skip these if you don't use Jira.

| Placeholder | Description |
|-------------|-------------|
| `{{JIRA_PROJECT_STRAT}}` | Your strategy/execution Jira project key (e.g., `MYSTRAT`) |
| `{{JIRA_PROJECT_RFE}}` | Your RFE/feature request Jira project key (e.g., `MYRFE`) |
| `{{JIRA_PROJECT_ENG}}` | Your engineering Jira project key (e.g., `MYENG`) |
| `{{COMPONENT_1}}`, `{{COMPONENT_2}}`, `{{COMPONENT_3}}` | Jira component names matching your vault components |
| `{{COMPONENT_1_SLUG}}`, `{{COMPONENT_2_SLUG}}` | Kebab-case versions of component names (matching `01-Components/` folder names) |
| `{{YOUR_ORG}}` | Your GitHub org name (used in prep-day for repo checks) |
| `{{REPO_1}}`, `{{REPO_2}}`, `{{REPO_3}}`, `{{REPO_DOCS}}` | Specific repo names to monitor |

**Setup:**
1. Map your Jira projects to the three-tier hierarchy, or simplify to a single project if you don't have separate RFE/strategy/engineering projects
2. Update the JQL queries in `jira-vault-sync.md` to match your project structure
3. Update component names to match your `01-Components/` folders

**MCP server:** See [mcp-setup.md](mcp-setup.md) for Jira MCP configuration.

## Commands That Don't Need Configuration

These commands work out of the box with no placeholder setup:

- `/decision` - Log decisions from natural language
- `/research` (partially, works without Jira but needs Jira placeholders for alignment analysis)

## Verifying Your Setup

After replacing placeholders, verify no placeholders remain:

```bash
grep -rn '{{' .claude/commands/
```

If this returns results, you have placeholders that still need values.
