#!/usr/bin/env python3
"""Report drift between a target repo and the repo-baseline template.

REPORTING / CI GATE ONLY — this tool never merges. Propagation and merge are
`copier update`'s job (3-way merge via .copier-answers.yml). Keep the two lanes separate.

Three drift rules, derived from baseline.yaml:
  * full-file    (Tier 1): the rendered template must equal the target file exactly.
  * marker-block (AGENTS.md, CLAUDE.md, .github/CODEOWNERS): only the region between the
                 `baseline:start` / `baseline:end` markers must match the baseline; content
                 outside the block is the repo's own. Works for both <!-- --> (markdown) and
                 # (CODEOWNERS) comment styles.
  * managed-keys (.claude/settings.json): permissions.deny and permissions.defaultMode must
                 be present and equal; allow/ask are free for the repo to extend.

Usage:
  python scripts/check_drift.py <target-repo-path>

Exit code: 0 = no drift, 1 = drift found (or a required file missing), 2 = bad invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MARKER_PATHS = {"AGENTS.md", "CLAUDE.md", ".github/CODEOWNERS"}


def _yaml(path):
    import yaml

    return yaml.safe_load(Path(path).read_text())


def manifest():
    return _yaml(ROOT / "baseline.yaml")


def question_defaults() -> dict:
    """Defaults declared for each Copier question (used to fill any unanswered vars)."""
    cfg = _yaml(ROOT / "copier.yml")
    out = {}
    for key, val in cfg.items():
        if key.startswith("_"):
            continue
        if isinstance(val, dict) and "type" in val and "default" in val:
            out[key] = val["default"]
    return out


def context_for(target: Path) -> dict:
    """Render context = Copier defaults overlaid with the target's recorded answers."""
    ctx = question_defaults()
    answers = target / ".copier-answers.yml"
    if answers.exists():
        for key, val in (_yaml(answers) or {}).items():
            if not key.startswith("_"):
                ctx[key] = val
    return ctx


def render_source(source_of_truth: str, ctx: dict) -> str:
    text = (ROOT / source_of_truth).read_text()
    if source_of_truth.endswith(".jinja"):
        from jinja2 import Environment, StrictUndefined

        env = Environment(undefined=StrictUndefined, keep_trailing_newline=True)
        text = env.from_string(text).render(**ctx)
    return text


def marker_block(text: str):
    """Return the inclusive baseline:start..baseline:end region, or None if absent."""
    lines = text.splitlines()
    start = end = None
    for i, line in enumerate(lines):
        if "baseline:start" in line and start is None:
            start = i
        elif "baseline:end" in line:
            end = i
    if start is None or end is None or end < start:
        return None
    return "\n".join(lines[start : end + 1])


def rule_for(element: dict):
    if element["mechanism"] != "copy":
        return None
    path = element["path"]
    if not path or path.endswith("/"):
        return None
    if path in MARKER_PATHS:
        return "marker-block"
    if path == ".claude/settings.json":
        return "managed-keys"
    return "full-file"


def check_managed_keys(template_text: str, target_text: str) -> list[str]:
    try:
        tmpl = json.loads(template_text).get("permissions", {})
        tgt = json.loads(target_text).get("permissions", {})
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    issues = []
    if tgt.get("defaultMode") != tmpl.get("defaultMode"):
        issues.append(
            f"defaultMode must equal {tmpl.get('defaultMode')!r} (found {tgt.get('defaultMode')!r})"
        )
    if sorted(tgt.get("deny", [])) != sorted(tmpl.get("deny", [])):
        issues.append(
            f"deny must equal baseline set {sorted(tmpl.get('deny', []))} "
            f"(found {sorted(tgt.get('deny', []))})"
        )
    return issues


def check(target: Path):
    data = manifest()
    ctx = context_for(target)
    findings = []
    evaluated = 0

    for element in data["elements"]:
        rule = rule_for(element)
        if not rule:
            continue
        evaluated += 1
        path = element["path"]
        target_file = target / path

        if not target_file.exists():
            if element.get("required"):
                findings.append((path, rule, "MISSING required file"))
            continue

        template_text = render_source(element["source_of_truth"], ctx)
        target_text = target_file.read_text()

        if rule == "full-file":
            if template_text != target_text:
                findings.append((path, rule, "content differs from rendered template"))
        elif rule == "marker-block":
            tmpl_block = marker_block(template_text)
            tgt_block = marker_block(target_text)
            if tgt_block is None:
                findings.append((path, rule, "baseline marker block missing in target"))
            elif tmpl_block != tgt_block:
                findings.append((path, rule, "managed marker block differs from baseline"))
        elif rule == "managed-keys":
            for msg in check_managed_keys(template_text, target_text):
                findings.append((path, rule, msg))

    return evaluated, findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Report baseline drift for a target repo (no merge).")
    ap.add_argument("target", help="Path to the target repo working tree.")
    args = ap.parse_args(argv)

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"error: not a directory: {target}", file=sys.stderr)
        return 2

    evaluated, findings = check(target)
    print(f"Drift check: {target}")
    print(f"  rules evaluated: {evaluated}")
    if not findings:
        print("  result: OK — no drift")
        return 0
    print(f"  result: DRIFT — {len(findings)} issue(s)")
    for path, rule, msg in findings:
        print(f"    [{rule:12}] {path}: {msg}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
