# Factory Configuration
<!-- This file configures the Remote Factory for your project. -->
<!-- The factory reads this during Init mode and generates .factory/config.json from it. -->
<!-- Fill in each section below. -->

## Goal
<!-- A single sentence describing what this project should achieve. -->

Provide a comprehensive, opinionated Obsidian vault template that centralizes work knowledge (strategy, research, decisions, meeting notes, project thinking) in a single structured source of truth alongside automation scripts and Claude Code skills for daily workflows.

## Scope

### Modifiable
<!-- Files and directories the factory is allowed to create or edit. -->
<!-- One path per line. Glob patterns are supported. -->

- scripts/**/*.py
- scripts/**/*.sh
- skills/**/*.md
- Templates/**/*.md
- eval/**/*.py
- CLAUDE.md
- Home.md
- Todo.md
- Automation.md
- Commands.md

### Read-only
<!-- Files the factory may read but must never modify. -->

- README.md
- LICENSE
- 01-Components/**/*
- 02-Weekly/**/*
- 03-Meetings/**/*
- 04-Inbox/**/*
- 05-People/**/*
- 06-Presentations/**/*
- 07-Usage/**/*
- 99-Archive/**/*
- docs/**/*

## Guards
<!-- Rules the factory must never violate. Checked before every commit. -->

- Do not delete or overwrite existing tests
- Do not modify files outside the declared scope
- Do not introduce secrets or credentials into the repository
- Do not post messages to Slack, Gmail, Google Chat, or any external channel directly
- Do not modify user content in vault directories (01-Components through 99-Archive)

## Eval

### Command
<!-- The shell command the factory runs to score a change. -->
<!-- It must output JSON to stdout matching the EvalResult format. -->

```bash
python eval/score.py
```

### Threshold
<!-- Minimum composite score (0.0-1.0) required to keep a change. -->

0.4

## Target Branch
<!-- Branch that experiment PRs target. Default: main -->

main

## Eval Spec

<!-- Auto-populated from .factory/eval_spec.json -->

- syntax_check (weight: 0.83, source: fallback): Verify code has no syntax errors
- observability (weight: 0.17, source: researched): Analyze logging coverage, structured logging, and request tracing

## Project Eval
<!-- User-defined project-specific eval dimensions (benchmarks, accuracy, latency, etc.) -->
<!-- Each dimension starts with '- name:' followed by indented key: value lines -->
<!-- Output format: JSON with {"score": 0.0-1.0} or exit code (0=pass, non-zero=fail) -->

## Eval Weights
<!-- Weight distribution across eval tiers (must sum to 1.0) -->
<!-- Only needed when Project Eval dimensions are defined -->
<!-- Default without project eval: hygiene 0.50, growth 0.50 -->

## Smoke Test
<!-- Optional shell command that must pass before any change is kept. -->
<!-- If configured, this runs as part of `factory precheck` — failure = mandatory revert. -->

```bash
python -c "import yaml; print('smoke test passed')"
```

## Constraints
<!-- Soft rules that guide behavior but don't block commits. -->

- Prefer small, incremental changes over large rewrites
- Each change should be accompanied by at least one test
- Follow the existing code style and conventions
- Maintain backward compatibility with existing vault structures
- Skills must follow the SKILL.md pattern with proper frontmatter

## Research Target
<!-- Only for research/benchmark projects. Define the metric to improve. -->

## Mutable Surfaces
<!-- Files the Builder is allowed to modify during research experiments. -->

## Fixed Surfaces
<!-- Ground truth files, test data, eval infrastructure. -->

## Research Constraints
<!-- Additional rules for the research loop. -->

## Cost Budget
<!-- Per-cycle or total budget constraints for research experiments. -->
