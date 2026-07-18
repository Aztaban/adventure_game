# Architecture

Status: current after the v0.9.1 foundation release

## Goal

Keep the game architecture small enough to understand while separating four things that should not own each other's work:

```txt
Pygame presentation   -> event handling, drawing, UI state
Gameplay rules        -> interactions, item use, recipes, exits
Reusable content      -> item/recipe data, scene factories, IDs, validation
Persistent state      -> inventory, scene position, flags, pickups, completions, ending
```

The project is still a prototype. Avoid large engine patterns unless the game actually needs them.

## Current project structure

```txt
src/
├── main.py
└── game/
    ├── app.py
    ├── game_content.py
    ├── game_session.py
    ├── game_state.py
    ├── scene_event_result.py
    ├── scene_manager.py
    ├── settings.py
    ├── state_snapshot.py
    ├── theme.py
    ├── content/
    │   ├── data/
    │   │   ├── items.json
    │   │   └── recipes.json
    │   ├── demo_world.py
    │   ├── flag_ids.py
    │   ├── interaction_ids.py
    │   ├── item_ids.py
    │   ├── items.py
    │   ├── json_loader.py
    │   ├── pickup_ids.py
    │   ├── recipes.py
    │   ├── scene_ids.py
    │   ├── validation.py
    │   └── scenes/
    │       ├── village_square.py
    │       ├── forest_path.py
    │       └── tower_interior.py
    ├── entities/
    │   ├── exit_hotspot.py
    │   ├── hotspot.py
    │   ├── item.py
    │   ├── item_hotspot.py
    │   └── npc.py
    ├── input/
    │   └── bindings.py
    ├── scenes/
    │   ├── base_scene.py
    │   └── adventure_scene.py
    ├── systems/
    │   ├── adventure_interaction_service.py
    │   ├── dialogue.py
    │   ├── inventory.py
    │   ├── item_combination.py
    │   ├── item_use.py
    │   └── recipe.py
    └── ui/
        ├── dialogue_box.py
        ├── inventory_bar.py
        ├── message_box.py
        └── text.py
```

## Composition overview

Current startup/session ownership:

```txt
GameApp
├── GameContent                 reusable content and rules
└── GameSession                 one current playable run
    ├── GameState               persistent runtime facts
    └── SceneManager            current scene and session scene instances
```

A new game/reset creates a new `GameSession`. It does not manually clear many unrelated objects.

## Application layer

### `main.py`

Responsibilities:

- create and run `GameApp`
- stay small
- contain no gameplay rules

### `game/app.py`

Responsibilities:

- initialize Pygame
- create the window and clock
- load/create reusable `GameContent`
- create a fresh `GameSession`
- own the main loop
- delegate scene events, updates, and drawing
- handle global quit behavior
- handle global new-game/reset input

`GameApp` composes the application. It should not implement item-use, recipe, quest, or save/load logic.

## Reusable content

### `game/game_content.py`

`GameContent` owns reusable static content and rules that can be shared across sessions.

Current responsibilities:

```txt
GameContent
├── items_by_id
├── recipe_book
├── scenes_by_id
├── starting_scene_id
├── flag_ids
├── pickup_ids
└── interaction_ids
```

Rules:

- `GameContent` is reusable.
- `GameContent` should not contain current inventory, selected item, current scene, collected pickups, completed interactions, or ending state.
- `GameContent.build_scenes(game_state)` creates fresh scene instances for one session.
- Reusable content should not depend on Pygame fonts, surfaces, or live UI state.

### `game/content/demo_world.py`

Responsibilities:

- create demo `GameContent`
- load items and recipes
- register scene builders
- build validation scenes once
- validate references before gameplay starts
- collect ID registries for snapshot validation

### Current supported content formats

Authoritative formats:

```txt
Items:     JSON data loaded into Item objects
Recipes:   JSON data loaded into Recipe / RecipeBook objects
Scenes:    Python factories
NPCs:      Python factories
Hotspots:  Python factories
Exits:     Python factories
Dialogue:  Python factories
```

