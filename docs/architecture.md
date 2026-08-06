# Architecture

Status: current through v0.12 D120-03 user-data path resolution

## Goal

Keep the game architecture small enough to understand while separating six things that should not own each other's work:

```txt
Application flow      -> title, Controls, gameplay, ending, global actions
Display presentation  -> logical drawing, physical scaling, fullscreen/window switching
Pygame presentation   -> event translation, drawing, UI state, optional asset playback
Gameplay rules        -> interactions, item use, recipes, exits
Reusable content      -> item/recipe data, scene factories, IDs, validation
Persistent state      -> inventory, scene position, flags, pickups, completions, ending
Save path resolution  -> operating-system user-data directory and manual-save filename
```

The project is still a prototype. Avoid large engine patterns unless the game actually needs them.

## Current project structure

```txt
src/
├── main.py
└── game/
    ├── app.py
    ├── asset_ids.py
    ├── display.py
    ├── game_content.py
    ├── game_session.py
    ├── game_state.py
    ├── scene_event_result.py
    ├── scene_manager.py
    ├── save_paths.py
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
        ├── asset_panel.py
        ├── controls_screen.py
        ├── dialogue_box.py
        ├── interaction_prompt.py
        ├── inventory_bar.py
        ├── menu_screen.py
        ├── message_box.py
        ├── resources.py
        └── text.py

assets/
├── images/                    replaceable PNG backgrounds and sprites
└── audio/                     replaceable Ogg sound effects
```

## Composition overview

Current startup/session ownership:

```txt
GameApp
├── AppMode                     title, Controls, playing, or ending
├── logical Surface             fixed 1280 x 720 drawing target
├── physical display Surface    fullscreen desktop or approved window preset
├── MenuScreen                  title and ending presentation
├── ControlsScreen              read-only binding presentation and local Back result
├── UIResources                 shared font/image/sound caches
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
- create the logical surface, physical display, and clock
- start in fullscreen desktop mode
- remember the last approved windowed preset for the current process only
- load/create reusable `GameContent`
- create a fresh `GameSession`
- own the title, Controls, playing, and ending application modes
- own top-level navigation and the Controls return mode
- own the main loop
- translate physical pointer events into logical coordinates before delegation
- delegate gameplay events, updates, and logical-surface drawing
- present the completed logical frame through one aspect-preserving output path
- draw the ending menu as an overlay over the entered tower scene
- handle global fullscreen and new-game actions
- handle global quit behavior
- play scene-transition presentation cues
- keep display recreation failures non-destructive to gameplay state

`GameApp` composes the application. It should not implement item-use, recipe, quest, or save/load logic.

## Display and input boundaries

### `game/display.py`

The display module owns the Pygame-light geometry and event-conversion operations used by `GameApp`:

```txt
logical frame: 1280 x 720
physical output: fullscreen desktop or an approved 16:9 window
presentation: one centered uniform scale
unused output: black letterbox/pillarbox space
pointer input: physical coordinates converted back into logical coordinates
```

Current responsibilities:

- read the primary desktop size
- create fullscreen or windowed display surfaces
- calculate the aspect-preserving destination rectangle
- scale and present the complete logical frame
- convert mouse motion and mouse button positions into logical coordinates
- reject pointer positions outside the presented logical rectangle
- wrap display recreation failures in `DisplayModeChangeError`

Scene, inventory, dialogue, and menu geometry remain expressed in logical `1280 x 720` coordinates. The display module does not own `GameSession`, application navigation, save data, or persistent settings.

### `game/input/bindings.py`

The input catalog is the authoritative mapping from Pygame events to semantic actions:

```txt
PRIMARY
CANCEL
DIALOGUE_ADVANCE
MENU_UP
MENU_DOWN
MENU_CONFIRM
NEW_GAME
FULLSCREEN_TOGGLE
```

Physical bindings and player-facing binding labels come from the same catalog. Overlapping keys are intentional: context decides whether `Space`/`Enter` advances dialogue or confirms a menu. Pointer hover remains presentation state rather than a semantic command action.

`GameApp` handles global actions before delegating local events. Menus and gameplay consume the same action vocabulary instead of maintaining separate raw-key checks.

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
- `GameContent.build_scenes(game_state, ui_resources)` creates fresh scene instances for one session.
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
- Dialogue choices are planned for v0.13, so the dialogue schema is not stable yet.
- Python factories currently give clearer errors and simpler refactoring than a premature scene loader.

Re-evaluate after v0.13, once dialogue choices have a real shape.

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

No `on_enter()` or `on_exit()` hooks are needed for the current behavior. The app detects scene-ID changes for the current transition sound. Add lifecycle hooks only when a future feature needs per-scene start/stop behavior such as looping music, animation timers, or loading transitions.

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
- apply returned messages, dialogue, target scene IDs, and optional sound cues
- own transient scene presentation state
- load optional scene/entity images through `UIResources`
- draw scene header, entities, hover prompts, inventory, messages, and dialogue

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

## Save path boundary

### `game/save_paths.py`

`resolve_save_paths()` is the single current boundary for save-file locations.

Rules:

- use `platformdirs.user_data_path()` with application name `Mysterious Forest`
- pass `appauthor=False` so no separate publisher/author directory is introduced
- keep `ensure_exists=False`; path lookup does not create a directory or file
- expose only the user-data directory and `save.json` manual-save path
- accept an injected user-data directory for tests and future composition
- keep paths out of `GameState`, snapshots, gameplay services, and screen objects
- do not define or create settings/configuration paths during v0.12

Directory creation belongs to the later save-write boundary, only when a write requires it.

## Save-file boundary

### `game/save_file.py`

The save-file boundary owns the versioned JSON envelope and non-mutating file inspection.

Envelope shape:

```txt
save_format_version
saved_at_utc
snapshot
```

Rules:

- save-file format version `1` is independent from the state-snapshot version
- create envelopes from plain snapshot data and aware timestamps normalized to UTC
- require exactly the three envelope fields and validate their types before snapshot validation
- validate ISO-8601 timestamps as UTC
- validate the nested snapshot without constructing or mutating a `GameSession`
- return `SaveFileStatus` outcomes for missing, valid, invalid JSON, invalid envelope, unsupported version, invalid snapshot, and unreadable files
- do not return raw filesystem, Unicode, JSON, or snapshot exceptions to menu/application code
- do not migrate or reinterpret unsupported versions

Reading and validation are available now. Directory creation, JSON writing, temporary files, flushing, syncing, and atomic replacement belong to D120-05.

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
- expose `validate_state_snapshot()` for non-mutating shape and content-ID validation
- defer Pygame-bound imports until actual restoration
- restore by constructing a fresh session and applying validated state

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
sound_effect_id
```

