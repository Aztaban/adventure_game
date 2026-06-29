# MVP

Status: draft

## MVP goal

Build the smallest playable adventure prototype that proves the core loop.

The MVP should not be a full RPG.

## One-sentence MVP

The player can explore a few scenes, talk to an NPC, collect and combine items, use the result to solve an obstacle, and finish the demo.

## MVP core loop

```txt
open game
enter scene
click NPC/object
read dialogue
collect item
combine items
use item on obstacle/NPC
unlock progress
finish demo
```

## MVP scope

### Required

- Game window opens
- Scene system
- At least 3 scenes
- Clickable hotspots
- Scene transitions through exits
- At least 2 NPCs
- Basic dialogue box
- At least 4 items
- Basic inventory
- Select/use item
- Combine at least 2 items into 1 new item
- One simple quest
- One locked obstacle
- One ending condition

### Allowed simplifications

- No walking animation required
- No pathfinding required
- No real art required
- No sound required
- No save/load required
- No polished UI required
- Placeholder rectangles/images are fine

## Hard non-goals for MVP

Do not implement these in MVP:

- combat
- magic combat
- character levels
- skill tree
- 3D graphics
- procedural generation
- many maps
- complex crafting system
- full quest journal
- advanced animation
- pathfinding
- real asset pipeline

## MVP demo example

### Scenes

```txt
village_square
forest_path
tower_entrance
```

### NPCs

```txt
retired_witch
mushroom_guard
```

### Items

```txt
empty_cup
moon_herb
glowing_tea
rusty_key
```

### Puzzle

```txt
empty_cup + moon_herb = glowing_tea
glowing_tea -> retired_witch = rusty_key
rusty_key -> tower_door = unlock ending
```

## MVP acceptance criteria

The MVP is done when:

- the game starts without errors
- the player can move between at least 3 scenes
- the player can interact with NPCs and objects
- the player can pick up items
- the player can see inventory contents
- the player can combine two items
- the player can use an item on an NPC or obstacle
- the game can track quest progress
- the player can finish the demo
