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
docs/decisions.md
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

- Work only on the supplied active GitHub issue; roadmap entries are not permission to implement future features.
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

## Task ownership

GitHub issues own scope, acceptance checklists, dependencies, and status. Supply the
issue text when an agent cannot access GitHub. Permanent docs describe design and
architecture. Do not recreate milestone task files, duplicate refactor backlogs, or
a documentation history archive; Git preserves previous versions.

## Version and release ownership

Follow [Development and release workflow](docs/ai-workflow.md) for PR titles,
automation, and packaging. Use `fix:` for patch, `feat:` for minor, and an explicit
`!` for major. Maintenance types bump patch. Automation prepares the version and
CHANGELOG on the PR branch; do not hand-bump or add manual changelog placeholders.
Keep `Python checks` passing on the final bot commit and update from main when stale.
Publishing is a separate manual action for current main, producing Windows/Linux
builds and the matching tag without another version bump. Never move published tags.
