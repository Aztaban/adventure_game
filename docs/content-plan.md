# Content Plan

Status: draft

## Purpose

This document tracks story, world, NPCs, scenes, items, and puzzles.

It can change often. Keep game content separate from engine architecture.

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

## First demo idea

The player wants to enter a cursed tower.

To enter, the player must solve a small chain of adventure puzzles.

## First demo scenes

### Scene 1: Village Square

Purpose:

- starting scene
- introduce tone
- first NPC
- first item

Possible hotspots:

- retired witch
- empty cup
- notice board
- exit to forest
- exit to tower entrance

### Scene 2: Forest Path

Purpose:

- find puzzle item
- meet strange NPC
- create mystery

Possible hotspots:

- moon herb
- mushroom guard
- suspicious stump
- exit to village
- exit to tower entrance

### Scene 3: Tower Entrance

Purpose:

- locked obstacle
- ending condition

Possible hotspots:

- tower door
- dramatic magical lock
- weird rune stone
- exit to village/forest

## First demo NPCs

### Retired Witch

Role:

- gives funny dialogue
- wants glowing tea
- gives rusty key after receiving glowing tea

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
- maybe blocks forest path in later version

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

Received from:

```txt
retired_witch after giving glowing_tea
```

Use:

```txt
unlock tower door
```

## First demo puzzle chain

```txt
1. Player sees locked tower door.
2. Door requires key.
3. Witch has key but wants glowing tea.
4. Player finds empty cup.
5. Player finds moon herb.
6. Player combines empty cup + moon herb = glowing tea.
7. Player gives glowing tea to witch.
8. Witch gives rusty key.
9. Player uses rusty key on tower door.
10. Demo ends.
```

## Optional inspect text ideas

### Tower Door

```txt
The door is covered in runes that look ancient, expensive, and slightly judgmental.
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
