# template-base

The starting point for new repos at Knowledgemonger-LLC. It carries a working agreement for AI
agents, a permission posture, and the handful of hygiene files every repo wants on day one.

It is used two ways, both the same mechanism:

1. **Copied to make a more specific template** — `template-web`, `template-sagemaker`, … A derived
   template is just a copy of this one that you specialize and then mark as a template itself.
2. **Copied to make an actual repo** — a product repo that starts from the baseline.

Either way: copy it once, and the copy is yours.

## Nothing here propagates

This is a GitHub **template repository**, not a live dependency. A repo created from it has no
upstream link, gets no merges, and is never checked for divergence. Deliberate: past attempts to
keep repos automatically in sync with a shared baseline cost more in tooling and merge conflicts
than the drift they prevented.

The trade-off is real — improvements made here reach existing repos only if a human carries them
over. [`CHANGELOG.md`](CHANGELOG.md) exists so you can see what has changed since you copied and
decide whether any of it is worth porting. Nothing will tell you automatically.

## Create a new repo

Click **Use this template → Create a new repository** on GitHub, or:

    gh repo create Knowledgemonger-LLC/<new-repo> --template Knowledgemonger-LLC/template-base --private --clone

Then open the new repo and run **`/bootstrap`**. A fresh copy still calls itself "template-base"
in several places; `/bootstrap` reads the actual code and re-points the identity slots — project
name, stack, the build/test/run/lint commands, the license holder, and the package-manager entry
in the permission allowlist.

## Create a more specific template

Same thing, plus one step at the end to make the result a template in its own right:

    gh repo create Knowledgemonger-LLC/template-<role> --template Knowledgemonger-LLC/template-base --public --clone
    # ... specialize it: add CI, stack configs, domain conventions ...
    gh repo edit Knowledgemonger-LLC/template-<role> --template

Add whatever that role needs — a CI workflow, lint configs, a framework scaffold — and rewrite
`README.md` and the `Working on template-base` section of `AGENTS.md` to describe the new thing.
Duplicating files that also exist here is expected: copying *is* the mechanism, and the copies
are free to diverge.

The shared `template-` prefix groups the family together in the org repo listing.

## What you get

| File | Why |
|---|---|
| `AGENTS.md` | The working agreement — Change protocol, how to ask a human for input, terminology and structure rules. Read by Claude Code and other agent tools. |
| `CLAUDE.md` | Thin Claude-specific pointer. Must not duplicate `AGENTS.md`. |
| `GLOSSARY.md` | Single source for what words mean in the repo: coined vocabulary, redefined ordinary words, domain terms of art. |
| `.claude/settings.json` | Permission posture: edits apply without prompting, `git push` asks, and `sudo` / `rm -rf` / reads of `.env*` and `~/.ssh/**` are denied. Git is the undo. |
| `.claude/commands/` | `/design`, `/implement`, `/bootstrap`. |
| `.editorconfig`, `.gitattributes`, `.gitignore` | Editor defaults, line-ending normalization, a minimal ignore base to extend. |
| `LICENSE` | Proprietary by default, so open-sourcing is always an explicit choice. Swap the body if the repo is meant to be open. |

## What you don't get, and why

**Governance files.** `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue templates,
and the PR template are **not** shipped here, because GitHub serves them automatically from an
org-level `.github` repository. Four things about that are easy to get wrong:

- The `Knowledgemonger-LLC/.github` repo must be **public**. Internal visibility is enough for
  the Markdown files but *not* for `ISSUE_TEMPLATE/` or `PULL_REQUEST_TEMPLATE.md`, which
  inherit only from a public `.github`.
- Inheritance keys on **account ownership**, not on the consumer's visibility — private repos
  do inherit. Only the source repo's visibility matters.
- Issue templates are **all-or-nothing**: a single local file under `.github/ISSUE_TEMPLATE/`
  makes the repo use *none* of the org defaults for that folder.
- Until that `.github` repo exists, inheritance silently no-ops. Nothing errors; the files are
  just absent.

**CODEOWNERS.** Looks like governance but cannot be inherited — GitHub reads `CODEOWNERS` only
from the repo itself. Add it per repo if you want it, and note two traps: the owning team must
exist in the org **with write access** or GitHub silently ignores the entry, and "Require review
from Code Owners" must stay **off** while a repo has one maintainer, since nobody can satisfy
their own required review.

**Renovate.** A `renovate.json` extending `github>Knowledgemonger-LLC/renovate-config` needs that
preset repo to exist and be public, or Renovate errors on every run. Add it once the preset is
real.

**CI.** No workflow ships here, because CI is language-specific — a Node pipeline is meaningless
in a Python or Terraform repo. CI belongs in the more specific templates.

## Repo visibility

Templates and any shared config repos are **public**: they hold scaffolding and governance
boilerplate, no product code or secrets, and GitHub's inheritance and preset resolution need it.
Product repos are **private** by default; nothing about being private blocks consuming a public
template.

See [`AGENTS.md`](AGENTS.md) for how to work in a repo built from this one.
