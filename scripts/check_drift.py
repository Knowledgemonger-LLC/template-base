#!/usr/bin/env python3
"""Report drift between a target repo and the baseline (REPORTING/CI gate only).

STUB — full implementation lands in a later phase. This tool NEVER merges; it only flags
divergence. Propagation/merge is `copier update`'s job (3-way merge via .copier-answers.yml).
Keep the two lanes separate.

Per-element drift rules (from baseline.yaml + the approved decisions):
  * Tier 1 (copy):   full-file equality against the rendered template.
  * Tier 3 markdown: marker-block equality between <!-- baseline:start --> / <!-- baseline:end -->;
                     content outside the block is ignored.
  * Tier 3 settings: .claude/settings.json managed-keys subset — baseline keys
                     (permissions.deny, defaultMode) must be present and equal; extra
                     allow/ask entries are permitted.
  * Tier 2 (inherit) / Tier 4 (extend): not drift-managed (presence checks only, if any).

Usage (intended):
  python scripts/check_drift.py <target-repo-path>
"""

import sys


def main() -> int:
    print("check_drift.py: not implemented yet (skeleton phase).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
