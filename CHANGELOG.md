# Changelog

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