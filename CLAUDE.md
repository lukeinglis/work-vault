# Work Vault -- Claude Code Context

## CRITICAL: Never Post on My Behalf
- NEVER send messages to Slack, Gmail, Google Chat, or any external channel directly. This includes post_message, send_dm, send_gmail_message, and any similar tools.
- Always draft the content and present it for me to copy/send myself.
- This is non-negotiable and applies to all contexts.

## Style & Voice (Applies to Everything)
- Write in my voice: concise, bullet-heavy, no fluff, no hedging
- No emdashes or double-dashes (--) in any output. Use commas, periods, or colons instead.
- Don't over-format. Headers and bold only where they add clarity
- When uncertain about routing or structure, ask before creating files
- When editing tickets, descriptions, or customer-facing content: minimal, targeted changes. Preserve the original author's voice and intent.

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
| `02-Weekly/` | Current week's scratch pad (`YYYY-Www.md`), `_summaries/` for EOW summaries, `_archive/` for past weeks |
| `03-Meetings/<recurring-meeting>/` | Notes for each recurring meeting series, `_transcripts/` inside |
| `03-Meetings/_one-off/` | Non-recurring meetings, `_transcripts/` inside |
| `04-Inbox/` | Quick capture -- triage to real homes |
| `05-People/` | Stakeholder reference |
| `06-Presentations/` | Slide decks by initiative (its/, fine-tuning/, red-hat-ai/, cross-initiative/) |
| `07-Usage/` | Claude Code session logs (`sessions/`), `_dashboard.md`, `_insights_cache.json` |
| `99-Archive/` | Shipped/killed work, completed todos by year |
| `Templates/` | Templates for every note type |
| `scripts/` | Automation: email-pull, slack-pull, sync-template, sanitize utilities |

## Conventions
- Meeting notes: `YYYY-MM-DD-short-topic.md`
- Weekly notes: `YYYY-Www.md`
- Everything else: kebab-case
- Every note has YAML frontmatter (minimum: `title`, `created`, `tags`). See `Templates/` for shapes.
- Use `[[wikilinks]]` liberally. Meeting notes tag initiatives via `initiatives:` frontmatter.
- Initiative status values: `active`, `paused`, `shipped`, `archived`

## Skill Execution Protocol

- **Sub-skill invocation:** When a skill says "Run `/skill-name`" or "Invoke `/skill-name`", use the Skill tool. Never inline a sub-skill's logic. The sub-skill's .md file defines its complete behavior.
- **Pagination:** Any API call that returns a `next_page_token`, `nextPageToken`, or `page_token` MUST be repeated with that token until no token is returned. Never process only the first page.
- **List completeness:** When processing a list of N items (emails, messages, meetings, tickets), process all N. State the count before starting ("Found N items") so gaps are visible.
- **Source enumeration for summaries:** Before writing any summary (day summary, weekly summary, meeting notes), list all sources by path and count. "Reading: N meeting notes [paths], M sessions." Read all listed sources before writing.

## Path-Scoped Rules

Context-specific rules are in `.claude/rules/` and load automatically when working on matching paths:
- `todo-management.md` -- Todo.md ownership, handoff, weekly cleanup rules
- `meeting-workflow.md` -- Meeting creation, transcript processing, action item extraction
- `weekly-workflow.md` -- Weekly note and EOW summary workflow
- `inbox-triage.md` -- Inbox processing and routing
- `components-research.md` -- Context loading, spec drafting, decision logging
