# AGENTS.md — template-base

**This file is the canonical, cross-tool source of truth for AI agents working in this repo.**
Tool-specific files (e.g. `CLAUDE.md`) reference it; they must not duplicate it.

## Boundaries — do not touch
- Do not edit generated files or dependency lockfiles by hand.
- Do not commit secrets. `.env*` is git-ignored (except `.env.example`).
- Do not weaken the `deny` rules or `defaultMode` in `.claude/settings.json`.

## Change protocol

A file either **defines** a decision others depend on, or **implements** one already recorded.
Defining files: `GLOSSARY.md` (what terms mean), this file, and any interface contract, schema,
infrastructure design, or requirements document. Everything else implements — source, tests,
migrations, build config, `README.md`, changelogs.

- **Defines** → write the change up and get approval before editing.
- **Implements** → edit directly, without asking.
- **Both** → decision first, reported, then implementation. Never both in one diff.

**Approval is per decision, not per edit.** Approval given in conversation counts, and recording it
in the owning document needs no second round. Once a decision is approved, every edit that follows
from it proceeds without further approval — however many files, however long it takes. Do not
re-confirm scope or ask permission to continue partway through; report when the work is done or
when it stops.

Come back mid-implementation only if the decision does not cover the case in front of you (a gap,
not a detail), if following it would produce something you believe is wrong, or if the next step is
irreversible or outward-facing. Ambiguity that any reasonable reading resolves the same way is not a
gap — take the reading, state the assumption, and keep going.

A change that sets a precedent rather than follows one — a test asserting behavior no document
specifies, a config value whose meaning changes rather than its number — is defining. A detail an
approved decision implies but did not enumerate is not. Never record a design decision only in a
code comment or a commit message.

## Asking for human input

Write for a reader who has not been following the work: intelligent, knows basic Python and data
science, has a high-level sense of what this repo is for, and no other technical or domain depth.
Do not assume they have read the conversation, the diff, or the file in question.

Give, in this order — **context**: what raised the question and why it cannot be settled without
them, restating the facts needed to answer even if established earlier; **options**: the real
alternatives and what each means in practice; **implications**: what each costs or forecloses, and
which are reversible; **recommendation**: one option, picked, with the reason. Never present a menu
without a pick.

Define any term not in `GLOSSARY.md`, expand acronyms, and never cite a file, tool, or symbol name
as if its meaning were self-evident. Ask the fewest questions that unblock the work, at the point
the answer is needed.

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
