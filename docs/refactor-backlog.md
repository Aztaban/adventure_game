# Refactor Backlog

Project: Adventure Game  
Current baseline: v0.8.0  
Next refactor release: v0.8.1  
Post-demo refactor release: v0.9.1

## Purpose

This backlog converts the v0.8 architecture review into small, test-first steps.

The v0.8.1 refactor must preserve the current gameplay flow. The larger content, lifecycle, and save-readiness refactor should happen only after the complete v0.9 demo is working.

## Working rules

- Complete tasks in order unless a task says otherwise.
- Add tests before changing protected behavior.
- Keep each task small enough for one focused review and usually one commit.
- Run `make check` after every task.
- Manually test every behavior-affecting task.
- Do not add new v0.9 content during v0.8.1.
- Do not introduce JSON loaders during v0.8.1.
- Do not add dependencies or build a generic engine.
- Keep the names `InventoryBar` and `inventory_bar.py`.

## Status legend

```text
[ ] not started
[~] in progress
[x] completed
[-] skipped after a documented decision
[?] decision required
```

---

# Part I — v0.8.1 focused refactor

## Goals

- Protect the complete v0.8 gameplay flow with tests.
- Fix confirmed interaction defects.
- Centralize persistent runtime state.
- Separate mutable state from content definitions.
- Move gameplay transactions out of `AdventureScene`.
- Use one target-resolution path for clicking and hovering.
- Remove small, proven UI duplication.
- Align the documentation with the resulting architecture.

## Out of scope

- New v0.9 story content or ending screen
- Save/load
- JSON content loading
- Quest engine, event bus, or entity-component system
- Generic renderer or UI framework
- Real assets, responsive UI, or inventory scrolling

## Planned order

| Order | ID | Task |
|---:|---|---|
| 1 | R081-00 | Freeze the v0.8 baseline |
| 2 | R081-01 | Fix hotspot inspection fallback |
| 3 | R081-02 | Add behavior and integration coverage |
| 4 | R081-03 | Add Python content validation |
| 5 | R081-04 | Centralize persistent world state |
| 6 | R081-05 | Make item-use definitions stateless |
| 7 | R081-06 | Extract recipe execution |
| 8 | R081-07 | Extract world interaction handling |
| 9 | R081-08 | Unify target resolution |
| 10 | R081-09 | Deduplicate UI helpers |
| 11 | R081-10 | Update documentation and scaffolding |
| 12 | R081-11 | Verify and release v0.8.1 |

---

## R081-00 — Freeze the v0.8 baseline

### Tasks

- [x] Confirm the version is `0.8.0`.
- [x] Run:

```bash
make check
```

- [x] Manually complete the current v0.7/v0.8 flow.
- [x] Confirm item collection, combining, witch interaction, tower unlock, and demo-completion flag.
- [x] Record any existing odd behavior before refactoring it.

### Done when

- Automated tests pass.
- The current flow works manually.
- Existing behavior is known before architecture changes begin.

---

## R081-01 — Fix hotspot inspection fallback

### Problem

`Hotspot.inspect_text_for()` can return `flagged_inspect_text`, including `None`, when the relevant flag is inactive. It should fall back to normal or completed inspection text.

### Tests first

- [ ] Default hotspot returns `inspect_text`.
- [ ] Completed interaction returns `completed_text`.
- [ ] Active matching flag returns `flagged_inspect_text`.
- [ ] Inactive flag falls back correctly.
- [ ] Priority is tested:

```text
matching flag text > completed text > default text
```

### Work

- [ ] Correct `Hotspot.inspect_text_for()`.
- [ ] Reuse `current_inspect_text` if it still expresses the intended fallback.
- [ ] Avoid unrelated entity changes.

### Manual check

Inspect the notice board, old well, stump, and pedestal before their flags are active. Each must display meaningful text.

### Done when

- No inspection path returns `None`.
- The new regression tests pass.
- `make check` passes.

