# Testing Plan

Project: Funny mysterious fantasy adventure game  
Initial test approach: simple pytest + manual gameplay testing

## 1. Purpose

This document defines how the project should be tested during development.

The goal is not to build a heavy custom test framework at the beginning. The goal is to keep testing simple, useful, and easy to run while the game grows step by step.

## 2. Testing philosophy

The project has two different kinds of behavior:

```txt
game logic      -> good for automated pytest tests
game feel / UI  -> better for manual testing
```

Automated tests should focus on pure logic that can be tested without opening a Pygame window.

Manual tests should be used for gameplay, visuals, mouse interaction, scene layout, and overall feeling.

## 3. Current test setup

Recommended initial structure:

```txt
tests/
├── __init__.py
└── test_placeholder.py
```

Initial placeholder test:

```python
def test_placeholder() -> None:
    assert True
```

This test does not test game logic yet. It only confirms that pytest is installed and that the test command works.

## 4. How to run tests

Using Makefile:

```bash
make test
```

Direct command:

```bash
PYTHONPATH=src .venv/bin/python -m pytest
```

Expected output at the beginning:

```txt
1 passed
```

## 5. What should be automated

Use pytest for systems that are mostly independent of rendering.

Good candidates:

```txt
inventory
recipes / item combining
quest flags
dialogue state
scene transition rules
save/load data later
```

## 6. What should be tested manually

Use manual testing for Pygame/gameplay behavior.

Manual testing is better for:

```txt
window opens correctly
ESC / close button exits cleanly
mouse clicks work
hotspot hover/click feels correct
dialogue box is readable
inventory UI is visible
scene transitions feel correct
placeholder objects are positioned reasonably
game can be completed from start to ending
```

## 7. Milestone testing checklist

### v0.1 — Window and game loop

Manual test:

```txt
- Run the game.
- Window opens.
- Background is drawn.
- ESC exits cleanly.
- Close button exits cleanly.
- No crash in terminal.
```

Automated test:

```txt
- Placeholder test only.
```

### v0.2 — Scene system

Manual test:

```txt
- Game starts in first scene.
- Scene name/background is visible.
- Clicking an exit changes to another scene.
- Scene change does not crash.
```

Possible automated tests later:

```txt
- SceneManager starts with expected scene.
- SceneManager can switch to valid scene id.
- Invalid scene id is handled safely.
```

### v0.3 — Hotspots

Manual test:

```txt
- Hotspot is visible or debug-visible.
- Mouse click on hotspot triggers interaction.
- Clicking outside hotspot does nothing.
- Interaction text appears.
```

Possible automated tests later:

```txt
- Hotspot detects point inside rectangle.
- Hotspot rejects point outside rectangle.
```

### v0.4 — Dialogue box and NPCs

Manual test:

```txt
- Clicking NPC opens dialogue.
- Dialogue text is readable.
- Dialogue can advance.
- Dialogue can close.
```

Possible automated tests later:

```txt
- Dialogue starts at first line.
- Dialogue advances to next line.
- Dialogue reports finished at the end.
```

### v0.5 — Inventory

Manual test:

```txt
- Clicking item picks it up.
- Item appears in inventory.
- Item disappears from scene after pickup.
- Same item cannot be picked up twice.
```

Automated tests:

```txt
- Inventory can add item.
- Inventory can check if item exists.
- Inventory can remove item.
- Duplicate behavior is defined and tested.
```

### v0.6 — Use item on hotspot/NPC

Manual test:

```txt
- Select inventory item.
- Use wrong item on hotspot.
- Failure text appears.
- Use correct item on hotspot.
- Progress changes.
```

Automated tests:

```txt
- Required item check succeeds with correct item.
- Required item check fails with wrong item.
```

### v0.7 — Item combining

Manual test:

```txt
- Inventory contains empty_cup and moon_herb.
- Combine them.
- Inventory removes input items.
- Inventory adds glowing_tea.
- Invalid combination shows failure message.
```

Automated tests:

```txt
- empty_cup + moon_herb returns glowing_tea.
- moon_herb + empty_cup also works if combinations are order-insensitive.
- Invalid combination returns None or a defined failure result.
```

### v0.8 — Quest flags

Manual test:

```txt
- Obstacle blocks progress before quest flag.
- Completing quest sets the correct flag.
- Obstacle reacts differently after flag is set.
```

Automated tests:

```txt
- Quest flag can be set.
- Quest flag can be checked.
- Unknown flag is false by default.
```

### v0.9 — First complete demo

Manual test:

```txt
- Start game from beginning.
- Visit all MVP scenes.
- Talk to required NPC.
- Collect required items.
- Combine required items.
- Give/use required item.
- Unlock final obstacle.
- Reach ending message/screen.
```

Automated tests:

```txt
- Core inventory/recipe/flag logic passes.
```

## 8. Suggested future test files

Once the systems exist, add:

```txt
tests/
├── __init__.py
├── test_inventory.py
├── test_recipes.py
├── test_quests.py
├── test_dialogue.py
└── test_scene_manager.py
```

Do not create all of these before the systems exist. Add them when useful.

## 9. Example future inventory test

```python
from game.systems.inventory import Inventory


def test_inventory_adds_item() -> None:
    inventory = Inventory()

    inventory.add("rusty_key")

    assert inventory.has("rusty_key")
```

## 10. Example future recipe test

```python
from game.systems.recipes import combine_items


def test_combines_cup_and_moon_herb() -> None:
    result = combine_items("empty_cup", "moon_herb")

    assert result == "glowing_tea"
```

## 11. Example future quest flag test

```python
from game.systems.quests import QuestFlags


def test_quest_flag_can_be_set() -> None:
    flags = QuestFlags()

    flags.set("door_unlocked")

    assert flags.has("door_unlocked")
```

## 12. What not to test automatically at first

Do not spend time writing automated tests for:

```txt
Pygame rendering
exact pixel positions
visual polish
animation smoothness
sound playback
game feel
complex mouse/UI flows
```

These are better checked manually during early development.

## 13. HTML test report

A custom HTML report is not needed at the start.

For now, use:

```bash
make test
```

A custom report can be added later if the project becomes larger, but it is currently unnecessary.

## 14. Recommended development rule

After every implemented milestone, the agent or developer should provide:

```txt
Changed files:
- ...

Manual test steps:
- ...

Automated tests:
- ...

Known issues:
- ...
```

## 15. Current status

```txt
pytest setup: planned
custom test runner: not needed
HTML report: not needed
manual milestone checklist: required
real automated tests: add when systems exist
```
