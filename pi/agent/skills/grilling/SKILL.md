---
name: grilling
description: Grill the user relentlessly about a product idea, plan, or decision until requirements and open questions are clear. Use when the user wants to harden product requirements, stress-test thinking, iron out idea details, or uses any "grill" trigger phrase.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **product requirements tree**: every product decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, existing code, web research, etc.), go find it yourself — dispatch a sub-agent if the search is nontrivial; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for it to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

Some questions are **ungrillable**: things like "how should this feel?" or "one long form or three short screens?" have no answer that talking will reach — they need something to react to, not more discussion. If you hit one, say so plainly, suggest the cheapest way to get a real answer (a sketch, a throwaway prototype, a quick look at a comparable), and move it out of the frontier rather than trying to talk your way to a decision.

Watch for **passive answers** — "sure", "agreed", "whatever you think" repeated across many questions with no pushback. That's a sign the questions have drifted below the fidelity the user actually cares about, or that the session is running past the point of value. Say so and offer to wrap up rather than grinding on.

The session is done when the frontier is empty: every branch of the product requirements tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
