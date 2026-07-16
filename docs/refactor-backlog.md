# Refactor Backlog

Project: Adventure Game  
Current baseline: v0.9.1 released  
Next feature milestone: v0.10

## Purpose

This backlog contains only unfinished or future refactor work.

Completed v0.8.1 tasks and completed v0.9.1 tasks have been removed. Historical implementation details remain available in the changelog and Git history.

## Working rules

- Add refactors only when a completed feature creates concrete pressure.
- Prefer one focused branch and one focused commit per backlog item.
- Protect behavior with tests before changing ownership or architecture.
- Run `make check` after every task.
- Manually test behavior-affecting changes.
- Keep gameplay logic independent from Pygame resources.
- Keep content definitions separate from session state.
- Do not introduce generic frameworks without a demonstrated need.
- Remove compatibility paths once all callers use the supported path.

## Status legend

```text
[ ] not started
[~] in progress
[x] completed
[-] skipped after a documented decision
[?] decision required
```

---

# Current architecture baseline

The following decisions are already implemented and are no longer backlog items:

```text
GameContent
- reusable item and recipe definitions
- reusable scene builders and ID registries
- starting scene ID
- validation boundary

GameSession
- fresh GameState
- current SceneManager and scene instances

GameState
- inventory and selected item
- progression flags
- collected pickup IDs
- completed interaction IDs
- ending state

AdventureInteractionService
- gameplay transactions and interaction outcomes

AdventureScene
- Pygame input adapter
- target resolution
- transient presentation state
- rendering coordination

UIResources
- shared/cached fonts
- stable future image/audio lookup boundary
```

Content format decision:

```text
Items: JSON
Recipes: JSON
Scenes: Python factories
Dialogue: Python factories until dialogue choices stabilize
```

State snapshots already use plain values and stable IDs. Save-file I/O and menus are intentionally deferred to v0.11.

---

# Future feature and refactor sequence

The v0.9.1 refactor, reset lifecycle, snapshot boundary, JSON pilot, UI-resource cleanup, and release verification are complete. They are architecture baseline, not active backlog work.

Refactor checkpoints should normally happen **after** the associated feature milestone has produced real requirements.

## Optional pre-v0.10 cleanup — Scene transition lifecycle

Do this only if manual testing reveals stale transient state when moving between scenes. New-game reset is already implemented and is not part of this task.

### Possible symptoms

- An old interaction message appears after returning to a scene.
- Dialogue remains open across a transition.
- Hover state survives after the target is no longer present.
- Future scene-local timers continue after leaving a scene.

### Candidate work

- [ ] Clear hover state on transition.
- [ ] Close active dialogue on transition.
- [ ] Clear ordinary interaction messages on scene entry.
- [ ] Keep persistent inventory, flags, pickups, interactions, and ending state untouched.
- [ ] Add minimal `on_enter()` / `on_exit()` hooks only if they clarify the policy.

### Tests

- [ ] Transition clears only transient presentation state.
- [ ] Persistent world state survives transition and reconstruction.
- [ ] `N` still creates a completely fresh session.

### Skip when

Skip this cleanup if current transition behavior is already intentional and no stale-state defect can be reproduced.

---

# v0.10 — Polish and presentation

## Feature goal

Improve the existing complete demo without changing its puzzle structure.

Possible feature work:

- Improved colors, spacing, typography, and visual hierarchy.
- Clearer selected-item and locked-exit feedback.
- Better ending presentation.
- Optional first real images or sound effects.
- Accessibility review for text size and contrast.

## Follow-up refactor: R101 — Presentation resource cleanup

Run this after v0.10 only if real presentation work creates pressure.

### Candidate tasks

- [ ] Confirm `UIResources` remains the single font/resource owner.
- [ ] Add an image cache only after images are actually loaded repeatedly.
- [ ] Add a small audio resource/channel owner only after sound is implemented.
- [ ] Move stable image/audio asset IDs into dedicated registries or a manifest.
- [ ] Separate theme values from content-specific presentation values.
- [ ] Remove temporary placeholder-rendering paths replaced by real assets.
- [ ] Keep layout fixed unless v0.10 explicitly adds resizing.

### Tests

- [ ] Repeated asset lookup returns cached resources where appropriate.
- [ ] Missing asset IDs fail clearly in development.
- [ ] Pure interaction tests remain free of Pygame resources.
- [ ] UI smoke tests cover the real resource path.

### Skip when

Skip R101 if v0.10 changes only colors/text and does not add meaningful asset-loading complexity.

---

# v0.11 — Save/load

## Feature goal

Persist and restore a game using the existing state-snapshot boundary.

### Decisions required before implementation

- [?] One manual save slot or multiple slots?
- [?] Save only from a menu, or allow a keyboard shortcut?
- [?] Should completed games remain loadable?
- [?] Where should save files live on each supported platform?

