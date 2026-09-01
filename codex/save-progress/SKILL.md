---
name: save-progress
description: Review the work done this session and bring the project's persistent context files (docs/journal.md, docs/decisions.md, docs/designs/, TODO.md — set up by project-init) up to date, so the next session doesn't have to re-derive it from chat history. Use when wrapping up a work session, or when the user asks to close out, wrap up, or save session progress.
---

# Save Progress

Reconciles the docs/ context files against what actually happened this session. Complements `project-init`, which creates these files — this skill is what keeps them alive.

## When to run

At the end of a work session, or when the user asks to close out, wrap up, or save progress. Requires `docs/journal.md`, `docs/decisions.md`, `docs/designs/`, and `TODO.md` to already exist (from `project-init`). If they don't, say so and suggest running `project-init` first rather than inventing the layout.

## Steps

1. Establish the cutoff: read `docs/journal.md`'s last entry to see what was already recorded. Everything after that — in this conversation, and in `git log`/`git diff` if the project is a git repo — is in scope.

2. **Journal** — append one new entry to `docs/journal.md` (today's date, `YYYY-MM-DD`): what changed, why, what's next. Never edit past entries; if something turns out to have been wrong, say so in the new entry instead.

3. **Decisions** — for each significant technical decision made this session that isn't already recorded (dependency choices, schema/architecture calls, rejected approaches — not routine implementation detail), append an entry to `docs/decisions.md`. Skip this step entirely if nothing decision-worthy happened; don't force an entry.

4. **Designs** — for any design document produced this session (specs, mockups, research write-ups) that exists only in chat or as a published artifact and hasn't been saved into `docs/designs/`, save it there now.

5. **TODO** — update `TODO.md`: check off what got done, add near-term work that surfaced this session, drop anything that's gone stale or is no longer relevant.

6. Report back concisely what was updated in each of the four files — or, for any file with nothing new to record, say so rather than padding it.

## Notes

- Append-only means append-only: journal and decisions entries are never rewritten, only added to or superseded by a new entry.
- If it's ambiguous whether something rises to "decision-worthy," ask rather than guessing — a memory-log entry that's too noisy is as useless as one that's missing.
