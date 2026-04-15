Log a decision quickly. Low friction -- accepts natural language and creates a properly structured decision record.

**Usage:** `/decision we chose X over Y because Z`

## Steps

1. **Parse the input** to extract:
   - What we chose
   - What alternatives existed (if mentioned)
   - Why (the reasoning)

2. **Determine scope** -- which component or initiative does this decision belong to?
   - Ask if ambiguous
   - Component-wide decisions go to `01-Components/<component>/decisions/`
   - Initiative-specific decisions go to `01-Components/<component>/initiatives/<initiative>/decisions/`

3. **Generate filename:** `YYYY-MM-DD-short-title.md`

4. **Create decision file** from `Templates/decision.md` with:
   - Context section (what forced the decision)
   - Options considered (if provided)
   - Decision and rationale
   - Consequences (what changes because of this)

5. **Add backlinks** to related files (initiative overview, meeting notes, specs)

6. **Report** the file path created
