# Decisions and open questions

Revision: 2026-11-06. Confirmed product choices come from the project owner.
Proposed defaults below guide the next review; they are not additional approvals.

## Confirmed product choices

| ID | Decision | Applies from |
| --- | --- | --- |
| DEC-01 | Original humorous 2D/2.5D adventure with a Polda-like visual feel: painted-style scenes and visible 2D characters on a floor area with depth. | Direction now; navigation in v0.13 |
| DEC-02 | Held arrow keys and mouse click-to-move are both required controls. | v0.13 |
| DEC-03 | Clicking a world target approaches it and interacts only when close enough. World item use follows the same proximity rule. | v0.14 |
| DEC-04 | Keep single-screen scenes while proving movement; a camera is deferred. | v0.13-v0.15 |
| DEC-05 | Load supported pre-movement saves at a safe default spawn for their saved scene, preserving quest/inventory progress. | v0.14 save upgrade |
| DEC-06 | Add player movement animation and ambient scene animation after navigation and interaction behavior is proven. | v0.15 |
| DEC-07 | The OS close button asks for confirmation whenever an unfinished game session is active, including pause and Controls opened from that session; title/ending exit directly. No unsaved-change tracking is needed. | v0.12 |
| DEC-08 | An unsupported-version save may be replaced only after an explicit warning and confirmation. Cancelling preserves the file and current session. | v0.12 |
| DEC-09 | Arrow input cancels automatic travel and gives keyboard control; releasing arrows never resumes the cancelled route. | v0.13 |
| DEC-10 | A ground click outside walkable floor chooses the nearest valid floor point reachable from the current player position, then walks there along a valid route. No teleporting or obstacle crossing. | v0.13 |
| DEC-11 | Opening pause or dialogue cancels automatic travel and clears held movement input. Returning from pause, dialogue, or Controls leaves the player stationary until a new movement command. | v0.13 |
| DEC-12 | Traversing an exit places the player at the corresponding destination entrance, with a safe position/facing that avoids immediately retriggering the return exit. | v0.14 |
| DEC-13 | Saving mid-walk records current position and facing; loading restores them standing still, with route and pending interaction cleared. | v0.14 |
| DEC-14 | Changing or clearing the selected inventory item while approaching a target to use it cancels the pending action and stops travel. | v0.14 |
| DEC-15 | The first player animation set supports four facing directions: up, down, left, and right. Movement may still be diagonal; diagonal art is not required. | v0.15 |
| DEC-16 | Pause freezes both player and ambient scene animation. Pause time does not advance their clocks or cause catch-up jumps on return. | v0.15 |

Polda is a genre/visual reference, not a requirement to copy its art, characters,
writing, interface, or exact mechanics. Original assets and writing remain the direction.

## Previously recorded v0.12 decisions retained

One manual slot; no autosave yet; `platformdirs` with application name
`Mysterious Forest` and `appauthor=False`; filename `save.json`; versioned JSON
save envelope and atomic replacement; title Continue only for valid saves;
Pause Load visible but disabled with a reason when unavailable; remove global N;
Escape closes dialogue, then clears inventory selection, then opens pause;
F11 remains presentation-only. Loading completed saves enters ending mode.
Settings remain separate from game saves. No general screen framework is planned.

The existing plan confirms overwrites of valid saves and loading/returning to
title/exiting from pause. Ending Title Menu and Exit are direct actions.

## Resolved v0.12 policies (2026-11-06)

The owner selected DEC-07 and DEC-08. Former OPEN-01 and OPEN-02 are resolved;
no separate decision issue is needed. Implement them in the confirmation task.

| Save state | Manual Save behavior |
| --- | --- |
| Missing | Save without overwrite confirmation. |
| Valid | Confirm replacement, as already agreed. |
| Corrupt / invalid JSON or snapshot | Retain the previously agreed no-confirmation replacement behavior; normal write failures still preserve the previous file. |
| Unsupported file or nested snapshot version | Warn explicitly and allow replacement only after confirmation. Never reinterpret a newer version as merely corrupt. |
| Unreadable existing file | Fail safely with useful feedback; do not replace a file whose status cannot be established. This is the non-destructive I/O default. |

Exit confirmation is based on an active unfinished session, not a dirty flag or
whether a manual save was just made. Cancel preserves session and prior navigation.
F11 remains presentation-only; repeated close requests must not stack dialogs.
Title and ending can exit directly. Loading from pause, returning to title, and
pause Exit retain their already agreed confirmations.

Unsupported versions can occur in the outer file envelope or nested snapshot. The
current code may group an unsupported nested snapshot under INVALID_SNAPSHOT;
preserve enough information to select the warning rather than overwriting silently.
Unknown versions still cannot be loaded. This is status classification, not migration.

## Confirmed v0.13 control behavior (2026-11-06)

DEC-09/10/11 are confirmed choices, not open questions. Implement and test them in
the navigation pilot. The nearest point is selected from floor positions reachable
from the current player position while respecting the complete actor footprint;
an isolated walkable island or the other side of an impassable obstacle is not valid.
Choose a deterministic distance/tie policy in the navigation implementation and
record it; the owner does not need to choose a pathfinding algorithm.

