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