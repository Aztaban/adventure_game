# Roadmap

Status: current after the v0.9.1 foundation release

## Development principle

Each milestone should be small, testable, and playable.

Do not implement future systems before the current gameplay need exists.

Prefer this order:

```txt
prove gameplay -> protect with tests -> refactor boundary -> document decision
```

## Completed milestones

### Milestone v0.1 — Window and game loop

Goal:

```txt
Open a game window and run a stable loop.
```

Delivered:

- Pygame window
- stable loop
- quit and ESC handling
- simple drawing baseline

### Milestone v0.2 — Scene system

Goal:

```txt
Display one scene and allow switching to another scene.
```

Delivered:

- `SceneManager`
- base scene interface
- placeholder adventure scenes
- exit-driven scene transitions

### Milestone v0.3 — Hotspots

Goal:

```txt
Clickable objects can show interaction text.
```

Delivered:

- inspectable hotspots
- hover detection
- click messages
- hotspot tests

### Milestone v0.4 — Dialogue box and NPCs

Goal:

```txt
NPCs can display dialogue.
```

Delivered:

- NPC entities
- dialogue state system
- dialogue box UI
- click, Space, and Enter advancement
- scene input consumption while dialogue is active

### Milestone v0.5 — Inventory

Goal:

```txt
Player can pick up items and see inventory.
```

Delivered:

- immutable item definitions
- item pickups
- player inventory
- inventory UI renamed to `InventoryBar`
- pickup persistence behavior now owned by `GameState`

### Milestone v0.6 — Use item on hotspot/NPC

Goal:

```txt
Selected inventory item can be used on an object or NPC.
```

Delivered:

- item selection and deselection
- item-use rules
- success/failure/completed outcomes
- optional item consumption
- result-item rewards
- state-dependent NPC/hotspot content

### Milestone v0.7 — Item combining

Goal:

```txt
Two inventory items can combine into a new item.
```

Delivered:

- order-independent recipe system
- Empty Cup -> Old Well = Cup of Water
- Cup of Water + Moon Herb = Glowing Tea
- inventory-combination operation extracted from `AdventureScene`
- atomic recipe transaction tests

### Milestone v0.8 — Quest flags

Goal:

```txt
Game can track progress through flags.
```

Delivered:

- progression flags
- flag-reactive NPC dialogue and hotspot text
- locked tower exit
- demo completion flag
- content validation

### Milestone v0.8.1 — Refactor and regression hardening

Goal:

```txt
Protect behavior and separate runtime state, rules, and presentation before adding final demo content.
```

Delivered:

- hotspot inspection regression fix
- behavior and integration coverage
- Python content validation
- persistent world state in `GameState`
- stateless item-use definitions
- recipe execution extracted from `AdventureScene`
- `AdventureInteractionService`
- unified target resolution for click and hover
- shared UI helpers for text wrapping and inventory layout
- documentation/scaffolding cleanup

### Milestone v0.9 — First complete demo

Goal:

```txt
Playable beginning-to-end mini adventure with the intended key-based tower puzzle.
```

Delivered flow:

```txt
Empty Cup -> Old Well -> Cup of Water
Cup of Water + Moon Herb -> Glowing Tea
Glowing Tea -> Retired Witch -> Rusty Key
Rusty Key -> Tower Gate -> tower opens
Enter Tower -> demo ending
```

Delivered features:

- Cup of Water item
- Rusty Key item
- Old Well fills Empty Cup
- recipe uses Cup of Water + Moon Herb
- witch gives Rusty Key instead of unlocking tower directly
- tower gate unlocks with Rusty Key
- `TOWER_UNLOCKED` remains the semantic world fact after key use
- full demo-flow integration test protects the route

## Milestone v0.9.1 — Post-demo foundation

Goal:

```txt
Clean up architecture after the complete demo proves the gameplay shape.
```

Delivered:

- deterministic `N = New Game` behavior through fresh `GameSession` construction
- reusable `GameContent` separated from current-session `GameState`
- explicit session scene ownership and documented scene-lifecycle behavior
- serialization-ready plain-data snapshots with version and stable-ID validation
- JSON-backed item and recipe definitions converted into typed domain objects
- documented decision to keep scenes and dialogue in Python through v0.12
- shared cached fonts and future asset lookup boundaries in `UIResources`
- clearer unit, integration, and Pygame-adapter test responsibilities
- one authoritative construction path: `create_demo_content()` → `create_game_session()` → `GameContent.build_scenes()`
- removal of obsolete demo-only construction wrappers and stale temporary documentation
- full Ruff and pytest verification protecting the existing v0.9 gameplay flow

Snapshot fields:

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

Content-format decision:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

Revisit dialogue JSON after v0.12 dialogue choices. Consider full-scene data only after a larger-scene pilot proves that its schema is clearer than Python factories.