Destination projection applies only after a click is classified as a ground command.
UI, dialogue, menu, physical letterbox, and other non-world clicks never project into
walkable ground. Clicks on world interaction targets retain their target identity;
the approach/interaction policy is implemented separately in v0.14.

If no valid reachable destination can be determined, do not teleport or invent a
route; report a deterministic failure and keep the actor in valid space. This is
exception handling, not a return to rejecting every outside-floor ground click.

Opening pause/dialogue clears the automatic route and held directions. A key that
remains physically held across a modal transition must not restart movement on
return without fresh input. Controls reached through pause stays stationary on
return. Do not resume a cancelled route when arrows are released or a modal closes.
Do not clear travel merely for F11: presentation-only mode changes preserve it.

## Confirmed v0.14 entry, load, and item-change behavior

The owner selected DEC-12/13/14. Former OPEN-07 and OPEN-08 are resolved; the item-change
part of OPEN-05 is also resolved. These are requirements, not implementation options.

- Ordinary exit traversal uses the corresponding entrance, not a last-visit position.
- A current-format save restores its saved foot position and facing, standing still;
  it does not resume travel or an approach/interaction request.
- A supported pre-movement save retains its saved scene and progress and uses that
  scene's safe default spawn/facing (DEC-05). Default fallback is not used to hide a
  malformed current-format position.
- Changing, deselecting, consuming, or losing the selected item invalidates a queued
  item-use action: cancel the action and stop walking. No old action silently uses
  the newly selected item on arrival. Ordinary inventory combination stays immediate.

Unavailable targets cannot be interacted with remotely. Exact feedback wording,
geometry representation, routing algorithm, distance tolerance, and replacement
implementation can be chosen during the scoped task; they are not new product
choices. Add no right-click or keyboard interaction mode merely to finish v0.14.

## Confirmed v0.15 animation scope

The owner chose DEC-15/DEC-16: four directional idle/walk presentations and a full
freeze of player plus ambient scene animations while paused. Eight-direction art
is not required. The four-facing art contract does not remove diagonal arrow or
mouse movement; choose/document deterministic cardinal facing for diagonal travel.

Pause stops time accumulation, not just frame rendering. Screens opened from pause
must not secretly advance scene clips. Ambient playback resumes from its frozen
phase without applying time spent paused. On return, player animation reflects
actual motion: the route remains cancelled under DEC-11, so an interrupted walk
must not resume merely because its clip exists. No animation frame/clock enters saves.

Exact art/frame dimensions, rates, layout, diagonal tie behavior, and scene-entry
reset behavior are implementation details within this bounded pilot. Player art
may be original or appropriately licensed. Interaction clips, extra directions,
NPC schedules, cinematics, cameras, and an animation editor remain separate scope.

## Proposed defaults to resolve at the relevant milestone

| ID | Question | Recommendation | Needed before |
| --- | --- | --- | --- |
| OPEN-03 | Floor/obstacle representation and routing method? | Small authored floor region plus obstacles and a bounded route solution that proves one detour; no new library by default. | v0.13 navigation |
| OPEN-04 | What feedback/action is used for an unreachable world interaction target? | Explain that it cannot be reached and never interact remotely. DEC-10 already settles ordinary ground-click projection; it does not make every target reachable. | v0.14 |
| OPEN-05 | How should a replacement world-target request be sequenced? | Keep one pending action; replace the old request atomically and revalidate the new target. Item selection changes are already settled by DEC-14, and arrow/modal cancellation by DEC-09/DEC-11. This is an implementation detail within the one-action contract. | v0.14 implementation |
| OPEN-06 | Add right-click inspect or a keyboard-only nearest-target action? | Neither is required for v0.14. Preserve contextual left-click and apply the agreed world-action proximity rule. Extra controls need a separate future product choice. | Deferred extension |
| OPEN-09 | Exact frame/asset contract and deterministic facing/clock details? | Four directions and full pause freeze are already confirmed (DEC-15/16). Choose frame sizes/count/rate, clip layout, diagonal-to-cardinal mapping, and scene reset/re-entry rules during the scoped art/playback task. These are implementation choices; request a new product decision only if scope changes. | v0.15 implementation |
| OPEN-10 | Which platform and distribution format is first? | Choose one desktop OS before committing to an executable build. A small playtest build may precede full v0.19 packaging. | First external playtest |

## Save compatibility boundary

DEC-05 is accepted, but the upgrade mechanism is not implemented. Keep v0.12
snapshot version 1 unchanged while finishing v0.12. In v0.14, introduce an explicit
movement-aware snapshot version and a narrow reader for known snapshot version 1.
Validate old data before assigning the saved scene's default spawn and facing.
Unknown versions still fail safely. The outer save-envelope version changes only
if its own contract changes. Avoid a generic migration framework.

## Review discipline

Resolve each OPEN item before its dependent task enters Ready. Record the chosen
behavior here and in the milestone acceptance contract. Do not reopen DEC-01
through DEC-16 unless the owner changes the direction. Exact speed, radius, and
animation frame rate are tunable pilot values, not permanent promises.
