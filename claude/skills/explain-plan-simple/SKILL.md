---
name: explain-plan-simple
description: Explain a proposed code change in plain English before implementation
disable-model-invocation: true
---

# Explain Implementation Plan (Simple)

Investigate a requested code change and explain it in plain English, as simply and concisely as possible. This command is a read-only preflight: do not implement the change after the explanation.

The requested change is: `$ARGUMENTS`

## Hard Boundary

- Do not modify or create any files.
- Do not begin implementation, even if the user approves the explanation. Approval confirms understanding only; implementation requires a separate request.

## Establish Scope

1. If the requested change is missing or too ambiguous to investigate, ask one short clarifying question before continuing.
2. Inspect only the code needed to understand the change. Do not exhaustively map the surrounding system.

## Required Explanation

Answer exactly two questions in plain English that a non-expert can follow:

1. **What is this change meant to accomplish?** One to three sentences describing the goal in everyday terms.
2. **How will we accomplish it?** A short numbered list of the concrete steps, each naming the file(s) it touches.

That is the whole explanation. No sections for data flow, abstractions, non-goals, risks, or verification unless the user asks.

## Response

- Return the explanation directly in chat using concise Markdown. Do not create any files or artifacts.
- Keep it under 200 words. Cut every sentence that does not help the user understand the goal or the steps.
- Stop after the explanation without coding or creating files.

## Quality Bar

- Use plain, simple language; avoid jargon and file-format details unless they are the point.
- Ground each step in the actual code; do not invent behavior.
- If something important is uncertain, say it in one short line instead of guessing.
