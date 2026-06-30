# repo-baseline

Single source of truth for everything that should exist in **every** repo at the org by
default — defined once, propagated by tooling, never hand-copied or allowed to drift.

> **Status:** skeleton (Phase 1). Template file contents and tooling are authored in later
> phases. Start with [`baseline.yaml`](baseline.yaml) (machine-readable source of truth) and
> [`BASELINE.md`](BASELINE.md) (generated human index).

## The four-tier model

| Tier | What | Mechanism |
|------|------|-----------|
| 1 | Truly universal files (`.editorconfig`, `.gitattributes`, base `.gitignore`, `LICENSE`) | **copy** — template + drift sync |
| 2 | Governance / community-health (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, `CODEOWNERS`, issue/PR templates) | **inherit** — org `.github` repo; no local copies |
| 3 | Agentic context (`AGENTS.md`, thin `CLAUDE.md`, `.claude/settings.json`, `.claude/commands/`) | **copy** — thin, reference shared rules |
| 4 | Universal in kind, specific in form (CI/CD, lint/format, tsconfig, Renovate, pre-commit) | **extend** — shared packages + reusable workflows referenced in a few lines |

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
