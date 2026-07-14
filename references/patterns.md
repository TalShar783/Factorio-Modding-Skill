# Proven Patterns — Factorio 2.x / Space Age

Ready-made architectures verified in production mod code. Prefer repeating one of these over inventing an ad-hoc solution. Each entry: when to use it, the recipe, and the failure it prevents.

---

## Compound entity (visible shell + hidden helpers)

**When:** one machine needs behaviors no single prototype supports — e.g. "accepts any fluid through one pipe," "stores five fluids separately," "crafts from script-staged ingredients."

**Recipe:**
- One **visible shell** entity — a real, functional prototype (not a cosmetic one), since the shell must carry whatever the player interacts with: fluid box, circuit connector, GUI, minability. Pick the native type closest to the shell's own job (e.g. `storage-tank` if the shell itself buffers fluid).
- N **hidden helpers** placed at/around the shell's position by the control script on build, each a native prototype doing exactly its native job (a `pump` for the real pipe connection, `storage-tank`s for per-fluid storage, an `assembling-machine` for crafting).
- Helper prototype template:
  ```lua
  helper.hidden         = true   -- top-level field, NOT a flags entry
  helper.minable        = nil
  helper.collision_mask = { layers = {} }   -- never collides
  helper.flags = { "not-on-map", "placeable-off-grid",
                   "not-blueprintable", "not-deconstructable" }
  helper.selectable_in_game = false
  ```
- Control script: create helpers in `on_built_entity` (and robot/platform variants), store the member handles in `storage` keyed by the shell's `unit_number`, destroy them all when the shell is removed — via the removal-event family plus the `on_object_destroyed` backstop (§ Guaranteed entity cleanup).
- Set `shell.fast_replaceable_group = nil` if the shell was deepcopied from a vanilla entity, or players can fast-replace it with the vanilla original.
- **Only the shell is blueprintable; helpers are respawned, never captured.** The `not-blueprintable` flag on helpers is load-bearing: without it a blueprint captures the helpers, so on paste the shell's build event spawns a fresh set *and* the blueprint places the captured ones — duplicated, orphaned helpers. The shell's build event (including robot/ghost revive) is the single source of helpers; the blueprint and its ghost carry the shell alone. (This is what the flag does — there is no `placed_by` field; `placeable_by` is unrelated, it only picks the smart-pipette item.)

**Why:** every attempt to force one prototype to host all behaviors hits engine walls (see graveyard: single-crafter fluid PMR, cosmetic-shell attempt). Composition keeps every behavior on an entity type the engine natively supports it on.

---

## One pipe, any fluid (intake pump + sealed buffer)

