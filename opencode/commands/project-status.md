---
description: Report the current state of a project's durable context and work
agent: plan
---

Read the project's persistent context instead of re-deriving status from chat history or guessing from code alone.

If `$ARGUMENTS` identifies a project directory, inspect it; otherwise use the current project. Expect `AGENTS.md`, `docs/journal.md`, `docs/decisions.md`, `docs/designs/`, and `TODO.md` to exist, normally from `/project-init`. If files are missing, say which ones are missing and do not invent a summary.

Read `AGENTS.md` for stack, commands, architecture, and project conventions. Read `TODO.md` in full and identify completed, open, blocked, agent-ready, and manual work when its task format supports it. Read the last few entries of `docs/journal.md`, then read `docs/decisions.md` in full. List `docs/designs/` and skim recent designs related to likely next steps.

Compare the written context with the actual repository when a contradiction materially affects the status. Do not treat stale documentation as current without calling it out.

Report a concise synthesis:

- What is built
- What is in progress
- What is next according to `TODO.md`
- Relevant decisions and design constraints
- Stale, missing, or contradictory context

This command is read-only. Do not edit project context files.
