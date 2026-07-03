# template-base

Single source of truth for everything that should exist in **every** repo at the org by
default — defined once, propagated by tooling, never hand-copied or allowed to drift.

> **Status:** authored and smoke-tested end-to-end (`copier copy` verified; `gen_baseline_md.py
> --check` and `check_drift.py --selftest` green). Not yet released — the `v1` tag and the two
> external repos in [Prerequisites](#prerequisites-external-repos-that-must-exist) are still
> pending. Start with [`baseline.yaml`](baseline.yaml) (machine-readable source of truth) and
> [`BASELINE.md`](BASELINE.md) (generated human index).

## How this fits together (three artifacts, don't confuse them)

Three separate things deliver the baseline. They cooperate; none replaces another.

| Artifact | What it is | When it runs | How it delivers | Owns |
|---|---|---|---|---|
| **template-base** (this repo) | a Copier template | once, at repo creation (+ `copier update`), on your machine | **writes files into** the new repo | Tiers 1, 3, 4 (+ CODEOWNERS) |
| **Knowledgemonger-LLC/.github** | a GitHub org-defaults *repository* (public) | continuously, at view-time, on GitHub's servers | **displays** fallback files; copies nothing | Tier 2 |
| **archetype templates** (future, e.g. `template-api`, `template-web`, `template-sagemaker`) | Copier templates that **compose** template-base | once, at creation | write archetype-specific files **on top of** the baseline | archetype layer |

A generated repo therefore gets: universal files *written in* by template-base, governance docs
*inherited* (displayed) from the `.github` repo, and — if created from an archetype template —
its specialized scaffold layered on. `.github` does **not** replace template-base; it delivers the
one tier (2) that template-base deliberately doesn't copy.

> **Two different `.github`s:** the org **repository** `Knowledgemonger-LLC/.github` (Tier-2
> inheritance source, public) is NOT the `.github/` **folder** inside this repo (which holds this
> repo's own CI workflows). Owner-slot = repo; deeper path = folder.

### Composition: archetypes layer on top of the base

Archetype templates do **not** fork or copy the base — they **compose** it via Copier template
composition: scaffolding applies **template-base first**, then the archetype layers its own
specialized files on top. The generated repo's `.copier-answers.yml` records **both** sources, so
it can `copier update` from each **independently** — the universal layer keeps flowing from
template-base, the archetype layer from its own template. The layers are **additive, not mutually
exclusive**.

Consequence: **never duplicate base files into an archetype template.** An archetype ships only
what is unique to it; everything universal stays in template-base and arrives by composition.

> **Current state:** template-base is the *only* template today; archetypes are the documented next
> layer, not yet built. An `archetype` answer (`base` | `api` | `web` | `sagemaker`) is recorded in
> `.copier-answers.yml` to capture intent, but ships no archetype-specific files yet. A small
> archetype-specific need can live inside template-base until it accumulates enough unique files to
> **graduate** into its own `template-<name>` repo — moving a concern out of the base is a deliberate
> step, not the default.

### Naming convention: `template-<role>`

- **`template-base`** — the universal foundation (this repo); `-base` marks the foundation.
- **`template-<archetype>`** — specializations that compose the base: `template-api`,
  `template-web`, `template-sagemaker`, …

The shared `template-` prefix groups the whole scaffolding family together in the org repo listing.

## Usage

### Create a new repo from this template
    copier copy git@github.com:Knowledgemonger-LLC/template-base.git <new-repo-dir>
Copier prompts for the answers defined in `copier.yml` (org, project name, license, stack,
package manager, the build/test/run/lint commands). Pin to the released major:
    copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-base.git <new-repo-dir>

Then create the repo on GitHub and push:
    cd <new-repo-dir>
    git init -b main && git add -A && git commit -m "Initial from template-base"
    git remote add origin git@github.com:Knowledgemonger-LLC/<new-repo>.git
    git push -u origin main

### Update an existing repo when template-base changes
Run inside a repo previously generated from the template (reads its .copier-answers.yml):
    copier update
This 3-way-merges baseline changes in while preserving local edits. Consumers pinned to @v1
also pick up reusable-workflow fixes automatically via the moving major tag.

> For scripted/non-interactive generation, pass answers with --data, e.g.
> `--data org=Knowledgemonger-LLC --data license=proprietary …` — but interactive is the norm.

## Prerequisites (external repos that must exist)

Generated repos depend on three "reference is correct, target must be created" items. Until each
exists, the corresponding feature silently no-ops or errors:

1. **`v1` tag on this repo** — callers pin `@v1`; see Releasing below. (Internal; you cut it.)
2. **Public `Knowledgemonger-LLC/.github`** — Tier-2 inheritance source. Must be **public** (private
   unsupported; issue/PR templates require public specifically). Without it, all Tier-2 inheritance
   no-ops. Holds all five Tier-2 file types — but NOT CODEOWNERS (see below).
3. **Public `Knowledgemonger-LLC/renovate-config`** — the preset the thin `renovate.json` extends.
   Without it, Renovate errors in every generated repo.

## The four-tier model

| Tier | What | Mechanism |
|------|------|-----------|
| 1 | Truly universal files (`.editorconfig`, `.gitattributes`, base `.gitignore`, `LICENSE`) | **copy** — template + drift sync. *Exception:* `LICENSE` is **generate-once** — scaffolded with `license_holder`/`license_year` stamped, but the license body is a per-repo choice (proprietary \| MIT \| Apache-2.0) and is **not** drift-enforced, unlike the other Tier-1 files. |
| 2 | Governance / community-health (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, issue/PR templates) | **inherit** — public org `.github` repo; no local copies |
| 2* | `CODEOWNERS` — governance, but **cannot inherit** (GitHub reads it only from the repo itself) | **copy** — shipped by template-base to `.github/CODEOWNERS` |
| 3 | Agentic context (`AGENTS.md`, thin `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`) | **copy** — thin, reference shared rules |
| 4 | Universal in kind, specific in form (CI/CD, lint/format, tsconfig, Renovate, pre-commit) | **extend** — shared packages + reusable workflows referenced in a few lines. **Renovate:** a thin **copy** pointer that *extends* the external `renovate-config` preset (managed-keys drift) — hence the prerequisite repo below. **pre-commit:** a **copied base** of universal hooks in a marker block, with **no** external preset — it is therefore **not** a prerequisite repo (nothing external to stand up). |

## How drift is killed

- **Propagation / merge:** `copier update` re-applies this template to existing repos via a
  3-way merge driven by `.copier-answers.yml` (shipped into target repos, never gitignored).
- **Reporting / CI gate:** `scripts/check_drift.py` flags divergence without merging. Two
  separate lanes — do not conflate them.

## Releasing (reusable-workflow versioning)

Consumers pin callers to a **major** tag (`...@v1`). We cut an immutable patch tag and move
the major tag to it:

1. Land the change on `main` (the commit must contain `.github/workflows/reusable-*.yml`).
2. Tag the immutable release: `git tag v1.0.0 && git push origin v1.0.0`.
3. The [`major-tag`](.github/workflows/major-tag.yml) workflow fires on the 3-part tag and
   force-moves `v1` to that commit. (First release only: create `v1` once —
   `git tag v1 v1.0.0 && git push origin v1` — subsequent v1.x re-points are automatic.)
4. Every later fix repeats step 2 with `v1.1.0`, `v1.2.0`, … and `v1` follows along.

Never let callers pin `@main`. Cut `v2.0.0` (and a new `v2`) only for breaking changes to the
reusable workflows.

See [`AGENTS.md`](AGENTS.md) for contributor/agent instructions.
