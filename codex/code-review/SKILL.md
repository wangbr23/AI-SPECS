---
name: code-review
description: Review a local diff or pull request for high-confidence correctness regressions and repository-instruction violations, optionally fixing confirmed issues when requested. Use for explicit code review requests or when another workflow requires a correctness review before handoff.
---

# Code Review

Review the requested change, focusing on defects introduced by that change rather than general codebase quality.

## Scope

- Read the applicable repository instruction files and the complete diff.
- Inspect nearby code, tests, types, and history only when needed to verify behavior.
- Prioritize correctness, authorization, data integrity, concurrency, resource lifecycle, accessibility, and user-visible regressions.
- Exclude style nits, speculative concerns, pre-existing problems, and issues already caught conclusively by routine lint or typechecking.
- Report only findings that remain convincing after checking the surrounding implementation.

## Fix mode

When invoked with `--fix` or explicitly asked to fix findings:

1. Apply fixes for confirmed in-scope issues directly.
2. Keep fixes minimal and preserve the original task's intent.
3. Run relevant validation after fixing.
4. Report what was fixed, what remains, and validation results.

Without fix mode, do not edit files. Lead with findings ordered by severity and include file and line references. If there are no findings, state that plainly and mention any validation gaps or residual risks.
