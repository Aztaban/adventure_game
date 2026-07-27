# Roadmap

Status: v0.11 implementation complete; automated dependency and manual display acceptance pending

## Development principle

Each milestone should be small, testable, and playable.

Do not implement future systems before the current gameplay need exists.

Prefer this order:

```txt
prove gameplay -> protect with tests -> refactor boundary -> document decision
```

## Completed milestones

### Milestone v0.1 — Window and game loop

Goal:

```txt
Open a game window and run a stable loop.
```

Delivered:

- Pygame window
- stable loop
- quit and ESC handling
- simple drawing baseline

### Milestone v0.2 — Scene system

Goal:

```txt
Display one scene and allow switching to another scene.
```

Delivered:

- `SceneManager`
- base scene interface
- placeholder adventure scenes
- exit-driven scene transitions

### Milestone v0.3 — Hotspots

Goal:

```txt
Clickable objects can show interaction text.
```

Delivered:

- inspectable hotspots
- hover detection
- click messages
- hotspot tests

### Milestone v0.4 — Dialogue box and NPCs

Goal:

```txt
NPCs can display dialogue.
```

Delivered:

- NPC entities
- dialogue state system
- dialogue box UI
- click, Space, and Enter advancement
- scene input consumption while dialogue is active

### Milestone v0.5 — Inventory

Goal:

```txt
Player can pick up items and see inventory.
```

Delivered:

- immutable item definitions
- item pickups
- player inventory
- inventory UI renamed to `InventoryBar`
- pickup persistence behavior now owned by `GameState`

### Milestone v0.6 — Use item on hotspot/NPC

Goal:

```txt
Selected inventory item can be used on an object or NPC.
```

Delivered:

- item selection and deselection
- item-use rules
- success/failure/completed outcomes
- optional item consumption
- result-item rewards
- state-dependent NPC/hotspot content

### Milestone v0.7 — Item combining

Goal:

```txt
Two inventory items can combine into a new item.
```

Delivered:

- order-independent recipe system
- Empty Cup -> Old Well = Cup of Water
- Cup of Water + Moon Herb = Glowing Tea
- inventory-combination operation extracted from `AdventureScene`
- atomic recipe transaction tests

### Milestone v0.8 — Quest flags

Goal:

```txt
Game can track progress through flags.
```

Delivered:

- progression flags
- flag-reactive NPC dialogue and hotspot text
- locked tower exit
- demo completion flag
- content validation

### Milestone v0.8.1 — Refactor and regression hardening

Goal:

```txt
Protect behavior and separate runtime state, rules, and presentation before adding final demo content.
```

Delivered:

- hotspot inspection regression fix
- behavior and integration coverage
- Python content validation
- persistent world state in `GameState`
- stateless item-use definitions
- recipe execution extracted from `AdventureScene`
- `AdventureInteractionService`
- unified target resolution for click and hover
- shared UI helpers for text wrapping and inventory layout
- documentation/scaffolding cleanup

### Milestone v0.9 — First complete demo

Goal:

```txt
Playable beginning-to-end mini adventure with the intended key-based tower puzzle.
```

Delivered flow:

```txt
Empty Cup -> Old Well -> Cup of Water
Cup of Water + Moon Herb -> Glowing Tea
Glowing Tea -> Retired Witch -> Rusty Key
Rusty Key -> Tower Gate -> tower opens
Enter Tower -> demo ending
```

Delivered features:

- Cup of Water item
- Rusty Key item
- Old Well fills Empty Cup
- recipe uses Cup of Water + Moon Herb
- witch gives Rusty Key instead of unlocking tower directly
- tower gate unlocks with Rusty Key
- `TOWER_UNLOCKED` remains the semantic world fact after key use
- full demo-flow integration test protects the route

## Milestone v0.9.1 — Post-demo foundation

Goal:

```txt
Clean up architecture after the complete demo proves the gameplay shape.
```

