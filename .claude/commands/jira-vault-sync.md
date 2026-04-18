Sync the work vault's initiative overviews with current Jira state.

## Steps

1. Run these JQL queries via the Jira MCP (`outputFormat: "json"`, `fields: "summary,status,issuetype,updated,assignee"`):

   - **ITS:** `project = RHAISTRAT AND component = "Inference-Time Techniques" AND status not in (Closed) ORDER BY updated DESC`
   - **Fine-Tuning:** `project = RHAISTRAT AND component in ("SDG", "Training Hub", "Fine Tuning") AND status not in (Closed) ORDER BY updated DESC`
   - **My RFEs:** `project = RHAIRFE AND assignee = currentUser() AND status not in (Closed) ORDER BY updated DESC`
   - **My RHAISTRAT:** `project = RHAISTRAT AND (reporter = currentUser() OR watcher = currentUser()) AND status not in (Closed) ORDER BY updated DESC`

2. Read the current overview files:
   - `01-Components/inference-time-scaling/_overview.md`
   - `01-Components/fine-tuning/_overview.md`

3. Compare Jira results against the overviews and report:
   - **New tickets** not yet in the overview
   - **Status changes** (e.g., New -> In Progress, In Progress -> Review)
   - **Newly closed tickets** that should be noted

4. Present a sync report:

```
## Jira Vault Sync Report — YYYY-MM-DD

### Inference-Time Scaling
- No changes / N changes found
  - [list changes]

### Fine-Tuning
- No changes / N changes found
  - [list changes]

### My RFEs
- No changes / N changes found
  - [list changes]
```

5. Ask for confirmation before updating the overview files.

6. When updating, **preserve all hand-written content** (summary, goals, blockers, open questions, stakeholders, timeline) — only update the Jira tables and the "What's Happening Now" bullet points.

7. Update the `updated:` field in the frontmatter to today's date.
