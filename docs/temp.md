## v0.8.1 — Refactor and behavior hardening

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

### Removed

* Removed empty/deferred JSON scaffolding from `src/data`.
* Removed the unused empty `quests.py` module.
* Removed leftover inventory-row convenience access after introducing the shared `InventoryBarLayout`.

### Notes

* JSON content loading is still intentionally deferred.
* Save/load is not implemented yet.
* v0.9 remains focused on completing the playable demo content.
* v0.9.1 is reserved for post-demo refactoring once the final demo flow is proven.
