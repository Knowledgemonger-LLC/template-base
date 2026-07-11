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

## Create a new archetype template from template-base (`template-<functional-domain>`)

When a set of files is unique to one functional domain (api, web, sagemaker, …) and has grown
past what belongs inside the base, graduate it into its own `template-<domain>` repo that
**composes** template-base rather than forking it. The archetype ships **only** the files unique
to that domain; everything universal keeps flowing from template-base by composition (see
[Composition](#composition-archetypes-layer-on-top-of-the-base)).

The walkthrough below creates `template-api` as a running example; substitute your own domain for
`api` throughout. It assumes you have this repo checked out (e.g. at `~/Repos/template-base`) and
run the commands from its parent dir (`~/Repos`).

1. **Create the archetype repo, then scaffold its authoring layer.** First generate it *from*
   template-base so it carries its own baseline (`.editorconfig`, `LICENSE`, `AGENTS.md`,
   `.claude/`, …) — Copier prompts you; answer for the archetype repo itself (`project_name`
   `template-api`, `archetype` `api`, and so on):

        copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-base.git template-api

   Then run the scaffolder (it lives in this repo, not the new one) to lay the authoring layer on
   top — it writes `copier.yml` (renamed answers file + hidden `archetype`/`language` intent),
   creates `template/`, and seeds a pinned `@v1` CI caller for Node archetypes:

        python template-base/scripts/new_archetype.py api ./template-api --language node

   The script refuses to run on a dir not bootstrapped from template-base and won't overwrite
   existing files without `--force`.
2. **Ship only what is unique to the domain — by editing, no `copier`.** Open `template-api/` in
   your editor. Do **not** copy any Tier 1–4 file template-base already delivers — duplicating a
   base file into an archetype is the one thing composition exists to prevent. Put domain-specific
   CI (e.g. the Node reusable-CI caller), configs, and scaffolding under `template-api/template/`.
3. **Author the domain layer.** The generated `copier.yml` already pins `_subdirectory: template`
   and a distinct `_answers_file: .copier-answers-api.yml` (so this layer `copier update`s
   independently of the base and never clobbers `.copier-answers.yml`), and records the
   `archetype`/`language` intent. What's left is yours: fill in the api-specific questions in
   `copier.yml` and rewrite `README.md`/`AGENTS.md` to describe the api layer. Leave the universal
   questions (`org`, `license`, `runtime_version`, the build/test/run/lint commands, …) to
   template-base — the base pass answers them; don't re-ask them here.
4. **Publish and version it — with `git`/`gh`, no `copier`.** Copier only wrote files; you still
   init the repo, push it, and cut the tags consumers pin to:

        cd template-api
        git init -b main && git add -A && git commit -m "Initial template-api from template-base"
        gh repo create Knowledgemonger-LLC/template-api --public --source=. --remote=origin --push
        git tag v1.0.0 && git push origin v1.0.0    # immutable release
        git tag v1 v1.0.0 && git push origin v1      # moving major (first release only; see Releasing)

   Consumers then compose `template-base@v1` + `template-api@v1`.

### Repeatable setup checklist

`scripts/new_archetype.py` handles the mechanical rows; the editorial rows are judgment work it
deliberately leaves to you (a blind rename of the base's docs would be wrong — an archetype's
README describes a *different, smaller* thing than the base's).

| Step | Automated by the script? |
|---|---|
| `copier.yml` with `_answers_file: .copier-answers-<domain>.yml` | ✅ |
| Hidden `archetype`/`language` intent recorded for generated repos | ✅ |
| `template/` created; Node archetypes get a pinned `@v1` CI caller | ✅ |
| Rewrite `README.md` / `AGENTS.md` for the archetype layer | ❌ editorial |
| Author the domain-specific `copier.yml` questions and `template/` files | ❌ editorial |
| Verify `template/` duplicates no base-owned file (anti-duplication rule) | ❌ review |
| Commit and cut a `v1` tag so callers can pin `template-<domain>@v1` | ❌ release |

## Create a new repo from template-base

The common case: scaffold an actual product repo from the baseline. Two variants — a plain baseline
repo, or a repo that also composes an archetype.

### Plain baseline repo (template-base only)

    copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-base.git <new-repo-dir>

Copier prompts for the answers in `copier.yml` (org, project name, license, stack, package
manager, runtime version, the build/test/run/lint commands). Omit `--vcs-ref=v1` to track `main`
(not recommended once `v1` exists). Then create the repo on GitHub and push:

    cd <new-repo-dir>
    git init -b main && git add -A && git commit -m "Initial from template-base"
    git remote add origin git@github.com:Knowledgemonger-LLC/<new-repo>.git
    git push -u origin main

### Repo composed from an archetype (base + archetype)
To also get an archetype's specialized scaffold (e.g. `template-api`), apply template-base first,
then layer the archetype on top of the **same** directory. Each pass writes its own answers file,
so the repo can later `copier update` from each source independently:

    copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-base.git      <new-repo-dir>
    copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-<domain>.git   <new-repo-dir>

Then `git init`/push as above. (Those archetypes are built via
[Create a new archetype template](#create-a-new-archetype-template-from-template-base-template-functional-domain).)

### Update an existing repo when template-base changes
Run inside a repo previously generated from the template (reads its `.copier-answers.yml`):

    copier update

This 3-way-merges baseline changes in while preserving local edits. A composed repo has one
answers file per layer, so `copier update` re-merges each independently — the universal layer from
template-base, the domain layer from `template-<domain>`. Consumers pinned to `@v1` also pick up
reusable-workflow fixes automatically via the moving major tag.

> For scripted/non-interactive generation, pass answers with `--data`, e.g.
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


## Repo visibility policy
- template-base, renovate-config, .github → PUBLIC. Required for the machinery:
  reusable-workflow calls, Renovate github> preset resolution, and community-health
  inheritance all need (or are simplest with) public hosts. These repos hold only
  scaffolding/governance boilerplate — no product IP or secrets.
- Product repos → PRIVATE by default. They consume the public baseline; nothing about
  being private blocks that (public reusable workflows are callable from private repos).
- If template-base ever must go private, enable Settings → Actions → General → Access →
  "org-accessible" so private repos can still call its reusable workflows.

## The four-tier model

| Tier | What | Mechanism |
|------|------|-----------|
| 1 | Truly universal files (`.editorconfig`, `.gitattributes`, base `.gitignore`, `LICENSE`) | **copy** — template + drift sync. *Exception:* `LICENSE` is **generate-once** — scaffolded with `license_holder`/`license_year` stamped, but the license body is a per-repo choice (proprietary \| MIT \| Apache-2.0) and is **not** drift-enforced, unlike the other Tier-1 files. |
| 2 | Governance / community-health (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, issue/PR templates) | **inherit** — public org `.github` repo; no local copies |
| 2* | `CODEOWNERS` — governance, but **cannot inherit** (GitHub reads it only from the repo itself) | **copy** — shipped by template-base to `.github/CODEOWNERS` |
| 3 | Agentic context (`AGENTS.md`, thin `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`) | **copy** — thin, reference shared rules |
| 4 | Universal in kind, specific in form (lint/format, tsconfig, Renovate, pre-commit) | **extend** — shared packages + reusable workflows referenced in a few lines. **CI:** the abstract *slots* are universal (every repo has a `pkg_manager`, a `runtime_version`, and build/test/lint/run commands — these stay as Copier questions), but the **CI workflow itself is language-specific and NOT shipped by the base** — Node/npm CI does not apply to Python or Terraform repos. CI is a **language-archetype** concern; see the `reusable-node-ci.yml` note below. **Renovate:** a thin **copy** pointer that *extends* the external `renovate-config` preset (managed-keys drift) — hence the prerequisite repo below. **pre-commit:** a **copied base** of universal hooks in a marker block, with **no** external preset — it is therefore **not** a prerequisite repo (nothing external to stand up). |

> **Note — `reusable-node-ci.yml` is Node-family, hosted here INTERIM.** template-base ships no
> language CI to generated repos. The Node reusable CI workflow
> (`.github/workflows/reusable-node-ci.yml`) and its example caller (`examples/caller-ci.yml`)
> are **Node-only** and belong to a Node archetype (`template-node` / `template-next-sanity`).
> They live in template-base for now; the physical relocation to that archetype is a planned
> follow-up. Non-Node repos (Python/ML/SageMaker/Glue/dbt, Terraform) do not receive or call it.

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
