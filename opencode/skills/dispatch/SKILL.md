---
name: dispatch
description: Read TODO.md, compute the agent-ready task frontier (per plan-tasks), and run those tasks in parallel — one fresh subagent per task, in its own git worktree, each self-cleaning via simplify and code-review before reporting — checking off TODO.md as tasks finish. Use when the user wants to build/implement the next wave of tasks, run tasks in parallel, or asks to dispatch agents against TODO.md.
---

# Dispatch

`plan-tasks` computes which tasks are safe to hand to parallel agents; this skill is what actually hands them out and runs them. One wave at a time, one fresh subagent per ready task, never auto-merged.

## When to run

When `TODO.md` has unblocked `agent` tasks ready to build, or the user asks to build/implement the next wave, run tasks in parallel, or dispatch agents. Not for a single task done inline in the current conversation — that's just doing the work directly.

## Requires

- The target project should already have `TODO.md` (from `project-init`) with tasks in `plan-tasks`' format. If it doesn't, say so and suggest running `plan-tasks` first rather than inventing task structure.
- The `codex` CLI installed and authenticated (`which codex`) for any task carrying a `complexity` tag — that's what routes implementation to it. Tasks without a `complexity` tag fall back to a Claude subagent implementing directly (see step 3), so an older `TODO.md` written before this field existed still works unmodified.

## Steps

### 1. Compute the frontier

Read `TODO.md` and apply `plan-tasks`' own rule verbatim — don't reimplement it differently:

- **Agent-ready set**: unchecked tasks tagged `agent` whose every `depends-on` id is already checked off.
- **Manual-ready set**: unchecked `manual` tasks whose dependencies are satisfied. Report these to the user separately; never let them block agent dispatch of unrelated tasks.
- Everything else is blocked. Don't dispatch it, don't wait on it.

If the agent-ready set is empty, say why (nothing ready yet / everything done / everything blocked on manual or unfinished work) and stop — this is a normal no-op, not an error.

### 2. Identify context per task — paths, not content

For every task in the agent-ready set, resolve which files ground it:

- The task's own `TODO.md` line (id, description, dependencies).
- `AGENTS.md` (repo conventions).
- `docs/decisions.md` (durable constraints already locked in).
- The governing design doc:
  - If the task has a `design:` field, use that path.
  - If it doesn't, and exactly one `docs/designs/*.md` exists, use that one.
  - If it doesn't, and more than one `docs/designs/*.md` exists, ask the user once which doc governs this batch before dispatching anything. Don't guess (e.g. by picking the most recently modified) — a wrong grounding doc is worse than asking.
  - If the design doc is long, also note which heading(s) actually bear on this task (e.g. "### Ingestion approach") so whoever reads it later doesn't have to read the whole thing.

**Don't read these files' contents into your own context here, and don't paste their contents into a subagent's prompt.** Every worktree already contains these files — hand over paths (plus, for a long design doc, the relevant heading), and let whoever actually needs the content (the reviewing subagent, or Codex inside the worktree) read it directly with its own tool calls, in its own context budget. Assembling and re-pasting full file contents through the dispatcher wastes tokens twice over: once holding it here, again when a subagent re-serializes it into a Codex brief. This is the single biggest token cost in a wave if skipped — don't skip it.

### 3. Launch the wave

For every task in the agent-ready set, launch one **fresh** subagent (the default/general-purpose agent type — explicitly not a fork, since a fork would inherit this entire conversation, including every prior phase of the pipeline, into a task that only needs its own slice of context) with worktree isolation, all in a single message so they run concurrently.

Give each subagent a **short** prompt: the task line, the worktree path, the file *paths* from step 2 (not their contents), and an instruction sequence that depends on whether the task carries a `complexity` tag. The subagent's own prompt should be small regardless of how big the task is — size lives in what Codex or the subagent reads for itself inside the worktree, not in what the dispatcher hands over. If a task genuinely needs a judgment call spelled out (a design doc leaves two options open, a scope boundary against a sibling task needs stating), write that as a few sentences pointing at *what to resolve*, not a restatement of the source material — one short paragraph, not a re-quoted section.

**Task has `complexity: simple` or `complexity: complex`** — Codex implements, this subagent reviews:

