---
paths: ["01-Components/**"]
---

# Component & Initiative Context Loading

When I reference a component, **read its `_overview.md` first**. For deeper questions, also read `research/`, `decisions/`, and relevant initiative folders.

When I reference a specific initiative, read the component `_overview.md` plus the initiative's `spec-drafts/` and `decisions/`.

## Spec Drafting

1. I dump rough ideas into `01-Components/<component>/initiatives/<initiative>/spec-drafts/`
2. We iterate -- you sharpen the problem, think through edge cases
3. **Proactively read** `_overview.md`, `research/`, `decisions/`, and tagged meeting notes before offering spec feedback
4. Once ready, I ship to Jira. Draft stays as thinking record.

## Decision Logging

Two levels of decisions:
- **Component-wide:** `01-Components/<component>/decisions/` -- cross-cutting decisions for the domain
- **Initiative-specific:** `01-Components/<component>/initiatives/<initiative>/decisions/` -- scoped to one initiative

Use `Templates/decision.md`. Low friction -- I say "log a decision that X over Y because Z" and you create it.

Filename: `YYYY-MM-DD-short-title.md`. When I ask "why did we decide X?", search `decisions/` first (both levels). Offer to log decisions whenever one surfaces -- this is a habit I'm building.
