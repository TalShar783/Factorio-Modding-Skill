# factorio-modding — Agent Skill for Factorio 2.x / Space Age

A Claude Agent Skill that stops agents from fighting the Factorio engine: verified constraints, proven compound-entity patterns, lifecycle/determinism rules, and query scripts that replace guesswork with lookups against the official API.

Scope: Factorio 2.x / Space Age only. Agent-facing usage instructions live in `SKILL.md` — that file, not this one, is what the agent reads.

If the project has [FMTK](https://github.com/justarandomgeek/vscode-factoriomod-debug) (`justarandomgeek.factoriomod-debug`) installed in VS Code with a Factorio version selected, the skill prefers FMTK's locally-generated API stub library over its own cached JSONs — see `SKILL.md` § Development environment (FMTK). The scripts/JSONs below are the fallback path for when FMTK isn't available.

## Layout

```
SKILL.md                          entry point: core paradigms, source-of-truth order, script directory
references/
  patterns.md                     proven architectures (compound entity, hidden crafter, cleanup, slicing...)
  lifecycle-and-determinism.md    load stages, on_init/on_load contracts, desync rules, event hygiene
  constraints.md                  verified engine constraints
  breaking-changes-2x.md          confirmed 1.x → 2.x renames/removals
  space-platforms.md              platform mechanics and events
  graveyard.md                    approaches known to fail, with verified reasons
  prototype-index.md              generated: all prototype classes, grouped, one line each
scripts/                          Python 3, stdlib only; see SKILL.md for the per-script contract
api/                              fallback: downloaded API JSONs (large; regenerable; gitignored)
```

## Setup (fallback path only, when FMTK isn't available) / after every game update

```
python scripts/fetch_api_jsons.py
python scripts/regenerate_indexes.py --prototype-json api/prototype-api.json --out-dir references
```

Generated files carry the game version in their header; regenerate when it no longer matches the installed game. Hand-curated reference files are never overwritten by scripts.

## Contributing / maintaining

- Verification standard: every reference entry must be backed by a loader/runtime error, in-game confirmation, game data on disk, the API JSONs, or the official auxiliary docs. Forum-sourced dev statements are marked as such. No speculation.
- Triage and supersession rules are in `SKILL.md` § Maintaining this skill. Never leave two entries that disagree.
- New tooling: Python 3, stdlib only. Git usage stays plain (see SKILL.md tooling conventions).
