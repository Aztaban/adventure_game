"""Build locally, or request/publish a release of the version already on main."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = "MysteriousForest"


def run(*args: str, capture: bool = False, cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=capture)
    return result.stdout.strip() if capture else ""


def version() -> str:
    value = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("Release version must be X.Y.Z.")
    return value


def notes(changelog: str, current: str, previous: str | None) -> str:
    """Include every version since the last published release, not just the last PR."""

    def parts(value: str) -> tuple[int, ...]:
        return tuple(map(int, value.removeprefix("v").split(".")))

    if previous is not None and parts(previous) >= parts(current):
        raise ValueError("Current version must be newer than the last published release.")
    sections = re.split(r"(?m)(?=^## \d+\.\d+\.\d+(?:\s|$))", changelog)[1:]
    selected = []
    for section in sections:
        section_version = re.match(r"## (\d+\.\d+\.\d+)", section)[1]
        if parts(section_version) <= parts(current) and (previous is None or parts(section_version) > parts(previous)):
            selected.append(section.strip())
    if not selected or not selected[0].startswith(f"## {current}\n"):
        # Legacy dated entries are accepted too, e.g. 0.11.1 - 2026-08-05.
        if not selected or not re.match(rf"## {re.escape(current)}(?:\s|$)", selected[0]):
            raise ValueError("Changelog has no entry for the current version.")
    introduction = (
        "Download and extract the archive for your system, then run MysteriousForest.exe (Windows) "
        "or ./MysteriousForest (Linux). Keep the _internal folder beside the executable. "
        "Python installation is not required.\n\n"
        "Targets: Windows 10/11 x64 and Ubuntu 22.04 or newer x64 (desktop required). "
        "Other Linux distributions are not yet verified. These are prototype/playtest builds.\n\n"
    )
    return introduction + "\n\n".join(selected) + "\n"


def build() -> None:
    system = platform.system()
    if system not in {"Windows", "Linux"} or platform.machine().lower() not in {"x86_64", "amd64"}:
        raise ValueError("Build on x64 Windows or Linux; cross-compilation is unsupported.")
    bundle_version = version()
    run(
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--windowed",
        "--name",
        APP,
        "--paths",
        "src",
        "--specpath",
        "build",
        "--noupx",
        "--add-data",
        f"{ROOT / 'assets'}:assets",
        "--add-data",
        f"{ROOT / 'src/game/content/data'}:game/content/data",
        "src/main.py",
    )
    folder = ROOT / "dist" / APP
    # Compare every shipped asset to its source: optional fallback rendering must not mask missing art.
    for source in (ROOT / "assets").rglob("*"):
        if source.is_file() and source.name != ".gitkeep":
            bundled = folder / "_internal" / "assets" / source.relative_to(ROOT / "assets")
            if not bundled.is_file() or bundled.read_bytes() != source.read_bytes():
                raise ValueError(f"Bundled asset missing or changed: {source.name}")
    (folder / "PLAY.txt").write_text(
        f"Mysterious Forest v{bundle_version}\n\n"
        "Extract the complete archive before running. Keep _internal next to the executable.\n"
        "Windows: double-click MysteriousForest.exe. Linux: run ./MysteriousForest.\n"
        "F11 switches fullscreen/windowed. Controls are available from the title menu.\n"
        "Python is included. A graphical desktop and system graphics/audio libraries are required.\n"
        "Windows 10/11 x64; Ubuntu 22.04+ x64. Other Linux distributions are unverified.\n"
        "This is an unsigned prototype/playtest build.\n",
        encoding="utf-8",
    )
    (folder / "BUILD.json").write_text(
        json.dumps(
            {
                "version": bundle_version,
                "commit": run("git", "rev-parse", "HEAD", capture=True),
                "system": system,
                "architecture": "x64",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    executable = folder / (APP + (".exe" if system == "Windows" else ""))
    env = {**os.environ, "SDL_VIDEODRIVER": "dummy", "SDL_AUDIODRIVER": "dummy"}
    with tempfile.TemporaryDirectory(dir=ROOT / "build") as temporary:
        subprocess.run([str(executable), "--smoke-test"], cwd=temporary, env=env, check=True, timeout=60)
    name = f"mysterious-forest-v{bundle_version}-{system.lower()}-x64"
    archive = shutil.make_archive(
        str(ROOT / "dist" / name),
        "zip" if system == "Windows" else "gztar",
        root_dir=folder.parent,
        base_dir=folder.name,
    )
    print(f"Built and smoke-tested: {archive}")


def publish() -> None:
    """Called only after both native builds pass; never move a tag or replace a release."""
    current = version()
    tag = f"v{current}"
    sha = run("git", "rev-parse", "HEAD", capture=True)
    repo = os.environ["GITHUB_REPOSITORY"]
    # A failed/partial previous publication must be inspected explicitly, never silently overwritten.
    releases = json.loads(
        run("gh", "api", f"repos/{repo}/releases?per_page=100", "--paginate", "--slurp", capture=True)
    )
    releases = [release for page in releases for release in page]
    if any(release["tag_name"] == tag for release in releases):
        raise ValueError(f"Release {tag} already exists (possibly a draft). Inspect it before retrying.")
    published = [release for release in releases if not release["draft"] and not release["prerelease"]]
    previous = max(published, key=lambda release: release["published_at"])["tag_name"] if published else None
    release_notes = notes((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), current, previous)
    artifacts = ROOT / "release-artifacts"
    expected = [
        artifacts / f"mysterious-forest-{tag}-{target}-x64{extension}"
        for target, extension in [("windows", ".zip"), ("linux", ".tar.gz")]
    ]
    for archive in expected:
        if not archive.is_file():
            raise ValueError(f"Missing platform archive: {archive.name}")
    checksums = artifacts / "SHA256SUMS.txt"
    checksums.write_text(
        "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in expected),
        encoding="utf-8",
    )
    notes_path = ROOT / "build" / "release-notes.md"
    notes_path.parent.mkdir(exist_ok=True)
    notes_path.write_text(release_notes, encoding="utf-8")
    existing = run("git", "tag", "--list", tag, capture=True)
    if existing:
        if run("git", "rev-list", "-n", "1", tag, capture=True) != sha:
            raise ValueError(f"Existing {tag} points to another commit; it will never be moved.")
    else:
        run("git", "config", "user.name", "github-actions[bot]")
        run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        run("git", "tag", "-a", tag, sha, "-m", f"Release {tag}")
        run("git", "push", "origin", f"refs/tags/{tag}")
    run(
        "gh",
        "release",
        "create",
        tag,
        *(str(path) for path in [*expected, checksums]),
        "--verify-tag",
        "--draft",
        "--title",
        f"Mysterious Forest {tag}",
        "--notes-file",
        str(notes_path),
    )
    run("gh", "release", "edit", tag, "--draft=false", "--latest")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["version", "build", "publish", "request"])
    args = parser.parse_args()
    if args.command == "version":
        print(version())
    elif args.command == "build":
        build()
    elif args.command == "publish":
        publish()
    else:
        # gh resolves this checkout's origin. Local changes/branch/version are never published.
        run("gh", "workflow", "run", "release.yml", "--ref", "main")
        print("Requested Windows and Linux builds from current remote main. Check GitHub Actions.")


if __name__ == "__main__":
    main()
