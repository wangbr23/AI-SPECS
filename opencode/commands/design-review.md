---
description: Draft, independently review, and finalize a grounded design document
agent: build
subtask: false
---

# Design Review

Run a three-point design process for the requested feature: ground and draft the design, obtain an independent read-only review from the `design-reviewer` subagent, then weigh the feedback and revise the document.

The feature or spec to review is: `$ARGUMENTS`

## Requirements

Read `AGENTS.md`, `docs/decisions.md`, and the relevant current code before drafting. If `$ARGUMENTS` names a spec, read it. The project should have `docs/designs/`; if it does not, report that and ask whether to create it rather than silently inventing a project layout.

## Draft

Create or revise `docs/designs/<date>-<slug>.md` using this structure:

- **Problem** — what is being solved and why
- **Grounding** — what exists now, citing real files
- **Goals / Non-goals** — explicit scope boundaries
- **Design** — the recommended approach and why it is the right-sized choice
- **Risks** — specific uncertainties and failure modes
- **Rollout** — build order when sequencing matters
- **Verification** — how success will be demonstrated

Choose one recommendation. Do not turn the document into an unranked survey of alternatives. Exclude line-level implementation code; that belongs in the build phase.

## Independent review

After saving the draft, invoke the `design-reviewer` subagent with the design path and ask it to review without editing. It must check:

1. Whether the design respects `AGENTS.md` and `docs/decisions.md`.
2. Whether a simpler approach meets the stated goals.
3. Security, privacy, data exposure, and operational risks.
4. Whether the scope is justified or over-built.
5. Whether the grounding and verification plan are sufficient.

Ask it to report each finding with its rationale and confidence. Do not paste entire context files into the subagent prompt; provide paths and let it read them in its own context.

## Weigh and revise

Read the review findings. For each finding, choose one of:

- Accept and revise the design.
- Reject with a brief reason when the concern does not hold up.
- Surface it to the user when it is a genuine unresolved judgment call.

Do not merge feedback mechanically. If a judgment call affects scope, architecture, security, or user-visible behavior, stop and ask the user rather than silently choosing a side.

Once finalized, append significant architectural decisions to `docs/decisions.md` and update `TODO.md` only when the design changes near-term work. Report the design path, accepted and rejected review findings, unresolved questions, and files updated.
