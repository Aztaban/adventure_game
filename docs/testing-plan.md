# Testing Plan

Status: current for the v0.10 presentation milestone

## Purpose

The goal is to protect gameplay behavior while keeping tests simple enough to maintain during fast prototype refactors.

The project uses pytest for automated tests and manual checks for game feel, visuals, and full-window behavior.

## How to run checks

Use the Makefile:

```bash
make check
```

This runs:

```bash
python -m ruff check src tests
python -m pytest
```

Run tests directly when debugging:

```bash
PYTHONPATH=src .venv/bin/python -m pytest
```

Run one focused test file:

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests/test_inventory.py
```

## Test boundaries

Automated tests should focus on observable behavior and state changes.

Good automated-test targets:

- inventory behavior
- game state flags, collected pickups, completed interactions, and ending state
- session reset/new-game behavior
- state snapshot export/restore behavior
- JSON item/recipe loading
- content validation
- recipe lookup and item-combination transactions
- item-use success/failure/completion behavior
- scene manager transitions
- dialogue state
- interaction service outcomes
- target resolution priority
- UI helper geometry and text wrapping
- complete demo-flow integration

Manual testing should cover:

- title screen opens before gameplay
- Start Game and Quit work with mouse and keyboard
- window opens and closes correctly
- `N` starts a fresh game from Village Square
- hover/click feel
- readability of hover prompts, dialogue, message boxes, title, and ending overlay
- image scaling and label readability
- sound volume, repetition, and clipping
- object positions and spacing
- whether the flow feels understandable
- visual regressions
- long text readability

Do not over-test exact pixels unless the layout rule is important for behavior.

## Test layers

Use three practical layers. Directory placement should reflect the behavior under test:

```txt
pure unit tests      -> inventory, recipes, state, item use, snapshots, loaders, validation
integration tests    -> real content flow, reset/isolation, snapshot restoration, world persistence
Pygame adapter tests -> event translation, hit testing, target priority, modal UI, drawing resources
```

A test belongs at the lowest layer that can protect the behavior. Pure gameplay rules should not require display creation. Pygame-dependent tests should initialize only the modules they need.

## Current automated test groups

```txt
tests/
├── integration/
│   ├── test_demo_flow.py
│   ├── test_game_session_reset.py
│   ├── test_json_content_loading.py
│   ├── test_state_snapshot.py
│   └── test_world_state_persistence.py
├── test_adventure_interaction_service.py
├── test_adventure_scene.py
├── test_content_validation.py
├── test_game_app.py
├── test_game_content.py
├── test_game_state.py
├── test_inventory*.py
├── test_item*.py
├── test_menu_screen.py
├── test_scene_manager.py
├── test_ui_resources.py
└── other focused unit and Pygame-adapter tests
```

Add new test files only when they describe a real boundary.

## Content-format testing strategy

Current authoritative formats:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

Tests should reflect that split.

### JSON tests

Use loader tests for:

- valid item files
- valid recipe files
- missing fields
- wrong field types
- duplicate item IDs
- duplicate recipe pairs
- unknown recipe references
- invalid JSON and missing files with useful path context

Gameplay tests should not inspect raw JSON dictionaries. They should assert behavior through `Item`, `Recipe`, `RecipeBook`, `GameContent`, and `GameSession`.

### Python scene/dialogue tests

Keep scene/dialogue tests focused on behavior:

- NPC default/completed/flagged dialogue
- hotspot default/completed/flagged inspection
- item-use outcomes
- exit locking/unlocking
- full demo flow

Do not add scene JSON tests until scene JSON is intentionally introduced.

## Full demo-flow integration test

`tests/integration/test_demo_flow.py` protects the current v0.9 playable path using real demo content.

It covers:

```txt
Village Square
→ collect Empty Cup
→ fill Empty Cup at Old Well to make Cup of Water
→ Forest Path
→ verify tower is locked
→ collect Moon Herb
→ combine Cup of Water + Moon Herb into Glowing Tea
→ return to the witch
→ give Glowing Tea to the witch
→ receive Rusty Key
→ verify WITCH_RECEIVED_TEA is set and TOWER_UNLOCKED is not set yet
→ return to Forest Path
→ use Rusty Key on Tower Gate
→ verify TOWER_UNLOCKED is set
→ enter tower
→ verify DEMO_COMPLETED and ending state
```

This test reflects the v0.9 implementation: the witch gives a Rusty Key, and the key unlocks the tower gate.

## v0.10 presentation regression checklist

### Title and ending flow

- startup begins on the title screen
- Start Game creates a fresh session in Village Square
- title Quit and `Esc` close the game
- reaching the ending shows the ending overlay over the Ancient Tower
- Play Again creates a fresh session
- ending Quit closes the game
- `N` still creates a fresh session from title, gameplay, or ending

### Presentation resources

- fonts, images, and sounds are cached by `UIResources`
- missing images fall back to labeled rectangles
- missing sounds or an unavailable mixer remain non-fatal
- pickup, dialogue, unlock, and scene-transition cues use stable asset IDs
- replacement requirements remain documented in `docs/asset-guide.md`

### Readability

- hover panel states the action and input clearly
- a selected item changes NPC/hotspot/locked-exit prompts to item-use wording
- dialogue speaker, body, and continuation hint do not collide
- message boxes remain inside the scene area and do not sit under the inventory panel
- entity labels remain readable over image assets

## v0.9.1 refactor regression checklist

Automated coverage protects these completed foundation behaviors during later changes.

### New-game/reset lifecycle

- partial progress resets to a fresh game
- completed game can reset and complete again in the same Python process
- two sessions do not leak state
- `N` triggers a fresh session from Village Square

### GameContent/session separation

- `GameContent` can be shared across sessions
- sessions get fresh `GameState`
- sessions get fresh scene instances
- static content/rules are not stored in `GameState`

### State snapshots

- fresh-state round trip
- mid-quest round trip
- completed-demo round trip
- selected item round trip
- invalid scene/item/flag/pickup/interaction IDs fail clearly
- snapshot data contains no Pygame objects or content definitions

### JSON item/recipe pilot

- valid files load
- missing or wrong fields fail clearly
- duplicate IDs fail
- unknown recipe references fail
- full demo works with loaded definitions

### Scene/dialogue format decision

- no scene JSON loader is added by accident
- no dialogue JSON source competes with Python dialogue
- docs say Python factories are the supported scene/dialogue format until v0.12 re-evaluation

## v0.8.1 regression checklist

Keep these protected while building future features.

### Hotspot inspection

- default text is returned without flags or completion
- completed text is returned after local completion
- flagged text wins when matching flag is active
- inactive flags fall back correctly
- priority is:

```txt
matching flag > completed interaction > default content
```

### Content validation

- valid demo content passes
- unknown starting scene fails clearly
- duplicate scene IDs fail clearly
- unknown exit targets fail clearly
- duplicate item IDs fail clearly
- unknown pickup items fail clearly
- unknown recipe ingredients/results fail clearly
- unknown item-use requirements/results fail clearly
- duplicate stable pickup/interaction IDs fail clearly

### Persistent world state

- new state has no collected pickups or completed interactions
- repeated collection is idempotent
- repeated completion is idempotent
- recreated scenes hide already-collected pickups
- recreated scenes restore completed interactions

### Stateless item use

- definitions do not store hidden completion state
- completion is read from `GameState`
- semantic world facts use flags
- local one-time completions use interaction IDs
- NPC and hotspot priority is:

```txt
matching flag > completed interaction > default content
```

### Recipe transactions

- valid recipe succeeds
- invalid pair leaves inventory unchanged
- missing ingredient cannot partially mutate inventory
- existing-result-item behavior is explicit
- recipe operation can be tested without rendering

### Interaction service

- pickup, inspect, item use, NPC dialogue, and exits are covered
- returned presentation outcome agrees with state mutation
- service tests do not require drawing

### Target resolution

- inventory UI wins over world targets
- world priority is:

```txt
NPC > exit > item pickup > hotspot
```

- empty space resolves to no target
- collected pickups do not resolve
- click and hover resolve the same world target
- exits have hover feedback

### UI helpers

- shared text wrapping handles short text, wrapped text, blank text, and long words
- `InventoryBar` drawing and hit testing use the same layout result
- planned maximum visible inventory size remains inside the fixed-window layout

## Manual test checklist

Run after each milestone or meaningful refactor:

```txt
- Start the game and confirm the title screen appears.
- Check title art, title/subtitle spacing, and button hover/selection states.
- Start with mouse, then restart and verify keyboard Start works.
- Confirm title Quit and Esc close cleanly.
- Start again and confirm Village Square appears.
- Talk to Retired Witch.
- Advance and close dialogue.
- Collect Empty Cup.
- Select Empty Cup in InventoryBar.
- Use Empty Cup on Old Well.
- Confirm Cup of Water appears and Empty Cup is removed.
- Travel to Forest Path.
- Confirm tower is locked before helping the witch.
- Collect Moon Herb.
- Select Cup of Water in InventoryBar.
- Click Moon Herb to combine.
- Confirm Glowing Tea appears and ingredients are removed.
- Return to Village Square.
- Give Glowing Tea to Retired Witch.
- Confirm Rusty Key appears and Glowing Tea is removed.
- Confirm witch dialogue/content changes.
- Return to Forest Path.
- Select Rusty Key in InventoryBar.
- Use Rusty Key on Tower Gate.
- Confirm tower exit is usable.
- Enter tower.
- Confirm the Ancient Tower appears behind the Demo Complete overlay.
- Check ending text and Play Again / Quit button spacing.
- Choose Play Again and confirm a fresh game starts.
- Complete or simulate the ending again and confirm Quit closes cleanly.
- Press N during a run.
- Confirm a fresh game starts from Village Square.
- Confirm inventory, flags, collected pickups, completions, and ending state are reset.
- Confirm hover prompts, long dialogue, and messages wrap readably without overlapping inventory.
- Confirm every included image is scaled cleanly and each label remains readable.
- Confirm pickup, dialogue, unlock, and transition sounds are audible but not harsh or clipped.
- Temporarily rename one image and one sound; confirm fallback visuals/silence do not crash the game.
- Confirm clicking each visible inventory row selects the matching item.
```

## Development rule

For every implemented refactor step, record:

```txt
Changed files
Automated tests run
Manual checks to perform
Known issues or intentional behavior
```

Keep tests close to the behavior they protect. Avoid testing private helpers unless the helper is a deliberately small boundary such as text wrapping, item combination, JSON loading, state snapshots, or target resolution.
