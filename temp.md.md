## 0.11.1 - Unreleased

### Fixed

- Consolidated logical drawing, physical presentation, destination-rectangle ownership, and pointer conversion in one `DisplayViewport` boundary.
- Removed duplicate viewport calculations so presentation and hit testing use the same stored geometry.
- Avoided unnecessary display recreation when the requested windowed mode is already active.
- Presented a complete current frame immediately after successful display creation or mode switching to reduce avoidable intermediate-frame flicker.
- Kept failed display recreation non-destructive to the active display, application mode, and gameplay session.
- Replaced drifting runtime key and mouse hints with labels derived from the authoritative semantic binding catalog.

### Tests

- Added regression coverage for stateful viewport geometry across approved, letterboxed, and pillarboxed outputs.
- Added coverage proving every displayed physical trigger activates its catalog action.
- Hardened tests for no-op display requests, immediate post-change drawing, pointer rejection, repeated mode switching, and preservation of scene, dialogue, inventory selection, and application mode.