# Factory Configuration

## Goal

Improve the work vault template's slash commands, automation scripts, templates, and documentation quality. The vault is an Obsidian-based knowledge management system with Claude Code slash commands, MCP integrations (Slack, Gmail, Google Calendar, Jira, Google Workspace), and Python automation scripts for daily workflows.

## Modifiable

- `scripts/`
- `skills/`
- `Templates/`
- `docs/`
- `eval/`
- `.claude/rules/`
- `.claude/settings.json`
- `CLAUDE.md`
- `SPEC.md`
- `factory.md`

## Guards

- Do NOT modify `.obsidian/` plugin configurations
- Do NOT modify user data files in `01-Components/` through `99-Archive/` (except `Templates/`)
- Do NOT modify `.factory/` internals (managed by the factory system)
- Do NOT send messages to Slack, Gmail, Google Chat, or any external channel

## Command

```
python eval/score.py
```

## Eval Threshold

0.5

## Smoke Test

```
python -c 'import ast; ast.parse(open("scripts/sanitize-for-template.py").read()); print("OK")'
```

## Target Branch

main
