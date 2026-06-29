# AI Workflow

Status: draft

## Goal

Use AI agents step by step without wasting tokens or creating uncontrolled code.

The project should be developed through small milestones.

## Main workflow

1. Pick one milestone from `docs/roadmap.md`.
2. Ask the agent to implement only that milestone.
3. Agent reads:
   - `AGENTS.md`
   - `docs/mvp.md`
   - `docs/roadmap.md`
   - `docs/architecture.md`
   - `docs/coding-standards.md`
4. Agent summarizes the plan before coding.
5. Agent changes only necessary files.
6. Agent explains what changed.
7. Agent gives manual test steps.
8. User tests locally.
9. Fix bugs before moving to next milestone.

## Good prompt example

```txt
Implement milestone v0.3 from docs/roadmap.md.
Follow AGENTS.md and docs/architecture.md.
Do not implement later milestones.
After the change, give me manual test steps.
```

## Bad prompt example

```txt
Build the whole game with inventory, quests, combat, magic and all scenes.
```

## Token-saving rule

Do not paste the whole GDD into every prompt.

Instead say:

```txt
Follow AGENTS.md and docs/gdd.md.
Implement only milestone v0.X.
```

## Agent response expectations

After coding, the agent should answer with:

```txt
Changed files:
- ...

What changed:
- ...

How to test:
- ...

Notes / next step:
- ...
```

## When to stop an agent

Stop or correct the agent if it:

- starts implementing future milestones
- rewrites unrelated files
- adds libraries without asking
- creates too many abstractions
- ignores existing architecture
- mixes all logic into one file
- starts combat/3D/levels too early

## Development rhythm

Recommended rhythm:

```txt
small prompt
small code change
manual test
commit
next milestone
```

## Commit style

Suggested commit messages:

```txt
feat: add basic game window
feat: add scene manager
feat: add hotspot interactions
feat: add basic dialogue box
feat: add inventory system
fix: prevent duplicate item pickup
docs: update MVP scope
```
