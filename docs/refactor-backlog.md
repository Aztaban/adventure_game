# Refactor Backlog

Project: Adventure Game  
Current baseline: v0.10 presentation milestone  
Next feature milestone: v0.11 save/load prototype

## Purpose

This file tracks only refactors that are still planned or being considered.

It is not a release history and does not retain completed task lists. Completed work belongs in `CHANGELOG.md`; stable architectural decisions belong in `docs/architecture.md` or the relevant design document.

Detailed implementation tasks should be written only after the related feature milestone has established a concrete need. Until then, this backlog records the refactor pressure, its trigger, and the intended outcome.

## Maintenance rules

- Keep only pending, deferred, or decision-gated refactors.
- Add a refactor when an implemented or approved feature creates clear architectural pressure.
- Describe the problem and desired boundary before prescribing classes, patterns, or file layouts.
- Plan detailed tasks after the related milestone behavior is stable enough to evaluate.
- Ask before changes that materially affect architecture or player behavior.
- Preserve the current gameplay flow and tests during every refactor.
- Remove completed items when the release is recorded in `CHANGELOG.md`.
- Avoid generic engine infrastructure without evidence from the game.

## Planned refactor points

### After v0.11 save/load prototype

- **Save repository boundary:** isolate filesystem access from snapshot creation and restoration after the first real save workflow is proven.
- **Save migrations:** add migration steps only after more than one supported save format exists.
- **Slot and autosave ownership:** refactor save-slot selection and autosave policy after player-facing behavior is decided.
- **Transient-state restoration:** decide whether open dialogue, messages, or other presentation state should remain intentionally excluded.

### After v0.12 dialogue choices

- **Dialogue model:** introduce stable dialogue-node IDs and branching structures only after the choice behavior is implemented and tested.
- **Dialogue content format:** reconsider dialogue JSON only when the choice schema is stable and demonstrably clearer than Python factories.
- **Conversation state:** separate persistent conversation outcomes from transient dialogue presentation if branching requires it.

### After v0.13 quest journal or objective hints

- **Objective model:** keep deriving objectives from current state while that remains simple; introduce explicit quest-step IDs only when derivation becomes unclear or duplicated.
- **Player-facing versus internal state:** separate objective text from internal flags when the journal needs independent wording, ordering, or completion history.

### After v0.14 larger-scene and camera pilot

- **Coordinate boundaries:** formalize world-space, camera-space, and screen-space conversion after the camera behavior is proven.
- **Camera ownership:** choose whether camera state belongs to the scene, session, or a focused component based on the pilot.
- **Spatial lookup:** add indexing only when measured target counts make linear hit testing inadequate.

### After v0.16 real asset and content production

- **Asset manifest and validation:** centralize asset IDs, paths, and validation when the number of real assets justifies it.
- **Fallback rendering policy:** decide whether placeholder rectangle rendering remains available for tests or debug builds.
- **Resource lifetime:** define preload and release behavior only if memory use or load pauses become observable problems.
- **Content construction:** reconsider scene data files only after larger content volume demonstrates that Python factories are a bottleneck.

## Unscheduled, evidence-gated candidates

These are not planned milestones. Reconsider them only when a concrete feature cannot remain clear without them:

- explicit scene enter/exit hooks when music, animation, timers, or loading transitions require them
- explicit quest definitions
- a command or action object for replayable interactions
- broader dependency injection or service composition
- a reusable widget hierarchy
- content tooling or editor support
- an event-dispatch layer for multiple independent listeners

## Not planned without strong evidence

- generic event bus
- entity-component system
- service locator
- scripting language for conditions
- inheritance-heavy UI framework
- universal command framework
- database-backed local prototype content
