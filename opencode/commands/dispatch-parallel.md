---
description: Implement all currently ready tasks in isolated git worktrees and review each result
agent: build
subtask: false
---

# Dispatch Parallel

Read `TODO.md` and compute the complete agent-ready frontier. An agent-ready task is an unchecked task tagged `agent` whose every `depends-on` task is checked off. Report manual-ready tasks separately and do not dispatch blocked tasks.

If there are no agent-ready tasks, report why and stop. If the repository is not a git worktree, report that separate worktrees are unavailable and stop. Before creating worktrees, check `git status --porcelain`. If the main worktree has changes, do not stash, reset, or silently include them; report the dirty paths and ask the user whether to proceed after they are committed or otherwise resolved.

For each ready task:

1. Create a unique git worktree from the current `HEAD`, with a branch named `agent/<task-id>-<slug>` under a temporary sibling directory such as `../.opencode-worktrees/`.
2. Launch one independent OpenCode implementation session in that worktree using `opencode run --dir <worktree> --agent <implementation-agent>`. Select `simple-builder` for `complexity: simple` and `complex-builder` for `complexity: complex`. Give it only the task line, the worktree path, and paths to `AGENTS.md`, `CLEANCODE.md`, `docs/decisions.md`, and the task's `design:` document. The worker must read those files itself.
3. Require the worker to implement only its task, keep the diff small and reviewable, run relevant verification, and report changed files and results. It must not modify other worktrees or the main worktree.
4. After that worker finishes, launch a separate read-only OpenCode session in the same worktree using `opencode run --dir <worktree> --agent code-reviewer`. Give it the task id and ask it to review the implementation diff.
5. Keep each worktree and branch intact. Do not merge, cherry-pick, rebase, delete worktrees, or check off TODO items automatically.

Run independent implementation and review sessions concurrently across tasks where practical, but ensure each review starts only after its own implementation session finishes. Wait for the full wave before reporting.

Report one section per task containing:

- Task id, branch, and worktree path
- Implementation result and verification
- Code-reviewer findings ordered by severity
- Anything unresolved or needing user action

Also report manual-ready and blocked tasks. The user reviews and integrates each branch before the next dispatch wave.
