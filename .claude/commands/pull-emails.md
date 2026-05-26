Pull emails labeled "z - Obsidian" from Gmail into the vault inbox intake folder, then remove the label.

## Execution Rules

- Execute every step in order. Do not skip, combine, or abbreviate steps.
- Before processing a list, state its count: "Found N messages" / "Creating N intake files."
- After completing a step that produces outputs, confirm: "Step N complete: processed X, skipped Y."
- If a step fails or partially completes, state what succeeded and what did not before moving on.

## Steps

1. Search Gmail for labeled emails:
   - Use `search_gmail_messages` with query `label:z---obsidian` and `user_google_email: {{GOOGLE_EMAIL}}`, `page_size: 25`
   - If the response includes a `next_page_token`, call `search_gmail_messages` again with that token. Repeat until no token is returned. Collect ALL message IDs across all pages before proceeding.
   - State: "Found N messages across P pages."
   - If no messages found, report "No new emails to pull" and stop

2. Load the imported IDs tracker:
   - Read `scripts/email-pull/.imported_ids.json`
   - Filter out any message IDs already in the tracker (skip duplicates)
   - If all messages are already imported, report "All labeled emails already imported" and stop

3. Fetch full content for new messages:
   - Use `get_gmail_messages_content_batch` with `format: "full"`, `body_format: "text"`
   - Batch up to 25 messages per call
   - **Also** fetch any Gemini meeting note emails (from: `gemini-notes@google.com`) or meeting recording emails (from: `meetings-noreply@google.com`) a second time with `body_format: "html"` to extract Google Doc/Drive URLs

4. For Gemini meeting note emails (from `gemini-notes@google.com`):

   **CRITICAL: Every Gemini note MUST result in a meeting file. The transcript IS the meeting record, even if the user didn't attend, was OOO, or left zero notes. Never leave a Gemini note as an intake file.**

   **4a. Fetch content using the Python script (primary method):**
   - Run: `python3 scripts/email-pull/gemini_docs.py <message_id>`
   - Parse the JSON output. It returns: `meeting_name`, `meeting_date`, `google_doc_url`, `summary`, `details`, `next_steps`, `full_text`
   - If the script fails or is unavailable, fall back to MCP tools: extract the Google Doc URL from the HTML body, then use `get_doc_content`
   - **The `google_doc:` URL MUST be stored in frontmatter regardless of whether content fetch succeeds**

   **4b. Match to an existing meeting file in `03-Meetings/`** using the meeting name matching logic below.

   **4c. If a match is found:**
   - Store the full Gemini doc content in `03-Meetings/<series-folder>/_transcripts/YYYY-MM-DD-meeting-slug-gemini.md`
   - Update the meeting file's frontmatter: set `transcript:` to point to the `_transcripts/` file, add `google_doc:` URL
   - Add a `## Gemini Summary` section (at the end of the meeting file) with the Summary portion from the doc
   - If `## Notes` is still placeholder, populate it with the Details section from the doc
   - Extract action items from the "Suggested next steps" into `## Action Items`
   - Do NOT create a file in `04-Inbox/intake/`
   - Log as "matched" in the report

   **4d. If no matching meeting file exists, CREATE one:**
   - Use the meeting name to find or create the appropriate series folder in `03-Meetings/`
   - If a series folder with a similar name exists, use it. Otherwise use `03-Meetings/_one-off/`
   - Create a meeting note file using the standard meeting template
   - Store transcript in `_transcripts/`, populate `## Gemini Summary` and `## Notes` from the doc content
   - Log as "created" in the report

   **4e. Only use the intake path as a last resort** if the Python script fails entirely (no doc URL, no content, error output). In that case, create the intake file but ALWAYS include whatever `google_doc:` URL was extracted, even partially.

   **Meeting name matching logic:**
   To match a Gemini email to an existing meeting file, normalize both names:
   1. Strip common prefixes: `Re:`, `Fwd:`, `Notes:`, mailing list tags like `[rhelai-devel]`, `[rh-ai-bu-pm]`, etc.
   2. Strip quoted meeting names (extract content between `"` quotes if present)
   3. Lowercase and slugify both names (replace spaces/special chars with `-`, collapse multiple `-`)
   4. Strip date suffixes from both (e.g., `apr-9-2026`, `april-10`)
   5. Match if the normalized slugs share >= 70% of words OR one contains the other
   6. Date must match (within 1 day tolerance for timezone edge cases)

