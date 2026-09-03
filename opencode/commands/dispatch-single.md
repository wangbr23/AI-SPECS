---
description: Implement the next ready task in the current worktree and review it
agent: build
subtask: false
---

# Dispatch Single

Read `TODO.md` and compute the agent-ready frontier. An agent-ready task is an unchecked task tagged `agent` whose every `depends-on` task is checked off. Manual tasks are not agent-ready and must be reported separately.

Select the next ready task by lowest numeric task id. If no agent-ready task exists, report whether the list is empty, blocked, or waiting on manual work and stop. Do not invent a task or bypass a dependency.

Before editing, read `AGENTS.md`, `CLEANCODE.md`, relevant `docs/decisions.md`, and the task's `design:` document when present. Inspect the current worktree and preserve unrelated existing changes. Select the implementation agent from the task's `complexity` field: use `simple-builder` for `complexity: simple` and `complex-builder` for `complexity: complex`. Implement only the selected task, keeping the diff small and reviewable. Run the relevant verification commands from `AGENTS.md`.

After implementation and verification, invoke the `code-reviewer` subagent in the current worktree. Give it the task id and ask it to inspect the resulting diff. The reviewer is read-only and must report findings; it must not modify, commit, or reset files.

Do not automatically fix reviewer findings. Report:

- The selected task and why it was ready
- Files changed and verification results
- Code-reviewer findings, ordered by severity
- Existing unrelated changes that were preserved
- Whether the task is ready for the user to mark complete

Do not check off the task automatically unless the user explicitly asks for that reconciliation step.