## Next planned milestone: v0.10 — Polish and presentation pass

Goal:

```txt
Make the complete demo nicer to play without expanding scope.
```

Possible features:

- title screen with Start / Quit
- clearer ending message or ending screen
- improved hover labels and interaction prompts
- better placeholder art or simple sprite assets
- basic sound effects for pickup, dialogue, unlock, and scene transition
- improved dialogue and message box spacing
- README play instructions

Tests/checks:

- title/new-game flow works
- ending can return to new game or quit
- full demo-flow integration still passes
- manual visual/readability checklist updated

Avoid:

- new quest chains
- save menu
- complex animation system
- asset pipeline larger than the current need

## Milestone v0.11 — Save/load prototype

Goal:

```txt
Save and restore the current demo state from a simple file.
```

Suggested scope:

- write snapshot to one local JSON save file
- load snapshot from that file
- basic menu or debug key for save/load
- visible error message for invalid/corrupt save
- preserve current scene, inventory, flags, pickups, completions, and ending state
- include save version

Tests/checks:

- fresh save/load
- mid-quest save/load
- completed-demo save/load
- invalid save file fails clearly
- loading older/unknown save version fails safely

Decide before implementation:

- one autosave slot or manual save slot?
- save/load from title screen, in-game, or debug keys first?
- should loading while dialogue is open close dialogue?

## Milestone v0.12 — Dialogue choices

Goal:

```txt
NPC dialogue can offer choices and branch in a small controlled way.
```

Suggested scope:

- dialogue nodes or simple choice objects
- keyboard/mouse choice selection
- choice text and response lines
- optional required flags for choices
- optional flags set by choices
- no arbitrary scripting or expression evaluation
- at least one NPC uses choices meaningfully

Tests/checks:

- dialogue with no choices still works
- choices display and select correctly
- unavailable choices are hidden or disabled according to one chosen rule
- selected choices can set flags
- scene clicks are still consumed while dialogue is active

Decision point:

```txt
After this milestone, re-evaluate dialogue JSON.
```

If the choice schema is simple and stable, dialogue text/nodes may become the next data-driven content type.

## Milestone v0.13 — Quest journal / objective hints

Goal:

```txt
The player can understand current goals without external instructions.
```

Suggested scope:

- small objective tracker or journal screen
- current objective text based on flags/inventory
- completed objective markers
- optional reminder from NPCs
- no full quest engine unless the simple approach breaks

Tests/checks:

- objective changes after filling cup
- objective changes after making tea
- objective changes after receiving key
- objective changes after unlocking tower
- completed demo objective appears

Decision point:

- Is a simple derived-objective function enough?
- Or do objectives need stable quest-step IDs?

## Milestone v0.14 — Larger scene and camera pilot

Goal:

```txt
Prove whether scenes can be larger than one screen.
```

Suggested scope:

- one larger test scene or expanded Forest Path
- camera offset for drawing
- mouse coordinates converted from screen space to world space
- hotspots/entities work with camera offset
- inventory UI remains screen-space
- no pathfinding yet

Tests/checks:

- clicking world targets works after camera movement
- hover text follows correct target after camera movement
- inventory clicks still use screen coordinates
- full demo still works with fixed scenes

Decision point:

- Keep one-screen scenes for the whole game?
- Or adopt camera/world coordinates before adding many larger areas?

## Milestone v0.15 — Click-to-move character pilot

Goal:

```txt
Test whether visible player movement improves the adventure feel.
```

Suggested scope:

- simple player marker or sprite
- click destination movement
- interaction range or move-then-interact behavior
- no complex pathfinding initially
- blocked areas can remain simple or absent

Tests/checks:

- click-to-move does not break hotspot interaction
- dialogue and inventory still consume input correctly
- scene transitions still work
- interaction order remains understandable

Decision point:

- Keep instant click interactions?
- Or require player movement before interaction?
- If movement is kept, when is pathfinding actually needed?

## Milestone v0.16 — Real asset/content production pass

Goal:

```txt
Replace placeholder feel with a more coherent vertical slice style.
```

Suggested scope:

- consistent scene background style
- simple character/NPC sprites
- item icons for inventory
- UI font and color polish
- small audio set
- asset path validation
- asset credits/license notes

Tests/checks:

- missing asset paths fail clearly
- inventory icons still map to correct items
- game remains playable without visual overlap
- long text remains readable with final font

Decision point:

- Use hand-made assets, generated placeholder assets, or free asset packs?
- Keep rectangle fallback rendering for tests/debug builds?
- Is an asset manifest needed?

## Deferred candidates after v0.16

Potential future milestones:

```txt
v0.17 magic puzzle ability
v0.18 simple skill/ability progression
v0.19 optional side quest
v0.20 combat prototype research
v0.21 content editor / modding research
```

Do not schedule these until the core adventure loop, save/load, dialogue choices, and content production needs are clearer.
