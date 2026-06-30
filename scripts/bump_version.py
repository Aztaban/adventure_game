#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
CHANGELOG = ROOT / "CHANGELOG.md"

VERSION_RE = re.compile(r'(?m)^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"\s*$')
TODO_TEXT = "TODO: describe changes."


def read_pyproject() -> str:
    if not PYPROJECT.exists():
        raise FileNotFoundError("pyproject.toml not found.")
    return PYPROJECT.read_text(encoding="utf-8")


def get_current_version(content: str) -> tuple[int, int, int]:
    match = VERSION_RE.search(content)
    if not match:
        raise ValueError('Could not find version = "X.Y.Z" in pyproject.toml.')

    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def bump_version(version: tuple[int, int, int], bump_type: str) -> tuple[int, int, int]:
    major, minor, patch = version

    if bump_type == "major":
        return major + 1, 0, 0
    if bump_type == "minor":
        return major, minor + 1, 0
    if bump_type == "patch":
        return major, minor, patch + 1

    raise ValueError(f"Unknown bump type: {bump_type}")


def version_to_str(version: tuple[int, int, int]) -> str:
    return f"{version[0]}.{version[1]}.{version[2]}"


def update_pyproject(content: str, new_version: str) -> str:
    return VERSION_RE.sub(f'version = "{new_version}"', content, count=1)


def ensure_no_unfinished_changelog() -> None:
    if not CHANGELOG.exists():
        return

    content = CHANGELOG.read_text(encoding="utf-8")
    if TODO_TEXT in content:
        raise RuntimeError(
            "CHANGELOG.md still contains TODO text. "
            "Finish the previous changelog entry before bumping again."
        )


def update_changelog(new_version: str) -> None:
    today = date.today().isoformat()

    entry = (
        f"\n## {new_version} - {today}\n\n"
        "### Added\n"
        f"- {TODO_TEXT}\n"
    )

    if not CHANGELOG.exists():
        CHANGELOG.write_text("# Changelog\n" + entry, encoding="utf-8")
        return

    content = CHANGELOG.read_text(encoding="utf-8")

    if content.startswith("# Changelog"):
        lines = content.splitlines()
        updated = (
            "\n".join(lines[:1])
            + "\n"
            + entry
            + "\n"
            + "\n".join(lines[1:]).lstrip()
        )
    else:
        updated = "# Changelog\n" + entry + "\n" + content

    CHANGELOG.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump project version.")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Version part to bump.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the new version without modifying files.",
    )

    args = parser.parse_args()

    content = read_pyproject()
    current_version = get_current_version(content)
    new_version = bump_version(current_version, args.bump_type)

    current = version_to_str(current_version)
    new = version_to_str(new_version)

    print(f"Current version: {current}")
    print(f"New version:     {new}")

    if args.dry_run:
        return

    ensure_no_unfinished_changelog()

    PYPROJECT.write_text(update_pyproject(content, new), encoding="utf-8")
    update_changelog(new)

    print("Updated pyproject.toml")
    print("Updated CHANGELOG.md")
    print("Now edit CHANGELOG.md, then run: make publish-version")


if __name__ == "__main__":
    main()
