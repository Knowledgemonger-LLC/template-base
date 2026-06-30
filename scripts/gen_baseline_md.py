#!/usr/bin/env python3
"""Generate BASELINE.md (human index) from baseline.yaml (source of truth).

STUB — full implementation lands in the next phase. The contract:
  * Read baseline.yaml, validate it against baseline.schema.json.
  * Render a grouped-by-tier table to BASELINE.md.
  * Tier 2 rows (path: null) render as "No action in target repo — inherited from <org>/.github".
  * NEVER hand-edit BASELINE.md; always regenerate via this script.

Usage (intended):
  python scripts/gen_baseline_md.py          # write BASELINE.md
  python scripts/gen_baseline_md.py --check  # CI: fail if BASELINE.md is stale
"""

import sys


def main() -> int:
    print("gen_baseline_md.py: not implemented yet (skeleton phase).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
