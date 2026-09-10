---
description: Explain completed code changes, their rationale, implementation, and connection to future work
agent: plan
---

# Explain Changes

Produce a grounded, developer-oriented walkthrough of recently completed work. Explain the implementation; do not review, modify, or merely restate the diff.

The task or scope to explain is: `$ARGUMENTS`

## Establish Scope

- If `$ARGUMENTS` names a task, commit, range, branch, worktree, or set of files, use that scope.
- Otherwise, default to the task most recently completed in the current conversation.
- Use conversation context to understand intent and the repository state to verify what was actually implemented.
- Do not attribute unrelated working-tree changes to the completed task. If scope remains ambiguous after inspecting the available context, ask one short clarifying question.

## Process

1. Read the repository's `AGENTS.md` and any directly relevant local instructions.
2. Establish the task's intended outcome from the current conversation, named task, issue, design document, or commit message.
3. Inspect the relevant diff and enough surrounding code to understand the resulting behavior, data flow, interfaces, and established architecture. Include staged changes and new files when applicable.
4. Read relevant sections of `TODO.md`, `docs/designs/`, `docs/decisions.md`, or similar planning files when they exist and help establish how this task relates to later work.
5. Reconcile intent with implementation. If the code differs materially from the stated plan, call out the difference rather than silently describing the plan as completed.
6. Explain the work at the level appropriate to its complexity, using file and line references for important implementation points.

## Response

Organize the explanation around behavior and concepts, not a file-by-file diff dump. Use only the sections that add value:

- **Outcome**: What capability, fix, or internal improvement now exists.
- **What Changed**: The major implementation pieces and how they work together.
- **Why**: The problem each important choice solves and any meaningful tradeoffs or constraints.
- **Execution Flow**: A concise end-to-end walkthrough for changes with non-obvious control flow, state transitions, data movement, or component interactions.
- **Future Work**: How this work enables, constrains, or serves as a prerequisite for known next tasks.
- **Verification**: Tests, checks, and relevant scenarios that establish confidence in the implementation.

Scale the depth to the change. A small fix may need only a few paragraphs; a cross-cutting feature may need all sections.

## Future Work

- Prefer explicit evidence from `TODO.md`, design documents, decisions, issue text, or the current conversation.
- Distinguish committed follow-up work from optional possibilities. Label possibilities as such.
- Explain the technical connection by identifying the API, data model, boundary, abstraction, or invariant that future work will build on.
- If no future work is documented or clearly implied, say so briefly instead of inventing a roadmap.

## Guardrails

- This command is read-only. Never edit code or project documentation.
- Do not perform a code review unless the user asks for one. Mention a limitation only when it is important to understanding what was built or remains unfinished.
- Do not narrate every changed line, import, formatting update, generated file, or lockfile entry.
- Do not claim motivations unsupported by context or code; mark uncertain inferences explicitly.
- Do not rely on the diff alone when surrounding code is needed to explain how the change behaves.
- Prefer concrete language and code references over generic praise or implementation summaries.
