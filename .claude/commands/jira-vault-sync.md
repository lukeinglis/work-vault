Sync the work vault's initiative overviews with current Jira state.

## Steps

1. Execute ALL FOUR JQL queries below via the Jira MCP (`outputFormat: "json"`, `fields: "summary,status,issuetype,updated,assignee"`). State results after: "Component 1: N results, Component 2: N results, My RFEs: N results, My Strategy: N results."

   - **Component 1:** `project = {{JIRA_PROJECT_STRAT}} AND component = "{{COMPONENT_1}}" AND status not in (Closed) ORDER BY updated DESC`
   - **Component 2:** `project = {{JIRA_PROJECT_STRAT}} AND component in ("{{COMPONENT_2}}", "{{COMPONENT_3}}") AND status not in (Closed) ORDER BY updated DESC`
   - **My RFEs:** `project = {{JIRA_PROJECT_RFE}} AND assignee = currentUser() AND status not in (Closed) ORDER BY updated DESC`
   - **My Strategy:** `project = {{JIRA_PROJECT_STRAT}} AND (reporter = currentUser() OR watcher = currentUser()) AND status not in (Closed) ORDER BY updated DESC`

2. Read the current overview files:
   - `01-Components/{{COMPONENT_1_SLUG}}/_overview.md`
   - `01-Components/{{COMPONENT_2_SLUG}}/_overview.md`

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
