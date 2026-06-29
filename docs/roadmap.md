# Roadmap

Status: draft

## Development principle

Each milestone should be small and manually testable.

Do not skip ahead.

## Milestone v0.1 — Window and game loop

Goal:

```txt
Open a game window and run a stable loop.
```

Features:

- create project structure
- open Pygame window
- handle quit/ESC
- draw simple background
- show FPS/title if useful

Manual test:

```txt
Run game.
Window opens.
ESC or close button exits cleanly.
```

## Milestone v0.2 — Scene system

Goal:

```txt
Display one scene and allow switching to another scene.
```

Features:

- scene manager
- scene class/data
- two placeholder scenes
- clickable exit hotspot
- scene transition

Manual test:

```txt
Click exit.
Scene changes.
No crash.
```

## Milestone v0.3 — Hotspots

Goal:

```txt
Clickable objects can show interaction text.
```

Features:

- hotspot rectangles
- mouse hover/click detection
- inspect text
- simple interaction result

Manual test:

```txt
Click object.
Text appears.
```

## Milestone v0.4 — Dialogue box and NPCs

Goal:

```txt
NPC can display dialogue.
```

Features:

- NPC hotspot
- dialogue box UI
- advance dialogue with click/key
- close dialogue

Manual test:

```txt
Click NPC.
Dialogue appears.
Advance and close it.
```

## Milestone v0.5 — Inventory

Goal:

```txt
Player can pick up items and see inventory.
```

Features:

- item hotspot
- inventory data structure
- inventory UI text/list
- remove item from scene after pickup

Manual test:

```txt
Click item.
Item appears in inventory.
Item disappears from scene.
```

## Milestone v0.6 — Use item on hotspot/NPC

Goal:

```txt
Selected inventory item can be used on object/NPC.
```

Features:

- select item
- use selected item on hotspot
- success/failure message
- required item logic

Manual test:

```txt
Use wrong item.
Get failure text.
Use correct item.
Progress changes.
```

## Milestone v0.7 — Item combining

Goal:

```txt
Two inventory items can combine into a new item.
```

Features:

- simple recipe system
- combine command/action
- remove input items
- add result item

Manual test:

```txt
Combine empty_cup + moon_herb.
Inventory now contains glowing_tea.
```

## Milestone v0.8 — Quest flags

Goal:

```txt
Game can track progress through flags.
```

Features:

- flag storage
- dialogue/hotspots react to flags
- obstacle unlock state
- demo completion flag

Manual test:

```txt
Before quest item, obstacle blocks.
After correct quest, obstacle unlocks.
```

## Milestone v0.9 — First complete demo

Goal:

```txt
Playable beginning-to-end mini adventure.
```

Features:

- 3 scenes
- 2 NPCs
- 4 items
- 1 item combination
- 1 obstacle
- ending screen/message

Manual test:

```txt
Start new game.
Complete full quest.
Reach ending.
```

## Milestone v0.10 — Polish pass

Goal:

```txt
Make the prototype nicer to play.
```

Possible features:

- better placeholder art
- hover labels
- simple menu
- improved dialogue UI
- basic sound effects
- better scene layout
- README instructions

## Future milestones

Only after MVP:

```txt
v0.11 save/load
v0.12 dialogue choices
v0.13 quest journal
v0.14 camera for larger scenes
v0.15 click-to-move character
v0.16 real assets pass
v0.17 magic puzzle ability
v0.18 simple skill/ability progression
v0.19 combat prototype research
```
