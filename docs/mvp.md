# MVP

Status: historical v0.9 MVP contract; revised movement is a post-MVP requirement (2026-11-04)

## MVP goal

Build the smallest playable adventure prototype that proves the core loop.

The MVP should not be a full RPG.

## One-sentence MVP

The player can explore a few scenes, talk to NPCs, collect and combine items, use the result to solve an obstacle, and finish the demo.

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

## Current v0.9 MVP

v0.9 completes the first intended story loop:

```txt
empty cup -> old well -> cup of water
cup of water + moon herb -> glowing tea
glowing tea -> retired witch -> rusty key
rusty key -> tower gate -> finish demo
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
- At least 5 story-relevant items by v0.9
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
- No full save/load menu required yet
- No polished UI required
- Placeholder rectangles/images are fine
- Full scene/dialogue JSON is not required yet

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
- full scene JSON loader before scene schema is proven
- dialogue JSON before the rescheduled v0.16 dialogue-choice pilot stabilizes

## MVP demo example for v0.9

### Scenes

```txt
village_square
forest_path
tower_interior
```

The current in-game scene name is `Ancient Tower`.

### NPCs

```txt
retired_witch
mushroom_guard
```

### Items

```txt
empty_cup
moon_herb
water_cup
glowing_tea
rusty_key
```

### Puzzle

```txt
empty_cup -> old_well = water_cup
water_cup + moon_herb = glowing_tea
glowing_tea -> retired_witch = rusty_key
rusty_key -> tower_gate = unlock tower
enter tower = finish demo
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
- the full demo-flow integration test protects the intended v0.9 path


## MVP content format

Current supported formats:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

This is enough for the MVP. Full scene/dialogue JSON is deferred until there is enough content and a stable enough schema to justify it. Dialogue JSON should be reconsidered after the rescheduled v0.16 dialogue-choice pilot.

## Post-MVP movement direction

The no-walking/no-pathfinding simplifications above describe the original MVP.
The owner now requires a visible player on a 2D floor, held arrow movement,
click-to-move, proximity-gated world interaction, and later player/ambient animation.
These are staged through v0.13-v0.15, not retroactive requirements for v0.9.
Keep the proven cup/herb/tea/key puzzle as the movement regression route.
See [GDD](gdd.md), [decisions](decisions.md), and [roadmap](roadmap.md).
