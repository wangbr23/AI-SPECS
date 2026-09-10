---
name: low-level-design
description: Draft a low-level design (LLD) from a high-level design doc — package/file layout, data model, API surface, flow sequences, pinned mechanism choices, failure paths, test mapping — written to docs/designs/ as a sibling -lld.md. Use when the user asks for a low-level design, LLD, detailed design, implementation design, or asks how something will actually be implemented or work together.
---

# Low-Level Design

The bridge between a high-level design (HLD: *what and why*) and the build phase (*code*). The LLD answers: what files will exist, what data flows through them, what the interfaces are, and how the pieces behave together — with enough pinned decisions that an implementing agent never has to guess a mechanism, but without writing the implementation.

## When to run

When the user asks for a "low-level design", "LLD", "detailed design", "implementation design", or asks "how will this actually work/be implemented". Requires an HLD to exist (usually `docs/designs/<date>-<slug>.md` from the design-review skill) — an LLD without a higher-level design drifts into re-deciding scope. If there's no HLD, say so and suggest drafting one first.

## Steps

### 0. Ground before deriving

- Locate the HLD: explicit path in the user's arguments, else the newest design doc in `docs/designs/` that is not itself an LLD (`-lld.md`). If ambiguous, ask.
- Read the HLD in full, `docs/decisions.md` in full, and `AGENTS.md`. Skim the source spec if the HLD links one.
- Inspect the actual repository state — file tree, existing code, platform contracts. An LLD grounded in a stale repo picture is worse than none.

### 1. Derive the LLD

Write `docs/designs/<date>-<slug>-lld.md` (same date and slug as the HLD, `-lld` suffix). Use this fixed structure:

- **Overview** — one paragraph: what will be built and how the pieces connect. Point to the HLD for decisions; never restate them.
- **Package/file layout** — file tree with a one-line responsibility per file. Flag any file likely to become a god file.
- **Data model** — core types as shape sketches (field names + comments, no methods), plus any invariant that other sections depend on (state it as a named rule).
- **Interfaces / API surface** — route tables, module boundaries, or protocol shapes, whatever the system's joints are.
- **Flow sequences** — numbered walkthroughs of the main end-to-end flows, naming the files/functions involved at each step.
- **Mechanisms** — the choices the HLD left open. Pin each with its one-line reasoning, and state any accepted weakening honestly.
- **Failure/degradation paths** — a table: failure → behavior. Failures the HLD accepted get carried forward, not silently dropped.
- **Test mapping** — how the HLD's verification list maps onto concrete test files/scenarios.
- **Open questions** — anything genuinely unresolved, numbered, with the accepted-for-now stance if there is one.

Rules:

- Shape sketches and command lines are fine; no implementation code. If a section needs real code to be intelligible, the design isn't done thinking.
- Pin every mechanism ("polling vs SSE → SSE, because EventSource can't set headers"). A mechanism with no stated why is a guess.
- Never contradict `docs/decisions.md`. If the derivation surfaces a conflict, stop and surface it to the user instead of quietly picking a side.
- Unresolved gaps become open questions — never a quiet guess dressed up as a decision.

### 2. Cross-link

Add an `**LLD:**` line under the HLD's header linking to the LLD, and link back to the HLD from the LLD header. The pair should be discoverable from either side.

### 3. Close the loop

- If derivation forced load-bearing decisions not already in `docs/decisions.md` (e.g. a security tradeoff with consequences), append a decision entry — that log is the terminal home for decisions, not this skill.
- Do not update `TODO.md` unless the LLD changed the work breakdown; an LLD usually refines existing tasks rather than creating them.
- Append a journal entry for the session as usual.

### 4. Sanity pass

Before reporting done, verify: every HLD goal has a corresponding LLD section; the test mapping covers the HLD's full verification list; no section re-litigates a settled decision; a reader who never saw the chat could implement from HLD + LLD without inventing a mechanism.
