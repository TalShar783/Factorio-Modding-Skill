# Space Platforms — Verified Mechanics & APIs

Space platforms are not planet surfaces. Do not carry surface assumptions onto them.

## What does NOT exist on platforms

- **No logistic network at all**: no roboports, no construction/logistic robots, no logistic chests.
- **No vanilla chests**: Space Age data-updates adds `surface_conditions = { { property = "gravity", min = 0.1 } }` to every vanilla container. Any custom container meant for platforms must explicitly allow gravity 0 (and copies of vanilla containers made in `data.lua` must set `surface_conditions` themselves — see constraints.md § deepcopy timing).
- **No rockets/cargo pods between two platforms**: pods travel platform ↔ planet surface only.

## How platform inventory works

- The `space-platform-hub` entity holds the platform's shared cargo inventory; inserters push/pull against it directly.
- Machines and inserters with "enable logistic connection" read the hub's contents wirelessly (the hub replaces the logistic network as the readable inventory).
- Script access (both verified):
  - `platform.hub` — `LuaSpacePlatform` attribute returning the hub entity (runtime-api.json).
  - `surface.find_entities_filtered({ type = "space-platform-hub" })[1]` — equivalent, production-tested.
  - Hub inventory: `hub.get_inventory(defines.inventory.hub_main)` (`hub_trash` also exists).
- `LuaSpacePlatform` has **no** `cargo_inventory` attribute — accessing it throws (C++ objects throw on unknown keys).

## Platform-to-platform transfer (2.1)

Platforms in orbit of the same body can request items from each other via the orbital request system. This is the **only** platform-to-platform mechanism — no rockets or pods involved.

## Non-landable space locations

`space-location` prototypes (Shattered Planet style) have no surface: no landing, no building, no cargo rockets. Platforms park there and interact with the location's asteroid/resource mechanics from orbit.

## Gravity & platform travel (`gravity_pull`)

`gravity_pull` (double; on `SpaceLocationPrototype`/`PlanetPrototype`; data-stage, read-only at runtime; default 0) is a **flat modifier on platform travel speed**, in the same units as the platform speed readout. Vanilla values: planets `+10`, solar-system-edge and shattered-planet `−10`. The underlying per-tick acceleration lives in `utility-constants.lua` (`space_platform_acceleration_expression`), but `gravity_pull` itself is applied in C++. Behavior below is **verified in-game (2.1)** with a 50-pull origin (Nauvis) and a 500-pull destination:

- **Only the nearest body's pull is active, switched at the connection midpoint — not a distance gradient.** On the origin half of a connection the origin's `gravity_pull` applies; past the midpoint the destination's applies. Within a half it does **not** vary with distance — it is all-or-nothing at the midpoint (confirmed: exactly 50 until midpoint, then exactly 500).
- **Sign:** the active pull is **subtracted** when thrusting *away* from that body and **added** when moving *toward* it. Net travel speed ≈ thrust-speed ± gravity_pull(nearest body).
- **Coasting (thrust off or insufficient) settles at a speed equal to the nearest body's `gravity_pull`, directed toward that body** — the platform physically drifts **backward** toward it (a platform coasting on Nauvis's half capped at −50).
- **Leaving a location requires thrust-speed to exceed that location's `gravity_pull`.** Below the threshold the platform stays in the parked/`in orbit` state even while thrusting, and the displayed speed climbs toward the threshold. Only when thrust-speed crosses `gravity_pull` does it flip to `in transit`, at which point net travel speed drops to (thrust-speed − gravity_pull) — e.g. ~5 when thrusting ~505 against a 500 pull.
- **Thrust depends only on the thrusters** (fuel/oxidizer throughput and count); it is independent of travel direction or which body's gravity is acting.
- **A backward-drifting platform travels physically backward**, so asteroids approach from the platform's rear (observed). Forcing a constant "face the destination" pose in transit is unresolved: `LuaSpacePlatform` exposes no `orientation` attribute, and `SpaceLocationPrototype.parked_platforms_orientation` is named for and applies to the *parked* pose only.
- **`gravity_pull` is a property of the location, not the route.** `SpaceConnectionPrototype` has no gravity field, so a location's pull applies uniformly to every connection touching it — it cannot be set per route natively. (`SpaceConnectionPrototype.length` *is* per-connection, so routes to the same body can differ in travel distance independently of gravity.) Per-route or graded gravity therefore requires scripting.

