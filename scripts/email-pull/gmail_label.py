#!/usr/bin/env python3
"""Remove Gmail labels using the MCP's stored OAuth credentials."""

import json
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = Path.home() / ".google_workspace_mcp" / "credentials" / "linglis@redhat.com.json"
LABEL_NAME = "z - Obsidian"


def get_credentials():
    """Load OAuth credentials from the MCP token store."""
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
    results = service.users().labels().list(userId="me").execute()
    for label in results.get("labels", []):
        if label["name"] == label_name:
            return label["id"]
    return None


def remove_label(message_ids):
    """Remove the Obsidian label from the given message IDs."""
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    label_id = get_label_id(service, LABEL_NAME)
    if not label_id:
        print(f"Error: label '{LABEL_NAME}' not found", file=sys.stderr)
        sys.exit(1)

    for msg_id in message_ids:
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": [label_id]},
        ).execute()
        print(f"Removed label from {msg_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <message_id> [message_id ...]", file=sys.stderr)
        sys.exit(1)
    remove_label(sys.argv[1:])
