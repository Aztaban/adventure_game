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

## How to play

- Choose **Start Game** on the title screen.
- Move the mouse over people, objects, items, and exits to see the available action.
- Left-click an NPC to talk.
- Left-click an object to inspect it.
- Left-click a pickup to add it to the inventory.
- Left-click an inventory item to select it.
- Click a second inventory item to try combining them.
- With an item selected, click a person, object, or locked exit to use it there.
- Advance dialogue with left-click, `Space`, or `Enter`.
- Close dialogue or clear an inventory selection with `Esc`.
- Press `N` at any time to start a completely fresh game.
- On the ending screen, choose **Play Again** or **Quit**.

## Demo objective

```txt
Empty Cup -> Old Well -> Cup of Water
Cup of Water + Moon Herb -> Glowing Tea
Glowing Tea -> Retired Witch -> Rusty Key
Rusty Key -> Tower Gate -> enter the tower
```

## Checks

```bash
make check
```

This runs Ruff and the complete pytest suite.

## Presentation assets

The current art and sound files are intentionally replaceable placeholders. See:

```txt
docs/asset-guide.md
```

Missing optional images or sounds fall back safely instead of stopping the game.

## Documentation

Start with:

```txt
docs/gdd.md
docs/mvp.md
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