This is intentional. Items and recipes have small stable schemas. Scenes and dialogue are still design-heavy and expected to change.

Python constants such as `EMPTY_CUP` or `RUSTY_KEY` are stable references used by Python scene logic. They are not duplicate item definitions. Item names/descriptions live in JSON.

## Content loading and validation

### `game/content/data/items.json`

Contains item definitions:

```txt
id
name
description
```

### `game/content/data/recipes.json`

Contains recipe definitions:

```txt
first_item_id
second_item_id
result_item_id
success_text
```

Recipe JSON references item IDs. It does not embed result item definitions.

### `game/content/json_loader.py`

Contains shared JSON loading helpers and shared content-load error handling.

Keep this module small. It should not become a content framework.

### `game/content/validation.py`

The validator catches broken content references early.

It checks things like:

- starting scene exists
- scene IDs are unique
- exits target known scenes
- item IDs are unique
- pickups reference known items
- recipes reference known items
- item-use requirements and result items reference known items
- pickup and interaction stable IDs are unique

The validator remains useful if more content later moves to JSON. The input shape may evolve, but the purpose remains the same.

## Content-format decision for scenes and dialogue

R091-06 decision:

```txt
Keep scenes and dialogue in Python for now.
```

Reasons:

- There are not enough scenes yet to justify full-scene JSON.
- The full-scene schema would include coordinates, entity types, item-use rules, flags, exits, and conditions.
- Dialogue choices are planned for v0.12, so the dialogue schema is not stable yet.
- Python factories currently give clearer errors and simpler refactoring than a premature scene loader.

Re-evaluate after v0.12, once dialogue choices have a real shape.

## Scene/session layer

### `game/game_session.py`

`GameSession` owns one playable run:

```txt
GameSession
├── game_state
└── scene_manager
```

Creating a new session gives a fresh game without restarting Python.

### `game/scene_manager.py`

Responsibilities:

- own the current session's scene instances
- remember the current scene ID
- route events, updates, and drawing to the active scene
- perform scene transitions requested by scene results

## Current scene lifecycle policy

Session scenes are created once when a `GameSession` is built and remain owned by that session.

Current transition behavior is intentionally small:

- `SceneManager` changes only the active scene ID.
- Persistent world facts remain in `GameState` and are never reset by a scene transition.
- Interaction messages remain local to the scene that produced them and are still present when that same scene is revisited.
- Dialogue input is modal, so an active dialogue cannot trigger an exit transition underneath it.
- Hover state is resolved from the current mouse position during drawing and is not stored across transitions.
- Creating a new session clears all scene-local presentation state because it creates fresh scene instances.
- Restoring a snapshot creates fresh scene instances and restores persistent state only; transient messages and open dialogue are not serialized.

No `on_enter()` or `on_exit()` hooks are needed for the current behavior. Add them only when a real feature such as timers, animation, audio, or loading transitions requires them.

### `game/scenes/base_scene.py`

Defines the common scene interface:

```txt
handle_event(event) -> SceneEventResult
update(delta_time)
draw(surface)
```

### `game/scenes/adventure_scene.py`

`AdventureScene` is mostly a Pygame adapter and presentation coordinator.

Responsibilities:

- receive Pygame events
- check inventory UI before world targets
- resolve clicked or hovered world targets
- call `AdventureInteractionService`
- apply returned messages, dialogue, and target scene IDs
- own transient scene presentation state
- draw scene header, entities, hover text, inventory, messages, and dialogue

It should not directly:

- add or remove recipe ingredients
- apply item-use flags
- decide item consumption
- mark interactions complete
- decide whether a pickup was already collected

Those belong to `AdventureInteractionService` and `GameState`.

## World target resolution

World target resolution lives in `AdventureScene` because it depends on scene-local rectangles and Pygame mouse positions.

