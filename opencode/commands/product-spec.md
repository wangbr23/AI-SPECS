---
description: Create a product spec — detailed functional and non-functional requirements from the user's perspective, no technical details
agent: build
---

Create a product specification document that defines what an app or feature should do from the user's perspective. This is a non-technical document — it describes behavior, not implementation. Technical decisions should work backwards from this document.

If `$ARGUMENTS` names a specific output path, write there; otherwise write to `docs/designs/product-spec.md`.

Gather, unless already known from the conversation or repository:

- Product/feature name
- One-line description
- Target users (who is this for, at what scale)
- Core concepts (the nouns — what are the main objects/entities the user interacts with?)
- What the user has already decided about functionality (features, modes, behaviors)
- Any non-functional constraints they care about (performance, offline, privacy, platform)
- What's explicitly out of scope

Write the spec as Markdown with this structure:

```
# <Product Name> — Product Spec

**Last updated:** <YYYY-MM-DD>

## Overview
One paragraph: what it is, who it's for, what scale.

## Core Concepts
Define each major object/entity the user interacts with.
For each: what it is, what properties it has, what states it can be in.
Write these as plain descriptions, not database schemas.

## Functional Requirements
Grouped by feature area (e.g. FR-1: Trip Management, FR-2: Maps).
Each requirement gets a numbered ID (FR-1.1, FR-1.2, ...).
Written as "The user can..." or "The system shows..." statements.
Specific enough to be testable.

## Non-Functional Requirements
Grouped by concern (performance, offline, privacy, usability, etc.).
Each gets a numbered ID (NFR-1.1, NFR-1.2, ...).
Include concrete thresholds where possible (e.g. "under 1 second" not "fast").

## Out of Scope for MVP
Explicit list of things that are NOT in this version.
```

Guidelines:

- Every requirement is from the user's perspective. "The user can..." not "The API exposes..."
- No implementation details. Don't mention databases, frameworks, APIs, or data types.
- Be specific enough to test. "The user can delete a trip" is better than "trip management."
- Include edge cases as requirements when they affect user-visible behavior.
- Group requirements logically by feature area, not by technical layer.
- Use present tense, active voice.
- Out of Scope is required — it's as important as what's in scope.

After writing, report the requirement count and suggest the user review before proceeding to technical planning.
