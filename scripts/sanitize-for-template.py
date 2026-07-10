#!/usr/bin/env python3
"""
Sanitize live vault files into generic template versions.
Preserves structural improvements while stripping personal content.
"""

import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.logging import configure_logging, get_logger, clear_and_bind

configure_logging()
log = get_logger("sanitize")

VAULT = Path.home() / "Documents" / "work-vault"
TEMPLATE = Path.home() / "projects" / "work-vault-template"

GLOBAL_REPLACEMENTS = [
    ("linglis@redhat.com", "{{GOOGLE_EMAIL}}"),
    ("C0ASX58TJ4T", "{{SLACK_CHANNEL_ID}}"),
    ("U08EC765D0X", "{{SLACK_USER_ID}}"),
    ("#obsidian-luke", "#{{SLACK_CHANNEL_NAME}}"),
    ("obsidian-luke", "{{SLACK_CHANNEL_NAME}}"),
    ("RHAISTRAT", "{{JIRA_PROJECT_STRAT}}"),
    ("RHAIRFE", "{{JIRA_PROJECT_RFE}}"),
    ("RHAIENG", "{{JIRA_PROJECT_ENG}}"),
    ("Red-Hat-AI-Innovation-Team", "{{YOUR_ORG}}"),
    ("sdg_hub_luke", "{{FORK_REPO}}"),
    ("its_hub_demo", "{{DEMO_REPO}}"),
    ("its_hub", "{{REPO_1}}"),
    ("sdg_hub", "{{REPO_2}}"),
    ("training_hub", "{{REPO_3}}"),
    ("lukeinglis", "{{GITHUB_USERNAME}}"),
    ("~/slack-mcp/scripts/setup-slack-mcp.py", "{{SLACK_TOKEN_REFRESH_CMD}}"),
]

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


def apply_global_replacements(text):
    replacements_made = 0
    for old, new in GLOBAL_REPLACEMENTS:
        count = text.count(old)
        if count > 0:
            text = text.replace(old, new)
            replacements_made += count
    if replacements_made > 0:
        log.debug("global_replacements_applied", replacements_made=replacements_made)
    return text


def sanitize_claude_md():
    log.info("sanitizing_file", file_path="CLAUDE.md")
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

    src = re.sub(
        r"\| `06-Presentations/` \| Slide decks by initiative \(.*?\) \|",
        "| `06-Presentations/` | Slide decks by initiative or cross-cutting theme |",
        src,
    )

    if "06-Presentations" not in src:
        src = src.replace(
            "| `05-People/` | Stakeholder reference |",
            "| `05-People/` | Stakeholder reference |\n"
            "| `06-Presentations/` | Slide decks by initiative or cross-cutting theme |",
        )

    (TEMPLATE / "CLAUDE.md").write_text(src)
    log.info("file_sanitized", file_path="CLAUDE.md")


def sanitize_todo_md():
    log.info("sanitizing_file", file_path="Todo.md")
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
    log.info("file_sanitized", file_path="Todo.md")


def sanitize_commands():
    """Replace hardcoded personal values in command files with placeholders."""
    log.info("sanitizing_commands")
    cmd_dir = TEMPLATE / ".claude" / "commands"
    if not cmd_dir.exists():
        log.warning("commands_dir_not_found", path=str(cmd_dir))
        return

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

        src = src.replace(repo_list_block, repo_list_replacement)

        fname = md_file.name
        if fname in jira_replacements:
            for old, new in jira_replacements[fname].items():
                src = src.replace(old, new)

        if fname == "pull-slack.md":
            src = src.replace(
                "RHAIRFE-1234, RHAISTRAT-567",
                "PROJ-1234, STRAT-567",
            )

        if fname == "research.md":
            src = sanitize_research_md(src)

        if fname == "prep-day.md":
            src = sanitize_prep_day_md(src)

        if fname == "sync-sessions.md":
            src = sanitize_sync_sessions_md(src)

        src = apply_global_replacements(src)

        src = re.sub(
            r"- Filter out personal repos \(.*?\)",
            "- Filter out personal repos (repos not related to your work)",
            src,
        )

        if src != original:
            md_file.write_text(src)
            count += 1

    log.info("commands_sanitized", files_modified=count)


