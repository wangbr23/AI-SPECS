---
name: plan-tasks
description: Break work into coverage-complete atomic tasks in TODO.md with ids, manual/agent tags, and validated dependency frontiers. Use when creating or adding tasks, decomposing a design, auditing task granularity, or preparing work for parallel dispatch.
---

# Plan Tasks

Task lists break down the moment "what can run in parallel" is tracked by which section a task sits in — a task's blockers change as work completes, and a fixed Parallel/Reliant split needs constant hand-maintenance to stay correct. Instead, give each task an id and let it declare what it's blocked by; "safe to parallelize" becomes something computed on demand, not stored.

A planner is not finished after writing the first plausible list. It must prove both directions: every confirmed requirement maps to a task, and every task is the smallest practical review unit rather than a feature-sized placeholder.

## Task format

One line per task in `TODO.md`, still a normal markdown checkbox:

```
- [ ] `T7` Define Drizzle schema for users/follows — agent, complexity: simple, depends-on: T3, T5, design: docs/designs/2026-08-20-social-graph.md
- [ ] `T8` Get Stripe account approved — manual
- [ ] `T9` Wire up checkout flow — agent, complexity: complex, depends-on: T8, design: docs/designs/2026-08-23-checkout.md
```

- **id** — `T<n>`, sequential. Scan the file for the highest existing `T<n>` and increment; never reuse or renumber an id, including after its task is checked off, so old `depends-on` references never dangle or collide.
- **manual vs agent** — `manual` if it needs something only the human can do: real-world accounts/credentials, a judgment call that isn't yet resolved, anything outside the repo. Otherwise `agent`.
- **complexity** (required for `agent` tasks) — `simple` or `complex`. This is what `dispatch` uses to route the task to a cheap/fast model vs. a stronger-reasoning one (see its own doc for the exact mapping) — don't skip it thinking it's cosmetic. Classify by what the task actually demands, not its line count:
  - `simple` — mechanical/narrow: config wiring, CRUD boilerplate, docs, a refactor following a pattern already established elsewhere in the repo. A fast/cheap model reliably gets these right in one pass.
  - `complex` — anything needing real design or algorithmic judgment, touching multiple interacting systems, or with subtle correctness constraints (concurrency, migrations, security-sensitive logic).
  - Omit only for `manual` tasks, where it doesn't apply.
- **depends-on** (optional) — ids of tasks that must be checked off first. Omit entirely when there's no dependency — that absence is what makes a task part of the parallel-safe frontier.
- **design** (optional) — path to the `docs/designs/*.md` doc this task was broken out of. Write it whenever the task originates from a design doc, since that's the only point where the link is cheap to record; omit for ad-hoc tasks added outside a design pass. This is what lets a dispatcher hand a task's worker the right grounding doc without guessing, once a project has more than one design doc on file. When the design has a low-level design sibling (`<slug>-lld.md`, from the low-level-design skill), reference the LLD — it cross-links back to the HLD, so one path still reaches both.

Headings/grouping by feature or story are fine for human readability, but they carry no ordering meaning — sibling tasks under one heading can still be parallel-safe, and tasks under different headings can still block each other. `depends-on` is the only thing that encodes a real constraint.

## What counts as a dependency

Add `depends-on` whenever running two tasks out of order, or at the same time, would break something:

- **Data/output dependency** — task B needs something task A produces (a provisioned resource, a schema, a decision).
- **Resource conflict** — tasks A and B would touch the same files or state even though neither's output feeds the other. There's no separate "conflict" relation — just pick an order and encode it as `depends-on` like any other blocker.

If neither applies, leave both dependency-free. That's the actual test for "these are parallel-safe," not a subjective sense that they're "different enough."

## Task granularity

For `agent` tasks that touch code, size each one to a single diff a human can actually review in one sitting. Small is the default; only bundle work that genuinely cannot leave the repository valid or the state transition safe when split.

An atomic task has:

- One primary deliverable
- One reason to change
- One focused acceptance story
- One likely implementation area, allowing its direct tests

Ask these questions for every proposed agent task:

1. Could either half be implemented, tested, and committed without the other?
2. Does it cross layers such as domain types, migration, repository, core behavior, adapter, command/tool surface, worker integration, or end-to-end verification?
3. Does it contain multiple independently meaningful verbs or a broad verb followed by a list of unrelated nouns?
4. Do its parts have different failure modes or require different review expertise?
5. Would a reviewer reasonably want to approve or revert one part without the others?

If any answer is yes, split the task and encode a dependency only when one part truly requires the other's output or would conflict on the same files/state.

Common review boundaries:

- One cohesive domain model or state machine
- One migration for one table family, including its upgrade test
- One repository
- One core rule or algorithm
- One endpoint, command, tool, or administrative mutation
- One adapter or worker handler
- One UI component or cohesive screen
- One security, performance, contract, or end-to-end scenario

Do not use one task per design section. Design sections describe product concerns; they commonly contain several review boundaries. In particular, do not bundle an entire initial database, all lifecycle actions, all command actions, or all verification bullets into one task merely because the repository is empty.

Keep focused unit or behavior tests with the implementation they verify. Split a test into its own task when it crosses components, requires a special environment or fixture corpus, measures performance, verifies a security boundary, or represents a full end-to-end scenario.

Retain genuinely atomic work:

- A type and its only inseparable caller
- A transactional state change whose intermediate state would be invalid or unsafe
- One validator covering multiple cases of the same invariant
- One command's parsing, dispatch, and output when none is independently useful

`manual` tasks are not held to diff sizing. If unsure whether an agent task is reviewable at a glance, split it further. Over-splitting adds some coordination cost; under-splitting creates a diff nobody can confidently review.

## Mandatory planning workflow

Complete all passes before reporting. Do not edit `TODO.md` during the first draft unless the user explicitly asks to see an intermediate plan.

### 1. Ground and inventory

Read `TODO.md` in full plus the relevant `AGENTS.md`, design, spec, decisions, and current code. When planning from a design, read both the HLD and its low-level design sibling (`<slug>-lld.md`) when one exists — the HLD for scope and decisions, the LLD for file layout, pinned mechanisms, and test mapping; the LLD's open questions belong in the requirement inventory. Build a temporary requirement inventory covering:

- Domain concepts and lifecycle transitions
- Persistence schemas, migrations, retention, deletion, and export
- Core rules and conflict behavior
- Integration and adapter surfaces
- Commands, tools, administrative actions, and manual setup
- Background jobs, recovery, and concurrency
- Privacy, authorization, outbound-data, and failure paths
- Metrics and observability
- Unit, contract, security, performance, and end-to-end verification

Include every confirmed rollout and verification bullet. Exclude explicit non-goals. Surface unresolved product decisions instead of inventing tasks for guessed behavior.

### 2. Draft without ids

Map each inventory entry to a proposed task. A requirement may need several tasks across layers. Multiple requirements may share one task only when they pass every atomicity question above.

### 3. Audit atomicity

Read every draft task individually. Scan not only for the word "and," but also comma-separated deliverable lists, slash-separated concerns, multiple verbs, multiple actions, and phrases such as "end to end" that hide several scenarios. Split every independent concern before assigning ids.

### 4. Audit coverage

Reverse-map every inventory entry to at least one task. Do not treat privacy, authorization, deletion, export, observability, error handling, or verification as implied acceptance criteria when they require independently reviewable code. Add missing tasks before writing the file.

### 5. Build the dependency graph

Add only data/output and resource-conflict dependencies. Do not encode feature order, rollout prose, or a subjective preference as a dependency. Check that each dependency points to the smallest task that produces the needed output.

### 6. Assign ids and write once

Find the highest `T<n>` in `TODO.md`, assign new ids sequentially, and write the audited plan.

For a new plan, append new tasks. When decomposing an existing unchecked task, preserve its id for the closest remaining responsibility, append new ids for extracted work, and update dependencies to match the narrowed responsibility. Never rewrite completed tasks, reuse an id, or renumber existing ids.

### 7. Validate the final file

Run the bundled validator from the target project directory:

```bash
node ~/.config/opencode/skills/plan-tasks/validate-todo.mjs TODO.md
```

It must pass before reporting completion. Then read the final task descriptions once more for semantic atomicity, because structural validation cannot detect bundled concerns.

The validator checks:

- Sequential, unique ids in file order
- Valid manual/agent metadata and required agent complexity
- Existing design paths when supplied
- Well-formed, existing, unique, non-self dependencies
- An acyclic dependency graph
- Current manual-ready and agent-ready frontiers

## Computing the frontier (what can run now)

When asked what's safe to parallelize, or before dispatching multiple agents:

- **Agent-ready set**: unchecked tasks tagged `agent` whose every `depends-on` id is already checked off. These can be dispatched to different agents simultaneously — that's the actual point of the format.
- **Manual-ready set**: unchecked `manual` tasks whose dependencies are satisfied — report these to the human separately; don't let them silently block agent dispatch of unrelated tasks.
- Everything else is blocked — don't dispatch it, and don't wait on it before dispatching the ready set.

Checking off a task (`[x]`) is what advances the frontier — nothing else needs to move or get re-sorted.
