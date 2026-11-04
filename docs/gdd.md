# Game Design Document

Status: current product direction revised 2026-11-04; movement/animation are planned, not implemented  
Working title: Mysterious Forest  
Genre: funny mysterious fantasy adventure  
Initial style: 2D / 2.5D point-and-click adventure  
Initial implementation target: Python + Pygame

## 1. High concept

A funny mysterious fantasy adventure where the player explores strange places, talks to eccentric NPCs, collects and combines items, solves absurd magical obstacles, and slowly uncovers a larger mystery.

The game should feel like a classic adventure game with RPG flavor, but the first prototype should stay small.

## 2. Design direction

### Main target

```txt
2D / 2.5D scene-based point-and-click adventure
```

The game should start as a simple 2D prototype and may later visually move toward a 2.5D/classic adventure style.

2.5D in this project means:

- painted or pre-rendered backgrounds
- 2D characters
- clickable objects/hotspots
- fake depth
- foot-anchor depth sorting and explicit foreground occlusion in the animation pilot
- scene transitions instead of full open-world movement

### Not the current target

```txt
Full 3D RPG
```

A future 3D remake is possible, but this project should not be designed around converting the first prototype directly into 3D.

## 3. Tone

The tone should be:

```txt
funny
mysterious
fantasy
slightly absurd
cozy but strange
```

The world can be magical and mysterious, but NPCs should often react to magic in a practical, annoying, or bureaucratic way.

Example tone:

```txt
The forest is cursed, but the local mushroom clerk still needs Form 7B before opening the gate.
```

## 4. Core gameplay loop

```txt
enter scene
look around
choose destination or world target
walk to a reachable interaction point
talk to NPCs
collect items
combine or use items
solve obstacle
unlock new scene or story step
```

## 5. Player actions

Initial player actions:

- inspect object
- talk to NPC
- pick up item
- use inventory item on hotspot/NPC
- combine two inventory items
- move with held arrow keys or click-to-move across a 2D floor
- approach world targets before interacting once the movement rollout is complete
- move between scenes through reachable exits
- complete simple quest

Uncommitted future ideas (outside the active roadmap):

- use magic
- unlock skills/abilities
- fight enemies
- solve optional side quests
- level up

## 6. Movement and interaction

### Agreed experience

The player is a visible 2D character standing on a floor area with depth, in the
visual spirit of Polda-like adventures. Both horizontal and vertical movement on
the floor are required; this is not limited to a left/right platforming lane.

- Hold arrow keys to move continuously.
- Left-click walkable ground to walk toward that position.
- Left-click an NPC, pickup, inspectable object, or exit to approach and then interact.
- Select an inventory item and click a world target to approach and use it in range.
- Inventory selection and combining inventory items do not require walking.
- Dialogue and menus consume input before movement or world interactions.

### Space and reachability

A scene needs authored walkable ground, blocking geometry, a default spawn, and
reachable approach points/areas for its targets. Visual rectangles, clickable
rectangles, interaction areas, and actor collision footprints are different concepts.
The player's logical position is the foot anchor, not the sprite's centre.

The route must stay inside walkable ground and avoid obstacles. Prove a simple
obstacle detour in the pilot before selecting broader routing machinery. Unreachable
targets never trigger remote interactions. Exact floor/routing representation and
failure wording are open decisions, recorded in [decisions](decisions.md).

### Commands, cancellation, and feedback

The intended sequence is target selection, travel, arrival/range revalidation, then
one interaction. A pending action must not execute early, twice, after its target
has disappeared, or using an inventory item that is no longer selected/available.
Proposed cancellation defaults are in OPEN-05; confirm them before implementation.
Keep the existing Escape modal order while adding movement; pause must stop travel.
F11 only changes presentation and must preserve the session.

### Phased delivery

- v0.13: one-scene navigation pilot with placeholder player art. It is an internal
  prototype, not full movement support for the demo or a new public save contract.
- v0.14: range-gated world interactions, all demo scenes, explicit exit entry points,
  and movement-aware saves. Older supported saves preserve progress and use default spawn.
- v0.15: directional idle/walk animation, scene occlusion, and small ambient animations.

The original MVP intentionally used immediate remote clicks. That historical
simplification does not describe the intended post-v0.14 behavior.

## 7. World structure

The game should use scenes.

A scene is one location, such as:

- village square
- forest path
- old well
- witch hut
- tower entrance

Each scene can contain:

- background
- exits
- NPCs
- items
- locked obstacles
- inspectable objects
- quest-related hotspots

### Scene size

MVP scenes should fit one screen.

Keep single-screen scenes through the movement and animation pilots. Larger scenes and a camera are deferred until content demonstrates a need.

