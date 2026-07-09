# Architecture

Status: current for v0.8.1

## Goal

Keep the game architecture small enough to understand while separating three things that should not own each other's work:

```txt
Pygame presentation  -> event handling, drawing, UI state
Gameplay rules       -> interactions, item use, recipes, exits
Persistent state     -> inventory, flags, collected pickups, completions
```

The project is still a prototype. Avoid large engine patterns unless the game actually needs them.

## Current project structure

```txt
src/
├── main.py
└── game/
    ├── app.py
    ├── game_state.py
    ├── scene_event_result.py
    ├── scene_manager.py
    ├── settings.py
    ├── theme.py
    ├── content/
    │   ├── demo_world.py
    │   ├── flag_ids.py
    │   ├── interaction_ids.py
    │   ├── item_ids.py
    │   ├── items.py
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

There is no JSON content loader in v0.8.1. Demo content is still Python-created and validated at startup.

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
- create shared `GameState`
- create static recipe rules
- create and validate demo scenes
- own the main loop
- delegate scene events, updates, and drawing
- handle global quit behavior

`GameApp` composes the application. It should not implement item-use, recipe, or quest logic.

## Scene layer

### `game/scene_manager.py`

Responsibilities:

- own scene instances
- remember the current scene ID
- route events, updates, and drawing to the active scene
- perform scene transitions requested by scene results

### `game/scenes/base_scene.py`

Defines the common scene interface:

```txt
handle_event(event) -> SceneEventResult
update(delta_time)
draw(surface)
```

### `game/scenes/adventure_scene.py`

`AdventureScene` is now mostly a Pygame adapter and presentation coordinator.

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

`GameState` is the authoritative owner of persistent facts that must survive scene changes or scene reconstruction.

Current responsibilities:

```txt
GameState
├── inventory
├── progression flags
├── collected pickup IDs
└── completed interaction IDs
```

Examples:

```txt
flag: tower_unlocked
pickup: pickup.village.empty_cup
interaction: interaction.village.old_well
```

Transient presentation state does not belong in `GameState`.

Do not store these in `GameState`:

- hover target
- current message box text
- open dialogue page/index
- Pygame fonts
- Pygame surfaces
- layout rectangles

## Static content and rules

Static content/rules are separate from runtime player/world state.

Examples:

```txt
content IDs
item definitions
scene definitions/factories
recipe definitions
item-use definitions
validation rules
```

### `game/content/`

Responsibilities:

- define stable scene/item/flag/pickup/interaction IDs
- create demo items
- create demo recipe book
- create demo scene objects
- validate content references before gameplay starts

IDs are stable strings. Keep user-facing names separate from stable IDs.

### `game/content/validation.py`

The validator catches broken Python-created content references early.

It checks things like:

- starting scene exists
- scene IDs are unique
- exits target known scenes
- item IDs are unique
- pickups reference known items
- recipes reference known items
- item-use requirements reference known items
- pickup and interaction stable IDs are unique

This validator will still be useful if content later moves to JSON. The input shape may change later, but the purpose remains the same.

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

## Interaction service

### `game/systems/adventure_interaction_service.py`

`AdventureInteractionService` owns gameplay transactions that happen after a target has been resolved.

Responsibilities:

- inventory selection and deselection
- item combination through `item_combination.py`
- item collection
- hotspot inspection
- NPC dialogue outcome selection
- using selected items on NPCs and hotspots
- item consumption
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

## Data-driven content

Deferred.

There is no active `src/data` content pipeline in v0.8.1. JSON loading should wait until the Python content shape is stable enough to justify schemas, parsing, validation, and useful error messages.

Recommended future order:

1. Keep Python content while v0.9 completes the demo.
2. Introduce clear content definition objects if needed.
3. Move item definitions to data files first.
4. Move recipes next.
5. Move scenes/dialogue only after their schema is stable.

## Design constraints

Do not add these for the current prototype:

- event bus
- command hierarchy
- entity-component system
- generic quest engine
- JSON loader
- save/load
- complex crafting system
- UI framework

Add them only when the game has a concrete need.