---

## R081-02 — Add behavior and integration coverage

### A. Complete demo-flow test

Use the real demo content rather than recreating it in the test.

- [ ] Start in the expected scene.
- [ ] Collect Empty Cup.
- [ ] Move to Forest Path.
- [ ] Confirm the tower is locked.
- [ ] Collect Moon Herb.
- [ ] Combine Empty Cup and Moon Herb.
- [ ] Confirm ingredients are removed and Glowing Tea is added.
- [ ] Return to the witch and give her the tea.
- [ ] Confirm the tea is consumed.
- [ ] Confirm `WITCH_RECEIVED_TEA` and `TOWER_UNLOCKED`.
- [ ] Enter the tower.
- [ ] Confirm the transition and `DEMO_COMPLETED`.

### B. Collection behavior

- [ ] Pickup adds an item.
- [ ] A pickup cannot be collected repeatedly.
- [ ] Collected state survives leaving and returning.
- [ ] Duplicate-item behavior is explicitly tested.

### C. Item-use behavior

- [ ] Correct and incorrect item on an NPC.
- [ ] Correct and incorrect item on a hotspot.
- [ ] Success consumes the item only when configured.
- [ ] Failure never consumes it.
- [ ] Completed interactions return completed text/dialogue.
- [ ] A target without item-use rules returns the generic response.
- [ ] Selected-item behavior after success and failure is explicit.

### D. Exit and input behavior

- [ ] Locked exit does not transition or set completion flags.
- [ ] Unlocked exit transitions and sets configured flags.
- [ ] Active dialogue consumes advance input.
- [ ] Advancing dialogue does not also trigger the object beneath the cursor.
- [ ] Inventory clicks take precedence over world targets.

### E. Recipe transaction behavior

- [ ] Invalid pair leaves inventory unchanged.
- [ ] Valid pair mutates inventory atomically.
- [ ] Existing-result-item behavior is explicit.
- [ ] Selection state after valid and invalid combinations is tested.

### Suggested organization

```text
tests/
├── integration/
│   └── test_demo_flow.py
└── ...existing focused tests
```

Add shared factories only when they remove meaningful duplication without hiding the gameplay story.

### Done when

- Important v0.8 behavior is protected before extraction begins.
- Tests assert public outcomes and state rather than private helpers.
- `make check` passes.

---

## R081-03 — Add Python content validation

### Goal

Detect broken content references during startup or tests.

### Current issue

The Suspicious Stump requires `missing_stump_item`, which does not exist. Its success branch is unreachable.

### Validation rules

- [ ] Starting scene exists.
- [ ] Scene IDs are unique.
- [ ] Every exit target exists.
- [ ] Item IDs are unique.
- [ ] Pickups reference known items.
- [ ] Recipe ingredients and results reference known items.
- [ ] Item-use requirements reference known items.
- [ ] Stable pickup/interaction IDs are unique once introduced.

### Work

- [ ] Add a small validator, for example `game/content/validation.py`.
- [ ] Validate the existing Python-created content objects.
- [ ] Produce useful errors naming the invalid ID and its owner.
- [ ] Remove the stump’s unreachable item-use rule unless an existing v0.8 item genuinely solves it.
- [ ] Do not add a new story item merely to satisfy validation.

### Tests

- [ ] Valid demo content passes.
- [ ] Unknown exit target fails clearly.
- [ ] Unknown recipe item fails clearly.
- [ ] Unknown required item fails clearly.
- [ ] Duplicate stable ID fails clearly.

### Done when

- Shipped demo content passes validation.
- Invalid references fail early and clearly.
- No JSON schema or loader has been introduced.
- `make check` passes.

---

## R081-04 — Centralize persistent world state

### Goal

Make `GameState` the authoritative owner of facts that must survive scene changes or scene reconstruction.

### Persistent state