Recommended path:

```txt
Current demo and movement pilots: one-screen scenes
Later evidence-gated experiment: larger scenes with camera
No open-world expansion is currently committed
```

## 8. Hotspots

Hotspots are clickable areas in a scene.

Types:

- item
- NPC
- exit
- locked obstacle
- inspectable object
- quest trigger

Hotspots should be central to the architecture.

Example hotspot data:

```txt
id: tower_door
name: Tower Door
type: obstacle
description: A tall door covered in dramatic-looking runes.
required_item: rusty_key
on_success: unlock_tower
on_failure: show_dialogue("The door ignores your lack of key.")
```

## 9. NPCs and dialogue

NPCs should be important.

NPCs can:

- give information
- give quests
- react to items
- block progress
- provide jokes/worldbuilding
- change dialogue based on quest flags

Initial dialogue can be simple linear text.

Later dialogue may include choices.

Example NPC style:

```txt
A tired witch who insists she is retired, but still keeps accidentally cursing furniture.
```

## 10. Inventory

The player should have an inventory.

MVP inventory:

- collect items
- display item list
- select item
- use selected item on hotspot/NPC
- combine two items through simple logic

Do not build a complex RPG inventory in the first version.

Future inventory improvements:

- item icons
- item descriptions
- drag-and-drop
- item categories
- quest items vs optional items

## 11. Item combining / crafting

The first version should use adventure-style item combining, not full crafting.

Good examples:

```txt
water_cup + moon_herb = glowing_tea
stick + string = fishing_rod
empty_bottle + fairy_dust = glowing_bottle
```

Avoid early:

- crafting grid
- resource farming
- many materials
- durability
- complex recipe UI

## 12. Quests

MVP quests should be simple.

Use quest flags first.

Example flags:

```txt
talked_to_witch = true
has_moon_herb = true
made_glowing_tea = true
door_unlocked = true
```

Future versions may add a quest journal.

## 13. Magic

Magic should exist in the world, but not as combat in MVP.

Early magic should be puzzle/flavor based:

- reveal hidden text
- open magical lock
- translate mushroom speech
- brew potion
- change NPC dialogue

Future magic could include:

- spells
- combat
- skill-based progression
- puzzle abilities

## 14. Combat

Combat is not part of MVP.

Combat may be added later if the prototype is stable.

Open questions:

- Should combat be turn-based?
- Should combat be real-time?
- Should combat be puzzle-based?
- Should magic be the main combat system?

Until decided, combat should remain a future feature.

## 15. Levels and skills

Levels/skills are not part of MVP.

Instead of numeric levels, early progression should use abilities/items/knowledge.

Example:

```txt
Player learns Mushroom Language.
Player unlocks Minor Illusion.
Player gets Ancient Lockpicking Certificate.
```

This gives progression without building a full RPG leveling system.

## 16. Assets

Real assets are not required at the start.

MVP can use:

- colored rectangles
- placeholder backgrounds
- temporary text labels
- simple shapes
- free placeholder sprites later

The code should not depend on final art.

## 17. First demo concept

A small demo should contain:

```txt
3 scenes
2 NPCs
5 items
1 item combination
1 locked obstacle
1 small quest
1 ending condition
```

Implemented first quest:

```txt
Find Empty Cup; fill it at the Old Well to obtain Cup of Water.
Collect Moon Herb; combine it with Cup of Water to make Glowing Tea.
Give Glowing Tea to the Retired Witch; receive Rusty Key.
Use Rusty Key on the tower gate; enter Ancient Tower; finish the demo.
```

Movement changes how the player reaches these interactions, not the puzzle solution.

## 18. Future expansion ideas

Future features after MVP:

- more scenes
- dialogue choices
- quest journal
- save/load
- larger scenes with camera only after a dedicated evidence-gated pilot
- richer interaction animation after the v0.15 idle/walk pilot
- magic puzzles
- optional skills
- simple combat
- sound/music
- better art
- 2.5D visual polish

## 19. Animation and a lively scene

v0.15 proves a small coherent visual set: directional idle and walk clips, a stable
foot anchor, consistent movement/animation timing, and one or two ambient loops
such as foliage, a lantern, smoke, or water. Gameplay completion must not depend on
an ambient animation frame. Full NPC schedules, cinematic cutscenes, skeletal
animation, and universal animation tooling are not part of this pilot.

## 20. Status and plan references

Current v0.12 code implements persistence foundations and a load method, but not
pause/confirmation/Continue screens. This document states the target design; see
[roadmap](roadmap.md) for actual progress and [architecture](architecture.md) for
implemented versus planned responsibilities. Dialogue choices now follow movement
and animation at v0.16; older forward references to v0.13 are superseded.
