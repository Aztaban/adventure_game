# Refactor Backlog

Project: Adventure Game
Current baseline: v0.11.1 display/input hardening implemented; real-Pygame transition verification pending
Next planned feature milestone: v0.12 pause, save/load, and menu foundation
Next planned refactor milestone: v0.12.1 persistence/menu hardening

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

## Planned refactor milestones

### v0.12.1 — Persistence/menu refactor

After the real one-slot save/load and pause flow is working, audit before extracting anything:

- trace one Save request from a screen result through snapshot creation, envelope creation, path resolution, and atomic replacement
- trace one Load request through status/validation, session restoration, transient-state reset, and final application mode
- verify filesystem access remains outside `GameState`, gameplay rules, and concrete screen objects
- consolidate save validity/status parsing only if title Continue and pause Load duplicate it
- consolidate error translation only if filesystem, JSON, envelope, and snapshot failures leak into multiple callers
- evaluate a small screen contract or stack only if title, Controls, pause, ending, and confirmation branching has become cumbersome
- keep `AppMode` and concrete screen objects when they remain explicit and smaller than the abstraction
- do not introduce a repository pattern for one manual slot
- do not add migrations until a second save-file version must be supported
- preserve the v0.12 save format and player behavior during refactoring

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
- compare regular fullscreen and borderless desktop behavior on supported target platforms only when real-Pygame evidence shows the current transition remains unacceptable

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
