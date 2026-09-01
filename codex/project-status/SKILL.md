---
name: project-status
description: Read docs/designs/, docs/journal.md, docs/decisions.md, and TODO.md to build an up-to-date picture of a project and report it back. Use at the start of a session on an existing project, or when the user asks for the current state of the project, what's been done, or what's next.
---

# Project Status

The read-side counterpart to `project-init` (creates these files) and `save-progress` (keeps them updated) — this skill catches up on a project's real state from its persistent context files, instead of re-deriving it from chat history or guessing from the code alone.

## When to run

At the start of a session on an existing project, or when the user asks something like "what's the state of this project," "what have we done so far," "what's next," or "catch me up." Requires `docs/journal.md`, `docs/decisions.md`, `docs/designs/`, and `TODO.md` to already exist (from `project-init`) — if they don't, say so and don't invent a summary from thin air.

## Steps

1. Read `AGENTS.md` for stack/architecture context — what the project actually is and how it's built.
2. Read `TODO.md` in full — current and near-term work, what's checked off vs. open.
3. Read the last few entries of `docs/journal.md` — enough to know what's actively in progress and what changed most recently. Only go further back if the user asks for deeper history.
4. Read `docs/decisions.md` in full — architecture decisions that constrain how new work should be done. Recency matters more than exhaustive coverage here, but don't skip entries that look load-bearing.
5. List `docs/designs/` and skim the most recent design doc(s), especially any whose scope overlaps what the user is likely about to work on next.
6. Report a concise summary: what's built, what's in progress, what's next (from `TODO.md`), and any decisions or design constraints relevant to likely next steps. Synthesize — don't just dump file contents back at the user.

## Notes

- Read-only. Never edit these files as part of this skill — that's what `save-progress` is for.
- If the docs are stale or contradict what the code actually shows (e.g. `TODO.md` still marks something incomplete that's clearly shipped), say so rather than reporting stale information as current.
