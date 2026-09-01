---
name: project-status
description: Read AGENTS.md, CLEANCODE.md, TODO.md, docs/specs, docs/designs, docs/journal.md, docs/decisions.md, and git/worktree state to summarize an existing project's current state and recommended next step. Use at session start or when the user asks what's done, in progress, blocked, or next.
---

# Project Status

Read-only project orientation. Builds an up-to-date picture from persistent context files and git state instead of guessing from chat history.

## When to run

Run at the start of a session on an existing project, after returning to a project, or whenever the user asks:

- what's the state of this project?
- what have we done so far?
- what's next?
- what tasks are ready?
- what branches/worktrees are in progress?

## Requires

Expected project scaffold from `project-init`:

- `AGENTS.md`
- `CLEANCODE.md` if present
- `TODO.md`
- `docs/journal.md`
- `docs/decisions.md`
- `docs/specs/`
- `docs/designs/`

If core files are missing, say what is missing and suggest `project-init` rather than inventing a status summary.

## Steps

### 1. Read project context

Read:

- `AGENTS.md` — project purpose, stack, commands, architecture, workflow.
- `CLEANCODE.md` if present — coding/reviewability rules.
- `TODO.md` in full — done/open/manual/agent tasks and dependency frontier.
- recent `docs/journal.md` entries — enough to understand the latest session state.
- `docs/decisions.md` in full — durable architecture/technical constraints.

### 2. Inspect specs and designs

List:

- `docs/specs/*.md`
- `docs/designs/*.md`

Skim the most recent and/or task-linked files, especially designs referenced in open TODO tasks.

### 3. Inspect git state

If this is a git repo, inspect read-only state:

```bash
git status --short
git branch --show-current
git branch --list
git worktree list
```

Look for:

- dirty working tree;
- dispatch branches like `dispatch/T...`;
- task worktrees awaiting review;
- signs that TODO may not reflect merged work.

Do not modify anything.

### 4. Compute task frontier

Using `plan-tasks` rules:

- **Agent-ready:** unchecked `agent` tasks whose dependencies are checked.
- **Manual-ready:** unchecked `manual` tasks whose dependencies are checked.
- **Blocked:** unchecked tasks waiting on dependencies.
- **Done:** checked tasks.

Also identify tasks that appear implemented in branches/worktrees but not yet landed, if possible.

### 5. Report status

Synthesize; do not dump file contents. Use this shape:

```md
## Project status

### What this project is
- ...

### Current state
- Built/done: ...
- In progress / awaiting review: ...
- Dirty working tree or branch notes: ...

### Task frontier
- Agent-ready: ...
- Manual-ready: ...
- Blocked: ...

### Relevant specs/designs
- ...

### Decisions to keep in mind
- ...

### Recommended next step
- Run `/skill:dispatch` / `/skill:code-review` / `/skill:land-task` / `/skill:save-progress` / other, with reason.
```

## Notes

- Read-only. Never edit files as part of this skill.
- If docs conflict with code/git state, say so plainly.
- Prefer actionable status over exhaustive history.
