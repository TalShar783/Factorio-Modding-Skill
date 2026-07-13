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

## Treating fluid `add_fluid`/`remove_fluid`/`set_fluid` as `(fluid, index)`

**The idea:** pass the fluid table first because it's the "important" argument.

**Why it's dead:** index is parameter 0 on all of them; passing the table first crashes at runtime ("'index': real number expected got table"). Listed here because it recurs — the alphabetized `parameters` array in runtime-api.json misleads; read each parameter's `order` field.
