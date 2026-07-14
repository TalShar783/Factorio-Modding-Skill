# Graveyard — Approaches Known to Fail

Architecture-level dead ends, each verified by hitting the wall in practice. Do not retry these; use the pattern listed as the replacement. (Field-level renames live in breaking-changes-2x.md; single-fact constraints in constraints.md.)

---

## Single crafting machine with "internal tank" fluid boxes

**The idea:** one `assembling-machine` (or chemical-plant deepcopy) holds extra sealed fluid boxes as internal storage, script accumulates arbitrary fluids in them, display recipes with an unobtainable "blocker" fluid ingredient stop native crafting from firing.

**Why it's dead (each step verified):**
1. `production_type = "none"` boxes are a hard loader error in 2.x — crafting-machine boxes must be `"input"`/`"output"`.
2. With `"input"` boxes, only the first M boxes exist at runtime (M = active recipe's fluid-ingredient count), and each filters to its recipe fluid — so every display recipe must enumerate every internal fluid, and the box count can never exceed the recipe's ingredient list.
3. `add_fluid` into a sealed crafting-machine box with no matching active recipe silently discards; `get_fluid` reads 0.
4. The one external pipe connection filters to the active recipe's fluid — "accept whatever arrives" is impossible on a crafting machine.

**Use instead:** compound entity — hidden `pump` intake + sealed `storage-tank`s for storage + hidden crafter for recipe-driven output (patterns.md).

---

## Cosmetic shell entity (`simple-entity-with-owner`) fronting a machine

**The idea:** the visible entity is a purely decorative `simple-entity-with-owner`; hidden functional entities do the work behind it.

**Why it's dead:** `simple-entity-with-owner` supports neither `fluid_box` nor `circuit_connector` — the shell can't be piped, wired, or given the interactions players expect from the machine they're clicking.

**Use instead:** make the shell a *real* functional prototype for whatever the shell itself must expose (e.g. a `storage-tank` shell provides fluid box + circuit connector + GUI anchor), and hide only the members the player never touches.

---

## Data-stage cooldown on a circuit-detonated land mine

**The idea:** a land mine used as a circuit-condition→`on_script_trigger_effect` bridge (patterns.md) re-fires every tick while the condition holds; throttle it in the data stage — via `trigger_interval`, `timeout`, or by wrapping its `action` effect in `TriggerEffectWithCooldown`.

**Why it's dead (each verified 2.1.10):**
1. `trigger_interval` governs only the *enemy-proximity* detonation scan; `timeout` governs only *initial post-placement* arming. Neither affects circuit re-detonation — both tested at 600 ticks, still one detonation per tick.
2. `TriggerEffectWithCooldown` is not in the `TriggerEffect` union; it's accepted only in `SegmentPrototype.update_effects[/_while_enraged]` and `StickerPrototype.update_effects[]`, so it can't sit in the mine's `action` (constraints.md § Triggers).

**Use instead:** pulse the input signal upstream (circuit edge-conditioning so the condition is true for exactly one tick per real event). A Lua-side debounce works but still pays the Lua↔engine boundary crossing every tick, defeating the point of a push bridge.

---

## Treating fluid `add_fluid`/`remove_fluid`/`set_fluid` as `(fluid, index)`

**The idea:** pass the fluid table first because it's the "important" argument.

**Why it's dead:** index is parameter 0 on all of them; passing the table first crashes at runtime ("'index': real number expected got table"). Listed here because it recurs — the alphabetized `parameters` array in runtime-api.json misleads; read each parameter's `order` field.
