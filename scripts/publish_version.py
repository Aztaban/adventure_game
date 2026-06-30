#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"

VERSION_RE = re.compile(r'(?m)^version\s*=\s*"(\d+\.\d+\.\d+)"\s*$')
TODO_TEXT = "TODO: describe changes."
ALLOWED_RELEASE_FILES = {"pyproject.toml", "CHANGELOG.md"}


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def get_current_version() -> str:
    if not PYPROJECT.exists():
        raise FileNotFoundError("pyproject.toml not found.")

    content = PYPROJECT.read_text(encoding="utf-8")
    match = VERSION_RE.search(content)

    if not match:
        raise ValueError('Could not find version = "X.Y.Z" in pyproject.toml.')

    return match.group(1)


def get_changelog_content() -> str:
    if not CHANGELOG.exists():
        raise FileNotFoundError("CHANGELOG.md not found.")
    return CHANGELOG.read_text(encoding="utf-8")


def ensure_changelog_ready(version: str) -> None:
    content = get_changelog_content()
    heading = f"## {version}"

    if heading not in content:
        raise RuntimeError(f"CHANGELOG.md does not contain section: {heading}")

    section_start = content.index(heading)
    next_section = content.find("\n## ", section_start + 1)

    if next_section == -1:
        section = content[section_start:]
    else:
        section = content[section_start:next_section]

    if TODO_TEXT in section:
        raise RuntimeError(
            f"CHANGELOG.md for version {version} still contains TODO text."
        )


def get_changed_files() -> set[str]:
    result = run_git(["status", "--porcelain"])
    changed: set[str] = set()

    for line in result.stdout.splitlines():
        if not line:
            continue
        path = line[3:].strip()
        changed.add(path)

    return changed


def ensure_only_release_files_changed() -> None:
    changed = get_changed_files()

    if not changed:
        print("No uncommitted release files found. Tagging current commit.")
        return

    unexpected = changed - ALLOWED_RELEASE_FILES

    if unexpected:
        files = "\n".join(f"- {file}" for file in sorted(unexpected))
        raise RuntimeError(
            "Only pyproject.toml and CHANGELOG.md should be changed "
            "when publishing a version.\n"
            f"Unexpected changed files:\n{files}"
        )


def tag_exists(tag_name: str) -> bool:
    result = run_git(["tag", "--list", tag_name])
    return bool(result.stdout.strip())


def commit_release(version: str) -> None:
    changed = get_changed_files()

    if not changed:
        return

    run_git(["add", "pyproject.toml", "CHANGELOG.md"])
    run_git(["commit", "-m", f"chore: release v{version}"])
    print(f"Created release commit for v{version}")


def create_tag(version: str) -> None:
    tag_name = f"v{version}"

    if tag_exists(tag_name):
        raise RuntimeError(f"Git tag already exists: {tag_name}")

    run_git(["tag", "-a", tag_name, "-m", f"Release {tag_name}"])
    print(f"Created git tag: {tag_name}")


def push_release() -> None:
    run_git(["push"])
    run_git(["push", "--tags"])
    print("Pushed commit and tags.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish current project version.")
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push release commit and tags to remote.",
    )

    args = parser.parse_args()

    version = get_current_version()
    print(f"Publishing version: {version}")

    ensure_changelog_ready(version)
    ensure_only_release_files_changed()
    commit_release(version)
    create_tag(version)

    if args.push:
        push_release()
    else:
        print("Release created locally. Push with: git push && git push --tags")


if __name__ == "__main__":
    main()
