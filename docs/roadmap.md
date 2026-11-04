# Roadmap

Status: planning revision 2026-11-04; supplied v0.12 branch implemented through D120-06; branch CI and desktop acceptance pending

## Development principle

Each milestone should be small, testable, and playable.

Do not implement future systems before the current gameplay need exists.

Prefer this order:

```txt
prove gameplay -> protect with tests -> refactor boundary -> document decision
```

## Historical delivered milestones

These entries record delivered implementations. They do not certify outstanding
desktop acceptance or verification for later branch changes.

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

Revisit dialogue JSON after the rescheduled v0.16 dialogue-choice pilot. Consider full-scene data only after a larger-scene pilot proves that its schema is clearer than Python factories.

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

Status: implemented in the supplied branch; desktop acceptance remains distinct from code delivery.

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

Status: display/input implementation is present, including DisplayViewport and
catalog-derived runtime hints. The audit questions below describe the original
scope, not unanswered instructions to repeat it. Desktop transition acceptance and
documentation reconciliation remain open; preserve historical evidence in the task log.

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

Status: in progress; D120-01 through D120-06 have recorded decisions/implementation.
Pause, confirmations, player-facing load/continue, and full acceptance remain open.
The supplied archive has no new GitHub workflows; incorporate main and obtain fresh
branch-specific CI results before continuing. The reported 304-test main run is not
evidence that this feature branch passes.

Goal:

```txt
Save and restore the current demo through clear player-facing menus.
```

Confirmed player behavior:

- use one manual save slot during v0.12
- defer autosave until a larger content milestone provides meaningful authored checkpoints
- title menu: New Game, Continue when the manual save is valid, Controls, Exit
- pause menu: Resume, Save Game, Load Game, Controls, Return to Title, Exit Game
- ending menu: Title Menu and Exit Game; do not start a fresh game directly from the ending
- remove the global `N` new-game shortcut and its Controls-screen entry
- `Escape` never quits the application directly
- gameplay `Escape` closes dialogue first, clears inventory selection next, and otherwise opens pause
- paused `Escape` resumes gameplay; Controls and confirmation dialogs keep their local Back/Cancel behavior
- keep `F11` global without closing menus, confirmations, dialogue, or changing gameplay state
- New Game does not delete the existing manual save
- restore a completed save directly into the ending presentation over its restored final scene
- restore persistent snapshot facts and clear transient dialogue, messages, hover, menu selection, pause, and confirmation state
- keep settings/configuration persistence separate and deferred

Persistence scope:

- store the manual save in an operating-system user-data directory resolved with `platformdirs`
- keep filesystem paths out of menus, `GameState`, and gameplay rules
- wrap the existing plain-data snapshot in a versioned save-file envelope
- write UTF-8 JSON atomically through a temporary file in the same directory and `os.replace()`
- preserve the last valid save when a new write fails
- distinguish missing, invalid JSON, invalid shape, unsupported version, invalid snapshot, unreadable, and write-failure cases clearly
- do not add migration infrastructure before a second save-file version exists

Confirmation behavior:

- confirm overwriting an existing valid manual save
- confirm replacing the active session when loading from pause
- confirm Return to Title and Exit Game from pause
- title New Game requires no confirmation because it starts from a non-playing surface and leaves the manual save intact
- ending Title Menu and Exit Game are direct actions after completion

Tests/checks:

- fresh, mid-quest, and completed-demo save/load
- title Continue visibility follows actual save validity
- missing, corrupt, unsupported, and invalid-snapshot saves fail safely
- pause Resume/Save/Load/Controls/Return to Title/Exit flow
- overwrite, load, return-to-title, and exit confirmations are modal
- failed save writes do not destroy the last valid save
- failed loads do not replace the active session
- loading creates a fresh valid session without stale transient UI
- loading preserves scene, inventory, selection, flags, pickups, completed interactions, and ending state
- `N` is no longer accepted or displayed
- unconsumed `Escape` pauses/resumes and never exits directly
- full demo-flow integration remains unchanged