Delivered:

- deterministic `N = New Game` behavior through fresh `GameSession` construction
- reusable `GameContent` separated from current-session `GameState`
- explicit session scene ownership
- serialization-ready plain-data snapshots with version and stable-ID validation
- JSON-backed item and recipe definitions converted into typed domain objects
- documented decision to keep scenes and dialogue in Python until the dialogue-choice milestone proves the schema
- shared cached fonts and future asset lookup boundaries in `UIResources`
- unit, integration, and Pygame-adapter test coverage for the new boundaries

Snapshot fields:

```txt
save_version
current_scene_id
inventory_item_ids
selected_item_id
flags
collected_pickup_ids
completed_interaction_ids
ending_reached
```

Content-format decision:

```txt
Items:     JSON
Recipes:   JSON
Scenes:    Python factories
Dialogue:  Python factories
```

Revisit dialogue JSON after v0.13 dialogue choices. Consider full-scene data only after a larger-scene pilot proves that its schema is clearer than Python factories.

## Milestone v0.9.2 — Post-refactor cleanup

Goal:

```txt
Remove obsolete construction paths and align documentation without changing gameplay.
```

Scope:

- remove obsolete demo-only session and scene construction wrappers
- keep one authoritative `GameContent` session-construction path
- update affected tests without moving unrelated test files
- document the current scene lifecycle and test-layer responsibilities
- replace historical refactor task logs with a future-only refactor backlog
- remove stale temporary documentation
- apply configured formatting and rerun all automated checks

Not in scope:

- gameplay changes
- save-file UI or persistence
- new content
- scene or dialogue JSON
- new architecture abstractions

## Milestone v0.10 — Polish and presentation pass

Status: implementation complete; release verification pending

Goal:

```txt
Make the complete demo nicer to play without expanding scope.
```

Implemented:

- title screen with Start Game / Quit
- ending overlay with Play Again / Quit
- clearer hover action panels and selected-item prompts
- replaceable PNG background, object, item, NPC, and exit placeholders
- optional Ogg sound effects for pickup, dialogue, unlock, and scene transition
- improved dialogue and message-box spacing
- README setup, controls, and demo instructions
- focused asset requirements in `docs/asset-guide.md`

Tests/checks:

- title/new-game flow works
- ending can return to a fresh game or quit
- keyboard and mouse menu input works
- full demo-flow integration remains unchanged
- missing optional assets fail safely
- manual visual/readability checklist updated

Intentionally avoided:

- new quest chains
- save menu
- complex animation system
- music/channel management
- resizable-window layout
- asset manifest, atlas, or pipeline larger than the current need

## Long-term direction

The project is intended to grow into a humorous, authored 2D point-and-click adventure inspired by the interaction feel of games such as *Polda*. It should emphasize dialogue, observation, inventory puzzles, memorable characters, and clear player feedback rather than combat or general RPG systems.

This is a design direction, not a requirement to copy another game's story, assets, interface, or exact controls. Interaction details that affect player behavior must be decided during the milestone that proves them.

Supporting design principles are documented in `docs/game-vision.md`.

## Milestone planning rule

Feature milestones prove player behavior. A focused `.1` milestone follows when the feature creates clear refactor pressure.

```txt
feature milestone -> behavior tests -> focused refactor/hardening -> document stable decision
```

A `.1` milestone must not become an unrelated architecture rewrite. It should preserve gameplay and remove only duplication, unclear ownership, or fragile boundaries exposed by the preceding feature.

## Milestone v0.11 — Display and controls foundation

Goal:

```txt
Support fullscreen and multiple window sizes without changing logical scene coordinates or breaking mouse interaction.
```

Implemented scope:

