---
title: "{{title}}"
date: {{date}}
type: ""  # recurring series name (e.g. "team-standup") or "one-off"
attendees: []
initiatives: []  # e.g. ["[[01-Components/my-component/_overview]]"]
transcript: ""   # e.g. "[[_transcripts/2026-04-08-standup-transcript]]"
recording: ""    # Google Drive or other link
tags: [meeting]
---

<!--
Claude Code instructions:
- Single file per meeting. All sources (my notes, AI summary, transcript, 
  recording) consolidated here.
- If `transcript` in frontmatter points to a file in _transcripts/, read it 
  and use it as the source of truth for ## Notes, ## Decisions, and ## Action Items.
- Extract my action items into Todo.md under Next Up (or This Week if 
  urgent), with a link back to this meeting note.
- Preserve ## Prep content if I already filled it in -- don't overwrite.
- Write in my voice: concise, bullet-heavy, no fluff.
-->

# {{title}}

**Date:** {{date}}
**Attendees:** 
**Initiatives:** 

## Prep

_What I want to get out of this meeting. Filled in before the meeting._

- 

## Notes

_Populated from the transcript or taken live during the meeting._

- 

## Decisions

_Explicit decisions made during the meeting. Log significant ones as decision files in the relevant initiative's `decisions/` folder._

- 

## Action Items

- [ ] _task_ -- @owner -- due date
- [ ] _task_ -- @owner -- due date

## Follow-ups

_Things to revisit next time or in another forum._

- 

## AI Summary

_Auto-generated summary from meeting AI (e.g., Google Gemini, Otter). Populated by /close-day or /pull-emails. Leave empty if no AI summary available._

## Scratch Pad

_Free-form notes, brain dumps, and raw context to process later._

