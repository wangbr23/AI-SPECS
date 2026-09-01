---
name: design-review
description: Draft an implementation design from a product spec using the current Pi agent, run two independent read-only DeepSeek R1 reviewer agents, synthesize their feedback, weigh it rather than merging blindly, and revise. Use after grill-me, when turning docs/specs requirements into docs/designs implementation plans.
---

# Design Review

Turns a hardened product spec into an implementation design. The current Pi agent is the designer. Two separate DeepSeek R1 Pi subprocesses review the design independently in read-only mode. The designer then combines, de-duplicates, and weighs their feedback before revising.

## When to run

Run after `grill-me` has produced `docs/specs/<slug>.md`, or whenever the user asks to turn product requirements into an implementation design. Not for code review or whole-codebase cleanup.

## Model roles

- **Designer:** the current Pi session/model. It drafts and revises the design.
- **Reviewers:** two independent DeepSeek R1 Pi agents, launched as separate read-only subprocesses.
- Default reviewer model pattern: `deepseek/deepseek-r1`.
- If that model is unavailable in this Pi setup, ask the user for the exact model pattern to use. Do not silently substitute a different reviewer model unless the user approves.

Reviewer subprocesses must be read-only:

```bash
pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "<review prompt>"
```

If the user's Pi install requires an explicit provider, use the user's configured pattern, e.g. `--model vercel-ai-gateway/deepseek/deepseek-r1` or another working DeepSeek R1 pattern.

## Requires

- `AGENTS.md`
- `CLEANCODE.md` if present
- `docs/decisions.md`
- `docs/specs/<slug>.md` from `grill-me`
- `docs/designs/` directory, usually created by `project-init`

If the project context scaffold is missing, say so and suggest running `project-init` first rather than inventing a layout.

## Steps

### 0. Select the spec

If the user provided a spec path, use it. Otherwise:

- If exactly one `docs/specs/*.md` exists, use it.
- If multiple specs exist, ask which one to design against.
- If none exist, say `grill-me` should run first unless the user wants to provide requirements inline.

### 1. Ground the draft before writing

Read, in full where practical:

- `AGENTS.md` — project stack, commands, architecture, workflow.
- `CLEANCODE.md` — coding conventions and quality bar.
- `docs/decisions.md` — durable constraints and prior architecture decisions.
- The selected `docs/specs/<slug>.md` — product requirements, non-goals, open questions.
- Relevant current code — cite real files in the design; do not design from memory.

A design built on stale grounding is worse than no design. This step is mandatory.

### 2. Draft the design

Write the design doc to:

```text
docs/designs/<date>-<slug>.md
```

Use `YYYY-MM-DD` for `<date>`. Reuse the spec slug unless the user asks for a different name.

Design doc structure:

- **Problem** — what is being solved and why, based on the spec.
- **Requirements grounding** — key product requirements and non-goals from the spec.
- **Current-state grounding** — what exists now, cited to real files.
- **Goals / Non-goals** — implementation scope boundaries.
- **Design** — recommended implementation approach and reasoning. State the pick and why; do not survey every possible alternative.
- **Data / interfaces** — schemas, APIs, files, events, or component boundaries that matter.
- **Risks** — named, specific uncertainties.
- **Rollout** — build order, if sequencing itself is a real decision.
- **Verification** — how to know the implementation worked.

Leave out line-level implementation code unless a tiny snippet clarifies an interface. This is a build plan, not the build.

### 3. Run two independent DeepSeek R1 reviews

Launch two separate read-only reviewer subprocesses. They should not see each other's feedback.

Use this review prompt for reviewer A:

```text
Review the design doc at <design-path> against the product spec at <spec-path> and the project context files AGENTS.md, CLEANCODE.md if present, and docs/decisions.md.

Check specifically:
1. Does the design satisfy the product requirements and respect non-goals?
2. Does it respect existing technical decisions and project conventions?
3. Is there a simpler implementation approach?
4. Is anything over-built, under-specified, or risky?
5. Are there security, privacy, data-exposure, migration, or operational concerns?
6. Is the verification plan sufficient?

Report findings only. Do not edit files. For each finding include: title, severity, why it matters, suggested change, and confidence.
```

Use a second prompt for reviewer B with the same checklist plus this instruction:

```text
You are the second independent reviewer. Do not assume another reviewer will catch anything. Be especially skeptical about hidden complexity, edge cases, and whether the design can be split into safe tasks.
```

Run both with read-only tools:

```bash
pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "<reviewer A prompt>"
pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "<reviewer B prompt>"
```

If the first command fails because the model pattern is unavailable, stop and ask the user for the correct DeepSeek R1 model pattern before running both reviews.

### 4. Combine and weigh feedback

Do not paste both reviews blindly into the design. Synthesize them:

1. Group duplicate or overlapping findings.
2. Note disagreements between reviewers.
3. For each combined finding, decide:
   - **Accept** — revise the design.
   - **Reject** — explain briefly why it does not hold up.
   - **Escalate** — ask the user if it is a real product/architecture judgment call.

The current designer agent owns the final judgment. The reviewers are advisors, not authors.

### 5. Revise and close the loop

Revise the design doc for accepted feedback.

Then:

- Append any significant implementation/architecture decisions to `docs/decisions.md` in its existing format.
- Update `TODO.md` only if near-term work changed directly. Detailed task breakdown belongs to `plan-tasks`, which normally runs next.
- Report:
  - design doc path
  - reviewer model used
  - accepted/rejected/escalated findings
  - decisions or TODO updates made

## Notes

- One two-reviewer round by default. Do not keep looping unless the user asks.
- If DeepSeek R1 is unavailable, offer to proceed with only the draft or ask for a different reviewer model.
- Keep product requirements in `docs/specs/`; keep implementation design in `docs/designs/`.
