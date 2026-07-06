# Changelog

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