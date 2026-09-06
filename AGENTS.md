# AGENTS.md — for working on the base copier

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