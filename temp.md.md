# Changelog

## 0.11.0 - Unreleased

### Added

- Added a fixed `1280 x 720` logical render surface used by title, Controls, gameplay, ending, and debug presentation.
- Added aspect-preserving output scaling with centered letterboxing or pillarboxing for non-16:9 physical displays.
- Added fullscreen-desktop startup and `F11` switching between fullscreen and the current-session windowed preset.
- Added approved `1280 x 720`, `1600 x 900`, and `1920 x 1080` windowed display modes.
- Added physical-to-logical pointer conversion for mouse motion and mouse button events, including rejection of letterbox input.
- Added a semantic input-action catalog for primary action, cancel, dialogue advance, menu navigation, menu confirmation, new game, and fullscreen toggle.
- Added a read-only Controls screen opened from the title menu and populated from the active binding catalog.
- Added focused display-contract, viewport-math, pointer-conversion, display-mode, input-binding, Controls-screen, and application-flow tests.

### Changed

- Updated the title menu to offer Start Game, Controls, and Quit.
- Routed title, Controls, gameplay, dialogue, and ending input through the shared semantic action vocabulary.
- Kept inventory hit testing ahead of world-target hit testing after coordinate conversion.
- Made display-mode changes presentation-only so they preserve the current `GameSession`, scene, dialogue, inventory selection, progress, and application mode.
- Made failed display recreation non-destructive and visible without replacing the active gameplay session.
- Updated README, architecture, testing, asset, roadmap, milestone, and refactor-planning documentation for the implemented display and controls foundation.
- Updated the package version to `0.11.0`.

### Notes

- Every fresh launch starts in fullscreen desktop mode.
- The first `F11` windowed fallback is `1280 x 720`; later toggles return to the last approved windowed preset used during the current process.
- Display choices are not persisted between launches.
- Arbitrary drag-resizing, editable bindings, and a general screen framework were not added.
- A player-facing selector for the larger approved windowed presets remains deferred to a future options/settings surface.
- The complete demo puzzle flow and persistent gameplay behavior remain unchanged.

## 0.10.0 - Unreleased

### Added

- Added a title screen with Start Game and Quit actions.
- Added a demo-complete overlay with Play Again and Quit actions while preserving the entered tower scene underneath.
- Added keyboard and mouse navigation for title and ending menus.
- Added replaceable PNG scene/object placeholder art with safe rectangle fallbacks.
- Added optional cached Ogg sound effects for pickup, dialogue, unlocking, and scene transitions.
- Added an asset guide describing filenames, formats, recommended dimensions, audio settings, and replacement workflow.
- Added README setup, controls, objective, and play instructions.
- Added automated coverage for menu input, title/new-game behavior, ending replay/quit behavior, and presentation sound cues.

### Changed

- Improved hover prompts with a bordered action panel and explicit left-click instructions.
- Improved locked-exit prompts so they describe inspection or selected-item use instead of implying immediate travel.
- Improved scene object rendering with image-backed labeled panels and readable hover borders.
- Improved dialogue spacing, speaker separation, continuation hints, and message-box placement.
- Expanded `UIResources` from font caching into the active optional image/audio cache boundary planned by v0.9.1.
- Hid the debug overlay by default while retaining a settings switch for development.
- Updated architecture, testing, content, roadmap, and refactor planning documentation for the presentation milestone.

### Notes

- The complete v0.9 puzzle chain and persistent gameplay state behavior are unchanged.
- Missing or invalid optional art/audio assets do not prevent gameplay.
- No new quest chains, save menu, animation framework, or general-purpose asset pipeline were added.

## 0.9.2 - Unreleased

### Changed

- Consolidated demo session construction around the existing `create_demo_content()` and `create_game_session()` composition path.
- Updated application, reset, and content-validation tests to use the authoritative generic construction APIs.
- Documented the current scene lifecycle and clarified unit, integration, and Pygame-adapter test responsibilities.
- Updated roadmap and supporting documentation to distinguish completed v0.9.1 work from the v0.9.2 cleanup patch.
- Applied the configured Ruff formatter across source and test files.

### Removed

- Removed the obsolete `create_demo_game_session()` convenience wrapper.
- Removed the obsolete `create_demo_scenes()` convenience wrapper.
- Removed stale temporary release documentation from `docs/temp.md`.
- Removed completed refactor task history from the active refactor backlog so it contains only planned work.

### Notes

- No gameplay behavior or save-readiness behavior changed.
- The complete v0.9 key-based demo flow remains unchanged.

## 0.9.1 - 2026-07-17

### Added

- Added deterministic in-process new-game/reset through fresh `GameSession` construction.
- Added reusable `GameContent` ownership for item, recipe, scene-builder, and validation registries.
- Added plain-data state snapshot export and validated session restoration with save-version checks.
- Added JSON-backed item and recipe loading with typed domain output and useful validation errors.
- Added `UIResources` as the shared cached font owner and future image/audio lookup boundary.
- Added integration coverage for session reset, snapshot round trips, content loading, and state isolation.

### Changed

- Separated reusable static content from one running session and its mutable `GameState`.
- Kept scenes and dialogue as Python factories after the content-format review.
- Organized tests around unit, integration, and Pygame-adapter responsibilities.

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