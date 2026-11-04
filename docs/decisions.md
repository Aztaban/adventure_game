# Decisions and open questions

Revision: 2026-11-04. Confirmed product choices come from the project owner.
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

## Proposed defaults to resolve at the relevant milestone

| ID | Question | Recommendation | Needed before |
| --- | --- | --- | --- |
| OPEN-01 | Does the OS close button confirm during gameplay/pause, and what about title/ending? | Reuse the exit confirmation during an active unfinished session; exit directly from title/ending. | v0.12 exit wiring |
| OPEN-02 | May an unsupported-version save be overwritten like other invalid files? | Warn explicitly before replacing an unsupported save; keep no-confirm replacement for missing/corrupt files if desired. This changes the old blanket invalid-file policy and requires a decision. | v0.12 save wiring |
| OPEN-03 | Floor/obstacle representation and routing method? | Small authored floor region plus obstacles and a bounded route solution that proves one detour; no new library by default. | v0.13 navigation |
| OPEN-04 | Click outside walkable ground or an unreachable target? | Reject with clear feedback; do not teleport or interact remotely. | v0.13/v0.14 |
| OPEN-05 | How do manual input, new clicks, pause, and selection changes cancel movement? | Arrow input replaces automatic travel; new world click replaces destination; pause/dialogue clear travel and queued interaction; changing item selection cancels queued item use. | v0.13/v0.14 |
| OPEN-06 | Inspect behavior and keyboard-only interaction? | Contextual left-click for now; apply proximity to inspect/talk/pickup/use/exit. Right-click inspect and a nearest-target keyboard action are separate optional decisions. | v0.14 |
| OPEN-07 | What position is used when re-entering a scene? | Each exit names a safe destination entry point; initial game/legacy-save load uses a scene default spawn. | v0.14 transitions |
| OPEN-08 | What should a save made mid-walk restore? | Persist the current valid foot position and facing; load stationary with no route, held keys, or queued action. | v0.14 save schema |
| OPEN-09 | Directional art and animation timing? | Begin with four cardinal facing directions and idle/walk states; use a small frame set and time-based playback. Eight directions and interaction clips are later choices. | v0.15 art pilot |
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
through DEC-06 unless the owner changes the direction. Exact speed, radius, and
animation frame rate are tunable pilot values, not permanent promises.
