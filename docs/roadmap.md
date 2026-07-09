# Roadmap

Status: current after v0.9 implementation

## Development principle

Each milestone should be small, testable, and playable.

Do not implement future systems before the current gameplay need exists.

## Completed milestones

### Milestone v0.1 — Window and game loop

Goal:

```txt
Open a game window and run a stable loop.
```

Delivered:

- Pygame window
- stable loop
- quit and ESC handling
- simple drawing baseline

### Milestone v0.2 — Scene system

Goal:

```txt
Display one scene and allow switching to another scene.
```

Delivered:

- `SceneManager`
- base scene interface
- placeholder adventure scenes
- exit-driven scene transitions

### Milestone v0.3 — Hotspots

Goal:

```txt
Clickable objects can show interaction text.
```

Delivered:

- inspectable hotspots
- hover detection
- click messages
- hotspot tests

### Milestone v0.4 — Dialogue box and NPCs

Goal:

```txt
NPCs can display dialogue.
```

Delivered:

- NPC entities
- dialogue state system
- dialogue box UI
- click, Space, and Enter advancement
- scene input consumption while dialogue is active

### Milestone v0.5 — Inventory

Goal:

```txt
Player can pick up items and see inventory.
```

Delivered:

- immutable item definitions
- item pickups
- player inventory
- inventory UI renamed to `InventoryBar`
- pickup persistence behavior now owned by `GameState`

### Milestone v0.6 — Use item on hotspot/NPC

Goal:

```txt
Selected inventory item can be used on an object or NPC.
```

Delivered:

- item selection and deselection
- item-use rules
- success/failure/completed outcomes
- optional item consumption
- state-dependent NPC/hotspot content

### Milestone v0.7 — Item combining

Goal:

```txt
Two inventory items can combine into a new item.
```

Delivered:

- order-independent recipe system
- Empty Cup -> Old Well = Cup of Water
- Cup of Water + Moon Herb = Glowing Tea
- inventory-combination operation extracted from `AdventureScene`
- atomic recipe transaction tests

### Milestone v0.8 — Quest flags

Goal:

```txt
Game can track progress through flags.
```

Delivered:

- progression flags
- flag-reactive NPC dialogue and hotspot text
- locked tower exit
- demo completion flag
- content validation

## Completed milestone: v0.8.1 — Refactor and regression hardening

Goal:

```txt
Protect current behavior and separate runtime state, rules, and presentation before adding the final demo content.
```

Scope:

- hotspot inspection regression fix
- behavior and integration coverage
- Python content validation
- persistent world state in `GameState`
- stateless item-use definitions
- recipe execution extracted from `AdventureScene`
- `AdventureInteractionService`
- unified target resolution for click and hover
- shared UI helpers for text wrapping and inventory layout
- documentation/scaffolding cleanup

Not in scope:

- JSON content loading
- save/load
- new v0.9 puzzle content
- event bus
- quest engine
- UI framework

Done when:

```txt
make check passes
current v0.8 behavior is protected
AdventureScene is mostly a Pygame adapter
misleading empty scaffolding is removed or documented
```

## Current milestone: v0.9 — First complete demo

Goal:

```txt
Playable beginning-to-end mini adventure with the intended key-based tower puzzle.
```

Chosen v0.9 puzzle flow:

```txt
Empty Cup -> Old Well -> Cup of Water
Cup of Water + Moon Herb -> Glowing Tea
Glowing Tea -> Retired Witch -> Rusty Key
Rusty Key -> Tower Gate -> tower opens
Enter Tower -> demo ending
```

Delivered features:

- add Cup of Water item
- add Rusty Key item
- update Old Well interaction to turn Empty Cup into Cup of Water
- update recipe to require Cup of Water + Moon Herb
- witch interaction gives Rusty Key instead of unlocking the tower directly
- tower gate requires Rusty Key
- keep `TOWER_UNLOCKED` as the semantic world fact after the key is used
- full demo-flow integration test updated
- keep the demo small and complete

Manual acceptance:

```txt
Start new game.
Collect required items.
Fill Empty Cup with water at the well.
Make Glowing Tea.
Give tea to witch.
Receive Rusty Key.
Use Rusty Key on tower gate.
Enter tower.
Reach ending.
```

## Milestone v0.9.1 — Post-demo refactor

Goal:

```txt
Clean up architecture after the complete demo proves the gameplay shape.
```

Possible scope:

- revisit content definitions after the key-based flow is real
- decide whether item definitions should move to data files first
- consider lightweight scene/content definition objects
- improve save/load readiness
- review whether flags and interaction IDs need naming cleanup
- review any `AdventureScene` responsibilities that remain too large
- improve manual-test docs for the complete demo

Not automatic:

- JSON should still only be added if it reduces real content pain
- no generic quest engine unless multiple quests need it
- no UI framework unless UI complexity increases

## Milestone v0.10 — Polish pass

Goal:

```txt
Make the prototype nicer to play.
```

Possible features:

- better placeholder art
- improved hover labels
- simple title/menu screen
- improved dialogue UI
- basic sound effects
- better scene layout
- README play instructions

## Future milestones

Only after the MVP/demo is complete:

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
