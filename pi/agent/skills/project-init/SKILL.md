---
name: project-init
description: Scaffold continuous-context files for a brand-new coding project — AGENTS.md, CLEANCODE.md, a CLAUDE.md pointer, specs/design docs folders, an append-only dev journal, an architecture decision log, and a TODO list. Use when starting a new project or empty repo, or when the user asks to set up project context/scaffolding for an AI coding workflow.
---

# Project Init

Scaffolds the files an AI coding workflow needs to keep context across sessions and across tools (Claude, Codex, etc.), instead of rediscovering the codebase and its decisions from scratch every time.

## When to run

At the start of a new project, before much real code exists. If the target directory already has an `AGENTS.md`, don't overwrite it — report what's missing from this list instead and ask before filling gaps.

## Steps

1. Gather (ask if not already known from the conversation):
   - Project name
   - One-line description
   - Stack: language/runtime, framework, package manager
   - Key commands: install, run/dev, test, lint/typecheck, build (skip any that don't apply yet)

2. Create these files from the templates in `templates/`, substituting `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, and `{{DATE}}` (today's date, `YYYY-MM-DD`):
   - `AGENTS.md` ← `templates/AGENTS.md.template`
   - `CLAUDE.md` ← `templates/CLAUDE.md.template`
   - `CLEANCODE.md` ← `templates/CLEANCODE.md.template`
   - `docs/journal.md` ← `templates/journal.md.template`
   - `docs/decisions.md` ← `templates/decisions.md.template`
   - `TODO.md` ← `templates/TODO.md.template`

3. Create these directories, each with a `.gitkeep`:
   - `docs/specs/` — grilled product/spec decisions, produced by the `grill-me` workflow.
   - `docs/designs/` — design documents, implementation plans, mockups, and research write-ups.
   - `.pi/skills/` — project-specific Pi skills as they're written.

4. Append to `.gitignore` (create it if absent):
   ```
   .pi/settings.local.json
   .claude/settings.local.json
   ```

5. Report what was created. Leave the Architecture section of `AGENTS.md` as a placeholder — write it once there's actually something to describe, not speculatively.

## Ongoing use

The generated `AGENTS.md` already documents what each file is for and when to update it (see its "Context files" section) — that's the persistent copy both tools read every session. Don't restate it here; just point the user to it if they ask.
