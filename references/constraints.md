# Verified Engine Constraints — Factorio 2.x / Space Age

Hard facts about how the engine behaves, confirmed by loader/runtime errors, in-game testing, game data on disk, or the API JSONs. These are architectural constraints, not style preferences — designs that fight them fail.

## Fluids & crafting machines

- **Crafting-machine fluid boxes belong to the recipe system.** On any `assembling-machine`-type entity (including chemical plants — chemical plant is not a separate type, just an assembling-machine with `fluid_boxes_off_when_no_fluid_recipe = false`):
  - Each input box **filters to the fluid named by the active recipe's ingredient**. Other fluids are rejected at the pipe-segment level; no script call overrides this.
  - **Only the first M boxes exist at runtime**, where M = the active recipe's fluid-ingredient count. Accessing index M+1 throws "Fluid index N is out of bounds" — derive valid indices from the assigned recipe's ingredient list, never from the prototype's box count.
  - Consequence: "one pipe that accepts whatever fluid arrives" is **impossible** on a crafting machine. Use a `storage-tank`/`pump` composition (see patterns.md).
- **Sealed fluid boxes (`pipe_connections = {}`) and script `add_fluid`:**
  - On **storage-tanks**: works. Sealed tank boxes accept `add_fluid` and are the standard script-side fluid store.
  - On **crafting machines**: only functional for boxes backed by the active recipe's fluid ingredients (see above). With no matching active recipe, `add_fluid` silently discards and `get_fluid` reads 0.
- Recipe ingredients can pin a fluid to a specific box via `fluid_ingredient.fluidbox_index` when script-feeding a multi-fluid crafter.
- `storage-tank` entities have **no `active` attribute** — no power state, not circuit-disableable. `active` belongs to crafting machines (`assembling-machine`, `furnace`, `rocket-silo`, …).

## Entities & placement

- **`create_entity` identifies prototypes by `name`, never by `type`.** `type` is a data-stage schema field only.
- **`next_upgrade` requires an identical bounding box.** Resizing a deepcopied machine (e.g. 3×3 → 1×1) while it inherits the base's `next_upgrade` is a hard data-stage error — set `next_upgrade = nil` or point it at a same-size entity.
- **Collision vs selection box convention** (verified across vanilla data): `selection_box` is flush with the tile footprint (±half the size); `collision_box` is inset so adjacent entities can be placed — vanilla 3×3 machines use ±1.2 to ±1.4 (0.1–0.3 inset). A flush collision box blocks adjacent placement (closed-interval collision).
- **Deepcopies don't inherit later-stage edits.** Anything another mod (including Space Age itself) adds in *data-updates*/*data-final-fixes* is absent from a copy made in your `data.lua`. Notable case: `surface_conditions` on vanilla containers.
- Hyphenated keys in Lua tables need bracket-string notation: `["day-night-cycle"] = 72000`, not `day-night-cycle = 72000`.
- `CargoBayPrototype.inventory_size_bonus` is required and **cannot be 0** (hard loader error; the API description states it). A cargo-bay always extends the hub/pad inventory by at least 1 slot.
- Container `inventory_type` variants (verified, prototype-api.json 2.1.8): `"normal"`, `"with_bar"` (default), `"with_filters_and_bar"`, `"with_custom_stack_size"`, `"with_weight_limit"`. Slot filters (`LuaInventory.set_filter(index, ItemFilter)`) require `with_filters_and_bar`; `ItemFilter` supports `{name, quality, comparator}`; `set_bar(1)` bars every slot. Enumerate these before scripting any inventory restriction.
- `LuaEntity.custom_status` is writable (`{diode = defines.entity_status_diode.red/yellow/green, label = LocalisedString}`) and renders in the entity GUI's status row (verified in-game on a cargo-bay). `LuaEntity.status` still reports the *actual* engine status even while a custom_status is set — usable for state checks like `defines.entity_status.not_connected_to_hub_or_pad` (the cargo-bay broken-chain state).

## Triggers & trigger effects

- **A land mine's circuit "Enable" condition means *detonate*, and detonation runs its `action` trigger.** Put `{type = "script", effect_id = ...}` in `action` and detonation raises `on_script_trigger_effect` — a circuit-condition→Lua bridge (see patterns.md). The event fires **even when the mine survives** (`force_die_on_attack = false`), and such a mine **auto re-arms**. (Verified in-game 2.1.10.)
- **Circuit detonation is evaluated every tick and is level-triggered.** While the condition stays true the mine re-fires **once per tick**. Neither `trigger_interval` (governs only the enemy-proximity scan) nor `timeout` (governs only initial post-placement arming) throttles circuit re-detonation — there is **no data-stage cooldown** for it (both tested, no effect, 2.1.10). Rate-limiting must come from pulsing the input signal upstream. (See graveyard.md.)
- **`TriggerEffectWithCooldown` is not a member of the `TriggerEffect` union.** It is accepted **only** in `SegmentPrototype.update_effects` / `update_effects_while_enraged` and `StickerPrototype.update_effects` (prototype-api 2.1.10). It cannot be placed in a land mine's `action` or any other plain `TriggerEffect` slot — the engine reads that slot as `TriggerEffect` and ignores/rejects the cooldown wrapper. General rule: a prototype field's behavior lives in the C++ for that specific field; a type does something only where the schema declares it.

## Recipes, items, subgroups

