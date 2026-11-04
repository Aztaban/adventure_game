# Documentation index

Planning revision: 2026-11-04. Source baseline: supplied v0.12 branch archive,
commit `cca8adfd3abe5dc24b2ba003ab556767c5fcd1cc`.

This revision changes documentation only. Movement, proximity, animations, and
save upgrades described as planned are not implemented by this documentation pack.

## Start here

- [Game vision](game-vision.md): experience and agreed direction.
- [Game design document](gdd.md): gameplay, controls, movement, and presentation.
- [Decisions and open questions](decisions.md): confirmed choices versus proposed defaults.
- [Roadmap](roadmap.md): implementation status and milestone order.
- [Architecture](architecture.md): current code first, planned movement boundaries separately.
- [Historical MVP](mvp.md): the original playable loop and its intentional simplifications.
- [Content plan](content-plan.md): story, puzzle dependencies, and scene-authoring work.
- [Asset guide](asset-guide.md): current asset contract and planned animation requirements.
- [Testing plan](testing-plan.md): verification responsibilities and acceptance scenarios.
- [Refactor backlog](refactor-backlog.md): evidence-gated audits; not mandatory rewrites.
- [Coding standards](coding-standards.md) and [AI workflow](ai-workflow.md).

## Active and near-term milestones

1. [v0.12 pause/save/load](milestones/v0.12-pause-save-load.md): in progress through D120-06.
2. [v0.12.1 persistence/menu audit](milestones/v0.12.1-persistence-menu-refactor.md).
3. [v0.13 player navigation pilot](milestones/v0.13-player-navigation.md).
4. [v0.14 approach and interact](milestones/v0.14-approach-and-interact.md).
5. [v0.15 animation pilot](milestones/v0.15-animation-pilot.md).

## Historical evidence

- [v0.11 display and controls](milestones/v0.11-display-and-controls.md).
- [v0.11.1 display/input audit](milestones/v0.11.1-display-input-refactor.md).

These task logs retain their original test-environment evidence. A later CI run
must not be described as having occurred during an earlier audit.

## Status ownership during migration to GitHub

This is a reviewable plan before creating further issues. Existing GitHub issue
#4 tracks v0.11.1 documentation reconciliation. Do not claim it or desktop
acceptance is complete because this pack exists.

Until tasks are migrated, milestone files contain the detailed execution plan.
After migration, GitHub issues own task status; retain stable decisions and
acceptance contracts here and replace duplicate progress checklists with real
issue links. Never invent issue numbers or links to CI runs.

The user reported 304 passing real-Pygame tests on main. This verifies that main
run, not this v0.12 archive. Incorporate current main into the feature branch,
resolve documentation/changelog differences, and establish fresh branch CI evidence.
