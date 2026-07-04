<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: baseline.yaml. Regenerate with: python scripts/gen_baseline_md.py -->

# BASELINE

Every element that should exist in every **Knowledgemonger-LLC** repo by default, and the mechanism
by which it gets there. Generated from [`baseline.yaml`](baseline.yaml) — do not hand-edit.

| Tier | Elements | Mechanism(s) |
|------|----------|--------------|
| 1 | 4 | copy |
| 2 | 6 | copy, inherit |
| 3 | 4 | copy |
| 4 | 7 | copy, extend |

## Tier 1 — Truly universal files

| Path | Mechanism | Source of truth | Required | Applies to | Notes |
|------|-----------|-----------------|----------|------------|-------|
| `.editorconfig` | copy | `template/.editorconfig` | yes | all | Universal editor settings. Full-file drift enforcement: target copy must match the rendered template exactly. |
| `.gitattributes` | copy | `template/.gitattributes` | yes | all | Line-ending and diff/merge attributes. Full-file drift enforcement. |
| `.gitignore` | copy | `template/.gitignore.jinja` | yes | all | Canonical base ignores. Full-file enforcement on the base content. Stack-specific ignores should be minimal and are expected to live in tool configs or below the base (see open question on gitignore appends). |
| `LICENSE` | copy | `template/LICENSE.jinja` | yes | all | Per-repo CHOICE, not a synced universal — the body is selected at creation (proprietary [default] \| MIT \| Apache-2.0) with {{ license_holder }} / {{ license_year }} templated. drift=generate-once: scaffolded once, NOT full-file enforced — a different license is a legitimate choice (proprietary product vs. deliberately open-sourced), not drift. check_drift only verifies presence and that holder/year are stamped. Default proprietary so open-sourcing is an explicit opt-in. |

## Tier 2 — Governance / community-health

