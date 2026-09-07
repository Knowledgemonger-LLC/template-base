---
name: change-protocol
description: How to tell a decision from its implementation, and which one needs approval before you edit. Use before changing AGENTS.md, GLOSSARY.md, an interface contract, a schema, an infrastructure design, or a requirements document; when a change would set a precedent rather than follow one; or when deciding whether to stop mid-implementation and come back for input.
---

# Change protocol

These are standing instructions. They apply for the rest of the task, not just the current step.

A file either **defines** a decision others depend on, or **implements** one already recorded.
Defining files: `GLOSSARY.md` (what terms mean), `AGENTS.md` (the working agreement), and any
interface contract, schema, infrastructure design, or requirements document. Everything else
implements — source, tests, migrations, build config, `README.md`, changelogs.

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

## The two steps

`/design` runs the **defines** step: work the decision out, present options, recommend one, and
stop without editing. `/implement` runs the **implements** step: treat an approved decision as
fixed input and carry it out. Both reference this protocol rather than restating it.
