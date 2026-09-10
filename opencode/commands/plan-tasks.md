---
description: Break a feature or design into coverage-complete atomic tasks with validated dependencies
agent: build
---

# Plan Tasks

Load and follow the `plan-tasks` skill. Break the requested work into the smallest practical set of independently understandable, reviewable tasks. The objective is to keep each agent-produced diff small enough for a human to review in one sitting without creating needless coordination overhead.

The work to plan is: `$ARGUMENTS`

This is planning only. Do not implement, dispatch, or mark tasks complete.

## Grounding

Read `AGENTS.md` and `CLEANCODE.md` if they exist. Read the relevant design or spec documents and `docs/decisions.md` when present. When planning from a design, read both the HLD and its low-level design sibling (`<slug>-lld.md`) when one exists — the HLD for scope and decisions, the LLD for file layout, pinned mechanisms, and test mapping; the LLD's open questions belong in the requirement inventory. Read the existing `TODO.md` in full before changing it. If the request refers to a design document, use that document rather than reconstructing its contents from memory.

If the requested scope is ambiguous or contains unresolved product decisions, surface those decisions instead of encoding guesses as implementation tasks.

## Mandatory workflow

Do not edit `TODO.md` after producing only a first-pass list. Complete these passes in working notes first, then write the audited plan once:

1. **Requirement inventory** — enumerate every confirmed deliverable, lifecycle action, boundary, failure path, rollout constraint, and verification scenario from the source design or spec. Treat design sections as requirement sources, not task boundaries. Exclude stated non-goals.
2. **Draft task map** — map every inventory entry to a proposed task. Separate domain types, migrations, repositories, core rules, adapter surfaces, administrative actions, background handlers, observability, and cross-component verification when they can be reviewed independently.
3. **Atomicity audit** — inspect every proposed agent task using the task-sizing tests below. Split it before assigning ids when any test fails.
4. **Coverage audit** — reverse-check every inventory entry against the draft. Add omitted work rather than assuming another task includes it implicitly.
5. **Dependency audit** — add only real output or resource-conflict dependencies, check for cycles and dangling references, and compute the ready frontiers.
6. **Write and validate** — update `TODO.md`, then run `node ~/.config/opencode/skills/plan-tasks/validate-todo.mjs TODO.md`. Fix every validation error before reporting completion.

## Task sizing

Split work at real review boundaries, usually one of:

- One schema or data model
- One migration
- One endpoint or command
- One service or integration boundary
- One UI component or cohesive screen
- One focused test or documentation change

Each agent task should have one primary deliverable, one reason to change, and one focused acceptance story. Split tasks when they cross implementation layers, have separate likely failure modes, or can be reviewed and committed independently.

Treat all of these as mandatory split warnings, not just the word "and":

- Multiple independently meaningful verbs in one description
- A broad verb followed by a list of unrelated nouns
- One task covering schema, persistence, core behavior, adapter exposure, and end-to-end verification
- Multiple administrative mutations or multiple end-to-end scenarios
- An entire subsystem or database grouped only because the repository is currently empty

For persistence work, prefer one ordered migration per cohesive table family. For command or tool work, separate the surface from independently reviewable mutations. Keep focused unit tests with the behavior they verify; split out security, performance, contract, and end-to-end tests when they span components.

Do not split work that must change atomically to leave the repository valid, such as a type and its inseparable caller. Do not create artificial one-line tasks, tasks that only move code without a reviewable purpose, or tasks whose coordination and integration cost exceeds the review benefit. When uncertain, prefer the smaller reviewable task and document the dependency.

Security-sensitive state changes may remain one task when splitting would expose an invalid intermediate state. State that reason in the final report.

## Task format

Add normal Markdown checkboxes to `TODO.md`, one line per task:

```text
- [ ] `T7` Define the user schema — agent, complexity: simple, depends-on: T3, design: docs/designs/2026-08-20-users.md
- [ ] `T8` Get the external account approved — manual, design: docs/designs/2026-08-20-users.md
- [ ] `T9` Wire the invitation endpoint — agent, complexity: complex, depends-on: T7, design: docs/designs/2026-08-20-users.md
```

Every task needs:

- A sequential `T<n>` id. Find the highest id already in `TODO.md`; never reuse or renumber ids, including completed tasks.
- Either `agent` or `manual`.
- For `agent` tasks, `complexity: simple` or `complexity: complex`.
- `depends-on` only when ordering is a real requirement.
- `design` when the task came from a design document. When the design has a low-level design sibling (`<slug>-lld.md`), reference the LLD — it cross-links back to the HLD, so one path still reaches both.

Use `manual` for credentials, accounts, real-world actions, or unresolved human judgment. Use `agent` when the work can be completed and verified inside the repository.

When decomposing an existing unchecked task, keep its id for the closest remaining responsibility and append new ids for extracted work. Update its description and dependencies to match the narrowed responsibility. Never rewrite completed tasks, reuse ids, or renumber the file.

Classify complexity by judgment required, not line count:

- `simple`: narrow, mechanical work following an established project pattern
- `complex`: design judgment, multiple interacting systems, migrations, concurrency, security, or subtle correctness requirements

## Dependencies and frontier

Add `depends-on` for data/output dependencies and resource conflicts. If two tasks can safely run at the same time, leave both dependency-free. Headings are for human organization only; dependencies are the only ordering mechanism.

Do not report completion until the final file has passed both the semantic coverage/atomicity audits and the deterministic validator. Then report:

- Tasks added, with ids and complexity
- Dependencies that define the current agent-ready frontier
- Manual-ready tasks that require the user
- Any tasks deliberately kept together for atomicity
- Any unresolved decisions that block planning
- The validator result, including the manual-ready and agent-ready sets