def sanitize_research_md(src):
    src = re.sub(
        r"that Red Hat should know about, respond to, or build on\?",
        "that your org should know about, respond to, or build on?",
        src,
    )
    src = re.sub(
        r"### Red Hat AI \(`redhat-ai`\) -- DEFAULT",
        "### {{YOUR_ORG_SHORT}} AI (`org-ai`) -- DEFAULT",
        src,
    )
    src = re.sub(
        r"Red Hat AI product portfolio, enterprise AI platform competition, "
        r"industry trends affecting Red Hat AI",
        "{{YOUR_ORG_SHORT}} AI product portfolio, enterprise AI platform competition, "
        "industry trends affecting {{YOUR_ORG_SHORT}} AI",
        src,
    )
    src = re.sub(
        r"Red Hat AI current offerings \(Red Hat OpenShift AI, RHOAI components, "
        r"InstructLab, Podman AI Lab, Neural Magic/vLLM\)",
        "{{YOUR_ORG_SHORT}} AI current offerings (list your org's AI products here)",
        src,
    )
    src = re.sub(
        r"How is Red Hat AI positioned",
        "How is {{YOUR_ORG_SHORT}} AI positioned",
        src,
    )
    src = re.sub(
        r"## Relevance to Red Hat",
        "## Relevance to {{YOUR_ORG_SHORT}}",
        src,
    )
    src = re.sub(
        r"Where Red Hat's offerings sit relative to the landscape",
        "Where {{YOUR_ORG_SHORT}}'s offerings sit relative to the landscape",
        src,
    )
    src = re.sub(
        r"Analyze where Red Hat's offerings sit relative to the landscape",
        "Analyze where {{YOUR_ORG_SHORT}}'s offerings sit relative to the landscape",
        src,
    )
    return src


def sanitize_prep_day_md(src):
    src = re.sub(
        r"its_hub: 2 PRs merged \(reward-hub refactor, docs update\)",
        "{{REPO_1}}: 2 PRs merged (feature-x, docs update)",
        src,
    )
    src = re.sub(
        r"nothing pressing, sdg_hub/training_hub quiet",
        "nothing pressing, {{REPO_2}}/{{REPO_3}} quiet",
        src,
    )
    src = re.sub(
        r"This launches four parallel background agents \(ITS, Fine-Tuning, AI Innovation, Red Hat AI\)",
        "This launches four parallel background agents (one per initiative)",
        src,
    )
    src = re.sub(
        r"its_hub had 2 PRs merged; other repos quiet",
        "{{REPO_1}} had 2 PRs merged; other repos quiet",
        src,
    )
    return src


def sanitize_sync_sessions_md(src):
    src = re.sub(
        r"fork-sync repos \(sdg_hub_luke\)",
        "fork-sync repos ({{FORK_REPO}})",
        src,
    )
    return src


def sanitize_commands_md():
    log.info("sanitizing_file", file_path="Commands.md")
    fpath = TEMPLATE / "Commands.md"
    if not fpath.exists():
        log.debug("file_not_found", file_path="Commands.md")
        return
    src = fpath.read_text()
    original = src

    src = apply_global_replacements(src)
    src = re.sub(
        r"Red Hat AI hygiene checklist",
        "{{YOUR_ORG_SHORT}} AI hygiene checklist",
        src,
    )
    src = re.sub(
        r"following the Red Hat AI process",
        "following the {{YOUR_ORG_SHORT}} AI process",
        src,
    )

    if src != original:
        fpath.write_text(src)
        log.info("file_sanitized", file_path="Commands.md")
    else:
        log.debug("file_unchanged", file_path="Commands.md")


