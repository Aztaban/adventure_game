# Development and release workflow

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
6. Open a small PR linked to the real issue, with a Conventional Commit title (see below).
   Let the bot prepare version/changelog; verify checks on the latest user/bot commit.
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

## PR versioning and changelog

`pyproject.toml` is the version source. `CHANGELOG.md` is generated history, not a
second manual task list. Each PR into `main` advances the version once. Opening or
updating a PR prepares its candidate version on that development branch; **merging
it** advances main. Unmerged candidates are not releases. A milestone can contain
several PRs and need not match the next literal version number.

Use the PR title to select the bump, based on current main:

| PR title example | Starting at 0.12.0 | Meaning |
| --- | --- | --- |
| `fix: repair save loading` | 0.12.1 | Bug fix |
| `feat: finish pause and save menus` | 0.13.0 | New feature |
| `feat!: replace the public save contract` | 1.0.0 | Explicit breaking change |
| `docs: explain controls` / `ci: improve checks` | 0.12.1 | Maintenance |

Optional scope is supported (`fix(save): ...`). Allowed types are `feat`, `fix`,
`perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `style`, and `revert`.
All except `feat` use patch; **any allowed type with `!` uses major, including
before 1.0**. This is the project's explicit policy. A milestone name, label, commit
body, or `BREAKING CHANGE` footer does not select a bump; put `!` in the PR title.
Unknown titles fail rather than guessing. Use a clear title: it becomes the generated
changelog line, including the real PR number. Prefer squash merge with that title.
Use the PR body for detail, acceptance evidence, and `Closes #<real issue>`.

Do not manually bump versions, add placeholder changelog entries, or run the retired
bump/tag scripts. The bot owns only the version field and changelog; dependency/tool
changes in pyproject remain intact. Title changes recalculate from main rather than
bumping again. If another PR merges first, **Update branch** from main, resolve any
version/changelog conflict, and let the bot regenerate. Never force-push main. Keep
main's required `Python checks` and up-to-date branch requirement enabled. A temporary
stale-version failure before the bot pushes is expected; the final commit must pass.
If a concurrent human push makes a bot push fail, rerun the failed preparation job;
it reads the current PR title and branch and never force-pushes.

Automation supports branches in this repository. Fork PRs do not receive the write
secret. Their authors can prepare manually after opening the PR, using its real number:

```bash
git fetch origin main
python scripts/pr_version.py --title "fix: repair save loading" --number 123
```

For a fork, `--base upstream/main` can select the fetched upstream remote instead.
`--check` validates without writing. Never use `pull_request_target` to execute fork code.

## Publish a playable build manually

Merging does not publish a release or create a tag. When current main is ready for a
playtest, use **Actions → Release playable builds → Run workflow → main**. Or, with
GitHub CLI installed and authenticated in the Codespace:

```bash
make release
# Equivalent, without make or a local virtual environment:
gh workflow run release.yml --ref main
```

The workflow captures main's commit at dispatch. Both Windows and Linux jobs install
real dependencies, run formatting/lint/pytest, build with PyInstaller, verify copied
assets, and launch the packaged executable headlessly from another directory. Only
after **both succeed**, publication creates `vX.Y.Z` at that captured commit and a
GitHub Release containing Windows ZIP, Linux tar.gz, and SHA256 checksums. It never
bumps the version. Release notes include **all changelog versions since the previous
published non-prerelease GitHub Release**, not just the latest PR. For the first
release, all existing changelog history is included. Existing historical tags alone
are not treated as published releases.

Both archives include Python, content JSON, images, sounds, and `PLAY.txt`. Extract
the complete archive; keep `_internal` next to the executable. Targets are x64
Windows 10/11 and Ubuntu 22.04+ with a graphical desktop; other Linux distributions
are unverified. Builds are unsigned prototype/playtest downloads. A headless startup
check does not establish desktop rendering, audio quality, or the complete puzzle:
check an extracted build on each desktop before sharing it as a validated playtest.

Publication refuses an existing release (including a draft) and never moves a tag.
If publication fails after creating a draft/tag, inspect Actions and the draft; delete
only the incomplete draft through GitHub before retrying. A tag at the exact captured
commit can be reused; a tag at another commit is an error. A successful published
release is immutable under this workflow: merge a fix and publish its new version.
Do not rerun a failed old workflow to publish a newer main; dispatch a new run.

For local packaging on either supported OS:

```bash
python -m pip install -e ".[dev,release]"
python scripts/release.py build
```

This builds only the host OS into `dist/`; it does not publish, tag, or cross-compile.
GitHub runners build each platform natively. Normal `.[dev]` installs do not need
PyInstaller. Build dependency version is pinned in the `release` extra.

## Repository setup and agent rules

- Keep `FORMATTER_TOKEN` restricted to this repository with Contents read/write.
  Formatting and PR version commits reuse it so their pushes automatically trigger
  normal CI. Renew it before expiry. Publication uses the built-in token with
  Contents write, only in the final job; no main-branch bypass is needed.
- Keep the main ruleset: PR required, zero approvals for solo work, resolved
  conversations, required `Python checks`, up-to-date branch, no deletion/force push.
  No additional required check name is needed: version validation is inside Python checks.
- Agents must choose the intended bump in the PR title, leave generated files to
  automation, preserve CI, and inspect results on the final bot commit. Never disable
  version validation, alter published history, or move existing tags to make a merge pass.
- Use GitHub Releases for download links and published notes; do not maintain another
  release-notes file or a duplicate milestone/history archive. `CHANGELOG.md` remains
  automatically generated source history.
