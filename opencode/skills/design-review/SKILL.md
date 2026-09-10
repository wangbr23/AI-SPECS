---
name: design-review
description: Draft a design doc for a feature, get an independent review from Codex (read-only), weigh its feedback rather than merging it blindly, and revise. Use when the user wants a three-point design review, a second opinion on a design from Codex, or asks to draft-review-revise a design doc.
---

# Design Review

A three-point design process: Claude drafts, Codex reviews (read-only, via `codex exec -s read-only`), Claude weighs the feedback and revises — surfacing genuine disagreements to the user rather than silently resolving them. The value of a second reviewer is a different model's blind spots; that only pays off if the feedback is actually weighed, not merged wholesale.

## When to run

When the user asks for a design doc with an independent review, wants "a second opinion" or "have Codex review this" on a design, or explicitly invokes a three-point / draft-review-revise design process. Not for reviewing code changes (use `/code-review`) and not for whole-codebase health audits (use `code-cleanup`).

## Requires

- The `codex` CLI installed and authenticated (`which codex` to confirm before starting; this skill shells out to it via Bash).
- The target project should already have `docs/designs/` and `docs/decisions.md` from `project-init` — if they don't exist, say so and suggest running `project-init` first rather than inventing the layout.

## Steps

### 0. Ground the draft before writing it

Read `AGENTS.md` (stack, conventions, any stated design principles), `docs/decisions.md` in full (existing constraints a new design must respect), and the actual current code relevant to the feature — not assumptions from memory or from an earlier session. A design built on stale grounding is worse than no design; this step is mandatory, not optional.

### 1. Draft

Write the design doc to `docs/designs/<date>-<slug>.md` (or revise an existing one if this is a follow-up pass), using this structure:

- **Problem** — what's being solved and why, one paragraph.
- **Grounding** — what actually exists right now, cited to real files.
- **Goals / Non-goals** — explicit scope boundaries.
- **Design** — the recommended approach with reasoning. State the pick and why; don't survey every alternative considered.
- **Risks** — named, specific uncertainties, not generic caveats.
- **Rollout** — build order, if sequencing itself is a real decision.
- **Verification** — how you'll know it worked.

Leave out: line-level implementation code (that's the build phase, not the design) and anything that belongs in `docs/journal.md` / `docs/decisions.md` rather than being duplicated here.

### 2. Review — Codex, read-only, checklist-driven

Shell out via Bash:

```
codex exec -s read-only "Review the design doc at <path>. Check specifically: (1) does it respect the existing constraints in docs/decisions.md? (2) is there a simpler alternative to the recommended approach? (3) any security or data-exposure concern? (4) is the stated scope (Goals/Non-goals) actually justified, or over-built? Report findings as: finding, why it matters, and how confident you are. Do not edit any files."
```

`-s read-only` is a real sandbox constraint, not just an instruction — Codex cannot write files in this mode, so it can critique but not quietly rewrite the doc itself. Adjust the checklist to the specific design if the four defaults don't fit (e.g. a UI-heavy design might ask about visual consistency instead of data exposure).

### 3. Weigh, don't merge

Read Codex's findings and, for each one, decide: accept and revise, or explain why it doesn't hold up. This is the step that makes the review worth having — do not apply findings mechanically just because a second model produced them.

- Where you agree: revise the doc.
- Where you disagree and it's clear-cut: note briefly why the suggestion wasn't taken.
- Where it's a genuine judgment call and reasonable reviewers could land differently: **surface it to the user explicitly** rather than silently picking a side. This is the one case where the skill should stop and ask, not resolve on its own.

### 4. Close the loop

Once the design is finalized: log any significant decisions it locked in to `docs/decisions.md`, and update `TODO.md` if it changes near-term work. This is what makes the design doc compose with `project-status` / `save-progress` instead of being a one-off artifact nobody revisits.

## Notes

- One review round by default. This is a personal workflow, not an infinite refinement loop — don't re-invoke Codex repeatedly on the same doc unless the user asks for another pass.
- Reserve this for genuinely significant design decisions. Two full model passes plus synthesis is real time and cost — not worth it for routine or small changes.
- If `codex exec` fails (not installed, not authenticated, etc.), say so plainly and offer to proceed with just the draft, rather than silently skipping the review step.
