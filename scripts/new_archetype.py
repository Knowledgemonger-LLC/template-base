#!/usr/bin/env python3
"""Scaffold the authoring layer of a new `template-<domain>` archetype repo.

An archetype template COMPOSES template-base — it ships only the files unique to one
functional domain and inherits everything universal by composition (see README ->
"Create a new archetype template"). First bootstrap the repo FROM template-base so it
carries its own baseline:

  copier copy --vcs-ref=v1 git@github.com:Knowledgemonger-LLC/template-base.git template-<domain>

then run this from a template-base checkout to lay down the *authoring* layer on top:

  python scripts/new_archetype.py <domain> <target-dir>          # e.g. api ./template-api
  python scripts/new_archetype.py web ./template-web --language node
  python scripts/new_archetype.py <domain> <target-dir> --force  # overwrite existing scaffold

It only performs the MECHANICAL, repeatable steps (renamed answers file, archetype/language
intent, a pinned CI caller seed for Node) and then prints the editorial checklist — the
judgment work (deciding what is unique to the domain, rewriting README/AGENTS) stays with you.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

LANGUAGES = ("none", "node", "python", "terraform")

COPIER_YML = """\
# Copier configuration for template-{domain} — an ARCHETYPE template that COMPOSES template-base.
#
# Ships ONLY files unique to the {domain} domain. Everything universal keeps flowing from
# template-base by composition — never duplicate a base file here. Scaffold a repo with:
#   copier copy --vcs-ref=v1 git@github.com:{org}/template-base.git      <new-repo>
#   copier copy --vcs-ref=v1 git@github.com:{org}/template-{domain}.git   <new-repo>

_subdirectory: template

# Distinct answers file so this layer `copier update`s INDEPENDENTLY of the base layer and
# never clobbers the base's .copier-answers.yml.
_answers_file: .copier-answers-{domain}.yml

_envops:
  keep_trailing_newline: true

# Universal questions (org, license, runtime_version, build/test/run/lint, …) are OWNED BY
# template-base and answered by the base pass — do NOT re-ask them here. Declare only the
# questions unique to the {domain} archetype below.

# Recorded intent for repos generated from this archetype (hidden — not prompted).
archetype:
  type: str
  default: {domain}
  when: false

language:
  type: str
  default: {language}
  when: false

# ---- {domain}-specific questions (author these) ----
# example_option:
#   type: str
#   help: "One-line prompt shown at generation time."
#   default: "TODO"
"""

# Node-only CI caller seed. Rendered into repos generated FROM the archetype as
# .github/workflows/ci.yml — the "extend, don't copy" pattern, pinned to @v1 (never @main).
NODE_CI_CALLER = """\
# Node CI caller — references the reusable workflow hosted in template-base. Pin @v1 (or a SHA).
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    uses: {{ org }}/template-base/.github/workflows/reusable-node-ci.yml@v1
    with:
      node-version: "{{ runtime_version }}"
      package-manager: {{ pkg_manager }}
"""

CHECKLIST = """\
Mechanical scaffolding done. Editorial steps left to you (judgment — not scriptable):

  [ ] Rewrite README.md and AGENTS.md to describe the {domain} ARCHETYPE layer — what it adds
      on top of the base — not a renamed copy of template-base's own docs.
  [ ] Author the {domain}-specific questions in copier.yml and the files under template/.
  [ ] Confirm template/ duplicates NO file template-base already ships (the anti-duplication
      rule) — diff against the base's template/ if unsure.
  [ ] Commit, then cut a v1 tag so callers can pin template-{domain}@v1 (see README -> Releasing).
"""


def write(path: Path, content: str, *, force: bool, actions: list[str]) -> None:
    """Write `content` to `path`, refusing to clobber unless `force`."""
    if path.exists() and not force:
        actions.append(f"skip   {path}  (exists; pass --force to overwrite)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    actions.append(f"wrote  {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("domain", help="Functional domain, e.g. api / web / sagemaker.")
    parser.add_argument("target", type=Path, help="Path to the bootstrapped template-<domain> repo.")
    parser.add_argument("--language", choices=LANGUAGES, default="none", help="Runtime ecosystem (default: none).")
    parser.add_argument("--org", default="Knowledgemonger-LLC", help="GitHub org for the composed-source URLs.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files.")
    args = parser.parse_args(argv)

    target: Path = args.target
    if not target.is_dir():
        parser.error(f"target dir does not exist: {target} — bootstrap it first with `copier copy … template-base`.")
    if not (target / ".copier-answers.yml").exists() and not args.force:
        parser.error(
            f"{target} has no .copier-answers.yml — it does not look bootstrapped from template-base. "
            "Run `copier copy … template-base` first, or pass --force to scaffold anyway."
        )

    actions: list[str] = []
    write(
        target / "copier.yml",
        COPIER_YML.format(domain=args.domain, language=args.language, org=args.org),
        force=args.force,
        actions=actions,
    )

    template_dir = target / "template"
    template_dir.mkdir(parents=True, exist_ok=True)
    if not any(template_dir.iterdir()):
        write(template_dir / ".gitkeep", "", force=args.force, actions=actions)

    if args.language == "node":
        write(
            target / "template" / ".github" / "workflows" / "ci.yml.jinja",
            NODE_CI_CALLER,
            force=args.force,
            actions=actions,
        )

    print(f"\nScaffolded template-{args.domain} authoring layer in {target}:")
    for line in actions:
        print(f"  {line}")
    if args.language != "node":
        print(f"  note   no CI caller seeded (language={args.language}); template-base ships no CI for it.")
    print()
    print(CHECKLIST.format(domain=args.domain))
    return 0


if __name__ == "__main__":
    sys.exit(main())