The service must not draw, create fonts, import UI widgets, play audio directly, or change `SceneManager` directly. A sound asset ID is only a presentation cue returned to the Pygame adapter.

## Entities

Entities are lightweight scene content objects with rectangle hit testing, optional image asset IDs, and safe placeholder drawing.

Current entities:

- `NPC`
- `Hotspot`
- `ItemHotspot`
- `ExitHotspot`
- `Item`

Some entities contain static interaction definitions, but runtime completion is stored in `GameState`.

## UI and presentation resources

Current focused UI components:

- `MenuScreen` for title and ending menus
- `ControlsScreen` for the read-only binding list and semantic Back result
- `InteractionPrompt` for hover action and input guidance
- `InventoryBar`
- `DialogueBox`
- `MessageBox`
- `asset_panel.draw_labeled_asset()` for image-backed entities with readable fallback labels

`game/ui/text.py` contains shared text wrapping.

`InventoryBar`, `MenuScreen`, and `ControlsScreen` calculate logical-resolution geometry used by both drawing and hit testing.

### `game/ui/resources.py`

`UIResources` owns small application-wide caches for:

```txt
font size -> pygame Font
(image asset ID, requested size) -> optional pygame Surface
audio asset ID -> optional pygame Sound
```

Rules:

- paths are derived from stable IDs in `game/asset_ids.py`
- images use `assets/images/<asset_id>.png`
- sounds use `assets/audio/<asset_id>.ogg`
- missing or invalid optional assets return `None`
- rendering falls back to labeled colored rectangles
- sound playback becomes a no-op when the mixer or file is unavailable
- no manifest, atlas, animation loader, channel manager, or preload phase is added yet

The exact replacement contract is documented in `docs/asset-guide.md`.

The current design uses a fixed logical resolution with a scalable physical output. Runtime assets and all UI geometry remain authored for `1280 x 720`; the complete frame is scaled uniformly after drawing. Do not add a generic layout engine, widget inheritance framework, arbitrary drag-resizing, responsive per-widget scaling, or a broad asset pipeline yet.

## Future content direction

Current order:

1. Items and recipes are JSON.
2. Scenes and dialogue stay in Python.
3. Dialogue format is revisited after v0.13 dialogue choices.
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
