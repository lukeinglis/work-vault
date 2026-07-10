#!/usr/bin/env python3
"""Remove Gmail labels using the MCP's stored OAuth credentials."""

import json
import sys
import uuid
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))
from lib.logging import configure_logging, get_logger, clear_and_bind

configure_logging()
log = get_logger("gmail_label")

TOKEN_FILE = Path.home() / ".google_workspace_mcp" / "credentials" / "{{GOOGLE_EMAIL}}.json"
LABEL_NAME = "z - Obsidian"


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


def get_label_id(service, label_name):
    """Find the Gmail label ID for a given label name."""
    log.debug("looking_up_label", label_name=label_name)
    results = service.users().labels().list(userId="me").execute()
    for label in results.get("labels", []):
        if label["name"] == label_name:
            log.info("label_found", label_name=label_name, label_id=label["id"])
            return label["id"]
    log.warning("label_not_found", label_name=label_name)
    return None


def remove_label(message_ids):
    """Remove the Obsidian label from the given message IDs."""
    operation_id = str(uuid.uuid4())[:8]
    clear_and_bind(operation_id=operation_id)
    log.info("remove_label_start", label=LABEL_NAME, message_count=len(message_ids))

    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    label_id = get_label_id(service, LABEL_NAME)
    if not label_id:
        log.error("label_missing", label=LABEL_NAME)
        print(f"Error: label '{LABEL_NAME}' not found", file=sys.stderr)
        sys.exit(1)

    for msg_id in message_ids:
        log.info("removing_label", message_id=msg_id, label_id=label_id)
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": [label_id]},
        ).execute()
        print(f"Removed label from {msg_id}")

    log.info("remove_label_complete", messages_processed=len(message_ids))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <message_id> [message_id ...]", file=sys.stderr)
        sys.exit(1)
    remove_label(sys.argv[1:])
