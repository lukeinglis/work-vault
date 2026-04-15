---
paths: ["Todo.md"]
---

# Task Management -- Todo.md

**Most important operational rule.** Todo.md is the shared workspace between me and you. Every task flows through it.

**Structure:** Four table sections: `This Week` (with Due column), `Next Up`, `Someday`, `Done (Last 7 Days)` (with Completed column). Tag with your initiative tags.

**Ownership values** (Owner column):
- `you` -- I own it
- `cc` -- You own it end-to-end
- `both` -- Collaborative

**This Week / Next Up format:** `| owner | task description | [[source-link]] | #tag | due-date |`
**Done format:** `| owner | task description | completed-date |`

**Rules:**
1. Every task links to its source (meeting note, inbox file, `_overview.md`). No orphan tasks.
2. When extracting meeting action items, append to Next Up with link back. Use `(you)`/`(cc)`/`(both)` as appropriate.
3. When I say "work on [task]", follow the link, read the source and connected files, surface context before starting.
4. When I complete a task, move to Done with completion date.

**When to propose vs. add directly:**
- **Propose** when you notice gaps (missing follow-ups, open loops, stale drafts)
- **Add directly** for clear operational extractions (meeting action items, weekly cleanup, archiving)

**Ownership & handoff:**
- Multi-session work you own: create a `(cc)` task for visibility
- When you finish a `(cc)` task, flip to `(both)` with "ready for your review." Never self-complete.
- Only I mark `(you)` tasks done. I give final sign-off on everything.

**Weekly cleanup (Fridays or on request):**
1. Walk `(you)` tasks -- ask which to roll forward
2. Report `(cc)` progress -- completed (awaiting review), in progress, blocked
3. Flag stale `(both)` tasks
4. Archive Done items older than 7 days to `99-Archive/completed-todos-YYYY.md`
5. Demote unfinished This Week to Next Up
6. Suggest promotions from Next Up to This Week