- keep `1280 x 720` as the logical game resolution
- start in fullscreen desktop mode on every launch
- support the approved `1280 x 720`, `1600 x 900`, and `1920 x 1080` windowed presets
- render the game to a logical surface before presenting it to the physical window
- scale uniformly with letterboxing or pillarboxing rather than stretching
- convert physical mouse positions back into logical coordinates before hit testing
- use `F11` to toggle between fullscreen desktop and the last windowed preset used during the current session
- use `1280 x 720` as the initial windowed fallback when no preset has yet been used
- introduce semantic input actions for gameplay and menus
- add a read-only Controls screen reachable from the title menu
- derive displayed control labels from the same binding definitions used by input handling
- preserve the complete demo flow and current presentation

Tests/checks:

- logical drawing remains `1280 x 720`
- every fresh application launch starts in fullscreen desktop mode
- all three approved windowed presets work
- `F11` uses `1280 x 720` as the initial windowed fallback
- `F11` later returns to the last windowed preset used during the current session
- display choices are not persisted between application launches
- mouse hit testing works at every supported output size
- letterbox areas do not activate game targets
- fullscreen/windowed switching preserves the active session
- title and ending menus work after display-mode changes
- Controls screen matches actual bindings
- complete demo-flow integration remains unchanged

Confirmed display decisions:

- logical render resolution is `1280 x 720`
- startup mode is fullscreen desktop
- approved windowed presets are `1280 x 720`, `1600 x 900`, and `1920 x 1080`
- arbitrary drag-resizing is deferred; v0.11 uses approved presets only
- `F11` toggles fullscreen
- returning to windowed mode uses the last preset selected during the current session
- the initial windowed fallback is `1280 x 720`
- display settings do not persist between launches during v0.11
- persistent display settings and possible arbitrary drag-resizing are reconsidered in v0.19

Detailed task list:

```txt
docs/milestones/v0.11-display-and-controls.md
```

Avoid:

- rewriting scene coordinates
- camera/world-space work
- editable key bindings
- arbitrary drag-resizing
- a general UI framework
- persistent display settings before v0.19

## Milestone v0.11.1 — Display/input refactor and regression hardening

Goal:

```txt
Consolidate the boundaries proven by v0.11 without changing player behavior.
```

Observed refactor focus:

- audit the existing `display.py` boundary before adding any new viewport class; geometry, presentation, display creation, and pointer conversion are already centralized
- verify the current semantic action/binding catalog and Controls labels cannot drift
- harden display-mode state preservation and failure behavior
- review whether `GameApp` remains understandable with four modes and global actions before v0.12 adds pause/save/load screens
- clarify ownership through tests and documentation before extracting classes

Decision gates during the milestone:

- Is the current function-based display boundary already coherent enough to keep?
- Does `GameApp` remain clearer with `AppMode`, or has concrete event/draw duplication appeared?
- Are any remaining changes true refactors, or only missing regression tests/documentation?
- Should the larger navigation decision wait for v0.12.1, when pause/save/load provides stronger evidence?

Detailed task list:

```txt
docs/milestones/v0.11.1-display-input-refactor.md
```

## Milestone v0.12 — Pause, save/load, and menu foundation

Goal:

```txt
Save and restore the current demo through clear player-facing menus.
```

Planned scope:

- add a pause menu
- add title-menu Continue/Load behavior when a valid save exists
- write and restore the existing plain-data snapshot format
- use an operating-system user-data location instead of the project directory
- write save files atomically
- show useful errors for missing, invalid, corrupt, or unsupported saves
- preserve current scene, inventory, selection, flags, pickups, completions, and ending state
- close transient dialogue, messages, hover, and menu selection state after load unless the milestone proves a better rule
- change unconsumed gameplay `Escape` from immediate quit to pause
- provide explicit quit and new-game confirmation where destructive behavior requires it

Tests/checks:

- fresh, mid-quest, and completed-demo save/load
- title Continue visibility follows save validity
- pause Save/Load/Resume/Quit flow works
- corrupt and unknown-version saves fail safely
- failed save writes do not destroy the last valid save
- loading creates a valid session without stale transient UI

