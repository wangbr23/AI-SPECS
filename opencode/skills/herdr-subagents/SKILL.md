---
name: herdr-subagents
description: Spawn subagents as coding agents in new Herdr tabs instead of in-process Task tool calls — tab per agent, self-contained prompt, state tracking via herdr CLI. Use when the user asks to spin up subagents in Herdr tabs, delegate work to parallel agents, run background agents, or when a project convention says subagents run in Herdr. Do not use for quick interactive Q&A delegation or when the user asks for a normal in-process subagent.
---

# Herdr Subagents

Runs subagent work as real agent processes in Herdr tabs rather than in-process subagents. The agents keep working across sessions, show `working`/`blocked`/`done` state in Herdr's sidebar, and can be attached to by the human at any time.

## When to use

- The user explicitly asks for subagents in Herdr tabs.
- Long-running or parallel tasks that benefit from persistence and visible state (dispatch-style work, one task per agent).
- Work that should keep running if this session ends.

Prefer in-process subagents for quick back-and-forth delegation — a tab agent shares no conversational context with this session, so anything it needs must be in the prompt or in files it can read.

## Requirements

This session must run inside a Herdr-managed pane. Verify first:

```bash
test "${HERDR_ENV:-}" = 1
```

If the check fails, say so and stop. Do not control a Herdr session from outside Herdr.

## Spawning a subagent

1. Create a tab in the current workspace. Read IDs from the JSON response (`.result.tab`, `.result.root_pane`) — never guess them:

   ```bash
   herdr tab create --cwd "$PWD" --label "<short-task-label>" --no-focus
   ```

2. Start a supported agent in that tab's root pane. Names must match `[a-z][a-z0-9_-]{0,31}` and be unique among live agents. `agent start` waits until the agent is detected and ready:

   ```bash
   herdr agent start <name> --kind opencode --pane <root_pane_id>
   ```

   Pass native agent arguments after `--` if needed.

3. Submit a **self-contained** prompt. The agent starts with zero shared context — point it at files instead of inlining everything (project conventions live in `AGENTS.md`, tasks in `TODO.md`, standards in `CLEANCODE.md`):

   ```bash
   herdr agent prompt <name> "Read AGENTS.md and CLEANCODE.md first. <task description with paths, constraints, and what to write where> Write your full report to <path> and finish." --wait --timeout 600000
   ```

   Have the agent write results to a file **inside the project cwd** (not `/tmp` or other external paths — those trigger a permission block) and report the path. That is the reliable way to collect output. `herdr agent read <name> --source recent-unwrapped --lines 200` is a fallback; agents on the alternate screen may not be readable that way. If blocked, `herdr agent read <name> --source visible` then `herdr agent send-keys <name> enter` to confirm a permission prompt.

4. For fire-and-forget parallel work, omit `--wait` and track completion with:

   ```bash
   herdr agent wait <name> --timeout 600000        # settled idle/done/blocked
   herdr agent wait <name> --until blocked --timeout 600000   # needs a decision
   ```

    If an agent is `blocked`, read its output (`herdr agent get`, `herdr agent read`) before sending input via `herdr agent prompt <name> "<answer>"`.

5. After you have collected the result, clean up what you created: delete the scratch result file (keep it only if the user asked to persist it) and close the tab. Do not leave throwaway reports in the project or in `/tmp`. Do not close tabs you did not create.

   ```bash
   rm -f <result-path>
   herdr tab close <tab_id>
   ```

## Rules

- Use `--no-focus` for background work unless the user asked to switch context.
- Parse IDs and states from JSON responses; do not derive them from sidebar order or examples.
- One concern per tab; use the task/TODO id as the agent name where one exists (e.g. `t3`).
- Close tabs you created once their work is collected. Do not close workspaces, tabs, panes, or agents you did not create unless the user explicitly asked.
- Never run `herdr server stop` from an active session.
- The installed binary is the authority on syntax — check `herdr <group>` help if a command shape is uncertain.

## Feedback into this skill

When a convention proves out in real use (prompt shape, result collection, naming), fold it back into this file so it persists. Machine-wide conventions belong here; per-project ones belong in the project's `AGENTS.md`.
