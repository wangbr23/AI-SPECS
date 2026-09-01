---
name: save-progress
description: End-of-session reconciliation for project memory: update docs/journal.md, docs/decisions.md, docs/specs, docs/designs, and TODO.md based on completed work, landed tasks, open branches, and newly surfaced follow-ups. Use when wrapping up or saving session progress.
---

# Save Progress

Bring the project's persistent context files up to date so the next session can resume from disk rather than chat history.

## When to run

Run at the end of a work session, after landing tasks, after producing specs/designs, or whenever the user asks to wrap up, close out, checkpoint, or save progress.

## Requires

Expected project scaffold from `project-init`:

- `AGENTS.md`
- `CLEANCODE.md` if present
- `TODO.md`
- `docs/journal.md`
- `docs/decisions.md`
- `docs/specs/`
- `docs/designs/`

If these are missing, say what is missing and suggest `project-init` first. Do not invent a different layout.

## Principles

- `docs/journal.md` and `docs/decisions.md` are append-only.
- `TODO.md` is mutable and should reflect real current work.
- Product requirements belong in `docs/specs/`.
- Implementation designs belong in `docs/designs/`.
- Do not check off a task merely because `dispatch` implemented a branch. Check it off only if it was reviewed/merged or the user explicitly confirms it is complete.
- Do not record noisy implementation trivia as architecture decisions.

## Steps

### 1. Establish what changed

Read:

- latest entries in `docs/journal.md` to identify the last saved checkpoint;
- `TODO.md`;
- `docs/decisions.md`;
- recent files in `docs/specs/` and `docs/designs/`;
- git state if this is a repo:

```bash
git status --short
git log --oneline --decorate -n 20
git branch --list
git worktree list
```

Use conversation context plus git/disk state. If there is uncertainty about whether something was completed or merely attempted, ask.

### 2. Update journal

Append one new entry to `docs/journal.md` with today's date (`YYYY-MM-DD`). Include:

- what changed this session;
- what was decided or clarified;
- what was implemented/landed;
- what remains in progress or awaiting review;
- recommended next step.

Never edit previous journal entries. If an older entry is now wrong, note the correction in the new entry.

### 3. Update decisions

Append entries to `docs/decisions.md` only for durable technical/architecture decisions, such as:

- dependency/framework choices;
- data model/schema decisions;
- API/interface boundaries;
- security/auth/storage strategy;
- rejected approaches worth remembering;
- decisions that future agents must not accidentally reverse.

Skip this step if no decision-worthy changes occurred. If ambiguous, ask before adding noise.

### 4. Save specs/designs if needed

If this session produced product requirements or implementation designs that only exist in chat, save them:

- product/requirements output -> `docs/specs/<slug>.md`
- implementation design output -> `docs/designs/<date>-<slug>.md`

Do not duplicate files that already exist. Prefer linking existing specs/designs from journal/TODO.

### 5. Reconcile TODO

Update `TODO.md` to match reality:

- Check off tasks only when reviewed/merged or explicitly confirmed complete.
- Leave dispatched-but-unmerged tasks unchecked; optionally add a note that they are awaiting review if useful.
- Add follow-up tasks discovered during implementation/review.
- Preserve task ids. Never renumber or reuse `T<n>` ids.
- Use `plan-tasks` format for new tasks: `agent`/`manual`, `depends-on`, `design:` when applicable, and `Done when:` for nontrivial tasks.
- Remove or rewrite stale open tasks only if they are clearly obsolete; otherwise ask.

### 6. Report what was updated

Return a concise summary:

```md
## Progress saved

- Journal: appended <date> entry
- Decisions: added <n> entries / none
- Specs: saved <paths> / none
- Designs: saved <paths> / none
- TODO: checked off <tasks>, added <tasks>, left awaiting review <tasks>
- Next recommended step: ...
```

## Notes

- Save-progress is not a merge tool. Use `land-task` for human-approved merges and TODO checkoff.
- Prefer asking one clarifying question over writing misleading persistent context.
- Context files should help future agents, not become a transcript dump.
