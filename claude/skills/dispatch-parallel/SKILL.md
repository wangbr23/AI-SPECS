---
name: dispatch-parallel
description: Implement ready tasks in isolated worktrees with risk-based review
disable-model-invocation: true
---

# Dispatch Parallel

Read `TODO.md` and compute the complete agent-ready frontier. An agent-ready task is an unchecked task tagged `agent` whose every `depends-on` task is checked off. Report manual-ready tasks separately and do not dispatch blocked tasks.

If there are no agent-ready tasks, report why and stop. If the repository is not a git worktree, report that separate worktrees are unavailable and stop. Before creating worktrees, check `git status --porcelain`. If the main worktree has changes, do not stash, reset, or silently include them; report the dirty paths and ask the user whether to proceed after they are committed or otherwise resolved.

For each ready task:

1. Create a unique git worktree from the current `HEAD`, with a branch named `agent/<task-id>-<slug>` under a temporary sibling directory such as `../.claude-worktrees/`.
2. Launch one independent implementation subagent with the `task` tool, instructing it to work in that worktree directory. Select `simple-builder` for `complexity: simple` and `complex-builder` for `complexity: complex`. Give it only the task line, the worktree path, and paths to `AGENTS.md`, `CLEANCODE.md`, `docs/decisions.md`, and the task's `design:` document. The worker must read those files itself.
3. Require the worker to implement only its task, keep the diff small and reviewable, run relevant verification, and report changed files and results. It must not modify other worktrees or the main worktree.
4. For `complexity: simple`, rely on the builder's self-review and successful verification; do not launch a separate reviewer. For `complexity: complex`, after the worker finishes, launch a separate read-only review subagent with the `task` tool (`code-reviewer` agent) in the same worktree. Give it the task id and ask it to review the implementation diff.
5. Keep each worktree and branch intact. Do not merge, cherry-pick, rebase, delete worktrees, or check off TODO items automatically.

Run independent implementation sessions concurrently across tasks where practical. Run each required complex-task review only after its implementation session finishes. Wait for the full wave before reporting.

Report one section per task containing:

- Task id, branch, and worktree path
- Implementation result and verification
- Code-reviewer findings ordered by severity, or that review was skipped for a simple task
- Anything unresolved or needing user action

Also report manual-ready and blocked tasks. The user reviews and integrates each branch before the next dispatch wave.
