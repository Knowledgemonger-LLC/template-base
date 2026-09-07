---
description: Run once in a fresh copy of template-base to re-point it at its own identity.
disable-model-invocation: true
---

This repo was copied from `template-base` and still describes template-base in places. Re-point
it at what it actually is. Run this once, near the start of the repo's life.

Work it out from the repo itself rather than asking me for things you can determine. Read what
code exists, the package manifest if there is one, the CI config, and the directory layout. Ask
only for what genuinely cannot be inferred — and if the repo is empty, ask what it is going to be
before writing anything.

Re-point these:

1. **`AGENTS.md`** — the title, the **Stack** section (languages, frameworks, runtimes, key
   services), and the **Build / Test / Run** commands. Use the real commands, verified against
   the manifest or scripts; do not invent them. Delete the **Working on template-base** section
   entirely — it describes template-base, not this repo.
2. **`CLAUDE.md`** and **`GLOSSARY.md`** — the titles.
3. **`README.md`** — replace it. template-base's README describes template-base; this repo needs
   its own, describing what it is and how to run it.
4. **`LICENSE`** — confirm the holder and year, and swap the body if this repo is not
   proprietary.
5. **`.claude/settings.json`** — add the package manager to `permissions.allow` in the form
   `Bash(<pm> install:*)` (npm, pnpm, uv, pip, …), matching what this repo actually uses. Leave
   `deny`, `ask`, and `defaultMode` alone.
6. **`CHANGELOG.md`** — clear template-base's entries and start the file over with one line
   recording that this repo was created from template-base, with today's date.

Then report what you changed and anything you could not determine. Offer to delete this command
file — it has done its job and does not apply again. If I accept, also drop its line from the
**Commands** list in `CLAUDE.md`, so that list does not point at a command the repo no longer has.
