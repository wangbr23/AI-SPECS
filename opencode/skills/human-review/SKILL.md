---
name: human-review
description: Render a visual, human-reviewable diff — for the current uncommitted changes, a single commit, a commit range, or another worktree/branch — with a short "why" written next to each changed file. The diff parsing and HTML rendering are done by a script (zero AI tokens); AI only writes the why text. Use when the user wants to visually review changes, see a diff with rationale, get a "human review" of what was built, or asks to review a worktree/commit/PR-style diff before merging.
---

# Human Review

Produces a local HTML page: one collapsible section per changed file, syntax-colored diff lines, and a one-line "why this changed" under each file's header. Complements `code-review` (correctness bugs) and `simplify` (cleanup) — this skill does neither; it's purely for a human to look at what changed and understand why, quickly.

**Token discipline is the point of this skill.** `scripts/gen_diff.py` does 100% of the git plumbing, diff parsing, and HTML/CSS rendering — no AI call is involved in producing the visualization. The only AI-generated content is a short why-string per file, written once, then spliced in by `scripts/inject_why.py` (also no AI). Never hand-write or regenerate the HTML yourself — always go through the scripts.

## Step 1 — pick the mode

Ask only if the target is genuinely ambiguous from context; otherwise infer it:

| User says... | mode | target |
|---|---|---|
| "review my changes" / "what did I just do" (nothing committed) | `current` | — |
| "review commit `<sha>`" | `commit` | `<sha>` |
| "review `main..feature`" / "review this PR" | `range` | `base..head` |
| "review the worktree at `<path>`" / a `dispatch`-created worktree | `worktree` | `<path>` |

## Step 2 — generate the diff + HTML (script, no AI)

```
python3 ~/.claude/skills/human-review/scripts/gen_diff.py <mode> [target] \
  --out <scratchpad>/human-review.html \
  --json <scratchpad>/human-review.json
```

- Use the session's scratchpad directory for `--out`/`--json`, not `/tmp` directly.
- `worktree` mode takes `--base <branch>` if the default main/master detection is wrong for this repo.
- `range` mode expects `base..head` (or `base...head` — both are treated as merge-base diffs).
- The command prints how many files changed. If it's 0, say so and stop — nothing to review.

## Step 3 — write the why (AI, this is the only prose step)

Read `--json`'s output (`files[].diff`, plus `commits[]` if present) — that's the deterministic diff content, no need to re-run git yourself. For each changed file, write one to three sentences on *why* this file changed, not what changed (the diff already shows what):

- If `commits[]` is populated and a commit's subject/body already explains the file's change, lean on it — summarize, don't reinvent.
- If the changes were made earlier in *this* conversation, use that context directly instead of re-deriving intent from the diff text.
- Otherwise, infer from the diff itself, but keep it to the rationale (what problem this solves, what it enables, what constraint it satisfies) — skip restating line-by-line mechanics.
- Skip files where "why" would just restate the filename (e.g. a generated lockfile) — write something short like "dependency lockfile, regenerated automatically" rather than forcing a strained explanation.

Write this as a flat JSON object, `{"path/to/file": "why text", ...}`, to a scratch file — do not edit the HTML directly.

## Step 4 — splice it in (script, no AI)

```
python3 ~/.claude/skills/human-review/scripts/inject_why.py \
  --html <scratchpad>/human-review.html \
  --why <scratchpad>/human-why.json
```

Check its output for "no placeholder found" warnings — that means a path in your why-map didn't match a file in the diff (usually a typo'd path); fix and rerun rather than leaving it silently dropped.

## Step 5 — hand it to the user

Default to opening it locally: `open <scratchpad>/human-review.html` (macOS). This costs nothing and needs no network.

Only publish via the `Artifact` tool if the user asks to share it or view it outside this machine — load `artifact-design` first per its own rules, and note the page is already self-contained (inline CSS, no external CDN calls) so it publishes as-is. Don't default to publishing; a local open is enough for the stated use case of the user reviewing their own work.

## Notes

- If a diff is large enough that writing a why-blurb per file would itself be a lot of tokens, group files that changed for the same reason (e.g. every file under a new module) and write one shared why-string, applying it to each of their keys in the JSON map — don't pad out near-duplicate sentences per file.
- This skill doesn't judge correctness or quality — if the user wants that too, chain into `code-review` afterward rather than folding bug-hunting into this pass.
