# CLAUDE.md

Read **[AGENTS.md](AGENTS.md)** first — it holds the canonical rules for working on this repo.
This file adds only Claude-specific notes.

## Claude-specific notes

- `BASELINE.md` is generated from `baseline.yaml`. Do not hand-edit it; edit the YAML and run
  `python scripts/gen_baseline_md.py`.
- Only `template/` is copied into target repos. Do not add target-repo files outside `template/`.
- Reusable-workflow callers must pin to `@v1` or a SHA, never `@main`.
- Use `/code-review` on your working diff before committing changes to the manifest or scripts.
