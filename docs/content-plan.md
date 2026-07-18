# Content Plan

Status: current for the v0.10 presentation milestone

## Purpose

This document tracks story, world, NPCs, scenes, items, and puzzles.

Keep game content decisions separate from engine architecture. Do not implement new story content in documentation-only refactors.

## Tone rules

The game should be:

- funny
- mysterious
- fantasy
- slightly absurd
- cozy but strange

Example tone:

```txt
Magic is real, but everyone is tired of filling magical paperwork.
```


## Current content format decision

R091-06 decision:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

Items and recipes are data-driven because their schemas are small and stable. Scene and dialogue content remain in Python because full scenes include coordinates, exits, entity types, conditions, flags, and interactions. Dialogue also stays in Python until the planned v0.13 dialogue-choice system proves its final shape.

Do not keep the same item or recipe definition in both Python and JSON. Stable Python constants are still acceptable when Python scene factories need to refer to item, flag, pickup, interaction, or scene IDs.

Re-evaluate dialogue JSON after v0.13. Re-evaluate full scene JSON only after at least one larger scene proves that a data schema would be clearer than Python factories.

## Current presentation assets

v0.10 adds replaceable presentation assets without changing story content:

```txt
Backgrounds: PNG
NPC/object/item/exit art: PNG with transparent backgrounds where useful
Sound effects: Ogg Vorbis
```

Stable IDs and exact replacement requirements are documented in `docs/asset-guide.md`.

The art remains presentation metadata on Python scene factories. Missing assets use the existing colored placeholder rendering, so asset replacement does not become a gameplay or content-loading dependency.

## Current v0.9 demo flow

The implemented v0.9 flow is key-based and includes filling the cup first:

```txt
empty cup -> old well -> cup of water
cup of water + moon herb -> glowing tea
glowing tea -> retired witch -> rusty key
rusty key -> tower gate -> tower opens
```

## First demo premise

The player wants to enter a cursed tower.

The tower gate is locked. The Retired Witch has an old key, but she wants Glowing Tea before she helps.

## First demo scenes

### Scene 1: Village Square

Purpose:

- starting scene
- introduce tone
- introduce Retired Witch
- provide Empty Cup
- provide village inspectables
- let the player fill the Empty Cup at the Old Well
- connect to Forest Path

Current/potential content:

- Retired Witch
- Empty Cup pickup
- Notice Board
- Old Well
- exit to Forest Path

### Scene 2: Forest Path

Purpose:

- provide Moon Herb
- introduce Mushroom Guard
- show locked tower access
- connect back to Village Square

Current/potential content:

- Moon Herb pickup
- Mushroom Guard
- Suspicious Stump
- exit to Village Square
- locked tower gate/exit

### Scene 3: Tower Interior / Tower Entrance

Purpose:

- final destination for first demo
- ending condition
- short payoff scene

Current/potential content:

- Ancient Pedestal
- completion text after entering

The implemented in-game name is `Ancient Tower`; the stable scene ID remains `tower_interior`.

## First demo NPCs

### Retired Witch

Role:

- gives funny dialogue
- wants Glowing Tea
- gives Rusty Key after receiving Glowing Tea in v0.9

Personality:

```txt
Tired, sarcastic, insists she is retired, but still knows too much.
```

Example dialogue idea:

```txt
"I stopped doing magic years ago. Now I only do suspiciously magical gardening."
```

### Mushroom Guard

Role:

- worldbuilding
- optional joke/dialogue
- reacts after progress changes

Personality:

```txt
Very official, very small, takes his job too seriously.
```

Example dialogue idea:

```txt
"No unauthorized ankles beyond this point."
```

## First demo items

### empty_cup

Found in:

```txt
village_square
```

Use:

```txt
fill at old_well
```

### water_cup

Created by:

```txt
empty_cup -> old_well
```

Use:

```txt
combine with moon_herb
```

### moon_herb

Found in:

```txt
forest_path
```

Use:

```txt
combine with water_cup
```

### glowing_tea

Created by:

```txt
water_cup + moon_herb
```

Use:

```txt
give to retired_witch
```

### rusty_key

Received from:

```txt
retired_witch after giving glowing_tea
```

Use:

```txt
unlock tower gate
```

## First demo puzzle chain for v0.9

```txt
1. Player sees the locked tower gate.
2. Gate requires Rusty Key.
3. Retired Witch has the key but wants Glowing Tea.
4. Player finds Empty Cup.
5. Player fills Empty Cup at the Old Well and gets Cup of Water.
6. Player finds Moon Herb.
7. Player combines Cup of Water + Moon Herb = Glowing Tea.
8. Player gives Glowing Tea to Retired Witch.
9. Witch gives Rusty Key.
10. Player uses Rusty Key on tower gate.
11. Gate opens / tower becomes reachable.
12. Player enters tower.
13. Demo ends.
```

## Optional inspect text ideas

### Tower Gate

```txt
The gate is covered in runes that look ancient, expensive, and slightly judgmental.
```

### Empty Cup

```txt
A cup. Empty, but emotionally available.
```

### Moon Herb

```txt
It glows softly, like a plant with unresolved secrets.
```

### Cup of Water

```txt
A cup of cold well water. The well claims it was artisanal.
```

### Rusty Key

```txt
A key with enough rust to count as extra security.
```

## Future content ideas

Do not implement yet.

- cursed library
- talking bridge
- goblin accountant
- spell that translates mushroom legal language
- magical bureaucracy office
- optional side quest with a lost hat
- simple magic puzzles
- larger mystery about why the tower is cursed

## Long-term authored adventure direction

The intended full game is a humorous, authored point-and-click adventure inspired by the puzzle/dialogue feel of games such as *Polda*. It should use original characters, worldbuilding, writing, art, and interface decisions.

Content growth should emphasize:

- connected scenes with memorable inspectable details
- character-driven dialogue and recurring jokes
- inventory puzzles with clear state changes
- optional observations that enrich the world without hiding required progress
- objective support before the number of active goals becomes confusing

## Content-format decision gates

Do not move content into JSON only because the project is larger. Move a content type when its schema is stable, validation is useful, and authoring becomes clearer.

```txt
v0.13 dialogue choices
    -> prove branching and stable IDs
    -> reconsider dialogue JSON

v0.15 larger-scene/camera pilot
    -> prove coordinate and interaction needs

v0.17 production content pilot
    -> compare one representative scene in Python and data form
    -> decide whether scene JSON is useful

v0.20 larger chapter pilot
    -> measure authoring duplication
    -> decide whether focused tooling is justified
```

Items and recipes should continue using stable JSON IDs. Add fields such as inventory icon IDs, examine text, or categories only when the corresponding player-facing feature is implemented.

## Interaction design gates

The exact Polda-style interaction language remains intentionally undecided until the relevant pilots:

- v0.15 decides contextual click, inspect behavior, selected-item cursor feedback, and larger-scene/camera needs
- v0.16 decides instant interaction versus visible move-then-interact behavior and whether pathfinding is required

Do not write large amounts of content that depend on one option before the option is proven.
