# Changelog

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