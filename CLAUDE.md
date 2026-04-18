# Work Vault -- Claude Code Context

## Style & Voice (Applies to Everything)
- Write in my voice: concise, bullet-heavy, no fluff, no hedging, no emdashes
- Don't over-format. Headers and bold only where they add clarity
- When uncertain about routing or structure, ask before creating files

## What This Vault Is

A work vault -- both thinking space and source of truth. Only tickets live in your project tracker; everything else (strategy, research, decisions, meeting notes, project thinking) is owned here and authoritative.

Customize the `01-Components/` folder to match your product areas. Each component is a permanent domain; initiatives are time-bound projects within each component.


## Vault Structure

| Path | Purpose |
|------|---------|
| `Home.md` | Dashboard (Dataview-powered, auto-updating) |
| `Todo.md` | **Single source of truth for all tasks** |
| `01-Components/<component>/` | `_overview.md`, `research/`, `decisions/`, `initiatives/` |
| `01-Components/<component>/initiatives/<initiative>/` | `spec-drafts/`, `decisions/` |
| `02-Weekly/` | Weekly scratch pads (`YYYY-Www.md`), `_summaries/` for curated EOW summaries |
| `03-Meetings/<recurring-meeting>/` | Notes for each recurring meeting series, `_transcripts/` inside |
| `03-Meetings/_one-off/` | Non-recurring meetings, `_transcripts/` inside |
| `04-Inbox/` | Quick capture -- triage to real homes |
| `05-People/` | Stakeholder reference |
| `06-Presentations/` | Slide decks and presentation materials |
| `07-Usage/` | Claude Code session logs (`sessions/`), `_dashboard.md`, `_insights_cache.json` |
| `99-Archive/` | Shipped/killed work, completed todos by year |
| `Templates/` | Templates for every note type |

## Conventions
- Meeting notes: `YYYY-MM-DD-short-topic.md`
- Weekly notes: `YYYY-Www.md`
- Everything else: kebab-case
- Every note has YAML frontmatter (minimum: `title`, `created`, `tags`). See `Templates/` for shapes.
- Use `[[wikilinks]]` liberally. Meeting notes tag initiatives via `initiatives:` frontmatter.
- Initiative status values: `active`, `paused`, `shipped`, `archived`

## Editing Principles
- When editing tickets, descriptions, or customer-facing content: make minimal, targeted changes. Do NOT rewrite or reframe beyond what's requested. Preserve the original author's voice and intent.

## Code Changes
- Always sanitize for edge cases like Infinity, NaN, null, and division by zero in frontend code.
- When implementing ranking/scoring logic, confirm tie-handling rules before coding.
- After making changes, verify the fix addresses the actual root cause -- don't assume the first hypothesis is correct.

## Path-Scoped Rules

Context-specific rules are in `.claude/rules/` and load automatically when working on matching paths:
- `todo-management.md` -- Todo.md ownership, handoff, weekly cleanup rules
- `meeting-workflow.md` -- Meeting creation, transcript processing, action item extraction
- `weekly-workflow.md` -- Weekly note and EOW summary workflow
- `inbox-triage.md` -- Inbox processing and routing
- `components-research.md` -- Context loading, spec drafting, decision logging
