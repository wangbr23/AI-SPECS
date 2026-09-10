---
name: project-init
description: Scaffold continuous-context files for a brand-new coding project — AGENTS.md, a CLAUDE.md pointer, an append-only dev journal, an architecture decision log, and a TODO list. Use when starting a new project or empty repo, or when the user asks to set up project context/scaffolding for an AI coding workflow.
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

3. Create `docs/designs/` (empty, add a `.gitkeep`) — where design documents (specs, mockups, research write-ups) get saved, so they persist alongside the journal and decisions log instead of living only in chat/artifact history.

4. Create `.claude/skills/` (empty, add a `.gitkeep`) so project-specific skills have a home as they're written.

5. Append to `.gitignore` (create it if absent):
   ```
   .claude/settings.local.json
   ```

6. Reference the machine's subagent convention: the generated `AGENTS.md` template already points at the `herdr-subagents` skill (opencode global skills) in its Conventions section. If that skill doesn't exist on this machine, strip that line rather than leaving a dead reference.

7. Report what was created. Leave the Architecture section of `AGENTS.md` as a placeholder — write it once there's actually something to describe, not speculatively.

## Ongoing use

The generated `AGENTS.md` already documents what each file is for and when to update it (see its "Context files" section) — that's the persistent copy both tools read every session. Don't restate it here; just point the user to it if they ask.
