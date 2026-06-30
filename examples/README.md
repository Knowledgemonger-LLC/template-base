# examples/

Consumer-side snippets showing how a target repo plugs into the baseline. Authored in a
later phase. Planned contents:

- **Tier 2 (inherit):** what the org `.github` repo provides and why target repos define no
  local governance files.
- **Tier 4 (extend):** thin caller workflows that `uses:` the reusable workflows hosted in
  this repo (pinned to `@v1`), plus thin `eslint.config.js` / `tsconfig.json` / `renovate.json`
  that extend the external shared packages and presets.
