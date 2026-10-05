---
name: explain-plan
description: Visually explain a proposed code change and its current data flow before implementation
disable-model-invocation: true
---

# Explain Implementation Plan

Investigate a requested code change and explain the implementation that would occur, using Lavish as an interactive review surface. This command is a read-only preflight: do not implement the change after the explanation.

The requested change is: `$ARGUMENTS`

## Hard Boundary

- Do not modify source code, tests, configuration, project documentation, generated files, or lockfiles.
- The only files you may create or update are the Lavish artifact and its local assets under `.lavish/`.
- Do not begin implementation, even if the user approves the explanation. Approval confirms understanding only; implementation requires a separate request.

## Establish Scope

1. Read the repository's `AGENTS.md` and any directly relevant local instructions.
2. If the requested change is missing or too ambiguous to investigate, ask one short clarifying question before continuing.
3. Inspect the relevant code, tests, interfaces, schemas, and design or decision documents. Follow the existing request and data flow end to end rather than inferring it from filenames or a diff alone.
4. Identify the smallest implementation that satisfies the request and follows established project patterns. Mark uncertainty explicitly; do not invent missing behavior.

## Required Explanation

The artifact must make these five topics easy to scan and annotate:

1. **Files and components involved**: Show each relevant file or component, its current responsibility, and whether it would be modified, added, or only referenced. Include useful file and line references.
2. **Existing request and data flow**: Use a clear, labeled flow diagram to trace the current path from entry point through processing, state or persistence, and response or rendering. Separate verified behavior from unresolved questions.
3. **Planned changes**: Explain the proposed behavior and implementation sequence, including where the current flow changes and why.
4. **New abstractions**: Name every proposed type, module, service, hook, component, helper, or interface and explain its responsibility and boundary. If none are needed, say `No new abstractions` and explain why existing structures are sufficient.
5. **Explicit non-goals**: State what will not change, including nearby behavior, interfaces, data, migration work, refactors, or compatibility paths that are intentionally outside scope.

Add concise sections for verification, meaningful risks, and unresolved questions when they affect the plan. Do not pad the artifact with generic advice.

## Lavish Workflow

1. Follow the lavish CLI's current guidance rather than relying on remembered instructions.
2. Run `npx -y lavish-axi --help` and open every matching playbook before authoring. At minimum use the `plan`, `diagram`, and `input` playbooks.
3. Inspect the subject project's design system and match it. If the project has no applicable visual language, run `npx -y lavish-axi design` and use its recommended fallback.
4. Create a descriptively named HTML artifact under `.lavish/`. Prefer a small architecture overview plus focused detail cards over one dense diagram. Keep it responsive and usable on mobile.
5. Include an interactive review form that lets the user queue either:
   - confirmation that the explanation is accurate, while clearly stating that no coding will begin; or
   - specific revision feedback about scope, flow, abstractions, or non-goals.
6. Open the artifact with `npx -y lavish-axi <html-file>` and state which design source was used and why.
7. Run `npx -y lavish-axi poll <html-file>` in the foreground and wait for feedback. Never kill or detach the poll.
8. If the user requests revisions, update only the artifact, reopen or resume it as directed by the CLI, and poll again. If the user confirms or ends the review, stop without coding and give a concise chat summary with the artifact path.

## Quality Bar

- Ground every architectural claim in inspected code and cite the strongest evidence.
- Explain the current state before the proposed state so the delta is obvious.
- Prefer plain language, short labels, diagrams, tables, and cards over long prose.
- Make proposed additions visually distinct from unchanged existing behavior.
- Do not disguise guesses as decisions. Surface conflicts and open questions for review.
- Keep the proposal minimal. Do not introduce an abstraction unless it has a concrete responsibility in this change.