def sanitize_automation_md():
    log.info("sanitizing_file", file_path="Automation.md")
    fpath = TEMPLATE / "Automation.md"
    if not fpath.exists():
        log.debug("file_not_found", file_path="Automation.md")
        return
    src = fpath.read_text()
    original = src

    src = apply_global_replacements(src)

    if src != original:
        fpath.write_text(src)
        log.info("file_sanitized", file_path="Automation.md")
    else:
        log.debug("file_unchanged", file_path="Automation.md")


def sanitize_gemini_docs_py():
    log.info("sanitizing_file", file_path="gemini_docs.py")
    fpath = TEMPLATE / "scripts" / "email-pull" / "gemini_docs.py"
    if not fpath.exists():
        log.debug("file_not_found", file_path="gemini_docs.py")
        return
    src = fpath.read_text()
    original = src

    src = src.replace(
        'Path.home() / ".google_workspace_mcp" / "credentials" / "linglis@redhat.com.json"',
        'Path.home() / ".google_workspace_mcp" / "credentials" / "{{GOOGLE_EMAIL}}.json"',
    )

    if src != original:
        fpath.write_text(src)
        log.info("file_sanitized", file_path="gemini_docs.py")
    else:
        log.debug("file_unchanged", file_path="gemini_docs.py")


def sanitize_other_files():
    """Apply global replacements to remaining files."""
    log.info("sanitizing_other_files")
    files_to_sanitize = [
        TEMPLATE / "scripts" / "slack-pull" / "Slack Channels.md",
        TEMPLATE / "scripts" / "email-pull" / "gmail_label.py",
    ]

    count = 0
    for fpath in files_to_sanitize:
        if not fpath.exists():
            continue
        src = fpath.read_text()
        original = src
        src = apply_global_replacements(src)
        if src != original:
            fpath.write_text(src)
            count += 1

    log.info("other_files_sanitized", files_modified=count)


def verify_no_leaks():
    """Scan all sanitized files for any remaining org-specific patterns."""
    import subprocess

    log.info("verifying_no_leaks")

    target_files = []
    for pattern in [
        "CLAUDE.md", "Todo.md", "Commands.md", "Automation.md", "Home.md",
    ]:
        f = TEMPLATE / pattern
        if f.exists():
            target_files.append(str(f))

    cmd_dir = TEMPLATE / ".claude" / "commands"
    if cmd_dir.exists():
        target_files.extend(str(f) for f in cmd_dir.glob("*.md"))

    for subdir in ["email-pull", "slack-pull"]:
        d = TEMPLATE / "scripts" / subdir
        if d.exists():
            target_files.extend(str(f) for f in d.iterdir() if f.is_file())

    if not target_files:
        log.warning("no_files_to_verify")
        print("  No files to verify")
        return True

    log.debug("scanning_files", file_count=len(target_files))
    grep_pattern = "|".join(BANNED_PATTERNS)
    result = subprocess.run(
        ["grep", "-E", "-n", grep_pattern] + target_files,
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        leak_count = len(result.stdout.strip().split("\n"))
        log.error("leaks_detected", leak_count=leak_count)
        print("  LEAK DETECTED: org-specific patterns remain:")
        for line in result.stdout.strip().split("\n"):
            print(f"    {line}")
        return False

    log.info("verification_passed")
    print("  Verification passed: no org-specific patterns found")
    return True


if __name__ == "__main__":
    operation_id = str(uuid.uuid4())[:8]
    clear_and_bind(operation_id=operation_id)
    log.info("sanitize_start")

    print("Sanitizing vault files...")
    sanitize_claude_md()
    sanitize_todo_md()
    sanitize_commands()
    sanitize_commands_md()
    sanitize_automation_md()
    sanitize_gemini_docs_py()
    sanitize_other_files()
    print("\nVerifying sanitization...")
    if not verify_no_leaks():
        log.error("sanitize_failed")
        print("\nFAILED: Some org-specific patterns were not sanitized.")
        exit(1)
    log.info("sanitize_complete")
    print("\nDone.")
