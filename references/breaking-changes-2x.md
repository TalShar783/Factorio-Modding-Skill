# Confirmed 1.x → 2.x / 2.1 Breaking Changes

Every entry here was confirmed by a live loader/runtime error or the API JSONs. When a familiar-looking field or method errors, check this table before anything else — the most likely cause is stale training data.

## Data stage (prototypes)

| Wrong (1.x / training data) | Correct (2.x) | Notes |
|---|---|---|
| `category = "crushing"` (recipe) | `categories = { "crushing" }` | 2.1 merged `category` + `additional_categories` into one array. Single string is a hard error. |
| `categories = { "recycling-or-hand-crafting" }` | `categories = { "recycling", "hand-crafting" }` | Combined category split in 2.1. |
| `{ ..., probability = 0.03 }` in recipe `results` | `{ ..., independent_probability = 0.03 }` | 2.1 rename, no semantic change. |
| `fuel_category = "x"` (burner energy source) | `fuel_categories = { "x" }` | Singular form is a hard error in 2.x. |
| `production_type = "none"` (crafting-machine fluid box) | Only `"input"` / `"output"` exist | "Crafting machine fluidboxes must be input or output types." |
| Fluid box without `pipe_connections` | `pipe_connections = {}` (empty array) | Required on **every** fluid box in 2.x, even sealed internal ones. Loader error indexes fluid boxes 0-based. |
| `flags = { ..., "hidden" }` | `hidden = true` as a top-level prototype field | `"hidden"` is not in the `EntityPrototypeFlags` enum (verified against prototype-api.json). |

## Runtime (control stage)

| Wrong (1.x / training data) | Correct (2.x) | Notes |
|---|---|---|
| `surface.create_entity{ name = "flying-text", ... }` | `player.create_local_flying_text{ position, text, color, time_to_live }` | `flying-text` entity removed. Verified: `LuaPlayer.create_local_flying_text` in runtime-api.json. |
| `game.item_prototypes[name]` (and all `game.*_prototypes`) | `prototypes.item[name]`, `prototypes.entity[...]`, `prototypes.recipe[...]`, … | Replaced by the `prototypes` global. Still throws on missing keys. |
| `entity.fluidbox[N]`, `entity.fluidbox.get_capacity(N)` | `entity.get_fluid(i)` / `set_fluid(i, fluid)` / `add_fluid(i, fluid)` / `remove_fluid(i, amount)` / `clear_fluid(i)` / `get_fluid_capacity(i)` | No `fluidbox` attribute and no `LuaFluidBox` class in 2.x — for **any** entity type. **Index is always the first argument.** |
| `for name, count in pairs(inv.get_contents())` | `for _, item in ipairs(inv.get_contents())` — entries are `{name, quality, count}` | Return type changed from `{[string]: uint}` to `ItemWithQualityCount[]`. Applies to `LuaInventory` **and** `LuaTransportLine`. Slot iteration (`for i = 1, #inv`) unaffected and preferred for inventories. |
| `defines.inventory.assembling_machine_input` / `_output` | `defines.inventory.crafter_input` / `crafter_output` (also `crafter_modules`, `crafter_trash`) | Verified in runtime-api.json; only `assembling_machine_dump` survives the old naming. Passing the old define gives nil → "real number expected got nil". |
| `a.connect_neighbour{ wire = ..., target_entity = b }` | `a.get_wire_connector(defines.wire_connector_id.circuit_red, true):connect_to(b.get_wire_connector(defines.wire_connector_id.circuit_red, true))` | `connect_neighbour`/`disconnect_neighbour` removed. Wires now go through `LuaWireConnector` (`connect_to`, `disconnect_from`, `disconnect_all`, `is_connected_to`). Second arg `true` creates the connector if absent. Verified: no `connect_neighbour` on LuaEntity; `LuaWireConnector` + `defines.wire_connector_id` present. |
