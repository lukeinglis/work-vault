Log a decision quickly. Low friction -- accepts natural language and creates a properly structured decision record in the right location.

**Usage:** `/decision <description>`

Examples:
- `/decision Use GRPO over DPO for RL training because memory efficiency`
- `/decision ITS gateway will use Envoy ext-proc, not standalone proxy`
- `/decision Inbox subcategories: comms, field-intel, initiatives, releases, strategy, process, other`

## Steps

1. **Parse the input:**
   - Extract the core decision from the argument text
   - Identify the "what we chose" and "why" if provided (look for "because", "over", "instead of", "rather than")
   - If alternatives are mentioned (X over Y), capture both as options

2. **Determine the scope and location:**
   - Ask: does this decision apply to a specific initiative, a component, or the vault itself?
   - Use these signals to determine:
     - If the decision mentions ITS, its-hub, gateway, tool calling, Lightspeed, or inference-time scaling keywords: `01-Components/inference-time-scaling/decisions/`
     - If the decision mentions SDG, training-hub, fine-tuning, RL, GRPO, chatterbox keywords: `01-Components/fine-tuning/decisions/`
     - If the decision mentions AI Innovation, team, hiring, research, random samples, website keywords: `01-Components/ai-innovation/decisions/`
     - If the decision is about the vault itself (structure, tooling, conventions): `01-Components/ai-innovation/decisions/` (vault is part of AI Innovation)
   - If scope is ambiguous, **ask before creating**

3. **Generate the filename:**
   - Format: `YYYY-MM-DD-short-title.md` using today's date
   - Derive short-title from the decision (kebab-case, 3-5 words max)
   - Example: `2026-04-14-grpo-over-dpo.md`

4. **Create the decision file:**
   - Use `Templates/decision.md` as the base structure
   - Fill in:
     - `title:` -- concise decision title
     - `date:` -- today's date
     - `initiative:` -- the component slug (inference-time-scaling | fine-tuning | ai-innovation)
     - `status:` -- `accepted` (default, since we're logging decisions already made)
     - `tags:` -- `[decision, <initiative-tag>]`
     - `## Context` -- brief context from what was provided, or leave placeholder if minimal input
     - `## Options Considered` -- if "X over Y" was given, fill both options. Otherwise leave as placeholder
     - `## Decision` -- the core decision statement
     - `## Consequences` -- leave as placeholder unless obvious from context
   - Keep it concise. The user can flesh it out later.

5. **Add backlinks:**
   - If this session is working on a meeting note, spec draft, or initiative file, add a `[[decisions/YYYY-MM-DD-short-title]]` link to the Related or Scratch Pad section of that file
   - If a relevant `_overview.md` exists, do NOT modify it (too noisy for every decision)

6. **Report:**
   - Show the file path created
   - Show the one-line decision summary
   - If called interactively (not from `/pull-slack`): suggest "Want to flesh out the context or options?"
   - If called from `/pull-slack`: just report the file path and summary, no prompt
