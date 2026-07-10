#!/usr/bin/env python3
"""Fetch Gemini meeting note content from Gmail messages and Google Docs.

Given a Gmail message ID (from a gemini-notes@google.com email), extracts the
linked Google Doc URL, fetches the doc content, and outputs structured JSON.

Uses the same OAuth credentials as gmail_label.py.
"""

import argparse
import base64
import json
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.logging import configure_logging, get_logger, clear_and_bind

configure_logging()
log = get_logger("gemini_docs")

TOKEN_FILE = (
    Path.home() / ".google_workspace_mcp" / "credentials" / "{{GOOGLE_EMAIL}}.json"
)

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4,
    "june": 6, "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}


def get_credentials():
    """Load OAuth credentials from the MCP token store."""
    log.debug("loading_credentials", token_file=str(TOKEN_FILE))
    data = json.loads(TOKEN_FILE.read_text())
    return Credentials(
        token=data["token"],
        refresh_token=data["refresh_token"],
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=data["scopes"],
    )


def find_html_part(payload):
    """Recursively find the text/html part in a Gmail message payload."""
    if payload.get("mimeType") == "text/html":
        return payload.get("body", {}).get("data", "")
    for part in payload.get("parts", []):
        result = find_html_part(part)
        if result:
            return result
    return ""


def extract_doc_url(html):
    """Extract Google Doc URL from email HTML body."""
    match = re.search(
        r"https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)", html
    )
    if match:
        log.debug("doc_url_extracted", doc_id=match.group(1))
        return match.group(0), match.group(1)
    log.debug("no_doc_url_found")
    return None, None


def parse_meeting_subject(subject):
    """Parse meeting name and date from Gemini email subject.

    Format: Notes: "Meeting Name" Mon DD, YYYY
    """
    # Try quoted format first
    quoted = re.match(r'Notes:\s*[""](.+?)[""]\s+(.+)', subject)
    if quoted:
        name = quoted.group(1).strip('" “”')
        date_str = quoted.group(2).strip()
    else:
        # Fallback: Notes: Meeting Name Mon DD, YYYY
        notes_match = re.match(r"Notes:\s*(.+)", subject)
        if notes_match:
            rest = notes_match.group(1).strip()
            # Try to split off the date at the end
            date_pattern = re.search(
                r"\b([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$", rest
            )
            if date_pattern:
                name = rest[: date_pattern.start()].strip()
                date_str = date_pattern.group(0)
            else:
                name = rest
                date_str = ""
        else:
            name = subject
            date_str = ""

    # Parse the date
    meeting_date = None
    if date_str:
        # Try: Mon DD, YYYY or Month DD, YYYY
        date_match = re.match(
            r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})", date_str.strip()
        )
        if date_match:
            month_str = date_match.group(1).lower()
            day = int(date_match.group(2))
            year = int(date_match.group(3))
            month = MONTHS.get(month_str)
            if month:
                try:
                    meeting_date = datetime(year, month, day).strftime("%Y-%m-%d")
                except ValueError:
                    pass

    return name, meeting_date


def fetch_doc_content(docs_service, doc_id):
    """Fetch and parse a Google Doc into structured sections."""
    log.info("fetching_doc", doc_id=doc_id)
    doc = docs_service.documents().get(documentId=doc_id).execute()

    sections = {}
    current_section = "_preamble"
    sections[current_section] = []

    for element in doc.get("body", {}).get("content", []):
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        style_type = para.get("paragraphStyle", {}).get("namedStyleType", "")

        line = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                line += el["textRun"]["content"]

        line = line.rstrip("\n")

        if style_type and style_type.startswith("HEADING"):
            current_section = line.strip().lower()
            sections[current_section] = []
        elif line.strip():
            sections[current_section].append(line)

    # Build full text
    full_lines = []
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" not in element:
            continue
        para = element["paragraph"]
        style_type = para.get("paragraphStyle", {}).get("namedStyleType", "")
        line = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                line += el["textRun"]["content"]
        line = line.rstrip("\n")
        if style_type and style_type.startswith("HEADING"):
            full_lines.append(f"\n## {line.strip()}\n")
        elif line.strip():
            full_lines.append(line)

    full_text = "\n".join(full_lines)

    # Extract named sections
    summary = "\n".join(sections.get("summary", []))
    details = "\n".join(sections.get("details", sections.get("key topics", [])))
    next_steps_keys = ["next steps", "suggested next steps", "action items"]
    next_steps = ""
    for key in next_steps_keys:
        if key in sections:
            next_steps = "\n".join(sections[key])
            break

    section_count = len([k for k in sections if k != "_preamble"])
    log.info("doc_parsed", doc_id=doc_id, section_count=section_count, text_length=len(full_text))
    return summary, details, next_steps, full_text


