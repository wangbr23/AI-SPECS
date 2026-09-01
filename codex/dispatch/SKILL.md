---
name: dispatch
description: Read TODO.md, compute the agent-ready task frontier, route workers by task complexity, run tasks in parallel in isolated worktrees, review each worker's diff, then merge the branches into the main worktree sequentially with conflict resolution and validation. Use when the user wants to build or integrate the next TODO wave with subagents.
---

# Dispatch

`plan-tasks` computes which tasks are safe to hand to parallel agents; this skill runs one wave at a time, keeps implementation context isolated in fresh workers, and integrates the reviewed branches one at a time.

## When to run

When `TODO.md` has unblocked `agent` tasks ready to build, or the user asks to build/implement the next wave, run tasks in parallel, or dispatch agents. Not for a single task done inline in the current conversation — that's just doing the work directly.

## Requires

The target project should already have `TODO.md` (from `project-init`) with tasks in `plan-tasks`' format. If it doesn't, say so and suggest running `plan-tasks` first rather than inventing task structure.

## Steps

### 1. Compute the frontier

Read `TODO.md` and apply `plan-tasks`' own rule verbatim — don't reimplement it differently:

- **Agent-ready set**: unchecked tasks tagged `agent` whose every `depends-on` id is already checked off.
- **Manual-ready set**: unchecked `manual` tasks whose dependencies are satisfied. Report these to the user separately; never let them block agent dispatch of unrelated tasks.
- Everything else is blocked. Don't dispatch it, don't wait on it.

If the agent-ready set is empty, say why (nothing ready yet / everything done / everything blocked on manual or unfinished work) and stop — this is a normal no-op, not an error.

### 2. Classify task complexity

Classify every task in the agent-ready set before launching workers, and include the classification and its brief rationale in the wave report:

- **Complex — `gpt-5.6-luna`**: the task requires substantial reasoning or judgment, such as changes across service or architectural boundaries, schema or migration work, concurrency, security or data-integrity concerns, ambiguous design tradeoffs, or a broad change whose effects must be traced through unfamiliar code.
- **Simple — `gpt-5.4-mini`**: the task is bounded and well specified, with localized or mechanical changes, clear acceptance criteria, and no material architectural or product tradeoff.

If the evidence is mixed, classify the task as complex. Complexity is about the reasoning needed, not estimated lines changed. Do not substitute a different model silently; if the selected model is unavailable, report the unavailable model and stop dispatching that task.

### 3. Assemble context per task

For every task in the agent-ready set, gather:

- The task's own `TODO.md` line (id, description, dependencies).
- `AGENTS.md` in full (repo conventions).
- `docs/decisions.md` in full (durable constraints already locked in).
- The governing design doc:
  - If the task has a `design:` field, use that path.
  - If it doesn't, and exactly one `docs/designs/*.md` exists, use that one.
  - If it doesn't, and more than one `docs/designs/*.md` exists, ask the user once which doc governs this batch before dispatching anything. Don't guess (e.g. by picking the most recently modified) — a wrong grounding doc is worse than asking.

### 4. Launch the wave

For every task in the agent-ready set, launch one **fresh** subagent using the model selected in step 2 (explicitly not a fork, since a fork would inherit this entire conversation, including every prior phase of the pipeline, into a task that only needs its own slice of context) with worktree isolation, all in a single message so they run concurrently.

Give each subagent only what it needs — the task line plus the context assembled in step 3 — and this exact instruction sequence:

1. Implement the task.
2. Run the `simplify` skill on your own diff (reuse/simplification cleanup, applies automatically).
3. Run `code-review --fix` on your own diff (correctness bugs, applies fixes).
4. Report back: what you built, what `simplify` and `code-review` changed or flagged (including anything left unfixed), and the worktree/branch it's on.

Doing steps 2–3 inside the worktree, before anyone reviews it, is what keeps tech debt from piling up wave over wave instead of accumulating for one big cleanup pass later.

Dispatch itself never sees a worker's intermediate tool calls, only its final report — the same as any backgrounded agent call. If a worker's own task needs sub-exploration, it can dispatch its own subagents for that; nothing extra is needed here for it to do so.

### 5. Reconcile as workers finish

Collect each subagent's report and confirm that implementation, simplification, correctness review, validation, and a branch commit all completed. A failed or uncommitted worker is not ready to integrate.

Do not copy implementation files through the main conversation or reimplement a worker's task in the main worktree. The worker branch is the artifact to integrate. Keep reports concise so implementation context stays isolated.

### 6. Integrate sequentially

Unless the user explicitly requests a review gate or asks not to merge, merge completed branches into the main worktree one at a time:

1. Choose an order that puts independent changes first and known overlapping changes next to each other, so conflicts are localized and understandable.
2. Inspect the branch summary and diff, then create a merge commit. Never flatten the worker branch by copying files.
3. If a conflict occurs, inspect both sides and their surrounding code. Resolve it by preserving the intended behavior of every already-integrated task and the incoming task; do not accept one side wholesale merely to finish the merge.
4. Run the relevant typecheck, lint, tests, and diff checks after each merge. Run the production build after the final merge, or earlier when a merge changes build-sensitive boundaries.
5. If validation fails, fix only integration defects, validate again, and record the fix in the merge commit. If correct resolution requires a product decision, stop and ask the user.
6. After a branch merges and validates, check off its task in the real `TODO.md`. Commit the TODO reconciliation after the wave is integrated.

Do not delete worker branches or worktrees unless the user asks; they remain useful review artifacts.

### 7. Report the wave, then stop

Once every ready branch has been integrated (or the user says stop), report one line per task: complexity classification and model, branch and commit, what was built, what `simplify` and `code-review` changed or flagged, merge result, and validation. Call out every conflict and how it was resolved.

## Notes

- Model routing is intentionally limited to the two complexity classes above. Do not add task tags, configurable routing, or more model tiers until a concrete requirement calls for them.
- Reserve this for genuinely parallel-safe waves. If the agent-ready set is a single task, it's often simpler to just do it inline rather than pay the overhead of a worktree and a subagent report round-trip — use judgment.
