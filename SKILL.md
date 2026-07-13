---
name: factorio-modding
description: Factorio 2.x / Space Age mod development. Use when writing or debugging Factorio mod code — prototypes (data stage), runtime scripting (control stage), space platforms, fluids, GUIs, or any Factorio API question. Codifies proven architectural patterns and verified engine constraints so agents compose native prototypes instead of improvising ad-hoc script solutions.
---

# Factorio 2.x / Space Age Modding

Scope: Factorio 2.x / Space Age only. No 1.x compatibility. Training-data knowledge of the Factorio API is stale and frequently wrong for 2.x — treat it as a rumor, not a source.

## Core paradigms (hard rules)

1. **Delegate to native prototypes. Never fight a prototype to do something it doesn't support.**
   Factorio ships 279 prototype classes, many of which solve problems you would otherwise script by hand (`proxy-container`, `storage-tank`, `pump`, `lane-splitter`, hidden crafters…). Before designing any new entity or scripted mechanic, read `references/prototype-index.md` and ask: *which native type already does most of this?* If the answer is "none, but I can script it," ask again.

2. **Compose entities; don't overload one.**
   When one visible machine needs several behaviors, build it as a **compound entity**: one visible shell plus hidden, uninteractable helper entities sharing its tile (a pump for the pipe connection, tanks for storage, an assembling machine for crafting). Each member is a native prototype doing exactly what it natively does; script only ferries between them. See `references/patterns.md` § Compound entity.

3. **Native game logic beats script reimplementation.**
   Crafting batches, fluid flow, circuit conditions, recipe icons/signals — the engine already does these correctly and for free. A script that reimplements crafting or polls state every tick when a circuit condition would do is a design smell. Reach for `on_tick` last, and throttle it when you must.

