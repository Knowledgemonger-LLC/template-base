# AGENTS.md — working ON repo-baseline

This file is for contributors and agents working **on this repo**. It is NOT the template's
`AGENTS.md` (that lives in `template/AGENTS.md` and is copied into target repos).

## What this repo is

`repo-baseline` is the single source of truth for everything that should exist in every repo
at the org by default. It does not modify target repos directly; it **ships a Copier template**
and **hosts reusable workflows**, and **documents** what is inherited from the org `.github`
repo. See `README.md` for the four-tier model.

## Cardinal rules

1. **`baseline.yaml` is the source of truth.** Every universal element is declared there.
2. **Never hand-edit `BASELINE.md`.** It is generated from `baseline.yaml`. Edit the YAML,
   then regenerate the index.
3. **`template/` is the only thing copied into target repos** (Copier `_subdirectory: template`).
   Everything else here — `baseline.yaml`, `scripts/`, `.github/`, `examples/`, this file —
   is meta and never leaves this repo.
4. **Two lanes, kept separate:**
   - `copier update` = propagation/merge (3-way merge via `.copier-answers.yml`).
   - `scripts/check_drift.py` = reporting/CI gate that flags divergence, never merges.
5. **Reusable workflows are pinned.** Callers reference `...@v1` or a SHA, never `@main`.
   Cut a `v1` tag before telling consumers to depend on it.

## Build / test commands

> Tooling is implemented in a later phase; these are the intended entry points.

```bash
# Regenerate the human index from the manifest
python scripts/gen_baseline_md.py

# CI: fail if BASELINE.md is stale relative to baseline.yaml
python scripts/gen_baseline_md.py --check

# Validate baseline.yaml against its JSON Schema
#   (e.g. `check-jsonschema --schemafile scripts/baseline.schema.json baseline.yaml`)

# Report drift of a target repo against the baseline (never merges)
python scripts/check_drift.py <target-repo-path>
```

## Drift rules (authoritative summary)

- **Tier 1 (copy):** full-file equality against the rendered template.
- **Tier 3 markdown (`AGENTS.md`, `CLAUDE.md`):** equality only inside the
  `<!-- baseline:start -->` / `<!-- baseline:end -->` block; content outside is the repo's own.
- **Tier 3 `.claude/settings.json`:** managed-keys subset — baseline keys (`permissions.deny`,
  `defaultMode`) must be present and equal; repos may add extra `allow`/`ask` entries.
- **Tier 2 (inherit) / Tier 4 (extend):** not drift-managed.

## Org parameterization

The org is a Copier variable (`org`, default `Knowledgemonger-LLC`) so all references can be
re-pointed in one place. Shared config packages (eslint/prettier/tsconfig) are external,
independently-versioned packages — referenced via `pkg:@<scope>/...`, not hosted here.