Inventory remains a separate UI-first check:

```txt
inventory UI > world target
```

World targets share one priority for both click and hover:

```txt
NPC > exit > item pickup > hotspot
```

The resolver returns a tagged target so clicking and hovering cannot disagree about the selected world entity.

Collected pickups are ignored by consulting `GameState`.

## Persistent runtime state

### `game/game_state.py`

`GameState` is the authoritative owner of persistent facts that must survive scene changes, reset/rebuild boundaries, and snapshot round trips.

Current responsibilities:

```txt
GameState
├── inventory
├── progression flags
├── collected pickup IDs
├── completed interaction IDs
└── ending state
```

Examples:

```txt
flag: tower_unlocked
pickup: pickup.village.empty_cup
interaction: interaction.village.old_well
ending: ending_reached
```

Transient presentation state does not belong in `GameState`.

Do not store these in `GameState`:

- hover target
- current message box text
- open dialogue page/index
- Pygame fonts
- Pygame surfaces
- layout rectangles

## Snapshot boundary

### `game/state_snapshot.py`

Snapshots prepare the project for save/load without adding file UI yet.

Snapshot data contains plain values only:

```txt
save_version
current_scene_id
inventory_item_ids
selected_item_id or null
flags
collected_pickup_ids
completed_interaction_ids
ending_reached
```

Rules:

- no Pygame objects
- no content definitions
- no `pickle`
- validate referenced IDs against `GameContent`
- restore by constructing a fresh session and applying state

## Gameplay systems

### `game/systems/recipe.py`

Defines static recipe objects and `RecipeBook` lookup.

Recipes are static rules. They are not stored inside `GameState`.

### `game/systems/item_combination.py`

Owns the inventory-combination transaction.

Responsibilities:

- receive two item IDs
- look up the recipe
- validate the full transaction before mutation
- avoid partial mutation
- remove ingredients
- add the result
- return a small result object with success/message/result item

`AdventureScene` should not perform the recipe mutation directly.

### `game/systems/adventure_interaction_service.py`

`AdventureInteractionService` owns gameplay transactions that happen after a target has been resolved.

Responsibilities:

- inventory selection and deselection
- item combination through `item_combination.py`
- item collection
- hotspot inspection
- NPC dialogue outcome selection
- using selected items on NPCs, hotspots, and exits
- item consumption and result-item rewards
- completion and flag updates
- locked/unlocked exit evaluation
- returning requested target scene IDs

It returns `AdventureInteractionOutcome`:

```txt
consumed
message
speaker_name
dialogue_lines
target_scene_id
```

The service must not draw, create fonts, import UI widgets, or change `SceneManager` directly.

## Entities

Entities are lightweight scene content objects with rectangle hit testing and placeholder drawing.

Current entities:

- `NPC`
- `Hotspot`
- `ItemHotspot`
- `ExitHotspot`
- `Item`

Some entities contain static interaction definitions, but runtime completion is stored in `GameState`.

## UI

Current UI widgets:

- `InventoryBar`
- `DialogueBox`
- `MessageBox`

`game/ui/text.py` contains shared text wrapping.

`InventoryBar` calculates one layout result used by both drawing and hit testing.

The current design is fixed-window and intentionally simple. Do not add a generic layout engine, widget inheritance framework, scrolling, or responsive UI yet.

## Future content direction

Current order:

1. Items and recipes are JSON.
2. Scenes and dialogue stay in Python.
3. Dialogue format is revisited after v0.12 dialogue choices.
4. Full scene JSON waits until a one-scene pilot proves the schema is simpler than Python.

Never evaluate arbitrary code or expression strings from content files.

## Design constraints

Do not add these until the game has a concrete need:

- event bus
- command hierarchy
- entity-component system
- generic quest engine
- full scene JSON loader
- dialogue scripting language
- complex crafting system
- UI framework

Add them only when real gameplay complexity justifies them.