Remaining decision checkpoints during the milestone:

- save identity and Load availability were already decided in D120-01; retain them
- resolve OPEN-01 (OS close behavior) and OPEN-02 (unsupported-save overwrite) in [decisions](decisions.md)
- decide the exact player-facing wording for save/load errors and confirmation prompts
- decide the smallest change needed for dynamic title/pause/ending menu options without introducing a general screen framework

Detailed task list:

```txt
docs/milestones/v0.12-pause-save-load.md
```

Avoid:

- autosave before authored checkpoint behavior exists
- multiple slots or profile management
- cloud saves
- save thumbnails
- settings/configuration persistence
- save migration machinery before version 2 exists
- a repository abstraction for one local slot
- a general screen framework during the feature milestone

## Milestone v0.12.1 — Persistence/menu refactor and hardening

Goal:

```txt
Audit and harden the proven save/load and menu flow without changing player behavior or save compatibility.
```

Expected audit focus:

- trace path resolution, envelope validation, atomic writing, snapshot restoration, and application-mode transitions
- verify filesystem access is isolated from snapshot creation, gameplay rules, and screen objects
- identify duplicated save-validity checks, error translation, confirmation state, or menu navigation
- evaluate whether `GameApp` remains understandable with title, Controls, gameplay, pause, ending, and confirmation behavior
- keep the current concrete-screen/AppMode design when it remains clearer than a new abstraction
- introduce a small screen contract or stack only if v0.12 creates concrete duplicated navigation/event/draw logic
- keep migrations deferred until more than one save-file version is supported

Detailed task list:

```txt
docs/milestones/v0.12.1-persistence-menu-refactor.md
```

## Revised sequence after v0.12

The owner confirmed arrow-key movement, click-to-move, approach-before-interact,
single-screen scenes first, and default-spawn loading for older supported saves.
See [decisions](decisions.md). Only future unpublished plan labels are reassigned;
existing release tags and historical task IDs are not rewritten.

| Version | Goal | Acceptance boundary |
| --- | --- | --- |
| v0.13 | Visible-player navigation pilot | One representative scene, arrow and mouse control, floor bounds, obstacle detour, predictable stopping |
| v0.14 | Approach and interact across the demo | Range-gated target actions, deferred exits, entry spawns, old-save fallback, full puzzle still completable |
| v0.15 | Player and ambient animation pilot | Directional idle/walk, foot anchoring, readable depth/occlusion, a small ambient loop |
| v0.16 | Dialogue choices | One authored branching conversation, persistent outcomes, mouse/menu-key input |
| v0.17 | Objective hints/journal | Clear current goals using existing facts before introducing quest machinery |
| v0.18 | Production presentation/content pilot | Separately scoped art, inventory, and audio experiments; do not bundle them into one large implementation task |
| v0.19 | Packaging/settings and release hardening | Chosen platform, reliable resources/user-data paths, approved persistent settings |
| v0.20 | Larger chapter production pilot | Connected authored content exposes real production bottlenecks |

v0.13-v0.15 are detailed below. Later versions are provisional planning containers,
not authorization to implement everything listed. A .1 audit may follow a feature;
it is not a mandatory release or an instruction to invent abstractions.

## Milestone v0.13 — Player navigation pilot

Goal: a visible player can walk across one authored 2D floor using held arrows or
a ground click. Choose one of the current demo scenes as the pilot.

- foot-anchored placeholder player and facing state
- continuous time-based movement with normalized diagonal speed
- one shared walkability/collision policy for keyboard and mouse travel
- a bounded route around one representative obstacle; no walking through scenery
- modal input, stopping, focus changes, and presentation-scale regression checks
- no scrolling camera, final animation art, remote interaction redesign, or broad engine framework

Details: [v0.13 task plan](milestones/v0.13-player-navigation.md).
This is an internal pilot. Legacy direct interaction and positionless saves remain
known temporary limitations until v0.14, not accepted final game behavior.

## Milestone v0.14 — Approach and interact

Goal: apply movement and proximity to the full demo without changing its puzzle.

