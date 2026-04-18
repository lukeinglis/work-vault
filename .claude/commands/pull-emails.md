Pull emails labeled "z - Obsidian" from Gmail into the vault inbox intake folder, then remove the label.

## Steps

1. Search Gmail for labeled emails:
   - Use `search_gmail_messages` with query `label:z---obsidian` and `user_google_email: linglis@redhat.com`, `page_size: 25`
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
   - Extract the Google Doc URL from the HTML body (look for `docs.google.com/document/d/DOCUMENT_ID` in an `<a>` tag)
   - Fetch the full doc content using `get_doc_content` with the extracted document ID
   - Extract the meeting name and date from the email subject (format: `Notes: "Meeting Name" Mon DD, YYYY`)
   - **Try to match to an existing meeting file in `03-Meetings/`** using the meeting name matching logic below
   - **If a match is found:**
     - Store the full Gemini doc content in `03-Meetings/<type>/_transcripts/YYYY-MM-DD-meeting-slug-gemini.md`
     - Update the meeting file's frontmatter: set `transcript:` to point to the `_transcripts/` file
     - Add a `## Gemini Summary` section (at the end of the meeting file) with the Summary portion from the doc
     - If `## Notes` is still placeholder, populate it with the Details section from the doc
     - Do NOT create a file in `04-Inbox/intake/`
     - Log as "matched" in the report
   - **If no match is found:**
     - Create the intake file in `04-Inbox/intake/` as before (close-day will route it)

   **Meeting name matching logic:**
   To match a Gemini email to an existing meeting file, normalize both names:
   1. Strip common prefixes: `Re:`, `Fwd:`, `Notes:`, mailing list tags like `[rhelai-devel]`, `[rh-ai-bu-pm]`, etc.
   2. Strip quoted meeting names (extract content between `"` quotes if present)
   3. Lowercase and slugify both names (replace spaces/special chars with `-`, collapse multiple `-`)
   4. Strip date suffixes from both (e.g., `apr-9-2026`, `april-10`)
   5. Match if the normalized slugs share >= 70% of words OR one contains the other
   6. Date must match (within 1 day tolerance for timezone edge cases)

4b. For meeting recording emails (from `meetings-noreply@google.com`):
   - Extract links from the HTML body:
     - Transcript doc: look for `docs.google.com/document/d/DOCUMENT_ID` linked with label "Transcript"
     - Recording: look for `drive.google.com/file/d/FILE_ID` linked with label "Recording"
   - If a transcript doc is found, fetch the full content using `get_doc_content`
   - **Try to match to an existing meeting file in `03-Meetings/`** using the same matching logic as step 4
   - **If a match is found:**
     - Add `recording:` field to frontmatter (Google Drive link)
     - Store transcript in `03-Meetings/<type>/_transcripts/YYYY-MM-DD-meeting-slug-transcript.md`
     - Update `transcript:` frontmatter to point to the `_transcripts/` file
     - Do NOT create a file in `04-Inbox/intake/`
   - **If no match:**
     - Create a new file in `04-Inbox/intake/` as before

5. For each new message, create a markdown file in `04-Inbox/intake/`:
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

6. After writing each file, add the message ID to the imported IDs list and save it back to `scripts/email-pull/.imported_ids.json`

7. Remove the "z - Obsidian" label from all newly imported messages:
   - Run: `python3 scripts/email-pull/gmail_label.py MSG_ID1 MSG_ID2 ...`
   - This calls the Gmail API to remove the label

8. Report results (one line): "Pulled 3 emails (1 Gemini note matched to ITS standup, 2 to intake). Labels removed."