Recommended first scope:

```text
one save slot
manual save
manual load
clear error messages
no autosave yet
```

## Follow-up refactor: R111 — Save repository and migrations

Run after the first real save/load feature works.

### Candidate tasks

- [ ] Introduce a small save repository responsible for filesystem I/O.
- [ ] Keep snapshots independent from file paths and JSON encoding.
- [ ] Add atomic write behavior to reduce corrupted saves.
- [ ] Handle missing, unreadable, and invalid save files clearly.
- [ ] Add explicit migration steps when `save_version` changes.
- [ ] Keep old-save compatibility tests for supported versions.
- [ ] Avoid coupling menus directly to filesystem operations.

### Tests

- [ ] Save then load reproduces mid-quest state.
- [ ] Corrupted JSON fails without destroying the current session.
- [ ] Unsupported future versions fail clearly.
- [ ] Supported older versions migrate successfully.
- [ ] Save/load after new-game reset behaves correctly.

---

# v0.12 — Dialogue choices

## Feature goal

Add player choices without turning dialogue into arbitrary scripting.

### Decisions required before implementation

- [?] Are unavailable choices hidden or shown disabled?
- [?] Can a choice require an item, a flag, or both?
- [?] Can choices set flags and give/take items?
- [?] Can dialogue return to an earlier node?
- [?] Is dialogue modal while a choice is open?

Recommended first scope:

```text
stable dialogue node IDs
2-3 choices per node
small declarative conditions
explicit next-node IDs
explicit effects
no arbitrary expressions
```

## Follow-up refactor: R121 — Dialogue model and content-format review

Run after real dialogue choices exist.

### Candidate tasks

- [ ] Separate dialogue definitions from dialogue runtime position.
- [ ] Introduce typed dialogue nodes and choices.
- [ ] Keep current node/choice state in the session, not definitions.
- [ ] Validate all next-node references.
- [ ] Keep condition operators intentionally small.
- [ ] Re-evaluate moving dialogue definitions to JSON.
- [ ] Pilot one conversation in JSON before migrating all dialogue.
- [ ] Ensure Python and JSON are never both authoritative for the same conversation.

### JSON decision gate

Move dialogue to JSON only if:

- Authors benefit from editing dialogue outside Python.
- The node/choice schema has stabilized.
- Loader errors remain clearer than nested Python construction.
- Conditions can stay declarative without a scripting language.

---

# v0.13 — Quest journal and objective hints

## Feature goal

Show player-facing objectives without exposing internal implementation flags.

### Decisions required before implementation

- [?] Show one active objective or a full quest list?
- [?] Can quests be optional?
- [?] Should completed objectives remain visible?
- [?] Are hints automatic or requested by the player?

## Follow-up refactor: R131 — Separate quest definitions from flags

Run after the first journal is playable.

### Candidate tasks

- [ ] Introduce stable quest and objective IDs.
- [ ] Keep player-facing text separate from internal progression flags.
- [ ] Define objective completion from existing semantic world facts.
- [ ] Avoid duplicating the same completion fact in quest state and flags.
- [ ] Add a small quest-evaluation service only if multiple objectives need it.
- [ ] Keep journal rendering separate from quest evaluation.
- [ ] Reconsider a quest JSON schema only after several quests exist.

### Tests

- [ ] Objectives update from real gameplay facts.
- [ ] Reset and load restore journal state correctly.
- [ ] Hidden/internal flags are not displayed directly.
- [ ] Completing objectives in different valid orders works.

---

# v0.14 — Larger scene and camera pilot

## Feature goal

Prove one scene larger than the fixed window.

### Decisions required before implementation

- [?] Horizontal-only scrolling or full two-dimensional camera?
- [?] Camera follows the player or a selected focus point?
- [?] Are interactions allowed outside the visible viewport?
- [?] Do UI elements stay in screen coordinates?

## Follow-up refactor: R141 — World and screen coordinate separation

Run after one larger scene proves the camera requirements.

### Candidate tasks

- [ ] Define explicit world coordinates for scene entities.
- [ ] Keep UI rectangles in screen coordinates.
- [ ] Centralize world-to-screen and screen-to-world conversion.
- [ ] Make hit testing use the correct coordinate space.
- [ ] Keep target priority unchanged.
- [ ] Add camera bounds based on scene dimensions.
- [ ] Add spatial indexing only if measured entity counts justify it.
- [ ] Remove assumptions that every scene equals window size.

### Tests

- [ ] A target resolves correctly after camera movement.
- [ ] Inventory UI still wins over overlapping world targets.
- [ ] Camera bounds prevent showing invalid space.
- [ ] Scene transitions and snapshots remain stable.

---

# v0.15 — Click-to-move character pilot

## Feature goal

Add a visible player character that moves before interacting.

### Decisions required before implementation

