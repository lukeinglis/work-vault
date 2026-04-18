#!/usr/bin/env python3
"""
Sanitize live vault files into generic template versions.
Preserves structural improvements while stripping personal content.
"""

import re
from pathlib import Path

VAULT = Path.home() / "Documents" / "work-vault"
TEMPLATE = Path.home() / "projects" / "work-vault-template"


def sanitize_claude_md():
    src = (VAULT / "CLAUDE.md").read_text()

    src = re.sub(
        r"My Product Management vault.*?I work deeply on a few things, not broadly on many\.",
        "A work vault -- both thinking space and source of truth. "
        "Only tickets live in your project tracker; everything else "
        "(strategy, research, decisions, meeting notes, project thinking) "
        "is owned here and authoritative.\n\n"
        "Customize the `01-Components/` folder to match your product areas. "
        "Each component is a permanent domain; initiatives are time-bound "
        "projects within each component.",
        src,
        flags=re.DOTALL,
    )

    src = re.sub(
        r"## Component Taxonomy\n.*?(?=\n## )",
        "",
        src,
        flags=re.DOTALL,
    )

    src = src.replace(
        "When editing Jira tickets, descriptions,",
        "When editing tickets, descriptions,",
    )

    src = re.sub(r"- `rfe-assessment\.md`.*\n", "", src)
    src = re.sub(r"- `jira-ecosystem\.md`.*\n", "", src)

    if "06-Presentations" not in src:
        src = src.replace(
            "| `05-People/` | Stakeholder reference |",
            "| `05-People/` | Stakeholder reference |\n"
            "| `06-Presentations/` | Slide decks and presentation materials |",
        )

    (TEMPLATE / "CLAUDE.md").write_text(src)
    print("  CLAUDE.md sanitized")


def sanitize_todo_md():
    src = (VAULT / "Todo.md").read_text()

    src = re.sub(r"updated: \d{4}-\d{2}-\d{2}", "updated: ", src)

    src = re.sub(
        r"> Shared task list between me \(human\) and Claude Code\.",
        "This is the shared task list between you and Claude Code.",
        src,
    )
    src = re.sub(
        r"Every task links to the source.*\n>",
        "See `.claude/rules/todo-management.md` for the full protocol.\n",
        src,
    )

    src = re.sub(
        r"> \*\*Ownership:\*\*.*",
        "**Owner legend:** `you` = you own it | `cc` = Claude Code owns it end-to-end | `both` = collaborative",
        src,
    )

    src = re.sub(r"> \*\*Tags:\*\*.*\n", "", src)

    src = re.sub(r"> \*\*Priority buckets:\*\*", "**Priority buckets:**", src)
    src = re.sub(r"> \*\*IDs:\*\*", "**IDs:**", src)

    lines = src.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("| -"):
            result.append(line)
            result.append(lines[i + 1])
            cols = len(line.split("|")) - 2
            empty = "| " + " | ".join(["     "] * cols) + " |"
            result.append(empty)
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
            continue

        result.append(line)
        i += 1

    src = "\n".join(result)
    # Replace Done section with example entries
    src = re.sub(
        r"(## Done \(Last 7 Days\)\n\n"
        r"\| Owner \| Task \| Completed \|\n"
        r"\|[-| ]+\|)\n.*",
        r"\1\n"
        "| both  | Example: set up vault structure and slash commands | 2026-01-01 |\n"
        "|       |       |           |\n",
        src,
        flags=re.DOTALL,
    )

    src = re.sub(r"\n{3,}", "\n\n", src)

    (TEMPLATE / "Todo.md").write_text(src)
    print("  Todo.md sanitized")


if __name__ == "__main__":
    sanitize_claude_md()
    sanitize_todo_md()
