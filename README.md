# Work Vault

Your PM knowledge is scattered across Slack threads, email chains, Google Docs, Jira tickets, and your head. When someone asks "why did we decide that?" or "what did we agree to in that meeting?", the answer is buried somewhere -- or lost entirely.

This vault puts everything in one place. Strategy, research, decisions, meeting notes, and roadmap thinking all live here as plain markdown files, powered by [Obsidian](https://obsidian.md/) for linking and visualization and [Claude Code](https://claude.ai/code) for automation and AI assistance.

<!-- TODO: Add screenshots of Home dashboard, filled meeting note, and Kanban board -->

## What You Get

**A structured vault** with folders for components, initiatives, meetings, weekly notes, people, and a triage inbox.

**Claude Code integration** that turns the vault into an interactive system:
- `/prep-day` -- fetches your calendar, creates meeting note shells, posts the schedule to Slack
- `/close-day` -- pulls emails, merges AI meeting summaries, ports notes to the right files, summarizes the day
- `/decision` -- log decisions from natural language ("we chose X over Y because Z")
- `/pull-slack` -- two-way Slack integration for capturing todos, notes, and commands from your phone
- `/research` -- deep competitive/landscape research that saves structured briefs
- `/jira-vault-sync` -- keeps initiative overviews in sync with Jira ticket state

**Templates** for every note type: meetings, decisions, specs, research, one-pagers, weekly scratch pads, initiative overviews, and more.

**A shared task system** (`Todo.md`) where you and Claude Code collaborate on tasks with clear ownership and handoff rules.

See [docs/examples/](docs/examples/) for what these look like filled in.

## Prerequisites

**Core:**
- [Obsidian](https://obsidian.md/) (free)
- [Claude Code](https://claude.ai/code) (requires Anthropic API access)

**For MCP integrations (optional):**
- Node.js 18+ (for MCP servers)
- [uv](https://docs.astral.sh/uv/) (Python package runner, for Jira and Google MCP servers)
- Python 3.10+ (only if using the fallback email scripts)

## Quick Start

### 1. Clone and Open in Obsidian

```bash
git clone https://github.com/lukeinglis/work-vault.git
cd work-vault
```

Open the `work-vault` folder as a vault in Obsidian. It will prompt you to trust the plugins -- accept to enable Dataview, Kanban, Templater, and other community plugins.

### 2. Customize Your Components

The vault ships with `01-Components/example-component/`. Rename and duplicate this for your product areas:

```
01-Components/
  payments/
    _overview.md
    decisions/
    initiatives/
    research/
    spec-drafts/
  onboarding/
    _overview.md
    ...
```

Each component gets an `_overview.md` (use `Templates/initiative-overview.md`). Initiatives are time-bound projects within a component.

### 3. Set Up MCP Servers (Optional but Recommended)

MCP servers connect Claude Code to external services. See [docs/mcp-setup.md](docs/mcp-setup.md) for detailed setup instructions for:

- **Jira** -- ticket sync and lookups
- **Slack** -- two-way command channel
- **Google Workspace** -- calendar, email, docs
- **Browser** -- web research (already configured in `.mcp.json`)

### 4. Start Using Claude Code

Open Claude Code in the vault directory and try:

```bash
cd work-vault
claude
```

Then:
- "Create a weekly note for this week"
- "What's in my inbox?"
- "Log a decision that we chose Postgres over DynamoDB because we need complex queries"
- `/prep-day` (if calendar MCP is configured)

## Getting Started: Week by Week

Don't try to set up everything at once. Ramp gradually:

**Week 1: Foundation**
- Set up your components in `01-Components/`
- Use `Todo.md` as your task list -- ask Claude Code to add and manage tasks
- Create meeting notes from `Templates/meeting.md` (manually or ask Claude Code)
- Capture stray thoughts to `04-Inbox/` and triage them with "process my inbox"

**Week 2: Daily rhythm**
- Set up the Google Workspace MCP server ([docs/mcp-setup.md](docs/mcp-setup.md))
- Start using `/prep-day` each morning and `/close-day` each evening
- Use `/decision` whenever a decision surfaces -- build the habit

**Week 3: Full integration**
- Set up the Slack MCP server and create your command channel
- Start using `/slack-listener` for mobile capture throughout the day
- Set up Jira MCP and try `/jira-vault-sync`
- Explore `/research` for competitive landscape briefs

**Ongoing:**
- Friday weekly cleanup becomes automatic (part of `/close-day`)
- Decision records accumulate -- start referencing them ("why did we choose X?")
- Weekly summaries build a searchable history of your work

## Vault Structure

```
work-vault/
  Home.md                  -- Dashboard (Dataview-powered)
  Todo.md                  -- Shared task list (you + Claude Code)
  Initiatives Board.md     -- Kanban board of all initiatives
  Commands.md              -- Reference for all slash commands
  Automation.md            -- Reference for all automation
  CLAUDE.md                -- Claude Code context and rules
  
  01-Components/           -- Product areas (permanent domains)
    example-component/
      _overview.md         -- Component overview and status
      decisions/           -- Decision records
      initiatives/         -- Time-bound projects
      research/            -- Research briefs
      spec-drafts/         -- Draft specs before shipping to Jira
  
  02-Weekly/               -- Weekly scratch pads
    _summaries/            -- Curated end-of-week summaries
  
  03-Meetings/             -- Meeting notes by recurring series
    _one-off/              -- Non-recurring meetings
      _transcripts/        -- AI transcripts
  
  04-Inbox/                -- Quick capture, triage later
    intake/                -- New items awaiting routing
  
  05-People/               -- Stakeholder reference
  06-Presentations/        -- Slide decks and materials
  07-Usage/                -- Claude Code session logs
  99-Archive/              -- Shipped/killed work
  
  Templates/               -- Templates for every note type
  scripts/                 -- Automation scripts
  docs/                    -- Setup guides and examples
  
  .claude/
    commands/              -- Slash command definitions
    rules/                 -- Path-scoped behavior rules
    settings.json          -- Claude Code project settings
  
  .obsidian/               -- Obsidian config and plugins
  .mcp.json                -- Project-level MCP server config
```

## Daily Workflow

A typical day looks like:

1. **Morning:** `/prep-day` -- creates meeting notes, posts schedule to Slack
2. **Start listening:** `/slack-listener` -- polls your Slack command channel every 5 minutes
3. **During the day:** Send commands from Slack (`todo: follow up on X`, `decision: chose Y because Z`)
4. **Between meetings:** Work on tasks from Todo.md, draft specs, log decisions
5. **End of day:** `/close-day` -- pulls emails, merges notes, summarizes, preps tomorrow

## Obsidian Plugins

The vault uses these community plugins (installed automatically when you open in Obsidian):

| Plugin | Purpose |
|--------|---------|
| **Dataview** | Powers the Home dashboard and dynamic queries |
| **Templater** | Template engine for creating notes |
| **Periodic Notes** | Auto-creates weekly notes |
| **QuickAdd** | Quick capture to inbox, todo, or scratch pad ([see shortcuts](docs/quickadd-shortcuts.md)) |
| **Kanban** | Visual initiative board |
| **Tasks** | Task rendering and queries |
| **Excalidraw** | Diagrams and sketches |
| **Terminal** | Run commands from within Obsidian |
| **Charts View** | Data visualization |
| **Meta Bind** | Interactive frontmatter widgets |

## Customization

### Adding a new component
1. Copy `01-Components/example-component/` to `01-Components/your-component/`
2. Edit `_overview.md` with your component details
3. It will automatically appear on the Home dashboard

### Adding a recurring meeting
1. Create a folder: `03-Meetings/your-meeting-name/`
2. Create a `_transcripts/` subfolder inside it
3. Meeting notes go in the folder, transcripts in `_transcripts/`

### Customizing the task system
Edit `.claude/rules/todo-management.md` to change ownership rules, table format, or cleanup behavior.

### Adding slash commands
Create a new `.md` file in `.claude/commands/`. The filename becomes the command name. Write the instructions for what Claude Code should do.

## Docs

| Doc | What's in it |
|-----|-------------|
| [Philosophy](docs/philosophy.md) | Why the vault is structured this way -- components vs. initiatives, the inbox pattern, decision logging, and the shared task system |
| [MCP Setup](docs/mcp-setup.md) | Step-by-step setup for Jira, Slack, Google Workspace, and Browser MCP servers |
| [QuickAdd Shortcuts](docs/quickadd-shortcuts.md) | The three pre-configured Obsidian capture shortcuts and how to customize them |
| [Examples](docs/examples/) | Filled-in examples of a meeting note, decision record, weekly scratch pad, and Todo.md |

## FAQ

**Do I need all the MCP servers?**
No. The vault works without any MCP servers -- you just won't have the automated calendar/email/Slack/Jira integrations. Add them incrementally as needed.

**Can I use this with a different AI tool?**
The vault structure, templates, and Obsidian plugins work independently. The `.claude/` directory (commands, rules) and `CLAUDE.md` are specific to Claude Code.

**How do I share this with my team?**
Each person clones the repo, customizes their components, and sets up their own MCP servers with their own credentials. The vault structure is shared; the content is personal.

**Where do credentials go?**
Never in the repo. MCP credentials go in `~/.mcp.json` (global, gitignored by default). The vault's `.mcp.json` only has credential-free configs like Browser MCP.

**Why not just use Notion / Confluence / [other tool]?**
See [docs/philosophy.md](docs/philosophy.md) -- the short answer is: local-first, plain markdown, no lock-in, and AI-native workflows that those tools can't match.

## License

[MIT](LICENSE)