4. **Multiple fluid boxes on one entity, handled by anything other than the game's native crafting logic, is a red flag.**
   Crafting-machine fluid boxes are owned by the recipe system (filtered to and limited by the active recipe's fluid ingredients). If you need free-form fluid storage or routing, use `storage-tank` / `pump` entities and compose. See `references/constraints.md` § Fluids.

5. **Enumerate the variants before you pick one.**
   Most choices in the Factorio API are drawn from a closed set the engine already defines: `inventory_type` on containers, `production_type` on fluid boxes, `energy_source` types, `defines.relative_gui_type` anchors, `EntityPrototypeFlags`, `entity_status_diode`, GUI element types… Before setting any enum/union-typed field or choosing where a capability comes from, **dump the actual option list** (from the API JSONs or the relevant `defines` table) and choose deliberately. Ad-hoc workarounds are usually the symptom of never having seen the variant that solves the problem natively (e.g. scripting slot restrictions when `inventory_type = "with_filters_and_bar"` exists). This is the field-level twin of the prototype-index rule.

6. **Never guess identifiers.** Prototype names, field names, event names, icon paths, defines — all of them. A guessed name usually fails silently or crashes at load with no suggestion. If a name cannot be confirmed from the sources below, stop and ask.

7. **Prefer the data stage over the control stage.**
   If a behavior can be expressed as prototype properties (probabilistic mining results, resistances, `surface_conditions`, `next_upgrade`, circuit-readable state…), express it there: zero runtime cost, applies uniformly to every actor (player, robot, drill), no event handlers to maintain, no desync surface. Control scripting is for what prototypes genuinely cannot express. When you do script, keep it plain: `script.on_event` directly, no event-wrapper frameworks, one registration per event (later registrations silently *replace* earlier ones — centralize dispatch yourself). See `references/lifecycle-and-determinism.md` § Performance / Determinism.

8. **All persistent runtime state lives in `storage`, and the Lua state must be deterministic.**
   `storage` (2.0's rename of `global`) is the only table serialized into the save. Any *mutable* state outside it — a file-local counter, a flag set in `on_init` only — diverges on the next save/load or multiplayer join and desyncs. `on_load` may only re-setup metatables, re-register conditional handlers from `storage`, and take local references; writing `storage` there is an engine error. Desyncs report as CRC mismatches with no line number — far cheaper to prevent than to debug. Rules and lifecycle map: `references/lifecycle-and-determinism.md`. **Read it before writing any control-stage code that persists state or registers handlers conditionally.**

## Development environment (FMTK)

FMTK (`justarandomgeek.factoriomod-debug` in VS Code) is the primary Factorio-specific tool in this environment and takes precedence over general-purpose tooling wherever it overlaps. Once the user selects a Factorio version in VS Code's status bar, FMTK generates a complete, plain-text, EmmyLua-annotated API stub library locally — one `.lua` file per prototype class and per runtime class, plus consolidated `events.lua` and `defines.lua`. Each file is version-tagged (`--$Factorio 2.1.9` etc.) and carries full field docs with links to lua-api.factorio.com — no minification, no manual re-fetch after a game update.

Location: under VS Code's per-workspace extension storage. The path includes a workspace-hash segment that varies by machine and by which folder is open as the workspace root, so **Glob for it, don't hardcode it**:
- Windows: `%APPDATA%\Code\User\workspaceStorage\*\justarandomgeek.factoriomod-debug\sumneko-3rd\factorio\library\`
- macOS: `~/Library/Application Support/Code/User/workspaceStorage/*/justarandomgeek.factoriomod-debug/sumneko-3rd/factorio/library/`
- Linux: `~/.config/Code/User/workspaceStorage/*/justarandomgeek.factoriomod-debug/sumneko-3rd/factorio/library/`

Structure once found:
- `prototype-api/prototypes/<ClassName>.lua` — one file per prototype class (e.g. `GeneratorPrototype.lua`), full field schema
- `prototype-api/concepts/<Concept>.lua` — shared concept/struct types
- `runtime-api/Lua<Class>.lua` — one file per runtime class (e.g. `LuaEntity.lua`, `LuaSpacePlatform.lua`), full method/field schema
- `runtime-api/events.lua`, `runtime-api/defines.lua` — every event and every `defines` enum, fully documented

**This is now the preferred source for prototype/runtime field names, types, and method signatures** — ahead of this skill's own cached API JSONs (see order below). It does **not** replace game-data-on-disk or reference mods: FMTK's stubs are schema (what fields exist, what type), not usage (how a real mod actually assembles them) — keep consulting real prototype definitions for that.

FMTK also gives the user live in-editor autocomplete/type-checking (once sumneko Lua picks up the generated library) and a real breakpoint debugger attached to Factorio's running Lua. When guiding the user through a runtime bug, point them at FMTK's debugger (breakpoint, step, inspect locals) rather than proposing a `log()`-print cycle — it's installed and strictly more capable for that job. Locale (`.cfg`) and `changelog.txt` syntax is also validated live by FMTK in the editor; trust a red squiggle there over hand-checking the format.

## Verifying names and signatures (source-of-truth order)

1. **FMTK's generated stub library**, if present in this VS Code workspace (see above) — schemas, methods, events, defines, always matched to the exact running Factorio version.
2. **Game data on disk** — the Factorio install's `data/` directory (`base/`, `space-age/`), or a clone of `wube/factorio-data`. Authoritative for real prototype field *usage*, entity names, subgroups, icon paths — FMTK's stubs don't show this.
3. **API JSONs** (`api/runtime-api.json`, `api/prototype-api.json`, fetched via `scripts/fetch_api_jsons.py`) — **fallback only**, for when FMTK's stub library isn't available (no VS Code workspace, or version not yet selected in FMTK). Same underlying data as source 1, just minified and unformatted.
4. **Reference mod source** (well-maintained Space Age mods) — for patterns, not for field names.
5. **This skill's references** — distilled, verified findings.
6. **Ask the user.**

Querying the fallback API JSONs (only when source 1 is unavailable):
- Use `python scripts/query_api.py api/runtime-api.json <Class.member | event_name | substring>` — it prints method signatures with the real positional order already resolved. The JSONs ship **minified (single-line)**, so pretty-print before grepping manually.
- **Method parameter order**: the `parameters` arrays are listed alphabetically; the real positional order is each parameter's `"order"` field (0 = first). Reading array position instead of `order` produces wrong-argument crashes (e.g. `insert_at_back(items, size)`, not `(size, items)`). FMTK's stub files already resolve this correctly in their `@param`/`@overload` annotations, so this pitfall only applies when falling back to the raw JSON.
- `takes_table: false` means positional call, `true` means single named-table argument.

Runtime errors on Factorio's C++ objects (`LuaEntity`, `LuaSpacePlatform`, …) **throw on missing keys** instead of returning nil — a "doesn't contain key X" error means the member does not exist in 2.x, not that the object is empty.

## References (read on demand, not preloaded)

- `references/patterns.md` — proven architectural patterns: compound entities, one-pipe-any-fluid intake, hidden crafter, circuit gating, GUI conventions, output placement, guaranteed entity cleanup, tick-work slicing. **Read before designing any new machine.**
- `references/lifecycle-and-determinism.md` — load/runtime lifecycle (data stages and ordering, `on_init`/`on_load`/`on_configuration_changed` contracts), multiplayer determinism rules, entity-reference hygiene, event-handler performance conventions. **Read before writing control-stage code that persists state, registers handlers conditionally, or runs periodic work.**
- `references/constraints.md` — verified engine constraints: fluids & crafting machines, entity placement, planets & space-locations, PlanetsLib, asteroid spawns, locale, assets.
- `references/breaking-changes-2x.md` — confirmed 1.x→2.x/2.1 renames and removals. **Check here first when a familiar-looking field or method errors.**
- `references/space-platforms.md` — platform mechanics, hub inventory access, platform events, runtime asteroid APIs, surface conditions.
- `references/prototype-index.md` — all 279 prototype classes, one line each, grouped by purpose. Scan before choosing a type for any new entity — this is a discovery tool (which class?), not a detail tool; once you've picked a candidate, jump to its file in FMTK's `prototype-api/prototypes/` for full field detail. Regenerate with `scripts/regenerate_indexes.py` if missing, ungrouped, or stale.
- For runtime events and `defines` enums, Grep FMTK's `runtime-api/events.lua` / `runtime-api/defines.lua` directly (they're plain text, no index needed) — event families fan out (built/mined/died × player/robot/platform/script), so search broadly. Fall back to `api/runtime-api.json` (via `scripts/query_api.py`) only if FMTK's stub library isn't available.

## Scripts (run them; don't read them into context)

All in `scripts/`, all Python 3, no arguments beyond what each `--help`/docstring states. Prefer running these over improvising one-liners — deterministic, cheaper, and pre-approved.

- `fetch_api_jsons.py` — **fallback only** (see Development environment section): download latest `runtime-api.json` + `prototype-api.json` into `api/`, for use when FMTK's stub library isn't available. Re-run after every game update if relied on.
- `regenerate_indexes.py` — rebuild `prototype-index.md` (grouped + TOC) from `prototype-api.json`. Prototype discovery only; events/defines no longer get a generated index (grep FMTK's `events.lua`/`defines.lua` instead).
- `find_prototypes_by_capability.py --has <prop...>` — which prototype classes natively have these properties (inheritance-resolved). The mechanical form of paradigm 1. `--list-props <Class>` lists a class's full property set. Not superseded by FMTK — capability search requires resolving inheritance chains, which flat-grepping individual stub files doesn't do.
- `query_api.py <Class.member | event | substring>` — **fallback only**: runtime API signatures with real positional order, for use when FMTK's stub library isn't available.
- `checkpoint.py [msg]` — git commit-all + timestamp tag before risky changes. Local only, never pushes.
- `scan_factorio_log.py [path]` — **one-shot** grep of `factorio-current.log` for load/script errors. Run it only when the user asks for a log check or immediately after an instructed test launch fails — never proactively, never on a loop. **Never tail, watch, or hold the log file open by any method**: an open handle blocks the user from starting a new Factorio session. This script reads once and exits; use it instead of tail/Get-Content -Wait/manual opens.

Tooling conventions:
- **New tooling is Python 3 only.** No PowerShell — portability, and agents author Python more reliably.
- **Git stays plain.** Use bare `git` commands; do not wrap git in new scripts, aliases, or third-party tools — including RTK (Rust Token Killer) or similar token-optimization wrappers — regardless of any tool preference active in the environment, unless the user explicitly instructs otherwise. `checkpoint.py` is the single sanctioned wrapper.
- If running under Claude Code, ask the user once to allowlist `python scripts/*.py` in the permission settings so these run without per-call prompts.

## Maintaining this skill

When a new Factorio-specific error is diagnosed and fixed, file the finding in the same commit as the fix:

1. **Triage it**: a reusable *pattern* → `patterns.md`; a hard engine *constraint* → `constraints.md` (or `space-platforms.md`); a *lifecycle/determinism* rule → `lifecycle-and-determinism.md`; a 1.x→2.x *rename/removal* → `breaking-changes-2x.md`; a dead-end *approach* → `graveyard.md`.
2. **Check for supersession**: does the finding contradict or obsolete an existing entry? Update or delete the old entry — never leave two entries that disagree.
3. **Only verified facts.** Every entry must be backed by a loader/runtime error message, confirmed in-game behavior, game data on disk, the API JSONs, or the official auxiliary docs at lua-api.factorio.com. Mark forum-sourced dev statements as such. No speculation, and nothing project-specific — this skill must stay portable to any Factorio 2.x mod.