- [ ] Inventory and selection
- [ ] Progression flags
- [ ] Collected pickup IDs
- [ ] Completed interaction IDs when no semantic flag already represents completion

### Transient state stays outside `GameState`

- Hover target
- Current message
- Open dialogue page/index
- Pygame fonts, surfaces, and layout rectangles

### Stable pickup IDs

- [ ] Add `pickup_id` to `ItemHotspot` definitions.
- [ ] Do not use list position or coordinates as identity.
- [ ] Do not assume `item_id` is globally unique in the world.
- [ ] Record collected pickup IDs in `GameState`.
- [ ] Hide/ignore collected pickups through state rather than relying only on removing them from a scene list.

Possible API:

```python
has_collected_pickup(pickup_id)
collect_pickup(pickup_id)
has_completed_interaction(interaction_id)
complete_interaction(interaction_id)
```

### Tests

- [ ] New state contains no collected pickups or completed interactions.
- [ ] Repeated collection is idempotent.
- [ ] A recreated scene still hides an already-collected pickup.
- [ ] Completion survives scene transitions/reconstruction.

### Done when

- Persistence no longer depends on retaining one exact mutable scene instance.
- A newly constructed scene can reproduce world state from `GameState`.
- Save/load is not implemented yet.
- `make check` passes.

---

## R081-05 — Make item-use definitions stateless

### Goal

Separate interaction rules from runtime completion.

### Work

- [ ] Give one-time interactions a stable `interaction_id` where needed.
- [ ] Remove mutable `is_completed` from `ItemUseInteraction`.
- [ ] Read and write completion through `GameState`.
- [ ] Continue using semantic flags such as `WITCH_RECEIVED_TEA` and `TOWER_UNLOCKED` when other content depends on them.
- [ ] Avoid representing the same fact twice without a reason.

### Completion rule

```text
semantic world fact used elsewhere -> progression flag
local one-time completion only      -> completed interaction ID
```

### Conditional content priority

Use and test the same priority for NPCs and hotspots:

```text
matching progression flag > completed interaction > default content
```

### Tests

- [ ] Recreating a definition does not reset completion.
- [ ] Successful use records completion once.
- [ ] Default/completed/flagged NPC dialogue priority is tested.
- [ ] Default/completed/flagged hotspot text priority is tested.

### Done when

- Content definitions no longer contain hidden mutable completion state.
- Completion is reproducible from shared state.
- `make check` passes.

---

## R081-06 — Extract recipe execution

### Goal

Move inventory-combination rules and mutation out of `AdventureScene`.

### Keep unchanged

- Recipes combine exactly two distinct ingredients.
- Ingredient order does not matter.
- No crafting screen or general crafting engine is added.

### Work

- [ ] Create a small combination operation owned by the gameplay interaction layer.
- [ ] Receive two selected item IDs.
- [ ] Look up the recipe.
- [ ] Validate the complete transaction before mutation.
- [ ] Remove both ingredients and add the result atomically.
- [ ] Return a small structured result such as success/message/result.
- [ ] Move `RecipeBook` out of `GameState`; recipes are static rules, not player state.
- [ ] Inject the recipe book into the operation/service.

### Tests

- [ ] Valid recipe succeeds.
- [ ] Invalid recipe leaves inventory unchanged.
- [ ] Missing ingredient cannot cause partial mutation.
- [ ] Existing result-item policy is tested.
- [ ] The operation can be tested without rendering.

### Done when

- `AdventureScene` no longer removes ingredients or adds recipe results directly.
- `GameState` no longer owns static recipe definitions.
- `make check` passes.

---

## R081-07 — Extract world interaction handling

### Goal

Make `AdventureScene` a Pygame adapter and presentation coordinator instead of the owner of gameplay transactions.

### Introduce one focused service

A suitable name is:

```text
AdventureInteractionService
```

Do not create a separate class for every click type.

### Service responsibilities

