#!/usr/bin/env bash
set -euo pipefail

VAULT="$HOME/Documents/work-vault"
TEMPLATE="$HOME/projects/work-vault-template"

if [ ! -d "$TEMPLATE/.git" ]; then
  echo "ERROR: Template repo not found at $TEMPLATE"
  echo "Clone it: git clone git@github.com:lukeinglis/work-vault.git $TEMPLATE"
  exit 1
fi

echo "Syncing vault scaffolding -> template repo..."

rsync -av --delete \
  "$VAULT/.claude/commands/" "$TEMPLATE/.claude/commands/"

rsync -av --delete \
  --exclude="jira-ecosystem.md" \
  --exclude="rfe-assessment.md" \
  "$VAULT/.claude/rules/" "$TEMPLATE/.claude/rules/"

rsync -av --delete \
  "$VAULT/Templates/" "$TEMPLATE/Templates/"

rsync -av --delete \
  --exclude="__pycache__/" \
  --exclude=".venv/" \
  --exclude="sheet_url.txt" \
  --exclude=".imported_ids.json" \
  --exclude="emails.csv" \
  "$VAULT/scripts/" "$TEMPLATE/scripts/"

if [ -d "$VAULT/docs/" ]; then
  rsync -av --delete \
    "$VAULT/docs/" "$TEMPLATE/docs/"
fi

cp "$VAULT/.claude/settings.json" "$TEMPLATE/.claude/settings.json"
cp "$VAULT/.gitignore" "$TEMPLATE/.gitignore"
cp "$VAULT/.mcp.json" "$TEMPLATE/.mcp.json"
cp "$VAULT/Automation.md" "$TEMPLATE/Automation.md"
cp "$VAULT/Commands.md" "$TEMPLATE/Commands.md"

for f in "$VAULT/.obsidian/app.json" \
         "$VAULT/.obsidian/community-plugins.json" \
         "$VAULT/.obsidian/plugins/periodic-notes/data.json" \
         "$VAULT/.obsidian/plugins/quickadd/data.json"; do
  if [ -f "$f" ]; then
    dest="$TEMPLATE/${f#$VAULT/}"
    mkdir -p "$(dirname "$dest")"
    cp "$f" "$dest"
  fi
done

echo "Sanitizing CLAUDE.md and Todo.md..."
python3 "$VAULT/scripts/sanitize-for-template.py"

echo ""
echo "--- Template repo status ---"
cd "$TEMPLATE"
git status --short

CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
  echo "No changes to sync."
  exit 0
fi

echo ""
echo "Changes detected. Review with: cd $TEMPLATE && git diff"
