# Refactor Backlog

Status: planning revision 2026-11-04; v0.12 implemented through D120-06 in supplied archive.

## Rules

Keep pending, evidence-gated work here. Do not turn every future audit into a
mandatory implementation or release. Completed changes belong in release history;
stable facts belong in architecture. Once tasks migrate to GitHub, issues own their
execution status and this file links only the relevant scope/decision.

Preserve gameplay, tests, and declared save compatibility. Prefer observed pressure
over named patterns. Do not add dependencies or materially change behavior without
the corresponding approved milestone/decision.

## v0.12.1 — Persistence and menu audit

After v0.12 acceptance, trace Save/Load, menu results, confirmations, errors, and
session replacement. Extract only duplicated/unclear ownership. Keep file I/O out
of gameplay and widgets; keep the snapshot/envelope/path boundaries; keep AppMode
if clearer than a stack. No migration/repository framework or extra slots.
See [task plan](milestones/v0.12.1-persistence-menu-refactor.md).

## Navigation audit after v0.13 (optional v0.13.1)

- Confirm held-input translation, movement stepping, walkability, and route planning
  have clear owners and one collision policy.
- Split pure geometry from Pygame only where testability or duplication warrants it.
- Do not introduce a camera/ECS/navigation service framework without need.

## Interaction and snapshot audit after v0.14 (optional v0.14.1)

- Check one range/arrival gate covers every player-facing world action.
- Check delayed transitions share one event/update result path.
- Check safe spawn/entry ownership and stale pending-action cancellation.
- Keep legacy snapshot-v1 loading narrowly defined and independently tested.
- Consolidate target identity/range rules only where the full demo exposes duplication.

## Animation audit after v0.15 (optional v0.15.1)

- Check frame timing, facing selection, foot anchors, and layer ordering.
- Keep cosmetic clocks separate from progression and persistence.
- Split animation/resource loading only if a representative asset set demonstrates need.

## Later evidence-gated reviews

| Feature | Possible audit pressure |
| --- | --- |
| v0.16 dialogue choices | Stable node/outcome IDs; persistent facts versus transient presentation; JSON only if clearer |
| v0.17 objectives | Wording ownership; derived facts versus explicit quest steps |
| v0.18 presentation/content | Asset roots/cache lifetime, inventory layout, audio channels/lifecycle, credits, optional scene-data pilot |
| v0.19 packaging/settings | Resource/save/config/log paths, safe startup, diagnostics, packaged dependency/content inclusion |
| v0.20 chapter production | Measured authoring duplication and focused tooling |

Camera/larger-scene coordinates need a separate pilot only when approved. Existing
single-screen logical geometry remains the baseline. Do not build a universal event
bus, ECS, service locator, widget inheritance tree, scripting system, database,
general editor, or modding platform without concrete game evidence.
