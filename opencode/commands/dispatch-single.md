---
description: Implement one ready task in the current worktree with risk-based review
agent: build
subtask: false
---

# Dispatch Single

Read `TODO.md` and compute the agent-ready frontier. An agent-ready task is an unchecked task tagged `agent` whose every `depends-on` task is checked off. Manual tasks are not agent-ready and must be reported separately.

Parse `$ARGUMENTS` for an optional task id such as `T2` and an optional `--review` flag. If a task id is provided, select it only if it is agent-ready; otherwise report why it is unavailable and stop. If no task id is provided, select the ready task with the lowest numeric id. If no agent-ready task exists, report whether the list is empty, blocked, or waiting on manual work and stop. Do not invent a task or bypass a dependency.

Before editing, read `AGENTS.md`, `CLEANCODE.md`, relevant `docs/decisions.md`, and the task's `design:` document when present. Inspect the current worktree and preserve unrelated existing changes. Implement only the selected task yourself, in this session — do not delegate implementation to a subagent. Keep the diff small and reviewable. Run the relevant verification commands from `AGENTS.md`.

For `complexity: simple`, rely on your own self-review and successful verification. Do not launch a separate reviewer unless `$ARGUMENTS` includes `--review`.

For `complexity: complex`, or whenever `$ARGUMENTS` includes `--review`, invoke the `code-reviewer` subagent in the current worktree after implementation and verification. Give it the task id and ask it to inspect the resulting diff. The reviewer is read-only and must report findings; it must not modify, commit, or reset files.

Do not automatically fix reviewer findings. Report:

- The selected task and why it was ready
- Files changed and verification results
- Code-reviewer findings ordered by severity, or that review was skipped by policy
- Existing unrelated changes that were preserved
- Whether the task is ready for the user to mark complete

Do not check off the task automatically unless the user explicitly asks for that reconciliation step.
