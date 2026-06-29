# Coding Standards

Status: draft

## General principles

- Keep code simple.
- Prefer readable code over clever abstractions.
- Implement one milestone at a time.
- Do not overengineer systems before they are needed.
- Use type hints where reasonable.
- Keep functions/classes small enough to understand.
- Avoid giant files.

## Python style

- Use Python 3.11+ or 3.12 if available.
- Use clear snake_case names.
- Use PascalCase for classes.
- Use constants for fixed settings.
- Keep imports organized.
- Do not hide important logic in magic one-liners.

## File organization

- `main.py` should stay small.
- Game loop belongs in `game/app.py`.
- Scene logic belongs in `game/scenes/`.
- Inventory/dialogue/quest logic belongs in `game/systems/`.
- UI drawing belongs in `game/ui/`.

## Agent rules

When an AI agent modifies the code:

- change only files relevant to the task
- do not rewrite unrelated files
- do not add dependencies without asking
- explain what changed
- provide manual test steps
- mention any follow-up TODOs

## Comments

Use comments to explain why, not obvious what.

Good:

```python
# Claiming an item should remove it from the scene to avoid duplicate pickups.
```

Bad:

```python
# Increment i by 1.
```

## Error handling

- Handle missing assets gracefully where possible.
- Use placeholder rendering if asset is missing.
- Avoid crashing because optional art is not ready.

## Testing

Early game development can use manual tests.

Every milestone should have manual test steps in the response/PR.

Later, add unit tests for pure logic:

- inventory
- recipes
- quest flags
- dialogue progression

## Performance

Do not optimize early.

For MVP, correctness and clarity matter more than performance.

## Scope control

Do not implement these without explicit request:

- combat
- levels
- skills
- 3D
- pathfinding
- procedural generation
- advanced save system
