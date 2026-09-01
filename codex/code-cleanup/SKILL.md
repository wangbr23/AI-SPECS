---
name: code-cleanup
description: Scan a codebase (not just a diff) for cleanup opportunities — dead code, duplication, convention drift, speculative complexity, leftover scaffolding, type-safety erosion, docs drift — and report a prioritized list. Fans out via subagents for large codebases. Use when the user asks to audit, clean up, or find cruft in a codebase, or wants a codebase health check.
---

# Code Cleanup

Complements an ordinary diff-scoped code review. This skill is whole-codebase and cruft-focused: for code produced quickly across many sessions — often by more than one AI tool — it finds where attention is most worth spending, since nobody has bandwidth to review all of it line by line.

## When to run

When the user asks to audit, clean up, find cruft in, or check the health of a codebase. Not for reviewing a specific change or automatically simplifying code that was just written.

## Scope

Default to the whole repository (respecting `.gitignore`). If the user names a directory or module, scope to that instead. For a codebase too large to read in one pass, fan out: launch one subagent per top-level directory or module, each returning its own findings, then merge and re-prioritize centrally rather than just concatenating — duplication and convention-drift findings in particular only make sense compared across the whole set, not judged per-subagent in isolation.

## What to look for

- **Dead code** — unused exports, orphaned files/components nothing imports, unreachable branches, commented-out blocks.
- **Duplication** — near-identical logic living in two or more places that should be one shared helper.
- **Convention drift** — code that doesn't match what `AGENTS.md` says (naming, error handling, import style, file layout). Weight this higher if the project is touched by more than one AI tool or session — check `docs/journal.md` for signs of that.
- **Speculative complexity** — abstractions, config options, or generic utilities with exactly one caller; anything that reads as building for a future need rather than a real one. Check directly against any KISS/simplicity principle already stated in `AGENTS.md`, if there is one.
- **Misplaced constants/utilities** — magic numbers or string literals that belong in a shared constants file instead of inline in a component; component-local functions that don't touch that component's state/props and are either already reused elsewhere or clearly reusable enough to belong in a `lib`/`utils` module instead. Judge against whatever placement convention the project already has (check `AGENTS.md` and existing `lib/`/`utils/`/constants files first) — flag genuine misplacement, not every literal or helper a component happens to use once. A one-off value or a function that's genuinely tied to one component's rendering isn't a violation.
- **Leftover scaffolding** — stray TODO/FIXME comments, placeholder copy, debug logging, unused dependencies in the package manifest.
- **Type-safety erosion** — `any`, non-null assertions, `@ts-ignore`/`@ts-expect-error` (or language equivalents) used without a stated reason.
- **Docs drift** — code that's quietly stopped matching `docs/decisions.md` or a design doc's stated architecture. Cross-reference with the `project-status` skill's output if it's been run recently in this session.

Skip style nitpicks a linter or formatter already enforces — this is for things tooling doesn't catch.

## Steps

1. Read `AGENTS.md` (stack, conventions, any stated design principles), and note the project's existing `lib`/`utils`/constants layout if it has one. This is the yardstick everything else gets checked against, not a generic best-practices checklist.
2. Enumerate the scope (whole repo or named directory). For a large scope, split into subagent-sized chunks by directory or module and launch them in parallel, each given the AGENTS.md conventions and the category list above in its prompt.
3. Collect findings, then de-duplicate and re-prioritize as one list — a duplication finding that spans two subagents' territory needs merging, not two separate entries.
4. Rank by leverage, not just severity: a five-minute dead-code deletion and a two-day refactor both matter, but the report should make clear which is which so the user can choose where to spend limited review time. Tag each finding with a rough effort level (quick win / moderate / larger refactor).
5. Report the findings most-impactful first. Each finding should include file(s), category, a one-sentence summary, why it matters, and an effort tag.
6. If `--fix` is passed: apply only the unambiguous, no-judgment-call findings (confirmed-dead code, confirmed-unused dependencies) directly. Leave duplication merges, convention rewrites, and anything else requiring a judgment call for the user to approve explicitly — never silently restructure code as part of a cleanup pass.

## Notes

- This is an audit, not a refactor tool. Default behavior never changes code.
- If the same category of finding keeps recurring across runs, that's a signal for a `docs/decisions.md` entry or an `AGENTS.md` convention update, not just another cleanup pass — mention it in the report when that happens.
