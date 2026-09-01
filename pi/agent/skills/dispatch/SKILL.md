---
name: dispatch
description: Compute the ready task frontier from TODO.md and run implementation agents in isolated git worktrees, using DeepSeek V3.2 by default with escalation rules. Use after plan-tasks, when the user wants to implement the next wave of agent-ready tasks.
---

# Dispatch

Runs one implementation wave from `TODO.md`: compute the unblocked `agent` tasks, create one branch/worktree per task, run a separate Pi worker for each task, and report branches for human review. Dispatch never merges and does not check off tasks before human review.

## When to run

Run after `plan-tasks` has written structured tasks to `TODO.md`, or when the user asks to implement the next wave / dispatch agents.

Do not use for a single tiny task that is simpler to do directly in the current session.

## Requires

- Git repo with a clean or understood working tree.
- `TODO.md` using `plan-tasks` format.
- `AGENTS.md`.
- `CLEANCODE.md` if present.
- `docs/decisions.md` if present.
- Linked `docs/designs/*.md` files for design-driven tasks.
- Pi CLI available as `pi`.

If `TODO.md` or project context is missing, say so and suggest running `project-init` / `plan-tasks` first.

## Model policy

Default implementation model:

```bash
deepseek/deepseek-v3.2
```

Allow the user to override the worker model, e.g.:

```text
/skill:dispatch model=sonnet:low
/skill:dispatch model=deepseek/deepseek-v3.2
```

Use the default implementation model for normal, well-scoped planned tasks.

### Escalation rule

Workers must stop and report escalation instead of forcing a solution if:

- the task reveals a missing product or architecture decision;
- the design doc is insufficient or contradictory;
- implementation requires a large unexpected refactor;
- security/privacy implications are unclear;
- tests repeatedly fail after reasonable attempts;
- the resulting diff would be too large for human review;
- the worker is not confident it can complete safely.

Escalation means no broad implementation. The worker should preserve any useful partial investigation only if it is clearly safe and reviewable; otherwise it should leave the worktree unchanged or revert partial changes.

## Frontier computation

Read `TODO.md` and compute exactly:

- **Agent-ready set:** unchecked tasks tagged `agent` whose every `depends-on` id is already checked off.
- **Manual-ready set:** unchecked tasks tagged `manual` whose dependencies are satisfied. Report these separately; never let them block unrelated agent dispatch.
- **Blocked set:** everything else.

If the agent-ready set is empty, report why and stop.

## Reviewability rule

Every dispatched task should produce a diff small enough for a human to review, understand, and commit independently.

If a ready task appears too broad before dispatching, do not run it. Instead, recommend splitting it with `plan-tasks`.

## Steps

### 1. Inspect project state

1. Confirm this is a git repo.
2. Check `git status --short`.
3. If the working tree has unrelated uncommitted changes, ask before dispatching. Worktrees branch from the current HEAD, so dispatching from a messy base can confuse review.
4. Read:
   - `TODO.md`
   - `AGENTS.md`
   - `CLEANCODE.md` if present
   - `docs/decisions.md` if present

### 2. Compute the wave

Apply the frontier rules. Report:

- tasks that will be dispatched;
- manual-ready tasks;
- blocked tasks summary if useful.

If there are many ready tasks, ask before launching a large wave. Prefer small waves that keep human review manageable.

### 3. Resolve task context

For each agent-ready task, collect:

- task checkbox line and any indented `Done when:` lines;
- linked `design: docs/designs/*.md` file if present;
- relevant spec path if the design references `docs/specs/*.md`;
- project context files listed above.

If a task has no `design:` and multiple design docs exist, ask which design governs the batch. Do not guess.

### 4. Create isolated worktrees

For each task, create a task slug from the task title and add a worktree outside the repo directory, for example:

```bash
git worktree add ../<repo-name>-worktrees/<task-id>-<slug> -b dispatch/<task-id>-<slug>
```

Use unique paths/branch names. If a branch or worktree already exists, ask whether to reuse, remove, or choose a new name.

### 5. Launch Pi workers

Run one separate Pi subprocess per task, from inside that task's worktree. Use the selected implementation model.

Template:

```bash
cd <worktree-path> && pi --model deepseek/deepseek-v3.2 -p '<worker prompt>'
```

Workers may run concurrently when practical. If launching manually through Bash, background jobs are acceptable, but make sure logs are captured per task so reports are not lost.

### 6. Worker prompt

Each worker prompt must include only the context it needs and this instruction set:

```text
You are implementing one planned task in an isolated git worktree.

Task:
<TODO task line and Done when criteria>

Context to read before editing:
- AGENTS.md
- CLEANCODE.md if present
- docs/decisions.md if present
- <linked design doc>
- <linked spec doc if applicable>

Rules:
- Implement only this task.
- Do not broaden scope.
- Keep the diff human-reviewable: one coherent change a human can understand and commit independently.
- Follow CLEANCODE.md and AGENTS.md.
- Keep refactors separate unless tiny and directly required.
- Do not commit or merge.
- If the task is unclear, too broad, risky, or requires a missing decision/credential, stop and report escalation.
- Run relevant checks from AGENTS.md when available.

Final report format:
- Task id and title
- Status: implemented / partial / escalated / failed
- Branch and worktree path
- Files changed
- Summary of implementation
- Done criteria status
- Checks run and results
- Review notes: what the human should focus on
- Escalation reason, if any
```

### 7. Reconcile results

For each worker result:

- Inspect `git -C <worktree> status --short` and optionally `git -C <worktree> diff --stat`.
- Do **not** merge.
- Do **not** check off the task automatically. Tasks are checked off only after human review/merge unless the user explicitly asks otherwise.
- If a worker escalated, preserve its report and recommend the next planning/design decision.

### 8. Report the wave

Return a concise wave summary:

```md
## Dispatch wave complete

### Implemented, awaiting human review

- `T7` Add checkout API route only
  - Branch: dispatch/T7-checkout-api
  - Worktree: ../repo-worktrees/T7-checkout-api
  - Files changed: ...
  - Checks: ...
  - Done criteria: satisfied / partly satisfied
  - Review focus: ...

### Escalated

- `T9` Add webhook handler
  - Reason: design does not specify idempotency strategy
  - Suggested next step: decide policy, update design/TODO

### Manual-ready

- `T8` Get Stripe account approved
```

End after one wave. Running `dispatch` again recomputes the frontier after the human has reviewed, merged, and checked off completed tasks.

## Notes

- Dispatch is an implementation launcher, not a review/merge tool.
- Favor fewer, smaller tasks over a giant wave that overwhelms human review.
- If Pi subprocesses cannot use the selected model, stop and ask for a working model pattern rather than silently changing models.
