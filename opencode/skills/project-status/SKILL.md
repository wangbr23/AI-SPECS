---
name: project-status
description: Read a project's durable context files and report what is built, in progress, next, and constrained by prior decisions. Use at the start of a session on an existing project or when the user asks for project status, progress, current state, or next steps.
---

# Project Status

Read the project's persistent context instead of re-deriving status from chat history or guessing from the code alone.

## When to run

Run at the start of a session on an existing project, or when the user asks what has been done, what is in progress, what is next, or for a catch-up.

This skill expects `AGENTS.md`, `docs/journal.md`, `docs/decisions.md`, `docs/designs/`, and `TODO.md` to exist, normally from `project-init`. If they do not exist, say which files are missing and suggest running `project-init`; do not invent a project summary from thin air.

## Steps

1. Read `AGENTS.md` for the stack, commands, architecture, and project-specific conventions.
2. Read `TODO.md` in full. Identify completed, open, blocked, agent-ready, and manual work when the task format supports it.
3. Read the last few entries of `docs/journal.md` to understand recent work and active threads. Read further back only if needed.
4. Read `docs/decisions.md` in full and identify decisions that constrain likely next work.
5. List `docs/designs/` and skim recent design documents, especially those related to likely next steps.
6. Compare the written context with the actual repository when a contradiction is apparent or materially affects the status. Do not treat stale documentation as current without calling it out.
7. Report a concise synthesis:
   - What is built
   - What is in progress
   - What is next according to `TODO.md`
   - Relevant decisions and design constraints
   - Stale, missing, or contradictory context

## Constraints

- Read-only: never edit project context files as part of this skill. Use `save-progress` for updates.
- Do not dump entire files back to the user; synthesize the relevant state.
- Do not infer completion solely from unchecked or checked TODO items when the code and journal clearly disagree. Report the discrepancy.
