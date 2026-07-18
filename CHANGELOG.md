# Changelog

## 0.9.2 - 2026-07-18

### Added
- Consolidated demo session construction around the existing create_demo_content() and create_game_session() composition path.
- Updated session reset, application, and content-validation tests to use the authoritative generic construction APIs.
- Documented the current scene lifecycle, including persistent state ownership and the handling of transient dialogue, messages, and hover state.
- Clarified the responsibilities of unit, integration, and Pygame-adapter tests.
- Updated roadmap and architecture documentation to reflect the completed v0.9.1 foundation and the next planned milestone.
- Applied the configured Ruff formatter across source and test files.

### Removed
- Removed the obsolete create_demo_game_session() convenience wrapper.
- Removed the obsolete create_demo_scenes() convenience wrapper.
- Removed stale temporary release documentation from docs/temp.md.
- Removed completed refactor records from the active refactor backlog so it contains only pending or deferred work.

## 0.9.1 - 2026-07-17

### Added
- Added GameSession as the owner of one running game session.
- Added deterministic new-game/reset behavior with N.
- Added GameContent as the reusable static-content composition root.
- Added serialization-ready state snapshots using plain Python values.
- Added snapshot restoration with save-version and content-reference validation.
- Added explicit ending-state persistence.
- Added JSON loading for item and recipe definitions.
- Added shared JSON loading and field-validation helpers.
- Added UIResources for shared and cached font ownership.
- Added stable future image and audio asset lookup boundaries.
- Added tests for session isolation, reset behavior, snapshot round trips, JSON loading, and UI resource reuse.
- Added documentation describing current content formats and future refactor checkpoints.

### Changed
- New games now construct a fresh session instead of manually clearing scattered runtime fields.
- Static content and rules are now separated from mutable session state.
- Multiple sessions can reuse the same GameContent without sharing runtime state.
- Scene instances are rebuilt from reusable content and fresh GameState.
- GameState remains the owner of inventory, selection, flags, collected pickups, completed interactions, and ending state.
- State snapshots now contain only stable IDs and serialization-safe values.
- Item names, descriptions, and recipe definitions now have JSON as their single authoritative source.
- Python item ID constants remain only as stable references for Python-authored scene logic.
- Scenes and dialogue remain Python-authored until dialogue choices stabilize.
- Scene and widget font construction now uses shared UIResources.
- Tests are now organized into clearer unit, integration, Pygame-adapter, and manual-testing layers.
- JSON content-loading tests were moved into the integration-test layer.
- Content validation now works through the current GameContent composition path.

## 0.9.0 - 2026-07-09

### Added

- Added the Cup of Water item.
- Added the Rusty Key item.
- Added item-use result items so interactions can transform or reward inventory items.
- Added key-based tower gate unlocking.
- Added validation for item-use result items and exit item-use requirements.
- Added tests for the complete key-based demo flow.

### Changed

- Updated the Old Well to turn Empty Cup into Cup of Water.
- Updated the Glowing Tea recipe to combine Cup of Water with Moon Herb.
- Updated the Retired Witch to give Rusty Key instead of unlocking the tower directly.
- Updated the Tower Gate to require Rusty Key before setting `TOWER_UNLOCKED`.
- Updated documentation to describe the implemented v0.9 puzzle flow.

## 0.8.1 - 2026-07-09

### Added

* Added regression coverage for hotspot inspection text priority.
* Added a full demo-flow integration test using the real demo content.
* Added Python content validation for scenes, exits, items, recipes, pickups, item-use requirements, and stable IDs.
* Added stable pickup IDs and interaction IDs for persistent world state.
* Added centralized persistent world-state tracking for collected pickups and completed interactions.
* Added a stateless item-use model where completion is stored in `GameState`.
* Added a render-free item-combination operation for recipe execution.
* Added `AdventureInteractionService` to handle gameplay interactions outside `AdventureScene`.
* Added unified world-target resolution for NPCs, exits, pickups, and hotspots.
* Added shared UI text wrapping helper.
* Added shared `InventoryBar` layout calculation for drawing and hit testing.
* Added and updated tests for integration behavior, item use, recipes, world-state persistence, target priority, and UI helpers.

### Changed

* `InventoryPanel` has been fully renamed to `InventoryBar`.
* `GameState` is now the owner of persistent runtime facts: inventory, selection, progression flags, collected pickups, and completed interactions.
* Static recipe rules were moved out of `GameState`.
* `AdventureScene` now acts more as a Pygame adapter and presentation coordinator.
* Recipe execution no longer happens directly inside `AdventureScene`.
* Item-use definitions no longer contain hidden mutable completion state.
* Collected pickups are ignored through `GameState` instead of relying on removal from a single scene instance.
* NPC and hotspot conditional content now follow the same priority: matching progression flag, then completed interaction, then default content.
* Click and hover world-target resolution now share the same priority order: NPC, exit, item pickup, hotspot.
* Exits now provide hover feedback.
* Documentation now reflects the current v0.8.1 architecture, testing boundaries, and roadmap.
* The intended v0.9 puzzle flow is now documented as: witch receives tea, gives a rusty key, and the key unlocks the tower.

### Fixed

* Fixed `Hotspot.inspect_text_for()` returning flagged inspection text, including `None`, when the relevant flag was inactive.
* Fixed unreachable Suspicious Stump item-use content by removing its invalid `missing_stump_item` requirement.
* Fixed content drift in documentation around the v0.9 tower-unlock flow.
* Fixed misleading empty scaffolding that implied JSON loading or quest systems were already implemented.

