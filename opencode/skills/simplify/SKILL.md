---
name: simplify
description: Simplify recently modified code for clarity, consistency, and maintainability while preserving exact behavior. Use after implementing or editing code, or when the user invokes /simplify.
---

# Simplify

Refine recently modified code immediately. Apply improvements rather than only reporting them, while preserving all existing functionality, outputs, and behavior.

## Scope

- Default to code modified in the current diff or session.
- If the user names a different scope, use that scope instead.
- Do not turn a focused simplification pass into a whole-codebase cleanup; use `code-cleanup` for that.
- Preserve unrelated changes and never revert work you did not make.

## Process

1. Read the repository's `AGENTS.md`, `CLEANCODE.md`, and any directly relevant local instruction files.
2. Inspect the scoped diff and enough surrounding code to understand behavior and established patterns.
3. Simplify only where the result is clearly more readable, direct, or consistent.
4. Apply the changes in place.
5. Run the relevant format, typecheck, test, and build commands documented by the repository.
6. Report significant refinements and verification results. If no worthwhile simplification exists, say so and leave the code unchanged.

## What To Improve

- Reduce unnecessary complexity, nesting, indirection, and redundant code.
- Remove speculative abstractions and wrappers without a present need.
- Improve unclear names and group closely related logic.
- Remove comments that merely restate obvious code while preserving comments that explain constraints or reasoning.
- Prefer explicit control flow over nested ternaries or dense one-liners.
- Reuse existing project utilities when that is clearer than duplicating logic.
- Keep code close to its use unless reuse or a shared reason to change already exists.

## Guardrails

- Never change externally observable behavior or remove supported functionality.
- Do not optimize for fewer lines at the expense of clarity.
- Do not combine unrelated responsibilities into one function or module.
- Do not remove useful abstractions that genuinely improve organization or have multiple real call sites.
- Do not introduce new dependencies or broaden public APIs merely to simplify local code.
- Do not make opportunistic fixes outside the scoped changes unless they are required to preserve correctness.