Decision gates during the milestone:

- One manual slot, one autosave slot, or both?
- Which menu surfaces expose Save and Load?
- Does `N` remain a development shortcut, require confirmation, or disappear from release controls?
- Is a separate settings/config file needed yet?
- Should loading a completed save show the ending immediately or enter the final scene first?

Avoid:

- multiple-profile management
- cloud saves
- save thumbnails unless needed by the chosen menu
- migration infrastructure before a second supported save version exists

## Milestone v0.12.1 — Persistence/menu refactor and hardening

Goal:

```txt
Separate proven file persistence and menu responsibilities after the save/load workflow works.
```

Expected refactor focus:

- isolate filesystem access from snapshot creation and session restoration
- centralize save-path resolution and atomic writes
- evaluate a small app-screen or screen-stack boundary if title, controls, pause, save/load, ending, and confirmations make `AppMode` branching cumbersome
- keep gameplay rules independent from menu and filesystem code
- add migration handling only if more than one save version must be supported

## Milestone v0.13 — Dialogue choices

Goal:

```txt
NPC dialogue can offer small, clear choices that affect conversation or world state.
```

Planned scope:

- dialogue nodes or another small branching representation
- keyboard and mouse choice selection
- optional requirements and flag outcomes
- at least one meaningful conversation
- no arbitrary script execution

Decision gates during the milestone:

- Are unavailable choices hidden or disabled?
- Which choice outcomes are persistent?
- Are stable dialogue-node IDs required for save/load?
- Is the proven schema clearer in JSON than in Python factories?

## Milestone v0.13.1 — Dialogue model/content refactor

Expected refactor focus:

- separate persistent conversation facts from transient dialogue presentation where needed
- consolidate branching structures and stable IDs
- pilot dialogue JSON only if the v0.13 schema is stable and easier to author than Python

## Milestone v0.14 — Objective hints and journal

Goal:

```txt
Players can understand the current goal without external instructions.
```

Decision gates during the milestone:

- Is objective text derived from inventory/flags sufficient?
- Are stable quest-step IDs needed?
- Should completed objectives remain visible?

## Milestone v0.14.1 — Objective-state refactor

Expected refactor focus:

- separate player-facing objective wording from internal progression flags if duplication appears
- introduce explicit quest definitions only when derived objectives become unclear

## Milestone v0.15 — Interaction UX and larger-scene/camera pilot

Goal:

```txt
Prove the intended Polda-style interaction language and whether scenes need world-space camera movement.
```

Planned experiments:

- one larger representative scene
- camera offset and screen/world coordinate conversion
- direct contextual click versus separate inspect/use behavior
- optional right-click inspect pilot
- selected inventory item cursor feedback
- inventory and menus remain screen-space

Decision gates during the milestone:

- Keep direct contextual interaction or introduce distinct inspect/use actions?
- Should inventory items attach visually to the cursor?
- Are one-screen scenes sufficient for the intended game?
- Who owns camera state?

## Milestone v0.15.1 — Scene coordinate and interaction refactor

Expected refactor focus:

- formalize logical-screen, world, and camera coordinate boundaries
- centralize target resolution under the chosen interaction model
- add spatial indexing only if measured target counts justify it
- split `AdventureScene` only where the pilot proves distinct responsibilities

## Milestone v0.16 — Visible player movement pilot

Goal:

```txt
Determine whether visible move-then-interact behavior improves the adventure feel.
```

Decision gates during the milestone:

- Keep instant interactions or require movement into range?
- Are simple walk areas sufficient?
- Is pathfinding necessary for authored scenes?
- How should movement interact with dialogue and scene transitions?

## Milestone v0.16.1 — Movement/runtime entity refactor

Expected refactor focus:

- separate content definitions, runtime state, and Pygame views only where movement/animation requires it
- isolate movement and interaction sequencing
- avoid an entity-component system unless a concrete need appears

