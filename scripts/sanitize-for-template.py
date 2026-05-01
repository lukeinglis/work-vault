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


def sanitize_commands():
    """Replace hardcoded personal values in command files with placeholders."""
    cmd_dir = TEMPLATE / ".claude" / "commands"
    if not cmd_dir.exists():
        return

    replacements = [
        # Google email
        ("linglis@redhat.com", "{{GOOGLE_EMAIL}}"),
        # Slack
        ("C0ASX58TJ4T", "{{SLACK_CHANNEL_ID}}"),
        ("U08EC765D0X", "{{SLACK_USER_ID}}"),
        ("#obsidian-luke", "#{{SLACK_CHANNEL_NAME}}"),
        ("obsidian-luke", "{{SLACK_CHANNEL_NAME}}"),
        ("~/slack-mcp/scripts/setup-slack-mcp.py", "{{SLACK_TOKEN_REFRESH_CMD}}"),
        # GitHub
        ("--author=lukeinglis", "--author={{GITHUB_USERNAME}}"),
        ("author=lukeinglis", "author={{GITHUB_USERNAME}}"),
    ]

    repo_list_block = (
        "  - `lukeinglis/its_hub_demo`\n"
        "  - `lukeinglis/its_hub_luke`\n"
        "  - `Red-Hat-AI-Innovation-Team/its_hub`\n"
        "  - `Red-Hat-AI-Innovation-Team/sdg_hub`\n"
        "  - `Red-Hat-AI-Innovation-Team/Red-Hat-AI-Innovation-Team.github.io`"
    )

    repo_list_replacement = (
        "  - `{{GITHUB_USERNAME}}/your-repo-1`\n"
        "  - `{{GITHUB_USERNAME}}/your-repo-2`\n"
        "  - `your-org/project-repo`\n"
        "  <!-- Add your repos here. See docs/setup-integrations.md -->"
    )

    jira_replacements = {
        "jira-vault-sync.md": {
            'project = RHAISTRAT AND component = "Inference-Time Techniques" AND status not in (Closed) ORDER BY updated DESC':
                'project = {{JIRA_PROJECT_STRAT}} AND component = "{{COMPONENT_1}}" AND status not in (Closed) ORDER BY updated DESC',
            'project = RHAISTRAT AND component in ("SDG", "Training Hub", "Fine Tuning") AND status not in (Closed) ORDER BY updated DESC':
                'project = {{JIRA_PROJECT_STRAT}} AND component in ("{{COMPONENT_2}}", "{{COMPONENT_3}}") AND status not in (Closed) ORDER BY updated DESC',
            'project = RHAIRFE AND assignee = currentUser() AND status not in (Closed) ORDER BY updated DESC':
                'project = {{JIRA_PROJECT_RFE}} AND assignee = currentUser() AND status not in (Closed) ORDER BY updated DESC',
            'project = RHAISTRAT AND (reporter = currentUser() OR watcher = currentUser()) AND status not in (Closed) ORDER BY updated DESC':
                'project = {{JIRA_PROJECT_STRAT}} AND (reporter = currentUser() OR watcher = currentUser()) AND status not in (Closed) ORDER BY updated DESC',
            "ITS:": "Component 1:",
            "Fine-Tuning:": "Component 2:",
            "My RFEs:": "My RFEs:",
            "My RHAISTRAT:": "My Strategy:",
            "inference-time-scaling": "{{COMPONENT_1_SLUG}}",
            "fine-tuning": "{{COMPONENT_2_SLUG}}",
        },
    }

    count = 0
    for md_file in sorted(cmd_dir.glob("*.md")):
        src = md_file.read_text()
        original = src

        for old, new in replacements:
            src = src.replace(old, new)

        src = src.replace(repo_list_block, repo_list_replacement)

        fname = md_file.name
        if fname in jira_replacements:
            for old, new in jira_replacements[fname].items():
                src = src.replace(old, new)

        if fname == "research.md":
            src = src.replace(
                "**Jira:** RHAISTRAT, component: Inference-Time Scaling",
                "**Jira:** {{JIRA_PROJECT_STRAT}}, component: {{COMPONENT_1}}",
            )
            src = src.replace(
                "**Jira:** RHAISTRAT, component: Fine-Tuning",
                "**Jira:** {{JIRA_PROJECT_STRAT}}, component: {{COMPONENT_2}}",
            )
            src = src.replace(
                "**Jira:** RHAISTRAT, component: AI Innovation",
                "**Jira:** {{JIRA_PROJECT_STRAT}}, component: {{COMPONENT_3}}",
            )
            src = src.replace(
                "**Jira:** RHAISTRAT, all components",
                "**Jira:** {{JIRA_PROJECT_STRAT}}, all components",
            )
            src = re.sub(
                r"Query RHAISTRAT for active Features",
                "Query {{JIRA_PROJECT_STRAT}} for active Features",
                src,
            )

        if fname == "pull-slack.md":
            src = src.replace(
                "RHAIRFE-1234, RHAISTRAT-567",
                "PROJ-1234, STRAT-567",
            )
            src = src.replace("RHAIRFE", "{{JIRA_PROJECT_RFE}}")
            src = src.replace("RHAISTRAT", "{{JIRA_PROJECT_STRAT}}")
            src = src.replace("RHAIENG", "{{JIRA_PROJECT_ENG}}")

        if fname == "prep-day.md":
            src = src.replace(
                "Red-Hat-AI-Innovation-Team/its_hub",
                "{{YOUR_ORG}}/{{REPO_1}}",
            )
            src = src.replace(
                "Red-Hat-AI-Innovation-Team/Red-Hat-AI-Innovation-Team.github.io",
                "{{YOUR_ORG}}/{{REPO_DOCS}}",
            )
            src = re.sub(
                r"`sdg_hub`, `training_hub`",
                "`{{REPO_2}}`, `{{REPO_3}}`",
                src,
            )
            src = src.replace("RHAISTRAT", "{{JIRA_PROJECT_STRAT}}")
            src = src.replace("RHAIRFE", "{{JIRA_PROJECT_RFE}}")

        src = re.sub(
            r"- Filter out personal repos \(.*?\)",
            "- Filter out personal repos (repos not related to your work)",
            src,
        )

        if src != original:
            md_file.write_text(src)
            count += 1

    print(f"  Commands sanitized ({count} files)")


def sanitize_other_files():
    """Replace personal data in Commands.md, Slack Channels, and email scripts."""
    replacements = [
        ("linglis@redhat.com", "{{GOOGLE_EMAIL}}"),
        ("C0ASX58TJ4T", "{{SLACK_CHANNEL_ID}}"),
        ("U08EC765D0X", "{{SLACK_USER_ID}}"),
        ("#obsidian-luke", "#{{SLACK_CHANNEL_NAME}}"),
        ("obsidian-luke", "{{SLACK_CHANNEL_NAME}}"),
    ]

    files_to_sanitize = [
        TEMPLATE / "Commands.md",
        TEMPLATE / "scripts" / "slack-pull" / "Slack Channels.md",
        TEMPLATE / "scripts" / "email-pull" / "gmail_label.py",
    ]

    count = 0
    for fpath in files_to_sanitize:
        if not fpath.exists():
            continue
        src = fpath.read_text()
        original = src
        for old, new in replacements:
            src = src.replace(old, new)
        if src != original:
            fpath.write_text(src)
            count += 1

    print(f"  Other files sanitized ({count} files)")


if __name__ == "__main__":
    sanitize_claude_md()
    sanitize_todo_md()
    sanitize_commands()
    sanitize_other_files()