5. For meeting recording emails (from `meetings-noreply@google.com`):
   - Extract links from the HTML body:
     - Transcript doc: look for `docs.google.com/document/d/DOCUMENT_ID` linked with label "Transcript"
     - Recording: look for `drive.google.com/file/d/FILE_ID` linked with label "Recording"
   - If a transcript doc is found, fetch the full content using `get_doc_content`
   - **Try to match to an existing meeting file in `03-Meetings/`** using the same matching logic as step 4
   - **If a match is found:**
     - Add `recording:` field to frontmatter (Google Drive link)
     - Store transcript in `03-Meetings/<series-folder>/_transcripts/YYYY-MM-DD-meeting-slug-transcript.md`
     - Update `transcript:` frontmatter to point to the `_transcripts/` file
     - Do NOT create a file in `04-Inbox/intake/`
   - **If no match:**
     - Create a new file in `04-Inbox/intake/` as before

6. For each new message, create a markdown file in `04-Inbox/intake/`:
   - State the count before creating files: "Creating intake files for N messages (M Gemini-matched, K already imported, J to write)." All numbers must sum to total messages found in step 1.
   - Filename: `YYYY-MM-DD-slugified-subject.md` (date from the email's sent date, slug max 60 chars)
   - If file already exists, append `-2`, `-3`, etc.
   - Use this template:

   ```
   ---
   title: "SUBJECT"
   captured: TODAY
   source: email
   processed: false
   suggested_destination: ""
   tags: [inbox, email]
   from: "FROM"
   date_sent: "DATE_ISO"
   message_id: "MSG_ID"
   ---

   # SUBJECT

   **From:** FROM
   **To:** TO
   **CC:** CC (if present)
   **Date:** DISPLAY_DATE

   ---

   BODY
   ```

   For Gemini meeting notes, use this template instead:

   ```
   ---
   title: "MEETING_TITLE"
   captured: TODAY
   source: gemini-meeting-notes
   processed: false
   suggested_destination: ""
   tags: [inbox, email, meeting-notes]
   from: "FROM"
   date_sent: "DATE_ISO"
   message_id: "MSG_ID"
   google_doc: "GOOGLE_DOC_URL"
   ---

   # MEETING_TITLE

   **Date:** DISPLAY_DATE
   **Source:** [Google Doc](GOOGLE_DOC_URL)

   ---

   ## Summary

   SUMMARY_FROM_DOC

   ## Details

   DETAILS_FROM_DOC

   ## Suggested Next Steps

   NEXT_STEPS_FROM_DOC
   ```

   For meeting recording emails, use this template (if no existing meeting note found):

   ```
   ---
   title: "MEETING_TITLE"
   captured: TODAY
   source: meeting-recording
   processed: false
   suggested_destination: ""
   tags: [inbox, email, meeting-notes]
   from: "FROM"
   date_sent: "DATE_ISO"
   message_id: "MSG_ID"
   recording: "DRIVE_RECORDING_URL (if present)"
   transcript_doc: "TRANSCRIPT_DOC_URL (if present)"
   ---

   # MEETING_TITLE

   **Date:** DISPLAY_DATE
   **Recording:** [Watch](DRIVE_RECORDING_URL) (if present)
   **Transcript:** [Google Doc](TRANSCRIPT_DOC_URL) (if present)

   ---

   ## Transcript

   TRANSCRIPT_CONTENT_FROM_DOC (if fetched)
   ```

   If a matching meeting note already exists (same date and similar title in `03-Meetings/`):
   - Add `recording:` and/or `transcript_doc:` fields to the existing file's frontmatter
   - Append a `## Transcript` section if transcript content was fetched and not already present
   - Do NOT create a new file in `04-Inbox/intake/`

7. After writing each file, add the message ID to the imported IDs list and save it back to `scripts/email-pull/.imported_ids.json`

8. Remove the "z - Obsidian" label from all newly imported messages:
   - Run: `python3 scripts/email-pull/gmail_label.py MSG_ID1 MSG_ID2 ...`
   - This calls the Gmail API to remove the label

9. **Verify:** Count of files in `04-Inbox/intake/` matching today's date equals J (from step 6 count). If mismatch, investigate before proceeding.

10. Report results (one line): "Pulled N emails across P pages (M Gemini-matched/created, J to intake). Labels removed."