## 0.8.0 - 2026-07-07

### Added

- Added centralized quest and progression flag identifiers.
- Added progression flags to successful item-use interactions.
- Added flag-dependent NPC dialogue.
- Added flag-dependent hotspot inspection text.
- Added locked exits with required progression flags.
- Added optional completion flags for successful exits.
- Added the locked Ancient Tower entrance.
- Added the Ancient Tower interior scene.
- Added the demo completion progression flag.
- Added automated tests for locked exits and flag-reactive content.

### Changed

- Updated the Retired Witch to require Glowing Tea.
- Updated the witch interaction to unlock the Ancient Tower.
- Updated Village Square and Forest Path content to react to quest progress.
- Updated exit rendering to visually distinguish locked exits.

## 0.7.0 - 2026-07-07

### Added

- Added an order-independent item recipe system.
- Added shared recipe storage to game state.
- Added inventory item combination interactions.
- Added the Glowing Tea inventory item.
- Added a recipe combining Empty Cup and Moon Herb.
- Added success and failure messages for item combinations.
- Added automated tests for recipes and inventory combinations.

### Changed

- Updated the InventoryBar to explain item selection and combination.
- Updated inventory clicks to combine a selected item with another item.
- Removed recipe ingredients after successful combinations.
- Added the recipe result item to inventory after successful combinations.

## 0.6.1 - 2026-07-06

### Added

- Added shared `GameState` for inventory and progression flags.
- Added centralized item ID constants and item factory functions.
- Added separate content modules for Village Square and Forest Path.
- Added a reusable wrapped interaction message box.
- Added behavioral tests for scene cancellation and item interactions.
- Added tests for shared game-state flags.

### Changed

- Refactored scene creation into individual scene modules.
- Refactored `AdventureScene` event handling into focused helper methods.
- Updated scenes to receive shared game state instead of inventory directly.
- Moved shared visual values into the theme module.
- Limited the settings module to application-level configuration.
- Updated exit hotspot rendering to use shared theme values.
- Replaced the debug text setting with the shared secondary text color.

## 0.6.0 - 2026-07-06

### Added

- Added inventory item selection and deselection.
- Added highlighted selected-item state in the inventory UI.
- Added reusable required-item interaction rules.
- Added support for using inventory items on hotspots and NPCs.
- Added success, failure, and completed interaction messages.
- Added optional item consumption after successful interactions.
- Added state-dependent hotspot inspection text.
- Added state-dependent NPC dialogue.
- Added automated tests for inventory selection.
- Added automated tests for required-item interactions.

### Changed

- Updated the Old Well to react to the Empty Cup.
- Updated the Retired Witch to require the Moon Herb.
- Updated Escape handling to clear selected inventory items before quitting.

## 0.5.0 - 2026-07-06

### Added

- Added immutable item definitions.
- Added collectible item hotspots.
- Added a shared player inventory system.
- Added an inventory panel showing collected items.
- Added the collectible Empty Cup and Moon Herb.
- Added automated tests for inventory operations.
- Added automated tests for item hotspot collision detection.

### Changed

- Updated adventure scenes to support collectible items.
- Updated the game application to own a shared inventory.
- Changed the Moon Herb from an inspectable hotspot into a collectible item.
- Removed collected items from their scenes after pickup.

## 0.4.1 - 2026-07-05

### Added
- Added automated tests for input bindings.
- Added automated tests for consumed scene events and event-driven scene transitions.

### Changed
- Refactored scene input handling to use reusable event results.
- Added centralized key-binding helpers for primary action, dialogue advance, and cancel actions.
- Decoupled global application input handling from AdventureScene.
- Centralized scene IDs to reduce string duplication and typo risk.
- Updated scene manager event handling to report whether an event was consumed.
- Added support for keypad Enter when advancing dialogue.
## 0.4.0 - 2026-07-05

### Added

- Added reusable NPC entities.
- Added dialogue state and progression system.
- Added a reusable dialogue box UI with wrapped text.
- Added mouse, Space, and Enter controls for advancing dialogue.
- Added Escape handling for closing active dialogue.
- Added the Retired Witch and Mushroom Guard placeholder NPCs.
- Added automated tests for dialogue progression and validation.

### Changed

- Updated adventure scenes to support NPC interactions.
- Prevented scene interactions while dialogue is active.

## 0.3.0 - 2026-07-05

### Added

- Added reusable inspectable hotspots.
- Added hotspot hover detection and visual feedback.
- Added click interaction text for scene objects.
- Added placeholder objects to Village Square and Forest Path.
- Added automated hotspot collision tests.

### Changed

- Updated adventure scenes to support both exits and inspectable objects.

## 0.2.0 - 2026-07-05

### Added
- Added a reusable base scene interface.
- Added a reusable adventure scene implementation.
- Added two placeholder scenes: Village Square and Forest Path.
- Added clickable exit hotspots for scene transitions.
- Added automated tests for scene selection and scene changes.

### Changed
- Updated the main game loop to delegate event handling, updates, and drawing to the active scene.
- Added current scene information to the debug display.

## 0.1.0 - 2026-07-03

### Added
- Added initial Pygame window.
- Added stable game loop.
- Added ESC and window-close handling.
- Added simple background and debug text.