- [ ] Inventory selection/deselection rules
- [ ] Item combination through the extracted operation
- [ ] Item collection
- [ ] Hotspot inspection
- [ ] NPC dialogue outcomes
- [ ] Using the selected item on NPCs/hotspots
- [ ] Item consumption
- [ ] Completion and flag updates
- [ ] Locked/unlocked exit evaluation
- [ ] Returning requested target scene IDs

### `AdventureScene` responsibilities afterward

- Receive Pygame events.
- Convert them to high-level actions.
- Resolve the clicked inventory/world target.
- Call the interaction service.
- Apply returned message/dialogue/transition information.
- Own transient presentation state.
- Draw the scene and UI.

### Structured outcome

Use one small result object with only currently needed fields, for example:

```text
consumed
message
speaker_name
dialogue_lines
target_scene_id
```

The service must not draw, import UI widgets, create fonts, or change `SceneManager` directly.

### Tests

- [ ] Service behavior covers pickup, inspect, item use, NPC dialogue, and exits.
- [ ] State mutation and returned presentation outcome agree.
- [ ] Full demo-flow integration test still passes.
- [ ] Scene tests focus on event priority and applying outcomes.

### Done when

- Gameplay behavior can mostly be tested without a rendered scene.
- `AdventureScene` no longer implements inventory transactions, item-use rules, or flag application directly.
- No event bus or command hierarchy was added.
- `make check` passes.

---

## R081-08 — Unify target resolution

### Goal

Make clicking and hovering use one world-target order.

### World priority

```text
NPC > exit > item pickup > hotspot
```

Inventory remains a separate UI-first check:

```text
inventory UI > world target
```

### Work

- [ ] Replace repeated `_find_*` collision loops with one resolver.
- [ ] Return a small tagged target containing kind and entity.
- [ ] Use the resolver for clicks.
- [ ] Use the resolver for hover text/rendering.
- [ ] Include exits in hover behavior.
- [ ] Ignore collected pickups through `GameState`.
- [ ] Keep priority in one obvious place.

### Tests

- [ ] Every target kind resolves correctly.
- [ ] Empty space returns no target.
- [ ] Overlapping targets follow documented priority.
- [ ] Collected pickups do not resolve.
- [ ] Click and hover resolve the same target at one position.
- [ ] Inventory still wins over overlapping world targets.

### Done when

- Click and hover cannot disagree about a world target.
- Exit hover feedback exists.
- Repeated target-search helpers are removed.
- `make check` passes.

---

## R081-09 — Deduplicate UI helpers

### A. Shared text wrapping

- [ ] Extract the duplicated `DialogueBox`/`MessageBox` wrapping algorithm into one pure helper.
- [ ] Keep rendering, borders, padding, and box-specific behavior in each widget.
- [ ] Test short text, wrapped text, and one long word according to the chosen policy.

Possible placement:

```text
src/game/ui/text.py
```

### B. Shared `InventoryBar` layout result

- [ ] Calculate panel rectangle and item rows together.
- [ ] Use the same layout result for drawing and hit testing.
- [ ] Keep the current fixed-window design.
- [ ] Test visible rows, gaps, padding, empty inventory, and planned maximum inventory size.

### Do not add

- Generic layout engine
- Widget inheritance framework
- Responsive resizing
- Scrolling or icon grid

### Manual check

- Long dialogue and messages still wrap readably.
- Clicking each visible inventory row selects the matching item.

### Done when

- Text wrapping has one implementation.
- `InventoryBar` drawing and hit testing share one geometry source.
- `make check` passes.

---

## R081-10 — Update documentation and scaffolding

### `docs/architecture.md`

- [ ] Document `GameState` as persistent runtime state owner.
- [ ] Separate static content/rules from runtime state.
- [ ] Document the interaction service and target resolver.
- [ ] Document transient scene/UI state.
- [ ] Remove outdated planned modules or names.

### `docs/testing-plan.md`

