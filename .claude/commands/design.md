---
description: Work out a decision and write it up for approval — the "defines" step of the Change protocol.
model: opus
---

Run the **defines** step of the Change protocol in `AGENTS.md`. Read that protocol first — this
command adds procedure, it does not restate or replace it.

1. Read `GLOSSARY.md` and any product or requirements docs bearing on the question. Say
   which you read.
2. State the decision to be made in one sentence, and what depends on it.
3. Produce **two or three competing options**, not one. For each: what it commits us to, what it
   forecloses, and whether it is reversible. A single confident answer is the failure mode here.
4. Recommend one, with the reason.
5. Flag every gap you hit — a term with no `GLOSSARY.md` entry, an entity the product docs
   imply but nothing defines, a question the inputs cannot settle. These are the output, not noise:
   a gap found here is a decision that would otherwise have been made silently during
   implementation.

Do not edit source, tests, or config, and do not implement the recommendation. Write the decision
up, present it, and stop. Record it in the owning document only after I approve it.

Follow the **Asking for human input** rules in `AGENTS.md` for the write-up.
