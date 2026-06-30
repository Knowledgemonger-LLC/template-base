# CLAUDE.md

Read **[AGENTS.md](AGENTS.md)** first — it holds the canonical rules for working on this repo.
This file adds only Claude-specific notes.

## Claude-specific notes

- `BASELINE.md` is generated from `baseline.yaml`. Do not hand-edit it; edit the YAML and run
  `python scripts/gen_baseline_md.py`.
- Only `template/` is copied into target repos. Do not add target-repo files outside `template/`.
- Reusable-workflow callers must pin to `@v1` or a SHA, never `@main`.
- Use `/code-review` on your working diff before committing changes to the manifest or scripts.

## Permissions
Tooling permissions are enforced in `.claude/settings.json`, not here. Posture:
read-only and local-reversible commands (inspection, validation scripts, `git add`/
`commit`, file edits via acceptEdits) run automatically; anything touching the network,
the remote, or releases (`pip install`, `git push`, `git tag`, `gh`, `copier copy`)
prompts; `sudo`/`rm -rf`/`curl` and secret reads (`.env`, `~/.ssh`) are denied.
Edit the allow/ask/deny lists in settings.json to change this.
