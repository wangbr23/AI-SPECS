---
name: orchestrate
description: Run the full idea-to-shipped pipeline for a piece of work — grilling, design-review, plan-tasks, dispatch, cleanup/review, save-progress — in order, pausing between phases for the human to confirm before advancing. Use when the user wants to run the whole workflow end to end, kick off a new feature or project through the full pipeline, or asks to "run the pipeline" / orchestrate a piece of work.
---

# Orchestrate

A thin sequencing layer over the existing pipeline skills. It never reimplements what a phase skill already does — it just calls them in order via the `Skill` tool and stops between phases for a human go-ahead. If you only want one phase, invoke that skill directly instead of this one.

## When to run

When the user wants the full idea → shipped-code pipeline run for a new piece of work, whether that's a brand-new project or a new feature on an existing one — same flow either way (`project-init` is the one-time exception, see step 0). Not for running a single phase in isolation.

## Requires

- `project-init` to have already been run in this repo at some point (`AGENTS.md`, `docs/`, `TODO.md` present). If not, say so and offer to run it first — don't invent the layout.
- The `plan-tasks`, `dispatch`, `design-review`, `save-progress`, `code-cleanup` skills, and the `simplify`/`code-review` built-ins, present as usual.

## Steps

### 0. Detect where to resume

Don't assume every run starts from zero. Look at what already exists on disk before picking a starting phase:

- No `docs/specs/*.md` for this piece of work yet → start at step 1 (grilling).
- A spec exists but no corresponding `docs/designs/*.md` → start at step 2 (design).
- A design exists but `TODO.md` has no tasks referencing it → start at step 3 (tasks).
- `TODO.md` has an agent-ready or manual-ready frontier → start at step 4 (dispatch).
- Everything above is done/empty → start at step 5 (cleanup gate).

If it's genuinely ambiguous which phase to resume at, ask the user rather than guessing. This is also what makes running `/orchestrate` again on an already-existing project correct for a *new* feature: `plan-tasks` (and everything after it) is meant to be re-run repeatedly over a project's life, not just once at conception — a rerun grounds `design-review` in the current codebase and appends new `T<n>` tasks onto the existing `TODO.md`, it doesn't restart `project-init` or overwrite anything.

### 1. Capture

Invoke `grill-me` via the Skill tool (it interviews via `grilling`, then saves the result to `docs/specs/<slug>.md`). `grill-me` has `disable-model-invocation: true`, which blocks Claude from *autonomously* triggering it by matching its description against ambient conversation — it does not block an explicit tool call, and running it here is exactly that: a deliberate step the user asked `orchestrate` to take, not a guess. Let its interview run normally (rounds of questions to the user); resume once it reports `docs/specs/<slug>.md` written.

If a spec already exists for this piece of work (per the resume detection in step 0), skip straight to step 2 using it instead of re-running `grill-me`.

### 2. Design

Invoke `design-review`, pointing it at `docs/specs/<slug>.md` as the spec to ground the design in (in addition to its own required grounding: `AGENTS.md`, `docs/decisions.md`, current code). It produces `docs/designs/<date>-<slug>.md` as it always does, Codex-reviewed.

Stop and confirm before moving on.

### 3. Tasks

Invoke `plan-tasks` against the design doc from step 2, so the tasks it appends to `TODO.md` carry the `design:` field pointing back to it.

Stop and confirm before moving on.

### 4. Build loop

Invoke `dispatch`. It runs one wave (the current agent-ready frontier) and stops — it never auto-merges. After it reports:

1. Wait for the human to review and merge the wave's branches.
2. Ask whether to run the next wave.
3. Repeat until `dispatch` reports both the agent-ready and manual-ready sets are empty.

Manual-ready tasks surfaced along the way are the user's to handle; don't let them stall the loop.

### 5. Cleanup gate

Once the build loop is done, invoke `code-cleanup` (whole-repo pass — this is what catches cross-task drift or duplication that no single task's own `simplify`/`code-review` pass, run inside `dispatch`, could ever see) and then `code-review` on the full set of changes as a final correctness pass. Report findings; let the user decide what to apply. This is a second, different-scope pass, not a redundant repeat of what each `dispatch` worker already did to its own diff.

Stop and confirm before moving on.

### 6. Checkpoint

Invoke `save-progress` to close out `docs/journal.md`, `docs/decisions.md`, and reconcile `TODO.md`. This ends the run.

## Notes

- Every phase transition pauses for explicit human confirmation by default — this generalizes the "human gate every wave" preference from `dispatch` to the whole pipeline, and is what keeps disagreements surfaced instead of silently steamrolled.
- `grill-me`/`grilling` and `design-review` are inherently interactive (they need the human's live answers/judgment calls) — they can't be backgrounded the way `dispatch`'s task workers are. Only step 4 involves parallel subagents; everything else in this skill runs in the main conversation.
- If the user only wants a subset of the pipeline (e.g. "just plan the tasks" or "just build the next wave"), invoke that phase's skill directly rather than going through `orchestrate` — this skill exists purely to save re-typing the sequence, not to gate access to the phases.
