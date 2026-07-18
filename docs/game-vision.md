# Game Vision

Status: long-term direction; implementation decisions remain milestone-gated

## Goal

Build a solid, humorous 2D point-and-click adventure inspired by the authored puzzle and dialogue feel associated with games such as *Polda*.

The project should develop its own world, characters, writing, art, interface, and interaction details. The reference describes the desired genre and player experience, not content to copy.

## Experience pillars

### Authored comedy and mystery

- memorable characters with distinct voices
- inspectable environments with optional jokes and clues
- a coherent mystery that grows across connected scenes
- dialogue that rewards curiosity without blocking progress unnecessarily

### Clear point-and-click interaction

- visible targets and readable feedback
- predictable inspect, talk, collect, combine, and use behavior
- inventory puzzles based on authored logic rather than generic crafting
- controls that can always be viewed from the menu
- interaction rules that remain consistent across scenes

### Deliberate puzzle progression

- short dependency chains with understandable causes and effects
- stable world facts and conversation outcomes
- objective hints or a journal before the game becomes large enough to feel directionless
- no puzzle solution should depend on hidden pixel hunting or undocumented controls

### Strong presentation without engine overgrowth

- fixed logical composition that scales cleanly to modern displays
- readable dialogue, prompts, menus, and inventory
- art and audio loaded through stable IDs
- feature-driven refactors instead of speculative abstract frameworks

## Current proven core

The v0.10 vertical slice proves:

```txt
explore scene
talk and inspect
collect item
use item on world target
combine items
unlock progression
reach ending
restart a fresh session
```

Current architecture already separates reusable content, one running session, persistent game state, interaction transactions, scene presentation, and snapshot data. This is sufficient to continue without a general rewrite.

## Important undecided interaction details

These decisions materially affect player behavior and must be made through milestone prototypes rather than documentation alone.

### Input language

Decide during v0.15:

- one contextual left-click action
- left-click action plus right-click inspect
- verb or cursor modes
- whether a selected inventory item visibly follows the cursor

### Player movement

Decide during v0.16:

- instant interaction from anywhere
- visible move-then-interact behavior
- simple authored walk areas
- pathfinding only if scene layouts require it

### Scene size

Decide during v0.15:

- continue using one-screen authored scenes
- support larger scenes with a camera
- mix both approaches under one coordinate policy

### Content data

Current rule:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

Future decisions:

- reconsider dialogue JSON only after v0.13 choices prove the schema
- reconsider scene JSON only after v0.15/v0.17 representative scene pilots
- prefer data files when they improve authoring and validation, not merely to reduce Python usage

## Scale strategy

The game should grow by proving one pressure point at a time:

```txt
logical display/input
-> pause and save/load
-> dialogue choices
-> objectives
-> interaction/camera pilot
-> player movement decision
-> production asset and inventory pilot
-> music/ambience
-> packaging/settings
-> larger chapter production
```

Each feature milestone may be followed by a focused `.1` refactor milestone. Refactors must solve observed duplication, ownership, or scalability problems while preserving behavior.

## Scope guard

The project is not currently aiming to become:

- a combat RPG
- a generic adventure-game engine
- an entity-component framework
- a procedural world generator
- a universal modding platform
- a complex crafting simulator

Those directions should not displace the authored point-and-click experience without a deliberate future design change.
