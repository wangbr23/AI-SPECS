---
name: code-cleanup
description: Whole-codebase cleanup audit for dead code, duplication, convention drift, speculative complexity, leftover scaffolding, type-safety erosion, docs drift, and oversized/unreviewable code. Use after several landed tasks, before milestones, or when the user asks for a codebase health check.
---

# Code Cleanup

Whole-codebase cruft audit. This complements `code-review`, which is branch/diff scoped. `code-cleanup` looks across the repository for issues that emerge over multiple tasks, agents, or sessions.

## When to run

Run:

- after several dispatched tasks have landed;
- before a milestone/release;
- when the user asks to audit, clean up, find cruft, or check codebase health;
- when `project-status` suggests docs/code/TODO drift.

Do not use this for reviewing a single branch/diff; use `code-review` for that.

## Scope

Default to the whole repository, respecting `.gitignore`. If the user names a directory/module, scope to that instead.

For large repos, split the audit by top-level directory/module. Pi does not have built-in subagents, so use either:

- the current agent for small/medium scopes; or
- separate read-only Pi subprocesses for large scopes, then synthesize findings centrally.

Example read-only audit subprocess:

```bash
pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "Audit <scope> for cleanup findings using AGENTS.md and CLEANCODE.md. Do not edit files."
```

## What to look for

- **Dead code** — unused exports, orphaned files/components, unreachable branches, commented-out blocks.
- **Duplication** — near-identical logic in multiple places that should become one shared helper/module.
- **Convention drift** — code that conflicts with `AGENTS.md`, `CLEANCODE.md`, or established project patterns.
- **Speculative complexity** — abstractions, generic utilities, config options, or indirection with only one real use or no present need.
- **Misplaced constants/utilities** — reusable domain logic or constants living in the wrong layer, judged against existing project structure.
- **Leftover scaffolding** — TODO/FIXME comments, placeholder copy, debug logging, unused dependencies, temporary files.
- **Type-safety erosion** — `any`, broad casts, non-null assertions, ignored type errors, loose domain modeling without reason.
- **Docs drift** — code that no longer matches `docs/specs`, `docs/designs`, `docs/decisions.md`, `AGENTS.md`, or `TODO.md`.
- **Reviewability problems** — oversized files, god modules, tangled changes, or patterns that make future task diffs hard for a human to review.
- **Testing gaps** — important behavior with no clear verification path, especially where `Done when:` criteria imply tests/checks should exist.

Skip style nitpicks that formatters/linters already enforce.

## Steps

### 1. Ground the audit

Read:

- `AGENTS.md`
- `CLEANCODE.md` if present
- `TODO.md`
- `docs/decisions.md` if present
- relevant/recent `docs/specs/*.md`
- relevant/recent `docs/designs/*.md`
- recent `docs/journal.md` entries

Note the project's existing layout and conventions before judging code. This is not a generic best-practices audit.

### 2. Enumerate scope

List files/directories in scope. Ignore generated/build/vendor outputs. Respect project conventions and `.gitignore`.

If the scope is large, split by directory/module and run read-only subprocess reviewers. Each reviewer should return findings with files, category, summary, why it matters, and confidence.

### 3. Analyze findings

De-duplicate and synthesize centrally. Do not just concatenate subprocess reports.

Pay special attention to cross-module findings:

- duplication across directories;
- inconsistent conventions between features;
- docs/design decisions implemented differently in different places;
- recurring task-size/reviewability problems.

### 4. Prioritize by leverage

Rank by impact and effort, not just severity.

Use effort tags:

- **quick win** — safe localized cleanup, minutes to an hour.
- **moderate** — contained refactor or focused cleanup.
- **larger refactor** — broad work requiring planning/review.

Use severity tags:

- **high** — likely correctness, security, maintainability, or future velocity issue.
- **medium** — meaningful cleanup with clear benefit.
- **low** — polish or opportunistic improvement.

### 5. Report

Use this format:

```md
## Code cleanup audit

Scope: <repo/path>

### Findings

1. [high][quick win] <category>: <summary>
   - Files: ...
   - Why it matters: ...
   - Suggested action: ...

2. [medium][moderate] <category>: <summary>
   - Files: ...
   - Why it matters: ...
   - Suggested action: ...

### Recurring patterns
- ...

### Suggested next tasks
- [ ] `T<n>` ... — agent/manual, depends-on: ..., design: ...
  - Done when: ...
```

Do not edit code by default.

### 6. Optional fix mode

If invoked with `--fix`, apply only unambiguous, localized fixes:

- confirmed dead code introduced or clearly unused;
- debug logs or commented-out experiments;
- unused imports;
- unused dependencies when verified;
- tiny documentation pointer corrections.

Do not silently restructure code, merge duplicated modules, rewrite conventions, or perform broad refactors. Those should become reviewable tasks in `TODO.md` and go through `plan-tasks` / `dispatch` / `code-review`.

After any fixes, run relevant checks and report changed files.

## Notes

- This is primarily an audit skill, not an automatic refactor tool.
- If the same finding type recurs, recommend updating `CLEANCODE.md`, `AGENTS.md`, or `docs/decisions.md` so future agents avoid repeating it.
- Prefer generating small reviewable cleanup tasks over one giant cleanup branch.
