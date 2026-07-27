# Refactor Backlog

Project: Adventure Game
Current baseline: v0.11 display and controls implementation; manual acceptance pending
Next planned milestone: v0.11.1 display/input hardening
Next feature milestone after hardening: v0.12 pause, save/load, and menu foundation

## Purpose

This file contains only pending or decision-gated refactor work.

It is not release history. Completed refactors belong in `CHANGELOG.md`, and stable implemented architecture belongs in `docs/architecture.md`. Detailed task sequences live in milestone task documents only when the related feature is close enough to implement.

## Maintenance rules

- Keep only refactors that have not been completed.
- Tie each planned refactor to the feature milestone that creates evidence for it.
- Describe the pressure and desired outcome before prescribing a pattern or class name.
- Use `.1` milestones for focused cleanup and regression hardening after a feature milestone.
- Skip a planned extraction when the preceding feature does not create enough duplication or ownership pressure.
- Preserve gameplay, save compatibility, and tests during refactors.
- Ask before changes that materially alter architecture or player behavior.
- Remove completed entries after they are recorded in `CHANGELOG.md`.
- Avoid generic engine systems without a demonstrated game need.

## Highest-priority refactor focus

### v0.11.1 — Display/input refactor and hardening

Trigger:

```txt
v0.11 has implemented fullscreen/window scaling, logical pointer conversion, semantic actions, and a Controls screen.
```

Observed pressure after implementation:

- `game/display.py` already contains the authoritative geometry, presentation, pointer-conversion, and display-creation functions.
- `GameApp` still owns the correct high-level state: logical surface, physical display surface, current fullscreen flag, last session-only preset, and top-level navigation.
- `GameApp` now coordinates four modes plus global `N`/`F11` actions; the branching remains readable, but v0.12 pause/save/load screens may create the first real navigation pressure.
- Actual bindings and player-facing physical labels already share one catalog; v0.11.1 should verify drift protection rather than redesign the input system.
- `ControlsScreen` is reusable and emits a semantic Back result without depending on `AppMode`.
- No duplicated scale/offset formula or duplicate raw-key menu path was observed after D110-07.
- Display errors are currently a transient application-level message. Keep this unless v0.12 introduces a reusable error/dialog surface.

Primary v0.11.1 focus:

- audit and harden the completed boundaries rather than automatically extracting new classes
- confirm `GameApp` remains understandable before pause/save/load adds more screens
- keep display math and physical-to-logical conversion in one tested module
- keep semantic bindings and displayed labels synchronized
- verify all display changes preserve application and gameplay state
- document skipped refactors when the existing boundary is already coherent

Likely outcomes:

- keep the current `display.py` function boundary unless the audit finds stateful duplication
- keep `AppMode` for v0.11.1 when four modes remain clearer than a screen protocol
- add only missing regression tests or small ownership clarifications
- carry a screen-navigation decision into v0.12.1 if pause/save/load creates concrete duplication

Do not add during this refactor:

- editable bindings
- a widget hierarchy
- pause/save/load features
- camera/world coordinates
- persistent display settings
- a general screen stack without demonstrated duplication

## Planned refactor milestones

### v0.12.1 — Persistence/menu refactor

After the real save/load flow is working:

- isolate filesystem access from snapshot creation and restoration
- centralize user-data/save path resolution and atomic writes
- evaluate a small screen or screen-stack boundary if menu-mode branching has become cumbersome
- add save migrations only when a second supported save format exists
- keep transient presentation state intentionally separate from persistent game state

### v0.13.1 — Dialogue model/content refactor

After dialogue choices prove their shape:

- introduce stable node/choice IDs where save/load or branching requires them
- separate persistent conversation outcomes from transient dialogue presentation
- pilot dialogue JSON only if it is clearer than Python factories
- avoid arbitrary expression evaluation or a scripting language

### v0.14.1 — Objective-state refactor

After objective hints/journal behavior is proven:

- separate player-facing objective wording from internal flags if duplication appears
- introduce explicit quest-step IDs only when derived objectives are insufficient
- avoid a general quest engine while a small objective model remains clear

### v0.15.1 — Scene coordinate and interaction refactor

After the interaction/camera pilot:

- formalize logical-screen, world, and camera coordinate conversion
- choose camera ownership from observed usage
- centralize target resolution under the selected point-and-click interaction model
- split `AdventureScene` only where distinct responsibilities are demonstrated
- add spatial lookup only if measured scene complexity requires it

### v0.16.1 — Movement/runtime entity refactor

After visible movement is proven useful:

- isolate movement and move-then-interact sequencing
- separate static definitions, runtime state, and Pygame views only where animation or movement requires it
- avoid an entity-component system without strong evidence

### v0.17.1 — Resource/content refactor

After production assets, larger inventory, and a content pilot:

- replace working-directory asset assumptions with packaged application paths
- split `UIResources` only if image, sound, music, path, or lifetime responsibilities have become unclear
- introduce an asset manifest and validation only if asset volume justifies it
- add bounded caches, preload groups, or release behavior only after measuring load time or memory pressure
- adopt scene JSON only if the representative data-driven scene is clearer to author and validate
- separate content definitions, runtime state, and views only where production entities require it

### v0.18.1 — Audio/lifecycle refactor

After music and ambience are implemented:

- separate short SFX, music streaming, and ambience responsibilities
- add scene enter/exit hooks only where audio lifecycle needs them
- centralize master/music/SFX volumes and channel policy

### v0.19.1 — Release architecture hardening

After packaging and settings are functional:

- centralize application resource, save, config, log, and credit paths
- remove development-current-directory assumptions
- validate packaged startup and failure diagnostics

### v0.20.1 — Content-authoring refactor

After the first larger chapter exposes real production friction:

- remove repeated scene/dialogue/content construction patterns
- add focused authoring helpers, loaders, or validation for proven bottlenecks
- consider lightweight tooling only when manual authoring has become measurably inefficient

## Unscheduled, evidence-gated candidates

These are not approved milestones:

- reusable UI widget hierarchy
- broad dependency injection or service composition
- generic event dispatch for multiple independent listeners
- universal command/action objects
- content editor or modding support
- localization framework beyond stable text ownership/readiness

## Not planned without strong evidence

- generic event bus
- entity-component system
- service locator
- embedded scripting language
- inheritance-heavy UI framework
- universal command framework
- database-backed local content
- general-purpose game engine extraction