- [?] Instant movement or animated movement?
- [?] Direct movement or pathfinding around obstacles?
- [?] Does clicking a target mean move-then-interact?
- [?] Can the player cancel movement with another click?
- [?] How close must the player be to interact?

Recommended first scope:

```text
simple direct movement
move-then-interact
small interaction radius
no general pathfinding until obstacles require it
```

## Follow-up refactor: R151 — Navigation and interaction separation

Run after the movement pilot works.

### Candidate tasks

- [ ] Separate player movement state from scene presentation state.
- [ ] Represent pending interaction intent explicitly.
- [ ] Keep `AdventureInteractionService` responsible for gameplay outcomes, not movement.
- [ ] Add a small navigation component only for actual movement needs.
- [ ] Keep input translation in the Pygame adapter.
- [ ] Add pathfinding only after direct movement fails on real scene geometry.
- [ ] Include player position and pending movement in snapshots only if saves require it.

### Tests

- [ ] Clicking a nearby target interacts correctly.
- [ ] Clicking a distant target moves then interacts once.
- [ ] A second click replaces or cancels pending intent according to policy.
- [ ] Scene transition cancels stale movement.
- [ ] Reset/load does not leak pending movement state.

---

# v0.16 — Content and asset production pass

## Feature goal

Scale from the small demo toward a larger adventure using proven systems.

Possible work:

- More scenes, items, recipes, interactions, and dialogue.
- Real visual/audio assets.
- Content-authoring workflow improvements.
- Packaging and distribution checks.
- Performance baseline with representative content volume.

## Follow-up refactor: R161 — Content pipeline and production hardening

Run after representative v0.16 content exists.

### Candidate tasks

- [ ] Measure where content authoring is slow or error-prone.
- [ ] Add asset manifests only if directory lookup becomes fragile.
- [ ] Batch-validate all content and asset references.
- [ ] Add development-only content diagnostics.
- [ ] Re-evaluate full-scene JSON using one real scene pilot.
- [ ] Add dialogue JSON only if the v0.12 schema proved stable.
- [ ] Keep typed definitions between raw data and gameplay code.
- [ ] Add packaging tests for JSON, images, audio, and fonts.
- [ ] Establish load-time and memory baselines.
- [ ] Add an editor only if manual file editing is a demonstrated bottleneck.

### Full-scene JSON decision gate

A scene-data pilot is justified only if:

- There are enough scenes to reduce meaningful Python churn.
- Entity and condition schemas have stabilized.
- Data remains simpler than Python factories.
- Error messages identify file, object, field, and invalid reference.
- Conditions do not require arbitrary expression evaluation.
- Content authors will actually edit the files.

---

# Part III — Cross-milestone maintenance

Apply these continuously rather than scheduling large cleanup releases.

## After every feature milestone

- [ ] Run the full automated suite.
- [ ] Run the relevant manual gameplay path.
- [ ] Update `CHANGELOG.md`.
- [ ] Update architecture/testing docs when ownership changes.
- [ ] Remove temporary adapters introduced during the feature.
- [ ] Search for duplicate authoritative content definitions.
- [ ] Confirm snapshots include every new persistent fact.
- [ ] Confirm new transient UI state resets on new game and transitions.
- [ ] Confirm stable IDs are validated and not derived from positions or list order.

## Performance rule

Do not optimize by architecture guesswork.

Measure before adding:

- Spatial indexes
- Object pools
- Background loading
- Complex caches
- Database storage
- General pathfinding

## Architecture rule

Do not introduce without strong evidence:

- Generic event bus
- Entity-component system
- Service locator or dependency-injection framework
- Scripting language for content conditions
- Inheritance-heavy widget framework
- Universal command hierarchy
- Database for local built-in content

---

# Decision log

## D-001 — Persistent-state owner

Status: implemented

```text
GameState owns inventory, flags, collected pickups,
completed interactions, and ending state.
```

## D-002 — Content/session separation

Status: implemented

```text
GameContent owns reusable content and validation registries.
GameSession owns one running game's state and scene manager.
```

## D-003 — AdventureScene responsibility

Status: implemented

```text
AdventureScene translates Pygame input, resolves targets,
applies presentation outcomes, and renders.
AdventureInteractionService performs gameplay transactions.
```

## D-004 — Current JSON scope

Status: implemented

```text
Items and recipes are loaded from JSON.
Python item/recipe definitions are not a second authority.
```

## D-005 — Scene/dialogue format

Status: decided for current milestones

```text
Scenes remain Python factories.
Dialogue remains Python until v0.12 choices stabilize.
Re-evaluate dialogue JSON after v0.12.
Re-evaluate full-scene JSON only after a representative later pilot.
```

## D-006 — Refactor timing

Status: agreed direction

```text
Build the feature first.
Refactor after real behavior reveals the required boundary.
Skip refactors whose motivating complexity did not appear.
```