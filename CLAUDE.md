# Claude Project Instructions

This file mirrors `AGENTS.md` for Claude Code.

## Project summary

Small 2D / 2.5D funny mysterious fantasy adventure game.

Initial implementation target:

```txt
Python + Pygame
```

The project should grow step by step through small milestones.

## Read first

```txt
docs/mvp.md
docs/roadmap.md
docs/architecture.md
docs/coding-standards.md
docs/ai-workflow.md
```

For design/story context:

```txt
docs/gdd.md
docs/content-plan.md
```

## Behavior rules

- Work only on the requested milestone.
- Keep changes small and reviewable.
- Do not add dependencies without asking.
- Do not implement combat, levels, skills, or 3D unless explicitly requested.
- Use placeholder art/assets.
- Keep code simple and readable.
- Explain manual test steps after every change.
- Prefer clarity over clever abstractions.

## Important design direction

This is currently an adventure prototype, not a full RPG.

Core loop:

```txt
explore -> talk -> collect item -> combine/use item -> solve obstacle -> progress
```