- [ ] Replace placeholder-era text with current unit/integration/manual boundaries.
- [ ] Document the full demo-flow test.
- [ ] Add the v0.8.1 regression checklist.

### `docs/roadmap.md`

- [ ] Replace `Milestone v0.8 - refactor` with v0.8.1.
- [ ] Keep v0.9 focused on the complete demo.
- [ ] Add v0.9.1 as the post-demo refactor milestone.
- [ ] Do not claim JSON was implemented in v0.8.1.

### Resolve content-plan drift

Choose and document one v0.9 flow:

```text
witch gets tea -> gives rusty key -> key unlocks tower
```

or:

```text
witch gets tea -> tower unlocks directly
```

Update `content-plan.md`, `mvp.md`, and related roadmap text consistently. Do not implement new v0.9 content in this documentation task.

### Review misleading scaffolding

```text
src/data/item.json
src/data/recipes.json
src/data/dialogue/.gitkeep
src/data/scenes/.gitkeep
src/game/systems/quests.py
```

- [ ] Remove empty JSON files or clearly document that loading is deferred.
- [ ] Resolve `item.json` versus documented `items.json`.
- [ ] Remove empty `quests.py` if it has no current responsibility.
- [ ] Do not add placeholder classes merely to keep empty files.

### Done when

- Documentation matches v0.8.1 code.
- The intended v0.9 puzzle flow is unambiguous.
- Empty scaffolding does not imply implemented functionality.
- `make check` passes.

---

## R081-11 — Verify and release v0.8.1

### Automated checks

```bash
make format
make check
```

- [ ] Tests do not depend on execution order.
- [ ] Full-flow test uses shipped content.
- [ ] Content validation passes.

### Manual regression

- [ ] Inspect all base hotspots before flags change.
- [ ] Collect Empty Cup and confirm it stays collected after travel.
- [ ] Collect Moon Herb.
- [ ] Try an invalid combination.
- [ ] Create Glowing Tea.
- [ ] Try the tea on an unrelated target.
- [ ] Give the tea to the witch.
- [ ] Confirm completed dialogue and tower unlock.
- [ ] Confirm exit hover feedback.
- [ ] Enter the tower and confirm demo completion.
- [ ] Confirm messages/dialogue remain readable.

### Architecture check

- [ ] `AdventureScene` coordinates input, presentation, and rendering.
- [ ] Interaction service owns gameplay transactions.
- [ ] `GameState` owns persistent runtime state.
- [ ] Static recipes/content are outside `GameState`.
- [ ] Content definitions carry no mutable completion state.
- [ ] Click and hover share one target resolver.
- [ ] No JSON loader or unnecessary framework was introduced.

### Release

- [ ] Update `CHANGELOG.md`.
- [ ] Bump version from `0.8.0` to `0.8.1`.
- [ ] Tag/publish only after all checks pass.

### Definition of done

```text
The complete v0.8 flow behaves the same or better,
persistent state has one clear owner,
AdventureScene no longer owns gameplay transactions,
important behavior is protected by tests,
and JSON remains intentionally deferred.
```

---

# Part II — v0.9 implementation gate

Do not begin the post-v0.9 refactor until all of these are true:

- [ ] The complete three-scene demo is finalized.
- [ ] Intended NPC and four-item flow are implemented.
- [ ] One item-combination puzzle and one obstacle work.
- [ ] Rusty-key versus direct-unlock design is resolved.
- [ ] A clear ending screen/state exists.
- [ ] A fresh game can be completed from start to ending.
- [ ] Automated full-flow tests pass.
- [ ] Manual start-to-ending test passes.

During v0.9, add content through the v0.8.1 boundaries. Defer optional generalization until the content model stops moving.

---

# Part III — v0.9.1 post-demo refactor

## Goals

- Guarantee a deterministic new-game/reset flow.
- Fully separate reusable content from one running game session.
- Prepare persistent state for save/load.
- Make an evidence-based JSON decision.
- Prepare rendering resources for the v0.10 polish pass.

