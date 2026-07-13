# Work Vault -- Claude Code Context

> System specification: see `SPEC.md` for the full domain model, workflow contracts, integration boundaries, and invariants.

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

For the full domain model, workflow contracts, integration boundaries, and component taxonomy, see `SPEC.md`.

## Component Disambiguation

- **Component 1** (primary): your main product area. Add disambiguation notes to avoid confusion with adjacent domains.
- **Component 2** (secondary): your secondary product area.
- **Component 3** (team-level): team management, research agenda, cross-cutting concerns.
- Components are permanent domains. Initiatives are time-bound projects within each component.
- Always ask for clarification before categorizing work into a component or initiative.

## Path-Scoped Rules

Context-specific rules are in `.claude/rules/` and load automatically when working on matching paths. See individual rule files for details.
