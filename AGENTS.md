# Agent Instructions

This file is for AI coding agents working on this project.

## Project summary

This is a small 2D / 2.5D funny mysterious fantasy adventure game.

The first implementation should be a **Python + Pygame prototype**.

The goal is to build the game step by step, not to generate a large engine at once.

## Read before coding

Before making changes, read:

```txt
docs/decisions.md
docs/roadmap.md
docs/architecture.md
docs/coding-standards.md
docs/ai-workflow.md
```

For game design context, read:

```txt
docs/gdd.md
docs/content-plan.md
```

## Current scope

Implement only the supplied active GitHub issue. Use `docs/roadmap.md` for direction, not a task checklist.

Do not implement future features unless explicitly asked.

## Hard rules

- Do not rewrite the whole project unless asked.
- Do not add new dependencies without asking.
- Do not implement combat yet.
- Do not implement levels/skills yet.
- Do not implement 3D.
- Do not overengineer.
- Keep code beginner-readable.
- Prefer small files and clear names.
- Use placeholder rectangles/assets until real assets exist.
- After changes, explain:
  - what changed
  - which files changed
  - how to manually test it
  - what should be done next

## Architecture rules

- Keep `main.py` small.
- Put game logic inside `src/game/`.
- Keep data/content in `src/data/` or `assets/` where appropriate.
- Separate scene/hotspot/dialogue/inventory logic where reasonable.
- Do not mix all systems into one giant file.

## Testing rule

For every milestone, provide manual test steps.

Example:

```txt
Run: python src/main.py
Expected:
- window opens
- player can click hotspot
- dialogue opens
- ESC closes game
```

## Task ownership

GitHub issues own scope, acceptance checklists, dependencies, and status. Supply the
issue text when an agent cannot access GitHub. Permanent docs describe design and
architecture. Do not recreate milestone task files, duplicate refactor backlogs, or
a documentation history archive; Git preserves previous versions.
