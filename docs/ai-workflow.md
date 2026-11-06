# AI Workflow

## Start from one GitHub issue

Read AGENTS.md, the active issue, [architecture](architecture.md), [coding standards](coding-standards.md),
and relevant [decisions](decisions.md). Use [GDD](gdd.md), [content plan](content-plan.md),
[testing guide](testing-plan.md), and [roadmap](roadmap.md) for context.
If an agent cannot access GitHub, supply the complete issue text including acceptance
criteria and dependencies. Do not reconstruct scope from a deleted milestone task file.

## Ownership

Issues own implementation checklists, status, blockers, and test evidence. GitHub
milestones group deliverables; the Project shows progress. Permanent docs hold design,
architecture, conventions, and reusable verification contracts. Git holds history.
Do not maintain parallel docs/milestones, docs/history, or refactor-backlog files.
No issue number or completed status should be invented in a documentation edit.

## Implementation loop

1. Resolve the issue's blocking product questions; verify its dependencies are complete.
2. Start a development branch and move the issue to In Progress when work actually begins.
3. Inspect current source/tests and explain the narrow change before coding.
4. Implement only that deliverable. Do not add dependencies or future systems without authorization.
5. Run meaningful focused/full checks with real declared dependencies; give desktop steps.
6. Open a small PR linked to the real issue; verify checks on the latest user/bot commit.
7. Merge through the main ruleset after required checks/conversations are satisfied.
8. Close only when that issue's acceptance is met. Keep desktop acceptance separate when needed.

## Honest verification and scope

Record tested branch/commit, commands, results, and limitations in the issue/PR.
Headless Pygame does not establish fullscreen/window-manager behavior, sound quality,
or animation feel. Main's 304-pass historical run does not verify another branch.
Older shim/dependency-light evidence remains evidence for that old environment only.
Formatting is not lint or pytest. Never hide failing checks merely to make CI green.

Before continuing an old feature branch, incorporate current main deliberately and
preserve its workflows/release history. Audit/refactor only demonstrated duplication
or unclear ownership; no generic screen/ECS/migration/navigation framework by default.

## Task prompt

```text
Implement only the supplied GitHub issue.
Follow AGENTS.md and the confirmed design decisions.
Do not implement later milestones or add unapproved dependencies.
Report behavior, changed files, verification results, and remaining desktop checks.
```