def process_message(gmail_service, docs_service, msg_id):
    """Process a single Gmail message ID and return structured data."""
    log.info("processing_message", message_id=msg_id)
    result = {
        "message_id": msg_id,
        "google_doc_url": None,
        "doc_id": None,
        "meeting_name": None,
        "meeting_date": None,
        "summary": "",
        "details": "",
        "next_steps": "",
        "full_text": "",
        "error": None,
    }

    try:
        msg = (
            gmail_service.users()
            .messages()
            .get(userId="me", id=msg_id, format="full")
            .execute()
        )
    except Exception as e:
        log.error("gmail_fetch_failed", message_id=msg_id, error=str(e))
        result["error"] = f"gmail_fetch_failed: {e}"
        return result

    # Extract subject and parse meeting info
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    subject = headers.get("Subject", "")
    name, date = parse_meeting_subject(subject)
    result["meeting_name"] = name
    result["meeting_date"] = date

    # Extract Google Doc URL from HTML body
    html_b64 = find_html_part(msg["payload"])
    if not html_b64:
        log.warning("no_html_body", message_id=msg_id)
        result["error"] = "no_html_body"
        return result

    html = base64.urlsafe_b64decode(html_b64).decode("utf-8", errors="replace")
    doc_url, doc_id = extract_doc_url(html)

    if not doc_url:
        log.warning("no_doc_url_in_email", message_id=msg_id)
        result["error"] = "no_doc_url_in_email"
        return result

    result["google_doc_url"] = doc_url
    result["doc_id"] = doc_id

    # Fetch doc content
    try:
        summary, details, next_steps, full_text = fetch_doc_content(
            docs_service, doc_id
        )
        result["summary"] = summary
        result["details"] = details
        result["next_steps"] = next_steps
        result["full_text"] = full_text
        log.info("message_processed", message_id=msg_id, meeting_name=name)
    except Exception as e:
        log.error("doc_fetch_failed", message_id=msg_id, doc_id=doc_id, error=str(e))
        result["error"] = f"doc_fetch_failed: {e}"

    return result


def process_doc_id(docs_service, doc_id):
    """Process a document ID directly (no Gmail fetch needed)."""
    log.info("processing_doc_direct", doc_id=doc_id)
    result = {
        "message_id": None,
        "google_doc_url": f"https://docs.google.com/document/d/{doc_id}",
        "doc_id": doc_id,
        "meeting_name": None,
        "meeting_date": None,
        "summary": "",
        "details": "",
        "next_steps": "",
        "full_text": "",
        "error": None,
    }

    try:
        summary, details, next_steps, full_text = fetch_doc_content(
            docs_service, doc_id
        )
        result["summary"] = summary
        result["details"] = details
        result["next_steps"] = next_steps
        result["full_text"] = full_text

        # Try to extract meeting name from doc title
        doc = docs_service.documents().get(documentId=doc_id).execute()
        title = doc.get("title", "")
        if title:
            name, date = parse_meeting_subject(f"Notes: {title}")
            result["meeting_name"] = name
            result["meeting_date"] = date
        log.info("doc_direct_processed", doc_id=doc_id, meeting_name=result["meeting_name"])
    except Exception as e:
        log.error("doc_fetch_failed", doc_id=doc_id, error=str(e))
        result["error"] = f"doc_fetch_failed: {e}"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Gemini meeting note content from Gmail/Google Docs."
    )
    parser.add_argument(
        "message_ids",
        nargs="*",
        help="Gmail message IDs to process",
    )
    parser.add_argument(
        "--doc-id",
        help="Google Doc ID to fetch directly (skip Gmail lookup)",
    )
    args = parser.parse_args()

    if not args.message_ids and not args.doc_id:
        parser.print_help()
        sys.exit(1)

    operation_id = str(uuid.uuid4())[:8]
    clear_and_bind(operation_id=operation_id)

    creds = get_credentials()
    results = []

    if args.doc_id:
        log.info("gemini_docs_start", mode="doc_id", doc_id=args.doc_id)
        docs_service = build("docs", "v1", credentials=creds)
        results.append(process_doc_id(docs_service, args.doc_id))
    else:
        log.info("gemini_docs_start", mode="message_ids", message_count=len(args.message_ids))
        gmail_service = build("gmail", "v1", credentials=creds)
        docs_service = build("docs", "v1", credentials=creds)
        for msg_id in args.message_ids:
            results.append(process_message(gmail_service, docs_service, msg_id))

    error_count = sum(1 for r in results if r.get("error"))
    log.info("gemini_docs_complete", total=len(results), errors=error_count)

    json.dump(results, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
