"""Prepare or validate the two generated version files against the PR's base."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = re.compile(r"^(feat|fix|perf|refactor|docs|test|build|ci|chore|style|revert)(?:\([^()\n]+\))?(!)?: (\S.*)$")
VERSION = re.compile(r'(?m)^version\s*=\s*"\d+\.\d+\.\d+"[ \t]*$')


def bump(version: str, title: str) -> str:
    match = TITLE.fullmatch(title)
    if match is None:
        raise ValueError("Use a Conventional Commit PR title, e.g. fix: repair loading or feat: add pause menu.")
    major, minor, patch = map(int, version.split("."))
    if match[2]:
        return f"{major + 1}.0.0"
    if match[1] == "feat":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def generated_files(base_project: str, base_log: str, title: str, number: int) -> tuple[str, str]:
    version = bump(tomllib.loads(base_project)["project"]["version"], title)
    project, count = VERSION.subn(f'version = "{version}"', base_project)
    if count != 1:
        raise ValueError("Expected exactly one static project version in pyproject.toml.")
    if not base_log.startswith("# Changelog\n"):
        raise ValueError("Expected '# Changelog' heading.")
    # Dates are deliberately omitted: a PR creation/run date is not its merge or release date.
    entry = f"## {version}\n\n- {title} (#{number})\n\n"
    changelog = "# Changelog\n\n" + entry + base_log[len("# Changelog\n") :].lstrip("\n")
    return project, changelog


def prepare(base: str, title: str, number: int, check: bool) -> None:
    def read_base(name: str) -> str:
        return subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=ROOT, text=True)

    base_project = read_base("pyproject.toml")
    base_log = read_base("CHANGELOG.md")
    expected_project, expected_log = generated_files(base_project, base_log, title, number)
    # Preserve intentional dependency/tool edits; only the version field is generated.
    current_project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    version = tomllib.loads(expected_project)["project"]["version"]
    new_project, count = VERSION.subn(f'version = "{version}"', current_project)
    if count != 1:
        raise ValueError("Expected exactly one static project version.")
    files = {"pyproject.toml": new_project, "CHANGELOG.md": expected_log}
    for name, content in files.items():
        path = ROOT / name
        if check:
            if path.read_text(encoding="utf-8") != content:
                raise ValueError(f"{name} is stale. Wait for Prepare PR version, then update from main if needed.")
        else:
            path.write_text(content, encoding="utf-8")
    print(f"{'Validated' if check else 'Prepared'} v{version} for PR #{number}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--title", help="PR title, for manual preparation (e.g. fork PRs).")
    parser.add_argument("--number", type=int, help="Real PR number, paired with --title.")
    args = parser.parse_args()
    if args.title is not None and args.number is not None:
        prepare(args.base, args.title, args.number, args.check)
        return
    metadata_path = os.environ.get("PR_METADATA_PATH")
    if metadata_path:
        pr = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
        if pr["state"] != "open" or pr["base"]["ref"] != "main":
            raise ValueError("This PR is no longer open against main.")
    else:
        event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        pr = event["pull_request"]
    prepare(args.base, pr["title"], int(pr["number"]), args.check)


if __name__ == "__main__":
    main()
