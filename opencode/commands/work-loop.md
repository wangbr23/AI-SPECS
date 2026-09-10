---
description: Work through TODO.md tasks one at a time — recompute the dependency frontier, implement, test, journal, commit, repeat; stop after a batch so the user can /compact.
---

Run the sequential TODO work loop (one task per round, no parallel dispatch or worktrees):

1. **Orient.** Read `TODO.md`, `AGENTS.md`, `CLEANCODE.md`, and the latest few entries in `docs/journal.md`. Before implementing a task, read any design doc it references (e.g. files under `docs/designs/`).
2. **Recompute the frontier EVERY round — never reuse the previous round's frontier.** A task is unblocked when every id in its `depends-on` is checked `[x]` in `TODO.md` (no `depends-on` means always unblocked). Pick the **lowest-numbered** unblocked task. Completing a task can unblock a lower-numbered one, so always re-derive before selecting.
3. **Implement** that single task, following project conventions and the referenced design docs.
4. **Verify.** Run the project's test, typecheck, and lint commands (see the Commands section of `AGENTS.md`) and make them pass. Unit tests are not enough when the task has an end-to-end surface: if it renders in a browser, do a real browser check with the Playwright/browser tools; if it runs a backend workflow (a server route, pipeline, CLI invocation, plugin hook, etc.), actually run that workflow end to end — start the real thing and exercise it, don't just call the units. Iterate until everything is green; do not mark a task done with failing checks.
5. **Close out.** Flip the task's checkbox to `[x]` in `TODO.md`, append a dated entry to `docs/journal.md` (what was done, decisions/deviations from the design, test status), then `git add` only the files belonging to this task and commit in the project's commit-message style. Never commit secrets or unrelated changes.
6. **Repeat** from step 2 until every task in `TODO.md` is `[x]` or no tasks remain unblocked.

Arguments: `$ARGUMENTS` may restrict the run to specific task ids (e.g. `/work-loop T15 T16`) plus whatever they depend on.

Stopping rules:
- Run until completion or blocker — do not stop mid-batch. If you approach a context limit, finish the current task cleanly (green checks, `[x]`, journal, commit) and report so the user can `/compact` and re-invoke.
- You cannot run `/compact` yourself. When done, report: tasks completed with commit hashes, test status, and any remaining work.
- Stop early and report if a task turns out blocked, tests cannot be made green after honest attempts, or a decision needs the user. Surface conflicts; never silently reconcile them.
- Keep commentary minimal — the loop is the work.