# AI Workflow

Status: planning and GitHub migration workflow revised 2026-11-04.

## Choose one deliverable

Before coding, identify the active milestone and one task or issue. Read AGENTS.md,
[roadmap](roadmap.md), [architecture](architecture.md), [coding standards](coding-standards.md),
and the relevant milestone plan. Consult [GDD](gdd.md), [content plan](content-plan.md),
and [decisions](decisions.md) when the task affects player behavior.

The confirmed movement direction supersedes older optional-movement language.
It does not authorize movement inside the unfinished v0.12 save/load task.

## Current branch baseline

The supplied v0.12 archive lacks newer main workflows and some main changelog entries.
Integrate current main deliberately, preserve feature work/history, resolve conflicts,
and establish CI on the feature branch before the next feature task. Do not overwrite
main wholesale with the uploaded ZIP or claim main's 304-pass run tested this branch.

## Planning review before issue creation

This revision precedes further GitHub migration. Resolve open decisions only when
they block upcoming work. Keep completed implementation separate from pending
verification. Do not create open issues for every completed checkbox or speculative
.1 refactor. Existing issue #4 remains a documentation-reconciliation task; do not
mark it done without its PR and checks.

After migration, use GitHub issues as execution status and these files as stable
scope/decision/acceptance references. Replace duplicate status checklists with actual
issue links once they exist; do not invent issue IDs. A Project draft card is not a
repository issue until converted. The active issue text must be supplied to an agent
that lacks authenticated GitHub access.

## Implementation loop

1. Move a well-scoped issue to Ready after its blocking decisions are resolved.
2. Move it to In Progress when implementation actually starts; use a development branch.
3. Summarize the narrow implementation and relevant tests before changing code.
4. Implement only that deliverable; avoid future systems and unrequested dependencies.
5. Run format/lint and meaningful focused/full tests with real declared dependencies.
6. Report what passed, what failed, and which desktop checks remain unavailable.
7. Open a PR describing behavior, relevant checks, and manual steps; link its issue.
8. Let development-branch formatting/CI complete; inspect the latest bot/user commit.
9. Resolve conversations, update from main as required, and merge only with required checks.
10. Close the issue only when its own acceptance is complete; retain separate desktop
    acceptance tasks when the coding task cannot establish visual/platform behavior.

`Closes #<real issue number>` in the PR description can close the linked issue on
merge. Do not close a combined coding-and-desktop issue while desktop acceptance
remains open. Configure Project status automation to reflect the chosen task boundary.

## Honest verification

Record branch/commit, command, dependencies, outcome, and manual limitations. Historical
shim-based or dependency-light tests remain historical evidence, not current real-Pygame
acceptance. Never silence failed tests merely to make CI green. Formatting does not
replace lint or pytest. Headless SDL cannot establish fullscreen transition feel or audio quality.

## Task prompt pattern

```text
Implement only task <ID or real issue number> from the active milestone.
Follow AGENTS.md and the linked design/architecture decisions.
Do not implement later milestones or add dependencies without asking.
Report changed files, behavior, verification results, and desktop checks still needed.
```

## Stop and resolve scope when

- a required product decision is still open
- unrelated rewrites or general frameworks appear
- an agent skips existing source/tests or duplicates content/state ownership
- combat, 3D, camera/editor work, extra save slots, or speculative migrations enter the task

Small change -> meaningful verification -> reviewable PR -> next deliverable.
