---
paths: ["02-Weekly/**"]
---

# Weekly Workflow

One file per week: `02-Weekly/YYYY-Www.md` from `Templates/weekly.md`. Dated subsections per weekday for free-form scratch.

**End-of-week summary** (Friday or on request): Read weekly note, write curated summary to `02-Weekly/_summaries/YYYY-Www-summary.md` (10-20 bullets: decisions, patterns, learnings, open loops). Flip `summarized: true` in original frontmatter. Then move the raw weekly note to `02-Weekly/_archive/`.

**Metrics capture** (part of EOW summary): Add a `metrics` block to the summary frontmatter and append a new row to `02-Weekly/_summaries/_trends.md` (both the charts data arrays and the Raw Data table). Metrics to capture:
- `meetings` -- count meeting note files created that week (glob `03-Meetings/*/YYYY-MM-DD-*.md` for dates in the week)
- `tasks_completed` -- count items in Todo.md Done section with completion dates in the week
- `open_loops` -- count items in the Open Loops section of the summary
- `decisions_logged` -- count new decision files created that week (glob `01-Components/*/decisions/YYYY-MM-DD-*.md`)
- `cc_sessions` -- sum sessions from usage dashboard data for dates in the week
- `cc_active_hours` -- sum active hours from usage dashboard data for dates in the week

Top-level `02-Weekly/` should only contain the current week's scratch pad. Past weeks live in `_archive/` after summarization.

For retrospective questions ("what did I work on in Q1?"), read summaries, not raw notes. If you need the raw scratch pad, check `_archive/`.
