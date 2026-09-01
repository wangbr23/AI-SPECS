---
name: simplify
description: Simplify a code change after implementation by removing unnecessary complexity, duplication, and scaffolding while preserving behavior. Use when the user asks to simplify a diff or when another workflow explicitly requires a simplification pass before review.
---

# Simplify

Review the current task's diff, not the whole repository, and apply worthwhile simplifications directly.

## Workflow

1. Read the repository instructions and understand the requested behavior.
2. Inspect the complete task diff and the nearby existing abstractions it touches.
3. Look for complexity introduced by the change: redundant branches, duplicated logic, unnecessary wrappers or state, speculative extensibility, stale comments, and new helpers that duplicate an established utility.
4. Make only changes that preserve the requested behavior and improve clarity or reuse. Prefer straightforward code over compressed cleverness. Do not broaden scope or perform unrelated cleanup.
5. Run the repository's relevant formatter, typecheck, lint, tests, or build in proportion to the change.
6. Report what was simplified and any complexity intentionally retained because removing it would change behavior or obscure a real constraint.

If the diff is already simple, leave it unchanged and say so.