- A recipe's `subgroup` must name an existing `item-subgroup` prototype, or the load crashes. **Omitting `subgroup` is always safe** — it inherits from the primary result item.
- If you set one, verify it exists in `base/prototypes/item-groups.lua` or `space-age/prototypes/item-groups.lua`. Confirmed-existing examples: `intermediate-product`, `ammo`, `capsule`, `production-machine`, `space-material`, `space-crushing`, `space-platform`, `planet-connections`. Confirmed **not** existing: `combat`.
- `entity.set_recipe()` from script requires the recipe to be `enabled`; combine `enabled = true` with `hidden = true` for script-only recipes.

## Planets & space-locations

- `PlanetPrototype` **inherits** `SpaceLocationPrototype`. Verified field placement (prototype-api.json 2.1.8):
  - On `SpaceLocationPrototype` (both types): `asteroid_spawn_definitions`, `asteroid_spawn_influence` (double), `auto_save_on_first_trip` (bool), `label_orientation` (RealOrientation), `procession_graphic_catalogue` (singular `graphic` — the plural spelling is silently ignored), `solar_power_in_space`, `magnitude`, `distance`, `orientation`, `draw_orbit`, `starmap_icon*`.
  - **Planet-only** (rejected/meaningless on space-locations): `map_gen_settings`, `surface_properties`, `surface_render_parameters` (incl. `shadow_opacity`), `pollutant_type` (optional `AirbornePollutantID` — omit for no pollutant), `persistent_ambient_sounds`, `entities_require_heating`.
- `map_gen_settings.autoplace_settings` keys are exactly `"entity"`, `"tile"`, `"decorative"` (singular — `"tiles"` silently places nothing). `treat_missing_as_default` is a real per-category `AutoplaceSettings` field.
- **Changing a location's `type` between `space-location` and `planet` corrupts saves with a platform parked there** (orbital-logistics consistency assert on load). Make such changes only against fresh saves.
- `space-connection` prototypes use `subgroup = "planet-connections"` (verified to exist in Space Age data; vanilla uses it for all connections).
- Vanilla planet discovery technologies follow the pattern `planet-discovery-<name>` (verified: Space Age technology.lua) — not `<name>-visitation` or bare `<name>`.
- The technology effect that unlocks a location is `{ type = "unlock-space-location", space_location = "<name>" }` — the field is `space_location`, not `location`.
- At **runtime**, `LuaForce.unlock_space_location(name)` unlocks a greyed-out location for a force with no technology at all (positional `SpaceLocationID`); `is_space_location_unlocked(name)` queries it and `lock_space_location(name)` is the inverse. Required for locations that ship without a discovery tech — otherwise they stay unreachable on the starmap. (Verified in-game 2.1.)

### PlanetsLib (if used)

- Register planets/locations through `PlanetsLib:extend({...})`, not `data:extend` — PlanetsLib wraps `data:extend` with registration logic, and bypassing it leaves the body invisible to PlanetsLib-aware mods.
- Extend with **colon** notation — `PlanetsLib:extend({...})` — dot notation omits `self` and errors inside the library.
- `PlanetsLib:extend` **requires `orbit`** on every body, satellite or not: `orbit = { parent = { type = ..., name = ... }, distance = N, orientation = N }`. `parent` is a `{type, name}` table, not a string. Do **not** also set top-level `distance`/`orientation` — PlanetsLib rejects that. `is_satellite` goes inside `orbit`, not top-level.

### Asteroid spawn definitions

`local asteroid_util = require("__space-age__.prototypes.planet.asteroid-spawn-definitions")`

- `asteroid_util.spawn_definitions(route)` — **no second argument** → route format (`spawn_points` arrays). Required by `space-connection`.
- `asteroid_util.spawn_definitions(route, position)` — position float → flat planet format (`probability`/`speed` fields). Required by `planet`/`space-location`. Using the wrong shape for the prototype type crashes at load ("Key 'spawn_points' not found").
- The `position` argument must be one of the route's **significant positions** (the union of `position` values in its `type_ratios` and `probability_on_range_*` tables — e.g. `0.1`/`0.4`/`0.9` for `fulgora_aquilo`). Any other float returns an empty table and crashes downstream.
- Hand-written chunk definitions must set `type = "asteroid-chunk"` on chunk-size entries only; larger sizes omit `type`.
- `has_promethium_asteroids = true` adds a fourth (promethium) type to all spawn math — vanilla sets it only on the Shattered Planet trip.
- Asteroid entity naming: chunks are `{type}-asteroid-chunk`; sized asteroids are `{size}-{type}-asteroid` (small/medium/big/huge; metallic/carbonic/oxide/promethium).

## Locale & assets

- **Duplicate section headers in a locale `.cfg` are a fatal load error** ("Duplicate key in property tree") — one `[item-name]` (etc.) header per file, all keys under it.
- Missing locale renders as `__mod-name__key__` in game — cosmetic, not fatal.
- `__base__` holds all pre-Space-Age assets (nuclear reactor, assemblers, vanilla science packs); `__space-age__` holds only expansion additions (planets, asteroid chunks, platform structures, EM/cryo/agri science). Wrong prefix = file-not-found at load with no suggestion. Verify icon paths against the game files on disk before use.

## GUI

- See patterns.md § Entity GUIs. Key constraint: setting `player.opened = nil` inside `on_gui_opened` fires `on_gui_closed` immediately — the two handlers must be written as a pair.

## Testing in the map editor

- **The map editor pauses game time by default.** Entities do not craft, generate, burn fuel, move fluid, or tick logistics, and space platforms do not travel, until time is resumed or stepped via the editor's **Time** controls. A frozen editor is routinely misdiagnosed as a broken prototype/config — before debugging "nothing works," confirm time is actually advancing. (Verified in-game: a fully-correct fusion reactor→generator chain read 0 power, and downstream machines showed "no power," purely because editor time was paused.)
