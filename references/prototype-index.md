# Factorio 2.x Prototype Index

Generated from prototype-api.json (api_version 6, game 2.1.9).
Entries marked **[NO DESC]** have blank descriptions in the API - fill these in manually.
Grouped by ancestry. 'Other' holds everything without an Entity/Item/Equipment/Tile/Achievement ancestor: recipes, technologies, fluids, categories, settings, visuals, utility prototypes.

## Contents

- [Entities](#entities) (147)
- [Items](#items) (21)
- [Equipment](#equipment) (13)
- [Tiles](#tiles) (1)
- [Achievements](#achievements) (32)
- [Other](#other) (65)

## Entities

| Prototype class | typename | Description |
|---|---|---|
| AccumulatorPrototype | accumulator | Entity with energy source with specialised animation for charging/discharging |
| AgriculturalTowerPrototype | agricultural-tower | **[NO DESC]** |
| AmmoTurretPrototype | ammo-turret | A turret that consumes ammo items |
| ArithmeticCombinatorPrototype | arithmetic-combinator | An arithmetic combinator |
| ArrowPrototype | arrow | The arrows used for example in the campaign, they are literally just arrows |
| ArtilleryFlarePrototype | artillery-flare | The entity spawned by the artillery targeting remote |
| ArtilleryProjectilePrototype | artillery-projectile | The projectile shot by artillery |
| ArtilleryTurretPrototype | artillery-turret | An artillery turret |
| ArtilleryWagonPrototype | artillery-wagon | An artillery wagon |
| AssemblingMachinePrototype | assembling-machine | An assembling machine - like the assembling machines 1/2/3 in the game, but you can use your own recipe categories |
| AsteroidCollectorPrototype | asteroid-collector | **[NO DESC]** |
| AsteroidPrototype | asteroid | **[NO DESC]** |
| BeaconPrototype | beacon | Entity with the ability to transfer module effects to its neighboring entities |
| BeamPrototype | beam | Used as a laser beam |
| BoilerPrototype | boiler | A boiler |
| BurnerGeneratorPrototype | burner-generator | An entity that produces power from a burner energy source |
| CaptureRobotPrototype | capture-robot | **[NO DESC]** |
| CarPrototype | car | Entity with specialized properties for acceleration, braking, and turning |
| CargoBayPrototype | cargo-bay | **[NO DESC]** |
| CargoLandingPadPrototype | cargo-landing-pad | **[NO DESC]** |
| CargoPodPrototype | cargo-pod | **[NO DESC]** |
| CargoWagonPrototype | cargo-wagon | A cargo wagon |
| CharacterCorpsePrototype | character-corpse | The corpse of a CharacterPrototype |
| CharacterPrototype | character | Entity that you move around on the screen during the campaign and freeplay |
| CliffPrototype | cliff | A cliff |
| CombatRobotPrototype | combat-robot | A combat robot |
| CombinatorPrototype *(abstract)* | *(abstract)* | Abstract base type for decider and arithmetic combinators |
| ConstantCombinatorPrototype | constant-combinator | A constant combinator |
| ConstructionRobotPrototype | construction-robot | A construction robot |
| ContainerPrototype | container | A generic container, such as a chest |
| CorpsePrototype | corpse | Used for corpses, for example the remnants when destroying buildings |
| CraftingMachinePrototype *(abstract)* | *(abstract)* | The abstract basis of the assembling machines and furnaces |
| CurvedRailAPrototype | curved-rail-a | A curved-A rail |
| CurvedRailBPrototype | curved-rail-b | A curved-B rail |
| DeciderCombinatorPrototype | decider-combinator | A decider combinator |
| DeconstructibleTileProxyPrototype | deconstructible-tile-proxy | Entity used to signify that the tile below it should be deconstructed |
| DisplayPanelPrototype | display-panel | Entity that display a signal icon and some text, either configured directly in the entity or through the circuit network |
| ElectricEnergyInterfacePrototype | electric-energy-interface | Entity with electric energy source with that can have some of its values changed runtime |
| ElectricPolePrototype | electric-pole | An electric pole - part of the electric system |
| ElectricTurretPrototype | electric-turret | A turret that uses electricity as ammunition |
| ElevatedCurvedRailAPrototype | elevated-curved-rail-a | An elevated curved-A rail |
| ElevatedCurvedRailBPrototype | elevated-curved-rail-b | An elevated curved-B rail |
| ElevatedHalfDiagonalRailPrototype | elevated-half-diagonal-rail | An elevated half diagonal rail |
| ElevatedStraightRailPrototype | elevated-straight-rail | An elevated straight rail |
| EnemySpawnerPrototype | unit-spawner | Can spawn entities |
| EntityGhostPrototype | entity-ghost | The entity used for ghosts of entities |
| EntityPrototype *(abstract)* | *(abstract)* | Abstract base of all entities in the game |
| EntityWithHealthPrototype *(abstract)* | *(abstract)* | Abstract base of all entities with health in the game |
| EntityWithOwnerPrototype *(abstract)* | *(abstract)* | Abstract base of all entities with a force in the game |
| ExplosionPrototype | explosion | Used to play an animation and a sound |
| FireFlamePrototype | fire | A fire |
| FishPrototype | fish | Entity that spawns in water tiles, which can be mined |
| FluidStreamPrototype | stream | Used for example for the handheld flamethrower |
| FluidTurretPrototype | fluid-turret | A turret that uses fluid as ammunition |
| FluidWagonPrototype | fluid-wagon | A fluid wagon |
| FlyingRobotPrototype *(abstract)* | *(abstract)* | Abstract base for construction/logistics and combat robots |
| FurnacePrototype | furnace | A furnace |
| FusionGeneratorPrototype | fusion-generator | Consumes a fluid to generate electricity and create another fluid |
| FusionReactorPrototype | fusion-reactor | Fusion reactor |
| GatePrototype | gate | A gate |
| GeneratorPrototype | generator | An entity that produces power from fluids, for example a steam engine |
| HalfDiagonalRailPrototype | half-diagonal-rail | A half diagonal rail |
| HeatInterfacePrototype | heat-interface | This entity produces or consumes heat |
| HeatPipePrototype | heat-pipe | A heat pipe |
| HighlightBoxEntityPrototype | highlight-box | Used to attach graphics for cursor boxes to entities during runtime |
| InfinityCargoWagonPrototype | infinity-cargo-wagon | A cargo wagon that can spawn or void items at will |
| InfinityContainerPrototype | infinity-container | A generic container, such as a chest, that can spawn or void items and interact with the logistics network |
| InfinityPipePrototype | infinity-pipe | This entity produces or consumes fluids |
| InserterPrototype | inserter | An inserter |
| ItemEntityPrototype | item-entity | The entity used for items on the ground |
| ItemRequestProxyPrototype | item-request-proxy | Entity used to signify that an entity is requesting items, for example modules for an assembling machine after it was blueprinted with modules inside |
| LabPrototype | lab | A lab |
| LampPrototype | lamp | A lamp to provide light, using energy |
| LandMinePrototype | land-mine | A land mine |
| LaneSplitterPrototype | lane-splitter | **[NO DESC]** |
| LegacyCurvedRailPrototype | legacy-curved-rail | A legacy curved rail |
| LegacyStraightRailPrototype | legacy-straight-rail | A legacy straight rail |
| LightningAttractorPrototype | lightning-attractor | Absorbs lightning and optionally converts it into electricity |
| LightningPrototype | lightning | Lightning randomly hits entities on planets with lightning_properties |
| LinkedBeltPrototype | linked-belt | A belt that can be connected to a belt anywhere else, including on a different surface |
| LinkedContainerPrototype | linked-container | A container that shares its inventory with containers with the same link_id, which can be set via the GUI |
| Loader1x1Prototype | loader-1x1 | Continuously loads and unloads machines, as an alternative to inserters |
| Loader1x2Prototype | loader | Continuously loads and unloads machines, as an alternative to inserters |
| LoaderPrototype *(abstract)* | *(abstract)* | Continuously loads and unloads machines, as an alternative to inserters |
| LocomotivePrototype | locomotive | A locomotive |
| LogisticContainerPrototype | logistic-container | A generic container, such as a chest, that interacts with the logistics network |
| LogisticRobotPrototype | logistic-robot | A logistic robot |
| MarketPrototype | market | Offers can be added to a market and they are shown when opening the entity |
| MiningDrillPrototype | mining-drill | A mining drill for automatically extracting resources from resource entities |
| OffshorePumpPrototype | offshore-pump | An offshore pump |
| ParticleSourcePrototype | particle-source | Creates particles |
| PipePrototype | pipe | An entity to transport fluids over a distance and between machines |
| PipeToGroundPrototype | pipe-to-ground | A pipe to ground |
| PlantPrototype | plant | **[NO DESC]** |
| PlayerPortPrototype | player-port | Deprecated in 2 |
| PowerSwitchPrototype | power-switch | A power switch |
| ProgrammableSpeakerPrototype | programmable-speaker | A programmable speaker |
| ProjectilePrototype | projectile | Entity with limited lifetime that can hit other entities and has triggers when this happens |
| ProxyContainerPrototype | proxy-container | A container that must be set to point at other entity and inventory index so it can forward all inventory interactions to the other entity |
| PumpPrototype | pump | The pump is used to transfer fluids between tanks, fluid wagons and pipes |
| RadarPrototype | radar | A radar |
| RailChainSignalPrototype | rail-chain-signal | A rail chain signal |
| RailPrototype *(abstract)* | *(abstract)* | The abstract base of all rail prototypes |
| RailRampPrototype | rail-ramp | A rail ramp |
| RailRemnantsPrototype | rail-remnants | Used for rail corpses |
| RailSignalBasePrototype *(abstract)* | *(abstract)* | The abstract base entity for both rail signals |
| RailSignalPrototype | rail-signal | A rail signal |
| RailSupportPrototype | rail-support | **[NO DESC]** |
| ReactorPrototype | reactor | A reactor |
| ResourceEntityPrototype | resource | A mineable/gatherable entity |
| RoboportPrototype | roboport | A roboport |
| RobotWithLogisticInterfacePrototype *(abstract)* | *(abstract)* | The common properties of logistic and construction robots represented by an abstract prototype |
| RocketSiloPrototype | rocket-silo | A rocket silo |
| RocketSiloRocketPrototype | rocket-silo-rocket | The rocket inside the rocket silo |
| RocketSiloRocketShadowPrototype | rocket-silo-rocket-shadow | The shadow of the rocket inside the rocket silo |
| RollingStockPrototype *(abstract)* | *(abstract)* | The abstract base of all rolling stock |
| SegmentPrototype | segment | Entity representing an individual segment in a SegmentedUnitPrototype |
| SegmentedUnitPrototype | segmented-unit | Entity composed of multiple segment entities that trail behind the head |
| SelectorCombinatorPrototype | selector-combinator | **[NO DESC]** |
| SimpleEntityPrototype | simple-entity | An extremely basic entity with no special functionality |
| SimpleEntityWithForcePrototype | simple-entity-with-force | By default, this entity will be a priority target for units/turrets, who will choose to attack it even if it does not block their path |
| SimpleEntityWithOwnerPrototype | simple-entity-with-owner | Has a force, but unlike SimpleEntityWithForcePrototype it is only attacked if the biters get stuck on it (or if EntityWithOwnerPrototype::is_military_target set to true to make the two entity types equivalent) |
| SmokePrototype *(abstract)* | *(abstract)* | Abstract entity that has an animation |
| SmokeWithTriggerPrototype | smoke-with-trigger | An entity with animation and a trigger |
| SolarPanelPrototype | solar-panel | A solar panel |
| SpacePlatformHubPrototype | space-platform-hub | **[NO DESC]** |
| SpeechBubblePrototype | speech-bubble | A speech bubble |
| SpiderLegPrototype | spider-leg | Used by SpiderLegSpecification for SpiderVehiclePrototype, also known as spidertron |
| SpiderUnitPrototype | spider-unit | **[NO DESC]** |
| SpiderVehiclePrototype | spider-vehicle | A spidertron |
| SplitterPrototype | splitter | A splitter |
| StickerPrototype | sticker | Entity that sticks to another entity, and damages/slows it |
| StorageTankPrototype | storage-tank | A storage tank |
| StraightRailPrototype | straight-rail | A straight rail |
| TemporaryContainerPrototype | temporary-container | A container that can automatically destroy itself when it is emptied or after it has existed for a certain time |
| ThrusterPrototype | thruster | Consumes two fluids as fuel to produce thrust for a space platform |
| TileGhostPrototype | tile-ghost | The entity used for tile ghosts |
| TrainStopPrototype | train-stop | A train stop |
| TransportBeltConnectablePrototype *(abstract)* | *(abstract)* | Abstract class that anything that is a belt or can connect to belts uses |
| TransportBeltPrototype | transport-belt | A transport belt |
| TreePrototype | tree | A tree |
| TurretPrototype | turret | A turret that needs no extra ammunition |
| UndergroundBeltPrototype | underground-belt | An underground belt |
| UnitPrototype | unit | Entity that moves around and attacks players, for example biters and spitters |
| ValvePrototype | valve | A passive device that provides limited control of fluid flow between pipelines |
| VehiclePrototype *(abstract)* | *(abstract)* | Abstract base of all vehicles |
| WallPrototype | wall | A wall |

## Items

| Prototype class | typename | Description |
|---|---|---|
| AmmoItemPrototype | ammo | Ammo used for a gun |
| ArmorPrototype | armor | Armor to wear on your in-game character for defense and buffs |
| BlueprintBookPrototype | blueprint-book | A blueprint book |
| BlueprintItemPrototype | blueprint | A blueprint |
| CapsulePrototype | capsule | A capsule, for example a combat robot capsule or the raw fish |
| CopyPasteToolPrototype | copy-paste-tool | A copy-paste or cut-paste tool |
| DeconstructionItemPrototype | deconstruction-item | A deconstruction planner |
| GunPrototype | gun | A gun |
| ItemPrototype | item | Possible configuration for all items |
| ItemWithEntityDataPrototype | item-with-entity-data | ItemWithEntityData saves data associated with the entity that it represents, for example the content of the equipment grid of a car |
| ItemWithInventoryPrototype | item-with-inventory | The inventory allows setting player defined filters similar to cargo wagon inventories |
| ItemWithLabelPrototype | item-with-label | Like a normal item but with the ability to have a colored label |
| ItemWithTagsPrototype | item-with-tags | Item type that can store any basic arbitrary Lua data, see LuaItemStack::tags |
| ModulePrototype | module | A module |
| RailPlannerPrototype | rail-planner | A rail planner |
| RepairToolPrototype | repair-tool | A repair pack |
| SelectionToolPrototype | selection-tool | Used in the base game as a base for the blueprint item and the deconstruction item |
| SpacePlatformStarterPackPrototype | space-platform-starter-pack | **[NO DESC]** |
| SpidertronRemotePrototype | spidertron-remote | The spidertron remote |
| ToolPrototype | tool | Items with a "durability" |
| UpgradeItemPrototype | upgrade-item | An upgrade planner |

## Equipment

| Prototype class | typename | Description |
|---|---|---|
| ActiveDefenseEquipmentPrototype | active-defense-equipment | Used by discharge defense and personal laser defense |
| BatteryEquipmentPrototype | battery-equipment | Used by personal battery |
| BeltImmunityEquipmentPrototype | belt-immunity-equipment | Used by belt immunity equipment |
| ElectricEnergyInterfaceEquipmentPrototype | electric-energy-interface-equipment | Provides or consumes power in equipment grids |
| EnergyShieldEquipmentPrototype | energy-shield-equipment | Used by energy shield |
| EquipmentGhostPrototype | equipment-ghost | The equipment used for ghosts of equipment |
| EquipmentPrototype *(abstract)* | *(abstract)* | Abstract base of all equipment modules |
| GeneratorEquipmentPrototype | generator-equipment | Used by portable fusion reactor |
| InventoryBonusEquipmentPrototype | inventory-bonus-equipment | **[NO DESC]** |
| MovementBonusEquipmentPrototype | movement-bonus-equipment | Used by exoskeleton |
| NightVisionEquipmentPrototype | night-vision-equipment | Used by nightvision |
| RoboportEquipmentPrototype | roboport-equipment | Used by personal roboport |
| SolarPanelEquipmentPrototype | solar-panel-equipment | A portable solar panel |

## Tiles

| Prototype class | typename | Description |
|---|---|---|
| TilePrototype | tile | A tile |

## Achievements

| Prototype class | typename | Description |
|---|---|---|
| AchievementPrototype | achievement | This prototype definition is used for the in-game achievements |
| AchievementPrototypeWithCondition *(abstract)* | *(abstract)* | **[NO DESC]** |
| BuildEntityAchievementPrototype | build-entity-achievement | This prototype is used for receiving an achievement when the player builds an entity |
| ChangedSurfaceAchievementPrototype | change-surface-achievement | This prototype is used for receiving an achievement when the player changes to a surface |
| CombatRobotCountAchievementPrototype | combat-robot-count-achievement | This prototype is used for receiving an achievement when the player has a certain robot follower count |
| CompleteObjectiveAchievementPrototype | complete-objective-achievement | **[NO DESC]** |
| ConstructWithRobotsAchievementPrototype | construct-with-robots-achievement | This prototype is used for receiving an achievement when the player constructs enough entities with construction robots |
| CreatePlatformAchievementPrototype | create-platform-achievement | This prototype is used for receiving an achievement when the player creates a space platform |
| DeconstructWithRobotsAchievementPrototype | deconstruct-with-robots-achievement | This prototype is used for receiving an achievement when the player deconstructs enough entities with construction robots |
| DeliverByRobotsAchievementPrototype | deliver-by-robots-achievement | This prototype is used for receiving an achievement, when the player requests and receives enough items using logistic robots |
| DepleteResourceAchievementPrototype | deplete-resource-achievement | This prototype is used for receiving an achievement when a resource entity is depleted |
| DestroyCliffAchievementPrototype | destroy-cliff-achievement | **[NO DESC]** |
| DontBuildEntityAchievementPrototype | dont-build-entity-achievement | This prototype is used for receiving an achievement when the player finishes the game without building a specific entity |
| DontCraftManuallyAchievementPrototype | dont-craft-manually-achievement | This prototype is used for receiving an achievement when the player finishes the game without crafting more than a set amount |
| DontKillManuallyAchievementPrototype | dont-kill-manually-achievement | This prototype is used for receiving an achievement when the player kill first entity using artillery |
| DontResearchBeforeResearchingAchievementPrototype | dont-research-before-researching-achievement | This prototype is used for receiving an achievement when the player researches with a specific science pack before unlocking another |
| DontUseEntityInEnergyProductionAchievementPrototype | dont-use-entity-in-energy-production-achievement | This prototype is used for receiving an achievement when the player finishes the game without receiving energy from a specific energy source |
| EquipArmorAchievementPrototype | equip-armor-achievement | This prototype is used for receiving an achievement when the player equips armor |
| GroupAttackAchievementPrototype | group-attack-achievement | This prototype is used for receiving an achievement when the player gets attacked due to pollution |
| KillAchievementPrototype | kill-achievement | This prototype is used for receiving an achievement when the player destroys a certain amount of an entity, with a specific damage type |
| ModuleTransferAchievementPrototype | module-transfer-achievement | This prototype is used for receiving an achievement when the player moves a module with the cursor |
| PlaceEquipmentAchievementPrototype | place-equipment-achievement | **[NO DESC]** |
| PlayerDamagedAchievementPrototype | player-damaged-achievement | This prototype is used for receiving an achievement when the player receives damage |
| ProduceAchievementPrototype | produce-achievement | This prototype is used for receiving an achievement when the player produces more than the specified amount of items |
| ProducePerHourAchievementPrototype | produce-per-hour-achievement | This prototype is used for receiving an achievement when the player crafts a specified item a certain amount, in an hour |
| ResearchAchievementPrototype | research-achievement | This prototype is used for receiving an achievement when the player completes a specific research |
| ResearchWithSciencePackAchievementPrototype | research-with-science-pack-achievement | **[NO DESC]** |
| ShootAchievementPrototype | shoot-achievement | This prototype is used for receiving an achievement when the player shoots certain ammo |
| SpaceConnectionDistanceTraveledAchievementPrototype | space-connection-distance-traveled-achievement | **[NO DESC]** |
| TrainPathAchievementPrototype | train-path-achievement | This prototype is used for receiving an achievement when the player has a specified train path length |
| UseEntityInEnergyProductionAchievementPrototype | use-entity-in-energy-production-achievement | This prototype is used for receiving an achievement when the player produces energy by entity |
| UseItemAchievementPrototype | use-item-achievement | This prototype is used for receiving an achievement when the player uses a capsule |

## Other

| Prototype class | typename | Description |
|---|---|---|
| ActiveTriggerPrototype *(abstract)* | *(abstract)* | The abstract base of all active trigger prototypes |
| AirbornePollutantPrototype | airborne-pollutant | A type of pollution that can spread throughout the chunks of a map |
| AmbientSound | ambient-sound | This prototype is used to make sound while playing the game |
| AmmoCategory | ammo-category | An ammo category |
| AnimationPrototype | animation | Specifies an animation that can be used with LuaRendering::draw_animation at runtime |
| AsteroidChunkPrototype | asteroid-chunk | **[NO DESC]** |
| AutoplaceControl | autoplace-control | A setting in the map creation GUI |
| BurnerUsagePrototype | burner-usage | Set of data affecting tooltips, looks of gui slots etc when burner is not supposed to be burning items but eating them |
| ChainActiveTriggerPrototype | chain-active-trigger | Jumps between targets and applies a Trigger to them |
| CollisionLayerPrototype | collision-layer | A collision layer |
| CustomEventPrototype | custom-event | Custom events share the same namespace as custom inputs and built-in events for subscribing to and raising them |
| CustomInputPrototype | custom-input | Used for custom keyboard shortcuts/key bindings in mods |
| DamageType | damage-type | A damage type |
| DecorativePrototype | optimized-decorative | Simple decorative purpose objects on the map, they have no health and some of them are removed when the player builds over |
| DelayedActiveTriggerPrototype | delayed-active-trigger | Delays the delivery of triggered effect by some number of ticks |
| DeliverCategory | deliver-category | **[NO DESC]** |
| DeliverImpactCombination | deliver-impact-combination | **[NO DESC]** |
| EditorControllerPrototype | editor-controller | Properties of the editor controller |
| EquipmentCategory | equipment-category | Defines a category to be available to equipment and equipment grids |
| EquipmentGridPrototype | equipment-grid | The prototype of an equipment grid, for example the one used in a power armor |
| FluidPrototype | fluid | A fluid |
| FontPrototype | font | Fonts are used in all GUIs in the game |
| FuelCategory | fuel-category | Each item which has a fuel_value must have a fuel category |
| GodControllerPrototype | god-controller | Properties of the god controller |
| GuiStyle | gui-style | The available GUI styles |
| ImpactCategory | impact-category | **[NO DESC]** |
| ItemGroup | item-group | An item group |
| ItemSubGroup | item-subgroup | An item subgroup |
| MapGenPresets | map-gen-presets | The available map gen presets |
| MapSettings | map-settings | The default map settings |
| ModData | mod-data | Block of arbitrary data set by mods in prototype stage |
| ModuleCategory | module-category | A module category |
| MouseCursor | mouse-cursor | Used by SelectionToolPrototype::mouse_cursor |
| NamedNoiseExpression | noise-expression | A NoiseExpression with a name |
| NamedNoiseFunction | noise-function | Named noise functions are defined in the same way as NamedNoiseExpression except that they also have parameters |
| ParticlePrototype | optimized-particle | An entity with a limited lifetime that can use trigger effects |
| PlanetPrototype | planet | **[NO DESC]** |
| ProcessionLayerInheritanceGroup | procession-layer-inheritance-group | Helps ProcessionLayers pass properties between subsequent transitions if they belong to the same group |
| ProcessionPrototype | procession | Describes the duration and visuals of a departure, arrival or an intermezzo while traveling between surfaces |
| Prototype *(abstract)* | *(abstract)* | **[NO DESC]** |
| PrototypeBase *(abstract)* | *(abstract)* | The abstract base for prototypes |
| QualityPrototype | quality | One quality step |
| RecipeCategory | recipe-category | A recipe category |
| RecipePrototype | recipe | A recipe |
| RemoteControllerPrototype | remote-controller | Properties of the remote controller |
| ResourceCategory | resource-category | A resource category |
| ShortcutPrototype | shortcut | Definition for a shortcut button in the shortcut bar |
| SoundPrototype | sound | Specifies a sound that can be used with SoundPath at runtime |
| SpaceConnectionPrototype | space-connection | **[NO DESC]** |
| SpaceLocationPrototype | space-location | A space location, such as a planet or the solar system edge |
| SpectatorControllerPrototype | spectator-controller | Properties of the spectator controller |
| SpritePrototype | sprite | Specifies an image that can be used with SpritePath at runtime |
| SurfacePropertyPrototype | surface-property | **[NO DESC]** |
| SurfacePrototype | surface | **[NO DESC]** |
| TechnologyPrototype | technology | A technology |
| TileEffectDefinition | tile-effect | Used to define the parameters for tile shaders |
| TipsAndTricksItem | tips-and-tricks-item | A tips and tricks entry |
| TipsAndTricksItemCategory | tips-and-tricks-item-category | A TipsAndTricksItem category, used for sorting of tips and tricks entries: Tips and trick entries are sorted first by category and then by their order within that category |
| TriggerTargetType | trigger-target-type | The base game always internally defines a "common" trigger target type |
| TrivialSmokePrototype | trivial-smoke | Smoke, but it's not an entity for optimization purposes |
| TutorialDefinition | tutorial | The definition of the tutorial to be used in the tips and tricks, see TipsAndTricksItem |
| UtilityConstants | utility-constants | Constants used by the game that are not specific to certain prototypes |
| UtilitySounds | utility-sounds | Sounds used by the game that are not specific to certain prototypes |
| UtilitySprites | utility-sprites | Sprites used by the game that are not specific to certain prototypes |
| VirtualSignalPrototype | virtual-signal | A virtual signal |

---
*Abstract prototypes are base types only - not used directly in data:extend.*