## Planned order

| Order | ID | Task |
|---:|---|---|
| 1 | R091-00 | Freeze the complete v0.9 demo |
| 2 | R091-01 | Add new-game/reset lifecycle |
| 3 | R091-02 | Separate `GameContent` from session state |
| 4 | R091-03 | Define scene lifecycle behavior |
| 5 | R091-04 | Add serialization-ready state snapshots |
| 6 | R091-05 | Pilot JSON for items and recipes |
| 7 | R091-06 | Decide scene/dialogue content format |
| 8 | R091-07 | Centralize UI resources |
| 9 | R091-08 | Strengthen test layering and remove old paths |
| 10 | R091-09 | Verify and release v0.9.1 |

---

## R091-00 — Freeze the complete v0.9 demo

- [ ] Finalize one real-content test from fresh state to ending.
- [ ] Verify every required item, interaction, flag, transition, and ending condition.
- [ ] Record expected state at important checkpoints.
- [ ] Create a matching manual demo checklist.
- [ ] Run `make check` and the full manual flow.

### Done when

The complete demo is protected independently of how content is constructed or loaded.

---

## R091-01 — Add new-game/reset lifecycle

### Required behavior

- [ ] Fresh `GameState`
- [ ] Empty/reset inventory and selection
- [ ] Reset flags, collected pickups, and completed interactions
- [ ] Starting scene restored
- [ ] Messages, dialogue, hover, and ending state cleared
- [ ] Static content reused safely without mutation

Prefer constructing a new session over manually clearing fields scattered across objects.

A small `GameSession` object is acceptable only if it clarifies ownership:

```text
GameSession
├── game_state
├── current scene/session position
└── other run-specific state
```

### Tests

- [ ] Partially progress, reset, and verify every fact is fresh.
- [ ] Complete the game, reset, and complete it again in the same process.
- [ ] Two sessions do not leak state into one another.

### Done when

A fresh game is deterministic without restarting Python.

---

## R091-02 — Separate `GameContent` from session state

### Static content may include

- Item, recipe, scene, NPC, hotspot, exit, and dialogue definitions
- Starting scene ID
- Validated ID registries

### Runtime/session state includes

- Inventory and selected item
- Current scene
- Flags
- Collected pickups
- Completed interactions
- Ending state

### Possible small composition object

```text
GameContent
├── items_by_id
├── recipes
├── scenes_by_id
└── starting_scene_id
```

### Tasks

- [ ] Make content definitions immutable by convention or frozen dataclasses where useful.
- [ ] Keep all runtime mutations in session/state objects.
- [ ] Validate content once during construction.
- [ ] Build scenes from definitions plus session state.
- [ ] Keep fonts and surfaces outside reusable content definitions.

### Tests

- [ ] Two sessions share content without sharing state.
- [ ] Resetting one session does not affect another.
- [ ] Full demo flow works through the new composition root.

### Done when

Every important object is clearly either reusable content or current-session state.

---

## R091-03 — Define scene lifecycle behavior

First decide what should happen to:

- Interaction messages when leaving and returning
- Open dialogue during scene transition
- Hover state during transition
- Ending-state transition
- Future scene-local timers

Add minimal hooks such as `on_enter()` and `on_exit()` only if current behavior needs them.

Likely policy:

- [ ] Clear hover on transition.
- [ ] Close dialogue on transition unless explicitly designed otherwise.
- [ ] Clear or intentionally retain messages according to documented behavior.
- [ ] Never reset persistent world state in scene lifecycle hooks.

### Done when

Scene transition behavior is explicit rather than an accident of persistent scene objects.

---

## R091-04 — Add serialization-ready state snapshots

### Goal

Prepare a clean save/load boundary without yet requiring a save menu or final file format.

### Snapshot should contain plain values only

