---
description: Break a feature or design into small, reviewable tasks with explicit dependencies
agent: build
---

# Plan Tasks

Break the requested work into the smallest practical set of independently understandable, reviewable tasks. The objective is to keep each agent-produced diff small enough for a human to review in one sitting without creating needless coordination overhead.

The work to plan is: `$ARGUMENTS`

## Grounding

Read `AGENTS.md` and `CLEANCODE.md` if they exist. Read the relevant design or spec documents and `docs/decisions.md` when present. Read the existing `TODO.md` in full before changing it. If the request refers to a design document, use that document rather than reconstructing its contents from memory.

If the requested scope is ambiguous or contains unresolved product decisions, surface those decisions instead of encoding guesses as implementation tasks.

## Task sizing

Split work at real review boundaries, usually one of:

- One schema or data model
- One migration
- One endpoint or command
- One service or integration boundary
- One UI component or cohesive screen
- One focused test or documentation change

Split tasks when they have separate concerns, separate likely failure modes, or can be reviewed and committed independently. If a description contains "and" joining two different concerns, treat that as a likely split point.

Do not split work that must change atomically to leave the repository valid, such as a type and its inseparable caller. Do not create artificial one-line tasks, tasks that only move code without a reviewable purpose, or tasks whose coordination and integration cost exceeds the review benefit. When uncertain, prefer the smaller reviewable task and document the dependency.

## Task format

Add normal Markdown checkboxes to `TODO.md`, one line per task:

```text
- [ ] `T7` Define the user schema — agent, complexity: simple, depends-on: T3, design: docs/designs/2026-08-20-users.md
- [ ] `T8` Get the external account approved — manual
- [ ] `T9` Wire the invitation endpoint — agent, complexity: complex, depends-on: T7, design: docs/designs/2026-08-20-users.md
```

Every task needs:

- A sequential `T<n>` id. Find the highest id already in `TODO.md`; never reuse or renumber ids, including completed tasks.
- Either `agent` or `manual`.
- For `agent` tasks, `complexity: simple` or `complexity: complex`.
- `depends-on` only when ordering is a real requirement.
- `design` when the task came from a design document.

Use `manual` for credentials, accounts, real-world actions, or unresolved human judgment. Use `agent` when the work can be completed and verified inside the repository.

Classify complexity by judgment required, not line count:

- `simple`: narrow, mechanical work following an established project pattern
- `complex`: design judgment, multiple interacting systems, migrations, concurrency, security, or subtle correctness requirements

## Dependencies and frontier

Add `depends-on` for data/output dependencies and resource conflicts. If two tasks can safely run at the same time, leave both dependency-free. Headings are for human organization only; dependencies are the only ordering mechanism.

After editing `TODO.md`, report:

- Tasks added, with ids and complexity
- Dependencies that define the current agent-ready frontier
- Manual-ready tasks that require the user
- Any tasks deliberately kept together for atomicity
- Any unresolved decisions that block planning