Design lever: to trap under-thrusted platforms, set a location's `gravity_pull` above the platform's maximum achievable thrust-speed — it can never cross the departure threshold, and coasting drags it back in. `gravity_pull` is a single flat scalar per location, so there is no native "event horizon at distance X"; the only distance effect is the midpoint hand-off between the two endpoints' pulls.

## Space routes & runtime travel levers

A platform travels a `space-connection` (`from`/`to` are `SpaceLocationID`s; `length` is per-connection). Position and motion are script-controllable — the levers below are what a custom route/gravity model manipulates:

- `LuaSpacePlatform.distance` **[RW]** — position along the current connection: `0` = `from`, `1` = `to`; `nil` when not in transit.
- `LuaSpacePlatform.speed` **[RW]** — **a progress rate toward the platform's currently *scheduled* stop, NOT a signed velocity along the connection's from→to axis** (verified 2.1.9: a platform scheduled to the `from` end with positive speed moves `distance` *downward*). Adding to speed always boosts the ship along its own travel direction, whichever way that is; read the travel direction from the schedule (`platform.schedule.records[platform.schedule.current].station`), never from the sign of speed or from `distance` jitter. Scripted-write behaviour (verified 2.1.9 by before/after instrumentation, platform under full thrust):
  - **Positive writes persist** across ticks, decaying by the engine's quadratic drag (~5e-4·speed² per tick observed) and composing with thrust.
  - **Negative writes are floored to 0** while the platform is thrusting: write −3.44, next tick the engine has reset speed to exactly 0.0000 and `distance` is bit-for-bit frozen. A script can therefore slow and **stall** a platform via speed subtraction, but can never drive it backward this way — backward motion must be expressed by writing `distance` directly. (The engine itself *can* move platforms at negative speed — vanilla `gravity_pull` coasting drift — but that path isn't reachable through speed writes under thrust.)
  - Scale for tuning: engine thrust acceleration observed at roughly ~0.06 speed/tick (8 thrusters, full thrust); scripted per-tick pulls should be sized against that, not against travel speeds.
  - Calibration: distance advances ≈ 3.3e-5 per tick per unit of speed (route length 15000).
- `LuaSpacePlatform.schedule` **[RW]**; writing `space_connection` places the platform mid-route (**sets `distance` to 0.5**); writing `space_location` parks it (**cancels pending item requests**).
- `LuaSpacePlatform.state` **[R]** = `defines.space_platform_state`: `on_the_path` (in transit), `waiting_at_station`, `waiting_for_departure`, `no_path`, `no_schedule`, `paused`, `starter_pack_requested`/`_on_the_way`, `waiting_for_starter_pack`. Filter on `on_the_path` to find actively-travelling platforms.
- Enumerate a force's platforms via `LuaForce.platforms`; remove one with `platform.destroy(ticks)` (delay in ticks from now).
- **`destroy()` is silently refused while a character is on the platform surface** (verified 2.1.9: `scheduled_for_deletion` reads 0 immediately after the call, no error, retried 10× over 600 ticks). Teleport every character off first; the same call then succeeds instantly (`scheduled_for_deletion`=ticks, platform invalid after the countdown). Being **in transit does NOT block deletion** — a platform deletes fine at `state = on_the_path`. Always verify a destroy took by reading `scheduled_for_deletion ~= 0` right after the call.
- **Moving a player off a platform: teleport the CHARACTER ENTITY, not the player.** `player.teleport()` while the player is in remote view moves only the view controller (verified: 10 attempts, `physical_surface` never changed), and `exit_remote_view()` + `player.teleport()` in the same tick also fails to move the character. What works: `player.character.teleport(position, surface)` — character entities teleport cross-surface and the call returns success (verified true, `physical_surface` updated same tick). Check aboard-ness via `player.physical_surface` (not `player.surface`, which follows the view).

Because `distance` and `speed` are both writable, a custom gravity model (graded/proximity-scaled pull, per-route curves, a research-dependent point-of-no-return, "fall in → destroy") is cheap: read/modify one field per in-transit platform per tick. Track the affected platforms via `on_space_platform_changed_state` (maintain a `storage` set) rather than rescanning `LuaForce.platforms` every tick.

## LuaSpacePlatform (verified member list, 2.1.8)

- Attributes: `damaged_tiles`, `distance`, `ejected_items`, `force`, `hidden`, `hub`, `index`, `last_visited_space_location`, `name`, `paused`, `schedule`, `scheduled_for_deletion`, `space_connection`, `space_location`, `speed`, `starter_pack`, `state`, `surface`, `valid`, `weight`
- Methods: `apply_starter_pack`, `can_leave_current_location`, `cancel_deletion`, `clear_ejected_items`, `create_asteroid_chunks`, `damage_tile`, `destroy`, `destroy_asteroid_chunks`, `eject_item`, `find_asteroid_chunks_filtered`, `get_schedule`, `repair_tile`
- **`scheduled_for_deletion` is a `uint32` MapTick, NOT a boolean** (`0` = not scheduled; a positive value is the tick deletion occurs). Since `0` is truthy in Lua, `if platform.scheduled_for_deletion then …` is **always true** and silently bails on every platform — test `platform.scheduled_for_deletion ~= 0` (or `> 0`). `platform.destroy(ticks)` sets it; `cancel_deletion()` clears it. General caution (cost a full debug session to find): Factorio C++ attributes that read like booleans are often numeric/tick-valued — check the API type; never rely on Lua truthiness for engine-returned numbers.
- Note the **runtime asteroid-chunk APIs**: `create_asteroid_chunks` / `find_asteroid_chunks_filtered` / `destroy_asteroid_chunks` — asteroid manipulation at runtime does not require data-stage spawn definitions.
  - `create_asteroid_chunks` takes an array of `AsteroidChunk` = `{ name = string, position = MapPosition, movement = Vector }` (all required). Because both spawn `position` and the `movement` velocity vector are script-set, **asteroid approach direction can be fully decoupled from the platform's travel velocity** — the native spawner ties approach direction to velocity sign, but scripted spawns do not. To use scripted approach vectors, suppress native spawns on that connection (empty `asteroid_spawn_definitions`) so the two don't mix. `find_asteroid_chunks_filtered` returns the same `{name, position, movement}` shape, so existing chunks' vectors can be read (and redirected via destroy+recreate).

## Platform events (verified list, runtime-api.json 2.1.8)

`on_space_platform_built_entity` (entity, platform, stack, tags), `on_space_platform_built_tile`, `on_space_platform_changed_state` (platform, old_state), `on_space_platform_mined_entity` (buffer, entity, platform — buffer valid this tick only), `on_space_platform_mined_item`, `on_space_platform_mined_tile`, `on_space_platform_pre_mined`.

Remember platforms build and mine things **without** a player or robot: any `on_built_entity`/`on_robot_built_entity` handler pair needs the `on_space_platform_built_entity` sibling (and likewise for mining) or platform actions are silently missed.

Cargo pod events for surface ↔ platform transfer: `on_cargo_pod_started_ascending`, `on_cargo_pod_finished_ascending`, `on_cargo_pod_finished_descending`, `on_cargo_pod_delivered_cargo` (spawned_container).
