---
description: Interactively sharpen a loose idea into a confirmed spec and save it to disk
agent: build
subtask: false
---

# Grill Me

Interview the user until a loose idea becomes a confirmed set of decisions, then persist the result so it survives the session. This is an interactive command: ask one round of questions, wait for the user's answers, and only then compute the next round.

The idea to grill is: `$ARGUMENTS`

## Start

If no idea was supplied, ask what idea the user wants to explore. Confirm that it is genuinely loose rather than an existing implementation plan or design document. If it is already fleshed out, explain that this command is for discovery and recommend a design review instead.

## Interview method

Maintain a decision tree. The current frontier is every decision whose prerequisites are settled. In each round:

1. Ask every question currently on the frontier in one message.
2. Number the questions and provide a recommended answer for each.
3. Explain the meaningful tradeoff briefly when it helps the user decide.
4. Wait for the user's answers before asking the next round.
5. Recompute the frontier from the answers. Do not ask downstream questions before their prerequisites are settled.

Use the native `question` tool for decisions that need structured user input. Ask open-ended questions when the decision cannot be reduced to useful options. Do not ask the user for facts that can be established from the repository, local tools, or external documentation.

For factual prerequisites, inspect the repository directly or invoke `@explore` for local read-only investigation and `@scout` for external documentation or dependency research. Keep those investigations read-only and report relevant findings before asking dependent questions.

Some decisions cannot be resolved through discussion, such as visual feel or interaction quality. Identify these as ungrillable, recommend the cheapest experiment or prototype that would answer them, and record them as explicitly open. Do not pretend a discussion settled them.

Watch for repeated passive answers such as "whatever you think." If the questions have become too detailed or the session is no longer producing useful decisions, say so and offer to wrap up.

The interview is complete only when the frontier is empty and the user confirms shared understanding. Do not build or write the spec before that confirmation.

## Save the result

After confirmation:

1. Choose a short kebab-case slug from the idea.
2. Create `docs/specs/` if it does not exist.
3. Write `docs/specs/<slug>.md` containing:
   - Title, date, and one-line description
   - Resolved decisions organized by topic or interview round
   - Reasoning behind each decision
   - Explicitly open questions and ungrillable items
4. If `docs/decisions.md` exists, append entries for decisions that affect architecture or system structure, linking to the spec. Do not create the decisions log solely for this command.
5. If `docs/journal.md` exists, append a short entry noting the interview and linking to the spec.
6. Report the files written.

Never edit prior journal or decision entries. If the project context files are missing, say so and still save the spec unless doing so would overwrite an existing file.
