# Roadmap

Planning direction: 2026-11-06. GitHub milestones/issues are authoritative for live
status, detailed scope, dependencies, task checklists, and verification results.
This page does not track completion percentages or duplicate those checklists.

## Proven foundation

The supplied code supports the original three-scene cup/well/herb/tea/witch/key/gate
puzzle, content/session separation, inventory transactions, display scaling, and
semantic input. The supplied v0.12 archive adds save paths, envelopes, atomic I/O,
and validated session restoration. Its menus are unfinished in that archive; check
current GitHub state before deciding what remains. Main's reported 304-pass CI result
is evidence for that tested commit, not every subsequent branch.

## Planned sequence

| Milestone | Goal |
| --- | --- |
| v0.12 — Pause, save/load, and menus | Finish safe one-slot persistence and player-facing menu flow |
| v0.12.1 — Persistence and menu hardening | Audit accepted behavior; create only evidence-based follow-up work |
| v0.13 — Player navigation pilot | One single-screen floor, visible placeholder player, held arrows, click travel, obstacles |
| v0.14 — Approach and interact | Full-demo proximity, corresponding entrances, position/facing saves, known legacy fallback |
| v0.15 — Player and ambient animation pilot | Four-direction idle/walk, stable feet, depth/foreground layering, small ambient loops; player/ambient animation freezes during pause |
| v0.16 — Dialogue choices | One meaningful branching conversation before generalizing content |
| v0.17 — Objective hints and journal | Clear goals from existing facts before introducing quest machinery |
| v0.18 — Production presentation/content | Small separate art, inventory, audio, and authoring experiments |
| v0.19 — Packaging/settings | Chosen platform, reliable paths, approved settings, useful diagnostics |
| v0.20 — Larger chapter pilot | Authored content growth exposes real production bottlenecks |

Feature issues may be created now in Backlog. Start implementation only when their
prerequisites and blocking decisions are satisfied. Optional .1 refactor issues are
derived from audits; .1 releases and code rewrites are not mandatory.

## Stable direction

See [GDD](gdd.md) and [decisions](decisions.md) for approved behavior. Preserve the
existing puzzle while introducing movement. Keep single-screen scenes through the
navigation/interaction/animation pilots. Routes and cosmetic animation are transient;
legacy saves preserve progress using safe default spawns.

The v0.13 pilot is internal: full-demo proximity and movement-aware saves arrive in
v0.14. Dialogue choices follow movement/animation at v0.16. Evaluate dialogue JSON
only after a representative conversation proves the schema; scenes remain Python
until a production example demonstrates a better authoring format.

## Deferred experiments and scope

A camera/larger scene, perspective scaling, interaction/cinematic animations,
autosave/checkpoints, extra slots, authoring editor, and modding need separate scope
and evidence. A small downloadable playtest can precede full v0.19 packaging on the
confirmed Windows/Linux targets (DEC-17). Keep combat, RPG progression, 3D, procedural generation,
and generic engine frameworks outside the active authored-adventure plan.