- stable target references, approach areas, interaction distance, revalidation on arrival
- click-to-approach for talk, inspect, pickup, item use, and exits
- explicit destination-scene entry points and update-driven transition handling
- save valid position/facing, clear routes/actions on load
- support known old saves through validated default-spawn fallback; reject unknown versions
- all existing scenes remain traversable and the original puzzle still completes

Details: [v0.14 task plan](milestones/v0.14-approach-and-interact.md).
Complete gameplay interactions at the arrival boundary; later animation is presentation.

## Milestone v0.15 — Player and ambient animation pilot

Goal: make proven movement feel alive using a small original or licensed asset set.

- directional idle/walk playback tied to actual movement
- stable foot anchors, correct depth and explicit foreground layering
- one or two ambient loops with no effect on puzzle rules
- deterministic playback, pause/load/reset behavior, and fallback visuals
- no full animation editor, NPC scheduling, cinematic system, or mandatory camera

Details: [v0.15 task plan](milestones/v0.15-animation-pilot.md).

## Milestone v0.16 — Dialogue choices

Build one meaningful branching conversation before generalizing dialogue content.
Decide unavailable-choice visibility, persistent outcomes, node IDs, and save behavior.
Revisit dialogue JSON only after this pilot proves a stable schema. No arbitrary
expression evaluation or embedded scripting. Follow with a focused model audit only
if the conversation reveals duplication or unclear state ownership.

## Milestone v0.17 — Objective hints and journal

Start with objectives derived from inventory and flags. Decide whether completed
objectives remain visible and add explicit quest-step IDs only if derived state is
insufficient. Validate hints against the existing puzzle and one representative
new authored goal. A general quest engine is not a prerequisite.

## Milestone v0.18 — Production presentation and content pilot

Choose small independent deliverables rather than one feature bundle:

- coherent production art and NPC/scene asset authoring using the proven animation contract
- inventory icons/examination plus paging or scrolling only when item count requires it
- music/ambience with explicit lifetime and master/music/SFX volume decisions
- scene data pilot only if Python factories are an authoring bottleneck
- credits, asset licenses, and practical localization readiness

Audit resource caching, audio lifetime, and data boundaries only after real usage.
A manifest, atlas, streaming layer, or JSON scene format is not required by default.

## Milestone v0.19 — Packaging, settings, and release hardening

Choose the first supported desktop OS and distribution format before building.
Resolve runtime assets independently of the current working directory; centralize
resource/save/config/log/credit paths where needed. Persist approved display/audio
settings separately from gameplay saves and provide safe failure diagnostics.

A minimal playtest build may be pulled forward after v0.14/v0.15 when someone needs
it; this does not require all settings work. Do not promise cross-platform binaries
before testing them. Consider drag-resizing only if approved presets prove inadequate.

## Milestone v0.20 — Larger chapter production pilot

Add enough connected authored content to measure writing, puzzle design, scene
construction, and validation friction. Consider autosave only when authored
checkpoints exist. A content editor is an optional future response to measured
bottlenecks, not a prerequisite to building scenes. Review tooling before committing
to a game-dev-club event or an editor project; those are separate decisions.

## Deferred experiments

- larger scenes and camera movement after the one-screen interaction model works
- perspective sprite scaling, extra facing directions, interaction/cinematic animation
- autosave/checkpoint authoring and extra save slots
- optional side quests, puzzle abilities, and broader accessibility improvements
- a small content-authoring helper/editor if chapter production demonstrates need

Combat, RPG progression, 3D, procedural generation, and generic engine frameworks
remain outside the active authored-adventure plan.

## Plan-to-issue migration

Review this revision before creating more GitHub tasks. Resolve only decisions that
block the next milestone. Then create issues for coherent unfinished deliverables,
use milestones as shared finish lines, and keep small verification steps as issue
checklists. Do not migrate completed code or every hypothetical .1 refactor into
open issues. Once migrated, link actual issues from these plans and let GitHub own
execution status; these files own scope, decisions, and acceptance contracts.
