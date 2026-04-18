---
title: Commands
tags: [reference]
---

# Commands

## Vault Commands

| Command               | What it does                                                                                                                     |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `/decision <text>`    | Log a decision quickly from natural language. Auto-routes to the right component's decisions/ folder.                            |
| `/prep-day [date]`    | Fetches calendar events, creates meeting note shells, and populates the scratch pad for the target day (defaults to today).      |
| `/close-day [date]`   | Pulls emails, merges Gemini notes, ports scratch pad notes to meeting files, summarizes the day, then preps tomorrow.            |
| `/pull-emails`        | Pulls emails labeled "z - Obsidian" from Gmail into the vault inbox, then removes the label.                                     |
| `/pull-slack`         | Dispatches commands from #obsidian-luke: todo, decision, note, meeting, search, jira. See [[scripts/slack-pull/Slack Channels]]. |
| `/slack-listener`     | Starts polling #obsidian-luke every 5 minutes. Run after `/prep-day` to listen all day.                                          |
| `/jira-vault-sync`    | Syncs initiative overviews with current Jira state and reports changes.                                                          |
| `/sync-presentations` | Pulls presentations from the Google Drive folder into 06-Presentations/ as searchable markdown.                                  |

## Jira Commands

| Command | What it does |
|---|---|
| `/jira-hygiene audit <KEY>` | Audits a Jira issue against the Red Hat AI hygiene checklist. |
| `/jira-hygiene create` | Guides creation of new Jiras following the Red Hat AI process. |
| `/jira-hygiene help` | Explains the Jira hierarchy, lifecycle, and links to canonical examples. |

## RFE Commands

| Command | What it does |
|---|---|
| `/rfe.create` | Write a new RFE from a problem statement or idea, asking clarifying questions first. |
| `/rfe.review <KEY> [KEY...]` | Review and improve RFEs by running rubric scoring, feasibility checks, and auto-revision. |
| `/rfe.submit` | Submit or update RFEs in Jira (creates RHAIRFE tickets or updates existing ones). |
| `/rfe.split <KEY> [KEY...]` | Split oversized RFEs into smaller, right-sized RFEs. |
| `/rfe.auto-fix <KEY/JQL>` | Batch review and fix RFEs automatically (reviews, revises, splits). |
| `/rfe.speedrun` | End-to-end RFE pipeline: create, review, auto-fix, and submit in one pass. |
| `/assess-rfe <KEY/path/text>` | Assess an RFE against quality criteria and score it. |
| `/export-rubric` | Export the RFE scoring rubric to artifacts/rfe-rubric.md. |

## Strategy Commands

| Command | What it does |
|---|---|
| `/strat.create` | Create RHAISTRAT strategies from approved RFEs by cloning from RHAIRFE. |
| `/strat.refine` | Add the HOW, dependencies, impacted teams, and non-functional requirements to strategies. |
| `/strat.review` | Adversarial review of strategies across feasibility, testability, scope, and architecture. |

## Review Commands

| Command | What it does |
|---|---|
| `/rfe-feasibility-review` | Reviews RFEs for technical feasibility, blockers, and alignment. |
| `/feasibility-review` | Reviews strategy features for technical feasibility and effort estimates. |
| `/testability-review` | Reviews strategy features for measurable acceptance criteria and edge cases. |
| `/scope-review` | Reviews strategy features for right-sizing and whether anything should be split. |
| `/architecture-review` | Reviews strategy features for dependencies, integration patterns, and component interactions. |
