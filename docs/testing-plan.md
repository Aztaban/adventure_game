# Testing Plan

Status: current for v0.8.1

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
- game state flags, collected pickups, and completed interactions
- recipe lookup and item-combination transactions
- item-use success/failure/completion behavior
- content validation
- scene manager transitions
- dialogue state
- interaction service outcomes
- target resolution priority
- UI helper geometry and text wrapping
- complete demo-flow integration

Manual testing should cover:

- window opens and closes correctly
- hover/click feel
- readability of dialogue and message boxes
- object positions and spacing
- whether the flow feels understandable
- visual regressions
- long text readability

Do not over-test exact pixels unless the layout rule is important for behavior.

## Current automated test groups

```txt
tests/
├── integration/
│   ├── test_demo_flow.py
│   └── test_world_state_persistence.py
├── test_adventure_interaction_service.py
├── test_adventure_scene.py
├── test_content_validation.py
├── test_dialogue.py
├── test_exit_hotspot.py
├── test_game_state.py
├── test_hotspot.py
├── test_input_bindings.py
├── test_inventory.py
├── test_inventory_bar.py
├── test_item_combination.py
├── test_item_hotspot.py
├── test_item_use.py
├── test_npc.py
├── test_quest_flags.py
├── test_recipe.py
├── test_scene_event_result.py
├── test_scene_manager.py
└── test_text_wrapping.py
```

Add new test files only when they describe a real boundary.

## Full demo-flow integration test

`tests/integration/test_demo_flow.py` protects the current v0.8.1 playable path using real demo content.

It covers:

```txt
Village Square
→ collect Empty Cup
→ Forest Path
→ verify tower is locked
→ collect Moon Herb
→ combine Empty Cup + Moon Herb into Glowing Tea
→ return to the witch
→ give Glowing Tea to the witch
→ verify WITCH_RECEIVED_TEA and TOWER_UNLOCKED
→ return to Forest Path
→ enter tower
→ verify DEMO_COMPLETED
```

This test currently reflects the v0.8.1 implementation, where the witch unlocks the tower directly after receiving tea.

The intended v0.9 story flow will add the rusty key step:

```txt
Glowing Tea -> Retired Witch -> Rusty Key -> Tower Gate -> ending
```

When that feature is implemented, update the demo-flow integration test at the same time.

## v0.8.1 regression checklist

Automated coverage should protect these behaviors before further feature work:

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
- unknown item-use requirements fail clearly
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
- Start the game.
- ESC and window close still quit cleanly.
- Talk to Retired Witch.
- Advance and close dialogue.
- Collect Empty Cup.
- Travel to Forest Path.
- Confirm tower is locked before helping the witch.
- Collect Moon Herb.
- Select Empty Cup in InventoryBar.
- Click Moon Herb to combine.
- Confirm Glowing Tea appears and ingredients are removed.
- Return to Village Square.
- Give Glowing Tea to Retired Witch.
- Confirm witch dialogue/content changes.
- Return to Forest Path.
- Confirm tower exit is usable.
- Enter tower.
- Confirm ending/progress text appears.
- Confirm long dialogue and messages wrap readably.
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

Keep tests close to the behavior they protect. Avoid testing private helpers unless the helper is a deliberately small boundary such as text wrapping, item combination, or target resolution.
