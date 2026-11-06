"""Regression checks for version policy, generated history and safe publication."""

import subprocess

import pytest

from scripts import pr_version, release


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("fix: repair a save", "0.12.1"),
        ("feat(menu): add pause", "0.13.0"),
        ("feat!: replace save format", "1.0.0"),
        ("fix(save)!: remove legacy reader", "1.0.0"),
        ("docs: explain releases", "0.12.1"),
        ("ci: improve checks", "0.12.1"),
    ],
)
def test_version_policy(title: str, expected: str) -> None:
    assert pr_version.bump("0.12.0", title) == expected


@pytest.mark.parametrize("title", ["Fix bug", "unknown: new thing", "feat: ", "feat: one\ntwo"])
def test_ambiguous_titles_are_rejected(title: str) -> None:
    with pytest.raises(ValueError, match="Conventional"):
        pr_version.bump("0.12.0", title)


def test_preparation_is_idempotent_preserves_dependencies_and_recalculates(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(pr_version, "ROOT", tmp_path)
    project = tmp_path / "pyproject.toml"
    changelog = tmp_path / "CHANGELOG.md"
    project.write_text('[project]\nname = "test"\nversion = "0.12.0"\ndependencies = []\n', encoding="utf-8")
    changelog.write_text("# Changelog\n\n## 0.12.0\n\n- Older feature.\n", encoding="utf-8")

    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True)

    git("init")
    git("add", ".")
    git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "base")
    base = git("rev-parse", "HEAD").stdout.strip()
    project.write_text(project.read_text().replace("dependencies = []", 'dependencies = ["pygame"]'))
    pr_version.prepare(base, "fix: repair save", 42, False)
    first = changelog.read_text()
    pr_version.prepare(base, "fix: repair save", 42, False)
    pr_version.prepare(base, "fix: repair save", 42, True)
    assert changelog.read_text() == first
    assert first.count("(#42)") == 1
    assert 'dependencies = ["pygame"]' in project.read_text()
    # A title change recalculates from main, never from the already incremented branch.
    pr_version.prepare(base, "feat: finish pause", 42, False)
    assert 'version = "0.13.0"' in project.read_text()
    assert "## 0.12.1" not in changelog.read_text()
    # Another merged PR updates the base. A stale generated branch must fail validation.
    project.write_text(project.read_text().replace("0.13.0", "0.12.1"))
    git("add", ".")
    git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "another PR")
    new_base = git("rev-parse", "HEAD").stdout.strip()
    with pytest.raises(ValueError, match="stale"):
        pr_version.prepare(new_base, "fix: repair save", 42, True)
    pr_version.prepare(new_base, "fix: repair save", 43, False)
    assert 'version = "0.12.2"' in project.read_text()


def test_notes_include_all_changes_since_last_published_release() -> None:
    history = "# Changelog\n\n## 0.13.1\n\n- Fix\n\n## 0.13.0\n\n- Feature\n\n## 0.12.0 - 2026-10-01\n\n- Old\n"
    result = release.notes(history, "0.13.1", "v0.12.0")
    assert "- Fix" in result
    assert "- Feature" in result
    assert "- Old" not in result
    assert "- Old" in release.notes(history, "0.13.1", None)


def test_notes_reject_republishing_or_missing_current_entry() -> None:
    with pytest.raises(ValueError, match="newer"):
        release.notes("# Changelog\n", "0.12.0", "v0.12.0")
    with pytest.raises(ValueError, match="no entry"):
        release.notes("# Changelog\n\n## 0.11.0\n\n- Old\n", "0.12.0", None)


def test_publish_never_overwrites_an_existing_release(monkeypatch) -> None:
    calls = []
    monkeypatch.setenv("GITHUB_REPOSITORY", "example/game")
    monkeypatch.setattr(release, "version", lambda: "0.12.0")

    def fake_run(*args, **kwargs):
        calls.append(args)
        return '[[{"tag_name": "v0.12.0", "draft": true}]]' if args[:2] == ("gh", "api") else "a" * 40

    monkeypatch.setattr(release, "run", fake_run)
    with pytest.raises(ValueError, match="already exists"):
        release.publish()
    assert all(call[:3] != ("gh", "release", "create") for call in calls)
    assert all(call[:2] != ("git", "tag") for call in calls)


def test_publish_refuses_to_move_tag_and_publishes_only_complete_artifacts(tmp_path, monkeypatch) -> None:
    import json

    monkeypatch.setattr(release, "ROOT", tmp_path)
    monkeypatch.setattr(release, "version", lambda: "0.12.1")
    monkeypatch.setenv("GITHUB_REPOSITORY", "example/game")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n\n## 0.12.1\n\n- Fix\n", encoding="utf-8")
    artifacts = tmp_path / "release-artifacts"
    artifacts.mkdir()
    for suffix in ["windows-x64.zip", "linux-x64.tar.gz"]:
        (artifacts / f"mysterious-forest-v0.12.1-{suffix}").write_bytes(b"test artifact")
    calls = []
    existing_tag_sha = "b" * 40

    def fake_run(*args, **kwargs):
        calls.append(args)
        if args[:2] == ("gh", "api"):
            return json.dumps([[]])
        if args[:2] == ("git", "rev-parse"):
            return "a" * 40
        if args[:3] == ("git", "tag", "--list"):
            return "v0.12.1"
        if args[:2] == ("git", "rev-list"):
            return existing_tag_sha
        return ""

    monkeypatch.setattr(release, "run", fake_run)
    with pytest.raises(ValueError, match="never be moved"):
        release.publish()
    assert all(call[:3] != ("gh", "release", "create") for call in calls)
    assert all(call[:2] != ("git", "push") for call in calls)
    existing_tag_sha = "a" * 40
    calls.clear()
    release.publish()
    create = next(call for call in calls if call[:3] == ("gh", "release", "create"))
    assert "--draft" in create and "--verify-tag" in create
    assert calls[-1] == ("gh", "release", "edit", "v0.12.1", "--draft=false", "--latest")
    assert len((artifacts / "SHA256SUMS.txt").read_text().splitlines()) == 2
    # Removing either platform blocks any publication.
    (artifacts / "mysterious-forest-v0.12.1-windows-x64.zip").unlink()
    calls.clear()
    with pytest.raises(ValueError, match="Missing platform"):
        release.publish()
    assert all(call[:2] != ("git", "push") for call in calls)
    assert all(call[:3] != ("gh", "release", "create") for call in calls)