```text
save version
current_scene_id
inventory_item_ids
selected_item_id or null
flags
collected_pickup_ids
completed_interaction_ids
ending state
```

### Tasks

- [ ] Add export/snapshot operation.
- [ ] Add restore/from-snapshot operation.
- [ ] Include a save-data version.
- [ ] Validate referenced IDs against `GameContent`.
- [ ] Exclude Pygame objects and content definitions.
- [ ] Do not use `pickle`.

### Tests

- [ ] Fresh-state round trip.
- [ ] Mid-quest round trip.
- [ ] Completed-demo round trip.
- [ ] Invalid scene/item/interaction ID fails clearly.

### Done when

Runtime state round-trips through plain Python data with stable IDs.

---

## R091-05 — Pilot JSON for items and recipes

### Decision gate

Proceed only when the v0.9 schemas are stable and data files provide a clear benefit.

Ask:

- [ ] Is content changing often enough to reduce code churn?
- [ ] Would someone reasonably edit it without touching Python?
- [ ] Are stable IDs and validation already reliable?
- [ ] Is the schema simpler than the Python definitions?

If most answers are no, mark this task skipped and keep Python definitions.

### If approved

Start only with items and recipes because they have small schemas.

- [ ] Parse JSON into typed domain definitions.
- [ ] Validate required fields and value types.
- [ ] Reject duplicates and unknown references.
- [ ] Include useful file/path context in errors.
- [ ] Keep gameplay code away from raw dictionaries.
- [ ] Remove the duplicate Python source once migration is accepted.

### Tests

- [ ] Valid files load.
- [ ] Missing/wrong fields fail clearly.
- [ ] Duplicate IDs fail.
- [ ] Unknown recipe references fail.
- [ ] Full demo works with the loaded definitions.

### Done when

The pilot demonstrably improves content editing and leaves only one authoritative source.

---

## R091-06 — Decide scene/dialogue content format

Do not assume full-scene JSON is automatically better. Scene definitions include coordinates, entity types, conditions, flags, interactions, and exits.

### Evaluate

- [ ] Are there enough scenes to justify a loader?
- [ ] Is the schema stable after v0.9?
- [ ] Can conditions remain declarative without creating a mini scripting language?
- [ ] Are loader errors clearer than Python/type errors?
- [ ] Will content authors edit the data directly?

### Valid outcomes

#### A. Keep scenes/dialogue in Python

- [ ] Document Python factories as the supported format.
- [ ] Keep immutable definitions and validation.
- [ ] Remove unused JSON scaffolding.

#### B. Move dialogue text only

- [ ] Load plain dialogue line arrays by stable ID.
- [ ] Keep conditional wiring in Python.
- [ ] Validate references.

#### C. Move full scenes to data

Only after one-scene pilot proves the schema is simpler.

- [ ] Use a versioned schema.
- [ ] Convert raw data to typed definitions.
- [ ] Keep conditional operators intentionally small.
- [ ] Never evaluate arbitrary code or expression strings.

### Done when

The chosen strategy is documented and Python/JSON are not both authoritative.

---

## R091-07 — Centralize UI resources

### Goal

Prepare for v0.10 polish without coupling domain logic to rendering resources.

- [ ] Move repeated font construction into a small UI resource owner/cache.
- [ ] Pass required resources to widgets/scenes.
- [ ] Keep interaction/state code free of Pygame resources.
- [ ] Define future image/audio lookup by stable asset IDs.
- [ ] Do not build a large asset pipeline before real assets exist.

Possible small object:

```text
UIResources
├── title_font
├── body_font
├── small_font
└── future asset lookup
```

### Tests

- [ ] Pure logic tests no longer initialize fonts.
- [ ] UI tests initialize only what they need.
- [ ] Scene construction does not duplicate resources unnecessarily.

### Done when

Rendering-resource ownership is clear and small.

---

## R091-08 — Strengthen test layering and remove old paths

### Test layers

