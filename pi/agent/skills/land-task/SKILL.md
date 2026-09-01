---
name: land-task
description: Human-gated finalization for a dispatched task branch: summarize the diff and review state, ask approval, merge only after approval, check off TODO.md, and optionally clean up the worktree/branch. Use after dispatch and code-review when a task is ready to land.
---

# Land Task

Finalize one implemented task after human review. This is the merge/checkoff step that `dispatch` intentionally does not do.

## Relationship to dispatch

`land-task` is part of the broader dispatch workflow, but it is a separate skill and human gate:

```text
dispatch -> code-review -> human reviews diff -> land-task -> dispatch next wave
```

Keep it separate so implementation agents cannot silently merge their own work or mark tasks complete before the human has reviewed them.

## When to run

Run when a dispatched task branch/worktree has been implemented, reviewed, and the human is ready to decide whether to merge it.

Do not run if:

- the branch has unresolved blocker findings;
- the human has not reviewed or approved the diff;
- the target base branch is unclear;
- the task id cannot be matched to `TODO.md`.

## Inputs

Accept any of:

- task id: `T7`
- branch: `dispatch/T7-checkout-api`
- worktree path: `../repo-worktrees/T7-checkout-api`
- explicit base branch: `base=main`

If the task, branch, worktree, or base branch is ambiguous, ask before making changes.

## Steps

### 1. Identify task and branch

Read `TODO.md` and find the matching unchecked task. Determine:

- task id and title;
- branch name;
- worktree path if present;
- base branch to merge into, usually `main` unless the user specifies otherwise.

Confirm the task line includes `agent` and is not already checked off. If it is already checked off, stop and ask what the user wants.

### 2. Inspect landing state

Run read-only checks first:

```bash
git status --short
git branch --show-current
git diff --stat <base>...<branch>
git diff --name-only <base>...<branch>
```

If using a worktree, run equivalent commands with `git -C <worktree>`.

Check for:

- uncommitted changes in the task worktree;
- whether the branch is behind/diverged from base;
- merge conflicts likely to occur;
- unexpected files changed;
- diff size that is too large for comfortable human review.

If the branch has uncommitted changes, ask whether to commit them before merging, leave them, or stop. Do not auto-commit without approval.

### 3. Summarize for approval

Before merging or editing TODO, show:

```md
## Ready to land?

Task: `T7` <title>
Branch: <branch>
Base: <base>
Worktree: <path if any>

Changed files:
- ...

Diff stat:
...

Review/check status:
- Code review: passed / findings remain / not run / unknown
- Checks: ...

TODO action:
- Mark `T7` complete in TODO.md after merge.
```

Then ask for explicit approval:

```text
Merge this branch into <base> and mark <task-id> complete?
```

Do not proceed without an affirmative answer.

### 4. Merge after approval

After approval:

1. Switch to the base branch in the main repo.
2. Ensure base is clean enough to merge.
3. Merge the task branch using the repo's normal style. If no style is specified, use a non-fast-forward merge for traceability unless the user requests squash/ff-only.

Example:

```bash
git checkout <base>
git merge --no-ff <branch>
```

If conflicts occur, stop and report. Do not invent conflict resolutions unless the user asks.

### 5. Check off TODO

After a successful merge, edit `TODO.md` and change only the matching task checkbox:

```md
- [ ] `T7` ...
```

to:

```md
- [x] `T7` ...
```

Do not renumber tasks. Do not check off dependencies or related tasks unless explicitly approved.

### 6. Optional cleanup

Ask whether to clean up the landed worktree/branch. If approved:

```bash
git worktree remove <worktree-path>
git branch -d <branch>
```

Use `-D` only if the user explicitly asks and understands it is force deletion.

### 7. Report

Final report:

```md
## Landed task

- Task: `T7` <title>
- Merged: <branch> -> <base>
- TODO: marked complete
- Commit: <merge commit hash>
- Cleanup: worktree removed / branch deleted / left intact
- Next: run `dispatch` again to compute the next frontier
```

## Notes

- Never merge without explicit human approval.
- Never mark TODO complete before a successful merge unless the user explicitly wants a different policy.
- If review findings remain, surface them before asking for approval.
- Landing one task at a time keeps the history and review loop understandable.
