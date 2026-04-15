# Design Philosophy

The thinking behind the vault's structure and conventions.

## The Core Problem

PM knowledge is scattered. Strategy lives in Google Docs. Decisions happen in Slack threads that disappear. Meeting notes sit in whatever app your calendar uses. Jira tracks execution but not thinking. Your actual reasoning -- why you chose X over Y, what the customer said, what you're worried about -- lives in your head.

This vault consolidates all of it into one searchable, linked, AI-assisted system.

## Components vs. Initiatives

**Components** are permanent product domains you're responsible for. They don't ship and they don't end. "Payments" is a component. "Search" is a component.

**Initiatives** are time-bound projects within a component. They have a lifecycle: discovery, design, in-build, rollout, shipped, archived. "Add Apple Pay support" is an initiative inside the Payments component.

Why the distinction? Because decisions, research, and context accumulate at the component level even as initiatives come and go. When you start a new initiative in a component you've worked in before, all the prior research and decisions are right there.

## The Inbox Pattern

Everything enters through `04-Inbox/`. Emails, Slack messages, quick thoughts, things someone said in a hallway -- all go to the inbox first, then get triaged to their real home.

Why not just put things where they belong immediately? Because in the moment, you often don't know where something belongs. Is that customer quote research or a decision input or an action item? The inbox gives you a zero-friction capture point. Triage happens later, when you have context and focus.

Claude Code helps with triage: "process my inbox" reads everything in `04-Inbox/` and proposes destinations. You confirm or redirect. Over time, it learns your routing patterns.

## Decision Logging

Most teams make decisions constantly but never record them. Six months later, someone asks "why did we do it this way?" and nobody remembers. Worse, teams re-litigate decisions because there's no record that they were already made.

The vault makes decision logging low-friction:
- Say `/decision we chose Postgres over DynamoDB because we need complex joins`
- Claude Code creates a properly structured record with context, options, and consequences
- The record lives in the relevant component or initiative's `decisions/` folder
- When someone asks "why Postgres?", search finds it instantly

The key insight: decisions are more valuable than specs. Specs describe what you're building. Decisions describe why you're building it that way. Decisions age well; specs don't.

## The Shared Task System

`Todo.md` is a shared workspace between you and Claude Code, not a personal todo list.

Three ownership levels:
- **you** -- you own it, Claude Code doesn't touch it
- **cc** -- Claude Code owns it end-to-end (research, drafts, analysis)
- **both** -- collaborative work with clear handoff rules

Why not just use Jira for tasks? Jira tracks team execution. Todo.md tracks your personal work surface -- the stuff that's too small for a ticket, too important to forget, and too context-dependent for a generic task manager. Things like "re-read the Q3 research before Thursday's meeting" or "draft a one-pager for the new initiative."

## Weekly Scratch Pads

Each week gets one file with day-by-day sections for freeform notes. This is your thinking space -- messy, unstructured, stream-of-consciousness.

At end of week, Claude Code distills it into a curated summary (10-20 bullets: decisions, patterns, learnings, open loops) that goes to `_summaries/`. The raw scratch pad stays for reference but the summary is what you'll actually re-read.

The weekly cadence matters. Daily notes are too granular (you end up with hundreds of tiny files). Monthly is too coarse (you forget what happened in week 1 by week 4). Weekly hits the sweet spot.

## Meeting Notes as First-Class Objects

Every meeting gets its own file. All sources -- your prep notes, live notes, AI transcripts, recordings -- consolidate into one file. No more hunting across three apps to reconstruct what happened.

The `## Prep` section is filled before the meeting (what you want to get out of it). The `## Notes` and `## Action Items` sections are filled during or after. Action items automatically flow to Todo.md with links back.

Recurring meetings get their own folders so you can see history. "What did we discuss in the last three standups?" becomes a quick folder scan.

## Why This Tool Stack

**Obsidian** because: local-first (your data, your machine), markdown (portable, future-proof), graph/backlinks (connections emerge naturally), plugin ecosystem (Dataview, Kanban, etc.).

**Claude Code** because: it reads and writes files directly (no API integration needed), slash commands define workflows in plain English, path-scoped rules let you encode context-dependent behavior, and MCP servers connect it to external services.

**MCP servers** because: they run locally and give Claude Code access to Jira, Slack, Gmail, Calendar without custom API code. Add what you need, skip what you don't.

The whole system is plain markdown files. If you stop using Claude Code tomorrow, everything still works in Obsidian. If you stop using Obsidian, everything is still readable text files. No lock-in at any layer.
