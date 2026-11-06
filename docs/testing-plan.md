# Testing guide

## Purpose and ownership

Protect observable gameplay with automated tests and use desktop testing for visual,
input-feel, window-manager, and audio behavior. Detailed execution checklists,
per-commit results, blockers, and acceptance status belong to GitHub issues/PRs.
This file holds reusable test strategy and contracts, not a second task tracker.

The supplied archive includes v0.12 persistence foundations but not finished menus.
The reported main CI result was 304 passing real-Pygame tests for that run. Do not
claim it verifies a different commit, unfinished movement, or desktop behavior.

## Commands and CI

```bash
make setup
make format
make check
```

`make format` changes files; `make check` runs configured Ruff lint and pytest.
For a non-mutating format check use `.venv/bin/python -m ruff format --check src tests`.
Run a focused test with `.venv/bin/python -m pytest tests/test_inventory.py`.
CI installs declared dependencies and runs format check, lint, and `pytest -q` using
real Pygame with headless SDL drivers. Quiet output still shows failures and traces.
Record the actual tested commit and latest result in the issue/PR.

## Test layers

| Layer | Use |
| --- | --- |
| Pure unit | Inventory/recipes/item use, flags, snapshot validation, paths/envelopes/I/O, geometry, movement stepping, animation timing |
| Integration | Real content/puzzle, new-session isolation, save round trips, application commands, approach/arrival and scene transitions |
| Pygame adapter | Event/held-input translation, UI priority, hit tests, drawing boundaries, logical/physical conversion |
| Desktop | Feel, readable targets/layout, fullscreen transitions, art/animation overlap, sound |

Choose the lowest layer that proves behavior. Keep pure transaction tests even when
the player-input adapter adds proximity. Use deterministic time inputs and temporary
save paths; do not depend on wall-clock sleeps, a real user-data directory, or a
compatibility shim to claim actual Pygame acceptance.

## Existing contracts to preserve

- Original cup/well/herb/tea/witch/key/gate puzzle and fresh session isolation.
- Inventory/recipe mutations are validated atomically; one-time pickups/interactions
  and semantic flags survive scene recreation and snapshot round trips.
- Item/recipe JSON has type/reference/duplicate validation; scene/dialogue Python
  factories remain authoritative until a deliberate format change.
- All world/UI drawing uses one 1280 x 720 logical surface; DisplayViewport owns
  uniform presentation, pointer conversion, and letterbox rejection.
- Shared input labels and accepted bindings agree. UI/modal input wins over world input.
- Missing optional art/audio has safe fallbacks; unavailable audio does not break gameplay.

## v0.12 persistence/menu contracts

Validate application Save through snapshot -> envelope -> path -> atomic writer, and
Load through inspection -> fresh session restoration -> commit after success. Check
fresh/mid-quest/selected-item/changed-scene/completed state. Use temporary directories
and induced write/flush/sync/replace failures to establish previous-file survival.

Validate missing/corrupt/unreadable/unsupported envelope and nested-snapshot statuses;
keep unsupported versions distinct for DEC-08 warning/confirmation. Cancelling a
replacement preserves exact existing bytes and current session. DEC-07 confirms OS
close for an unfinished active session even immediately after a save; title/ending
can exit directly. Cancel/modal/F11 behavior follows decisions.md. Remove obsolete
N/direct Escape-quit expectations only when their replacement behavior is implemented.

## Planned navigation contracts

Future coverage must prove normalized, time-based arrow movement; common footprint/
collision policy; obstacle detours; arrival tolerance; valid-position preservation;
and deterministic nearest-reachable-floor projection for outside-floor ground clicks.
Test disconnected floor areas and exclude UI/letterbox clicks before projection.

DEC-09: arrows permanently cancel click travel. DEC-11: pause/dialogue clears route
and held input; returning from pause/dialogue/Controls stays stationary until fresh
input, including when an arrow remained physically held. F11 alone preserves travel.
Check focus-loss clearing and bounded large-frame behavior without tunnelling.

## Planned approach/entrance/save contracts

All real-input talk/inspect/pickup/item-use/exit paths wait for range/reachability and
revalidate target/item/progression at arrival. Test stale/missing targets, replaced
requests, boundaries, unreachable approaches, exactly-once completion, and no early
mutation. Inventory UI remains immediate.

DEC-12: both directions of each exit use corresponding entrances once, without an
immediate bounce back; transitions can occur after update and never during drawing.
DEC-14: changing/deselecting the item during approach cancels use and stops travel;
a replacement item must not silently execute the old request.

DEC-13: mid-walk saves restore valid position/facing standing still. Clear route,
pending action, held input, and transient UI. Known version-1 snapshots preserve
scene/progress at default spawns (DEC-05); malformed current snapshots receive no
silent legacy fallback. Unknown versions fail safely. Exact fields/version are
specified during implementation before tests lock in the new schema.

## Planned animation contracts

Test actual-motion idle/walk selection, directional fallback, elapsed-time frame
advancement, stable foot anchors, deterministic ground/foreground ordering, and
missing-clip fallback. Cosmetic loops cannot mutate puzzle facts or own interaction
success. Define pause/load/reset/scene-entry clock behavior in the animation issue;
frame clocks and routes do not belong in saved progress.

## Desktop acceptance

Issue checklists should cover the actual feature: complete the puzzle, save/load,
controls/modal transitions, invalid input/files, scaled/fullscreen pointer alignment,
focus loss, readable UI/targets, grounded path/occlusion, stride/speed, ambient
subtlety, and audio quality. Record OS/output configuration and tested commit.
Passing headless CI never closes a desktop issue whose required checks remain open.

## Confirmed four-direction and pause-freeze contracts

DEC-15: up/down/left/right idle/walk presentations exist, or follow the explicitly
chosen visible fallback policy. Diagonal travel maps deterministically to a cardinal
facing, including ties and stops, while retaining normalized movement speed.

DEC-16: record player/ambient phase on pause entry and assert it does not advance
across repeated paused updates or Controls reached through pause. Exclude paused
elapsed time; ambient clips resume without fast-forwarding. On resume the player
selects its true stationary state under DEC-11, never restarting a cancelled route.
Keep numeric phase/state tests deterministic. Desktop acceptance checks foot sliding,
anchor jitter, foreground overlap, readability, and ambient subtlety separately.