**When:** a machine must accept *whatever fluid arrives* through a single external pipe connection — impossible on any crafting-machine fluid box (they filter to the active recipe's ingredient).

**Recipe:**
- The assembly's only real pipe connection is a **hidden pump** at the machine's edge, facing outward. Widen its `collision_box` if needed so the connection position sits inside the declared bounding box (harmless when `collision_mask` is empty).
- The pump discharges nowhere: it has no engine link to the rest of the assembly. Its own fluid box just fills from the network; script drains it (`get_fluid`/`remove_fluid`) into a sealed buffer tank (`pipe_connections = {}` on a `storage-tank`), then routes onward (e.g. to per-fluid sub-tanks) via `add_fluid`.
- **Circuit-gate the pump** so a second fluid type can never enter while the buffer still holds the first: wire pump to shell, `circuit_condition` = `signal-everything == 0` against the shell tank's read-contents signal. The gate is native circuit logic — no per-tick script check.
- `flow_direction = "input"` on the pump makes the intake genuinely one-directional; extraction back out needs a separate path.

**Why:** storage-tanks don't filter by recipe, and sealed storage-tank boxes accept script `add_fluid` fine. The pipe segment itself enforces one-fluid-per-network, but the pump+tank pair accepts each arriving fluid in turn, letting script sort fluids by name.

---

## Hidden crafter (script-selected recipes, native crafting)

**When:** a machine should produce real recipe-driven output from script-staged ingredients — skip this pattern and you end up reimplementing batching, crafting speed, and output logic in Lua.

**Recipe:**
- Hidden `assembling-machine` co-located with the shell, chemical-plant style (`fluid_boxes_off_when_no_fluid_recipe = false`). Fluid boxes sealed (`pipe_connections = {}`), script-fed.
- A **dedicated recipe category used by nothing else**, strictly one-to-one: only this crafter has the category, and its recipes have no other category. Recipes stay `hidden = true` (never player-selectable) but `enabled = true` (they're assigned via `entity.set_recipe()`, which requires an enabled recipe).
- Script flow per cycle: pick an affordable recipe from the category → `set_recipe()` → move exactly the needed fluid/items into the crafter's input boxes/inventory (`defines.inventory.crafter_input`) → let vanilla logic craft → drain `defines.inventory.crafter_output`.
- When feeding fluids, derive valid fluid box indices **from the currently assigned recipe's ingredient list** — indices beyond the active recipe's fluid-ingredient count are out of range at runtime, not merely empty.
- Free bonuses from staying native: the active recipe renders as the ghost icon, and the machine can output its current recipe as a circuit signal.

**Why:** verified working end-to-end in production. The alternative (one machine with "internal tank" fluid boxes and blocker-ingredient recipes) is a graveyard entry.

---

## Circuit gating between compound members

**When:** one member of a compound entity must run only while another is in some state (empty, below threshold, etc.).

**Recipe:** wire the members together with a scripted circuit connection at build time and set a `circuit_condition` on the controlled member. The engine evaluates it every tick for free; script never polls.

**Why:** replaces the most common `on_tick` abuse. A condition like "pump enabled only while tank empty" is exactly what the circuit network natively does.

---

## Hidden combinators for native-speed counting/thresholding (offload from `on_tick`)

**When:** you would otherwise poll an entity every tick (or every nth tick) in Lua to count events, hold a running total, or fire when a value crosses a threshold — and the quantity you need is exposed as a circuit signal or derivable by combinator arithmetic. This generalizes the gating pattern above from "one condition" to "stateful computation."

**Recipe:**
- Build the logic from script-created `constant-`/`arithmetic-`/`decider-combinator` entities as hidden helpers of a compound entity (prefixed names, `raise_built = false`), exactly like any other hidden part.
- **Wire them with the 2.0 API** (this is a 1.x→2.0 breaking change — `connect_neighbour` no longer exists): `a.get_wire_connector(defines.wire_connector_id.circuit_red, true):connect_to(b.get_wire_connector(defines.wire_connector_id.circuit_red, true))`. Pass `true` to create the connector if absent.
- **Memory cell / latch** for zero-storage state: a decider wired output→input holds its value indefinitely (red loop = held value; a green counter signal decides when to update). Pair with a self-clock (decider wired to itself + a constant combinator) and a pulse (`=` decider on the clock) to get counters, thresholds, and periodic triggers entirely in-network.
- **Read a network value back into Lua** only when you actually need it: `entity.get_circuit_network(defines.wire_connector_id.circuit_red).get_signal(...)`.
- **Tear down every combinator when the parent dies** — compound-entity teardown discipline (see the compound-entity pattern); orphaned combinators keep computing.

**Why:** circuit logic runs in the engine's native C++ solver, not interpreted Lua, and costs **zero Lua↔C++ boundary crossings** — the crossing is the expensive part (reads off an entity measured ~4× a Lua table read; multiply by machine count × ticks for an `on_tick` poll). Combinator state is also **deterministic and multiplayer-safe by construction**: no `storage` table, no `on_load` re-registration, no desync risk, no migration.

**Costs (when NOT to):** combinators are real entities occupying tile positions — a genuine footprint cost, not free, and on space platforms footprint is often the thing you're trying to minimize. Each combinator adds **1 tick of step-delay** (a chain's latency is the tell — Filter Combinator's advertised 3-tick delay is three combinator steps), so this is unusable for same-tick response. And combinators can only do signal arithmetic: they **cannot touch inventories, mutate item durability, move items, or call any API**. Anything that mutates game state still needs Lua.

**The hybrid (the high-value case):** let combinators do the cheap high-frequency part and Lua do only the rare mutation. Example — per-craft durability drain with no per-tick Lua: enable the machine's native recipe-finished pulse (see next pattern), feed it into a combinator memory cell that counts crafts and emits a signal at threshold; Lua reacts only when that signal fires and does the one thing combinators can't — decrement the tool item's `LuaItemStack.durability`. Per-tick Lua work collapses to near-zero.

---

## Detecting machine craft completion (no event exists)

**When:** script must react to an assembling-machine/furnace finishing a craft. **There is no machine-crafting event** — `on_player_crafted_item` covers only character crafting; nothing fires for machines. Two verified pull-based levers:

- **`LuaEntity.products_finished`** (read-only `uint32`): lifetime count of products the machine has finished. Diff it against a stored previous value on a **budgeted** poll (`on_nth_tick`, not `on_tick`) to detect completions cheaply. Simplest for a small, bounded set of purpose-built machines.
- **Native "recipe finished" circuit pulse**: set `control_behavior.circuit_read_recipe_finished = true` and `circuit_recipe_finished_signal = {...}` on the machine's `LuaAssemblingMachineControlBehavior`. Emits a one-tick pulse per completed craft — feed it straight into the combinator pattern above for zero-Lua counting.

**Why:** avoids the outdated/expensive approaches (polling `crafting_progress` fractions or scanning output inventory every tick). Prefer the circuit pulse when the reaction can stay in-network; use `products_finished` when Lua must act and the machine count is small.

---

## GUI standards checklist

**When:** any custom panel. Work through this list in order — every deviation from vanilla GUI conventions reads as jank to players.

**1. Anchoring — enumerate your options first.**
- Preferred: `player.gui.relative` anchored beside the entity's own GUI. Close button, E/Esc handling, and positioning come free, and the default entity GUI stays visible (use it to show current contents).
- **Enumerate `defines.relative_gui_type` to find the owning window's anchor** — do not assume one exists. Not every entity GUI has a relative type (verified: storage-tank has none), and the engine-rendered native windows are not children of `player.gui.screen`, so their positions cannot be read or docked to.
- Fallback when no anchor exists: a `player.gui.screen` panel (see 2–4 below).

**2. Screen panels get vanilla chrome.** Title bar = a flow with `drag_target = frame`, a `frame_title`-style label, a stretchable `draggable_space_header` filler, and a `frame_action_button` close button using `utility/close` sprites. Optionally a `status_image` sprite in the title bar for live state (working/yellow/red).

**3. Hotkey behavior must match vanilla.** Tie the panel's lifecycle to the owning entity's `on_gui_opened`/`on_gui_closed` so E and Esc close it with the entity GUI; the close button sets `player.opened = nil` rather than destroying the frame directly. Handle **both** open and close events — and **never** set `player.opened = nil` inside `on_gui_opened` to suppress a default GUI (it fires `on_gui_closed` immediately and corrupts your state tracking).

**4. Position for every resolution.** Compute placement from `player.display_resolution` divided by `player.display_scale` — never hardcode pixels for one monitor. If a fixed position is unavoidable, expose the corner as a runtime-per-user mod setting so players can move it.

**5. Update in place.** Store references to the mutable elements (bars, labels, status sprites) when building the panel and refresh values on tick; never rebuild the panel per refresh (flicker, focus loss).

---

## Output placement: belts by type, with fallback chain

**When:** script places produced items into the world next to a machine.

**Recipe:**
- Match candidate belts by `entity.type == "transport-belt"` (all tiers share the type), **never** by prototype name (`"transport-belt"` the name is only the base tier).
- Insert onto a belt via `LuaTransportLine.insert_at_back(items, belt_stack_size)` — items table first.
- Fall back in order: belt → adjacent container's inventory → `surface.spill_item_stack` on the ground.

---

## Throttling engine passthrough (token bucket + inserter hand-watching)

**When:** a rate limit on item flow through an entity whose movement is pure engine logic (proxy-container, native inventories) — there is no per-transfer event to hook.

**Recipe:**
- **Token bucket in script storage**: refill at R items/sec each pass, cap at ~1 second's worth. Each observed item subtracts. At ≤ 0, refuse traffic (for a proxy-container: `proxy_target_entity = nil` — inserters stall harmlessly holding their items) and set `custom_status` (red diode + label). Reattach when the bucket refills. Never interrupt a swing mid-flight: overshoot just drives the budget further negative, lengthening the cooldown proportionally.
- **Counting**: watch the hands of the inserters targeting the entity. Rescan nearby inserters occasionally (~120 ticks) keeping those whose `pickup_target`/`drop_target` is the entity (or its proxy — targets resolve to whichever entity occupies the tile, match both). Each throttle pass (~5 ticks, well under one swing time), diff each hand's `held_stack` count: decrease while dropping at the entity = insertion; increase while picking from it = extraction. Re-baseline hands on reattach so unrelated movement during the cooldown isn't billed.
- **Blind spots — document them where the throttle lives**: only inserters are counted. Player hand-transfers bypass the count (usually desirable — throttle automation, not the player); loaders/bots/anything else would too, so keep them unable to reach the proxy.
- **Close the native bypass**: if the visible entity is a cargo-bay-family prototype, set `allow_unloading = false` and the smallest accepted `inventory_size_bonus` — the engine **rejects 0** with a "Cannot be 0" loader error (hit in testing); use `1`+ and accept the small bonus — so the throttled proxy is the *only* item path — a connected bay with native unloading lets inserters pull from the hub uncounted.

**Proven:** in-game verified — sustained feeds hit the cooldown, bulk swings pass whole with proportionally longer cooldowns, red status renders.

---

## Research-driven script values: read technology levels live

**When:** any script behavior scales with research (limits, rates, ranges).

**Recipe:** derive the value from `force.technologies["tech-name"]` at point of use — for upgrade techs the completed count is `tech.researched and tech.level or (tech.level - 1)`. Do **not** accumulate a counter in `on_research_finished`. (The `(tech.level - 1)` branch for *partially-researched* upgrade techs is confirmed in-game: editor de-research/re-research visibly stepped the derived rate per level, 2026-07-13.)

**Why (verified in-game):** event counters miss every research change that doesn't fire the event normally — scenario scripts researching everything at init, editor un-research/re-research, `research_all_technologies()`. A counter-based rate sat at base level in an all-researched scenario and ignored editor changes entirely; live reads track all of them, including un-research.

---

## Script storage as the source of truth

**When:** tracking per-entity state, accumulated amounts, or compound-entity membership.

**Recipe:** key everything in `storage` by the visible shell's `unit_number`; store member entity handles at creation instead of re-finding them each tick; validate with `entity.valid` before every use after any time has passed.

---

## Surface-restricted placement (`surface_conditions`)

**When:** an entity should be placeable only on space platforms, or only on planets.

**Recipe:**
- Platform-only: `surface_conditions = { { property = "gravity", min = 0, max = 0 } }`
- Planet-only: `surface_conditions = { { property = "gravity", min = 0.1 } }` (what Space Age itself applies to vanilla containers)
- **Deepcopy timing trap:** Space Age adds its `surface_conditions` to vanilla entities in *data-updates*. A `table.deepcopy` of a vanilla entity made in your `data.lua` runs **before** that and does not inherit the condition — always set `surface_conditions` explicitly on copies.

---

## Guaranteed entity cleanup (`on_object_destroyed` backstop)

**When:** any state keyed to an entity's lifetime — compound-entity members, `storage` entries, GUIs — that must never leak.

**Recipe:**
- On creation, call `script.register_on_object_destroyed(entity)` and store the returned registration number in `storage`, mapped to the entity's cleanup data.
- Handle `on_object_destroyed` and tear down by registration number. The event fires at end of the current or next tick, after the object is already gone — clean up state, don't touch the entity.
- Keep the ordinary removal handlers (`on_player_mined_entity`, `on_entity_died`, platform variants, …) for anything needing the live entity or its buffers (refunds, item transfers). The registration is the backstop, not the replacement.
- Verify the exact signature/fields in runtime-api.json before use (per SKILL.md rule 6).

**Why (dev-stated):** entities can vanish with *no* normal event — editor operations, other mods calling `destroy()` without `raise_destroy`, surface deletion. `register_on_object_destroyed` is the only path the devs guarantee covers all removals. Mods that rely solely on mined/died events leak orphaned helpers and `storage` entries. This is also why every stored entity handle needs an `entity.valid` check before use.

---

## Tick-work slicing (spread bulk scans across ticks)

**When:** periodic work over many tracked entities that would lag if done in one burst.

**Recipe:**
- Fixed cadence, small population: `script.on_nth_tick(n, fn)` — not `on_tick` + modulo.
- Large population: process a deterministic slice per tick, e.g. `for key, e in pairs(storage.units) do if key % 64 == game.tick % 64 then update(e) end end`. Keying the slice by `unit_number` self-balances as entities are added/removed.
- Slice selection must derive only from game state (`game.tick`, `storage` contents) — never wall-clock or per-client data (desync; see lifecycle-and-determinism.md).

**Why:** steady small cost per tick beats a lag spike every N seconds; the modulo-slice pattern is the forum-standard answer for thousands-strong entity lists. Before reaching for this at all, check whether a circuit condition or native prototype behavior removes the need to poll (core paradigm 3).

---

## Circuit-condition → Lua event bridge (land mine)

**When:** you need a circuit condition (or any in-world moment with no native event) to *push* into Lua without per-tick polling. Companion to § Detecting machine craft completion — that covers the recipe-finished pulse; this is the general circuit-condition case.

**Recipe:**
- Build a purpose-built `land-mine` (deepcopy vanilla, rename). A land mine is the one entity whose circuit "Enable" condition **detonates** it, and detonation runs its `action` trigger.
- Set `action` to a single `{type = "script", effect_id = "<unique>"}` — strip all damage/explosion effects. Detonation then does nothing but raise `on_script_trigger_effect`.
- Handler: `script.on_event(defines.events.on_script_trigger_effect, fn)`, branch on `event.effect_id`. Optionally re-raise a `custom-event` so other mods can subscribe.
- `force_die_on_attack = false` → the mine **survives detonation and auto re-arms**, so no per-event script respawn is needed.
- Make it inert to *physical* triggering: empty `trigger_collision_mask`, tighten `trigger_force`, minimal `trigger_radius`; blank `picture_safe`/`picture_set`/`picture_set_enemy` to hide it. Script-place it (`raise_built = false`, `not-blueprintable`, respawn on the owner's build event) and lifecycle-clean it (full built/removed matrix + `on_entity_cloned`).

**Critical (verified in-game 2.1.10):** circuit detonation is evaluated **every tick** and is **level-triggered** — while the condition holds true the mine re-fires once per tick, and no data field throttles it (see constraints.md § Triggers, graveyard.md). The design is only cheap for **rare** events, so the *consumer* must **pulse the input signal** (true for one tick per real crossing) via upstream circuit edge-conditioning. A sustained-true condition is the worst case (one boundary crossing per tick).

**Why:** the only native circuit-condition→trigger path in the engine. Wins over polling only when events are genuinely rare (rarer than ~1 per 5–10 s) and the signal is pulsed; otherwise stay in-circuit or poll on a budget.
