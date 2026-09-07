# CLAUDE.md — template-base

**[AGENTS.md](AGENTS.md) is the source of truth — read it first.** This file holds only
Claude-specific notes and must not duplicate AGENTS.md.

## Commands
- `/bootstrap` — run once in a fresh copy of this repo to re-point it at its own identity.
  You invoke it; Claude never runs it on its own.

## Permissions
Permission rules live in [.claude/settings.json](.claude/settings.json). Policy: file edits
apply without prompting (`defaultMode: acceptEdits`), so commit at each logical checkpoint —
git is the undo, not the edit prompt. `git push` prompts (ask); `sudo`, `rm -rf`, reads of
`.env*`, and reads of `~/.ssh/**` are denied. Do not weaken these.

## MCP servers
<!-- List repo-specific MCP servers and how to authenticate them, or "none". -->
none

## Subdirectory overrides
<!-- Note any nested AGENTS.md / CLAUDE.md that override this one for a subtree. -->
none
