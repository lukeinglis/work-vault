#!/usr/bin/env python3
"""Verify that no org-specific patterns remain in sanitized template files."""

import re
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent

BANNED_PATTERNS = [
    r"linglis@redhat\.com",
    r"RHAISTRAT",
    r"RHAIRFE",
    r"RHAIENG",
    r"Red-Hat-AI-Innovation-Team",
    r"Red Hat",
    r"sdg_hub_luke",
    r"its_hub_demo",
    r"\bits_hub\b",
    r"\bsdg_hub\b",
    r"\btraining_hub\b",
    r"C0ASX58TJ4T",
    r"U08EC765D0X",
    r"obsidian-luke",
    r"lukeinglis",
]

SANITIZED_FILES = [
    "Commands.md",
    "Automation.md",
    "CLAUDE.md",
    "Todo.md",
    "Home.md",
    ".claude/commands/research.md",
    ".claude/commands/prep-day.md",
    ".claude/commands/sync-sessions.md",
    ".claude/commands/pull-slack.md",
    ".claude/commands/jira-vault-sync.md",
    "scripts/email-pull/gemini_docs.py",
    "scripts/email-pull/gmail_label.py",
    "scripts/slack-pull/Slack Channels.md",
]

EXCLUDE_FILES = {
    "scripts/sanitize-for-template.py",
    "scripts/test_sanitize.py",
}


def test_no_org_patterns():
    target_files = []
    for rel in SANITIZED_FILES:
        f = TEMPLATE / rel
        if f.exists():
            target_files.append(f)

    cmd_dir = TEMPLATE / ".claude" / "commands"
    if cmd_dir.exists():
        for f in cmd_dir.glob("*.md"):
            if f not in target_files:
                target_files.append(f)

    combined = re.compile("|".join(BANNED_PATTERNS))
    failures = []

    for fpath in target_files:
        rel = str(fpath.relative_to(TEMPLATE))
        if rel in EXCLUDE_FILES:
            continue
        content = fpath.read_text()
        for i, line in enumerate(content.splitlines(), 1):
            if combined.search(line):
                failures.append(f"  {rel}:{i}: {line.strip()}")

    if failures:
        print(f"FAIL: {len(failures)} org-specific pattern(s) found:")
        for f in failures:
            print(f)
        return False

    print(f"PASS: checked {len(target_files)} files, no org-specific patterns found")
    return True


if __name__ == "__main__":
    success = test_no_org_patterns()
    sys.exit(0 if success else 1)
