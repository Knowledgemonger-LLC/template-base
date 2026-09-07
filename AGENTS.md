# AGENTS.md — template-base

**This file is the canonical, cross-tool source of truth for AI agents working in this repo.**
Tool-specific files (e.g. `CLAUDE.md`) reference it; they must not duplicate it.

## Boundaries — do not touch
- Do not edit generated files or dependency lockfiles by hand.
- Do not commit secrets. `.env*` is git-ignored (except `.env.example`).
- Do not weaken the `deny` rules or `defaultMode` in `.claude/settings.json`.

## Change protocol

Defining files — `GLOSSARY.md`, this file, and any interface contract, schema, infrastructure
design, or requirements document — need the change written up and approved before you edit them.
Everything else you edit directly, without asking. The **`change-protocol`** skill holds the full
rules: what counts as setting a precedent, why approval is per decision rather than per edit, and
when to stop mid-implementation. Read it before changing a defining file.

## Terminology and structure

- Reuse existing vocabulary. Never introduce a synonym for a term already in use — reuse it, or flag
  the duplication. Never use a plain-English word to mean something this project defines differently.
- A type, constant, or schema has exactly one owning location — import it, do not redeclare it.
- A fact lives in one place. Do not store what can be derived. A cache is the exception, when
  documented as one with its invalidation stated.
- Do not propose splitting, merging, or reorganizing modules, services, or repos unless asked.

## Stack

Documents and configuration only — Markdown, JSON, and dotfiles. No application code, no
dependencies, no package manager.

## Build / Test / Run

None. There is nothing to build, test, or run. Verification is review: read the files as a
newcomer would and confirm they would still make sense in a repo that is not this one.

## Conventions
- Match the existing style of whatever you are editing.
- Keep changes scoped and atomic. Use Conventional Commits (`feat:`, `fix:`, `chore:` …).
- Prefer the documented commands above over ad-hoc invocations.

## Working on template-base

This repo is the starting point other repos are copied from. Four rules follow from that:

1. **Copies are one-way.** Nothing here propagates. A repo created from this one never looks
   upstream again, and no tooling detects that it has fallen behind.
2. **The whole repo is the payload.** There is no `template/` subdirectory — what sits at the root
   is exactly what a new repo receives. Anything you add here, every future repo inherits.
3. **Record what is worth porting.** A change to the working agreement only reaches existing repos
   if a human carries it there. Add a line to `CHANGELOG.md` so they know it exists.
4. **Keep it copy-ready.** Nothing specific to template-base belongs outside this section — that is
   what keeps `/bootstrap`'s job small. Write for the next repo, not for this one.

<!-- Add repo-specific conventions, architecture notes, and gotchas below. -->
