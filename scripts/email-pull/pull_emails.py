#!/usr/bin/env python3
"""Pull exported emails from Google Sheet CSV into the work-vault inbox."""

import argparse
import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent
INBOX_DIR = VAULT_ROOT / "04-Inbox"
CSV_FILE = SCRIPT_DIR / "emails.csv"
IMPORTED_IDS_FILE = SCRIPT_DIR / ".imported_ids.json"


# ---------------------------------------------------------------------------
# CSV reading
# ---------------------------------------------------------------------------

def read_csv(csv_path):
    """Read the exported CSV file and return parsed rows (list of dicts)."""
    if not csv_path.exists():
        print(
            f"Error: {csv_path} not found.\n"
            "Download the 'Emails' tab from your Google Sheet as CSV\n"
            "and save it as emails.csv in this directory.\n"
            "See README.md for instructions.",
            file=sys.stderr,
        )
        sys.exit(1)
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ---------------------------------------------------------------------------
# Filename generation
# ---------------------------------------------------------------------------

def slugify(text, max_len=60):
    """Convert text to a kebab-case slug suitable for filenames."""
    text = text.lower().strip()
    text = re.sub(r"[:/\\|]", "-", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    text = text.strip("-")
    if len(text) > max_len:
        truncated = text[:max_len]
        last_hyphen = truncated.rfind("-")
        if last_hyphen > 20:
            text = truncated[:last_hyphen]
        else:
            text = truncated
    return text or "email"


def unique_filepath(base_path):
    """Ensure a filepath is unique by appending -2, -3, etc."""
    if not base_path.exists():
        return base_path
    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def row_to_markdown(row):
    """Convert a Sheet CSV row (dict) to a markdown file (filename, content)."""
    msg_id = row.get("id", "")
    subject = row.get("subject", "(no subject)")
    from_addr = row.get("from", "")
    to_addr = row.get("to", "")
    cc_addr = row.get("cc", "")
    date_str = row.get("date", "")
    body = row.get("body", "")
    links = row.get("links", "")
    attachments = row.get("attachments", "")

    # Parse date for filename
    try:
        date_prefix = date_str[:10]  # "2026-04-07" from ISO string
        # Validate it looks like a date
        datetime.strptime(date_prefix, "%Y-%m-%d")
    except (ValueError, IndexError):
        date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = slugify(subject)
    filename = f"{date_prefix}-{slug}.md"

    # Escape quotes in title for YAML
    safe_title = subject.replace('"', '\\"')

    # Format the date for display
    try:
        display_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        display_date_str = display_date.strftime("%B %d, %Y %I:%M %p")
    except (ValueError, AttributeError):
        display_date_str = date_str

    # Build frontmatter
    lines = [
        "---",
        f'title: "{safe_title}"',
        f"captured: {today}",
        "source: email",
        "processed: false",
        'suggested_destination: ""',
        "tags: [inbox, email]",
        f'from: "{from_addr}"',
        f'date_sent: "{date_str}"',
        f'message_id: "{msg_id}"',
        "---",
        "",
        f"# {subject}",
        "",
        f"**From:** {from_addr}  ",
        f"**To:** {to_addr}  ",
    ]
    if cc_addr:
        lines.append(f"**CC:** {cc_addr}  ")
    lines.append(f"**Date:** {display_date_str}  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Body
    lines.append(body.strip())

    # Links extracted from HTML (if any beyond what's in plain text)
    if links.strip():
        link_list = [l.strip() for l in links.strip().split("\n") if l.strip()]
        if link_list:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("**Links:**")
            for link in link_list:
                lines.append(f"- {link}")

    # Attachments with Drive links
    if attachments.strip():
        att_pairs = [a.strip() for a in attachments.strip().split("\n") if a.strip()]
        if att_pairs:
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("**Attachments:**")
            for pair in att_pairs:
                if "|" in pair:
                    name, url = pair.split("|", 1)
                    lines.append(f"- [{name}]({url})")
                else:
                    lines.append(f"- {pair}")

    lines.append("")
    content = "\n".join(lines)
    return filename, content, msg_id


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------

def load_imported_ids():
    """Load the set of previously imported message IDs."""
    if IMPORTED_IDS_FILE.exists():
        return set(json.loads(IMPORTED_IDS_FILE.read_text()))
    return set()


def save_imported_ids(ids):
    """Save the set of imported message IDs."""
    IMPORTED_IDS_FILE.write_text(json.dumps(sorted(ids), indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pull exported emails from Google Sheet into the vault inbox."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_FILE,
        help=f"Path to exported CSV file (default: {CSV_FILE.name})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without writing files",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed progress"
    )
    args = parser.parse_args()

    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    # Read CSV
    if args.verbose:
        print(f"Reading CSV from {args.csv}...")
    rows = read_csv(args.csv)
    if not rows:
        print("No emails found in the sheet.")
        return
    if args.verbose:
        print(f"Found {len(rows)} row(s) in sheet.")

    # Load idempotency tracker
    imported_ids = load_imported_ids()

    imported_count = 0
    skipped_count = 0

    for row in rows:
        msg_id = row.get("id", "")
        if not msg_id:
            continue
        if msg_id in imported_ids:
            skipped_count += 1
            if args.verbose:
                print(f"  Skipping (already imported): {row.get('subject', '?')}")
            continue

        filename, content, gmail_id = row_to_markdown(row)
        filepath = unique_filepath(INBOX_DIR / filename)

        if args.dry_run:
            print(f"  Would import: {row.get('subject', '?')} -> {filepath.name}")
        else:
            filepath.write_text(content)
            imported_ids.add(gmail_id)
            save_imported_ids(imported_ids)
            if args.verbose:
                print(f"  Imported: {filepath.name}")
            imported_count += 1

    if args.dry_run:
        total = len(rows) - skipped_count
        print(f"\nDry run: {total} email(s) would be imported, {skipped_count} skipped.")
    else:
        print(
            f"Done: {imported_count} imported, {skipped_count} skipped (already imported)."
        )


if __name__ == "__main__":
    main()
