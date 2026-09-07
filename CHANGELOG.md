# CHANGELOG

Changes to template-base worth knowing about if you copied it earlier.

Nothing propagates — a repo created from this one never sees these updates automatically. This
file is the manual substitute: read it, decide whether anything is worth porting by hand, and
ignore the rest. Most entries will not be worth porting, and that is fine.

Record an entry only for changes to the working agreement or the shipped files. Changes to this
repo's own documentation about itself do not belong here.

## 2026-09-05

- **Strategy change: nothing propagates any more.** template-base was a Copier template with a
  drift checker, a generated baseline manifest, reusable workflows pinned to a moving `v1` tag,
  and an archetype-composition model. All of it is gone. The repo is now a GitHub template
  repository: copy it once, and the copy is yours. Repos created under the old model — there are
  none — would have kept working; `copier update` simply has nothing to update from.
- **The whole repo is the payload.** The `template/` subdirectory is gone; its contents moved to
  the root. What you see is what a new repo gets.
- **`DOMAIN_MODEL.md` dropped.** The versioned entity definitions with per-entity changelogs were
  more ceremony than they earned. `GLOSSARY.md` stays.
- **`/build` and `/onboard` replaced by `/design` and `/implement`**, one per step of the Change
  protocol. `/bootstrap` added, to re-point a fresh copy at its own identity.
- **`defaultMode` is now `acceptEdits`.** File edits apply without prompting; git is the undo,
  not the edit prompt. The `deny` list carries the weight it used to share — it guards what git
  cannot undo.
- **Dropped from the shipped set:** `renovate.json`, `.github/CODEOWNERS`, and
  `.pre-commit-config.yaml` — to keep the seed small, so that each repo owns only what it
  actually uses. None of the three was dropped because it was broken.
