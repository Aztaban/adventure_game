# Content Plan

Status: current direction after v0.8.1

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

## Current v0.8.1 implementation note

The current playable v0.8.1 flow still unlocks the tower directly when the Retired Witch receives Glowing Tea.

That is acceptable as temporary behavior while architecture is being refactored.

## Chosen v0.9 demo flow

The intended v0.9 flow is key-based:

```txt
witch gets tea -> gives rusty key -> key unlocks tower
```

Do not keep both designs in story docs. The key-based flow is the v0.9 target.

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

The exact name can be cleaned up during v0.9. Use one consistent in-game name once the final flow is implemented.

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
combine with moon_herb
```

### moon_herb

Found in:

```txt
forest_path
```

Use:

```txt
combine with empty_cup
```

### glowing_tea

Created by:

```txt
empty_cup + moon_herb
```

Use:

```txt
give to retired_witch
```

### rusty_key

Planned for v0.9.

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
5. Player finds Moon Herb.
6. Player combines Empty Cup + Moon Herb = Glowing Tea.
7. Player gives Glowing Tea to Retired Witch.
8. Witch gives Rusty Key.
9. Player uses Rusty Key on tower gate.
10. Gate opens / tower becomes reachable.
11. Player enters tower.
12. Demo ends.
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
