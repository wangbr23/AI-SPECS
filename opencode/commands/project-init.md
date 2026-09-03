---
description: Scaffold durable project context files for a new or empty repository
agent: build
---

Scaffold the files an AI coding workflow needs to preserve context across sessions, models, agents, and coding tools.

If `$ARGUMENTS` identifies a target directory, work there; otherwise use the current project. Do not overwrite an existing `AGENTS.md`. If it exists, report which expected files are missing and ask before filling gaps.

Gather, unless already known from the conversation or repository:

- Project name
- One-line description
- Language/runtime, framework, and package manager
- Install, dev/run, test, lint/typecheck, and build commands

Read the templates in `~/.config/opencode/templates/project-init/` and substitute `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, and `{{DATE}}` using today's date in `YYYY-MM-DD` format. Create:

- `AGENTS.md` from `AGENTS.md.template`
- `CLAUDE.md` from `CLAUDE.md.template`
- `CLEANCODE.md` from `CLEANCODE.md.template`
- `docs/journal.md` from `journal.md.template`
- `docs/decisions.md` from `decisions.md.template`
- `TODO.md` from `TODO.md.template`

Also create `docs/designs/` with a `.gitkeep`, and `.claude/skills/` with a `.gitkeep` for project-specific Claude-compatible skills. Append `.claude/settings.local.json` to `.gitignore`, creating it if absent and avoiding duplicate entries.

Leave the Architecture section of `AGENTS.md` as a placeholder until the system has real shape. Do not invent architecture speculatively. Report what was created or left unchanged.
