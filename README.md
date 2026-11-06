# Adventure Game

Working title: **Mysterious Forest**

A small funny-mysterious fantasy point-and-click adventure built with Python and Pygame.

The complete demo loop is:

```txt
explore -> talk -> collect item -> combine/use item -> solve obstacle -> enter tower
```

## Requirements

- Python 3.11 or newer
- A desktop environment supported by Pygame

## Setup

```bash
make setup
```

This creates `.venv` and installs the game with its development tools.

## Run the game

```bash
make run
```

Or run it directly:

```bash
PYTHONPATH=src .venv/bin/python src/main.py
```

The game starts in fullscreen desktop mode. It renders through a fixed `1280 x 720` logical frame and scales the completed frame uniformly to the physical display. Non-16:9 displays use black letterbox or pillarbox space instead of stretching the game.

Press `F11` to toggle between fullscreen and windowed mode. The first windowed fallback is `1280 x 720`; after another approved preset is selected through the application API, `F11` returns to that preset for the current running session. Display choices are not saved between launches during v0.11.

Approved windowed sizes are:

```txt
1280 x 720
1600 x 900
1920 x 1080
```

A player-facing preset selector is not part of v0.11. Arbitrary drag-resizing and persistent display settings remain deferred.

## Controls

Choose **Controls** on the title screen to view the active bindings from the same catalog used by the game.

```txt
Left Click                   Interact / select item
Space / Enter / Numpad Enter Advance dialogue
Space / Enter / Numpad Enter Confirm menu action
Esc                          Cancel / Back
Up / W                       Move menu selection up
Down / S                     Move menu selection down
N                            Start a completely fresh game
F11                          Toggle fullscreen
```

Additional behavior:

- Choose **Start Game** on the title screen to begin in Village Square.
- Move the mouse over people, objects, items, and exits to see the available action.
- Left-click an NPC to talk.
- Left-click while dialogue is open to advance it.
- Left-click an object to inspect it.
- Left-click a pickup to add it to the inventory.
- Left-click an inventory item to select it.
- Click a second inventory item to try combining them.
- With an item selected, click a person, object, or locked exit to use it there.
- During gameplay, `Esc` closes dialogue first, clears an inventory selection next, and otherwise exits the current application.
- On the ending screen, choose **Play Again** or **Quit**.
- `N` starts a fresh game from title, Controls, gameplay, or ending modes.
- `F11` changes only the physical display mode and preserves the current menu, scene, dialogue, inventory selection, and progress.

## Demo objective

```txt
Empty Cup -> Old Well -> Cup of Water
Cup of Water + Moon Herb -> Glowing Tea
Glowing Tea -> Retired Witch -> Rusty Key
Rusty Key -> Tower Gate -> enter the tower
```

## Checks

```bash
make format
make check
```

`make format` applies the configured Ruff formatter. `make check` runs Ruff lint checks and the complete pytest suite.

## Presentation assets

The current art and sound files are intentionally replaceable placeholders. See:

```txt
docs/asset-guide.md
```

Missing optional images or sounds fall back safely instead of stopping the game. Runtime art is authored for the logical `1280 x 720` composition; the display layer scales the complete frame rather than loading separate assets for each physical resolution.

## Documentation

Start with:

```txt
docs/game-vision.md
docs/gdd.md
docs/decisions.md
docs/roadmap.md
docs/architecture.md
docs/testing-plan.md
docs/asset-guide.md
```

Agent instructions:

```txt
AGENTS.md
CLAUDE.md
```

## Scope rule

Work one milestone at a time. Do not expand the demo with additional quest chains while a presentation, architecture, or save milestone is in progress.
