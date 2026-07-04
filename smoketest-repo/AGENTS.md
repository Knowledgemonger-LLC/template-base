# AGENTS.md — smoketest-repo

<!-- baseline:start -->
<!-- Managed by template-base (Tier 3). The content INSIDE this block is synced across all
     Knowledgemonger-LLC repos via `copier update`; edits here will be overwritten on the next update.
     Put repo-specific content OUTSIDE this block, where it is preserved. -->

**This file is the canonical, cross-tool source of truth for AI agents working in this repo.**
Tool-specific files (e.g. `CLAUDE.md`) reference it; they must not duplicate it.

## Boundaries — do not touch
- Do not edit generated files or dependency lockfiles by hand.
- Do not commit secrets. `.env*` is git-ignored (except `.env.example`).
- Do not weaken the `deny` rules or `defaultMode` in `.claude/settings.json`.
- Do not hand-tune shared lint/format/tsconfig — those are inherited (Tier 4).
- Changes to CODEOWNERS-gated paths require review by @Knowledgemonger-LLC/maintainers.
<!-- baseline:end -->

## Stack
TypeScript / Node 20

## Build / Test / Run
```bash
# Build
pnpm build

# Test
pnpm test

# Run
pnpm dev

# Lint
pnpm lint
```

## Conventions
- Match the existing code style; formatting and lint config are shared — do not override locally.
- Keep changes scoped and atomic. Use Conventional Commits (`feat:`, `fix:`, `chore:` …).
- Prefer the documented commands above over ad-hoc invocations.
<!-- Add repo-specific conventions, architecture notes, and gotchas below. -->