## Milestone v0.17 — Production assets, inventory scalability, and content pilot

Goal:

```txt
Prove a coherent production-art workflow and a content structure that can support a larger chapter.
```

Planned scope:

- production-quality scene and character asset pilot
- inventory icons and fixed-size grid or scrolling behavior
- item examination presentation
- asset credits and license tracking
- one representative data-driven scene experiment only if Python factories have become a bottleneck
- localization-ready handling for growing player-facing text where practical

Decision gates during the milestone:

- Is an asset manifest justified?
- Which assets are shared, scene-owned, preloaded, or releasable?
- Should rectangle fallbacks remain in tests/debug builds?
- Is scene JSON clearer than the equivalent Python factory?
- Is inventory paging or scrolling the better interaction?

## Milestone v0.17.1 — Resource/content refactor

Expected refactor focus:

- resolve assets relative to the installed package/application
- split image, audio, and path responsibilities only if `UIResources` has become overloaded
- add bounded scaled-image caching or scene resource release only if measured memory use requires it
- centralize asset validation and manifest data if approved
- separate static definitions, runtime state, and views where production entities require it

## Milestone v0.18 — Music, ambience, and audio settings

Goal:

```txt
Add controlled scene audio without turning short sound-effect loading into a general media engine.
```

Decision gates during the milestone:

- Which scene lifecycle events start and stop music/ambience?
- Which channels and volume groups are needed?
- How should transitions fade or crossfade?

## Milestone v0.18.1 — Audio/lifecycle refactor

Expected refactor focus:

- separate short effects, streaming music, and ambience ownership
- introduce explicit scene enter/exit hooks only when proven necessary
- centralize master/music/SFX volume behavior

## Milestone v0.19 — Packaging, settings, and user-data hardening

Goal:

```txt
Run as an installable game with reliable asset, save, configuration, and diagnostic paths.
```

Planned scope:

- executable/package build
- platform user-data and config paths
- persist the selected fullscreen/windowed mode and last approved windowed preset
- persist audio and other approved user settings separately from game-save data
- evaluate whether arbitrary drag-resizing is useful beyond the approved 16:9 presets
- if drag-resizing is approved, add aspect-preserving live resizing, minimum-size behavior, and reliable pointer conversion
- logging and useful crash diagnostics
- asset license/credit output
- localization-readiness review

Decision gates during the milestone:

- Should the game continue to launch with the saved display mode, or provide a safe startup override?
- Are the approved windowed presets sufficient for the target players and platforms?
- If arbitrary drag-resizing is added, what minimum physical window size preserves readable text and usable controls?
- Which display, audio, text, language, and accessibility settings belong in the first persisted configuration schema?

## Milestone v0.19.1 — Release architecture hardening

Expected refactor focus:

- centralize application paths and configuration loading
- remove development-working-directory assumptions
- validate packaged resources and release startup behavior

## Milestone v0.20 — First larger chapter production pilot

Goal:

```txt
Build enough connected content to test whether authoring and runtime systems scale beyond the original demo.
```

Decision gates during the milestone:

- Are Python scene factories still efficient to author and review?
- Is content validation sufficient for the larger chapter?
- Is lightweight tooling needed?
- Which systems are genuinely reusable and which remain game-specific?

## Milestone v0.20.1 — Content-authoring refactor

Expected refactor focus:

- remove authoring duplication exposed by the chapter pilot
- add focused loaders or tools only for proven content bottlenecks
- avoid a general editor or scripting language unless chapter production clearly requires one

## Deferred candidates

Potential future work:

```txt
optional side quests
additional puzzle abilities
accessibility features beyond the initial settings baseline
content editor or modding research
combat research only if the game's final design genuinely requires it
```

Do not schedule combat, RPG progression, a generic engine framework, or a universal content editor while the authored point-and-click loop still has higher-priority needs.
