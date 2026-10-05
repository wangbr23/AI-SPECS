---
name: explain-plan-quick
description: Quickly explain a proposed code change and its current data flow before implementation
disable-model-invocation: true
---

# Explain Implementation Plan (Quick)

Investigate a requested code change and explain the implementation directly in chat. This command is a read-only preflight: do not implement the change after the explanation.

The requested change is: `$ARGUMENTS`

## Hard Boundary

- Do not modify source code, tests, configuration, project documentation, generated files, or lockfiles.
- Do not create a Lavish artifact or any other files.
- Do not begin implementation, even if the user approves the explanation. Approval confirms understanding only; implementation requires a separate request.

## Establish Scope

1. Read the repository's `AGENTS.md` and any directly relevant local instructions.
2. If the requested change is missing or too ambiguous to investigate, ask one short clarifying question before continuing.
3. Inspect the relevant code, tests, interfaces, schemas, and design or decision documents. Follow the existing request and data flow end to end rather than inferring it from filenames or a diff alone.
4. Identify the smallest implementation that satisfies the request and follows established project patterns. Mark uncertainty explicitly; do not invent missing behavior.

## Required Explanation

Make these five topics easy to scan:

1. **Files and components involved**: Show each relevant file or component, its current responsibility, and whether it would be modified, added, or only referenced. Include useful file and line references.
2. **Existing request and data flow**: Trace the current path from entry point through processing, state or persistence, and response or rendering. Use a concise numbered flow or text diagram when it improves clarity. Separate verified behavior from unresolved questions.
3. **Planned changes**: Explain the proposed behavior and implementation sequence, including where the current flow changes and why.
4. **New abstractions**: Name every proposed type, module, service, hook, component, helper, or interface and explain its responsibility and boundary. If none are needed, say `No new abstractions` and explain why existing structures are sufficient.
5. **Explicit non-goals**: State what will not change, including nearby behavior, interfaces, data, migration work, refactors, or compatibility paths that are intentionally outside scope.

Add concise sections for verification, meaningful risks, and unresolved questions when they affect the plan. Do not pad the response with generic advice.

## Response

- Return the explanation directly in chat using concise Markdown. Do not create any HTML artifacts or files.
- Prefer a short overview followed by focused sections over one long narrative.
- Scale the depth to the requested change while covering all five required topics.
- Stop after the explanation without coding or creating files.

## Quality Bar

- Ground every architectural claim in inspected code and cite the strongest evidence.
- Explain the current state before the proposed state so the delta is obvious.
- Prefer plain language, short labels, lists, and small tables over long prose.
- Clearly distinguish proposed additions from unchanged existing behavior.
- Do not disguise guesses as decisions. Surface conflicts and open questions for review.
- Keep the proposal minimal. Do not introduce an abstraction unless it has a concrete responsibility in this change.
