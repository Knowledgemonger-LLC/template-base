---
description: Implement an already-approved decision — the "implements" step of the Change protocol.
model: sonnet
---

Run the **implements** step of the Change protocol. Read the **`change-protocol`** skill first.

1. Name the approved decision this work follows from and where it is recorded — `GLOSSARY.md`,
   an interface contract, or an approved write-up in this conversation. Do this before editing
   anything.
2. Treat it as fixed input. Do not re-decide it, re-scope it, or improve on it. If it looks wrong,
   stop and say so rather than working around it.
3. Implement it. Edits apply without prompting, so commit at each logical checkpoint — git is the
   undo, not the edit prompt.
4. Run the test and lint commands documented in `AGENTS.md`.
5. Report what changed, what passed, and anything left out and why.

Do not ask permission to continue partway through: approval is per decision, not per edit. Come back
only for a genuine gap in the decision, something you believe is wrong, or an irreversible or
outward-facing step.

If the work turns out to require a decision nobody has made, stop and say so — that is a `/design`
task, not this one.
