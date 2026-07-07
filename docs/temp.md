# v0.7.0

## Manual test
1. Pick up Empty Cup.
2. Travel to Forest Path.
3. Pick up Moon Herb.
4. Click Empty Cup in the InventoryBar.
5. Empty Cup becomes selected.
6. Click Moon Herb.
7. Empty Cup disappears.
8. Moon Herb disappears.
9. Glowing Tea appears.
10. Combination message appears.

Also test failure behavior:

1. Select Empty Cup.
2. Click another item without a recipe.
3. Failure text appears.
4. Both items remain.
5. Empty Cup remains selected.


Changelog for v0.7.0
## 0.7.0 - YYYY-MM-DD

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

## v0.8.0
Expected game flow once manual testing is possible:

1. Pick up Empty Cup.
2. Pick up Moon Herb.
3. Combine them into Glowing Tea.
4. Visit Forest Path before helping the witch.
5. Tower Gate is locked.
6. Give Glowing Tea to Retired Witch.
7. tower_unlocked flag is set.
8. Witch dialogue changes.
9. Notice Board and forest characters react.
10. Tower Gate becomes usable.
11. Enter Tower.
12. demo_completed flag is set.
13. Inspect Ancient Pedestal.
14. Demo completion text appears.
Changelog for v0.8.0
## 0.8.0 - YYYY-MM-DD

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