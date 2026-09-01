---
name: code-review
description: Review an implementation branch or current diff against its TODO task, design doc, specs, AGENTS.md, and CLEANCODE.md. Uses a read-only reviewer model by default and reports correctness, security, test, scope, and reviewability findings before human merge.
---

# Code Review

Review a completed implementation task before the human merges it. This is a diff-focused correctness and quality gate, not a whole-codebase cleanup pass.

## When to run

Run after `dispatch` reports a task branch/worktree is implemented and awaiting human review, or whenever the user asks to review a branch/diff before merge.

Do not use for broad repo health audits; use `code-cleanup` for that later.

## Review goals

Check whether the implementation:

- satisfies the TODO task and its `Done when:` criteria;
- follows the linked design doc and product spec;
- respects `AGENTS.md`, `CLEANCODE.md`, and `docs/decisions.md`;
- is correct, secure, and maintainable;
- keeps the diff human-reviewable;
- avoids hidden scope expansion, unrelated refactors, or speculative complexity;
- has adequate tests or verification for the change.

## Model policy

Default reviewer model:

```bash
deepseek/deepseek-r1
```

The current Pi agent coordinates the review, gathers context, and synthesizes findings. The reviewer subprocess should be read-only:

```bash
pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "<review prompt>"
```

Allow override when invoked, e.g.:

```text
/skill:code-review model=sonnet:high branch=dispatch/T7-checkout-api
```

If the configured reviewer model is unavailable, stop and ask for a working model pattern instead of silently substituting.

## Inputs

Accept any of these review targets:

- current working tree diff;
- a dispatch worktree path;
- a branch name;
- a task id like `T7`.

If only a task id is given, find the corresponding TODO entry and ask for the branch/worktree if it is ambiguous.

## Steps

### 1. Establish review target

Determine what is being reviewed:

- current repo diff, or
- `branch` compared to its base, or
- `worktree` compared to its base.

Run appropriate read-only git inspection commands, such as:

```bash
git status --short
git branch --show-current
git diff --stat
git diff --name-only
git diff
```

For a branch/worktree, compare against the branch point or main branch. If the base is ambiguous, ask the user.

### 2. Gather grounding context

Read:

- `AGENTS.md`
- `CLEANCODE.md` if present
- `TODO.md`
- `docs/decisions.md` if present
- the matching TODO task and its `Done when:` criteria
- linked `design: docs/designs/*.md` if present
- linked/referenced `docs/specs/*.md` if present
- changed files and relevant neighboring code

Do not review from the diff alone if task/design context exists.

### 3. Run read-only reviewer

Launch the reviewer model with read-only tools and a prompt like:

```text
Review this implementation before human merge.

Target: <branch/worktree/current diff>
Task: <TODO task line and Done when criteria>
Design: <design path or none>
Spec: <spec path or none>

Read AGENTS.md, CLEANCODE.md if present, docs/decisions.md if present, TODO.md, the linked design/spec docs, and the changed files.

Check specifically:
1. Does the implementation satisfy the task and Done when criteria?
2. Does it match the design/spec and avoid scope creep?
3. Are there correctness bugs, edge cases, race conditions, or broken assumptions?
4. Are there security, privacy, auth, validation, or data-exposure issues?
5. Are tests/verification adequate?
6. Is the diff small and coherent enough for human review?
7. Are there unrelated refactors, dead code, debug logs, type-safety erosion, or convention violations?

Report findings only. Do not edit files. For each finding include:
- title
- severity: blocker / important / minor
- file(s)
- why it matters
- suggested fix
- confidence

Also state whether you think this is ready for human review after fixes.
```

If the diff is small and the user wants a faster inline review, the current agent may perform the review directly, but default to the independent reviewer for dispatch outputs.

### 4. Synthesize findings

The current agent reads the reviewer output and produces a final review report. Do not mechanically trust the reviewer; weigh findings against the code and context.

Classify findings:

- **Blocker** — should be fixed before human review/merge.
- **Important** — likely worth fixing, but not necessarily merge-blocking if the human accepts the tradeoff.
- **Minor** — polish, clarity, or low-risk maintainability.
- **No action** — reviewer concern does not hold up; explain briefly if relevant.

### 5. Optional fix mode

If invoked with `--fix`, apply only unambiguous, localized fixes:

- clear correctness bugs;
- missing validation called out by the design/task;
- failing tests with obvious cause;
- debug logs/unused imports/dead code introduced by the diff;
- small convention violations.

Do not apply broad refactors, architecture changes, product behavior changes, or anything that would make the diff no longer human-reviewable. Ask first.

After fixes, rerun relevant checks.

### 6. Report

Final report format:

```md
## Code review: <target>

Task: `T7` <title>
Design: <path>
Reviewer model: deepseek/deepseek-r1

### Verdict
Ready for human review / Needs fixes / Escalate decision

### Findings
- [blocker] <title> — <files>
  - Why it matters: ...
  - Suggested fix: ...
  - Confidence: ...

### Done criteria
- ... satisfied / not satisfied

### Checks
- <command>: passed/failed/not run

### Review focus for human
- ...
```

Do not merge. Do not check off TODO unless the user explicitly says the task has been reviewed and merged.

## Notes

- This skill is branch/diff-scoped. It is not a substitute for `code-cleanup` after several waves.
- Prefer fixing small concrete issues over expanding scope.
- If the review reveals missing requirements or architecture decisions, escalate to the user and update design/tasks before continuing.