```text
pure unit tests     -> inventory, recipes, state, interactions, validation
integration tests   -> demo flow, reset, state round trips, content loading
Pygame adapter tests -> input translation, hit testing, modal UI behavior
manual tests        -> readability, layout, hover feel, audio, ending presentation
```

### Tasks

- [ ] Keep Pygame-dependent tests a clearly identified minority.
- [ ] Avoid global mutable content in tests.
- [ ] Use narrow fixtures rather than one giant hidden setup.
- [ ] Keep the complete-demo test readable as a gameplay story.
- [ ] Remove obsolete mutable completion fields.
- [ ] Remove scene-list mutation retained only for compatibility.
- [ ] Remove duplicate recipe ownership and target helpers.
- [ ] Remove duplicate Python/JSON definitions.
- [ ] Remove deprecated constructors, temporary adapters, and empty modules.

Verify usage before deleting anything.

### Done when

There is one clear path for state, content, interactions, and target resolution, and test failures point to the correct layer.

---

## R091-09 — Verify and release v0.9.1

### Automated

```bash
make format
make check
```

- [ ] Full demo-flow test passes.
- [ ] New-game/reset tests pass.
- [ ] Snapshot round trips pass if implemented.
- [ ] JSON loader tests pass if the pilot was accepted.

### Manual

- [ ] Complete the demo from a fresh session.
- [ ] Start a second new game without restarting the process.
- [ ] Confirm no item, flag, dialogue, pickup, or ending state leaks.
- [ ] Confirm all scenes and UI still render correctly.

### Documentation and release

- [ ] Update architecture, testing plan, roadmap, content plan, and changelog.
- [ ] Document the final JSON decision, including a decision to remain with Python.
- [ ] Bump `0.9.0` to `0.9.1`.
- [ ] Tag/publish only after all checks pass.

### Definition of done

```text
The complete demo remains stable,
a fresh game is deterministic,
content and session state are clearly separated,
runtime state is serialization-ready,
and the project has made an evidence-based content-format decision.
```

---

# Part IV — Deferred refactor candidates

Reconsider these only when a concrete feature creates pressure.

## During v0.10 polish

- [ ] Asset cache after real images/audio exist.
- [ ] More flexible scene layout after current positions become limiting.
- [ ] Inventory scrolling only after content exceeds the visible panel.
- [ ] UI scaling only with resizable-window support.
- [ ] Specialized rendering after placeholder rectangles are replaced.

## With real save/load

- [ ] Save-file repository and filesystem error handling.
- [ ] Save-data migrations.
- [ ] Multiple slots and autosave checkpoints.

## With dialogue choices or quest journal

- [ ] Explicit quest definitions.
- [ ] Dialogue-node IDs and branching conditions.
- [ ] Player-facing objectives separate from internal flags.

## With larger scenes

- [ ] Camera and world/screen coordinate separation.
- [ ] Spatial indexing only when entity counts justify it.

## Do not introduce without strong evidence

- Generic event bus
- Entity-component system
- Service locator or dependency-injection framework
- Scripting language for conditions
- Inheritance-heavy widget toolkit
- Universal command framework
- Database for local prototype content

---

# Decision log

## D-001 — JSON during v0.8.1

Status: decided

```text
Keep Python content factories during v0.8.1.
Separate runtime state first and reconsider external data after v0.9.
```

## D-002 — Persistent-state owner

Status: agreed scope

```text
GameState owns inventory, flags, collected pickups,
and completed interactions. Static recipes/content do not belong to GameState.
```

## D-003 — `AdventureScene` responsibility

Status: agreed scope

```text
AdventureScene translates Pygame input, resolves targets,
applies presentation outcomes, and renders.
A focused interaction service performs gameplay transactions.
```

## D-004 — Post-v0.9 content format

Status: open

```text
Pilot items and recipes first.
Move scenes/dialogue to data only if the resulting schema
is simpler and more useful than Python factories.
```
