---
paths: ["03-Meetings/**"]
---

# Meeting Workflow

Meetings in `03-Meetings/` by recurring series name, or `_one-off/` for non-recurring. Tag initiatives via frontmatter, not folder placement.

**Creating:** Use `Templates/meeting.md`. Fill what I give, leave placeholders. Filename: `YYYY-MM-DD-short-topic.md`.

**Transcript-driven notes** (when `transcript:` field points to `_transcripts/` file):
1. Read transcript as source of truth for `## Notes` and `## Action Items`
2. Extract decisions into `## Decisions`
3. Extract action items with owners into `## Action Items`
4. Add my action items to Todo.md with link back
5. Preserve `## Prep` if already filled
6. Write concise, bullet-based summary in my voice
