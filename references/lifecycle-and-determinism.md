# Lifecycle & Determinism — Factorio 2.x

How mod code loads, when each hook runs, and the rules that keep a mod deterministic (multiplayer- and replay-safe). Sources: the official auxiliary docs (`data-lifecycle`, `storage`) at lua-api.factorio.com and dev statements on the official forums — documentation-verified rather than error-verified. Violating the determinism rules produces desyncs, which surface as CRC mismatches with no line number, often long after the causing code ran; they are the single most expensive class of bug to diagnose, so these rules are cheaper to follow than to debug.

## Load stages and ordering

- Two prototype-defining stages run at game launch: **settings** and **data**. Each runs three rounds across *all* mods in dependency order: `<stage>.lua` for every mod, then `<stage>-updates.lua` for every mod, then `<stage>-final-fixes.lua` for every mod. The rounds exist so mods can modify other mods' prototypes without depending on load order.
- Stage placement etiquette (official docs + wiki-admin guidance):
  - **`data.lua`** — create your own prototypes. Create as early as possible: later-stage creation misses other mods' (and the base game's) automatic processing, e.g. a fluid added in final-fixes gets no barreling recipes.
  - **`data-updates.lua`** — modify prototypes other mods created.
  - **`data-final-fixes.lua`** — last resort only. Everything piling into final-fixes recreates the load-order conflicts the round system exists to prevent.
  - If you must see a specific mod's prototypes before yours run, declare it as an (optional) dependency in `info.json` rather than reaching for a later stage.
- The data-stage Lua state is **discarded** when loading finishes. No variable, function, or non-prototype data crosses into runtime. The only channel from data stage to control stage is the prototypes themselves; properties the engine doesn't recognize are silently dropped, so you cannot smuggle custom data through a prototype field.
- The `mods` global (name → version for all enabled mods) is available during the data stage for conditional compatibility logic.

## Runtime lifecycle (control stage)

Each mod gets its own Lua state, created fresh **every time a save is created or loaded**. Order of hooks and their contracts:

1. **`control.lua` top level** — runs on every load. Register event handlers, remote interfaces, commands. `game` is unavailable; `storage` is *not yet restored* and anything written to it here is overwritten. Do not initialize state here — use `on_init`.
2. **`on_init`** — new save, or mod newly added to an existing save. Full access to `game` and `storage`. This is where `storage` gets its initial shape.
3. **Migrations** — run once per save per migration file, full game access. The right place for prototype-rename fixups; `on_configuration_changed` is not (per official docs, things like recipe/tech unlock adjustments belong in migration scripts).
4. **`on_load`** — every load of a save the mod was already in. `game` unavailable; `storage` readable but **writing to it is an error** (enforced by the engine to prevent desyncs). Exactly three legitimate uses:
   - re-setup metatables not registered via `LuaBootstrap.register_metatable` (registered ones relink automatically),
   - re-register **conditional** event handlers based on what `storage` says,
   - create local references to `storage` subtables.
   Anything else here is a desync or an error. If a function needs to run in both `on_init` and `on_load`, split it into an on_load-safe part and the rest rather than branching inside.
5. **`on_configuration_changed`** — fires for all mods at once when the game version, any mod version, the mod set, a startup setting, or the prototype set changed. Reshape `storage` structures here. It does **not** fire when a client joins a running multiplayer session.
6. **Multiplayer join path:** a joining client runs *only* steps 1 and 4. Whatever those two steps produce must leave the joiner's Lua state identical to every other peer's — this is why conditional handler registration must be derived purely from `storage`, never from local flags or "first run" logic.

## Determinism rules (desync prevention)

- **`storage` is the only persistent store.** It is serialized into the save; each mod has its own instance; circular references are handled. It holds only nil/string/number/boolean, tables of those, and LuaObject references — no functions, no metatables (except registered ones). (2.0 renamed the old `global` table to `storage`.)
- **Any mutable state outside `storage` desyncs multiplayer.** A file-local counter that increments during play is the classic case (dev-confirmed desync reports): a joining client re-runs `control.lua` and starts the counter at its default while everyone else has a later value. Constants and pure functions at file scope are fine; anything that *changes after load* is not.
- **Conditional event registration must be reproducible from `storage` alone**, and re-done in `on_load`. Registering `on_tick` only from `on_init`, or based on a local flag, means joiners/loaders silently lack the handler — the historical desync-loop bug.
- **One handler per event per mod.** `script.on_event(id, fn)` *replaces* any previous handler for that id (a second `script.on_load(...)` likewise overwrites the first). Centralize: one registration per event that dispatches internally. Corollary from the devs: skip event-wrapper frameworks (multi-subscriber systems à la old stdlib) — they add overhead and mishandle invalidation; plain `script.on_event` plus your own dispatch is the endorsed shape.
- Deferring work by tick must key off game state (`game.tick`, values in `storage`) — never wall-clock or anything client-local.

## Entity reference hygiene

- **Check `.valid` before every use of a stored LuaObject** once any time has passed since you obtained it. Entities can disappear with *no* build/mine/die event: editor operations, other mods calling `destroy()` without `raise_destroy`, surface deletion.
- The guaranteed cleanup path is `LuaBootstrap.register_on_object_destroyed` + the `on_object_destroyed` event — the devs state it covers **all** removal paths, including the eventless ones above. See patterns.md § Guaranteed cleanup. Ordinary removal events are still worth handling for immediate response (e.g. refunding contents on mine); the registration is the backstop, not a replacement.
- Handle the **whole event family**, not one member. "Built" and "removed" each fan out across player/robot/platform/script variants (`on_built_entity`, `on_robot_built_entity`, `on_space_platform_built_entity`, `script_raised_built`, …; `on_player_mined_entity`, `on_robot_mined_entity`, `on_entity_died`, `script_raised_destroy`, …). Per core paradigm 5: dump the actual event list from runtime-api.json and enumerate the family deliberately before wiring handlers.

## Performance conventions

- **Filter at the engine, not in Lua.** Many entity events accept C++-side filter arrays (`{{filter = "name", name = "my-entity"}}` and richer and/or/invert combinations — see each event's `…EventFilter` type in runtime-api.json). A filtered registration never invokes Lua for non-matching entities; an unfiltered handler with an `if` at the top pays a Lua call for every biter death on the map.
- **`script.on_nth_tick(n, fn)`** for periodic work instead of `on_tick` + modulo when the cadence is fixed.
- **Slice bulk work across ticks** instead of bursting: steady small cost per tick beats a lag spike every N seconds. See patterns.md § Tick-work slicing.
- Keep per-event Lua cheap: hoist `local` references, don't call expensive API methods (`find_entities_filtered`, inventory scans) inside hot handlers when the result can be cached in `storage` at build time — which the compound-entity pattern already does by storing member handles.