1. Write a **short** implementation brief to a scratch file: the task line, done-when criteria, and the file paths from step 2 with an instruction to read them itself before writing code (e.g. "read AGENTS.md, CLEANCODE.md, docs/decisions.md, and the 'Ingestion approach' section of docs/designs/<file>.md before implementing"). Do not paste those files' contents into the brief — Codex has read access to the whole worktree in `workspace-write` mode and can read them itself, in its own context, for free relative to this subagent's budget.
2. Run Codex non-interactively in the worktree, piping the brief in on stdin, with model/effort chosen by the task's `complexity`:

   | complexity | model | effort |
   |---|---|---|
   | `simple` | `gpt-5.4-mini` | `low` |
   | `complex` | `gpt-5.6-luna` | `medium` |

   ```
   codex exec -s workspace-write -C <worktree-dir> -m <model> -c model_reasoning_effort=<effort> - < <brief-file>
   ```

   `-s workspace-write` lets Codex write inside the worktree without interactive approval prompts, and without full-disk access. This model mapping is a deliberate choice already discussed with the user, not this skill's own judgment call — don't second-guess or "correct" it against outside model documentation without asking first.
3. Run the `simplify` skill on the resulting diff (reuse/simplification cleanup, applies automatically) — it grounds itself in repo conventions by reading `AGENTS.md`/`CLEANCODE.md` as part of its own process; don't pre-supply them.
4. Run `code-review --fix` on the resulting diff (correctness bugs, applies fixes) — same: it reads what it needs itself.
5. Report back: which model/effort ran, what Codex built, what `simplify` and `code-review` changed or flagged (including anything left unfixed), and the worktree/branch it's on.

**Task has no `complexity` tag** (pre-existing `TODO.md` entries) — this subagent implements directly, unchanged from before:

1. Implement the task, reading `AGENTS.md`, `CLEANCODE.md`, `docs/decisions.md`, and the relevant design-doc section directly from the worktree as needed — don't expect them pre-pasted into your prompt.
2. Run the `simplify` skill on your own diff.
3. Run `code-review --fix` on your own diff.
4. Report back: what you built, what `simplify` and `code-review` changed or flagged, and the worktree/branch it's on.

Doing the review steps inside the worktree, before anyone reviews it, is what keeps tech debt from piling up wave over wave instead of accumulating for one big cleanup pass later — this holds regardless of who implemented the task.

Dispatch itself never sees a worker's intermediate tool calls, only its final report — the same as any backgrounded agent call. If a worker's own task needs sub-exploration, it can dispatch its own subagents for that; nothing extra is needed here for it to do so.

If `codex exec` fails (not installed, not authenticated, sandbox rejects the change, etc.), the subagent should say so plainly in its report and stop rather than silently falling back to implementing the task itself — a silent fallback would hide that the intended routing didn't happen.

### 4. Reconcile as workers finish

As each subagent's report comes back, check off `[x]` its task on the real `TODO.md` immediately — this is the authoritative, real-time update. (`save-progress` also touches `TODO.md`, but only as an end-of-session reconciliation sweep — dropping stale items, adding newly-surfaced work — not a competing writer of these same checkboxes.)

Dispatch only ever writes `TODO.md` checkboxes. It does not touch `docs/journal.md` or `docs/decisions.md` — that stays `save-progress`'s job.

### 5. Report the wave, then stop

Once every subagent in the wave has finished (or the user says stop), report a summary: one line per task — worktree/branch, what got built, what `simplify`/`code-review` changed or flagged. **Do not merge anything.** The human reviews and merges each branch by hand. Running `/dispatch` again after merging computes the next wave's frontier and starts over.

## Notes

- Keep prompts (to subagents, and inside their briefs to Codex) to paths and pointers, not pasted file contents — see step 2 and step 3. An earlier version of this skill had the dispatcher assemble and paste full `AGENTS.md`/`CLEANCODE.md`/`docs/decisions.md`/design-doc content into every subagent's prompt; across a 5-task wave that meant near-identical multi-thousand-token blocks repeated five times, then re-serialized a second time into each Codex brief. Every worktree already has these files on disk — the reader (subagent or Codex) should read them directly, in its own budget, not have them pre-chewed and pasted by the dispatcher.
- Implementation now routes by task: `complexity`-tagged tasks go to Codex (model/effort per the table in step 3), untagged tasks still go to a Claude subagent directly. Either way, the dispatched Claude subagent always does the review (`simplify` + `code-review --fix`) before reporting — that part isn't runner-dependent.
- The Codex model/effort mapping in step 3 was chosen with the user directly, and deliberately doesn't match this environment's own bundled model-tier docs (`gpt-5.6-luna` is documented there as the high-throughput/low-latency tier, not the reasoning-heavy one — `gpt-5.6-sol` or `gpt-5.6-terra` would match "higher reasoning" more literally). The user was shown that discrepancy and chose `luna` anyway. Don't silently "fix" this mapping later without raising it again first.
- Reserve this for genuinely parallel-safe waves. If the agent-ready set is a single task, it's often simpler to just do it inline rather than pay the overhead of a worktree and a subagent report round-trip — use judgment.
