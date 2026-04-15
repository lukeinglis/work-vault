Sync the work vault's initiative overviews with current Jira state.

**Usage:** `/jira-vault-sync`

## Prerequisites
- Jira MCP server configured (see `docs/mcp-setup.md`)
- Initiative `_overview.md` files with Jira links in their Key Links section

## Steps

1. **Read initiative overviews** from `01-Components/*/initiatives/*/_overview.md`
   - Extract Jira epic/feature keys from the Key Links section

2. **Run JQL queries** via Jira MCP to get current state of tracked tickets
   - Query by project, component, or specific keys depending on your setup

3. **Compare Jira results** against what's in the overview files:
   - New tickets not yet in the overview
   - Status changes (e.g., ticket moved to Done)
   - Closed/resolved tickets

4. **Present sync report** showing:
   - New tickets to add
   - Status changes to update
   - Tickets that may need archiving

5. **Ask for confirmation** before making any updates

6. **Update overview files**:
   - Preserve all hand-written content
   - Only update Jira-related tables and status bullets
   - Add new tickets to the appropriate section
