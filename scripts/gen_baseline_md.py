#!/usr/bin/env python3
"""Generate BASELINE.md (human index) from baseline.yaml (the source of truth).

Never hand-edit BASELINE.md — edit baseline.yaml and regenerate.

  python scripts/gen_baseline_md.py          # write BASELINE.md
  python scripts/gen_baseline_md.py --check   # CI: exit 1 if BASELINE.md is stale
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "baseline.yaml"
SCHEMA = ROOT / "scripts" / "baseline.schema.json"
OUT = ROOT / "BASELINE.md"

TIER_TITLES = {
    1: "Tier 1 — Truly universal files",
    2: "Tier 2 — Governance / community-health",
    3: "Tier 3 — Agentic context files",
    4: "Tier 4 — Universal in kind, specific in form",
}


def load():
    import yaml

    data = yaml.safe_load(MANIFEST.read_text())
    try:
        import jsonschema

        jsonschema.validate(data, json.loads(SCHEMA.read_text()))
    except ImportError:
        print("warn: jsonschema not installed — skipped schema validation", file=sys.stderr)
    return data


def cell(value) -> str:
    """Make a value safe for a Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render(data) -> str:
    org = data["org"]
    lines = [
        "<!-- GENERATED FILE — DO NOT EDIT BY HAND.",
        "     Source of truth: baseline.yaml. Regenerate with: python scripts/gen_baseline_md.py -->",
        "",
        "# BASELINE",
        "",
        f"Every element that should exist in every **{org}** repo by default, and the mechanism",
        "by which it gets there. Generated from [`baseline.yaml`](baseline.yaml) — do not hand-edit.",
        "",
    ]

    counts = Counter(e["tier"] for e in data["elements"])
    lines += ["| Tier | Elements | Mechanism(s) |", "|------|----------|--------------|"]
    for tier in (1, 2, 3, 4):
        if counts.get(tier):
            mechs = sorted({e["mechanism"] for e in data["elements"] if e["tier"] == tier})
            lines.append(f"| {tier} | {counts[tier]} | {', '.join(mechs)} |")
    lines.append("")

    for tier in (1, 2, 3, 4):
        els = [e for e in data["elements"] if e["tier"] == tier]
        if not els:
            continue
        lines += [
            f"## {TIER_TITLES[tier]}",
            "",
            "| Path | Mechanism | Source of truth | Required | Applies to | Notes |",
            "|------|-----------|-----------------|----------|------------|-------|",
        ]
        for e in els:
            path = e["path"]
            path_cell = "_(no local file)_" if path is None else f"`{path}`"
            applies = e["applies_to"]
            applies = applies if isinstance(applies, str) else ", ".join(applies)
            required = "yes" if e["required"] else "no"
            lines.append(
                f"| {path_cell} | {cell(e['mechanism'])} | `{cell(e['source_of_truth'])}` "
                f"| {required} | {cell(applies)} | {cell(e.get('notes', ''))} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="Exit 1 if BASELINE.md is stale.")
    args = ap.parse_args(argv)

    data = load()
    out = render(data)

    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        if current != out:
            print("BASELINE.md is STALE — run: python scripts/gen_baseline_md.py", file=sys.stderr)
            return 1
        print("BASELINE.md is up to date.")
        return 0

    OUT.write_text(out)
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(data['elements'])} elements).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
