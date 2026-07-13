# QuickAdd Shortcuts

The vault ships with three [QuickAdd](https://github.com/chhoumann/quickadd) capture shortcuts pre-configured. These let you capture thoughts without leaving your current note in Obsidian.

## How to Use

Open the command palette in Obsidian (`Cmd+P` / `Ctrl+P`) and type "QuickAdd" to see the available shortcuts. You can also assign hotkeys to any of them via Settings > Hotkeys.

## Available Shortcuts

### 1. Capture to Inbox

**What it does:** Creates a new file in `04-Inbox/intake/` with today's date and your text as the title.

**When to use:** Quick capture of anything -- a thought, a link someone shared, something from a meeting. Don't worry about where it belongs; triage it later with Claude Code ("process my inbox").

**Output:** `04-Inbox/intake/2026-03-18-quick-capture.md` with inbox frontmatter.

### 2. Add Action Item to Next Up

**What it does:** Appends a row to the `## Next Up` table in `Todo.md` with you as the owner.

**When to use:** When you think of a task during a meeting or while reading. Captures it to the right place without switching files.

**Output:** A new row in Todo.md: `| you | your text here |  |  |`

Note: The task won't have a source link or tag -- fill those in later during your next Todo.md review, or ask Claude Code to clean up orphan tasks.

### 3. Quick Scratch Note

**What it does:** Appends a bullet to the current week's scratch pad (`02-Weekly/YYYY-Www.md`).

**When to use:** Stream-of-consciousness note-taking during the day. Just dump the thought; the weekly note is your scratch space.

**Output:** A new bullet appended to the current weekly note.

Note: The weekly note must already exist. If it doesn't, create one first using the Periodic Notes plugin (it auto-creates on the weekly cadence) or manually from `Templates/weekly-periodic.md`.

## Customization

QuickAdd config lives in `.obsidian/plugins/quickadd/data.json`. You can:

- **Add new shortcuts** for capture patterns you repeat often
- **Change the capture format** (e.g., add a timestamp prefix)
- **Change the target file** (e.g., capture to a different section of Todo.md)
- **Add macros** for multi-step workflows (e.g., create a meeting note AND add a task)

See the [QuickAdd docs](https://quickadd.obsidian.guide/) for the full configuration reference.