| Path | Mechanism | Source of truth | Required | Applies to | Notes |
|------|-----------|-----------------|----------|------------|-------|
| _(no local file)_ | inherit | `Knowledgemonger-LLC/.github:CONTRIBUTING.md` | yes | all | No action in target repo — inherited from Knowledgemonger-LLC/.github. DECISION (final): that repo is PUBLIC. Inheritance keys on ACCOUNT OWNERSHIP, not consumer visibility, so PRIVATE product repos DO inherit; only the source .github visibility matters. (This file-type could also inherit from an INTERNAL .github, but PUBLIC is chosen — see the Tier-2 escape-hatch note.) Docs-verified. |
| _(no local file)_ | inherit | `Knowledgemonger-LLC/.github:SECURITY.md` | yes | all | No action in target repo — inherited from Knowledgemonger-LLC/.github. DECISION (final): that repo is PUBLIC. Inheritance keys on ACCOUNT OWNERSHIP, not consumer visibility, so PRIVATE product repos DO inherit; only the source .github visibility matters. (This file-type could also inherit from an INTERNAL .github, but PUBLIC is chosen — see the Tier-2 escape-hatch note.) Docs-verified. |
| _(no local file)_ | inherit | `Knowledgemonger-LLC/.github:CODE_OF_CONDUCT.md` | yes | all | No action in target repo — inherited from Knowledgemonger-LLC/.github. DECISION (final): that repo is PUBLIC. Inheritance keys on ACCOUNT OWNERSHIP, not consumer visibility, so PRIVATE product repos DO inherit; only the source .github visibility matters. (This file-type could also inherit from an INTERNAL .github, but PUBLIC is chosen — see the Tier-2 escape-hatch note.) Docs-verified. |
| `.github/CODEOWNERS` | copy | `template/.github/CODEOWNERS.jinja` | yes | all | FINAL DECISION: COPIED (not inherited) because GitHub does NOT auto-inherit CODEOWNERS from org/.github the way it does community-health files. Marker-block drift (baseline:start / baseline:end, using # comments valid in CODEOWNERS) with default `* {{ default_owner }}`; repo-specific path rules are appended OUTSIDE the block. The maintainers team must exist with WRITE access; keep code-owner-required review OFF while the repo is solo. |
| _(no local file)_ | inherit | `Knowledgemonger-LLC/.github:.github/ISSUE_TEMPLATE/` | yes | all | No action in target repo — issue templates inherited from Knowledgemonger-LLC/.github. DECISION (final): that repo is PUBLIC — REQUIRED here, since ISSUE_TEMPLATE and PULL_REQUEST_TEMPLATE inherit ONLY from a public .github (internal is insufficient). Inheritance keys on ACCOUNT OWNERSHIP (private repos DO inherit). ALL-OR-NOTHING: any local .github/ISSUE_TEMPLATE file makes the repo use NONE of the org defaults for that folder — the planned open-source repo will deliberately OVERRIDE with its own tailored templates. Docs-verified. |
| _(no local file)_ | inherit | `Knowledgemonger-LLC/.github:.github/PULL_REQUEST_TEMPLATE.md` | yes | all | No action in target repo — PR template inherited from Knowledgemonger-LLC/.github. DECISION (final): that repo is PUBLIC — REQUIRED, since PULL_REQUEST_TEMPLATE inherits ONLY from a public .github (internal insufficient). Inheritance keys on ACCOUNT OWNERSHIP (private repos DO inherit). Docs-verified. |

## Tier 3 — Agentic context files

| Path | Mechanism | Source of truth | Required | Applies to | Notes |
|------|-----------|-----------------|----------|------------|-------|
| `AGENTS.md` | copy | `template/AGENTS.md.jinja` | yes | all | Canonical, cross-tool agent context. Marker-block sync: baseline content lives between <!-- baseline:start --> and <!-- baseline:end -->; repo-specific content is allowed outside the block and is preserved. |
| `CLAUDE.md` | copy | `template/CLAUDE.md.jinja` | yes | all | Thin Claude-specific pointer to AGENTS.md. Marker-block sync (<!-- baseline:start --> / <!-- baseline:end -->). |
| `.claude/settings.json` | copy | `template/.claude/settings.json.jinja` | yes | all | Permission model. JSON — NO markers. Managed-keys-subset rule: baseline keys (permissions.deny, defaultMode) must be present and equal; the repo may add extra allow/ask entries. |
| `.claude/commands/` | copy | `template/.claude/commands/` | no | all | Shared slash commands. Baseline commands are synced; repos may add local commands alongside them. |

## Tier 4 — Universal in kind, specific in form

| Path | Mechanism | Source of truth | Required | Applies to | Notes |
|------|-----------|-----------------|----------|------------|-------|
| `.github/workflows/ci.yml` | extend | `Knowledgemonger-LLC/template-base/.github/workflows/reusable-node-ci.yml@v1` | no | node | NODE-ONLY, not universal. CI is language-specific: Node/npm CI does not apply to Python or Terraform repos (no package.json, no `<pm> run` scripts). template-base itself ships NO language CI — this thin caller is provided by a NODE archetype (template-node / template-next-sanity), not by the base, so Copier does NOT emit it for base/non-Node repos. When present it MUST pin to @v1 or a commit SHA, never @main. As an `extend` element it is never drift-managed. INTERIM: the reusable-node-ci.yml it calls is hosted in template-base for now and RELOCATES to the Node archetype template later (physical move is a follow-up). |
| `.github/workflows/release.yml` | extend | `Knowledgemonger-LLC/template-base/.github/workflows/reusable-release.yml@v1` | no | publishing | Thin caller for the shared release/publish reusable workflow. Pin to @v1 or a SHA. OPT-IN — NOT universal: gated by the Copier question `include_release_workflow` (default false). It fires on `v*` tags and would fail / mis-publish in non-publishing repos, so Copier ships it ONLY when enabled (conditional filename skips it otherwise). As an `extend` element it is never drift-managed, so check_drift does NOT flag it missing in repos that opted out. |
| `eslint.config.js` | extend | `pkg:eslint-config` | no | javascript, typescript | Thin local config extending the published, independently-versioned shared package. Package lives in its own repo (NOT hosted here). npm SCOPE intentionally unset — pinned at first publish. |
| `.prettierrc.json` | extend | `pkg:prettier-config` | no | javascript, typescript | Thin pointer to the shared Prettier config package (external). npm SCOPE intentionally unset — pinned at first publish. |
| `tsconfig.json` | extend | `pkg:tsconfig` | no | typescript | Extends the shared tsconfig base (e.g. <scope>/tsconfig/base). External package. npm SCOPE intentionally unset — pinned at first publish. |
| `renovate.json` | copy | `template/renovate.json.jinja` | yes | all | COPIED thin pointer. Marker-block-style drift, but JSON can't hold # markers, so it is enforced as managed-keys (like settings.json): MANAGED = `$schema` and `extends` must contain github>Knowledgemonger-LLC/renovate-config; repo-owned keys (packageRules, schedule, …) are FREE alongside it. Full-file would forbid legitimate per-repo Renovate customization. Rules themselves live in the external preset, NOT inlined here. DEFERRED EXTERNAL PREREQUISITE: Renovate errors on target repos until Knowledgemonger-LLC/renovate-config exists with a base preset — same "reference is right, target must be created" class as the v1 tag. Preferred over Dependabot. |
| `.pre-commit-config.yaml` | copy | `template/.pre-commit-config.yaml.jinja` | no | all | COPIED with marker-block drift: the managed region (trailing-whitespace, end-of-file-fixer, check-yaml, check-json, detect-secrets) is synced; stack-specific hooks are appended OUTSIDE the region. Uses # comment markers (valid YAML). |
