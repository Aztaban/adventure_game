# Architecture

Status: draft

## Goal

Create a simple Python/Pygame architecture that supports a small adventure game without becoming a huge engine.

The code should be easy to understand and easy for an AI agent to modify step by step.

## Proposed project structure

```txt
.
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── game/
│   │   ├── app.py
│   │   ├── settings.py
│   │   ├── scene_manager.py
│   │   ├── scenes/
│   │   │   ├── base_scene.py
│   │   │   └── adventure_scene.py
│   │   ├── entities/
│   │   │   ├── hotspot.py
│   │   │   ├── npc.py
│   │   │   └── item.py
│   │   ├── systems/
│   │   │   ├── inventory.py
│   │   │   ├── dialogue.py
│   │   │   ├── quests.py
│   │   │   └── recipes.py
│   │   ├── ui/
│   │   │   ├── dialogue_box.py
│   │   │   └── inventory_bar.py
│   │   └── assets.py
│   └── data/
│       ├── scenes/
│       ├── dialogue/
│       ├── items.json
│       └── recipes.json
├── assets/
│   ├── images/
│   ├── audio/
│   └── fonts/
└── tests/
```

This structure can be simplified during early milestones if needed.

## Main modules

### `main.py`

Responsibilities:

- start the app
- keep file small
- avoid game logic here

### `game/app.py`

Responsibilities:

- initialize Pygame
- create window
- run main loop
- handle global events
- update current scene
- draw current scene

### `game/scene_manager.py`

Responsibilities:

- hold current scene
- switch scenes
- pass shared game state between scenes

### `game/scenes/`

Responsibilities:

- represent locations/screens
- contain hotspots/NPCs/items
- handle scene-specific interactions

### `game/entities/hotspot.py`

Responsibilities:

- rectangle/clickable area
- name/description
- interaction callback or action id

### `game/systems/inventory.py`

Responsibilities:

- store items
- add/remove/check item
- select active item
- combine items

### `game/systems/dialogue.py`

Responsibilities:

- store current dialogue
- advance dialogue
- close dialogue
- later support choices

### `game/systems/quests.py`

Responsibilities:

- track flags
- check/set flags
- expose simple state to scenes/dialogue

### `game/systems/recipes.py`

Responsibilities:

- define item combinations
- combine two item ids into result item id

### `game/ui/`

Responsibilities:

- draw dialogue box
- draw inventory
- draw hover text
- draw ending screen later

## Game state

Shared game state should include:

```txt
current_scene
inventory
quest_flags
selected_item
active_dialogue
```

Possible class:

```txt
GameState
├── inventory
├── flags
├── selected_item
└── completed
```

## Scene design

First scenes can be hardcoded Python objects.

Later scenes can be data-driven through JSON.

Example scene concept:

```txt
Scene
├── id
├── name
├── background
├── hotspots
├── exits
└── npcs
```

## Hotspot interaction model

A hotspot click can produce actions:

```txt
show_text
start_dialogue
pickup_item
change_scene
use_required_item
set_flag
finish_demo
```

Do not build a complex scripting system in MVP.

## Data-driven content

Recommended later, not required in v0.1.

Possible data files:

```txt
src/data/items.json
src/data/recipes.json
src/data/dialogue/retired_witch.json
src/data/scenes/village_square.json
```

## Rendering approach

MVP:

- draw colored backgrounds
- draw rectangles for hotspots/NPCs/items
- draw text labels
- draw inventory as text or simple boxes

Later:

- load background images
- load sprites
- animate player/NPCs
- add 2.5D depth sorting

## 2D to 3D note

The first prototype should not attempt to be directly convertible to 3D.

Reusable later:

- story
- item definitions
- quest flags
- dialogue
- recipes
- general game rules

Likely rewritten for 3D:

- rendering
- movement
- collision
- camera
- map format
- asset pipeline

## Dependency policy

Initial dependency:

```txt
pygame
```

Do not add other libraries unless there is a clear reason.
