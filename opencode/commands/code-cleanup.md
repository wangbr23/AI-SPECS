---
description: Audit the current task for focused cleanup opportunities without scanning the whole repository
agent: build
subtask: false
---

# Code Cleanup

Audit only the code touched by the current task. Do not perform a whole-repository cleanup unless the user explicitly asks for that scope.

The task or scope to clean up is: `$ARGUMENTS`

## Establish scope

If `$ARGUMENTS` names files, a module, a task id, a branch, or a commit range, use that as the scope. If no scope is provided, inspect the current diff and its directly affected files. Do not expand into unrelated callers or neighboring modules unless needed to understand a finding.

Before reviewing, read `AGENTS.md` and `CLEANCODE.md` when present, plus the relevant design or decision document. Use those project conventions as the yardstick rather than a generic style checklist.

## What to look for

- Dead code, unused imports, debug logging, and leftover scaffolding introduced or exposed by the task
- Duplication within the task's scope that has a clear shared reason to change
- Speculative abstractions or configuration with no present need
- Misplaced constants or utilities when the project has an established location for them
- Type-safety erosion such as unjustified `any`, broad casts, ignored errors, or non-null assertions
- Missing error handling or validation that the task's behavior requires
- Documentation, tests, or TODO entries that the task should have updated
- Drift from project conventions or the governing design and decisions

Skip style issues already enforced by formatters or linters. Do not propose broad refactors, unrelated modernization, or speculative improvements. Prefer a small cleanup that makes this task's diff clearer and safer.

## Report

Report findings before making any changes, ordered by leverage and severity. For each finding include:

- File and line or symbol
- Category
- What should change
- Why it matters
- Effort: quick win, moderate, or larger refactor

If no cleanup is warranted, say so and mention any residual risks or testing gaps.

## Fix mode

If `$ARGUMENTS` contains `--fix`, apply only unambiguous, low-risk fixes within the task scope, such as confirmed dead code, unused imports, debug logging, or confirmed-unused dependencies. Do not silently restructure duplicated logic, rewrite conventions, or broaden scope. Re-run relevant verification after fixes and report what changed.

Without `--fix`, do not edit files.
