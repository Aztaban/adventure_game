# Game Design Document

Status: draft  
Working title: TBD  
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
- possible depth sorting later
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
click objects/NPCs
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
- move between scenes
- complete simple quest

Future player actions:

- use magic
- unlock skills/abilities
- fight enemies
- solve optional side quests
- level up

## 6. Movement

### MVP movement

For the first prototype, movement can be simplified.

Allowed MVP behavior:

```txt
click hotspot -> interaction happens
click exit -> change scene
```

The player character does not need real walking/pathfinding in the first version.

### Later movement

Later versions may add:

- click-to-move
- walking animation
- straight-line movement to target
- navigation areas
- simple pathfinding

Keyboard movement is optional and not the main target.

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

Later, a scene may be larger than the screen and use a camera.

Recommended path:

```txt
MVP: one-screen scenes
Later: larger scenes with camera
Much later: larger world exploration
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
cup + moon_herb = glowing_tea
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
4 items
1 item combination
1 locked obstacle
1 small quest
1 ending condition
```

Possible first quest:

The player wants to enter a cursed tower.

Obstacle:

```txt
The tower door is locked by a dramatic magical lock.
```

Quest chain:

```txt
Talk to retired witch.
Find cup.
Find moon herb.
Combine cup + moon herb = glowing tea.
Give glowing tea to witch.
Witch gives rusty key.
Use rusty key on tower door.
Demo ends.
```

## 18. Future expansion ideas

Future features after MVP:

- more scenes
- dialogue choices
- quest journal
- save/load
- larger scenes with camera
- click-to-move animation
- magic puzzles
- optional skills
- simple combat
- sound/music
- better art
- 2.5D visual polish
