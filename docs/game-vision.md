# Game Vision

Status: direction agreed 2026-11-04; implementation staged by milestone.

## Goal

Build an original humorous fantasy adventure with the authored puzzle/dialogue
feel and 2D/2.5D visual character of classic adventures such as Polda. Painted-style
backgrounds, visible characters, grounded movement, clear interaction, and a lively
world support the comedy and mystery. No 3D engine is required.

## Experience pillars

- Memorable characters, authored jokes, readable clues, and coherent puzzle chains.
- A visible player walking across a two-dimensional floor area with depth.
- Arrow-key control and click-to-move as equal supported movement methods.
- Click a person/object/item/exit: approach a reachable point, then act when close.
- Inventory selection and combination remain immediate UI actions.
- One consistent logical display composition; clear targets without pixel hunting.
- Player idle/walk animation and small ambient scene motion after movement is sound.
- One useful playable example per feature; no speculative general-purpose engine.

## Confirmed scope

See [decisions](decisions.md) for the authoritative confirmed choices and open details.
Initial movement uses the existing single-screen scene model. Grounded actors use
foot anchors; depth and occlusion are visual composition concerns, not physics in 3D.
A scrolling camera, perspective scaling, and elaborate animation systems are deferred.

The original direct-click demo remains the current implementation until the movement
milestones replace that behavior. It is a completed proof of puzzle rules, not the
final intended control model.

## Development sequence

1. Finish v0.12 pause/save/load and establish branch-specific CI and desktop evidence.
2. Perform a focused v0.12.1 audit only where the feature exposes concrete pressure.
3. Prove arrow and mouse navigation in one scene with a visible placeholder player.
4. Apply approach/range interaction, exits, scene-entry positions, and save compatibility
   across the original demo.
5. Add one coherent player animation set and a small ambient animation pilot.
6. Build dialogue choices and objective guidance using representative authored content.
7. Grow production assets, audio, inventory presentation, packaging, and chapter content.

## Scope guard

Keep combat, levels/skills, procedural generation, multiplayer, a general editor,
modding support, ECS/event-bus frameworks, and 3D outside the active roadmap.
Obstacle-aware navigation is approved as part of the movement pilots; it is not
permission to create a general navigation engine. Refactors require observed evidence.
