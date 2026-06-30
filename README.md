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

See [`AGENTS.md`](AGENTS.md) for contributor/agent instructions.
