---
name: grill-me
description: A relentless interview to sharpen a loose project idea into product requirements and decisions, then save the outcome to disk. User-invoked only — run /skill:grill-me.
disable-model-invocation: true
---

# Grill Me

Takes a loose idea and interviews the user until they can commit to it, then writes down what was decided so the session isn't lost when the conversation ends.

## Steps

1. Ask what idea is being grilled, if it isn't already stated. Confirm you're starting from a genuinely loose idea, not a plan someone already wrote — if a fleshed-out plan already exists, this is the wrong tool (that's a review, not a grilling).

2. Load the `grilling` skill instructions from the sibling skill (`../grilling/SKILL.md`) and run the interview to completion: rounds of frontier questions, one round at a time, until the frontier is empty and the user confirms shared understanding.

3. Once the session is done, save it:
   - Pick a short kebab-case slug from the idea (e.g. `subscriber-email-digest`).
   - Write `docs/specs/{{slug}}.md` (create `docs/specs/` if this project has no docs scaffolding yet, mirroring what `project-init` sets up for `docs/designs/`). Keeping specs in their own directory, separate from `docs/designs/`, avoids collision with `design-review`'s `docs/designs/<date>-<slug>.md` output — same idea/feature, two different documents (what/why vs. how), at predictably different paths:
     - Title, date, one-line description of the idea.
     - The resolved decisions, organized by the rounds/topics they came up in — not a raw transcript, a clean synthesis: each decision stated plainly with the reasoning, not just "Q: ... A: ...".
     - Anything explicitly left open or marked ungrillable (needs a prototype, needs data, etc.), so it isn't silently forgotten.
   - If `docs/decisions.md` already exists in this project, append one entry there in its existing format for any decision that's architecturally load-bearing (affects structure, not just scope) — pointing back to the spec for full context. Skip this step if the file doesn't exist; don't create a whole decisions log just for one entry.
   - If `docs/journal.md` already exists, append a short entry noting the grilling session happened and linking the new spec.
   - Report the file(s) written.

Don't skip the save step even if the user seems ready to move straight to building — the whole point is that the resolved idea outlives the chat.
