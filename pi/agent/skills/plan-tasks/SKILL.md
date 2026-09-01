---
name: plan-tasks
description: Break work into small, human-reviewable tasks in TODO.md with ids, manual/agent tags, depends-on links, done criteria, and design references. Use after design-review, when creating or adding tasks, or before dispatching multiple agents.
---

# Plan Tasks

Break a design into tasks that agents can execute safely and humans can review confidently. Parallelism is computed from dependencies; reviewability is enforced by task size.

## Core rule: reviewable diffs

Every `agent` coding task should produce a diff small enough for a human to review, understand, and commit independently.

Default guidance:

- One coherent change per task.
- Clear completion condition.
- Touch only related files/layers.
- Avoid mixing setup, refactor, schema, API, UI, styling, and tests unless the combination is tiny and necessary.
- If a task would produce a broad or hard-to-review diff, split it and use `depends-on` to preserve ordering.
- Keep refactors separate from feature work unless the refactor is very small and directly required.
- Keep dependency/tooling setup separate from product behavior.

Allowed exceptions include initial project scaffolding, mechanical renames, generated files, and unavoidable repo-wide migrations. Mark those clearly in the task description.

## Task format

Use normal markdown checkboxes in `TODO.md`:

```md
- [ ] `T7` Define Drizzle schema for users/follows — agent, depends-on: T3, T5, design: docs/designs/2026-08-20-social-graph.md
  - Done when: schema exports compile, migrations are generated, and existing DB tests pass.
- [ ] `T8` Get Stripe account approved — manual
  - Done when: live account is approved and webhook signing secret is available locally.
- [ ] `T9` Add checkout API route only, no UI — agent, depends-on: T8, design: docs/designs/2026-08-23-checkout.md
  - Done when: route creates a checkout session, errors are handled, and route tests pass.
```

- **id** — `T<n>`, sequential. Scan for the highest existing `T<n>` and increment. Never reuse or renumber ids.
- **manual vs agent** — `manual` if it needs the human: accounts, credentials, external approvals, judgment calls, or work outside the repo. Otherwise `agent`.
- **depends-on** (optional) — ids that must be checked off first. Omit when there is no dependency.
- **design** (optional) — path to the governing `docs/designs/*.md`. Include it for tasks created from a design doc.
- **Done when** — add for every nontrivial task. It should make completion observable: behavior, files, tests/checks, or manual confirmation.

Headings/grouping by feature or story are fine for readability, but carry no ordering meaning. `depends-on` is the only ordering mechanism.

## Splitting tasks

Split by the smallest coherent review unit:

- **Setup before behavior** — install/configure dependencies separately from feature logic.
- **Data before users of data** — schema/types/storage first, then API/services, then UI.
- **One layer at a time** — backend route, frontend component, and styling should usually be separate tasks.
- **Refactor before feature** — if cleanup is needed, make it its own task and depend on it.
- **Tests with implementation** — include tests in the same task when they are small and clarify behavior; split test-only hardening if it becomes large.
- **Explicit scope boundaries** — use phrases like “API only, no UI” or “UI only, uses existing mock data” when that keeps the diff reviewable.

If a task cannot be made reviewable without losing coherence, keep it whole but call out why.

## Stop / escalate conditions

When planning, create `manual` tasks or explicit blockers for anything that requires:

- a product decision not settled in the spec/design;
- credentials, accounts, approvals, or external services;
- a risky architecture decision;
- a large unexpected refactor;
- unclear security/privacy implications;
- work whose output would be too large for human review unless split.

Do not hide these inside an `agent` task.

## What counts as a dependency

Add `depends-on` whenever running two tasks out of order or concurrently would break something:

- **Data/output dependency** — task B needs something task A produces.
- **Resource conflict** — tasks would touch the same files/state in conflicting ways. Pick an order and encode it with `depends-on`.
- **Decision dependency** — an agent task depends on a manual decision or approval.

If neither applies, leave both dependency-free. That is the actual test for parallel safety.

## Assigning tasks

1. Read `AGENTS.md`, `CLEANCODE.md` if present, existing `TODO.md`, and the governing design doc.
2. Find the highest existing `T<n>` in `TODO.md`.
3. Break the design into reviewable tasks using the splitting rules above.
4. For each task, write the description, classify `manual`/`agent`, add real dependencies, record `design:` when applicable, and add `Done when:` for nontrivial work.
5. Append new tasks. Do not retroactively renumber existing tasks.
6. Report the first ready frontier after writing tasks.

## Computing the frontier

When asked what can run now, or before dispatching agents:

- **Agent-ready set:** unchecked `agent` tasks whose every `depends-on` id is already checked off.
- **Manual-ready set:** unchecked `manual` tasks whose dependencies are satisfied. Report these separately; do not let them silently block unrelated agent dispatch.
- **Blocked set:** everything else.

Checking off a task (`[x]`) is what advances the frontier.
