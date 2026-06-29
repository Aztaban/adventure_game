# Adventure Game

Working title: **TBD**

A small funny mysterious fantasy adventure game prototype.

The first goal is not to build a full RPG. The first goal is to create a small playable adventure loop:

```txt
explore scene -> talk to NPC -> collect item -> combine/use item -> solve obstacle -> finish demo
```

## Current direction

- 2D / 2.5D point-and-click adventure
- Funny mysterious fantasy tone
- Scene-based world
- NPC dialogue
- Inventory
- Item usage and item combining
- Simple quest flags
- Combat, magic combat, levels, and skills are future features, not MVP

## Planned technology

Initial implementation:

```txt
Python + Pygame
```

The project should be written so that game content and core gameplay rules are separated from rendering where reasonable.

## Docs

Read these first:

```txt
docs/gdd.md
docs/mvp.md
docs/roadmap.md
docs/architecture.md
docs/ai-workflow.md
```

Agent instruction files:

```txt
AGENTS.md
CLAUDE.md
```

## Current development rule

Work step by step. Do not implement later milestones before the current milestone works.
